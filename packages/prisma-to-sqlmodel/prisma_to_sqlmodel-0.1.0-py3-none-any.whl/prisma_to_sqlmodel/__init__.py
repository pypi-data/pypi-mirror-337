import re
import subprocess
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
import numpy as np
from sqlalchemy import Column, Index, Text, sql, PrimaryKeyConstraint

from pgvector.sqlalchemy import Vector

class RelationInfo:
    def __init__(self, field_name: str, related_model: str, is_list: bool, fk_field: Optional[str] = None, 
                 ref_field: Optional[str] = None, ondelete: Optional[str] = None):
        self.field_name = field_name
        self.related_model = related_model
        self.is_list = is_list
        self.fk_field = fk_field
        self.ref_field = ref_field
        self.ondelete = ondelete
        self.back_populates_field = None  # Will be set when processing the other side of the relationship

class PrismaConverter:
    TYPE_MAPPING = {
        "String": "str",
        "Int": "int",
        "Float": "float",
        "Boolean": "bool",
        "DateTime": "datetime",
        "Json": "dict",
        "BigInt": "int",
        "Decimal": "float",
    }

    def __init__(self, prisma_file: str):
        self.prisma_file = Path(prisma_file)
        self.models: Dict[str, List[str]] = {}
        self.model_fields: Dict[str, Dict[str, str]] = {}  # model -> {field_name: field_type}
        self.relationships: Dict[str, Dict[str, RelationInfo]] = {}  # model -> {field_name: RelationInfo}
        self.indexes: Dict[str, List[str]] = {}  # model -> [index_fields]
        self.primary_keys: Dict[str, List[str]] = {}  # model -> [primary_key_fields]
        self.text_fields: Dict[str, List[str]] = {}  # model -> [text_field_names]
        self.updated_at_fields: Dict[str, List[str]] = {}  # model -> [updated_at_field_names]
        
    def read_prisma_schema(self) -> str:
        return self.prisma_file.read_text()
    
    def parse_models(self, content: str) -> None:
        # First pass: collect all model names
        model_pattern = r"model\s+(\w+)\s*{([^}]*)}"
        for match in re.finditer(model_pattern, content):
            model_name = match.group(1)
            self.relationships[model_name] = {}
            self.indexes[model_name] = []
            self.primary_keys[model_name] = []
            self.model_fields[model_name] = {}
            self.text_fields[model_name] = []
            self.updated_at_fields[model_name] = []
        
        # Second pass: collect fields and relationships
        for match in re.finditer(model_pattern, content):
            model_name = match.group(1)
            model_content = match.group(2)
            self._collect_fields(model_name, model_content)
        
        # Third pass: link back-populates fields
        self._link_relationships()
        
        # Final pass: generate model code
        for match in re.finditer(model_pattern, content):
            model_name = match.group(1)
            model_content = match.group(2)
            self.models[model_name] = self._parse_fields(model_name, model_content)
    
    def _link_relationships(self):
        """Link relationships between models to establish correct back_populates fields"""
        for model_name, relationships in self.relationships.items():
            for field_name, rel_info in relationships.items():
                # Find the corresponding relationship in the related model
                related_model = rel_info.related_model
                for other_field, other_rel in self.relationships[related_model].items():
                    if other_rel.related_model == model_name:
                        # We found the other side of the relationship
                        rel_info.back_populates_field = other_field
                        other_rel.back_populates_field = field_name
                        break
                
                # If no explicit back-reference was found, create an implicit one
                if not rel_info.back_populates_field:
                    # Use model name in camelCase for implicit back-references
                    implicit_name = model_name[0].lower() + model_name[1:]
                    if rel_info.is_list:
                        implicit_name += 's'  # pluralize for lists
                    rel_info.back_populates_field = implicit_name
    
    def _collect_fields(self, model_name: str, model_content: str) -> None:
        """Collect field names, types, and special attributes for a model"""
        lines = model_content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line: 
                continue
            
            # Handle model relationships and indexes
            if line.startswith('@@'):
                if '@@id' in line:
                    id_fields_match = re.search(r'@@id\(\[([^\]]+)\]\)', line)
                    if id_fields_match:
                        fields = [f.strip() for f in id_fields_match.group(1).split(',')]
                        self.primary_keys[model_name].extend(fields)
                elif '@@index' in line:
                    index_match = re.search(r'@@index\(\[([^\]]+)\]\)', line)
                    if index_match:
                        fields = [f.strip() for f in index_match.group(1).split(',')]
                        self.indexes[model_name].extend(fields)
                continue
                
            # Parse field definition
            field_match = re.match(r'(\w+)\s+(\w+)(\[\])?(\?)?(\s+@\w+)?(\([^)]*\))?(\s+@\w+\([^)]*\))?(\s+@\w+\([^)]*\))?', line)
            if field_match:
                field_name = field_match.group(1)
                field_type = field_match.group(2)
                is_list = bool(field_match.group(3))
                is_optional = bool(field_match.group(4))
                
                # Store field type
                self.model_fields[model_name][field_name] = field_type
                
                # Check for primary key
                if '@id' in line:
                    self.primary_keys[model_name].append(field_name)
                
                # Check for Text fields
                if '@db.Text' in line:
                    self.text_fields[model_name].append(field_name)
                
                # Check for updatedAt fields
                if '@updatedAt' in line:
                    self.updated_at_fields[model_name].append(field_name)
                
                # Check for relations
                if field_type in self.relationships:
                    relation_match = re.search(r'@relation\(([^)]*)\)', line)
                    fk_field = None
                    ref_field = None
                    ondelete = None
                    
                    if relation_match:
                        relation_args = relation_match.group(1)
                        fields_match = re.search(r'fields:\[([^\]]+)\]', relation_args)
                        references_match = re.search(r'references:\[([^\]]+)\]', relation_args)
                        ondelete_match = re.search(r'onDelete:\s*(\w+)', relation_args)
                        
                        if fields_match and references_match:
                            fk_field = fields_match.group(1).strip()
                            ref_field = references_match.group(1).strip()
                        if ondelete_match:
                            ondelete = ondelete_match.group(1)
                    
                    # Create relationship info
                    rel_info = RelationInfo(
                        field_name=field_name,
                        related_model=field_type,
                        is_list=is_list,
                        fk_field=fk_field,
                        ref_field=ref_field,
                        ondelete=ondelete
                    )
                    self.relationships[model_name][field_name] = rel_info
    
    def _parse_fields(self, model_name: str, model_content: str) -> List[str]:
        fields = []
        lines = model_content.strip().split('\n')
        has_vector_field = False
        vector_field_name = None
        vector_dimensions = None
        
        # First add all non-relationship fields
        for line in lines:
            line = line.strip()
            if not line or line.startswith('@@'): continue
            
            # Parse field definition
            field_match = re.match(r'(\w+)\s+(\w+)(\[\])?(\?)?(\s+@\w+)?(\([^)]*\))?(\s+@\w+\([^)]*\))?(\s+@\w+\([^)]*\))?', line)
            if field_match:
                field_name = field_match.group(1)
                field_type = field_match.group(2)
                is_list = bool(field_match.group(3))
                is_optional = bool(field_match.group(4))
                
                # Skip relationship fields
                if field_type in self.relationships:
                    continue
                
                decorators = []
                
                # Handle foreign key fields from relationships
                for rel_info in self.relationships[model_name].values():
                    if rel_info.fk_field == field_name:
                        ref_model = rel_info.related_model
                        ref_field = rel_info.ref_field or 'id'
                        decorators.append(f'foreign_key="{ref_model}.{ref_field}"')
                        break
                
                # Handle common decorators
                if '@id' in line:
                    decorators.append('primary_key=True')
                if '@default' in line:
                    default_match = re.search(r'@default\(([^)]*)\)', line)
                    if default_match:
                        default_value = default_match.group(1).strip()
                        
                        # Handle function-based defaults more robustly
                        lower_val = default_value.lower()
                        if 'uuid(' in lower_val:
                            decorators.append('default_factory=uuid4')
                        elif 'now(' in lower_val:
                            decorators.append('default_factory=datetime.utcnow')
                        elif 'autoincrement()' in lower_val:
                            # SQLModel handles autoincrement automatically for primary keys
                            continue
                        elif default_value.startswith('"') or default_value.startswith("'"):
                            decorators.append(f'default={default_value}')
                        # Fix boolean values
                        elif default_value.lower() == 'true':
                            decorators.append('default=True')
                        elif default_value.lower() == 'false':
                            decorators.append('default=False')
                        else:
                            decorators.append(f'default={default_value}')
                if '@unique' in line:
                    decorators.append('unique=True')
                
                # Handle updatedAt fields
                if field_name in self.updated_at_fields.get(model_name, []):
                    decorators.append('sa_column=Column(sql.func.now(), onupdate=sql.func.now())')
                
                # Special handling for vector types
                if field_type == "Unsupported":
                    vector_match = re.search(r'Unsupported\("vector\((\d+)\)"\)', line)
                    if vector_match:
                        dimensions = vector_match.group(1)
                        has_vector_field = True
                        vector_field_name = field_name
                        vector_dimensions = dimensions
                        # Use numpy array type for vector fields
                        py_type = f"np.ndarray"
                        # Add Field with special vector configuration
                        field_def = f"    {field_name}: {py_type} = Field(sa_column=Column(Vector({dimensions})))"
                        fields.append(field_def)
                        continue
                
                # Convert type
                py_type = self.TYPE_MAPPING.get(field_type, 'str')
                if is_list:
                    py_type = f"List[{py_type}]"
                if is_optional:
                    py_type = f"{py_type} | None"
                
                # Handle special text fields
                if field_name in self.text_fields.get(model_name, []):
                    decorators.append('sa_column=Column(Text)')
                
                # Add nullable constraint based on field definition
                if not is_optional and not field_name.startswith('@'):
                    decorators.append('nullable=False')
                
                # Add foreign key constraint for fields ending with 'Id'
                if field_name.endswith('Id') and field_name != 'id':
                    # Extract the model name from the field name (e.g., 'empresaId' -> 'Empresa')
                    ref_model = field_name[:-2]  # Remove 'Id'
                    ref_model = ref_model[0].upper() + ref_model[1:]  # Capitalize first letter
                    if ref_model in self.relationships:
                        decorators.append(f'foreign_key="{ref_model}.id"')
                
                # Create field definition
                if decorators:
                    field_def = f"    {field_name}: {py_type} = Field({', '.join(decorators)})"
                else:
                    field_def = f"    {field_name}: {py_type}"
                
                fields.append(field_def)
        
        # Now add relationship fields
        if model_name in self.relationships:
            fields.append("")  # Add newline before relationships
            for field_name, rel_info in self.relationships[model_name].items():
                relationship_kwargs = []
                if rel_info.ondelete:
                    ondelete_value = "CASCADE" if rel_info.ondelete == "Cascade" else "RESTRICT"
                    relationship_kwargs.append(f'"ondelete": "{ondelete_value}"')
                
                # Add the relationship field
                if rel_info.is_list:
                    if relationship_kwargs:
                        fields.append(f"    {field_name}: List[\"{rel_info.related_model}\"] = Relationship(back_populates=\"{rel_info.back_populates_field}\", sa_relationship_kwargs={{{', '.join(relationship_kwargs)}}})")
                    else:
                        fields.append(f"    {field_name}: List[\"{rel_info.related_model}\"] = Relationship(back_populates=\"{rel_info.back_populates_field}\")")
                else:
                    if relationship_kwargs:
                        fields.append(f"    {field_name}: Optional[\"{rel_info.related_model}\"] = Relationship(back_populates=\"{rel_info.back_populates_field}\", sa_relationship_kwargs={{{', '.join(relationship_kwargs)}}})")
                    else:
                        fields.append(f"    {field_name}: Optional[\"{rel_info.related_model}\"] = Relationship(back_populates=\"{rel_info.back_populates_field}\")")
        
        # Handle composite primary key
        if len(self.primary_keys[model_name]) > 1:
            pk_fields = [f"'{pk}'" for pk in self.primary_keys[model_name]]
            fields.append("")
            fields.append("    @classmethod")
            fields.append("    def __table_args__(cls):")
            fields.append(f"        return (PrimaryKeyConstraint({', '.join(pk_fields)}),)")
        
        # Add vector index creation
        if has_vector_field:
            if any(line.strip().startswith("    @classmethod") and "__table_args__" in line for line in fields):
                # We already have a __table_args__ method, need to modify it
                vector_index = [
                    f"            Index(",
                    f"                f'idx_{model_name.lower()}_{vector_field_name}_vector',",
                    f"                'embedding',",
                    f"                postgresql_using='ivfflat',",
                    f"                postgresql_with={{'lists': 100}},",
                    f"                postgresql_ops={{'embedding': 'vector_cosine_ops'}}",
                    f"            ),",
                ]
                
                # Find the __table_args__ method and insert the vector index
                for i, line in enumerate(fields):
                    if "__table_args__" in line:
                        # Find the closing parenthesis of the return tuple
                        for j in range(i+1, len(fields)):
                            if "return (" in fields[j]:
                                # Insert before the closing parenthesis
                                closing_index = fields[j].find(")") 
                                if closing_index > 0:
                                    fields[j] = fields[j][:closing_index] + vector_index[0] + fields[j][closing_index:]
                                    for k, v_line in enumerate(vector_index[1:]):
                                        fields.insert(j+k+1, v_line)
                                    break
                        break
            else:
                # Add a new __table_args__ method
                fields.append("")
                fields.append("    @classmethod")
                fields.append("    def __table_args__(cls):")
                fields.append(f"        return (")
                fields.append(f"            Index(")
                fields.append(f"                f'idx_{model_name.lower()}_{vector_field_name}_vector',",)
                fields.append(f"                'embedding',")
                fields.append(f"                postgresql_using='ivfflat',")
                fields.append(f"                postgresql_with={{'lists': 100}},")
                fields.append(f"                postgresql_ops={{'embedding': 'vector_cosine_ops'}}")
                fields.append(f"            ),")
                fields.append(f"        )")
        
        return fields
    
    def generate_sqlmodel_code(self) -> str:
        imports = [
            "from __future__ import annotations",
            "from datetime import datetime",
            "from uuid import uuid4",
            "from typing import Optional, List, Any",
            "from sqlmodel import Field, SQLModel, Relationship",
            "import numpy as np",
            "from sqlalchemy import Column, Index, Text, sql, PrimaryKeyConstraint",
            "from pgvector.sqlalchemy import Vector",
            "",
            "# Enable pgvector extension if not enabled",
            "# You'll need to run this SQL first: CREATE EXTENSION IF NOT EXISTS vector;",
            "",
        ]
        
        model_codes = []
        # Generate model classes
        for model_name, fields in self.models.items():
            model_code = [
                f"class {model_name}(SQLModel, table=True):",
                f'    __tablename__ = "{model_name}"',
                ""  # Add newline after tablename
            ]
            model_code.extend(fields)
            
            # Add Config class with all indexes if any exist
            has_config = any("class Config:" in line for line in model_code)
            if model_name in self.indexes and self.indexes[model_name] and not has_config:
                # Convert list of fields to list of tuples for proper index format
                index_tuples = [f"('{field}',)" for field in self.indexes[model_name]]
                if index_tuples:
                    model_code.append("")
                    model_code.append("    class Config:")
                    model_code.append(f"        indexes = [{', '.join(index_tuples)}]")
            
            model_codes.append('\n'.join(model_code))
        
        return '\n\n'.join(imports + [""] + model_codes)  # Use double newlines between models
    
    def convert(self) -> str:
        content = self.read_prisma_schema()
        self.parse_models(content)
        return self.generate_sqlmodel_code()

def format_with_black(file_path: str) -> None:
    try:
        subprocess.run(['black', file_path], check=True)
        print("Successfully formatted with black")
    except subprocess.CalledProcessError:
        print("Error while formatting with black")
    except FileNotFoundError:
        print("black not found. Please install it with: pip install black")

def main():
    # Get the path to the schema.prisma file
    script_dir = Path(__file__).parent
    prisma_file = script_dir.parent.parent / "frontend" / "prisma" / "schema.prisma"
    output_file = script_dir.parent / "src" / "generated" / "schema.py"
    
    # Create the converter and run it
    converter = PrismaConverter(prisma_file)
    python_code = converter.convert()
    
    # Write the output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(python_code)
    
    # Format with black
    try:
        subprocess.run(['uvx', 'black', str(output_file)], check=True)
        print(f"Generated and formatted SQLModel schema at {output_file}")
    except subprocess.CalledProcessError:
        print(f"Generated SQLModel schema at {output_file}")
        print("Warning: Failed to format with uvx black")
    except FileNotFoundError:
        print(f"Generated SQLModel schema at {output_file}")
        print("Warning: uvx black not found. Please install it with: pip install uvx")

if __name__ == "__main__":
    main() 