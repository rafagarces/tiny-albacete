# Zona SE — plan por escenas (21 nov 18:20, analisis sobre se_pnoa_mid.jpg + se_atlas_mid.jpg)
Registro verificado (estadio 31,11 y borde urbano oeste anclan <10px). Ref: PNOA vuelo 2024.
El atlas dibuja un suburbio-jardin inventado (chalets, viales sinuosos, rotondas, piscinas, pistas) donde PNOA muestra: campos de cultivo en arcos, casas rurales dispersas, un vertedero/chatarra central, lineas de arboles, industria rural a lo largo del anillo.
El atlas SI respeta aproximadamente el trazado del anillo (carretera curva que entra por el oeste ~y5900, baja al sur y sale por el este) -> preservarlo como conexion respaldada.
Borde del arte (alfa 0): desde ~y8185 en x>14350 hacia el este; el extremo oeste (x<14350) sigue por debajo de 8704. 30,15: soporte recortado a alfa.

Escenas (orden = juntas caen en territorio ya corregido; bordes de escena dentro del crop con margen):
1. S2 norte-interior: box (14848,5632,1280,1280). PNOA: campos + casas dispersas + matorral; borde N = tejido real ya verificado (adyacente al estadio), W = borde urbano real.
2. S3 este-interior: box (16128,5632,1280,1280). PNOA: campos grandes + lineas de arboles + caserio en borde E; adyacente a S2 corregida.
3. S4 vertedero+anillo oeste: box (14848,6912,1280,1280). PNOA: cluster chatarra + industria rural junto al anillo; adyacente a S2.
4. S5 colina 30,15: box (16128,6912,1280,1280). PNOA: naves dispersas; soporte recortado al alfa del arte (NO ampliar perimetro); adyacente a S3/S4.
5. S0 franja oeste: box (13056,6912,1280,1280). PNOA: tejido urbano continuo donde atlas pone matorral/parque; adyacente a tejido real verificado al N y W.
Por escena: refs cur(reensamblado justo antes)+pnoa; prompt = sustituir suburbio por escena real del PNOA (campos/casas/naves), preservar anillo y conexiones respaldadas; soporte=diff conectado (excluir nada salvo nota); QA 4 strips + straddle; pipeline normal. Reensamblar cur de cada escena DESPUES de publicar la anterior si se solapan.
