/* Tiny Albacete — visor isométrico. Implementación propia; experiencia inspirada en tinyvalencia.com */
(async () => {
  const C=CFG.C, TOP=CFG.TOP, W=CFG.W, H=CFG.H;
  const q=new URLSearchParams(location.search);
  const T=await fetch('tiles.json').then(r=>r.json());
  const PLACES=window.PLACES||[];

  // lat/lon ↔ píxeles del mapa
  const toPx=(lat,lon)=>{
    const e=(lon-CFG.LON0)*CFG.MLON, n=(lat-CFG.LAT0)*CFG.MLAT;
    return [(e+n)*C-CFG.sx0, (e-n)*0.5*C-CFG.sy0];
  };
  const toLl=(x,y)=>{
    const s=(x+CFG.sx0)/C, d=(y+CFG.sy0)/(0.5*C);
    const e=(s+d)/2, n=(s-d)/2;
    return [CFG.LAT0+n/CFG.MLAT, CFG.LON0+e/CFG.MLON];
  };
  const onMap=(x,y)=>x>=0&&y>=0&&x<W&&y<H;

  const BLANK='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
  const tileSource={
    width:W, height:H, tileSize:1024, maxLevel:TOP, minLevel:TOP-8,
    getTileUrl:(l,x,y)=> (T.have[l]||{})[`${x}_${y}`] ? `painted/${l}/${x}_${y}.webp` : BLANK,
  };

  const small=matchMedia('(max-width: 760px)').matches;
  const viewer=OpenSeadragon({
    id:'map', showNavigationControl:false,
    showNavigator:!small, navigatorPosition:'BOTTOM_LEFT', navigatorSizeRatio:0.17,
    navigatorAutoFade:false, navigatorMaintainSizeRatio:true, navigatorOpacity:1,
    maxZoomPixelRatio:3, minZoomImageRatio:0.6, visibilityRatio:0.35, constrainDuringPan:true,
    animationTime:1.0, springStiffness:7, zoomPerScroll:1.3, zoomPerClick:2,
    gestureSettingsMouse:{clickToZoom:false,dblClickToZoom:true,flickEnabled:true},
    gestureSettingsTouch:{pinchRotate:false,flickEnabled:true,dblClickToZoom:true},
    imageLoaderLimit:32, timeout:60000, preserveImageSizeOnResize:true,
    smoothTileEdgesMinZoom:Infinity,
    tileSources:[{tileSource,x:0,y:0,width:1}],
  });
  const vp=()=>viewer.viewport;
  const cw=()=>viewer.container.clientWidth||innerWidth;
  const vpZoomFor=z=>Math.pow(2,z-TOP)*W/cw();
  const zoomOf=vz=>TOP+Math.log2(vz*cw()/W);
  const pt=(x,y)=>new OpenSeadragon.Point(x/W,y/W);

  function jump({lat,lon,zoom}){
    const [x,y]=toPx(lat,lon);
    vp().panTo(pt(x,y),true); vp().zoomTo(vpZoomFor(zoom),pt(x,y),true);
  }
  function flyLl(lat,lon,zoom){
    const [x,y]=toPx(lat,lon);
    viewer.viewport.panTo(pt(x,y),false);
    viewer.viewport.zoomTo(vpZoomFor(zoom),pt(x,y),false);
  }
  function home(){ viewer.viewport.goHome(true); }

  // estado en la URL
  let t;
  viewer.addHandler('viewport-change',()=>{
    clearTimeout(t);
    t=setTimeout(()=>{
      const b=vp().getBounds(true);
      const [lat,lon]=toLl((b.x+b.width/2)*W,(b.y+b.height/2)*W);
      const p=new URLSearchParams(location.search);
      p.set('lat',lat.toFixed(6)); p.set('lng',lon.toFixed(6)); p.set('zoom',zoomOf(vp().getZoom(true)).toFixed(2));
      history.replaceState(null,'',`?${p}`);
    },250);
  });

  // apertura
  const START={lat:38.9942,lon:-1.8558,zoom:16.6};
  viewer.addHandler('open',()=>{
    if(q.has('lat')) jump({lat:+q.get('lat'),lon:+q.get('lng'),zoom:+(q.get('zoom')||16.5)});
    else jump(START);
  });

  // búsqueda
  const sb=document.getElementById('searchbox'), si=document.getElementById('searchInput'),
        sr=document.getElementById('searchResults');
  const norm=s=>s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');
  function showResults(list){
    sr.innerHTML='';
    for(const p of list.slice(0,12)){
      const li=document.createElement('li');
      li.textContent=p.n; li.setAttribute('role','option');
      li.onclick=()=>{ flyLl(p.lat,p.lon,17.2); sb.hidden=true; };
      sr.appendChild(li);
    }
  }
  function openSearch(){ sb.hidden=false; si.value=''; showResults(PLACES); si.focus(); }
  si.addEventListener('input',()=>{
    const v=norm(si.value.trim());
    showResults(v?PLACES.filter(p=>norm(p.n).includes(v)):PLACES);
  });
  document.getElementById('searchBtn').onclick=()=> sb.hidden?openSearch():(sb.hidden=true);

  // aleatorio
  function randomView(){
    const p=PLACES[Math.floor(Math.random()*PLACES.length)];
    if(p) flyLl(p.lat,p.lon,16.8+Math.random()*1.2);
  }
  document.getElementById('randBtn').onclick=randomView;

  // zoom visible + compartir
  document.getElementById('zinBtn').onclick=()=>{viewer.viewport.zoomBy(1.5);viewer.viewport.applyConstraints();};
  document.getElementById('zoutBtn').onclick=()=>{viewer.viewport.zoomBy(1/1.5);viewer.viewport.applyConstraints();};
  document.getElementById('shareBtn').onclick=async ()=>{
    const u=location.href;
    try{ await navigator.clipboard.writeText(u); toast('Enlace copiado'); }
    catch(e){ prompt('Copia el enlace:',u); }
  };
  function toast(msg){
    const t=document.createElement('div'); t.className='toast panel'; t.textContent=msg;
    document.body.appendChild(t); setTimeout(()=>t.remove(),1800);
  }

  // pantalla completa
  document.getElementById('fullBtn').onclick=()=>{
    if(document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen();
  };

  // about
  const dlg=document.getElementById('about');
  document.getElementById('aboutBtn').onclick=()=>dlg.showModal();
  document.getElementById('aboutLink').onclick=()=>dlg.showModal();

  // monstruos
  const monsterFiles={godzilla:'monsters/godzilla.png',robot:'monsters/robot.png',manchega:'monsters/manchega.png'};
  let monstersOn=false, monsterEls=[];
  const MONS=(window.MONSTERS||[]);
  function setMonsters(on){
    monstersOn=on;
    document.getElementById('monsterBtn').setAttribute('aria-pressed',String(on));
    if(on){
      for(const m of MONS){
        const el=document.createElement('img');
        el.src=monsterFiles[m.kind]; el.className='monster'; el.alt=m.kind;
        viewer.addOverlay({element:el,location:pt(...toPx(m.lat,m.lon)),placement:OpenSeadragon.Placement.BOTTOM});
        monsterEls.push({el,m});
      }
      sizeMonsters();
    }else{
      for(const {el} of monsterEls) viewer.removeOverlay(el);
      monsterEls=[];
    }
  }
  function sizeMonsters(){
    const z=vp().getZoom(true)*cw();
    for(const {el,m} of monsterEls){
      el.style.width=(m.wpx*z/W)+'px';
    }
  }
  viewer.addHandler('zoom',()=>{ if(monstersOn) sizeMonsters(); });
  addEventListener('resize',()=>{ if(monstersOn) sizeMonsters(); });
  document.getElementById('monsterBtn').onclick=()=>setMonsters(!monstersOn);

  // teclado
  addEventListener('keydown',(e)=>{
    if(e.target.tagName==='INPUT') { if(e.key==='Escape') sb.hidden=true; return; }
    switch(e.key){
      case 'r': case 'R': randomView(); break;
      case 'h': case 'H': home(); break;
      case 'f': case 'F': document.getElementById('fullBtn').click(); break;
      case '+': document.getElementById('zinBtn').click(); break;
      case '-': document.getElementById('zoutBtn').click(); break;
      case '/': e.preventDefault(); openSearch(); break;
      case 'm': case 'M': setMonsters(!monstersOn); break;
      case 'Escape': sb.hidden=true; break;
    }
  });
})();
