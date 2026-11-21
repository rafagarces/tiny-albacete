# Tiny Albacete - decisiones y limites

Sitio: https://tiny-albacete.pages.dev (Cloudflare Pages, proyecto `tiny-albacete`, plan gratuito, sin tarjeta).

## Origen y derechos
- Inspirado en la experiencia de Tiny Valencia (mapa isometrico pixel-art con zoom, lugares, idioma, monstruos). No se copia codigo, arte ni teselas. Implementacion propia: OpenSeadragon (BSD), fuente Pixelify Sans (OFL), sprites de monstruos propios.
- Datos: huellas y plantas de edificios del Catastro (INSPIRE, CC BY 4.0); calles, parques, agua y arboles de OpenStreetMap (ODbL). Atribucion visible en el pie.
- Sin datos personales de nadie en la web.

## Como se genera
- `src/render2.py` pinta cada tesela desde las huellas con camara isometrica fija; `src/pyramid.py` crea los niveles de zoom; `src/chk.py` borra teselas corruptas. Los datos de entrada (`bu_parts.json`, `bu_blds.json` del Catastro; `roads.json`, `green.json` de OSM) no se versionan por tamano; `src/parse_bu.py` y `src/catparse.py` los reconstruyen.
- Determinista: semillas por coordenadas, nunca `id()`.
- Despliegue: `npx wrangler pages deploy . --project-name tiny-albacete --branch main` con un token de Cloudflare restringido (guardado en la boveda, no en el repo).
- Mirror de respaldo: este repositorio (incluye `painted/`).

## Decisiones
- Alturas = plantas oficiales x 3 m + 2 m; no son mediciones. Edificios sin plantas: altura estimada.
- Cubiertas a dos aguas para edificios no industriales < 4000 m2 y <= 40 vertices; planas el resto.
- Texto: no se afirma "pintado a mano" ni nada sobre ausencia general de IA. Solo: la imagen del mapa se genera a partir de datos abiertos, sin fotos, satelite ni generacion de imagen. Subtitulo "Albacete en miniatura" / "Albacete in miniature". Sin cifra de area.
- Agua clasificada por tags OSM. Borde de piedra y pilon solo para `amenity=fountain` / `water=fountain`; `basin`, `well` y `canal` llevan borde neutro. Acequias/drenajes (`ditch`, `drain`, `stream`) como linea fina apagada, no como canal.
- Hitos: campanario de la catedral conservado, con proporcion tomada de foto verificada (estimada, no medida); Teatro Circo con contorno exterior cerrado y color de piel (sin cupula exterior); Pasaje de Lodares con cubierta acristalada sobre el eje OSM (altura aproximada). No se inventan fuentes, fachadas ni elementos historicos.
- Peatones por longitud de camino con adelgazado espacial (evita agrupaciones); arboles de calle con 7 verdes y rango de tamano deterministas.
- UI: busqueda visible, botones Compartir/Monstruos/Al azar con texto, idioma ES/EN (el boton muestra el idioma destino; el inicial sale de localStorage o navigator.language), panel de lugares (38).
- Vercel descartado (limite de uso). Sin gasto, sin facturacion automatica.

## Limites conocidos
- Camara fija: no hay rotacion ni varios rumbos. Girar exigiria renderizar y alojar 4 rumbos (4x teselas) con reordenado de edificios; un giro plano deformaria la perspectiva.
- Nivel de detalle y variedad de fachadas por debajo de la referencia; es un renderizador procedural, no obra ilustrada a mano.
- Teatro Circo: sin piel curva ni cubierta inclinada, solo cierre del volumen y color. Lodares: parcialmente tapado por vecinos segun el angulo.
- Pruebas moviles con viewport emulado (iframe 390 px) y capturas de escritorio 1280x720; no se probo en dispositivo fisico.

## 16 noviembre 2026: dirección Catedral validada
- Rafa aprobó el piloto3D propio de Catedral, con estimaciones señaladas, y pidió continuar en esa dirección. El gusto validado es el del piloto, no una promesa de igualar otra referencia.
- Nueva ruta `/zona-catedral/`: unas500m de contexto,1.240partes de edificios Catastro, calles OSM y modelo propio parcial Catedral. El mapa general y sus teselas se preservan. Enlaces de ida/vuelta, no sustitución silenciosa de cobertura.
- Catedral: se eliminan del contexto todas las partes9271101WJ9197A. Maqueta posicionada con giro aproximado-24° y desplazamiento(-13.1,6.7)m en el sistema local del mapa. No es un registro topográfico. Mesh original754caras.
- Vecinos: huellas Catastro, alturas plantas×3+2m (máx50m),9m si faltan plantas. Sin ventanas, balcones o tejados históricos inventados. Son contexto simplificado, no un cumplimiento de réplica edificio por edificio. Materiales artísticos suaves.
- WebGL local sin motor remoto ni API facturable. Controles de giro/inclinación,zoom y desplazamiento(Shift+arrastrar o botón derecho), teclado flechas/+/-; fallback explícito al mapa general si no hayWebGL. No se instalan recursos de pago.
- Calles consultadas16/11/2026, extracto API OSM bbox-1.8600,38.9925,-1.8515,38.9990. Trazado real; anchos estimados. Fuente exacta: https://www.openstreetmap.org/api/0.6/map?bbox=-1.8600,38.9925,-1.8515,38.9990 . DerivadoOSM en zona-catedral/osm-source.json,ODbL.
- Créditos/licencias de fuentes fotográficas y limitaciones en zona-catedral/sources.html y pilots/catedral-3d/README.md. Modelo Catedral y renders:CC BY-SA4.0. NoGoogle. No datos personales ni secretos en el repositorio o deploy.
- Reproducibilidad: modelo publicado, generadores src/build_zone.py y pilots/catedral-3d/build.py. El primero requiere Catastro bu_parts.json reconstruible con src/parse_bu.py y el extractoOSM incluido. Datos originales Catastro no se redistribuyen en bruto. Respaldo del mapa previo:git9ef5c64.

## 16 noviembre 2026: Casa de Hortelano
- Segunda ampliación dentro de la dirección aprobada. Modelo propio parcial de 1033 caras, no una fachada genérica. Referencias libres Rodelar (27 abril 2024) y User041 (17 abril 2026), CC BY-SA 4.0. Créditos, enlaces y límites en sources.html.
- Huella Catastro 9272019WJ9197S, frente de 15.93 m. Se sustituyen sus partes catastrales por el modelo. Contexto ahora: 1238 partes, no 1238 fachadas reconstruidas. El resto del museo anexo conserva volúmenes de contexto.
- Galería superior de cinco ventanas, tres huecos bajos, entrada/mirador derechos, azulejo verde, torres asimétricas y pináculos según fotos inspeccionadas. Talla floral simplificada. Profundidades, alturas, cubierta y geometría ornamental estimadas; caras ocultas sin detalle.
- Selector Catedral / Cuchillería / Vista general, con encuadres propios. Se preservan oclusión y geometría, sin retirar vecinos para forzar la vista. Ruta directa ?l=museo. Mapa general intacto.
- Generador reproducible pilots/hortelano-3d/build.py. Sin fotos originales dentro del deploy, sin servicios remotos, facturación ni contacto con terceros. Primera zona respaldada en da9fd6d.

## 16 noviembre 2026: Ayuntamiento antiguo / Casa Cortés
- Fachada parcial original basada solo en JPOK, 10 noviembre 2016, CC0, foto inspeccionada; fecha histórica visible. Identidad contrastada con Turismo de Albacete, OSM y Catastro 9371110WJ9197A. No se presenta como registro actual.
- Frente Catastro20.14m, registro sobre arista(161.2,-60.6)->(178.8,-70.4). Se mantienen masas catastrales traseras; ajuste frontal11.2m según proporción fotográfica, alturas/profundidades estimadas. Sin fachada lateral genérica.
- Dos ventanas superiores y dos rejas bajas por lado, acceso/balcón centrales, torre con dos esferas visibles, escudo esquemático y coronación. Sin copiar carteles, banderas o tráfico; sin heráldica, texto ni talla ornamental inventados. Agujas estáticas artísticas, no hora real.
- Generador y modelo propios CC BY-SA4.0, fuenteCC0 acreditada. Navegación Ayto. antiguo y ?l=ayuntamiento. Zoom mínimo corregido de30a12m para evitar salto hacia atrás al pulsar+desde encuadreHortelano24m.

## 16 noviembre 2026: Teatro Circo moderno
- Foto DnTrotaMundos ☮,22septiembre2010,CC BY3.0 inspeccionada; créditos/licencia/cambios publicados. No se confunden lonas con fachadas históricas reales. Retirada de lonas junio2025 contrastada enLaTribuna, por eso se omiten.
- Pórticos, telón curvo, marquesina y rótulo simplificados; no carteles. Catastro9472601WJ9197A,frente35.28m,partes8/9sustituidas,1236partescontexto restantes. No interior ni trasera reconstruidos.
- COACM2024 documenta cubierta cónica decobre; se aproxima sobre partescurvas6/12 con altura11-18m y vértice estimados, no cúpula arbitraria. Fotografías/planos de COACM y CasaArquitectura no copiados.
- Encaje/curvatura/cubierta/altura y letras estimados. Vecinos no se eliminan para ocultaroclusiones. SelectorTeatroCirco y ?l=teatro, mapa completo intacto. 0€sinserviciosnuevos.

## 2026-11-16 · Landmark orientation
The header and page title now name the selected landmark rather than always saying Cathedral. Overview uses a deterministic camera independent of the last inspected building. No geometry or map coverage changes.

## 2026-11-16 · Palacio Provincial partial front
Photo-led frontage registered to Catastro9472604WJ9197S. Two2017 free photos, elevations estimated. Lower floor/attic/hidden facades simplified rather than invented inventories. Rear/courtyard/context masses retained, including occlusions. No image textures, heraldry or interior reconstruction.

## 2026-11-16 · Casa Perona, western edge
Two documented facades and blue/white dome interpreted from free photos; no claimed exact carving, ironwork or dimensions. Capture dates unknown despite Commons publication dates. Catastro8971009WJ9187B and OSM street corner registration. Extend context50m west to avoid clipping the parcel, retaining previous coverage. All new neighbor parts remain estimated masses without invented facade details.

## 2026-11-16 · Navigation consistency
Landmark selection updates the shareable URL and accessible canvas label as well as visible title. Explicit Cathedral links enter the close view. Escape closes information; desktop helper explains Shift-drag panning rather than touch gestures. A ground-shadow experiment was kept out of production pending physical-device performance evidence.

## 2026-11-16 Gran Hotel parcial
El Gran Hotel incorpora dos frentes parciales y su chaflán: tres cupulillas azules con linternas, ático con parejas de ventanas y jerarquía de balcones documentados. Geometría, alturas, chaflán y ubicación de cúpulas estimados. Planta baja simplificada, sin comercios ni detalle de talla. No se reconstruyen el tercer lienzo de Marqués de Molins, patio, interior ni fachadas ocultas.
Catastro9470007WJ9197A y DOCM2019. Dos frentes registrados, pequeño chaflán estimado sustituye esquina generalizada; tercer lienzo no añadido sin registro suficiente. Fotos libres2008/2009/2017/publicación2020 con licencias atribuidas.3007caras originales, no texturas. Contexto general y mapa anterior conservados.

## 2026-11-16 Lectura conjunta de siete hitos
Comparadas cámaras móviles de Teatro, Perona y Gran Hotel. Nuevos ángulos permiten leer mejor acceso del Teatro y retorno de Perona, y las tres cupulillas del Gran Hotel, sin quitar o transparentar vecinos ni editar geometría. La información inicial se centra en el hito elegido y enlaza su apartado de fuentes; Vista general permite leer las siete descripciones. Se mantienen explícitos límites y estimaciones.

## 2026-11-16 Teatro: corregir cubierta con evidencia2017
Cono interior ajustado robustamente a266retornos PNOA2017, vértice21.2m y pendiente0.50; anillo exterior separado como cubierta12m. Se corrige abanico erróneo anterior sobre partecatastral12noestrellada. Error mediano absoluto0.25m del ajuste no equivale a precisión actualglobal. Datos/filtro/script y atribución guardados. No cambio automático masivo de alturas por percentiles. Cámara recentrada para incluir sala y fachada sin recorte.

## 2026-11-16 Roof footprints: constrained triangulation
The previous Delaunay mesh filtered triangles by a representative point. A triangle could pass that test yet cross a courtyard or a concave boundary. Replaced it with constrained Delaunay triangulation (Shapely >=2.1, GEOS >=3.10). Repaired MultiPolygon surfaces are retained rather than silently omitted.

Offline regression checks 1,345 context roof footprints against the same source rings and chamfer adjustment. Previous method differed on 94, including one omitted MultiPolygon, with about731m² outside and1,143m² missing when summed per roof part. These are algorithmic differences against input footprints, not newly surveyed real-world area. New union-to-input difference below1e-6m² per footprint. Building count, floor heights and coverage unchanged. See tests/check_roof_triangulation.py. The inner Teatro cone fan was separately checked to stay inside its footprint.

## 2026-11-16 Cathedral: separate the documented south low aisle
The inspected Nakuir 2026 source photograph shows the low aisle projecting in front of the upper window wall, a tile shed roof and a slightly raised roof over the portal. Previously the low doorway and upper windows occupied one flat wall. Added only the observed south stepped mass, with explicitly estimated 4.3 m projection and 11.8-14.2 m wall/roof heights. Moved existing lower openings onto that outer face. No extra gabled pediment, hidden north/east facade or exact dimensions claimed.

An exploratory fit of the historical main roof showed multiple clusters and registration sensitivity, not a clean single-roof measurement. Left the main nave/ridge estimates unchanged rather than applying that fit. Reproducible audit remains a research artifact, not model geometry.

## 2026-11-16 Artistic ground shadows
Added restrained fixed-sun ground-only shadows projected from the same meshes, stencil union prevents overlap darkening; depth test preserves opaque buildings. It is illustrative lighting, not a solar study or current-time simulation. No mesh geometry, facade claim or height changed. No shadow depth-texture dependency; missing stencil safely omits shadows. An experimental full shadow-map path showed surface artifacts under QA and was rejected before publication. Kept simple projected shadows after actual pixel checks. Existing lower-resolution pixel-art canvas and event-driven render remain.

## 2026-11-16 Shared spatial frame, and reproducible zone inputs
Audit found an inconsistency: cadastral meshes use EPSG:25830 offsets while OSM and first LiDAR audit used an approximate latitude/longitude tangent plane. Difference at Theatre about2m, at Perona3m. All zone OSM input is now transformed through EPSG:25830 to the same local origin. Landmark registration is unchanged because it was already based on cadastral edges. Theatre historic fit repeated in that frame:274samples, apex(163.4508,52.2973,21.1897),slope0.50465,median absolute residual0.2675m; renderer rounds to(163.45,52.30,21.2),slope0.505. Supersedes earlier266sample fit, not a new survey. Annular12m reference retained after corrected inset sample median11.845m. No other historic-height estimates promoted to geometry.
A1362-record transformed/bounded Catastro input and dependency/runner files now allow rebuilding the zone without transient files. Seven landmark builders reproduce identical mesh JSON; legacy full-map renderers remain archived and are not claimed reproducible by this zone build.

## 2026-11-16 Preserve cadastral interior rings
A direct original-GML audit found the legacy parser had kept only the first posList and discarded119interior rings in85of1362bounded input parts. Updated parser and normalized source to preserve those rings, with source GML/input SHA256manifest. No source feature in this bounded snapshot has multiple exteriors. Context roofs now use118interior rings in84parts (one extra belongs to a replaced/excluded landmark mass), and their inner vertical boundaries are modelled with the same estimated heights. This removes3409.28m²of incorrectly capped upper roof area summed per part, not newly surveyed open-air courtyard area: lower building parts may remain underneath. Gran Hotel and Perona cadastral context also benefit, without new facade reconstruction. Test1345input roof polygons has zero triangulation difference within1e-6m²perpart. Earlier94affected triangulation comparison refers to the prior outer-only input; this change fixes parsing, a separate earlier stage. Face count49683, footprints/storey heights/landmark meshes otherwise unchanged.

## 2026-11-16 · approved artistic direction, separate illustrated pilot

The owner approved the detailed Cathedral illustration and asked for this finish throughout. Add an isolated `ilustrado/` route, linked from the general map, rather than replacing the existing complete-map tiles or claiming to have textured the rotating 3D model. The first bounded scene uses the existing f77a36c Catastro/OSM model's fixed-camera composition, finished as an interpreted illustrated neighborhood. The separate Cathedral close-up is the owner-approved artwork. Both are image-backed scenes with a fixed camera, zoom and pan, not interchangeable views of a coherent multi-angle model. Unobserved neighbor facades use local Albacete visual conventions; exact per-parcel correspondence is not claimed. Sources and limits are visible in the page, including assisted image generation and the distinction from the older procedural map.

Preserve all 49683 faces and source geometry of f77a36c. Unpublished procedural-block and Gran Hotel axis experiments are excluded from this branch. No billing setup, paid product or external communication required. The page loads only static files already hosted in the project's existing deployment. Rendering context scene: fixed camera -154deg, elevation .60rad, scale118, focus -13/7, 1536x1024. Artistic output can shift small boundaries and must not serve as a cadastral viewer. Each expansion needs overlap/continuity QA, not automatic city-wide propagation from a single generated image.


## 2026-11-16 · contiguous illustrated expansion to Gran Hotel

Extend the approved fixed-camera environment from1536x1024 to2048x1024 with a512px right strip. Keep entorno.webp byte-identical and display it at world x0,width.75, with east.webp at x.75,width.25. The two tiles form one continuous environment, not a scene switch. The separate Cathedral close-up remains separate. Migration of old environment URLs multiplies x/y by.75 and zoom by4/3; revision2 URLs use the expanded normalized frame. Base comparison uses the expanded same-camera raster.

Expanded geometric input retains1362 bounded municipal records and adds1819 parts from the same downloaded municipal GML, with actual projected footprints rather than extending blank or invented block geometry. Context heights remain storey estimates. Expanded base uses the pending Gran Hotel axis correction as a drawing guide only; production3D model unchanged. Generated strip required localized review and correction from five to three cupolas, following the regional heritage catalogue and DnTrotaMundos2011 Commons photograph. Art remains interpreted and must not be described as exact parcel correspondence. Original approved finished pixels are retained.

QA: desktop1280 and mobile390/320, no overflow/errors/failed assets; three cupolas and tile seam visually checked; legacy URL migration, comparison registration and restored view tested. Existing rotating3D and whole-map assets preserved. No billing, new paid resource, contact or obligation.


## 2026-11-16 · lower contiguous illustrated strip

Add a2048x512 lower strip at world x0,y.5,width1, for total2048x1536 coverage. Original entorno/east/detail assets and previous URL coordinate revision remain unchanged, with same original screen positions. Extend local geometry bounds westward using1022additional municipal GML records,4203source parts total,4187context parts rendered. Storey heights remain estimates and artistic output can shift boundaries. The expanded base is a separate comparison image, not changes to the live3D mesh.

QA rejected an enlarged gold/blue invented dome near the largely occluded Perona location and replaced it with ordinary low roof/courtyard context. No claim to reconstruct Perona in this camera. A visible horizontal rectangle on a beige party wall at the old/new boundary was locally repaired only in new pixels. Inspect final seam, roof/street joins and entire map at desktop/mobile before publication. Scene is still a bounded fixed-camera illustration, not the whole city or parcel-accurate architecture.


## 2026-11-16 · second right-side contiguous illustrated strip

Add512x1536right-hand strip, total2560x1536, placed at world x1,y0,width.25. Keep world units anchored to2048pixels rather than re-normalizing old coordinates on every expansion. Expanded comparison is width1.25 in the same world frame; URL restoration now accepts x through1.25. All previous illustration files and production3D remain byte-identical.

Local geometry base expands southward with843additional source records from municipal GML,5046records total/5030rendered context parts. Reprojected expanded crop matches previous base RMS0.59/255before extension; this verifies camera registration, not artistic parcel fidelity. Existing bounded OSM street source covers the added strip; road widths remain estimated. Generated ordinary building facades use already-documented local conventions, no new monument identification. New strip is interpreted, not new measured architecture. Reviewed full scene and vertical join for roof, wall and street continuity. No billing or paid resources enabled.


## 2026-11-16 · second lower contiguous illustrated strip

Add2560x512at world(0,.75),width1.25. Total atlas2560x2048. Source base extended with1433additional municipal building-part records,6479total,6463rendered context parts. Same local UTM frame and existing OSM street extract. Camera overlap RMS<=.53/255per channel against prior base, no map-wide accuracy claim. Ordinary facades remain interpreted, not an inventory. Existing five illustration assets and rotating3D preserved unchanged. Fine-detail pass is applied only within the added region. Archive updated with source snapshot and repeatable camera/base instructions. No billing or paid resources enabled.


## Requested next phase,16November2026,12:25Europe/Madrid

After this illustrated quality is extended across the city, Rafa requests a whole-city reference pass to bring it close to the current real appearance. His approved routes include photographs, Google Maps and other suitable visual references. Preserve the explicit order: artistic extension first, current-reality fidelity pass second. Reference dates, observed features and inferred details must stay distinct; an old photograph is not evidence of current appearance. This does not replace the approved artistic direction or promise an exact replica. Keep0EUR/no billing/no third-party contact constraints. A visual reference can inform interpretation; do not copy third-party imagery,3D or textures into the delivered map without compatible rights.


## 2026-11-16 · third right contiguous illustrated strip

Add512x2048at world(1.25,0),width.25. Total3072x2048. This strip is inside the previously archived6479-part municipal source coverage and existing OSM street extract, so no new source inventory is claimed. Same camera projection, overlap RMS<=.60/255per channel. Only new strip pixels changed; previous six art assets and rotating3D unchanged. Interpreted ordinary architecture without new monument claims. No billing or paid resources.

## 2026-11-16 · explicit spatial catalog, coverage and scaling

Replace hard-coded image positions with a local JSON tile catalog, keeping the same six surroundings tiles and all image bytes. Dynamic bounds admit future growth to negative coordinates without moving existing world coordinates or URL revision2. Local tests cover normal catalog, temporary catalog failure with bundled fallback, and test-only negative coordinates. No test-only tile is published. Add an independent overlap/gap/dimension/hash validator.

Current fixed-camera ground-plane envelope is approximately0.592km2, recorded as GeoJSON with explicit projection/height/artistic-drift limits. This is a small central area, not citywide coverage. No completion percentage is claimed. A whole-city operational mask remains under contrast: municipal neighborhood maps, actual built form, parks, industrial areas and fringes must not be silently replaced by one SIU planning-class component. The later citywide current-facade reference pass remains after artistic extension. Spatial/orthophoto work here defines territorial scope, not facade-currentness.


## 2026-11-16 · third bottom strip

Add3072x512atworld(0,1),total3072x2560,approximately0.740km2ground-plane envelope. Citywide coverage is still incomplete and no percentage is claimed. Art extends the main urban area using three overlapping geometry-guided panels with edge matching confined to new pixels. Prior seven art files and rotating3D unchanged. Expanded municipal base and OSM streets archived for reproduction. Additional source records do not certify a count of faithfully illustrated buildings. No new monument identification or current-facade claims.0EUR,no billing, no external contact.


## 2026-11-16 · first left strip

Extend512x2560to negative worldx[-.25,0], total3584x2560,approximately0.863km2 ground envelope. Existing art and coordinate links unchanged. Negative coordinates tested in real content, no renormalization. Same interpreted-art limits and0EUR/no billing/no external contact. Remaining city target provisional, no completion percentage.


## 2026-11-16 · on-demand illustrated display and territorial ledger

Replace eager loading of all full illustrations with an explicitly registered WebPDeepZoompyramid. Source spatial coordinates, fixed framing, previous URLs and original art files remain unchanged. Top level is lossless relative to decoded originals. Tested local image-transfer bytes: mobile-left1.69MBinstead of4.64MB, desktop-home1.55MBinstead of4.64MB; default mobile4.44MBso no universal speedup claim. Work ledger inventories25official2016neighborhoods,30SIUcomponents and exterior sectors. No city completion percentage until a contrasted current operational target exists.0EUR,no billing,no contact.


## 2026-11-16 · first top strip

Add3584x512atworld(-.25,-.25),total3584x3072,approx1.036km2groundenvelope. All previous sourceart and URLs remain unchanged. Geometry-guided interpretation, open spaces retained, four overlapping panels. Current-facade reference pass remains later, not claimed now. Main user asked no intermediate updates; internal progress only until city complete. No completionpercentage, no new monument certification.0EUR,no billing,no contact.


##2026-11-16 fourth bottom strip

Add3584x512atworld(-.25,1.25),total3584x3584,approx1.208km2groundenvelope. Originalartandcoordinatesunchanged. Fourgeometry-guidedpanels, no current-facadeclaim.0EUR,no billing,no contact. Internalprogressonlyuntilcitycomplete.


##2026-11-16 second top strip

Add3584x512atworld(-.25,-.5),total3584x4096,approx1.381km2groundenvelope. Originalartandcoordinatesunchanged. Fourgeometry-guidedpanels, no current-facadeclaim.0EUR,no billing,no contact. Internalprogressonlyuntilcitycomplete.


##2026-11-16 second left strip

Add512x4096atworld(-.5,-.5),total4096x4096,approx1.578km2groundenvelope. Originalartandcoordinatesunchanged. Fourgeometry-guidedpanels, no current-facadeclaim.0EUR,no billing,no contact. Internalprogressonlyuntilcitycomplete.


## 2026-11-16 bottom5

Append tile at(-0.5,1.5),size(2.0,0.25),total4096x4608,approx1.776km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Capture4096x4608,scale531,focus(-268.88441051,-183.44623608),angle-154,tilt.60. ExistingbaseoverlapRMS<=1.766/255. Fourgeometry-guidedpanels.


## 2026-11-16 right4

Append tile at(1.5,-0.5),size(0.25,2.25),total4608x4608,approx1.997km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Capture4608x4608,scale531,focus(-243.02051285,-236.47508481),angle-154,tilt.60. ExistingbaseoverlapRMS<=2.326/255. Fourgeometry-guidedpanels.


## 2026-11-16 Atlas cache consistency

Two immediate post-deploy comparison checks briefly changed the viewport, then passed on repeat. Independent stale metadata is a suspected cause, not proven. Construct DZI sources from the current catalog instead of independently cached DZI metadata. Version raster tile requests by source-content digest, fetch catalog without storage, and revalidate viewer entry points. This removes a cross-revision metadata dependency; physical device cache behavior remains untested.


## 2026-11-16 Municipal neighborhood vectors

Retrieve all25public municipal neighborhood features and18singular entities. Use official neighborhood geometry rather than manual outer tracing for the expanded principal candidate. Retain prior raster approximation as an audit artifact. Keep historical approval, database timestamp and current reality distinct. No completion percentage or silent exclusion of external sectors.


## 2026-11-16 top3

Append tile at(-0.5,-0.75),size(2.25,0.25),total4608x5120,approx2.219km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. No new OSM fetch for this band: reuses archived right4 source URLs and geometry. Capture4608x5120,scale590,focus(-149.10471439,-190.66928932),angle-154,tilt.60; priorbaseoverlapRMS<=.624/255. Originalart pixels preserved.


## 2026-11-16 left3

Append tile at(-0.75,-0.75),size(0.25,2.5),total5120x5120,approx2.466km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Reuses right4 geometry and source URLs without additional OSM requests. Camera square5120,focus(-174.96861205,-137.64044059),scale590; shared reference overlap RMS <=0.568/255. Five reference-led panels, existing pixels preserved exactly. Geometry is cadastral/OSM, facade details interpreted, not current-photo evidence.


## 2026-11-16 bottom6

Append tile at(-0.75,1.75),size(2.5,0.25),total5120x5632,approx2.713km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Camera5120x5632,focus(-268.88441051,-183.44623607),scale649. Additional cadastral parts and1061OSMways extend western base edge. Shared-reference RMS<=1.276/255 includes additional roads; artistic previous pixels unchanged. Five panels with interpreted facades, no claim of current facade verification.


## 2026-11-16 right5

Append tile at(1.75,-0.75),size(0.25,2.75),total5632x5632,approx2.984km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Five overlap-aligned right panels. Existing source pixels unchanged. Same municipal/OSM geometry extent adequate for strip; capture uses narrow viewport to avoid WebGLcontextloss above31millionpixels. Rounded central Romica PNOAsample confirmsJuly2024/25cm, no2026currentnessclaim.


## 2026-11-16 top4

Append tile at(-0.75,-1.0),size(2.75,0.25),total5632x6144,approx3.255km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Five top panels. Empty outer land preserved. Fixed projection narrow5632x1024capture,overlapRMS<=3.04includingnewgeometry. Previous artwork pixels untouched. Bpaneltimeoutrecoveredaftertwomissingfilechecks. No2026currentfacadeclaim.


## 2026-11-16 left4

Append tile at(-1.0,-1.0),size(0.25,3.0),total6144x6144,approx3.551km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Real cadastral geometry with distinctive curved and elongated complexes preserved. Five overlapping art panels; former pixels unchanged. Southern SciencePark/Botanic explicitly inventoried as points and imagery, not certified boundaries.


## 2026-11-16 top5

Append tile at(-1.0,-1.25),size(3.0,0.25),total6144x6656,approx3.847km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Cached OSM data only, no requests after throttle. Downloaded successful bboxes cover99.9733percent of new band;79m2tip visually checked against PNOA and existing full-way centerlines. Open arterial roadside land preserved. Previous art unchanged.


## 2026-11-16 right6

Append tile at(2.0,-1.25),size(0.25,3.25),total6656x6656,approx4.168km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Six reference-ledpanels, all priorpixelsunchanged. OSM429paused;97.995percentcachequerycoverage,newgapthreepolygons6420m2checkedPNOAandcachedfullwaycenterlines. Catastro707additionalrecords. LaPulgosaexplicitpointinventory,noexclusionbyprincipalborder.


## 2026-11-16 bottom7

Append tile at(-1.0,2.0),size(3.25,0.25),total6656x7168,approx4.488km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Six aligned illustration panels, georeferenced cadastral buildings and regional Geofabrik roads. Earlier source IDs retained;8764 suitable new regional IDs added,800 additional cadastral records. Capture-only projected-frustum crop avoids renderer memory exhaustion without changing source geometry. Existing art pixels unchanged.


## 2026-11-16 left5

Append tile at(-1.25,-1.25),size(0.25,3.5),total7168x7168,approx4.833km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Seven aligned panels with regional roads and507 additional cadastral records. Circular market complex kept as covered concentric rings; rejected stadium-like draft. Last panels use1024px overlap. All prior art preserved exactly; narrow capture-only projected crop, full model archived.


## 2026-11-16 bottom8

Append tile at(-1.25,2.25),size(3.5,0.25),total7168x7680,approx5.179km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Seven geometry-led illustrated panels extending the principal candidate, final overlap1024. Prior24sourceimages unchanged. Regionalroads alreadycached;2615newCatastrorecords. Current2026facades pending.


## 2026-11-16 right7

Append tile at(2.25,-1.25),size(0.25,3.75),total7680x7680,approx5.548km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Seven geometry-led panels; all existing cadastral and regionalroad records cover this strip, no newIDs. No citywide currentfacadeclaim.


## 2026-11-16 bottom9

Append tile at(-1.25,2.5),size(3.75,0.25),total7680x8192,approx5.918km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Seven panels visually inspected. Three seam segments inspected. Prior26sourcebytes and original3D preserved. Reference preflight PNOAJuly2024 at3points: barefields/dirtpaths retained, no claim2026facades. Temporary image precision interruptions recovered for all7production panels.


## 2026-11-16 right8

Append tile at(2.5,-1.25),size(0.25,4.0),total8192x8192,approx6.313km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Dated PNOA July2024 preflight. Seven successful high-detail panels cover entire strip; F/H meet at contiguous pixel6656 after redundant G timed out. Join visually inspected. No current-facade claim.


## 2026-11-16 right9

Append tile at(2.75,-1.25),size(0.25,4.0),total8704x8192,approx6.707km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Contiguous city-core extension; railway alignments recovered from the existing regional cache, estimated track widths. PNOA July2024 three-point date check and same-camera reference preflight; no2026facade claim. F3overlap repairs rejected zero-overlap roof-ground seam.


## 2026-11-16 active city-only scope

Continue the contiguous Albacete city core. No pedanias or automatic detached industrial/park additions. Prior source inventories stay available as evidence, not additional obligations. Administrative neighborhood/planning candidates do not require filling every polygon. Existing art, general map and rotating3D remain intact.


## 2026-11-16 right10

Append tile at(3.0,-1.25),size(0.25,4.0),total9216x8192,approx7.102km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Contiguous city-core extension. PNOA July2024 three-point date check and same-camera reference preflight preserve dry vacant ground and low flat institutional sites; no2026facade claim. Seven overlapping panels visually checked, previous29art sources preserved.


## 2026-11-16 right11

Append tile at(3.25,-1.25),size(0.25,4.0),total9728x8192,approx7.497km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Contiguous city-core extension. PNOA July2024 same-camera preflight retains low flat grey institutional roofs, dry vacant lots and construction. Seven overlapping panels and seams visually checked; previous30art sources preserved. No2026facade claim.


## 2026-11-16 left6

Append tile at(-1.5,-1.25),size(0.25,4.0),total10240x8192,approx7.891km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Contiguous city-core extension using existing model sources. PNOA July2024 same-camera preflight, railway fan, irregular central blocks and paved feria forecourt. Seven overlapping panels and joins visually checked, previous31art sources preserved. No2026facade claim.


## 2026-11-16 left7

Append tile at(-1.75,-1.25),size(0.25,4.0),total10752x8192,approx8.286km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. Contiguous city strip. Same-camera PNOA July2024 samples. Interpretation, not surveyed facades. No new source records.


## 2026-11-16 right12

Append tile at(3.5,-1.25),size(0.25,4.0),total11264x8192,approx8.680km2 groundenvelope, notcitypercentage. Originalart/coordinatespreserved. No current-facadeclaim.0EUR,nobilling,nocontact. Internalprogressonlyuntilcitycomplete. RIGHT12 contiguous campus/sports edge. PNOA July2024 same-camera ground reference, municipal2021/2024 tree palette; varied rounded broadleaf crowns in new artwork, not botanical inventory. Existing artwork untouched; full city tree corrections pending.

## 2026-11-17 Palace of Justice reference correction

Replaced the invented red-tile residential treatment only at the Palace of Justice, cadastral parcel 9471408WJ9197A, after matching PNOA July 2024 footprint to Altozano and San Agustin corner. Front and side appearance grounded in official Street View May/November 2025. Modern pale stone, regular narrow window grid, horizontal bands and flat roofs replace the false historicist houses. Rear height/massing follows cadastral parts as an estimate, not a survey. No historical eagle copied. Existing Gran Hotel and red historic neighbor remain untouched. Surrounding plaza surfaces/tree positions remain unreviewed and are not certified by this correction. Bounded replacement preserves all outside decoded source pixels; changed source WebPs are lossless. Extent remains RIGHT12 with 34 sources. Private LEFT8/RIGHT13 candidates are not included. Both general map and rotating 3D assets unchanged. Detailed source/limitations record: ilustrado/justice-reference-20261117.json.

### Comparison-label correction
The former "Base geometrica" layer was inspected at close zoom and found to be a historical working montage containing previous illustration as well as geometric expansion captures, not a pure geometric reference. Renamed it "Vista de trabajo previa" and added explicit explanation in viewer and sources. No layers removed and no comparison imagery changed. Added dated Justice reference provenance and remaining facade/surface limits to the source page. It must not be used as independent evidence for fidelity.

### Station and north rail corridor, 17 November
Replace only a bounded continuous railway/station corridor, not the north neighbourhood wholesale. Current OSM line geometry and five registered PNOA crops dated July 2024 identify both northeastern dark bands as railway, not asphalt highways. Earlier contrary visual diagnosis was withdrawn, as was any general claim that newer north buildings were invented. Retain newer urban blocks unless independently disproven. Station massing, white platform roofs, solar parking and west depot follow aerial layout and station architect/operator references. Art remains interpretive, including individual tracks, switches, vegetation and fine facade details.
Four overlapping rail seams and a narrow station south-edge transition repaired after actual pixel review. Source-image changes are zero outside the saved bounded mask; exact high-resolution pyramid equals the integrated montage. Extent remains 11264 x 8192, 34 source images. No citywide fidelity or coverage claim. Mobile390/desktop1280 inspected, comparison preserves viewport, existing map and 3D links retained. No spend, billing setup or third-party contact.

### RIGHT13 reference-led city extension, 17 November
Add one512x8192source strip to the east at worldx3.75, total11776x8192 and35sourceimages. PNOA aerial layout and sample acquisition datesJuly2024, current OSM building-footprint inventory477ways, cached municipal Catastro geometry. These do not certify 2026facades. Keep dated sources distinct; March2025SanVicentePaul views are west of this strip and do not authenticate these exact blocks. No wholesale deletion from older imagery.
Football stadium changed from erroneous initial athletic-oval candidate to rectangular stands/pitch matching aerial reference; separate blue athletic oval retained. North continues both real railway corridors and sparse field layout. Only339072existingdecodedpixels changed in a buffered north join within right12; every other existing source pixel remains unchanged. Both display pyramids exact at native level. Comparison grows from historical working view and geometric addition, explicitly not a pure geometry control. Original map and rotating3D files identical.
Area9.074826km2is camera ground envelope only, not city completion. No completion percentage or claim of allcity. Art style highly detailed, fine roofs/facades/trees interpreted. No spend, billing or contact. Preserve user silence.

### LEFT8 west edge and bounded north repairs, 2026-11-17
Added one contiguous west strip and reconciled only explicit old-image join and NW masks. Current OSM footprints plus dated PNOA support open western plots and low sheds. The real CIAb water tower is retained as a tall shaft and elevated tank, with operator description and September 2026 photos as references; it is not an invented squat roof cylinder. Upper north asphalt and lower rail corridors remain distinct. No blanket railway/highway conversion. Source images are lossless WebP; historical working comparison is now JPEG to avoid memory failure and is not independent geometric evidence. Native pyramids match source pixels. Previous pixels outside correction masks, general map and 3D source files are unchanged against baec131. Reference-led interpretation remains, not a current parcel inventory or exact architectural replica. Camera envelope does not measure city completion.

### LEFT9 contiguous west continuation, 2026-11-17
Extended the adjacent west strip with current OSM footprint cross-checks (359 ways in four rectangles) and registered PNOA sampled July 2024. Open land, low sheds, school/sports grounds, apartment slabs and residential blocks follow those references; ordinary facade and tree details remain interpreted. Rejected variants that copied the landmark park into the wrong panel or replaced a sports pitch with orchard. Adjusted the private C/D seam to avoid a duplicated small roundabout. Existing water tower and all old pixels outside a narrow left8 overlap remain exact against fbdc7dc. Only591227 old pixels changed, confined to that overlap. All400 native tiles in each pyramid match their source. Map general and rotating3D sources remain exact. The9.8639409km2camera envelope is not complete-city coverage or a completion percentage.

### LEFT10 contiguous west continuation, 2026-11-17
Advanced one adjacent west strip after checking the historical neighborhood outline against the current camera envelope. The administrative outline is not a mandatory fill mask. Current OSM470footprint ways and PNOA July2024 samples ground low residential blocks, sports pitch, dry plots, the small paired-loop road footbridge and the separate railway corridor. A missing private preparation-mesh fringe was expanded without changing the public rotating3D. All37previous sources checked: only661032pixels ofleft9 changed, strictly within the narrow overlap mask.416native art tiles and416comparison tiles match their sources. Map and public3D remain exact against754dd6d. No completion percentage;10.2584986km2is the ground-plane camera envelope only. One image request timed out and was retried successfully. No new billable resources or external contact.

## 2026-11-17: siguiente continuidad oeste (LEFT16)

- Se conserva el mapa general y la zona 3D sin cambios. La ilustración añade512px al oeste:46fragmentos fuente,17408×8192px. La envolvente13,414960km² no es superficie urbana completada ni porcentaje de ciudad.
- Base da88b7f. Solo left15.webp previo cambia:715954píxeles dentro de la máscara explícita de solape. Las otras44fuentes previas no cambian. Siete paneles y siete uniones continuas inspeccionados antes de integrar.
- Referencias:220huellas OSM y842corredores en cuatro rectángulos,108partes catastrales añadidas al modelo de trabajo. PNOA recuperado17nov, tres muestras fechadas julio2024. El ferrocarril queda separado de las carreteras elevadas. No se certifica vigencia2026 de todas las fachadas.
- Se conservan vacíos, cultivos y pistas. No se rellenan automáticamente polígonos administrativos ni se incluyen pedanías o polígonos industriales separados. El montaje RIGHT16 incompleto no forma parte de este cambio.
- Pirámides reconstruidas0–15,544teselas nativas por vista. QA local390/1280:sin errores JS/HTTP,pellizco,Catedral,mapa,rotación3D y comparación sin salto. Publicación en el proyecto existente sin activar facturación.

## 2026-11-17: Universidad/Medicina con borde escalonado, sin continuación rural

- Se aprovecha solo el tramo previamente dibujado de RIGHT16 hasta5632px. Se añade una fuente512×5632 junto al campus y se deja fuera de esta ampliación el jardín botánico y la continuación rural. No se ha creado imagen para rellenar la esquina. Las áreas vecinas previamente dibujadas se conservan.
- El atlas17920×8192 tiene una esquina transparente512×2560. Al centrar el visor fuera de las fuentes, el rótulo lo identifica como fuera del área ilustrada. Es un límite de esta entrega de arte, no el borde urbano definitivo.
- La huella se calcula como unión de rectángulos fuente reales antes de proyectarlos al terreno.555celdas equivalentes, no560de la caja.13,686218km² dehuella dearte, no porcentaje de ciudad. Pruebas: sin agujeros interiores, sin pérdida previa y11celdas nuevas. Ledger actualizado con el mismo método.
- Base9d80cc9.46fuentes previas auditadas:solo420246píxeles de right15 cambian dentro de máscara.45restantes, mapa y3D byteexactos.47fuentes en total.
- Las referencias de los rectángulos de investigación, más amplios que este recorte, incluyen715huellas y1229corredoresOSM,PNOAjulio2024 en3muestras y94partescatastrales de apoyo. No son una revisión exhaustiva de fachadas2026.
- QA local390/1280 de campus,cruceferroviario,esquina transparente,comparaciónsin salto,pellizco,Catedral,mapayrotación3D.560teselas nativas de cada vista comprobadas pixel a pixel. Sin nuevos servicios ni facturación.

## 2026-11-17: bounded Medicina continuity RIGHT17

Added a512×4096source at world[4.75,-.75,5,1.25], using existing RIGHT16 as fixed overlap. PNOA July2024 samples, mapped footprints and OSM corridors guide layout; facade and vegetation details are artistic interpretation. Eight new source cells, actual union563cells versus576atlas cells. Transparent stepped exterior is explicitly outside supplied illustration, not missing completed art or a claim to city completion. Only right16 changes within an explicit overlap mask (441141pixels); all other46previous sources and general map/rotating3D remain unchanged. Native576tiles per view verified pixel-exact, no interior coverage holes or old cell regressions. Local390/1280QA includes pinch, cathedral, map,3Drotation and comparison without camera jump. Two preliminary panelc outputs that shifted framing were discarded, not integrated. Main sources and limitations in right17-reference-20261117.json. Remains city-core only and0EUR, no new billing or resources.


## RIGHT18 bounded residential continuation, 2026-11-17

Added eight cells at x5..5.25,y-.75..1.25, using PNOA July2024 (three samples) and live OSM. Facades and vegetation remain artistic interpretation.49 sources,18944×8192 atlas,571 actual source-union cells rather than592 rectangular bounds cells;14.080775667113734km² is coverage, not city completion. Only351284 pixels of right17 changed inside explicit overlap mask;other47 prior sources and general map/rotating3D exact. All592 native tiles per view checked pixel-exact. Ledger412→414 candidate intersections, no old fraction regressions. Sparse exterior remains transparent and labelled. No detached sectors or pedanias added. Municipal reference cache is16Nov, refresh17Nov timed out.


## BOTTOM10 localized south tip, 2026-11-17

Four cells only at x1.5..2.5,y2.75..3, not a full atlas row. PNOA July2024 (three samples), live OSM and cached footprint layout support low attached houses, patios/workshops and fields. Earlier tall artistic volumes above the seam remain unchanged, not verified heights. Generated art did not preserve the top reference; registration to artwork failed (2 matches, rejected). Selected ground-to-PNOA registration235inliers,median0.743px; preserved original pixels outside min-cost seam mask.50sources18944×8704,575actual source cells/629bounds,14.17941507634051km²,not completion.Only164756pixels of bottom9 changed,other48source/map/3D exact.629native tiles/view exact. Ledger414→418,no fraction regressions. First comparison build exhausted memory without publication; builder changed to skip unnecessary RGBA atlas loading for comparison, full rebuild and pixel validation passed. Sparse exterior remains transparent.No detached additions.


## RIGHT19 seven-cell residential ring-road continuation, 2026-11-17

Added x5.25..5.5,y-.75..1 only. Excluded last lower generated512row: no automatic full-height edge fill. PNOA July2024 three-point check, live OSM359building ways/755corridor ways. Triangular courtyard/pool and curved avenue confirmed in aerial; roof/facade interpretation remains non-exact.51sources19456×8704,582actual source-union cells/646bounds,14.35203404248763km²,not completion.Only372286pixels right18 changed inside explicit mask,49other sources/map/3D exact.646native tiles/view pixel-exact. Reference-art registrations3109/1570/2403inliers,median0.42/0.54/0.40px. Local390/1280QA passed0JS/HTTP, pinch,3Drotation,comparison without jump.

## 2026-11-17 BOTTOM11 localized Vereda edge
Four cells x-0.5..0.5,y2.75..3. July2024 PNOA and live OSM, original art registration1632inliers median0.499px. PNOA automatic registration rejected(2matches). Existing sources all unchanged except237196 masked bottom9 pixels. Preserve older artistic heights above seam, not surveyed. No detached outskirts added. Memory-safe tiled pyramid build, native tiles checked exact; lower levels use contextual Lanczos reduction.

## 2026-11-17 RIGHT20 bounded Calle Maraton
Two sourcecells x5.5..5.75,y.25...75 complete the contiguous pale-roof blocks.1794artregistrationinliers,median0.421px;3PNOAsamplesJuly2024,liveOSM.Only94581maskedright19pixels changed;51other sources exact,map/3D exact.663native tiles perview checked,588actualcells/663bounds,14.499993156327605km2. Not completion or current2026survey. Wider researched lower ground excluded.

## 2026-11-17 LEFT17 bounded Canicas
Eleven new sourcecells complete contiguous shopping center and sports facilities. Top-left motorway-side cell excluded. Two registered panels1064/1241inliers,median0.672/0.721px. ThreePNOAsamplesJuly2024 plus liveOSM.350217maskedleft16pixels changed;52other sources exact,map/3D exact.697native tiles/view pixel-exact,599actualcells/697bounds,14.77125153170115km2. Not completion or current2026survey.

## 2026-11-17 LEFT18 dated construction interpretation
One512square cell x[-4.25,-4],y[.75,1] completes city-side construction site. Two exact currentOSM construction footprints(lastedit7Mar2025),threePNOAsamplesJuly2024,andmunicipality24Mar2026streetnamecontext;3Nov2026reportUA2beingbuilt. Art explicitly depicts dated2024foundations,notcertified2026floorheightsorcompletion. No finished future blocks or pools. PrivateEsri19Sep2025contrastnotinputtogenerationorpublished. V1rejectedfootprintdrift,V2correctedwithannotatedOSM,V3onlyboundedroadjoin.2074registrationinliers,median0.462px.96539maskedoldpixelschangedinleft16/left17a,53otherprior sources exact,map/3D exact.697native tiles/viewpixel-exact,600actualcells/697bounds,14.79591138400819km2,ledger421to422noregression. Notcitycompletion.

## 2026-11-17 inventory derived-fact refresh
Historical point inventories imported stale art extents. Recompute against actualcurrent sourceunion afterevery scopeapply. Science/Botanicpointsinside;Botanicpolygon0.011441043206623334km2inside,0.05852223751175938outside. Pulgosa0overlap,polygon478.4334933644463mfromart,point856.6896372593111m. Pointsarenotwhole-sitecoverage. Sourcegeometrydatespreserved,notcurrent2026survey. Noimage/catalog/map/3Dchange,56sourcefilesexact.

## 2026-11-21 Objeto 32 (nave junto a edificio curvo) restaurado por contorno de objeto

Reanudacion autorizada por Rafa el 21 nov ("Avanza tuuuu"). Primera correccion aplicada con la via de objeto completo aceptada en local el 18 nov, nunca desplegada entonces.

- Produccion anterior mostraba bloques residenciales de teja inventados; la ortofoto PNOA (mosaico mas reciente, servida 2026-11-21 via WMS IGN) muestra una nave industrial blanca junto al edificio curvo y la rotonda. Contraste geografico rehecho hoy de forma independiente (registro marco atlas->UTM validado contra edificio curvo, rotonda y plaza circular); la nave, aceras y cruce coinciden con la referencia. PNOA no prueba estado 2026 ni fachada exacta.
- Composicion por poligono de contorno de objeto (16 vertices) con desenfoque de 1 px sobre right5.webp; 32.470 pixeles cambiados en L15, 16 teselas de piramide, cero diferencias RGBA fuera del soporte y su proyeccion en todos los niveles, alfa original intacto. Reproducible con el paquete isolated32 (compose.py/atlas.py/verify.py).
- QA visual propia a resolucion nativa y niveles 14/13/12: integracion sin costuras, rectangulos ni velos; vecinos conservados pixel a pixel. right5.webp y manifiesto actualizados; mapa general, 3D y demas fuentes sin cambios.

## 2026-11-21 — Restauración de 5 regiones invertidas el 18 nov (35, 40, 42, 44, 45)

- El 18 nov se revirtieron por caja 5 regiones que la comparación con PNOA
  muestra correctas en el contenido previo. Reintegración quirúrgica:
  donante f7651d32 (previo a lotes 14–22), soporte = dif |donante−actual|>12
  dilatada 3 px con pluma 1.5 px; 0 difs RGBA fuera del soporte en cada
  pirámide; alfa idéntico. Fuentes webp actualizadas igualmente.
- Regiones: 35 (patios en zigzag CEIP), 40 (parking + glorieta),
  42 (nave gris + campos), 44 (colegio con pistas roja/azul),
  45 (borde urbano: suprimido ferrocarril inventado).
- Verificación: 0 difs fuera de soporte en todos los niveles; hoja L14 y
  recortes de borde a resolución nativa sin costuras; trípticos por región
  contra PNOA.
- Región 33: EXCLUIDA de este lote — el donante tiene el borde del campo
  verde difuso que el 18 nov motivó la reversión; pendiente reparación
  guiada por PNOA, no publicación del donante tal cual.
- Regiones 20/47/51: sin cambios (bloqueadas 18 nov).

## 2026-11-21 — Celda 12,8: eliminado el segundo coso inventado

- El atlas original contenía dos plazas de toros: la real (15,8, verificada
  alineada con PNOA) y un coso inventado en 12,8 sobre manzanas ordinarias
  (PNOA y Catastro: bloques de viviendas y plazuela). Contenido del atlas
  original, no de lotes 1–22, por lo que no cabía reversión: sustitución
  guiada por ortofoto (edición de imagen con doble referencia, atlas+PNOA).
- Integración por soporte: componente conectada del diff suavizado
  (umbral sobre media local, dilatación 20 px hasta ejes de calle, pluma
  2 px). 0 difs RGBA fuera del soporte en todos los niveles; alfa intacto.
- Verificación: 0 difs fuera de soporte; cuatro bordes inspeccionados a
  resolución nativa sin costuras; tríptico actual|nuevo|PNOA conforme;
  consistencia del warp PNOA comprobada por solape (dif media 4,9).
- Alcance de la corrección: la ELIMINACIÓN del coso está contrastada con
  PNOA+Catastro (no existe tal edificio; hay manzanas y plazuela). El
  reemplazo es ilustración interpretada: tipología (bloques con patios y
  plazuela) y trazado viario contrastados con la ortofoto, pero las
  viviendas, patios y árboles individuales generados NO están verificados
  uno a uno contra referencia. No computa como verificación geométrica.
- Fuentes left5–left8 actualizadas en consecuencia.

## 2026-11-21 — Celda 31,15: eliminados vía férrea y estación inventadas

- El atlas original dibujaba una vía con estación en el sureste (huertas),
  sin respaldo en PNOA 2024 ni en la realidad del enclave: sustitución
  guiada por ortofoto (edición con doble referencia atlas+PNOA).
- Integración por soporte: componente conectada del diff suavizado,
  dilatación 20 px, pluma 2 px. 0 difs RGBA fuera del soporte en todos los
  niveles; alfa intacto (el soporte queda por encima del borde de encuadre
  y=8192). Fuentes right10–right13 actualizadas.
- Verificación: bordes internos y externos (incluido el borde del propio
  recorte) inspeccionados a resolución nativa sin costuras; tríptico
  antes|después|PNOA conforme.
- Alcance: la ELIMINACIÓN de vía y estación está contrastada con PNOA
  (ausencia en la referencia). El reemplazo (huertas, caminos de tierra,
  lindes) es ilustración interpretada coherente con el entorno y la
  ortofoto, NO verificación parcela a parcela.

## 2026-11-21 — Celda 25,13: nave logística genérica corregida a lo que muestra PNOA

- El atlas original dibujaba una nave logística tan con camiones donde PNOA
  muestra una gran cubierta gris con filas de paneles solares y pabellón
  blanco adosado, y una nave pequeña con patio donde PNOA muestra un
  complejo deportivo (pista de atletismo roja, pabellón, campo de fútbol).
  Sustitución guiada por ortofoto (edición con doble referencia).
- Integración por soporte de diff conectado (dilatación 20 px, pluma 2 px).
  0 difs RGBA fuera del soporte en todos los niveles; alfa intacto.
  Fuentes bottom6–8 y right5–6 actualizadas.
- Verificación: cuatro bordes a resolución nativa sin costuras; tríptico
  antes|después|PNOA conforme.
- Alcance: contrastado con PNOA — la cubierta con paneles solares, el
  pabellón adosado y la existencia/disposición del complejo deportivo.
  Interpretado — detalle fino de paneles, líneas de las pistas y
  vegetación interior (no verificables a esta escala).

## 2026-11-21 — Celda 25,13 (revisión): complejo deportivo rehecho con la geometría de PNOA

- La primera sustitución del complejo deportivo dejaba el campo de fútbol
  como rectángulo verde separado y superficies rojas rectangulares; PNOA
  muestra un único estadio: óvalo de atletismo color arena que encierra el
  campo, pabellón largo de cubierta blanca con lucernarios circulares al
  suroeste, pista pequeña rojiza al sureste y gradas en cuña al sur.
- Re-edición guiada por ortofoto solo del complejo (crop 700×700 en
  12500,6650). Soporte 125.641 px, sin tocar bordes del crop; 0 difs RGBA
  fuera del soporte; alfa intacto; cuatro bordes nativos limpios.
- Contrastado con PNOA: óvalo que encierra el campo, pabellón blanco con
  círculos al SO, pista rojiza al SE. Interpretado: color exacto de la
  pista, líneas, gradas y vegetación interior.

## 2026-11-21 — Celda 25,13 (rectificación): el estadio ovalado era un error mío; restaurado el campo de tierra real

- Rectificación de la entrada anterior: la pista ovalada de atletismo que
  dibujé en la revisión anterior NO está respaldada por la referencia.
  Verificación con fuentes identificables (consultadas 2026-11-21):
  · Nominatim/OSM (38.984171,-1.869209): Calle Méjico, barrio Pedro Lamata.
    https://nominatim.openstreetmap.org/reverse?lat=38.984171&lon=-1.869209&zoom=18&format=jsonv2&accept-language=es
  · Censo de Instalaciones Deportivas de Castilla-La Mancha (CSV oficial):
    CAMPO DE FÚTBOL 'PEDRO LAMATA', PISTA POLIDEPORTIVA 'PEDRO LAMATA',
    PISTAS DE PETANCA 'PEDRO LAMATA'.
    https://datosabiertos.castillalamancha.es/sites/datosabiertos.castillalamancha.es/files/Listado%20Censo%20Instalaciones%20Deportivas%20CLM.csv
  · PNOA WMS IGN ampliada: campo de tierra RECTANGULAR con marcas blancas,
    sin óvalo; pista polideportiva roja al SE; edificio de franja blanca con
    lucernarios circulares al SO; calles de petanca al S.
- Corrección: el estadio se sustituye por el campo de fútbol de tierra
  rectangular (misma huella y orientación que en PNOA). Se conservan del
  trabajo previo el pabellón blanco con círculos (SO), la pista roja (SE),
  las pistas de petanca (S) y la cubierta solar industrial.
- Soporte 40.724 px centrado, sin tocar bordes; 0 difs RGBA fuera; alfa
  intacto; cuatro bordes nativos limpios.
- Contrastado: rectangularidad del campo, marcas de fútbol, pista
  polideportiva SE, pabellón SO, petanca S. Interpretado: textura fina de
  la tierra, porterías y líneas exactas.
