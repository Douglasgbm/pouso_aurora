// Verifica JavaScript com DOM simulado; não renderiza nem valida CSS.
// Executar: node tools/verificar_painel.cjs
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const repo=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(repo,'painel/index.html'),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
class Element {
 constructor(){this.dataset={};this.style={};this.textContent='Painel';this.events={};this.children=[];this.offsetWidth=272;this.offsetHeight=150;this.clientWidth=350;this.attrs={};const set=new Set();this.classList={contains:k=>set.has(k),add:k=>set.add(k),remove:k=>set.delete(k),toggle:(k,v)=>v?set.add(k):set.delete(k)};}
 append(...a){this.children.push(...a)} replaceChildren(...a){this.children=a} setAttribute(k,v){this.attrs[k]=v} addEventListener(k,f){this.events[k]=f} blur(){} getContext(){return new Proxy({},{get:(t,k)=>k==='measureText'?()=>({width:20}):k.startsWith('create')?()=>({addColorStop(){}}):()=>{}})}
}
for(const compact of [false,true]){
 const els={};for(const m of html.matchAll(/id="([^"]+)"/g))els[m[1]]=new Element();
 const body=new Element(),media={matches:compact,addEventListener(k,f){this.change=f}};
 const ctx={console,URLSearchParams,location:{search:'?t=0'},document:{body,getElementById:id=>els[id],createElement:()=>new Element(),createElementNS:()=>new Element(),addEventListener(){}},requestAnimationFrame:()=>1,innerWidth:compact?390:1440,innerHeight:900,devicePixelRatio:1,matchMedia:()=>media,addEventListener(){}};ctx.window=ctx;
 vm.createContext(ctx);vm.runInContext(fs.readFileSync(path.join(repo,'painel/dados.js'),'utf8'),ctx);vm.runInContext(script,ctx);
 assert.equal(body.classList.contains('leitura'),compact);
 const result=vm.runInContext('window.MISSOES.map(m=>{escolher(m.nome,0);for(const c of roteiro.cenas) irPara(c.inicio);return conferirFinal(m,roteiro)})',ctx);assert(result.every(x=>x==='ok'));
 els['modo-leitura'].events.click();assert.equal(body.classList.contains('leitura'),!compact);
 els['modo-leitura'].events.click();assert.equal(body.classList.contains('leitura'),compact);
 media.change({matches:false});els['t-fila'].events.keydown({key:'Enter',preventDefault(){}});assert(els['t-fila'].classList.contains('aberta'));
 media.change({matches:true});assert(!els['t-fila'].classList.contains('aberta'));
 els['b-inicio'].events.click();els['b-passo'].events.click();
 assert(!Object.values(els).some(e=>String(e.style.transform).includes('NaN')));
 console.log({compact,scenarios:result.length,result:'OK',coverage:'JavaScript com DOM simulado; não valida renderização CSS'});
}
