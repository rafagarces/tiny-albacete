# Catedral 3D: bounded integration
Original WebGL, no remote runtime dependencies. About 500 m context. Cathedral geometry: ../pilots/catedral-3d/model.json (754 faces); Casa de Hortelano: ../pilots/hortelano-3d/model.json (1033 faces). Neighbours: 1238 Catastro building parts, estimated heights, no reconstructed facades. Streets derived from OpenStreetMap, ODbL. Both original landmark models under CC BY-SA 4.0; sources and limits in sources.html.

build_zone.py requires Python 3, shapely, Catastro parser output /tmp/tinyalba/bu_parts.json, and included osm-source.json. Regenerate from repository root: python src/build_zone.py. Serve root over HTTP. Open /zona-catedral/; ?l=museo focuses Hortelano; ?l=zona opens the wider area.

QA 16 November 2026: 1280x800, 390x844, 320x800 emulated. Chrome WebGL software rendering, not a physical mobile GPU. Rotation, zoom, landmark selector, overview, info/source and general map links checked. No horizontal overflow at 320 px. General map scripts, search and tiles preserved. No claim of a fully reconstructed city.
