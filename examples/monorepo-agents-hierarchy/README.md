# Example: Monorepo AGENTS.md Hierarchy

Demonstrates multi-tier instruction resolution in a polyglot monorepo:
```
root/
├── AGENTS.md (Root build commands and global invariants)
├── services/
│   ├── auth-api/
│   │   └── AGENTS.md (Go-specific testing and build tags)
│   └── web-dashboard/
│       └── AGENTS.md (TypeScript/React testing and storybook commands)
```
