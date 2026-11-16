# Catedral 3D: bounded integration
Original WebGL, no remote runtime dependencies. About 550m wide x500m context. Cathedral geometry: ../pilots/catedral-3d/model.json (754 faces); Casa de Hortelano: ../pilots/hortelano-3d/model.json (1033 faces). Ayuntamiento facade: ../pilots/ayuntamiento-3d/model.json (1492 faces); existing cadastral rear masses retained, not full building reconstruction. Neighbours: 1346 Catastro building parts, estimated heights, no reconstructed facades. Streets derived from OpenStreetMap, ODbL. Six original landmark models under CC BY-SA 4.0; sources and limits in sources.html.

build_zone.py requires Python 3, shapely, Catastro parser output /tmp/tinyalba/bu_parts.json, and included osm-source.json. Regenerate from repository root: python src/build_zone.py. Serve root over HTTP. Open /zona-catedral/; ?l=museo focuses Hortelano; ?l=ayuntamiento focuses the old town hall; ?l=teatro focuses TeatroCirco; ?l=zona opens the wider area.

QA 16 November 2026: 1280x800, 390x844, 320x800 emulated. Chrome WebGL software rendering, not a physical mobile GPU. Rotation, zoom, landmark selector, overview, info/source and general map links checked. No horizontal overflow at 320 px. General map scripts, search and tiles preserved. No claim of a fully reconstructed city.

TeatroCirco facade224faces plus auditorium roof in zonegenerator. Frontmassparts8/9 replaced, remainingcontext retained. Roofis documentedconical; apex/height/shapejunctionestimated.

Palacio Provincial front: pilots/diputacion-3d, Catastro9472604WJ9197S. Partial front only, rear/side/attic/ground-floor details unmodeled. Two2017 CC BY-SA2.0 photo references, elevations estimated. ?l=diputacion selects it. Header and page title follow landmark; overview camera deterministic.

Casa Perona:1906faces, partial north/east facades and dome. Free photos published2006PD and2020CCBYSA2.0, capture dates unconfirmed. Heights and dome registration estimated. Cadastral modern annexes retained. Context extends50m west, no prior coverage lost. ?l=perona.
