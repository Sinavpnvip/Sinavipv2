# Migration

## From ≤2.0.x (seed port bug)
On startup, `repair_seed_port_bug()` fixes rows where `enable > 1` and `internal_port == 1` by swapping values. Ambiguous rows are left alone and logged.

## Default credentials
If still using legacy `sinamzxr`/`Sina990`, change password immediately (rotates session secret).

## VPS → Cloudflare hybrid
1. Export backup from panel (`/api/backup`).
2. Validate JSON (`format` field).
3. Import into D1 via provided migration script (dry-run first).
4. Cut over Telegram webhook only after dual-write freeze.
5. Keep old VPS read-only until reconciliation of balances/orders.

## Rollback
Restore previous SQLite file from verified backup; secret will need re-login after any restore that ran import_all.
