---
title: Conventional Commits
version: 1.0.0
---

## Summary

The **Conventional Commits** specification is a lightweight convention for
structuring commit messages. It:

- Encourages an **explicit commit history**, making it simpler to:
  - Generate changelogs automatically.
  - Derive semantic version bumps (major/minor/patch).
  - Communicate the nature of changes to maintainers and users.
  - Automate builds/publishes based on commit message types.

## Basic Format

A commit message **must** follow the structure:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Required Parts

- **type**
  - Common examples:
    - `fix`: Patches a bug (Semantic Versioning **PATCH**).
    - `feat`: Introduces a new feature (Semantic Versioning **MINOR**).

- **description**
  - A short summary of the code changes (imperative, present tense).

### Optional Parts

- **scope** (in parentheses):
  - Clarifies which part of the codebase was affected, e.g. `feat(parser): ...`.
- **body**:
  - Provides extended details or context; begins one blank line after the
    description.
- **footers**:
  - Provide extra metadata or references.
  - Common footers include:
    - `BREAKING CHANGE: <description>`
    - `Refs: #issueNumber`
    - `Reviewed-by: Name`
  - Each footer is placed one blank line after the body, can follow the
    [Git trailer format](https://git-scm.com/docs/git-interpret-trailers).

## Notable Types

Besides `fix` and `feat`, you can also use types like:

- `build`
- `chore`
- `ci`
- `docs`
- `style`
- `refactor`
- `perf`
- `test`

> **Important**: By default, only `fix` and `feat` correlate to **patch** and
> **minor** releases in Semantic Versioning. Additional types do **not** affect
> versioning unless they include a `BREAKING CHANGE`.

## Breaking Changes

To signal a **major** version bump, you must indicate a breaking change. This
can be done in **two** ways:

1. **Add `!`** after the type/scope:
   - Example: `feat!: drop support for Node 6`
   - Or: `feat(api)!: rename order field to sequence`
   - The description or body must clarify the breaking change.

2. **Add a `BREAKING CHANGE:` footer**:
   - Example:
     ```
     feat: allow provided config object to extend other configs

     BREAKING CHANGE: `extends` key in config file is now used for extending other config files
     ```

> If `!` is used in the type, `BREAKING CHANGE:` in the footer can be omitted
> (the description can explain the breaking change instead).

## Examples

### 1. Commit with Description and Breaking Change Footer

```
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

### 2. Commit with `!` for a Breaking Change

```
feat!: send an email to the customer when a product is shipped
```

### 3. Commit with Scope and `!`

```
feat(api)!: send an email to the customer when a product is shipped
```

### 4. Commit with `!` + `BREAKING CHANGE` Footer

```
chore!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

### 5. Commit with No Body

```
docs: correct spelling of CHANGELOG
```

### 6. Commit with Scope

```
feat(lang): add Polish language
```

### 7. Commit with Multi-paragraph Body and Multiple Footers

```
fix: prevent racing of requests

Introduce a request id and a reference to the latest request. Dismiss
incoming responses other than from the latest request.

Remove timeouts used to mitigate the racing issue but now obsolete.

Reviewed-by: Z
Refs: #123
```

## Specification Details

1. **Must** prefix commits with a `type` followed by optional `scope`, optional
   `!`, then a required colon (`:`) and space.
2. **`fix`** → a bug fix (patch release), **`feat`** → a feature (minor
   release).
3. Scope is a **noun** describing the impacted area in parentheses, e.g.
   `fix(parser): ...`.
4. Description is a short summary, e.g. `fix: array parsing issue with spaces`.
5. Body is free-form text, one blank line after description.
6. Footers (one blank line after body) can follow
   [git trailer convention](https://git-scm.com/docs/git-interpret-trailers).
7. **`BREAKING CHANGE:`** token signals major release. If using a `!` in type
   (like `feat!:`), you can skip the `BREAKING CHANGE:` footer.
8. Additional types (e.g., `docs`, `perf`) **do not** imply version changes
   unless they include a `BREAKING CHANGE`.
9. **Case Insensitivity**: The types (`feat`, `fix`, etc.) aren’t case
   sensitive.
10. `BREAKING-CHANGE:` is synonymous with `BREAKING CHANGE:` in footers.

## Why Use Conventional Commits

- **Changelog Generation**: Automate creation of release notes.
- **Semantic Versioning**: Derive major/minor/patch from commit types.
- **Clarity**: Teammates and stakeholders see at a glance what each commit does.
- **Triggering CI**: Some pipelines can trigger tasks based on commit types
  (`feat` or `fix`).
- **Ease of Contribution**: Encourages smaller, more focused PRs and commits.

## FAQ

### How to Handle Commits in Initial Development?

Act as if the product is already released. People using the software still need
to know what's fixed or changed.

### Are Types Uppercase or Lowercase?

Any casing **may** be used, but pick one and be consistent (commonly lowercase).

### What if a Commit Covers Multiple Types?

Ideally, split it into multiple commits. Each commit should represent one
logical change.

### Does This Slow Down Rapid Development?

It discourages disorganized speed. Conventional Commits helps you scale your
pace while retaining clarity and structure.

### How Does This Relate to SemVer?

- `fix` → **PATCH**
- `feat` → **MINOR**
- Any commit with `BREAKING CHANGE` → **MAJOR**

### What if I Used the Wrong Type?

If still unmerged, use `git rebase -i` to amend. If already released, it depends
on your release process. Tools may miss incorrectly typed commits.

### Are All Contributors Required to Use This?

Not necessarily—if you use a squash-based workflow, maintainers can edit the
final commit message. But encouraging all contributors helps keep history
consistent.

### How to Handle Reverts?

Use a `revert:` type or custom logic. Typically:

```
revert: remove feature X

Refs: commitSha
```

---

**End of Conventional Commits 1.0.0**
