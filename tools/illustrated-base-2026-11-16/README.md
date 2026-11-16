# Expanded illustrated base,16November2026

This is a build-only snapshot. It does not alter the published rotating3D. The final illustrated rasters are reviewed, interpreted assets rather than deterministic renders.

## Inputs and reproduction

Create a disposable copy of this repository, decompress `zone-building-parts.json.gz` to `data/zone-building-parts.json`, copy `build_zone.py` and `parse_bu.py` to `src/`, and copy `granhotel-layout-model.json` to `pilots/granhotel-3d/model.json`. Run `python src/build_zone.py` with Shapely2.1+andpyproj. All other landmark models, source streets, `local_frame.py` and `catparse.py` come from the repository. Do not run this directly in a production worktree: it overwrites the disposable copy's `zona-catedral/model.json`.

The snapshot contains6479municipal building-part records, including original1362plus1819right,1022bottom 843second-right and1433second-bottom records. Render filters keep6463context parts,699OSM street ways and177259total mesh faces including landmarks. Source URLs and limitations are in `ilustrado/sources.html`. Heights use floor estimates, not current measurements.

## Fixed camera

Capture the repository's WebGL viewer with angle-154degrees,tilt0.60,orthographic scale236,viewport2560x2048and focus(-149.10471439263353,-190.66928932379824)in the shared local metre frame. The previous2560x1536crop is the top1536pixels of that capture. RMS pixel residual for that overlap was0.53/255maximum per channel before illustration. This tests registration, not parcel accuracy.

## Compositing invariant

Final atlas coordinates: original1536x1024at(0,0),first512x1024right strip at(1536,0),2048x512bottom at(0,1024),second512x1536right strip at(2048,0),second2560x512bottom strip at(0,1536). Never regenerate old tiles when adding a strip. World units remain1/2048per pixel. Cathedral detail is a separate illustration.

Catastro INSPIRE data attribution and OSM attribution remain as documented on the source page. The original full GML is not duplicated here.
