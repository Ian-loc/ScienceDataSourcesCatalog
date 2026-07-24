const qualityTarget = id => document.getElementById(id);
const qualityNorm = value => String(value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();

async function loadQualitySummary() {
  const targets = {
    official: qualityTarget("q-official-docs"),
    peer: qualityTarget("q-peer-reviewed"),
    access: qualityTarget("q-access-uncertain"),
    license: qualityTarget("q-license-uncertain"),
    links: qualityTarget("q-link-role-pending")
  };
  if (Object.values(targets).some(target => !target)) return;

  try {
    const response = await fetch("data/data_resources.json");
    if (!response.ok) throw Error("Falha ao carregar indicadores de qualidade.");
    const resources = await response.json();

    targets.official.textContent = resources.filter(resource => /^https:\/\//.test(resource.verification_url || "")).length;
    targets.peer.textContent = resources.filter(resource => resource.academic_evidence_type === "artigo revisado por pares").length;
    targets.access.textContent = resources.filter(resource => {
      const combined = qualityNorm(`${resource.access_conditions} ${resource.authentication_required} ${resource.programmatic_access}`);
      return combined.includes("desconhecido") || combined.includes("varia") || combined.includes("parcial") || combined.includes("restrito");
    }).length;
    targets.license.textContent = resources.filter(resource => {
      const license = qualityNorm(resource.license);
      return !license || license.includes("nao localizada") || license.includes("varia") || license.includes("consultar") || license.includes("especifica");
    }).length;
    targets.links.textContent = resources.filter(resource => resource.homepage_url && resource.homepage_url === resource.data_access_url).length;
  } catch (error) {
    Object.values(targets).forEach(target => { target.textContent = "?"; });
  }
}

loadQualitySummary();
