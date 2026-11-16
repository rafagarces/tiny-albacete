# Illustrated atlas spatial control

`ilustrado/tiles.json` is the published tile catalog. Its coordinates use a fixed world unit of2048pixels. They do not renormalize when the atlas grows. Existing URL revision2coordinates remain unchanged. Negative coordinates can be added for future north/left growth; no hypothetical tile is published. The viewer uses the published bounds and falls back to the last bundled catalog if the JSON read fails.

Run `python tools/illustrated-atlas/validate.py` to check exact rectangular coverage, no overlaps, source image dimensions and all prior asset hashes. A rectangular coverage check establishes mosaic continuity, not that every drawn building matches reality.

`ilustrado/coverage.geojson` is an approximate ground-plane envelope of the current fixed-camera atlas in longitude/latitude. It uses the real orthographic projection and shared UTM anchor. Ground area is approximately4.168km2. Raised buildings project beyond their ground positions, and interpreted artwork drifts relative to the geometry. Do not use this as a surveyed parcel coverage polygon.

The whole-city target mask is NOT yet fixed. Work is contrasting municipal2016neighborhood plans, SIU planning classes with metadata date01May2025, municipal building footprints and PNOA orthophotography. Five sampled PNOA points returnedJuly2024imagery at25cm. This does not establish a single imagery date for the whole city or current2026facade conditions. Do not compute or publish a city-completion percentage by treating one SIU component as the target. Parks, modern fringes, industrial areas and separate settlements need explicit inclusion/exclusion records.

Sources inspected:
- https://www.albacete.es/es/ciudad/cartoteca/divisiones-administrativas
- https://gerencia-urbanismo.albacete.es/es/pgou-modificaciones-pgou/plan-general-ordenacion-urbana-pgou
- https://mapas.fomento.gob.es/arcgis/rest/services/SIU/CLASES_DE_SUELO/MapServer/0
- https://www.ign.es/wms-inspire/pnoa-ma?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0

A future target-grid ledger should identify every cell by stable column/row, source coverage, target-mask intersection, art state and review state. Target cells are not automatically complete because a cadastral source exists. No current-completion claim is inferred from source-part counts.


## Territorial ledger

`ilustrado/coverage-ledger.json` inventories stable512pixel cells, the inspected25municipal neighborhoods (2016raster), all30disconnected SIUplanning components and named exterior industrial sectors without silently excluding them.169published cells currently intersect the429-cell principal-SIUcandidate. This is a work ledger, NOT city progress or a final city mask. The single SIUcomponent omits portions of the neighborhood plan and parks; do not use429as a final denominator. Individual ground-envelope intersection is now computed from25official vector polygons; this is not certification of drawn buildings or facade accuracy. Citywide current-facade checks have not happened.

## On-demand display

The spatial source catalog remains the authority. Display pyramids load512pixel tiles at the required level, with1pixel overlap. The top display level is lossless relative to decoded source WebPimages; smaller levels are downsampled. Original illustration files remain untouched. Atlas and comparison each use248display tiles at the present extent. OSD4.1requires explicit WebPsupport registration for DZI, safe here because all existing source illustrations already require WebP. Old catalog compatibility is retained.


The expanded principal candidate now uses the actual25municipal neighborhood vectors, not the earlier manual raster trace:12.639917km2union with main SIU,579cells, still provisional. See territorial-sources.md and municipal-vector-provenance.json.
