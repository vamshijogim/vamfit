# -*- coding: utf-8 -*-
"""One-time patch: VamFit loads Vamshi's settings automatically from docs/settings.enc.json (encrypted).
The key reaches each device once through a link ending in #k=...; it is kept in that browser and never sent anywhere."""
import os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, "gym_card_template.html")
s = open(p, encoding="utf-8").read()
assert "syncSettings" not in s, "already patched"
shutil.copy(p, os.path.join(HERE, "gym_card_template.before-step5.html"))

KEY_GRAB = '''// Auto-sync key: arrives once as #k=..., kept on this device only, then removed from the address bar.
(function () {
  const m = /^#k=([A-Za-z0-9_-]{43})$/.exec(location.hash || "");
  try { if (m) { localStorage.setItem("vamfitKey", m[1]); history.replaceState(null, "", location.pathname + location.search); } } catch (e) {}
})();
const SETTINGS_KEY = "vamfitSettings";'''
s = s.replace('const SETTINGS_KEY = "vamfitSettings";', KEY_GRAB, 1)

SYNC = '''// Auto-sync: settings.enc.json is published next to the page (AES-GCM). A newer "rev" replaces this device's settings.
async function syncSettings() {
  let k = null; try { k = localStorage.getItem("vamfitKey"); } catch (e) {}
  if (!k || !window.crypto || !crypto.subtle) return;
  try {
    const r = await fetch("settings.enc.json?t=" + Date.now(), { cache: "no-store" }); if (!r.ok) return;
    const f = await r.json(); const last = +(localStorage.getItem("vamfitRev") || 0); if (!(f.rev > last)) return;
    const b = x => { x = x.replace(/-/g, "+").replace(/_/g, "/"); while (x.length % 4) x += "="; return Uint8Array.from(atob(x), c => c.charCodeAt(0)); };
    const key = await crypto.subtle.importKey("raw", b(k), "AES-GCM", false, ["decrypt"]);
    const pt = await crypto.subtle.decrypt({ name: "AES-GCM", iv: b(f.iv) }, key, b(f.ct));
    S = merge(DEFAULTS, JSON.parse(new TextDecoder().decode(pt))); saveSettings();
    localStorage.setItem("vamfitRev", String(f.rev)); render(); loadWx();
  } catch (e) {}
}
syncSettings();
document.addEventListener("visibilitychange", () => { if (!document.hidden) syncSettings(); });
render();
</script>'''
assert s.count("render();\n</script>") == 1
s = s.replace("render();\n</script>", SYNC, 1)
open(p, "w", encoding="utf-8").write(s)
print("patched")
