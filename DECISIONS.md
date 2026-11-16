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
