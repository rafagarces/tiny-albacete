# Catedral 3D: bounded first integration
Original WebGL, no remote runtime dependencies.500m context. Cathedral geometry comes from ../pilots/catedral-3d/model.json. Neighbours:1240Catastrobuildingparts, heights estimated, no reconstructed facades. Streets derived from OpenStreetMap,ODbL,source and licence in sources.html. Cathedral underCC-BY-SA4.0. Context geometry is already transformed, not raw Catastro redistribution.

build_zone.py requires Python3,shapely,the existing Catastro parser output /tmp/tinyalba/bu_parts.json,and the included osm-source.json. Regenerate from repository root: python src/build_zone.py. Serve root overHTTP. Open /zona-catedral/. Index/source page and noWebGL fallback are plainHTML.

QA16November2026:1280x800,390x800,320x800emulated. ChromeWebGLsoftware rendering,not a physical mobileGPU. Rotation,zoom,reset,area,info/source links and map link checked. General map's scripts,search and existing tiles preserved. Camera framing on320adapted,controls fit320. No claim of a fully reconstructed city.
