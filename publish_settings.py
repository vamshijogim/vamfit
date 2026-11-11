# -*- coding: utf-8 -*-
"""Locks (encrypts) my-settings\\vamfit-settings.json into docs\\settings.enc.json so every device picks it up by itself.
Run: python make_my_settings.py  ->  python publish_settings.py  ->  commit + push.
The key lives ONLY in my-settings\\sync-key.txt (never in the repo). Each device gets it once via the link printed below.
Needs: pip install cryptography"""
import os, json, time, base64, secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HERE = os.path.dirname(os.path.abspath(__file__))
MY = os.path.join(HERE, "my-settings")
SITE = "https://vamshijogim.github.io/vamfit/"
kp = os.path.join(MY, "sync-key.txt")
if not os.path.exists(kp):  # first run only; replacing the key means opening the new link on every device again
    open(kp, "w").write(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip("="))
k = open(kp).read().strip()
key = base64.urlsafe_b64decode(k + "=" * (-len(k) % 4))
data = open(os.path.join(MY, "vamfit-settings.json"), encoding="utf-8").read()
json.loads(data)  # must be valid JSON
iv = secrets.token_bytes(12)
ct = AESGCM(key).encrypt(iv, data.encode("utf-8"), None)
out = {"v": 1, "rev": int(time.time()), "iv": base64.b64encode(iv).decode(), "ct": base64.b64encode(ct).decode()}
open(os.path.join(HERE, "docs", "settings.enc.json"), "w").write(json.dumps(out))
print("wrote docs/settings.enc.json rev", out["rev"])
print("device setup link is in my-settings/sync-key.txt (open SITE + '#k=' + key once per device)")
