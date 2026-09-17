# Architecture

## Modes

| Mode | Control plane | Xray | Data |
|------|---------------|------|------|
| **VPS / Docker** (primary) | aiohttp on VPS | Same host (subprocess) | SQLite under `SF_DATA_DIR` |
| **PaaS** | aiohttp + L4 router | Same process tree, internal ports | SQLite volume |
| **Cloudflare hybrid** | Workers + D1 (control API + Telegram webhook) | Separate VPS **node agent** | D1 for panel; SQLite on node |

## Trust boundaries
- Browser → Panel API (Bearer token HMAC)
- Telegram → Bot (token in settings / secrets)
- Panel → Xray (local subprocess or authenticated agent)
- Only trusted proxies may inject `X-Forwarded-For`

## Official references (retrieved 2026-09-17)
- Cloudflare Workers limits & bindings: https://developers.cloudflare.com/workers/
- D1: https://developers.cloudflare.com/d1/
- Durable Objects / Queues for financial correctness when needed

A pure Workers-native Xray is **not** supported (no arbitrary TCP listeners / subprocesses in standard Workers).
