// megaZINE inbox: a tiny Cloudflare Worker with one KV namespace (binding INBOX).
//   POST   /inquiry      from megazine.org/contact/ : {name, email, message, proof}  -> stored
//   GET    /inbox        editors only (Authorization: Bearer <ADMIN_KEY>)            -> newest first
//   DELETE /inbox?id=... editors only
// Nothing here is public: the dashboard at /stats/ asks for the key, which is kept for the tab only.
const ORIGIN = "https://megazine.org";
const HOURLY_LIMIT = 5;           // inquiries per visitor address per hour
const KEEP_SECONDS = 60 * 60 * 24 * 365;

const json = (body, status, cors) => new Response(JSON.stringify(body), { status, headers: { ...cors, "content-type": "application/json" } });
const str = (v, max) => (typeof v === "string" ? v.trim().slice(0, max) : "");

function authed(req, env) {
  const a = req.headers.get("authorization") || "", want = "Bearer " + (env.ADMIN_KEY || "");
  if (!env.ADMIN_KEY || a.length !== want.length) return false;
  let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ want.charCodeAt(i);
  return d === 0;
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const cors = { "access-control-allow-origin": ORIGIN, "access-control-allow-methods": "GET,POST,DELETE,OPTIONS",
      "access-control-allow-headers": "content-type,authorization", vary: "origin" };
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });

    if (url.pathname === "/inquiry" && req.method === "POST") {
      if ((req.headers.get("origin") || "") !== ORIGIN) return json({ error: "origin" }, 403, cors);
      const ip = req.headers.get("cf-connecting-ip") || "?", rl = "rl:" + ip;
      const used = parseInt((await env.INBOX.get(rl)) || "0", 10);
      if (used >= HOURLY_LIMIT) return json({ error: "slow down" }, 429, cors);
      let b; try { const t = await req.text(); if (t.length > 12000) throw 0; b = JSON.parse(t); } catch (e) { return json({ error: "bad body" }, 400, cors); }
      const name = str(b.name, 80), email = str(b.email, 160), message = str(b.message, 3000);
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || message.length < 5) return json({ error: "email and message" }, 400, cors);
      const p = b.proof && typeof b.proof === "object" ? b.proof : {};
      const proof = { mode: str(p.mode, 12), shots: +p.shots | 0, ms: +p.ms | 0, fails: +p.fails | 0 };
      const at = Date.now(), id = "msg:" + String(9999999999999 - at).padStart(13, "0") + ":" + Math.random().toString(36).slice(2, 8);
      await env.INBOX.put(id, JSON.stringify({ at, name, email, message, proof }), { expirationTtl: KEEP_SECONDS });
      await env.INBOX.put(rl, String(used + 1), { expirationTtl: 3600 });
      return json({ ok: true }, 200, cors);
    }

    if (url.pathname === "/inbox") {
      if (!env.ADMIN_KEY) return json({ error: "no key set" }, 503, cors);
      if (!authed(req, env)) return json({ error: "no" }, 401, cors);
      if (req.method === "GET") {
        const list = await env.INBOX.list({ prefix: "msg:", limit: 200 });
        const rows = await Promise.all(list.keys.map(async k => { const v = await env.INBOX.get(k.name); return v ? { id: k.name, ...JSON.parse(v) } : null; }));
        return json(rows.filter(Boolean), 200, cors);
      }
      if (req.method === "DELETE") {
        const id = url.searchParams.get("id") || "";
        if (!id.startsWith("msg:")) return json({ error: "id" }, 400, cors);
        await env.INBOX.delete(id); return json({ ok: true }, 200, cors);
      }
    }
    return json({ error: "not found" }, 404, cors);
  }
};
