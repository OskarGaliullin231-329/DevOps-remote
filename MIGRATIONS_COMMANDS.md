| Command | What it does | When to use |
|---------|-------------|------------|
| `flask db current` | Show current database version | Verify migrations applied |
| `flask db history` | List all migrations in order | Understand version history |
| `flask db upgrade` | Apply all pending migrations | After creating new migration |
| `flask db downgrade` | Revert last migration | Undo recent change |
| `flask db downgrade -1` | Go back 1 migration | Specific rollback |
| `flask db downgrade abc123` | Jump to specific version | Cherry-pick version |
| `flask db migrate -m "text"` | Auto-create migration from models | After editing models.py |
| `flask db revision -m "text"` | Create empty migration for manual editing | Complex changes |
| `flask db merge heads` | Merge conflicting migration branches | Multi-developer scenarios |
| `flask db branches` | Show migration branches | Check branching status |
| `flask db show abc123` | Display specific migration details | Review specific version |
| `flask db upgrade --sql` | Show SQL without executing | Test/review before applying |
| `flask db downgrade --sql` | Show rollback SQL | Verify downgrade won't break things |

---

## Typical Workflow

1. **Edit model** → `nano models.py`
2. **Create migration** → `flask db migrate -m "description"`
3. **Review** → `cat migrations/versions/*latest*.py`
4. **Apply** → `flask db upgrade`
5. **Verify** → `flask db current`
6. **Commit** → `git add migrations/versions/*`

---

## From `app/` directory only:
```bash
cd app
flask db [command]
```
