# database-variants Specification

## Purpose

TBD - created by archiving change 'multi-database-and-addons'. Update Purpose after archive.

## Requirements

### Requirement: MariaDB branch availability

The template SHALL provide a `template/mariadb` git branch that is rebased from `main` and uses MariaDB as the primary database with `aiomysql` as the async driver and SQLModel/SQLAlchemy as the ORM.

#### Scenario: MariaDB branch is functional

- **WHEN** a user clones the `template/mariadb` branch and runs `docker compose up`
- **THEN** the FastAPI application SHALL start successfully and connect to the MariaDB service


<!-- @trace
source: multi-database-and-addons
updated: 2026-03-17
code:
  - .env.example
  - docker-compose.yml
  - src/main.py
  - src/shared/storage.py
  - src/shared/lakefs.py
  - pyproject.toml
  - src/shared/redis.py
-->

---
### Requirement: PostgreSQL branch availability

The template SHALL provide a `template/postgres` git branch that uses PostgreSQL as the primary database with `asyncpg` as the async driver and SQLModel/SQLAlchemy as the ORM.

#### Scenario: PostgreSQL branch uses correct driver

- **WHEN** the `DB_URL` environment variable is set to `postgresql+asyncpg://...`
- **THEN** `src/shared/database.py` SHALL create an `AsyncEngine` using the `asyncpg` dialect without requiring any code changes

#### Scenario: PostgreSQL docker-compose service is defined

- **WHEN** a user runs `docker compose up` on the `template/postgres` branch
- **THEN** a PostgreSQL service SHALL start and the app container SHALL connect to it via the `DB_URL` environment variable


<!-- @trace
source: multi-database-and-addons
updated: 2026-03-17
code:
  - .env.example
  - docker-compose.yml
  - src/main.py
  - src/shared/storage.py
  - src/shared/lakefs.py
  - pyproject.toml
  - src/shared/redis.py
-->

---
### Requirement: MongoDB branch availability

The template SHALL provide a `template/mongo` git branch that uses MongoDB as the primary database with `motor` as the async driver and `beanie` as the ODM, replacing SQLModel/SQLAlchemy entirely.

#### Scenario: MongoDB branch initializes with Beanie

- **WHEN** the application starts on the `template/mongo` branch
- **THEN** `init_db()` SHALL call `beanie.init_beanie()` with the Motor database instance

#### Scenario: MongoDB branch has no SQLModel dependency

- **WHEN** `pyproject.toml` on the `template/mongo` branch is inspected
- **THEN** it SHALL NOT contain `sqlmodel`, `sqlalchemy`, or `aiomysql` as dependencies

#### Scenario: MongoDB docker-compose service is defined

- **WHEN** a user runs `docker compose up` on the `template/mongo` branch
- **THEN** a MongoDB service SHALL start and the app container SHALL connect to it via the `MONGO_URL` environment variable


<!-- @trace
source: multi-database-and-addons
updated: 2026-03-17
code:
  - .env.example
  - docker-compose.yml
  - src/main.py
  - src/shared/storage.py
  - src/shared/lakefs.py
  - pyproject.toml
  - src/shared/redis.py
-->

---
### Requirement: Branch-specific environment variables

Each database branch SHALL provide a `.env.example` file with the correct environment variable names and example values for its respective database.

#### Scenario: postgres branch env vars are correct

- **WHEN** `.env.example` on the `template/postgres` branch is inspected
- **THEN** it SHALL contain `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, and a `DB_URL` using the `postgresql+asyncpg://` scheme

#### Scenario: mongo branch env vars are correct

- **WHEN** `.env.example` on the `template/mongo` branch is inspected
- **THEN** it SHALL contain `MONGO_URL` and `MONGO_DB` variables, and SHALL NOT contain `DB_URL`


<!-- @trace
source: multi-database-and-addons
updated: 2026-03-17
code:
  - .env.example
  - docker-compose.yml
  - src/main.py
  - src/shared/storage.py
  - src/shared/lakefs.py
  - pyproject.toml
  - src/shared/redis.py
-->

---
### Requirement: SQLite fallback preserved on SQL branches

On `main`, `template/mariadb`, and `template/postgres` branches, `src/shared/database.py` SHALL retain the SQLite in-memory fallback when `DB_URL` is not set, to support running tests without a database service.

#### Scenario: No DB_URL set on SQL branch

- **WHEN** `DB_URL` environment variable is not set on a SQL branch
- **THEN** the application SHALL use `sqlite+aiosqlite:///:memory:` as the database URL

<!-- @trace
source: multi-database-and-addons
updated: 2026-03-17
code:
  - .env.example
  - docker-compose.yml
  - src/main.py
  - src/shared/storage.py
  - src/shared/lakefs.py
  - pyproject.toml
  - src/shared/redis.py
-->