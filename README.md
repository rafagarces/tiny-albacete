# Tiny Albacete
Mapa isometrico pixel-art de Albacete generado a partir de datos abiertos (Catastro y OpenStreetMap). Ver `DECISIONS.md` para decisiones, limites y como se genera. Sitio: https://tiny-albacete.pages.dev


## Rebuild only the bounded3Dzone

The original general map remains intact. The new3Dzone is partial, not an exact reconstruction of the whole city. See published `zona-catedral/sources.html` and each landmark README for attribution and estimated versus observed features.

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-zone.txt
python src/rebuild_zone.py
python -m http.server 8000
```

Open `/zona-catedral/` on the local server. The rebuild works offline after dependencies are installed; it needs no account, paid API, source-photo download, or transient data directory. `data/README.md` records the bounded normalized Catastro input, limitations and licenses. `src/local_frame.py` unifies OSM and Catastro in EPSG:25830. `pilots/teatro-3d/fit_roof.py` separately repeats the historic fit. This runner does not regenerate the legacy general-map image tiles; their existing output is retained. Browser QA still required after visual changes.
