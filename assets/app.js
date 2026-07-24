const $ = selector => document.querySelector(selector);

const els = {
  q: $("#q"),
  scope: $("#scope"),
  area: $("#area"),
  brazil: $("#brazil"),
  download: $("#download"),
  programmatic: $("#programmatic"),
  coverage: $("#coverage"),
  format: $("#format"),
  evidence: $("#evidence"),
  sort: $("#sort"),
  list: $("#list"),
  empty: $("#empty"),
  count: $("#count"),
  activeFilters: $("#active-filters"),
  advancedFilters: $("#advanced-filters"),
  advancedCount: $("#advanced-count"),
  areaLinks: $("#area-links"),
  heroSearch: $("#hero-search"),
  catalogHeading: $("#catalog-heading")
};

let all = [];
let filtered = [];
let scopeRegistry = null;

const SEARCH_FIELDS = [
  "resource_name", "acronym", "official_identity", "description", "research_areas",
  "keywords", "data_product_types", "data_formats", "visualization_types",
  "geographic_coverage", "data_sources", "access_protocols", "access_conditions",
  "license", "owner_or_manager", "academic_uses", "limitations", "academic_evidence_note",
  "_scope_search"
];

const ENUM_ORDER = ["sim", "parcial", "não", "desconhecido", "não se aplica"];
const ENUM_LABELS = {
  "sim": "Sim",
  "parcial": "Parcial",
  "não": "Não",
  "desconhecido": "Desconhecido",
  "não se aplica": "Não se aplica"
};
const IGNORED_FORMATS = new Set(["formatos variados", "varia", "visualização web"]);

const split = value => String(value || "").split("|").map(item => item.trim()).filter(Boolean);
const norm = value => String(value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
const esc = value => String(value || "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[char]));
const validUrl = value => /^https:\/\//.test(String(value || ""));
const formats = resource => [...new Set(split(resource.data_formats).map(value => value.split(";")[0].trim()).filter(value => value && !IGNORED_FORMATS.has(value.toLowerCase())))];
const searchText = resource => norm(SEARCH_FIELDS.map(key => resource[key]).join(" "));
const reducedMotion = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const domId = value => String(value || "resource").replace(/[^a-zA-Z0-9_-]/g, "-");

function buildScopeIndex(registry) {
  const index = new Map();
  registry.tiers.forEach((tier, order) => {
    tier.resource_ids.forEach(resourceId => {
      index.set(resourceId, {
        priority_tier: tier.priority_tier,
        priority_order: order,
        source_origin: tier.source_origin,
        brazil_scope_class: tier.brazil_scope_class,
        display_label: tier.display_label,
        inclusion_role: tier.inclusion_role,
        description: tier.description
      });
    });
  });
  return index;
}

function attachScope(resources, registry) {
  const index = buildScopeIndex(registry);
  return resources.map(resource => {
    const scope = index.get(resource.resource_id);
    if (!scope) throw Error(`Prioridade Brasil ausente para ${resource.resource_id}.`);
    return {
      ...resource,
      _scope: scope,
      _scope_search: `${scope.display_label} ${scope.description} ${scope.source_origin} ${scope.inclusion_role}`
    };
  });
}

function detail(label, value) {
  return `<div class="detail"><strong>${esc(label)}</strong><span>${esc(value || "Não informado")}</span></div>`;
}

function actionLink(label, url, className = "action-secondary") {
  return validUrl(url) ? `<a class="${className}" href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(label)} <span aria-hidden="true">↗</span><span class="sr-only"> (abre em nova aba)</span></a>` : "";
}

function statusClass(value) {
  const key = norm(value);
  if (key === "sim") return "status-yes";
  if (key === "parcial") return "status-partial";
  if (key === "nao") return "status-no";
  if (key === "nao se aplica") return "status-na";
  return "status-unknown";
}

function statusSymbol(value) {
  const key = norm(value);
  if (key === "sim") return "✓";
  if (key === "parcial") return "◐";
  if (key === "nao") return "—";
  if (key === "nao se aplica") return "·";
  return "?";
}

function statusBadge(label, value) {
  const readable = ENUM_LABELS[value] || value || "Desconhecido";
  return `<div class="status-badge ${statusClass(value)}" role="group" aria-label="${esc(label)}: ${esc(readable)}"><span class="status-symbol" aria-hidden="true">${statusSymbol(value)}</span><span><small>${esc(label)}</small><strong>${esc(readable)}</strong></span></div>`;
}

function scopeBadge(resource) {
  const scope = resource._scope;
  return `<span class="scope-badge scope-${esc(scope.priority_tier.toLowerCase())}" title="${esc(scope.description)}">${esc(scope.display_label)}</span>`;
}

function detailGroup(title, content, links = "") {
  return `<section class="detail-group"><h4>${esc(title)}</h4><div class="detail-grid">${content}</div>${links ? `<div class="detail-links">${links}</div>` : ""}</section>`;
}

function countValues(values) {
  return values.filter(Boolean).reduce((counts, value) => {
    counts.set(value, (counts.get(value) || 0) + 1);
    return counts;
  }, new Map());
}

function populateSelect(element, values, emptyLabel, preferredOrder = null, labelMap = {}) {
  const counts = countValues(values);
  const entries = [...counts.entries()];
  entries.sort((a, b) => {
    if (preferredOrder) {
      const ai = preferredOrder.indexOf(a[0]);
      const bi = preferredOrder.indexOf(b[0]);
      if (ai !== -1 || bi !== -1) return (ai === -1 ? 999 : ai) - (bi === -1 ? 999 : bi);
    }
    return a[0].localeCompare(b[0], "pt-BR");
  });

  element.innerHTML = "";
  const empty = new Option(emptyLabel, "");
  empty.dataset.label = emptyLabel;
  element.add(empty);
  entries.forEach(([value, count]) => {
    const label = labelMap[value] || value;
    const option = new Option(`${label} (${count})`, value);
    option.dataset.label = label;
    element.add(option);
  });
}

function optionLabel(element) {
  const option = element.selectedOptions[0];
  return option?.dataset.label || option?.textContent || element.value;
}

function card(resource) {
  const cardId = `resource-${domId(resource.resource_id)}`;
  const descriptionId = `${cardId}-description`;
  const acronym = resource.acronym && resource.acronym !== resource.resource_name ? `<span class="acronym">${esc(resource.acronym)}</span>` : "";
  const areas = split(resource.research_areas);
  const areaChips = areas.map(area => `<span class="chip">${esc(area)}</span>`).join("");

  const accessGroup = detailGroup(
    "Acesso",
    detail("Download gratuito", resource.free_download) +
    detail("Condições de acesso", resource.access_conditions) +
    detail("API ou acesso automatizado", resource.programmatic_access) +
    detail("Protocolos e ferramentas", resource.access_protocols) +
    detail("Autenticação", resource.authentication_required),
    actionLink("Documentação de acesso", resource.access_documentation_url)
  );

  const coverageGroup = detailGroup(
    "Cobertura",
    detail("Prioridade no escopo Brasil", `${resource._scope.priority_tier} — ${resource._scope.display_label}`) +
    detail("Origem da fonte", resource._scope.source_origin) +
    detail("Papel no catálogo", resource._scope.inclusion_role) +
    detail("Cobertura geográfica", resource.geographic_coverage) +
    detail("Dados para o Brasil", resource.covers_brazil) +
    detail("Resolução espacial", resource.spatial_resolution) +
    detail("Cobertura temporal", resource.temporal_coverage) +
    detail("Resolução temporal", resource.temporal_resolution)
  );

  const productsGroup = detailGroup(
    "Produtos e dados",
    detail("Produtos", resource.data_product_types) +
    detail("Formatos", resource.data_formats) +
    detail("Visualizações", resource.visualization_types) +
    detail("Origem dos dados", resource.data_sources)
  );

  const academicGroup = detailGroup(
    "Uso acadêmico",
    detail("Utilidade acadêmica", resource.academic_uses) +
    detail("Áreas de pesquisa", resource.research_areas) +
    detail("Palavras-chave", resource.keywords)
  );

  const evidenceGroup = detailGroup(
    "Evidências",
    detail("Tipo de evidência", resource.academic_evidence_type) +
    detail("Síntese da evidência", resource.academic_evidence_note),
    actionLink("Evidência acadêmica ou técnica", resource.academic_evidence_url) +
    actionLink("Evidência oficial", resource.verification_url)
  );

  const evaluationGroup = detailGroup(
    "Avaliação e governança",
    detail("Limitações", resource.limitations) +
    detail("Responsável", resource.owner_or_manager) +
    detail("Tipo de instituição", resource.institutional_status) +
    detail("Licença", resource.license) +
    detail("Registro revisado em", resource.last_verified) +
    detail("Identificador interno", resource.resource_id)
  );

  return `<article class="card" role="listitem" aria-labelledby="${cardId}" aria-describedby="${descriptionId}">
    <header class="card-header">
      <div class="card-title"><div class="scope-line">${scopeBadge(resource)}</div><div class="title-line"><h3 id="${cardId}">${esc(resource.resource_name)}</h3>${acronym}</div><p class="identity">${esc(resource.official_identity)}</p></div>
      <span class="verified-date">Registro revisado em ${esc(resource.last_verified)}</span>
    </header>
    <p class="description" id="${descriptionId}">${esc(resource.description)}</p>
    <div class="chips" aria-label="Áreas de pesquisa">${areaChips}</div>
    <div class="status-grid" aria-label="Resumo de acesso">
      ${statusBadge("Download gratuito", resource.free_download)}
      ${statusBadge("API ou acesso automatizado", resource.programmatic_access)}
      ${statusBadge("Dados para o Brasil", resource.covers_brazil)}
    </div>
    <div class="card-highlights">
      <div class="highlight academic-use"><span>Mais indicada para</span><p>${esc(resource.academic_uses)}</p></div>
      <div class="highlight limitation"><span>Principal limitação</span><p>${esc(resource.limitations)}</p></div>
    </div>
    <div class="card-actions">
      ${actionLink("Acessar dados", resource.data_access_url, "action-primary")}
      ${actionLink("Site oficial", resource.homepage_url)}
    </div>
    <details class="card-details">
      <summary aria-label="Ver detalhes técnicos, evidências e avaliação de ${esc(resource.resource_name)}">Ver detalhes técnicos, evidências e avaliação</summary>
      <div class="detail-groups">${accessGroup}${coverageGroup}${productsGroup}${academicGroup}${evidenceGroup}${evaluationGroup}</div>
    </details>
  </article>`;
}

function relevanceScore(resource, query) {
  if (!query) return 0;
  const name = norm(resource.resource_name);
  const acronym = norm(resource.acronym);
  let score = 0;
  if (name === query) score += 100;
  if (name.startsWith(query)) score += 50;
  if (name.includes(query)) score += 25;
  if (acronym === query) score += 40;
  if (acronym.includes(query)) score += 15;
  SEARCH_FIELDS.forEach(key => {
    if (norm(resource[key]).includes(query)) score += 1;
  });
  return score;
}

function sortResults(query) {
  const byName = (a, b) => a.resource_name.localeCompare(b.resource_name, "pt-BR");
  const byScope = (a, b) => a._scope.priority_order - b._scope.priority_order;
  if (els.sort.value === "verified") {
    filtered.sort((a, b) => String(b.last_verified).localeCompare(String(a.last_verified)) || byScope(a, b) || byName(a, b));
  } else if (els.sort.value === "name") {
    filtered.sort(byName);
  } else if (els.sort.value === "relevance" && query) {
    filtered.sort((a, b) => relevanceScore(b, query) - relevanceScore(a, query) || byScope(a, b) || byName(a, b));
  } else {
    filtered.sort((a, b) => byScope(a, b) || (query ? relevanceScore(b, query) - relevanceScore(a, query) : 0) || byName(a, b));
  }
}

function render() {
  els.list.setAttribute("aria-busy", "true");
  els.list.innerHTML = filtered.map(card).join("");
  els.empty.hidden = filtered.length > 0;
  const coreCount = filtered.filter(resource => resource._scope.priority_tier === "P0").length;
  els.count.textContent = `${filtered.length} ${filtered.length === 1 ? "fonte encontrada" : "fontes encontradas"} · ${coreCount} ${coreCount === 1 ? "fonte brasileira" : "fontes brasileiras"} · ${all.length} no catálogo`;
  els.list.setAttribute("aria-busy", "false");
}

function renderActiveFilters() {
  const items = [];
  if (els.q.value.trim()) items.push({key: "q", label: `Busca: ${els.q.value.trim()}`});

  [
    ["scope", "Escopo", els.scope],
    ["area", "Área", els.area],
    ["brazil", "Brasil", els.brazil],
    ["download", "Download", els.download],
    ["programmatic", "API", els.programmatic],
    ["coverage", "Cobertura", els.coverage],
    ["format", "Formato", els.format],
    ["evidence", "Evidência", els.evidence]
  ].forEach(([key, label, element]) => {
    if (element.value) items.push({key, label: `${label}: ${optionLabel(element)}`});
  });

  const advancedActive = [els.coverage, els.format, els.evidence].filter(element => element.value).length;
  els.advancedCount.textContent = advancedActive ? `(${advancedActive} ${advancedActive === 1 ? "ativo" : "ativos"})` : "";
  if (advancedActive) els.advancedFilters.open = true;

  document.querySelectorAll("[data-area]").forEach(button => {
    const active = button.dataset.area === els.area.value;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  document.querySelectorAll("[data-scope]").forEach(button => {
    const active = button.dataset.scope === els.scope.value;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-pressed", String(active));
  });

  els.activeFilters.hidden = items.length === 0;
  els.activeFilters.innerHTML = items.length ? `<span>Filtros ativos:</span>${items.map(item => `<button type="button" data-remove="${item.key}" aria-label="Remover ${esc(item.label)}">${esc(item.label)} <b aria-hidden="true">×</b></button>`).join("")}` : "";
  els.activeFilters.querySelectorAll("[data-remove]").forEach(button => button.addEventListener("click", () => {
    const key = button.dataset.remove;
    const target = key === "q" ? els.q : els[key];
    target.value = "";
    filter();
    target.focus();
  }));
}

function writeUrl() {
  const params = new URLSearchParams();
  const values = {
    q: els.q.value.trim(),
    scope: els.scope.value,
    area: els.area.value,
    brazil: els.brazil.value,
    download: els.download.value,
    api: els.programmatic.value,
    coverage: els.coverage.value,
    format: els.format.value,
    evidence: els.evidence.value,
    sort: els.sort.value === "brazil" ? "" : els.sort.value
  };
  Object.entries(values).forEach(([key, value]) => { if (value) params.set(key, value); });
  const query = params.toString();
  history.replaceState(null, "", `${location.pathname}${query ? `?${query}` : ""}${location.hash}`);
}

function setSelectFromParam(element, value) {
  if (!value) return;
  const valid = [...element.options].some(option => option.value === value);
  if (valid) element.value = value;
}

function readUrl() {
  const params = new URLSearchParams(location.search);
  els.q.value = params.get("q") || "";
  setSelectFromParam(els.scope, params.get("scope"));
  setSelectFromParam(els.area, params.get("area"));
  setSelectFromParam(els.brazil, params.get("brazil"));
  setSelectFromParam(els.download, params.get("download"));
  setSelectFromParam(els.programmatic, params.get("api"));
  setSelectFromParam(els.coverage, params.get("coverage"));
  setSelectFromParam(els.format, params.get("format"));
  setSelectFromParam(els.evidence, params.get("evidence"));
  setSelectFromParam(els.sort, params.get("sort"));
}

function filter(syncUrl = true) {
  const query = norm(els.q.value.trim());
  filtered = all.filter(resource =>
    (!query || searchText(resource).includes(query)) &&
    (!els.scope.value || resource._scope.brazil_scope_class === els.scope.value) &&
    (!els.area.value || split(resource.research_areas).includes(els.area.value)) &&
    (!els.brazil.value || resource.covers_brazil === els.brazil.value) &&
    (!els.download.value || resource.free_download === els.download.value) &&
    (!els.programmatic.value || resource.programmatic_access === els.programmatic.value) &&
    (!els.coverage.value || resource.geographic_coverage === els.coverage.value) &&
    (!els.format.value || formats(resource).includes(els.format.value)) &&
    (!els.evidence.value || resource.academic_evidence_type === els.evidence.value)
  );
  sortResults(query);
  render();
  renderActiveFilters();
  if (syncUrl) writeUrl();
}

function goToCatalog() {
  els.catalogHeading.scrollIntoView({behavior: reducedMotion() ? "auto" : "smooth", block: "start"});
  els.catalogHeading.focus({preventScroll: true});
}

function setQuery(value) {
  els.q.value = value;
  filter();
  goToCatalog();
}

function setScope(value) {
  els.scope.value = value;
  filter();
  goToCatalog();
}

function renderAreas() {
  const counts = countValues(all.flatMap(resource => split(resource.research_areas)));
  els.areaLinks.innerHTML = [...counts.entries()]
    .sort((a, b) => a[0].localeCompare(b[0], "pt-BR"))
    .map(([area, count]) => `<button class="area-card" type="button" data-area="${esc(area)}" aria-pressed="false"><strong>${esc(area)}</strong><span>${count} ${count === 1 ? "fonte" : "fontes"}</span></button>`)
    .join("");
  els.areaLinks.setAttribute("aria-busy", "false");

  els.areaLinks.querySelectorAll("[data-area]").forEach(button => button.addEventListener("click", () => {
    els.area.value = button.dataset.area;
    filter();
    goToCatalog();
  }));
}

function populateFilters() {
  const scopeOrder = scopeRegistry.tiers.map(tier => tier.brazil_scope_class);
  const scopeLabels = Object.fromEntries(scopeRegistry.tiers.map(tier => [tier.brazil_scope_class, `${tier.priority_tier} — ${tier.display_label}`]));
  populateSelect(els.scope, all.map(resource => resource._scope.brazil_scope_class), "Todas as prioridades", scopeOrder, scopeLabels);
  populateSelect(els.area, all.flatMap(resource => split(resource.research_areas)), "Todas as áreas");
  populateSelect(els.brazil, all.map(resource => resource.covers_brazil), "Qualquer situação", ENUM_ORDER, ENUM_LABELS);
  populateSelect(els.download, all.map(resource => resource.free_download), "Qualquer situação", ENUM_ORDER, ENUM_LABELS);
  populateSelect(els.programmatic, all.map(resource => resource.programmatic_access), "Qualquer situação", ENUM_ORDER, ENUM_LABELS);
  populateSelect(els.coverage, all.map(resource => resource.geographic_coverage), "Todas as coberturas");
  populateSelect(els.format, all.flatMap(formats), "Todos os formatos");
  populateSelect(els.evidence, all.map(resource => resource.academic_evidence_type), "Todos os tipos");
}

async function init() {
  try {
    const [resourcesResponse, scopeResponse] = await Promise.all([
      fetch("data/data_resources.json"),
      fetch("data/brazil_scope_priorities.json")
    ]);
    if (!resourcesResponse.ok) throw Error("Não foi possível carregar os dados.");
    if (!scopeResponse.ok) throw Error("Não foi possível carregar a política de prioridade Brasil.");

    scopeRegistry = await scopeResponse.json();
    all = attachScope(await resourcesResponse.json(), scopeRegistry);
    populateFilters();
    renderAreas();
    readUrl();

    [els.q, els.scope, els.area, els.brazil, els.download, els.programmatic, els.coverage, els.format, els.evidence, els.sort].forEach(element => element.addEventListener(element === els.q ? "input" : "change", () => filter()));
    els.heroSearch.addEventListener("submit", event => { event.preventDefault(); filter(); goToCatalog(); });
    document.querySelectorAll("[data-query]").forEach(button => button.addEventListener("click", () => setQuery(button.dataset.query)));
    document.querySelectorAll("[data-scope]").forEach(button => button.addEventListener("click", () => setScope(button.dataset.scope)));
    $("#clear").addEventListener("click", () => {
      $("#filters").reset();
      els.q.value = "";
      els.sort.value = "brazil";
      els.advancedFilters.open = false;
      filter();
      els.q.focus();
    });
    window.addEventListener("popstate", () => { readUrl(); filter(false); });

    $("#n-total").textContent = all.length;
    $("#n-brazilian").textContent = all.filter(resource => resource._scope.priority_tier === "P0").length;
    $("#n-intl-br").textContent = all.filter(resource => resource._scope.priority_tier === "P1").length;
    $("#n-secondary").textContent = all.filter(resource => ["P2", "P3"].includes(resource._scope.priority_tier)).length;
    $("#updated").textContent = all.map(resource => resource.last_verified).filter(Boolean).sort().at(-1) || "não informada";
    filter(false);
  } catch (error) {
    els.areaLinks.setAttribute("aria-busy", "false");
    els.list.setAttribute("aria-busy", "false");
    els.count.textContent = "Falha ao carregar o catálogo";
    els.list.innerHTML = `<div class="empty"><h3>Falha ao carregar o catálogo</h3><p>${esc(error.message)}</p></div>`;
  }
}

init();
