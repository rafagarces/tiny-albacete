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
