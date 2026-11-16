# Expanded illustrated base,16November2026

This is a build-only snapshot. It does not alter the published rotating3D. The final illustrated rasters are reviewed, interpreted assets rather than deterministic renders.

## Inputs and reproduction

Create a disposable copy of this repository, decompress `zone-building-parts.json.gz` to `data/zone-building-parts.json`, decompress `osm-source.json.gz` to `zona-catedral/osm-source.json`, copy `build_zone.py` and `parse_bu.py` to `src/`, and copy `granhotel-layout-model.json` to `pilots/granhotel-3d/model.json`. Run `python src/build_zone.py` with Shapely2.1+andpyproj. All other landmark models, source streets, `local_frame.py` and `catparse.py` come from the repository. Do not run this directly in a production worktree: it overwrites the disposable copy's `zona-catedral/model.json`.

The current snapshot contains10190municipal building-part records. Render filters keep10174context parts,2344OSM street ways and283560total mesh faces including landmarks. The6479-part version preceded the third lower extension. Source URLs and limitations are in `ilustrado/sources.html`. Heights use floor estimates, not current measurements.

## Fixed camera

Capture the repository's WebGL viewer with angle-154degrees,tilt0.60,orthographic scale236,viewport2560x2048and focus(-149.10471439263353,-190.66928932379824)in the shared local metre frame. The previous2560x1536crop is the top1536pixels of that capture. RMS pixel residual for that overlap was0.53/255maximum per channel before illustration. This tests registration, not parcel accuracy.

## Compositing invariant

Final atlas coordinates: original1536x1024at(0,0),first512x1024right strip at(1536,0),2048x512bottom at(0,1024),second512x1536right strip at(2048,0),second2560x512bottom strip at(0,1536). Never regenerate old tiles when adding a strip. World units remain1/2048per pixel. Cathedral detail is a separate illustration.

Catastro INSPIRE data attribution and OSM attribution remain as documented on the source page. The original full GML is not duplicated here.


## Third right strip

The same archived base also covers the512x2048strip at global x2560. Capture3072x2048,scale236,angle-154,tilt.60,focus(-123.2408167310922,-243.6981380554508). Overlap against the prior2560x2048base RMS<=.60/255per channel. Atlas now3072x2048,world bounds(0,0,1.5,1),keeping1/2048units per pixel.


## Third bottom strip and expanded streets

Current build snapshot contains10190building-part records,10174rendered context parts,2376OSM source elements,2344road ways and283560total faces. Additional3711source parts support the expanded geometry extent; these counts do not certify illustrated building fidelity. Decompress `osm-source.json.gz` into the disposable copy's `zona-catedral/osm-source.json` as well as the prior instructions. Previous street ways win on duplicate IDs so their geometry is not replaced. The new ways were read from the public OSM map API on16November2026 in three bounded requests, stored without user information.

Capture3072x2560,angle-154,tilt.60,scale295,focus(-217.156615188007,-289.503933543245)in the same local metre frame. Top2048pixels register with previous3072x2048base with RMS<=1.59/255per channel after expanded streets; this is camera/base registration, not parcel accuracy. Add3072x512at global(0,2048),world(0,1),width1.5,height.25. Atlas3072x2560,worldbounds(0,0,1.5,1.25). Preserve all prior illustrated tiles.


## First left strip

Atlas now spans world[-.25,0,1.5,1.25],3584x2560pixels. Negative world coordinates extend rather than shift the existing map. Append512x2560atworld(-.25,0). Capture3584x2560,scale295,focus(-243.020512845,-236.475084811),same angle-154/tilt.60. Geometry source parts unchanged10190/10174rendered;2852OSMelements/2817roadways/289498faces. Additional476source ways preserved existing IDs; two small public OSM API requests16November2026, no contact or user data. Existing base overlap after street additions RMS<=1.78/255per channel.


## First top strip

Atlas bounds[-.25,-.25,1.5,1.25],3584x3072pixels. Added3584x512at(-.25,-.25). Capture3584x3072,scale354,focus(-149.10471439,-190.66928932),angle-154,tilt.60. Additional4113municipalparts yield14303records/14287renderedparts.3731OSMelements/3666roadways/404527faces. Street additions preserve oldIDs; no claim of current building facade accuracy. Existing base overlapRMS<=0.464/255perchannel. All prior art remains untouched.


## Fourth bottom strip

Atlasbounds[-.25,-.25,1.5,1.5],3584x3584pixels. Add3584x512atworld(-.25,1.25). Capture3584x3584,scale413,focus(-243.02051285,-236.47508481),sameangle-154/tilt.60. Source14303records/14287renderedparts,4042OSMelements/3973roadways/408069faces. Sourcegeometrynotcertifiedfacades. ExistingbaseoverlapRMS<=.666/255perchannel.


## Second top strip

Atlasbounds[-.25,-.5,1.5,1.5],3584x4096pixels. Add3584x512atworld(-.25,-.5). Capture3584x4096,scale472,focus(-149.10471439,-190.66928932),sameangle-154/tilt.60. Source14303records/14287renderedparts,4484OSMelements/4409roadways/413249faces. Sourcegeometrynotcertifiedfacades. ExistingbaseoverlapRMS<=1.275/255perchannel. New OSMapi reads archived with source URLs.


## Second left strip

Atlasbounds[-.5,-.5,1.5,1.5],4096x4096pixels. Add512x4096atworld(-.5,-.5). Capture4096x4096,scale472,focus(-174.96861205,-137.64044059),sameangle-154/tilt.60. Source14303records/14287renderedparts,5020OSMelements/4944roadways/418189faces. Sourcegeometrynotcertifiedfacades. ExistingbaseoverlapRMS<=2.920/255perchannel. New OSMapi reads archived with source URLs.


## bottom5

4096x4608px, bounds[-0.5, -0.5, 1.5, 1.75]. Source records15547, renderedparts15531, roadways5451, faces451721, OSMelements5529. Capture4096x4608,scale531,focus(-268.88441051,-183.44623608),angle-154,tilt.60. ExistingbaseoverlapRMS<=1.766/255. Fourgeometry-guidedpanels.


## right4

4608x4608px, bounds[-0.5, -0.5, 1.75, 1.75]. Source records16917, renderedparts16901, roadways6649, faces500052, OSMelements7166. Capture4608x4608,scale531,focus(-243.02051285,-236.47508481),angle-154,tilt.60. ExistingbaseoverlapRMS<=2.326/255. Fourgeometry-guidedpanels.
