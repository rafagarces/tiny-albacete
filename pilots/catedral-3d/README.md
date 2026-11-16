# Catedral de Albacete, partial estimated 3D pilot
16 November 2026. A model to evaluate before extending the city. Not an exact replica.

## Reproduce / reuse
Run python build.py (Python,numpy,Pillow) offline. Generates coloured polygon model.json, Wavefront catedral.obj+catedral.mtl, and two orthographic renders. No external resources or billable services. This is a true polygonal3D model, not a photograph filter. The full viewing page uses a local WebGL renderer and no remote mapping API.

## Sources
- Source2013, JnCrlsMG, CC-BY-SA4.0: https://commons.wikimedia.org/wiki/File:Catedral_de_San_Juan_de_Albacete_(Albacete)_-_Fachada_Principal.jpg . Main portal, rose, tower, projecting lateral masses observed. Relief sizes estimated.
- Fernando,6Aug2021,CC-BY-SA4.0: https://commons.wikimedia.org/wiki/File:Albacete_Cathedral_2021_-_west_fa%C3%A7ade.jpg . Reference view, not measured elevation.
- Nakuir,27Sep2026,CC-BY-SA4.0: https://commons.wikimedia.org/wiki/File:Catedral_Albacete_Lateral_2026.jpg . Three large upper south windows, buttresses and side portal observed; coordinates and depth estimated. Licence verified from source-page link.
- CatastroINSPIRE Albacete building ES.SDGC.BU.9271101WJ9197A. https://www.catastro.hacienda.gob.es/INSPIRE/Buildings/02/02900-ALBACETE/A.ES.SDGC.BU.02900.zip . Matched actual cathedral point. Reference footprint area2022.71m², envelope65.02x50.26m. The rectangular nave deliberately SIMPLIFIES this footprint; it is not an exact extrusion. Licence https://www.catastro.hacienda.gob.es/webinspire/documentos/Licencia.pdf permits transformed works.
- PNOA2017,CC-BY4.0 compatible SCNE.1943class6points within footprint: median height24.065m,max39.555m. Nave24m,eaves/ridge32m,tower38.5m are rounded MODEL ESTIMATES informed by these heights, not separately verified feature measurements. Source tile https://open-lidar-data.s3.eu-central-1.amazonaws.com/data/ES/CNIG/Lidar_2015-2021_epsg25830/copc/PNOA_2017_CLM-SE_598-4318_ORT-CLA-RGB.copc.laz . Policy https://centrodedescargas.cnig.es/CentroDescargas/politica-datos . Derived from LiDAR-PNOA-cob2,SCNE/IGN. Normalisation via local groundpoints, not survey-grade.

## Estimated vs documented
Every vertex is an estimated placement. The model's kind fields distinguish photo-inspired features, artistic material and unknown simplified faces; no mesh vertex is falsely labelled surveyed.
Documented feature existence is distinct from estimated geometry. Roof continuity, front-mass symmetry, portal depths, rose tracery interpretation, exact heights and window locations remain estimated. North/east faces deliberately have no facade details. Roof tile rows and stone courses are artistic material patterns, NOT actual counts or measured joint positions.
Ground platform is a presentation base, not a plaza survey. Sources span2013/2017/2021/2026, not a verified current state. Not architectural or engineering documentation.

## Licence
Original model and rendered adaptations:CC BY-SA4.0. Attribute JnCrlsMG,Fernando,Nakuir for photo references and IGN/SCNE for LiDAR as above. Changes: original approximate3Dmodelling, materials, lighting and orthographic rendering. No image texture is pasted onto the mesh. This pilot does not use Google meshes, textures or imagery.

## Production
The first pilot was reviewed before publication. The model is now part of the bounded Cathedral zone on Tiny Albacete, not a claim that the city is reconstructed or that the Isometric NYC visual target has been reached. No billable service or third-party contact is used.

## South lower aisle refinement, 16 November 2026
The Nakuir south-side photograph above clearly shows a low aisle projecting beyond the upper window wall, its tile shed roof, and a slightly raised roof over the side portal. The first pilot flattened the low doorway and upper wall into one plane. Added that documented stepped mass and moved the existing side doorway and lower windows onto its outer face. No extra facade was invented on the unknown north/east sides.

Width 47 m follows the existing simplified nave; projection about 4.3 m, low wall height 11.8 m, roof heights 11.9-13.2 m and portal roof 12.9-14.2 m are **model estimates**, not measured dimensions. The low roof is not a separate gabled pediment. Opening counts and positions remain interpreted. Main roof continuity and registration are still simplified. A trial fit to 2017 main-roof returns showed multiple height clusters and registration sensitivity, so no main-roof height change was made from that trial. Historical returns alone do not identify every architectural surface.
