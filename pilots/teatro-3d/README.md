# Teatro Circo: modern front and estimated auditorium roof
16 November 2026. Original geometry CC BY-SA 4.0, no pasted images.
Primary photo: DnTrotaMundos ☮, Teatro Circo de Albacete,22September2010,CC BY3.0:
https://commons.wikimedia.org/wiki/File:Teatro_Circo_de_Albacete_-_panoramio.jpg
License https://creativecommons.org/licenses/by/3.0/ fetched and verified. Pixels inspected: concrete pylons, curved mesh curtain, glazed ground floor, large sloping canopy, line lettering. Model changes: approximate3Dgeometry, own materials, simplified lettering, no posters. Grid simplified to broad panel surfaces to avoid false tiny detail.

Architecture factual sources, NO photos/plans copied:
- https://lacasadelaarquitectura.es/recurso/rehabilitacion-del-teatro-circo-de-albacete/7df6431f-24b5-481f-be38-13fc71b7aa6b : modern curtain and portal in2002rehabilitation.
- https://www.coacm.es/es/1-Noticias/2-COACM-en-los-medios/480--El-Teatro-Circo-de-Albacete-premio-a-la-Permanencia-del-COACM-busca-ser-declarado-Patrimonio-Mundial.htm : conical copper auditorium roof. Cone follows curved Catastro parts6/12; apex(163.5,51.5),rim11m,top18m are estimates,not measured.
- https://www.latribunadealbacete.es/noticia/z84fe0fb2-87a4-4839-950e21917bc58a68/202506/el-teatro-circo-recupera-su-fachada : four historic facade banners removedJune2025. They are omitted, not mistaken for real old facades.

Parcel9472601WJ9197A matched with OSM TeatroCircoQ11951071 and architecturerecord coordinates. Frontedge(130.7,31.7)->(161.1,13.8),width35.28m. Parts8/9genericfrontmasses replaced; remainingcontextparts kept, heights storeyestimates. No reconstructed rear/interior. Camera preserves real occlusion from opposite street buildings. Depth/curve/canopy dimensions estimated. Some entrance/lettering occluded at ordinary angles.

Other inspected photos (santiagolopezpastor2020page / EXIFuncertain and Siempremolinicos2007) were NOT used for geometry, only triage. Only licensed2010photo supplies facadeform. No sourcephotos included in repo or deployment.
Run python pilots/teatro-3d/build.py then python src/build_zone.py.

## Roof correction, 16 November 2026
The previous viewer incorrectly fanned annular part 12 to the same apex as part 6. It now has a separate 12 m flat reference roof. The inner part 6 uses a robust cone fitted to 266 class-6 returns from PNOA 2017 tile 598-4318.

Normalized height uses the median of the eight nearest class-2 ground points. Selection: current Catastro part 6 inset 1 m, local northing 40-60 m, normalized height 12-24 m. These filters exclude backstage and ground outliers. Fitted local east/north centre: (164.0969, 50.1663) m; apex height 21.1963 m; slope 0.49989 m/m. Rounded for rendering to 21.2 m and 0.50. Median absolute residual 0.25 m is sample-fit quality only, not global accuracy or a current cornice measurement. Boundary heights and registration remain interpolation estimates. No blanket percentile-to-height replacement was made.

Source: https://open-lidar-data.s3.eu-central-1.amazonaws.com/data/ES/CNIG/Lidar_2015-2021_epsg25830/copc/PNOA_2017_CLM-SE_598-4318_ORT-CLA-RGB.copc.laz . Data: LiDAR PNOA 2017, IGN/SCNE, CC BY 4.0 compatible licence; COPC copy: https://github.com/flai-ai/open-lidar-data . Policy: https://centrodedescargas.cnig.es/CentroDescargas/politica-datos .

Transformed selected roof returns are shared in `roof-samples-2017.json` as [local east m, local north m, normalized height m]. Reproduce with `python fit_roof.py` using numpy and scipy. Samples are historical and may not match today. Backstage building masses remain estimated; no interiors are modelled.
