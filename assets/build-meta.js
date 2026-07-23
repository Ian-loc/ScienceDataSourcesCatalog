async function renderBuildMeta(){
  const targets=[...document.querySelectorAll("[data-build-meta]")];
  try{
    const response=await fetch("data/build-meta.json",{cache:"no-store"});
    if(!response.ok)throw new Error("metadados indisponíveis");
    const meta=await response.json();
    const commit=String(meta.commit||"desconhecido");
    const shortCommit=commit==="local"?commit:commit.slice(0,12);
    const productPart=Number.isInteger(meta.products)?` · ${meta.products} produtos`:"";
    const label=`v${meta.version||"?"} · ${shortCommit} · ${meta.records||"?"} fontes × ${meta.fields||"?"} campos${productPart}`;
    targets.forEach(target=>target.textContent=label);

    const quality=meta.quality||{};
    const values={
      "q-official-docs":quality.official_documentation_records,
      "q-peer-reviewed":quality.peer_reviewed_evidence_records,
      "q-access-uncertain":quality.access_uncertainty_records,
      "q-license-uncertain":quality.license_uncertainty_records,
      "q-link-role-pending":quality.link_role_pending_records
    };
    Object.entries(values).forEach(([id,value])=>{
      const target=document.getElementById(id);
      if(target)target.textContent=Number.isInteger(value)?String(value):"—";
    });
  }catch(error){
    targets.forEach(target=>target.textContent="versão não identificada");
    ["q-official-docs","q-peer-reviewed","q-access-uncertain","q-license-uncertain","q-link-role-pending"].forEach(id=>{
      const target=document.getElementById(id);
      if(target)target.textContent="—";
    });
  }
}
renderBuildMeta();
