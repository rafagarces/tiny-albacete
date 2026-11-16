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
