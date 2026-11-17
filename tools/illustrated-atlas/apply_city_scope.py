"""Apply user's city-only clarification after rebuilding historical source inventories.
No boundary clipping: an administrative/planning candidate is evidence, not required scope.
"""
from pathlib import Path
import json,shutil,re
r=Path('/tmp/fiel-albacete/art-release');p=r/'ilustrado/coverage-ledger.json';d=json.load(open(p));notice={'status':'contiguous-city-core-only','clarified':'2026-11-16','included':'Albacete continuous urban core; reference-led artistic interpretation','excluded':'Pedanias and other municipal settlements','deferred':'Ambiguous detached industrial/park additions are not presumed included.','candidate_caveat':'Administrative neighborhoods and planning-class union are research candidates, not an obligation to fill every polygon.','preservation':'Existing artwork and general map access preserved; no automatic clipping or deletion.','completion_percentage':None};d['active_scope']=notice
for row in d.get('exterior_inventory',[]):row['status']='excluded-from-city-only-task'if 'pedan' in row.get('name','').lower()else 'deferred-not-automatically-included-in-city-only-task'
for row in d.get('municipal_planning_components',[]):
 if not row['role'].startswith('principal'):row['role']='detached planning component retained as source evidence, not active city-only task'
for row in d.get('municipal_entities',[]):
 if isinstance(row,dict):row['status']='not-an-authorized-city-boundary; detached settlements excluded'
for key in ['southern_science_botanic_inventory','exterior_park_geometry_candidates','exterior_industrial_geometry_inventory']:
 if isinstance(d.get(key),dict):
  d[key]['active_scope_status']='deferred-not-automatically-included'
  for row in d[key].get('rows',[]):row['scope_status']='deferred-not-automatically-included-in-city-only-task'
if isinstance(d.get('singular_entity_inventory'),dict):
 d['singular_entity_inventory']['active_scope_status']='detached settlements excluded; source inventory is not a city boundary'
 for row in d['singular_entity_inventory'].get('rows',[]):row['status']='source-inventory-only; detached settlements excluded'
if isinstance(d.get('southern_pulgosa_inventory'),dict):d['southern_pulgosa_inventory']['scope_status']='deferred-not-automatically-included-in-city-only-task'
for key in ['expanded_principal_candidate','official_neighborhood_candidate']:
 if isinstance(d.get(key),dict):d[key]['scope_caveat']=notice['candidate_caveat']
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
for name in ['exterior-industrial-candidates.geojson','exterior-park-candidates.geojson']:
 p=r/'ilustrado'/name;j=json.load(open(p));j['active_scope_status']='source-inventory-only; additions-deferred-under-city-only-task'
 for f in j['features']:f['properties']['scope_status']='deferred-not-automatically-included-in-city-only-task'
 p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
p=r/'ilustrado/principal-extent-candidate.geojson';j=json.load(open(p));j['properties']['active_scope_caveat']=notice['candidate_caveat'];p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
p=r/'tools/illustrated-atlas/README.md';text=p.read_text();text=re.sub(r'\d+published cells currently intersect the429-cell principal-SIUcandidate\.', 'Published ground-envelope intersections are recorded in coverage-ledger.json; these are not completed reference reviews.', text);text=text.replace('all30disconnected SIUplanning components and named exterior industrial sectors without silently excluding them.','all30disconnected SIUplanning components and named exterior sectors as source inventory, not active city scope.');text=text.split('\n\n## City-only scope clarification')[0];text+='\n\n## City-only scope clarification 2026-11-16\n\nThe active task is the continuous Albacete city core. Pedanias and other detached municipal settlements are excluded. Ambiguous exterior industrial and park additions are deferred, not automatically included. Existing artwork and general map access remain intact. Administrative neighborhood and planning-class candidate polygons do not obligate filling every parcel. No city completion percentage is inferred. See city-scope.json.\n';p.write_text(text)
p=r/'tools/illustrated-atlas/city-scope.json';p.write_text(json.dumps(notice,indent=2)+'\n');destination=r/'tools/illustrated-atlas/apply_city_scope.py';shutil.copyfile(__file__,destination) if Path(__file__).resolve()!=destination.resolve() else None;print('city-only scope applied without deleting existing art or expanding to candidates')

# Every imported inventory may carry old art measurements. Refresh derived facts last.
import runpy
runpy.run_path("/tmp/fiel-albacete/refresh_inventory_measurements.py")

# Bounded completion of the same urban-edge Botanic landmark, not a new exterior target.
p=r/'ilustrado/coverage-ledger.json';d=json.load(open(p));scope_note='Same Botanic enclosure at the urban avenue entrance completed as a dated interpretation; no LaPulgosa or detached-sector expansion.'
d['active_scope']['bounded_landmark_completion']={'name':'Jardin Botanico de Castilla-La Mancha','date':'2026-11-17','scope':scope_note,'reference':'botanic19-reference-20261117.json'}
for key in ['southern_science_botanic_inventory','exterior_park_geometry_candidates']:
 group=d.get(key,{})
 if isinstance(group,dict):
  group['active_scope_status']='row-specific; Botanic enclosure included, other exterior candidates remain deferred'
  for row in group.get('rows',[]):
   if str(row.get('osm_way'))=='139980346' or 'bot' in row.get('name','').lower():row['scope_status']='included-bounded-same-Botanic-enclosure';row['scope_note']=scope_note
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
p=r/'ilustrado/exterior-park-candidates.geojson';j=json.load(open(p));j['active_scope_status']='row-specific; Botanic enclosure included, LaPulgosa remains deferred'
for f in j['features']:
 if str(f['properties'].get('osm_way'))=='139980346':f['properties']['scope_status']='included-bounded-same-Botanic-enclosure';f['properties']['scope_note']=scope_note
p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
p=r/'tools/illustrated-atlas/city-scope.json';j=json.load(open(p));j['bounded_landmark_completion']=d['active_scope']['bounded_landmark_completion'];p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
