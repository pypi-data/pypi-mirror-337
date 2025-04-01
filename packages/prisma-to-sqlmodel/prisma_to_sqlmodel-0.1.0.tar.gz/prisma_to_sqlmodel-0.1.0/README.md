# Prisma to SQLModel

A tool to convert Prisma schema files to SQLModel models. This tool helps you migrate from Prisma to SQLModel while preserving your data model structure, relationships, and indexes.

## Features

- Converts Prisma models to SQLModel classes
- Preserves relationships (one-to-one, one-to-many, many-to-many)
- Handles indexes and primary keys
- Supports vector fields with pgvector
- Maintains field types and constraints
- Generates proper SQLModel relationships with back_populates

## Installation

```bash
pip install prisma-to-sqlmodel
```

## Usage

### Command Line Interface

```bash
prisma-to-sqlmodel schema.prisma output.py
```

### Python API

```python
from prisma_to_sqlmodel import PrismaConverter

converter = PrismaConverter("schema.prisma")
python_code = converter.convert()

# Write to file
with open("output.py", "w") as f:
    f.write(python_code)
```

## Example

### Input (schema.prisma)

```prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String   @db.Text
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### Output (output.py)

```python
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    __tablename__ = "User"

    id: int = Field(primary_key=True)
    email: str = Field(unique=True)
    name: Optional[str] = None
    posts: List["Post"] = Relationship(back_populates="author")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(sa_column=Column(sql.func.now(), onupdate=sql.func.now()))

class Post(SQLModel, table=True):
    __tablename__ = "Post"

    id: int = Field(primary_key=True)
    title: str
    content: str = Field(sa_column=Column(Text))
    author: User = Relationship(back_populates="posts")
    author_id: int = Field(foreign_key="User.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(sa_column=Column(sql.func.now(), onupdate=sql.func.now()))
```

## Development

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
4. Install dependencies: `pip install -e ".[dev]"`
5. Run tests: `pytest`

## License

MIT License
