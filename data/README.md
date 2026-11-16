# Bounded transformed source data

`zone-building-parts.json` holds1362normalized Catastro INSPIRE building-part records used by the bounded3Dzone. Snapshot source downloaded16November2026: https://www.catastro.hacienda.gob.es/INSPIRE/Buildings/02/02900-ALBACETE/A.ES.SDGC.BU.02900.zip . Attribution: Dirección General del Catastro. Conditions: https://www.catastro.hacienda.gob.es/webinspire/documentos/Licencia.pdf . Geometric source only, not address/owner data.

Adaptation: `src/parse_bu.py` extracted the first source ring per feature, normalized it to local EPSG:25830 offsets, rounded coordinates to0.1m, and retained building-part ID, floors/use/area. Then selected mean-vertex x[-300,250],abs(y)<=250,area>=18. This is the exact existing transformed input, not a claim to preserve every interior/multipart ring in original GML or every present-day building. Roof regression tests check these input rings, not the complete original GML. Source fields are not surveyed heights. Unknown floors remain unknown.

OSM extract remains in `zona-catedral/osm-source.json`, attribution/ODbL in published sources. Coordinate conversion uses `src/local_frame.py`, EPSG:25830 minus the original Catastro origin defined in `src/parse_bu.py`. That origin is retained to preserve existing handcrafted registrations. LiDAR roof samples and their license/provenance are in `pilots/teatro-3d/`.
