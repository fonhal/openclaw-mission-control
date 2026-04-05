# Docs style guide

## Principles

- **默认使用中文。** 本项目文档、任务说明、阶段总结、协作输出默认使用中文。
- **Be concrete.** Prefer commands, examples, and “expected output” over prose.
- **Don’t invent behavior.** If unsure, link to the source file and mark it as “verify”.
- **Optimize for scanning.** Short sections, bullets, and tables.
- **Call out risk.** Anything destructive or security-sensitive should be labeled clearly.

## Language conventions

- Human-facing explanations should default to Chinese.
- Code identifiers, API paths, config keys, protocol fields, and log snippets may remain in English.
- When English terms are necessary, prefer `中文说明（English term）` or `中文说明 + English term`.
- Avoid large blocks of unexplained English in project-facing docs unless preserving an external original is necessary.

## Markdown conventions

- Use sentence-case headings.
- Prefer fenced code blocks with a language (`bash`, `yaml`, `json`).
- For warnings/notes, use simple callouts:

```md
> **Note**
> ...

> **Warning**
> ...
```

## Common templates

### Procedure

1. Prereqs
2. Steps
3. Verify
4. Troubleshooting

### Config reference entry

- **Name**
- **Where set** (`.env`, env var, compose)
- **Default**
- **Example**
- **Notes / pitfalls**
