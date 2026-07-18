const $=s=>document.querySelector(s);
const split=v=>String(v||"").split("|").map(x=>x.trim()).filter(Boolean);
const esc=v=>String(v||"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));
const countValues=values=>values.filter(Boolean).reduce((acc,v)=>(acc[v]=(acc[v]||0)+1,acc),{});
const sorted=obj=>Object.entries(obj).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0],"pt-BR"));
function bars(target,entries){const max=Math.max(1,...entries.map(([,n])=>n));$(target).innerHTML=`<div class="bars">${entries.map(([label,n])=>`<div class="bar-row"><div class="bar-label"><span>${esc(label)}</span><strong>${n}</strong></div><div class="bar-track" aria-label="${esc(label)}: ${n}"><span style="width:${(n/max)*100}%"></span></div></div>`).join("")}</div>`}
async function init(){try{const res=await fetch("data/data_resources.json");if(!res.ok)throw Error("Falha ao carregar os dados.");const all=await res.json();
const peer=all.filter(r=>r.academic_evidence_type==="artigo revisado por pares").length;
$("#summary").innerHTML=[["Fontes",all.length],["Áreas",new Set(all.flatMap(r=>split(r.research_areas))).size],["Download gratuito",all.filter(r=>r.free_download==="sim").length],["Acesso programático",all.filter(r=>r.programmatic_access==="sim").length],["Com dados do Brasil",all.filter(r=>["sim","parcial"].includes(r.covers_brazil)).length],["Com artigo revisado por pares",peer]].map(([k,v])=>`<div><strong>${v}</strong><span>${k}</span></div>`).join("");
bars("#chart-areas",sorted(countValues(all.flatMap(r=>split(r.research_areas)))));
bars("#chart-download",sorted(countValues(all.map(r=>r.free_download))));
bars("#chart-programmatic",sorted(countValues(all.map(r=>r.programmatic_access))));
bars("#chart-brazil",sorted(countValues(all.map(r=>r.covers_brazil))));
bars("#chart-evidence",sorted(countValues(all.map(r=>r.academic_evidence_type))));
const ignored=new Set(["formatos variados","varia","visualização web"]);
const formats=all.flatMap(r=>split(r.data_formats).map(x=>x.split(";")[0].trim())).filter(x=>x&&!ignored.has(x.toLowerCase()));
bars("#chart-formats",sorted(countValues(formats)).slice(0,14));
bars("#chart-visualizations",sorted(countValues(all.flatMap(r=>split(r.visualization_types)))));
}catch(e){$("#analise").innerHTML=`<div class="empty"><h2>Falha ao carregar a análise</h2><p>${esc(e.message)}</p></div>`}}
init();
