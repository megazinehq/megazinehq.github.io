// megaZINE inbox: a tiny Cloudflare Worker with one KV namespace (binding INBOX) and one secret (ADMIN_KEY).
//   GET    /challenge    nine drawn squares, what to shoot, and a signed token. The answer is not in the reply.
//   POST   /verify       {token, mask}: which squares were shot. Right, once, and not too fast -> a pass.
//   POST   /inquiry      {pass, name, email, message, proof} from megazine.org/contact/ -> stored, and Slack is pinged (SLACK_WEBHOOK)
//   GET    /inbox        editors only (Authorization: Bearer <ADMIN_KEY>) -> newest first
//   DELETE /inbox?id=... editors only
// The page cannot grade its own test: the squares are drawn here, the answer stays here, and nothing is stored
// without a pass that this Worker signed. Every token works once.
import { squares } from "../../contact/squares.js";      // the drawings, shared with the page's preview

const SITE = "https://megazine.org";
const INQUIRIES_PER_HOUR = 5, TRIES_PER_HOUR = 30;
const MIN_SOLVE_MS = 1500, CHALLENGE_MS = 10 * 60e3, PASS_MS = 45 * 60e3;
const KEEP_SECONDS = 60 * 60 * 24 * 365;

const json = (body, status, cors) => new Response(JSON.stringify(body), { status, headers: { ...cors, "content-type": "application/json", "cache-control": "no-store" } });
const str = (v, max) => (typeof v === "string" ? v.trim().slice(0, max) : "");
const same = (a, b) => { if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) return false; let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i); return d === 0; };
const enc = new TextEncoder();
async function sign(env, msg) {
  const key = await crypto.subtle.importKey("raw", enc.encode("captcha:" + env.ADMIN_KEY), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return [...new Uint8Array(await crypto.subtle.sign("HMAC", key, enc.encode(msg)))].map(b => b.toString(16).padStart(2, "0")).join("");
}
const nonce = () => crypto.randomUUID().replace(/-/g, "");
async function overLimit(env, key, max) {
  const used = parseInt((await env.INBOX.get(key)) || "0", 10);
  if (used >= max) return true;
  await env.INBOX.put(key, String(used + 1), { expirationTtl: 3600 }); return false;
}
// a token is "<time>.<nonce>.<signature>"
function parts(tok) { const p = str(tok, 200).split("."); return p.length === 3 && /^\d{13}$/.test(p[0]) && /^[0-9a-f]{32}$/.test(p[1]) ? { t: +p[0], n: p[1], sig: p[2] } : null; }

// Tell the editors on Slack, the way the BBS does. SLACK_WEBHOOK is an incoming-webhook address; without it, nothing is sent.
const slackSafe = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
async function ping(env, m) {
  if (!env.SLACK_WEBHOOK) return;
  const text = `:envelope: *megaZINE note* from ${slackSafe(m.name || "no name")} (${slackSafe(m.email)})\n>${slackSafe(m.message.slice(0, 1200)).replace(/\n/g, "\n>")}\n_Read and reply: megazine.org/stats/_`;
  try { await fetch(env.SLACK_WEBHOOK, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ text }) }); } catch (e) { /* the note is stored either way */ }
}

function isEditor(req, env) { return !!env.ADMIN_KEY && same(req.headers.get("authorization") || "", "Bearer " + env.ADMIN_KEY); }

export default {
  async fetch(req, env, ctx) {
    const url = new URL(req.url), site = env.SITE || SITE;      // env.SITE is only for trying it out locally
    const cors = { "access-control-allow-origin": site, "access-control-allow-methods": "GET,POST,DELETE,OPTIONS",
      "access-control-allow-headers": "content-type,authorization", vary: "origin" };
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    if (!env.ADMIN_KEY) return json({ error: "no key set" }, 503, cors);
    const ip = req.headers.get("cf-connecting-ip") || "?", fromSite = (req.headers.get("origin") || "") === site;
    const body = async () => { try { const t = await req.text(); if (t.length > 12000) return null; const b = JSON.parse(t); return b && typeof b === "object" ? b : null; } catch (e) { return null; } };

    if (url.pathname === "/challenge" && req.method === "GET") {
      const { ask, tiles, mask } = squares(), t = Date.now(), n = nonce();
      return json({ token: `${t}.${n}.${await sign(env, `c|${t}|${n}|${mask}`)}`, ask, tiles }, 200, cors);
    }

    if (url.pathname === "/verify" && req.method === "POST") {
      if (!fromSite) return json({ error: "origin" }, 403, cors);
      if (await overLimit(env, "try:" + ip, TRIES_PER_HOUR)) return json({ error: "slow down" }, 429, cors);
      const b = await body(), c = b && parts(b.token), mask = b ? b.mask : -1;
      if (!c || !Number.isInteger(mask) || mask < 0 || mask > 511) return json({ ok: false, why: "bad" }, 200, cors);
      const age = Date.now() - c.t;
      if (age > CHALLENGE_MS || age < 0) return json({ ok: false, why: "expired" }, 200, cors);
      if (await env.INBOX.get("n:" + c.n)) return json({ ok: false, why: "used" }, 200, cors);
      await env.INBOX.put("n:" + c.n, "1", { expirationTtl: 900 });                 // one go per set of squares, right or wrong
      if (age < MIN_SOLVE_MS) return json({ ok: false, why: "fast" }, 200, cors);
      if (!same(await sign(env, `c|${c.t}|${c.n}|${mask}`), c.sig)) return json({ ok: false, why: "wrong" }, 200, cors);
      const t = Date.now(), n = nonce();
      return json({ ok: true, pass: `${t}.${n}.${await sign(env, `p|${t}|${n}`)}` }, 200, cors);
    }

    if (url.pathname === "/inquiry" && req.method === "POST") {
      if (!fromSite) return json({ error: "origin" }, 403, cors);
      const b = await body(); if (!b) return json({ error: "bad body" }, 400, cors);
      const p = parts(b.pass);
      if (!p || Date.now() - p.t > PASS_MS || !same(await sign(env, `p|${p.t}|${p.n}`), p.sig) || await env.INBOX.get("n:" + p.n)) return json({ error: "pass" }, 401, cors);
      const name = str(b.name, 80), email = str(b.email, 160), message = str(b.message, 3000);
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || message.length < 5) return json({ error: "email and message" }, 400, cors);
      if (await overLimit(env, "rl:" + ip, INQUIRIES_PER_HOUR)) return json({ error: "slow down" }, 429, cors);
      const q = b.proof && typeof b.proof === "object" ? b.proof : {};
      const proof = { mode: str(q.mode, 12), shots: +q.shots | 0, ms: +q.ms | 0, fails: +q.fails | 0 };   // what the page says happened; a curiosity, not evidence
      const at = Date.now(), id = "msg:" + String(9999999999999 - at).padStart(13, "0") + ":" + nonce().slice(0, 6);
      await env.INBOX.put(id, JSON.stringify({ at, name, email, message, proof }), { expirationTtl: KEEP_SECONDS });
      await env.INBOX.put("n:" + p.n, "1", { expirationTtl: 3600 });
      const told = ping(env, { name, email, message }); if (ctx && ctx.waitUntil) ctx.waitUntil(told); else await told;
      return json({ ok: true }, 200, cors);
    }

    if (url.pathname === "/inbox") {
      if (!isEditor(req, env)) return json({ error: "no" }, 401, cors);
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
