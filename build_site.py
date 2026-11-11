# -*- coding: utf-8 -*-
"""Builds the Claude-independent copy of the Gym Card for Vamshi's own Netlify site (https://vamfit-gym.netlify.app).
Vamshi 2026-10-23: "what if I discontinue claude membership... I want the calendar to be independent" -> the page lives on
his free Netlify account, works offline (service worker) and can be added to the iPhone home screen.
Usage: python build_site.py <out_dir>   then deploy <out_dir> to the vamfit-gym Netlify project."""
import sys, os, subprocess, json

HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "docs")
os.makedirs(out, exist_ok=True)
page = os.path.join(out, "index.html")
subprocess.run([sys.executable, os.path.join(HERE, "build_card.py"), page], check=True)

body = open(page, encoding="utf-8").read()
body = body.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
head = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="VamFit">
<meta name="robots" content="noindex, nofollow">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-180.png">
<style>body { padding-bottom: 96px !important }</style>
"""
sw = """<script>
if ("serviceWorker" in navigator) addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
</script>
"""
open(page, "w", encoding="utf-8").write(head + body + sw)

open(os.path.join(out, "sw.js"), "w", encoding="utf-8").write("""// Offline copy for the gym: network first, cached copy when there's no signal.
const C = "vamfit-v12";
self.addEventListener("install", e => { self.skipWaiting(); e.waitUntil(caches.open(C).then(c => c.addAll(["./", "index.html", "icon.svg"]))); });
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(fetch(e.request).then(r => { const k = r.clone(); caches.open(C).then(c => c.put(e.request, k)); return r; })
    .catch(() => caches.match(e.request, { ignoreSearch: true }).then(r => r || caches.match("index.html"))));
});
""")
open(os.path.join(out, "manifest.webmanifest"), "w", encoding="utf-8").write(json.dumps({
    "name": "VamFit Gym Card", "short_name": "VamFit", "start_url": "./", "display": "standalone",
    "background_color": "#0d1311", "theme_color": "#0d7a69",
    "icons": [{"src": "icon.svg", "sizes": "any", "type": "image/svg+xml"}, {"src": "icon-180.png", "sizes": "180x180", "type": "image/png"}]}))
svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180"><rect width="180" height="180" rx="36" fill="#0d7a69"/>
<g fill="#fff"><rect x="34" y="72" width="16" height="36" rx="4"/><rect x="130" y="72" width="16" height="36" rx="4"/>
<rect x="50" y="60" width="16" height="60" rx="4"/><rect x="114" y="60" width="16" height="60" rx="4"/><rect x="66" y="84" width="48" height="12" rx="3"/></g></svg>"""
open(os.path.join(out, "icon.svg"), "w", encoding="utf-8").write(svg)
try:                                   # PNG for the iPhone home-screen icon (iOS ignores SVG touch icons)
    import fitz
    doc = fitz.open(stream=svg.encode(), filetype="svg")
    doc[0].get_pixmap().save(os.path.join(out, "icon-180.png"))
except Exception as e:
    print("png icon skipped:", e)
open(os.path.join(out, "netlify.toml"), "w", encoding="utf-8").write('[build]\n  publish = "."\n  command = ""\n')  # no BOM (Netlify rejects it)
open(os.path.join(out, "_headers"), "w", encoding="utf-8").write("/*\n  X-Robots-Tag: noindex, nofollow\n/sw.js\n  Cache-Control: no-cache\n")
print("site ->", out, sorted(os.listdir(out)))
