# VPS / Docker deployment

## Quick start (Docker)

```bash
git clone <this-repo> && cd SF-panel
cp .env.example .env   # set ADMIN_USER, ADMIN_PASS, ports
docker compose up -d --build
```

Open `http://SERVER:2087` — complete setup if env credentials were not set.

## Environment

| Variable | Default | Notes |
|----------|---------|-------|
| `DEPLOY_MODE` | auto | `vps` or `paas` |
| `PANEL_PORT` / `PORT` | 2087 | Public panel port |
| `ADMIN_USER` / `ADMIN_PASS` | — | Optional first-run provisioning |
| `TG_BOT_TOKEN` | — | Telegram bot |
| `TG_ADMIN_IDS` | — | Comma-separated chat IDs |
| `PUBLIC_DOMAIN` | — | Domain/IP for subscription links |
| `TRUSTED_PROXIES` | — | CIDRs allowed to set XFF |
| `SF_DATA_DIR` | `./data` | Persistent volume |

## Upgrade
1. Backup via panel or copy `data/`.
2. Pull new image / code.
3. Restart; `repair_seed_port_bug` runs automatically if needed.

## Health
`GET /healthz` → `{"ok": true, ...}`
