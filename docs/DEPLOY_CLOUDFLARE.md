# Cloudflare hybrid deployment

> Research date: 2026-09-17 — based on official Cloudflare Workers / D1 documentation.

## What runs where

| Component | Runtime |
|-----------|---------|
| Web UI static assets | Workers Assets / Pages |
| Control API + Telegram webhook | Workers (TypeScript recommended) |
| Persistent panel data | D1 |
| Xray core | **VPS only** via `node-agent` |

## Why not full Workers-native?
Standard Workers do not support:
- Long-lived subprocesses (Xray)
- Arbitrary inbound TCP listeners
- Local SQLite files with multi-writer threads

Claiming “fully Workers-compatible Xray” would be false.

## Scaffold
See `/workers` (Wrangler config stub) and `/node-agent` (authenticated management agent contract).

## Steps (outline)
1. Create D1 database and run migrations (from existing SQLite export — see `docs/MIGRATION.md`).
2. `wrangler secret put ADMIN_PASS_HASH` etc.
3. Deploy Workers; set Telegram webhook to `https://<worker>/tg/webhook` with secret header.
4. Install node-agent on VPS; configure mutual auth token.
5. Point panel “node URL” to agent endpoint (HTTPS + allowlist IP).

Rollback: keep VPS mode as fallback; D1 export → SQLite import path documented in MIGRATION.md.
