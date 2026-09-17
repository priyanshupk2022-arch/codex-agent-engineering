# Sandbox Execution Boundaries & Approval Policies

Codex operates terminal commands inside an OS-enforced execution sandbox. Configuring the sandbox and approval policies correctly balances autonomous development speed with host security.

---

## 1. Sandbox Isolation Modes

Codex provides three standard sandbox levels configured in `.codex/config.toml`:

```toml
[sandbox]
mode = "workspace-write" # Options: "read-only", "workspace-write", "danger-full-access"
allowed_network_hosts = ["github.com", "registry.npmjs.org", "pypi.org"]
```

### Mode Breakdown
1. **`read-only`**:
   - Filesystem: Read-only access to workspace. No write operations permitted.
   - Network: Completely blocked.
   - Ideal for: Deep research, initial repository audits, security scanning, pull request reviews.
2. **`workspace-write`** (Default & Recommended):
   - Filesystem: Read/write restricted strictly to the workspace root directory and system temp.
   - Network: Limited to package registries and git origins.
   - Ideal for: Everyday feature implementation, bug fixing, test running, refactoring.
3. **`danger-full-access`**:
   - Filesystem: Unrestricted host access.
   - Network: Unrestricted host access.
   - Danger: Destructive operations outside repo boundaries (e.g. accidental `rm -rf /` or credential leakage) can occur. Never enable in multi-tenant or automated CI without container boundaries.

---

## 2. Approval Policies

Approval policies govern when Codex must pause execution and request human consent:

| Policy | Trigger Condition | Interruption Rate | Safety Level | Recommended Use |
| :--- | :--- | :--- | :--- | :--- |
| **`on-request`** | Only when an action exceeds declared safe boundaries (e.g. external network, package installation). | Low | High | Standard interactive developer pairing. |
| **`untrusted`** | Every single shell command or state mutation prompts for consent. | Very High | Maximum | High-risk production environments or reviewing untrusted code. |
| **`never`** | All actions execute automatically without prompting. | Zero | Requires Sandboxing | Isolated containerized CI/CD benchmarking runners. |

---

## 3. `--approve-for-me` Flag Behavior
In interactive CLI sessions, `--approve-for-me` activates a heuristic pre-approver that evaluates commands against a safety allowlist (e.g., `git status`, `git diff`, `pytest`, `npm test`) while still prompting on dangerous or irreversible commands (e.g., `git push --force`, `rm -rf`).
