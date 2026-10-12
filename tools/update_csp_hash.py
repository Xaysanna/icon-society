#!/usr/bin/env python3
"""Recalcule le hash sha256 du bloc <script> inline et met a jour la CSP.

A lancer apres toute modification du script inline de index.html :
    python3 tools/update_csp_hash.py
Sinon le navigateur refuse d'executer le script et le workflow Archive Guard echoue.
"""
import re, hashlib, base64, sys, pathlib

f = pathlib.Path(__file__).resolve().parent.parent / 'index.html'
html = f.read_text(encoding='utf-8')

scripts = re.findall(r'<script>(.*?)</script>', html, re.S)
if len(scripts) != 1:
    sys.exit(f'Erreur : {len(scripts)} blocs <script> inline (1 attendu).')

body = scripts[0].replace('\r\n', '\n').replace('\r', '\n')
new_hash = 'sha256-' + base64.b64encode(hashlib.sha256(body.encode()).digest()).decode()

m = re.search(r"'sha256-[A-Za-z0-9+/=]+'", html)
if not m:
    sys.exit('Erreur : aucun hash sha256 trouve dans la CSP.')
old = m.group(0)

if old == f"'{new_hash}'":
    print('Deja a jour :', new_hash)
else:
    f.write_text(html.replace(old, f"'{new_hash}'", 1), encoding='utf-8')
    print('Hash mis a jour :', new_hash)
