# Node agent scaffold

Implement a small authenticated HTTP service that:
1. Accepts desired Xray config from the control plane
2. Validates JSON
3. Writes atomically and restarts Xray
4. Reports observed state

Do **not** expose a remote shell.
