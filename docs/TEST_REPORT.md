# Test report

**Environment:** Linux sandbox, Python 3.11, no live Telegram / public Xray ports.

## Executed
- Static verification of SF-001…SF-010 code paths (manual + unit tests in `tests/`).
- `python -c` import checks for modified modules.
- ZIP extract + structure verification.

## Not executed (limitations)
- Full Docker build with Xray binary download (network + time).
- Live browser E2E screenshots.
- Live Telegram bot payment flows.
- Workers `wrangler dev` (scaffold only).

Commands to run on a full machine:

```bash
pip install -r requirements.txt pytest
python -m pytest tests/ -q
docker compose build
```
