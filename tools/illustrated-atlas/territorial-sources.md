# Territorial source ledger

Sources checked 16November2026. This is not a final city mask.

- Municipal administrative map index: https://www.albacete.es/es/ciudad/cartoteca/divisiones-administrativas . Official publisher. Describes25neighborhoods approved2016 and PDFmaps using2015base.
- Public folder linked by that index: https://aytoab365-my.sharepoint.com/:f:/g/personal/ayuntamiento_albacete_es/ElE9CmKfrRRPgZLkaFcnYqcBpIWlL8wooRP--SmTUHhllw?e=NYeWkf . Inspected general2016map visually. Single rasterPDF,966612bytes, image1653x1169. Boundary extraction from red lines rejected because letters/internaldivisions contaminate it. Registration fit106printedUTMcrosses,RMSpixel0.372,max0.789. Registration quality is not current boundary accuracy.
- Official SIUplanning classes: https://mapas.fomento.gob.es/arcgis/rest/services/SIU/CLASES_DE_SUELO/MapServer/0 . EPSG25830 municipalurban+nonconsolidatedunion18.4665km2,30components. Largest8.7814km2candidate does not match built-upcity or all administrative neighborhoods. Metadata2025 referencesGeneralPlan1999.
- PNOA service: https://www.ign.es/wms-inspire/pnoa-ma?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0 . Official orthophoto checked for territorial extent, not currentfacades. DateJuly2024/25cmverified at onlyonecentralpoint.
- Municipal economic infrastructure directory: https://www.albacete.es/es/empleo-promocion-economica/promocion-economica/infraestructuras-para-actividad-economica . Confirms Campollano,Romica,Ajusa,PALandSciencePark. Namedexteriorsectors explicitlypending, notexcluded.
- Municipal Romica description: https://www.albacete.es/es/directorio/poligono-industrial-romica . Places separateindustrialarea northofcity. No reliance on inconsistent areaheadline(near3millionversus2.7millionm2).
- Contemporary reporting about2016neighborhoodrevision: https://www.albaceteabierto.es/albacete-noticias/item/18963-albacete-actualiza-la-delimitacion-de-sus-barrios-para-conseguir-una-mejor-gestion-de-los-servicios-municipales . Secondarysource21June2016, corroborates25urbanneighborhoodsandseparateruraldistrict.

Allcoveragefiguresarefixed-cameraground-planeenvelopes,notfaithfullyverifiedfacades. No completionpercentage before an operationaltargethasbeencontrasted.

## Expanded principal candidate, still not final

The outer red line of the25neighborhood2016map was manually traced and visually overlaid on the source raster, avoiding the failed automatic extraction. Historic envelope12.3689km2. Its union with the largestSIUcomponent is archived separately as principal-extent-candidate.geojson, not a final2026city boundary or city completion denominator. This preserves parks and neighborhood areas missing from the planning-class-only candidate. Generalization about15-30m is much larger than the registration fit error.

PNOAJuly2024/25cmnowconfirmed atfive sample points acrossprincipalextentandCampollano, not everypixel. A live north-up ortho overview was visually inspected against the historic envelope andSIU. External industrial and detached settlement areas remain separately inventoried. Currentfacades still require thelaterreferencepass. ExactGetMapandGetFeatureInfoURLs are retained incoverage-ledger.json.


## Live municipal vectors recovered2026-11-16

The public municipal cartographic viewer exposes25neighborhood polygons (layer ws_albacete:barrios), described by the viewer as approved JGL29/06/2016. Actual database record timestamps run2022-2023, not evidence of current imagery. Sanitized geometry and names are archived in ilustrado/neighborhoods-official.geojson, with exact WFS URL and row-date provenance in municipal-vector-provenance.json. Official vector union12.277911km2 replaces the manual outer approximation for the principal candidate. Its union with the largest SIU component is12.639917km2 and still touches579gridcells. This remains a provisional administrative/planning candidate, not a2026built-edge mask or city-completion denominator. Ground-envelope intersection is now computed separately for all25neighborhoods. It is not verification of drawn facades or artistic completion.

18official singular entities are inventoried with unresolved scope, without substituting their administrative/statistical territories for built-up footprints. Industrial exteriors still need their own geometry and current-condition checks.

Sources:
- https://ide.ayto-albacete.es/gvsigonline/core/load_public_project/visorgenerico/
- https://ide.ayto-albacete.es/geoserver/ws_albacete/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=ws_albacete%3Abarrios&outputFormat=application%2Fjson&srsName=EPSG%3A4326&count=100
- https://ide.ayto-albacete.es/geoserver/ws_albacete/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=ws_albacete%3Aentidad_singular&outputFormat=application%2Fjson&srsName=EPSG%3A4326&count=1000


## Exterior geometry,16November2026

Four named OSM industrial landuse polygons recovered directly through bboxAPI; source URLs in exterior-evidence/*-source.json. They are community landuse boundaries, not official built-edge or final scope. Named geocode points all fall inside corresponding polygons, independently confirming location only. Campollano3.8282km2,Romica2.8281,Ajusa0.3199,PAL0.7538. Romica,Ajusa,PAL have no overlap with the downloaded SIU urban-class union, showing that even all30SIU components cannot define whole city. Campollano3.5786km2 lies outside principal candidate. No target percentage is introduced.

Fetched municipal descriptions: https://www.albacete.es/es/directorio/parque-empresarial-campollano ; https://www.albacete.es/es/directorio/poligono-industrial-romica ; https://www.albacete.es/es/directorio/parque-empresarial-ajusa ; https://www.albacete.es/es/directorio/parque-aeronautico-logistico . Undated descriptions, inconsistent extent figures across historical promotional documents, not polygon authority. Independent OSM-derived named sources fetched https://mapcarta.com/es/W205937669 and https://mapcarta.com/es/W31137184 .

PNOA inspected individually for industrial polygons. Acquisition metadata sampled centrally, stored in exterior-evidence/pnoa-point-dates.json; point month does not certify every pixel. Romica and Ajusa include large empty industrial plots: industrial landuse must not be filled with invented buildings. PAL outline cuts past structures along northeast edge and imagery has obscured land beyond: not a complete industrial built-edge. Campollano closeup initialWMS502twice, rounded whole-sector request succeeded. No2026currentness claim. Separate settlements remain an unresolved scope outcome, not silently excluded.


## Romica date-query recovery,16November2026

A rounded central200mx200mGetFeatureInfosample returned2024-07and0.25m. The exact centroid query had timedout twice. This dates the single rounded central sample, not all pixels nor2026conditions. Preserved response in exterior-evidence/romica-date-rounded.html and sourceURL in JSON.
