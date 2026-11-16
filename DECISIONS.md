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
