import pytest
from pathlib import Path
from prisma_to_sqlmodel import PrismaConverter

def test_basic_model_conversion(tmp_path):
    # Create a test Prisma schema
    prisma_schema = """
    model User {
        id        Int      @id @default(autoincrement())
        email     String   @unique
        name      String?
        createdAt DateTime @default(now())
        updatedAt DateTime @updatedAt
    }
    """
    
    prisma_file = tmp_path / "schema.prisma"
    prisma_file.write_text(prisma_schema)
    
    # Convert the schema
    converter = PrismaConverter(prisma_file)
    python_code = converter.convert()
    
    # Check that the output contains expected elements
    assert "class User(SQLModel, table=True):" in python_code
    assert "__tablename__ = \"User\"" in python_code
    assert "id: int = Field(primary_key=True, default=autoincrement(, nullable=False)" in python_code
    assert "email: str = Field(unique=True, nullable=False)" in python_code
    assert "name: str | None" in python_code
    assert "createdAt: datetime = Field(default_factory=datetime.utcnow, nullable=False)" in python_code
    assert "updatedAt: datetime = Field(sa_column=Column(sql.func.now(), onupdate=sql.func.now()), nullable=False)" in python_code

def test_relationship_conversion(tmp_path):
    # Create a test Prisma schema with relationships
    prisma_schema = """
    model User {
        id        Int      @id @default(autoincrement())
        email     String   @unique
        posts     Post[]
    }

    model Post {
        id        Int      @id @default(autoincrement())
        title     String
        author    User     @relation(fields: [authorId], references: [id])
        authorId  Int
    }
    """
    
    prisma_file = tmp_path / "schema.prisma"
    prisma_file.write_text(prisma_schema)
    
    # Convert the schema
    converter = PrismaConverter(prisma_file)
    python_code = converter.convert()
    
    # Check that the output contains expected elements
    assert 'posts: List["Post"] = Relationship(back_populates="author")' in python_code
    assert 'author: Optional["User"] = Relationship(back_populates="posts")' in python_code
    assert "authorId: int = Field(nullable=False)" in python_code

def test_vector_field_conversion(tmp_path):
    # Create a test Prisma schema with a vector field
    prisma_schema = """
    model Document {
        id        Int      @id @default(autoincrement())
        content   String
        embedding Unsupported("vector(1536)")
    }
    """
    
    prisma_file = tmp_path / "schema.prisma"
    prisma_file.write_text(prisma_schema)
    
    # Convert the schema
    converter = PrismaConverter(prisma_file)
    python_code = converter.convert()
    
    # Check that the output contains expected elements
    assert "embedding: np.ndarray = Field(sa_column=Column(Vector(1536)))" in python_code
    assert "from pgvector.sqlalchemy import Vector" in python_code
    assert "import numpy as np" in python_code 