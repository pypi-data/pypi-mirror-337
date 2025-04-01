# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-03-28

### Added
- Initial release
- Convert Prisma schema files to SQLModel models
- Support for basic field types (String, Int, Float, Boolean, DateTime, Json, BigInt, Decimal)
- Support for relationships (one-to-one, one-to-many, many-to-many)
- Support for indexes and primary keys
- Support for vector fields with pgvector
- Support for field constraints (unique, nullable)
- Support for default values and auto-increment
- Support for updatedAt fields
- Command-line interface with black formatting option
- Comprehensive test suite
- GitHub Actions for testing, linting, and publishing 