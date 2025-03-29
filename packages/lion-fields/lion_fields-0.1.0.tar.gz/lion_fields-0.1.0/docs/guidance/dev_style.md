---
title: Development Style Guide
created: 2025-03-28
updated: 2025-03-28
version: 1
---

## 1. Introduction

### 1.1 Purpose & Scope

This guide **MANDATES** how all code, tests, documentation, and processes must
be structured, written, and maintained within **[Project Name]**. It ensures
that contributions:

1. **Look & Feel Consistent** (formatting, naming)
2. **Are Secure, Tested, and Performant**
3. **Follow Good Design Principles** (SRP, low coupling, clarity)
4. **Are Resilient & Maintainable**

All team members (and integrated tools like LLMs) must follow these rules. For
any proposed changes, open a Pull Request referencing relevant sections.

### 1.2 Core Principles

1. **Clarity & Explicitness**
   - Code must be easily understood. Document “why” when non-obvious.
2. **Consistency**
   - Follow the same approach for naming, formatting, error handling, etc.
3. **Simplicity (KISS)**
   - Favor minimal designs. Avoid over-engineering. Justify complexity if
     introduced.
4. **Robustness**
   - Validate all inputs. Fail cleanly on errors. No silent failures.
5. **Testability**
   - Thoroughly test all logic. Testing is non-negotiable.
6. **Security**
   - Build security in from day one (input validation, dependency checks, no
     secrets in code).
7. **Maintainability**
   - Easy to refactor, well-documented, with a logical structure.

### 1.3 Living Document

This file can evolve via a Pull Request. Provide clear reasons for any proposed
changes.

---

## 2. Formatting & Linting

**Requirement**: All code must be auto-formatted and pass lint checks **before**
merging.

1. **Tools**
   - **Python**: [Black](https://github.com/psf/black) for formatting,
     [Ruff](https://github.com/astral-sh/ruff) for linting.
   - **Rust**: `cargo fmt` + `cargo clippy`.
   - **TypeScript/JS**: [Prettier](https://prettier.io/) +
     [ESLint](https://eslint.org/).
2. **Configuration**
   - Python: `pyproject.toml`
   - Rust: `rustfmt.toml` (optional) + `clippy.toml`/`Cargo.toml` settings
   - TS/JS: `.prettierrc.*`, `.eslintrc.*`
3. **Pre-commit Hooks**
   - Use [pre-commit](https://pre-commit.com/) or relevant alternatives (e.g.,
     Husky for JS).
   - Hooks run all formatters/linters automatically.
   - Don’t bypass hooks unless absolutely necessary, with a note.
4. **No Manual Overrides**
   - Don’t disable rules or reformat code manually. If you must, add a short
     inline comment explaining why.

---

## 3. Naming Conventions

**Requirement**: Use consistent, descriptive names across the codebase.

1. **General**
   - Avoid one-letter names except simple loop counters (`i`, `j`).
   - No unclear placeholders like `data`, `obj`, `manager`—be specific.
   - Use standard abbreviations (`cfg`, `init`) if widely recognized.
2. **Python**
   - Functions/Vars: `snake_case`
   - Classes: `PascalCase`
   - Constants: `ALL_CAPS_SNAKE_CASE`
   - “Private” members: prefix `_` or `__` carefully.
3. **Rust**
   - Follow
     [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/naming.html).
   - Typically `snake_case` for functions/vars, `PascalCase` for types.
   - `SCREAMING_SNAKE_CASE` for constants.
4. **TypeScript**
   - `camelCase` for functions/vars; `PascalCase` for classes/interfaces.
   - `UPPER_SNAKE_CASE` for constants.

Aim for clarity. “Describe the entity’s purpose in the name.”

---

## 4. Repository & Code Organization

1. **Folder Layout**
   - `src/` (or `lib/` in Rust) for main code.
   - `tests/` for tests, mirroring `src/`.
   - `docs/` for design docs, `dev_style.md`, references.
   - `scripts/` for build, deploy, or other utility scripts.
   - `config/` or `examples/` for example config files, `.env.example`.
2. **Modularity**
   - Keep modules well-focused (Single Responsibility).
   - Avoid large “god classes” or “utility modules” that handle everything.
3. **Data Models**
   - Python: Pydantic models in `models/`, or near their usage.
   - Rust: Structs/enums with Serde attributes for input/output.
   - TS: Interfaces/types in relevant domain directories.
4. **Documentation**
   - Use docstrings (Python, Rust docs, JSDoc) for non-trivial classes, methods,
     modules.
   - Explain “why” the code is structured a certain way.

---

## 5. Data Modeling & Validation

**Mandatory**: All external or untrusted data must be validated on receipt.

1. **Pydantic (Python)**
   - Mark critical fields as required (`...`).
   - Use `Optional[...]` only if truly optional.
   - Add custom validators (`@validator`, `@field_validator`) for
     domain-specific rules.
2. **Serde (Rust)**
   - Derive `Deserialize` for input data.
   - If advanced checks are needed, use the `validator` crate or custom logic.
3. **TypeScript**
   - Use static types plus runtime checks (e.g.,
     [Zod](https://github.com/colinhacks/zod)) if data is from untrusted
     sources.
4. **Avoid `default_factory`** for conceptually required fields—**don’t** mask
   incomplete LLM data or other input. Let validation fail, then handle or
   re-prompt.
5. **On Validation Fail**:
   - Log the error details.
   - Reject the invalid data or provide a meaningful error.
   - Don’t silently skip or auto-default; that hides real problems.

---

## 6. Error Handling

1. **No Silent Failures**
   - Code must explicitly handle errors.
   - Log or re-raise them with context.
2. **Language-Specific**
   - Python: Raise specific exceptions; catch only what you can handle.
   - Rust: Use `Result<T, E>`; define custom error enums. Use `?` for simple
     propagation.
   - TS: Use typed errors or classical `try/catch`.
3. **Validation Errors**
   - Distinguish them from other errors.
   - Typically treat them as 4xx in a web environment, or fail fast in local
     CLI.
4. **Logging**
   - Include relevant context (non-sensitive) in log messages.
   - Don’t leak secrets in logs.

---

## 7. Testing

Testing is **non-negotiable**. Code changes must have tests.

1. **Frameworks**
   - Python: [pytest](https://docs.pytest.org/).
   - Rust: `cargo test` + optional coverage with `cargo tarpaulin`.
   - TS: [Jest](https://jestjs.io/) or [Vitest](https://vitest.dev/).
2. **Structure**
   - Mirror `src/` layout in `tests/`.
   - `test_<module>.py`, `mod_test.rs`, `myfile.test.ts` naming.
3. **Types of Tests**
   - **Unit**: Isolated from external systems. Mock dependencies.
   - **Integration**: Multiple modules or services interacting. Possibly spin up
     test DB.
   - **E2E** (CLI/API): Real user flows.
4. **Coverage**
   - Target ~80–90% on critical logic.
   - Use coverage tools (`pytest --cov`, `tarpaulin`, `jest --coverage`).
   - Address big coverage drops before merging.
5. **Fast & Repeatable**
   - Keep tests consistent, no hidden dependencies.
   - Ensure they pass locally and in CI.

---

## 8. Git & Branching Strategy

1. **Branch Model**
   - Typically “GitHub Flow”:
     - `main` is production-ready, protected.
     - Feature branches from `main` named `feat/shortdesc`, `fix/issue-###`,
       etc.
     - Merge via Pull Requests only.
2. **Commits**
   - Must follow [Conventional Commits](https://www.conventionalcommits.org/)
     strictly.
   - Examples: `feat: add user login`, `fix(cli): handle missing args`.
   - Keep subject lines to ~50 chars, use 72-char wrapping in body.
3. **Pull Requests**
   - Must pass lint, format, test, coverage checks.
   - Write clear, thorough descriptions: _what_, _why_, _how to test_.
   - At least one reviewer approval.
   - “Squash and Merge” is recommended for a clean commit history.
4. **Commit Granularity**
   - Keep commits atomic, e.g., “Add function X.”
   - Rebase or squash fixups prior to merge to maintain clarity.

---

## 9. Dependencies & Security Scanning

1. **Dependency Management**
   - Python: Use `poetry` or `pip-tools` with a lock file.
   - Rust: `cargo` manages `Cargo.lock`.
   - TS: `npm`, `yarn`, or `pnpm` with a lock file.
2. **Vulnerability Checks**
   - Python: `pip-audit` or `safety check` in CI.
   - Rust: `cargo audit`.
   - TS: `npm audit` or `yarn audit`.
   - Address high severity issues ASAP.
3. **Regular Updates**
   - Tools like Dependabot or Renovate can automate upgrade PRs.
   - Keep track of major version bumps, test thoroughly.

---

## 10. Logging

1. **Structured Logging**
   - Use JSON or a structured format in production to facilitate parsing.
   - Development logs can be more human-readable.
2. **Log Levels**
   - `DEBUG` for dev details, `INFO` for key actions, `WARNING` for possible
     issues, `ERROR` for recoverable errors, `CRITICAL` for unrecoverable.
3. **No Secrets**
   - Never log passwords, tokens, or personal info.
4. **Context**
   - Include request IDs, user IDs, transaction IDs when relevant.

---

## 11. Configuration & Secrets

1. **Configuration**
   - Store in environment variables or config files separate from code.
   - Validate config on startup (e.g., Pydantic `Settings`).
   - Provide `.env.example` for local dev.
2. **Secrets**
   - **Never** commit secrets in code or example files.
   - Use environment variables, or a vault solution.
   - Mark `.env` in `.gitignore`.
3. **12-Factor**
   - Favor “12-Factor” app principles. Keep config minimal, consistent, and easy
     to override in different environments.

---

## 12. Security Guidelines

1. **Input Validation**
   - All user/LLM input is untrusted by default. Validate thoroughly (Section
     5).
2. **Output Encoding**
   - Use proper escaping or parameterization to avoid injection.
3. **Authentication & Authorization**
   - Use robust libraries/protocols.
   - Enforce principle of least privilege.
4. **Dependencies**
   - Address vulnerabilities promptly (Section 9).
5. **Incident Logging**
   - Log suspicious events with enough context but no sensitive info.
6. **Secrets Management**
   - Strictly no secrets in git. Use environment or vault.
7. **Secure by Default**
   - Prefer HTTPS, secure ciphers, safe defaults.

---

## 13. Tooling & Environment

1. **Setup**
   - `README.md` or `CONTRIBUTING.md` must detail how to set up dev environment.
   - Provide simple steps or scripts (e.g., `make setup` or `poetry install`).
2. **Task Runner**
   - Could be a Makefile, `justfile`, or npm scripts.
   - Expose tasks: `make format`, `make lint`, `make test`, `make run`,
     `make clean`.
3. **Local vs. CI**
   - Keep local dev consistent with CI environment.
   - Document any differences (e.g., Docker usage, extra container
     dependencies).

---

## 14. LLM Integration

1. **LLM Outputs**
   - Treat LLM code, text, or config as **untrusted**.
   - Must pass all format/lint checks, validation, security screening.
2. **Validation**
   - Let strict Pydantic/Serde/TS schemas catch missing or malformed fields.
   - If incomplete, log errors, possibly re-prompt the LLM with better
     instructions.
   - Avoid adding `default_factory` or optional fields just to handle LLM
     oversights. Fail fast, fix the prompt or data.
3. **Testing**
   - LLM-generated logic must have the same (or stricter) test coverage.
   - Carefully check for edge cases or potential security pitfalls.
4. **Document**
   - Optionally comment that certain blocks are “AI-generated” so future
     maintainers know.

---

## 15. Extended Considerations

1. **Concurrency**
   - Python: `asyncio` or threading. Document concurrency model.
   - Rust: `tokio` or threads. Mind ownership rules.
   - TS: `async/await`, handle race conditions carefully.
   - Keep concurrency patterns consistent, with thorough tests.
2. **Performance Profiling**
   - Python: `cProfile`, `line_profiler`.
   - Rust: `cargo bench`, `cargo flamegraph`.
   - TS: Node’s built-in profiler, or DevTools.
   - Profile only when needed; keep clarity in code.
3. **Microservices vs. Monolith**
   - If microservices: keep each service self-contained with a well-defined API.
   - If monolith: maintain clear module boundaries.
   - Document architecture diagrams in `docs/`.

---

## 16. Pull Request & Merging Policy

Recapping essential points on PR workflow:

1. **Mandatory Checks**
   - All commits pass format/lint/tests/coverage.
   - CI must be green.
2. **Conventional Commits**
   - PR title must conform (like `feat: add user signup endpoint`).
   - Include references to issues or Jira tickets in the description.
3. **Review**
   - Minimum 1–2 approvals based on your team policy.
   - Address all feedback.
   - Keep PR scope small for easier review.
4. **Merge**
   - “Squash and Merge” recommended.
   - Final commit message aligns with Conventional Commits.

---

## 17. Living Document

If you find contradictions, missing sections, or outdated info:

- Open an Issue describing the problem.
- Submit a PR to update `dev_style.md` with a clear rationale.
- The team reviews and merges changes if approved.

---

## 18. Conclusion

This style guide is **lengthy** but sets a **strict, thorough foundation** for:

- Code style & structure,
- Validation & error handling,
- Testing & coverage,
- Security & secrets management,
- LLM usage guidelines,
- Branching & commit discipline,
- Logging & configuration,
- Overall maintainability.

By adhering to it, we ensure a **consistent**, **secure**, and **high-quality**
codebase that fosters rapid iteration, robust operation, and smoother
collaboration among both humans and AI-driven tools.

**Thank you for reading!**

> Remember: If in doubt, keep things simple, tested, and well-documented.
