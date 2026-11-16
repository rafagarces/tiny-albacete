# Expanded illustrated base,16November2026

This is a build-only snapshot. It does not alter the published rotating3D. The final illustrated rasters are reviewed, interpreted assets rather than deterministic renders.

## Inputs and reproduction

Create a disposable copy of this repository, decompress `zone-building-parts.json.gz` to `data/zone-building-parts.json`, copy `build_zone.py` and `parse_bu.py` to `src/`, and copy `granhotel-layout-model.json` to `pilots/granhotel-3d/model.json`. Run `python src/build_zone.py` with Shapely2.1+. All other landmark models, source streets, `local_frame.py` and `catparse.py` come from the repository. Do not run this directly in a production worktree: it overwrites the disposable copy's `zona-catedral/model.json`.

The snapshot contains5046municipal building-part records, including original1362plus1819right,1022bottom and843second-right records. Render filters keep5030context parts,699OSM street ways and143952total mesh faces including landmarks. Source URLs and limitations are in `ilustrado/sources.html`. Heights use floor estimates, not current measurements.

## Fixed camera

Capture the repository's WebGL viewer with angle-154degrees,tilt0.60,orthographic scale177,viewport2560x1536and focus(-55.188915935596825,-144.863493835118)in the shared local metre frame. The previous2048x1536crop is the left2048pixels of that capture. RMS pixel residual for that overlap was0.59/255before illustration. This tests registration, not parcel accuracy.

## Compositing invariant

Final atlas coordinates: original1536x1024at(0,0),first512x1024right strip at(1536,0),2048x512bottom at(0,1024),second512x1536right strip at(2048,0). Never regenerate old tiles when adding a strip. World units remain1/2048per pixel. Cathedral detail is a separate illustration.

Catastro INSPIRE data attribution and OSM attribution remain as documented on the source page. The original full GML is not duplicated here.
