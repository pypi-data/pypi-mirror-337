import pytest
from pathlib import Path

@pytest.fixture
def sample_prisma_schema():
    return """
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
    """

@pytest.fixture
def sample_prisma_file(tmp_path, sample_prisma_schema):
    prisma_file = tmp_path / "schema.prisma"
    prisma_file.write_text(sample_prisma_schema)
    return prisma_file 