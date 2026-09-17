/**
 * SF-Panel control-plane scaffold for Cloudflare Workers.
 * This is intentionally incomplete: implement API parity against the
 * Python handlers and wire D1 migrations before production use.
 */
export interface Env {
  DB: D1Database;
  NODE_TOKEN?: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === "/healthz") {
      return Response.json({ ok: true, runtime: "workers", app: "SF-Panel" });
    }
    return new Response("SF-Panel Workers scaffold — see docs/DEPLOY_CLOUDFLARE.md", {
      status: 501,
      headers: { "content-type": "text/plain; charset=utf-8" },
    });
  },
};
