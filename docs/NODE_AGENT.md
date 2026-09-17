# Node agent (Xray host)

Least-privilege HTTP agent on the VPS that applies inbound configs and reports status.

## Contract (v1)
- `POST /v1/apply` — body: desired Xray JSON; header: `Authorization: Bearer <node_token>`
- `GET /v1/status` — running version, last apply result
- `POST /v1/restart`

No shell execution endpoint. Replay protection via `X-Request-Id` + short TTL nonce store recommended.

Network: bind to localhost or private interface; expose via reverse proxy with mTLS or Cloudflare Tunnel.
