# Tiny Albacete — estado recuperable (21 nov 2026, 17:15 CET)

## Verdad actual
- Rama de registro: art-bottom-extension-3 (HEAD 85fd98be). main = espejo viejo, NO usar.
- Produccion https://tiny-albacete.pages.dev == contenido del deploy eb471c73 (22 archivos del 31,11 verificados sha256). DECISIONS.md en prod va un commit por detras (docs-only, sin impacto visual).
- Deploy: desde RAIZ /tmp/tiny-albacete: CLOUDFLARE_API_TOKEN=$(cat /home/sandbox/.vault/cloudflare-entre-dos-deploy-token-instinct-45fbd0/password) CLOUDFLARE_ACCOUNT_ID=abbb1b9304d4ac2efd8ac10fc3039459 npx -y wrangler@4 pages deploy . --project-name tiny-albacete --branch main --commit-dirty=true
- Push: GIT_ASKPASS=/tmp/askpass.sh git push origin HEAD:art-bottom-extension-3 (PAT en vault, askpass en /tmp/askpass.sh del workspace box).
- Geo: celda (c,r) -> L15 px (c*512, r*512); frame 20992x8704. Affine atlas->UTM30 en ops/build.py (M, off2). PNOA WMS IGN OI.OrthoimageCoverage EPSG:25830; receta pnoa_scaled corregida en worklog 17:12.

## Metodo validado (6 correcciones publicadas hoy)
image.edit smart, refs [crop atlas, PNOA mismo extent], aspecto 1:1; soporte = componente conectada mayor del diff suavizado (Gauss 24, >32), dilate MaxFilter 41, pluma Gauss 2; composite; 0 diffs fuera del soporte; QA visual de 4 bandas de borde a res nativa (+straddle si el soporte toca borde); propagacion L15->L0 con mascara, RGBA alfa preservado; patch webps fuente via tiles.json; manifest+DECISIONS (contraste vs interpretado, URLs+fechas); commit+push+deploy; sha256 de los cambiados en prod.
Regla 429 (main 12:01): tras 3 429 seguidos, proximo intento >=1h despues del ultimo. Cuota org compartida 250/min ajena.
NUNCA: parches rectangulares con pluma, reversion por caja, borrado de contenido aprobado sin evidencia, deploy desde ilustrado/.

## Hecho hoy (21 nov, todo verificado sha256 en prod)
objeto 32; donantes 35/40/42/44/45; retirada coso 12,8; retirada via+estacion 31,15; 25,13 nave solar + complejo Pedro Lamata (con rectificacion del ovalo: campo rectangular, commits 4348a04d+3c90d371); 31,11 estadio atletismo UCLM completo (62112b4e). Fuentes+fechas en DECISIONS.md.

## Verificado sin accion
24,13, 20,11 coinciden con PNOA. 25,8 PARCIAL: emplazamiento+extension si, interior estilizado no verificado.

## Pendiente (orden)
1. 27,1 tejido inventado (bloques 3-4 plantas vs tejido bajo disperso PNOA). Refs /tmp/restore_work/edit27_1_cur.png+edit27_1_pnoa.png; box 13440,128,1280,1280; EXCLUIR banda autovia (y<410) del soporte; OUT=atlas_n27. Wake 18:05 con prompt completo.
2. 28,1: RE-ENSAMBLAR cur tras publicar 27,1 (solape 768px); pnoa /tmp/restore_work/edit28_1_pnoa.png; box 13952,128,1280,1280; OUT=atlas_n28.
3. Zona SE (~30 celdas, col 28-34, filas 11-17; evidencia /downloads/se_survey.jpg; main 17:07 la incluye en alcance, SIN ampliar perimetro). NO por bloques fijos (main 17:12): segmentar por escenas reales del PNOA (colegio/pistas, poligono de naves, arcos de cultivo entre carreteras) con bordes de escena (viales, lindes) dentro del crop con margen; soporte por escena; preservar trazado respaldado y acabado. En 30,15 el soporte se recorta al alfa del arte.
4. Region 33 (borde donante defectuoso en campo verde, reparacion guiada).
5. Piscinas PNOA ~(14340-14540,1500-1560, celda 28,2) ausentes en atlas — evaluar.
6. Barrido bandas 76px + bordes 30%; Campollano (decision aplazada por main 18 nov); reconciliacion inventario por ID.

## Separacion de epocas (main 17:12)
PNOA = vuelo 2024 (contraste geometrico). Nunca presentar como estado 2026. Fuentes 2026 (Nominatim, censo CLM, UCLM) ya citadas con fecha en DECISIONS.

## Recursos no versionados clave (workspace box)
/tmp/restore_work/: worklog en /tmp/worklog_tiny_albacete.md (fuera de repo; copia enviada a main), refs de edits en cola, srcbackup_* (webps originales), prop_*_log.json, atlas_vel/atlas_sc2 (tiles propagados ya publicados). /downloads: evidencias (tri_*, lm_*, sc_*, wide_*, se_survey, *_hires). Paquete zip enviado a main como adjunto antes del relevo.
