# Estado por celda del pase de fidelidad (fusion 21 nov 18:25)
Fuentes: sweep-class-20261118.txt (clases 18 nov: A=aceptable, M=menor, C=correccion clara, U=sin verificar; SOLO 70% central de cada celda -> bandas 76px y 30% bordes sin barrer), trabajo verificado hoy 21 nov (ver DECISIONS), plan SE ops/se_scene_plan.md.
Leyenda estado: HECHO=publicado y sha256 OK hoy; VERIF=contrastado con PNOA hoy sin accion; C/M/U=clase 18 nov pendiente; PARCIAL=verificado parcial.

## Franja norte (filas 0-2)
- 27,1 C + 28,1 C: EN CURSO (autorizadas 12:03; refs listas; esperando ventana de cuota).
- 26,1 C "bloques altos vs adosados bajos": cubierta en parte por el crop de 27,1 (x13440-13824); completar tras 27,1/28,1.
- 25,2 26,2 27,2 28,2 29,2 30,2 31,2 = C; 24,2 M; 34,2 M: SIGUIENTE BLOQUE tras fila 1 (juntas sur de 27,1/28,1 quedan dentro de esta zona; autorizado por alcance 17:07 sin consulta por celda). Nota: piscinas ausentes en 28,2 (PNOA ~14340-14540,1500-1560).
- 25,1: RETIRADA 18 nov (corte contra 26,1) + clase C -> pendiente de reconstruccion fiel, no solo retirada.
- 30,0 M, 31,0 M, 24,0 M, 24,1 M, 31,1 M, 32,1 M, 16,0 M, 17,0 M, 18,0 M, 23,0 M, 3,0 C, 6,0 C, 8,0 M: menores/varios, evaluar en barrido de bordes.

## Centro verificado hoy
- 24,13 VERIF (18 nov: C -> hoy coincide tras correccion 25,13). 20,11 VERIF. 25,8 PARCIAL (emplazamiento+extension; interior estilizado no verificado).
- 12,8 HECHO (coso retirado). 25,13 HECHO+rectificado (Pedro Lamata). 31,11 HECHO (estadio UCLM).

## Zona SE (filas 11-16) -> ops/se_scene_plan.md
- 29,13 U->mismatch confirmado hoy (suburbio vs naves/campos). 30,15 C->mismatch confirmado hoy (barrio colina vs naves; recorte a alfa).
- C pendientes: 24,15 26,15 31,15(hoy HECHO) 25,11 26,11 27,11 28,11 29,11 30,11 31,11(hoy HECHO) 27,12 28,12; M: 24,11 26,12 25,15 25,16 26,16.
- U (sweep no verifico, probablemente fuera del 70% o arte posterior): 29,1 30,1 26,13 27,13 28,13 30,13 31,13 32,13 24,14 26,14 27,14 28,14 29,14 30,14 31,14 27,15 28,15 29,15 32,15: verificar contra PNOA antes de clasificar.

## Inventario por ID de objetos (PENDIENTE, distinto del por-celda)
Fuentes identificadas: review_classification.json (48 items: 21 aceptable_o_no_concluyente, 11 aceptable_o_menor, 11 correccion_clara, 3 no_concluyente, 2 menor_dudoso), fidelity-restore-batches1-13-20261118.json (10 restauradas R1.1,R1.2,R3.1,R10.0,R10.3,R10.4,R10.5,R12.0,R13.1,R13.3; 4 kept_mild; retiradas 25,11+24,12+25,1), coverage-ledger.json, fidelity-batch1..22. Las cifras 18 nov (45 presentes/28 retiradas) aun no reconciliadas en una tabla unica.
