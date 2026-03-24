# CLAUDE.md — CLI-Anything API Harness Reference

## What is CLI-Anything

Framework for building agent-usable CLI wrappers ("harnesses") around software and APIs. Each harness is a standalone pip-installable Python Click package living in `<software>/agent-harness/`. Supports one-shot CLI commands and interactive REPL mode. Follows a 7-phase methodology documented in `cli-anything-plugin/HARNESS.md`.

## Standard Harness Directory Structure

```
<software>/agent-harness/
├── setup.py                        # Package config (entry_points, deps)
├── <SOFTWARE>.md                   # SOP document
└── cli_anything/<software>/
    ├── __init__.py
    ├── __main__.py                 # python -m entry
    ├── <software>_cli.py           # Main Click CLI (groups, commands, REPL)
    ├── core/                       # Business logic modules
    ├── utils/
    │   ├── <software>_backend.py   # API/subprocess wrapper
    │   └── repl_skin.py            # Copied from cli-anything-plugin/repl_skin.py
    ├── skills/SKILL.md             # Agent-discoverable skill definition
    ├── tests/
    │   ├── TEST.md                 # Test plan + results
    │   ├── test_core.py            # Unit tests
    │   └── test_full_e2e.py        # E2E tests
    └── README.md
```

## API Harness Pattern

### Backend Module (`utils/<software>_backend.py`)

- `API_BASE` from env var with sensible default
- `ENV_API_KEY` / `ENV_API_TOKEN` constant naming the env var
- Config dir at `~/.config/cli-anything-<software>/`
- Auth chain: CLI flag → env var → config file
- `_require_api_key()` raises `RuntimeError` with setup instructions
- `_make_auth_headers()` returns Bearer token header dict
- Generic HTTP helpers or per-endpoint functions
- Error handling must redact credentials from output
- Reference: `novita/agent-harness/cli_anything/novita/utils/novita_backend.py`

### CLI Module (`<software>_cli.py`)

- `@click.group(invoke_without_command=True)` with `--json` and `--token`/`--api-key` options
- Default to REPL when no subcommand is given
- `handle_error` decorator for consistent error output
- Global `_json_output` and `_repl_mode` flags
- `output()` function that respects `--json` flag
- Command groups per resource/domain
- Reference: `novita/agent-harness/cli_anything/novita/novita_cli.py`

### Session (`core/session.py`)

- `_locked_save_json()` for atomic file writes
- Stores at `~/.cli-anything-<software>/session.json`
- Reference: `novita/agent-harness/cli_anything/novita/core/session.py`

### REPL (uses `repl_skin.py` copied from `cli-anything-plugin/repl_skin.py`)

- `ReplSkin("<software>", version="1.0.0")`
- Auto-detects `SKILL.md`
- Command dispatch via `cli.main(parts, standalone_mode=False)`
- **repl_skin.py must be a superset** — when copying, keep ALL existing accent colors from other harnesses and add your own. Check the novita copy for the most complete `_ACCENT_COLORS` dict as reference.

## Key Conventions

- `--json` flag on root group for machine-readable output
- Errors: `RuntimeError` for user-facing, `ValueError` for logic errors
- Auth: never hardcode tokens; use env vars or config files
- Config files: `chmod 0o600` for security
- Dependencies: `click>=8.0.0`, `requests>=2.28.0`, `prompt-toolkit>=3.0.0`
- Python: `>=3.10`
- All commands must work both in REPL and one-shot mode

## setup.py Pattern

```python
with open("cli_anything/<software>/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cli-anything-<software>",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "cli-anything-<software>=cli_anything.<software>.<software>_cli:main"
        ]
    },
    package_data={"cli_anything.<software>": ["skills/*.md"]},
    install_requires=["click>=8.0.0", "requests>=2.28.0", "prompt-toolkit>=3.0.0"],
)
```

## Registry

Add entry to `registry.json` at the project root with these fields:
- `name`, `display_name`, `version`, `description`
- `requires`, `install_cmd`, `entry_point`
- `skill_md`, `category`, `contributor`
- `contributor_url` — **must not be empty**; use GitHub profile URL (e.g. `https://github.com/<user>`)

## Testing

- `test_core.py` — Unit tests with mocked responses, no external deps
- `test_full_e2e.py` — Real API/tool integration tests
- `TEST.md` — Write test plan during Phase 4, append results during Phase 6
- Include Click `CliRunner` tests for CLI-level coverage (`--help`, `--json` mode, error cases)
- Do not leave development scratchpads (e.g. `test.md`) in the repo — consolidate into `TEST.md`

## Key Reference Files

| File | Purpose |
|------|---------|
| `cli-anything-plugin/HARNESS.md` | Full 7-phase methodology |
| `novita/agent-harness/` | Best API harness example |
| `ollama/agent-harness/` | Another REST API harness |
| `adguardhome/agent-harness/` | Network API harness |
| `cli-anything-plugin/repl_skin.py` | Shared REPL UI component |
| `CONTRIBUTING.md` | Contribution guidelines |

## Contributing a Harness — Workflow

Upstream repo: `HKUDS/CLI-Anything` (GitHub).
Fork: `galke7/CLI-Anything` (GitHub).
Fork remote name: `fork`.

### PR Checklist (learned from PR #131 review)

Before opening PR against `HKUDS/CLI-Anything:main`:

- [ ] **Rebase onto latest `origin/main`** — `registry.json` and `.gitignore` are frequently edited upstream; always `git fetch origin main && git rebase origin/main` before pushing
- [ ] `<SOFTWARE>.md` — SOP document at `<software>/agent-harness/<SOFTWARE>.md`
- [ ] `SKILL.md` — must use **multi-line scalar** frontmatter format (`name: >-\n  cli-anything-<software>`), only `name` and `description` fields (no `version`/`category`)
- [ ] `setup.py` — must include `long_description` read from `README.md` (see setup.py pattern above)
- [ ] `registry.json` — entry with **non-empty `contributor_url`** (GitHub profile URL)
- [ ] `repl_skin.py` — copy must be a **superset** of all accent colors from other harnesses (check novita's copy for most complete `_ACCENT_COLORS`), plus add your own harness color
- [ ] Tests — `test_core.py` unit tests + Click `CliRunner` tests, `test_full_e2e.py` with real token
- [ ] `README.md` — at `cli_anything/<software>/README.md`
- [ ] **No scratchpads** — remove any `test.md` or development logs; consolidate into `TEST.md`
- [ ] **Security** — password/secret CLI args should offer `--<arg>-stdin` alternative to avoid shell history exposure
- [ ] Commit messages — conventional format (`feat:`, `test:`, `docs:`, `fix:`)

### Push and PR Flow

```bash
# Rebase onto latest upstream
git fetch origin main && git rebase origin/main
# Resolve conflicts (registry.json, .gitignore are common)
git push fork <branch> --force-with-lease

# Open PR
gh pr create --repo HKUDS/CLI-Anything \
  --title "feat: add <Software> harness" \
  --body "..."
```

### Notes

- Use `python -m pytest` (not bare `pytest`) to avoid namespace package import errors
- Use `python -m cli_anything.<software>` as entry point (console_scripts may fail with uv editable installs)
- RMS API token stored in `.env` at project root
