# optional-addons Specification

## Purpose

TBD - created by archiving change 'multi-database-and-addons'. Update Purpose after archive.

## Requirements

### Requirement: Redis add-on infrastructure

The template SHALL provide a Redis service in `docker-compose.yml` under the `redis` profile on all database branches.

#### Scenario: Redis service starts when profile is active

- **WHEN** a user runs `docker compose --profile redis up`
- **THEN** a Redis service using the `redis:7-alpine` image SHALL start and be reachable on port `6379`

#### Scenario: Redis service does not start without profile

- **WHEN** a user runs `docker compose up` without specifying the `redis` profile
- **THEN** the Redis service SHALL NOT start


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
### Requirement: Redis app-level client

The template SHALL provide `src/shared/redis.py` with an async Redis client that is auto-initialized when `REDIS_URL` is set.

#### Scenario: Redis client initializes when env var is set

- **WHEN** the `REDIS_URL` environment variable is set and `init_redis()` is called during app startup
- **THEN** `redis_client` SHALL be a connected `Redis` instance

#### Scenario: Redis client is None when env var is not set

- **WHEN** the `REDIS_URL` environment variable is not set
- **THEN** `init_redis()` SHALL return without raising an error and `redis_client` SHALL remain `None`

#### Scenario: Accessing Redis client when not configured raises error

- **WHEN** `get_redis()` helper is called and `redis_client` is `None`
- **THEN** it SHALL raise `RuntimeError` with a descriptive message


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
### Requirement: MinIO add-on infrastructure

The template SHALL provide a MinIO service in `docker-compose.yml` under the `minio` profile on all database branches.

#### Scenario: MinIO service starts when profile is active

- **WHEN** a user runs `docker compose --profile minio up`
- **THEN** a MinIO service SHALL start with API on port `9000` and console on port `9001`

#### Scenario: MinIO service does not start without profile

- **WHEN** a user runs `docker compose up` without specifying the `minio` profile
- **THEN** the MinIO service SHALL NOT start


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
### Requirement: MinIO app-level client

The template SHALL provide `src/shared/storage.py` with an async MinIO client using `miniopy-async` that is auto-initialized when `MINIO_ENDPOINT` is set.

#### Scenario: MinIO client initializes when env vars are set

- **WHEN** `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, and `MINIO_SECRET_KEY` are set and `init_storage()` is called
- **THEN** `storage_client` SHALL be a configured `Minio` instance

#### Scenario: MinIO client is None when env vars are not set

- **WHEN** `MINIO_ENDPOINT` is not set
- **THEN** `init_storage()` SHALL return without raising an error and `storage_client` SHALL remain `None`

#### Scenario: Accessing MinIO client when not configured raises error

- **WHEN** `get_storage()` helper is called and `storage_client` is `None`
- **THEN** it SHALL raise `RuntimeError` with a descriptive message


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
### Requirement: LakeFS add-on infrastructure

The template SHALL provide a LakeFS service in `docker-compose.yml` under the `lakefs` profile on all database branches.

#### Scenario: LakeFS service starts when profile is active

- **WHEN** a user runs `docker compose --profile lakefs up`
- **THEN** a LakeFS service SHALL start and be reachable on port `8001`

#### Scenario: LakeFS service does not start without profile

- **WHEN** a user runs `docker compose up` without specifying the `lakefs` profile
- **THEN** the LakeFS service SHALL NOT start


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
### Requirement: LakeFS app-level client

The template SHALL provide `src/shared/lakefs.py` with a LakeFS client that is auto-initialized when `LAKEFS_ENDPOINT` is set. The client SHALL wrap synchronous SDK calls using `asyncio.to_thread` due to the lack of an official async SDK.

#### Scenario: LakeFS client initializes when env vars are set

- **WHEN** `LAKEFS_ENDPOINT`, `LAKEFS_ACCESS_KEY`, and `LAKEFS_SECRET_KEY` are set and `init_lakefs()` is called
- **THEN** `lakefs_client` SHALL be a configured client instance ready to make API calls

#### Scenario: LakeFS client is None when env vars are not set

- **WHEN** `LAKEFS_ENDPOINT` is not set
- **THEN** `init_lakefs()` SHALL return without raising an error and `lakefs_client` SHALL remain `None`

#### Scenario: Accessing LakeFS client when not configured raises error

- **WHEN** `get_lakefs()` helper is called and `lakefs_client` is `None`
- **THEN** it SHALL raise `RuntimeError` with a descriptive message


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
### Requirement: Add-on initialization in app lifespan

`src/main.py` lifespan SHALL call `init_redis()`, `init_storage()`, and `init_lakefs()` during startup on all database branches.

#### Scenario: All add-on inits are called at startup

- **WHEN** the FastAPI application starts
- **THEN** `init_redis()`, `init_storage()`, and `init_lakefs()` SHALL each be called, and those without corresponding env vars SHALL silently skip initialization


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
### Requirement: Add-on environment variables in .env.example

All database branches SHALL include commented-out add-on environment variable examples in `.env.example`.

#### Scenario: Add-on env vars are present but commented out

- **WHEN** `.env.example` is inspected on any branch
- **THEN** it SHALL contain commented-out entries for `REDIS_URL`, `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `LAKEFS_ENDPOINT`, `LAKEFS_ACCESS_KEY`, and `LAKEFS_SECRET_KEY`

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