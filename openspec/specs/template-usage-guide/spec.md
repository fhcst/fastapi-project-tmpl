## Requirements

### Requirement: README provides a concise project overview

The README.md file SHALL serve as a 2-minute overview that covers: what the template is, the tech stack, and a 3-step quick start. It SHALL link to `docs/Usage.md` for detailed instructions. The README SHALL NOT contain unfilled placeholders.

#### Scenario: Student lands on the repository page

- **WHEN** a student opens the GitHub repository page
- **THEN** they SHALL see the project description, tech stack badges, and a clear quick-start section within the first screenful

#### Scenario: Student wants detailed setup instructions

- **WHEN** a student needs more detailed instructions
- **THEN** the README SHALL direct them to `docs/Usage.md` via a clearly labeled link


<!-- @trace
source: update-template-documentation
updated: 2026-03-20
code:
  - README.md
  - CONTRIBUTING.md
  - docs/Usage.md
-->

---
### Requirement: Usage guide covers the full workflow from fork to first API

The `docs/Usage.md` file SHALL provide a step-by-step tutorial in Traditional Chinese covering four sequential phases: (1) obtaining the template via Fork and Clone, (2) environment setup with uv and Docker, (3) verifying the service is running via Swagger UI, (4) adding a new API endpoint with a working code example.

#### Scenario: Student forks and clones the template

- **WHEN** a student follows the "取得 Template" section
- **THEN** they SHALL have a local copy of the repository ready for development

#### Scenario: Student sets up the development environment

- **WHEN** a student follows the "建置環境" section
- **THEN** they SHALL be able to run `uv sync`, configure `.env`, and start Docker services successfully

#### Scenario: Student verifies the service is running

- **WHEN** a student completes the setup steps
- **THEN** they SHALL be able to open Swagger UI at `http://localhost:8000/docs` and see the API documentation

#### Scenario: Student adds a new API endpoint

- **WHEN** a student follows the "新增第一個 API Endpoint" section
- **THEN** they SHALL be able to add a `GET /items` endpoint by following the provided code example, and verify it appears in Swagger UI


<!-- @trace
source: update-template-documentation
updated: 2026-03-20
code:
  - README.md
  - CONTRIBUTING.md
  - docs/Usage.md
-->

---
### Requirement: CONTRIBUTING.md uses clear TODO callouts for customizable sections

The `CONTRIBUTING.md` file SHALL replace all `[placeholder]` text with `> [!NOTE]` callout blocks that clearly instruct students which sections to customize. The Git workflow and commit convention sections SHALL remain intact and complete.

#### Scenario: Student opens CONTRIBUTING.md to customize it

- **WHEN** a student opens the file to adapt it for their own project
- **THEN** all sections requiring customization SHALL be clearly marked with a `> [!NOTE]` or `> [!IMPORTANT]` callout explaining what to change

#### Scenario: Student reads the Git workflow section

- **WHEN** a student reads the development workflow section
- **THEN** they SHALL find complete, actionable instructions for the Feature Branch workflow without any placeholder text

<!-- @trace
source: update-template-documentation
updated: 2026-03-20
code:
  - README.md
  - CONTRIBUTING.md
  - docs/Usage.md
-->