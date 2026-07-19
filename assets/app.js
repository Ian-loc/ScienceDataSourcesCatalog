const $ = selector => document.querySelector(selector);

const els = {
  q: $("#q"),
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
  heroSearch: $("#hero-search")
};

let all = [];
let filtered = [];

const SEARCH_FIELDS = [
  "resource_name", "acronym", "official_identity", "description", "research_areas",
  "keywords", "data_product_types", "data_formats", "visualization_types",
  "geographic_coverage", "data_sources", "access_protocols", "access_conditions",
  "license", "owner_or_manager", "academic_uses", "limitations", "academic_evidence_note"
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
const detail = (label, value) => `<div class="detail"><strong>${label}</strong><span>${esc(value || "Não informado")}</span></div>`;
const link = (label, url) => url && /^https:\/\//.test(url) ? `<a class="source" href="${esc(url)}" target="_blank" rel="noopener">${label} ↗</a>` : "";
const formats = resource => [...new Set(split(resource.data_formats).map(value => value.split(";")[0].trim()).filter(value => value && !IGNORED_FORMATS.has(value.toLowerCase())))];
const searchText = resource => norm(SEARCH_FIELDS.map(key => resource[key]).join(" "));

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
  const acronym = resource.acronym && resource.acronym !== resource.resource_name ? `<span class="acronym"> · ${esc(resource.acronym)}</span>` : "";
  return `<article class="card">
    <div class="top"><h3>${esc(resource.resource_name)}${acronym}</h3><span class="tag">${esc(resource.official_identity)}</span></div>
    <p class="description">${esc(resource.description)}</p>
    <div class="chips">${split(resource.research_areas).map(area => `<span class="chip">${esc(area)}</span>`).join("")}</div>
    <div class="access"><span>Download gratuito: <b>${esc(resource.free_download)}</b></span><span>API ou acesso automatizado: <b>${esc(resource.programmatic_access)}</b></span><span>Dados para o Brasil: <b>${esc(resource.covers_brazil)}</b></span></div>
    <details><summary>Ver detalhes, evidências e limitações</summary>
      <div class="details">
        ${detail("Palavras-chave", resource.keywords)}
        ${detail("Produtos", resource.data_product_types)}
        ${detail("Formatos", resource.data_formats)}
        ${detail("Visualizações", resource.visualization_types)}
        ${detail("Protocolos e ferramentas", resource.access_protocols)}
        ${detail("Autenticação", resource.authentication_required)}
        ${detail("Resolução espacial", resource.spatial_resolution)}
        ${detail("Cobertura temporal", resource.temporal_coverage)}
        ${detail("Resolução temporal", resource.temporal_resolution)}
        ${detail("Origem dos dados", resource.data_sources)}
        ${detail("Condições de acesso", resource.access_conditions)}
        ${detail("Licença", resource.license)}
        ${detail("Responsável", resource.owner_or_manager)}
        ${detail("Tipo de instituição", resource.institutional_status)}
        ${detail("Utilidade acadêmica", resource.academic_uses)}
        ${detail("Limitações", resource.limitations)}
        ${detail("Tipo de evidência acadêmica", resource.academic_evidence_type)}
        ${detail("Síntese da evidência", resource.academic_evidence_note)}
        ${detail("Verificado em", resource.last_verified)}
      </div>
      <div class="source-links">
        ${link("Acessar dados", resource.data_access_url)}
        ${link("Página oficial", resource.homepage_url)}
        ${link("Documentação de acesso", resource.access_documentation_url)}
        ${link("Evidência acadêmica ou técnica", resource.academic_evidence_url)}
        ${link("Evidência oficial", resource.verification_url)}
      </div>
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
  if (els.sort.value === "verified") {
    filtered.sort((a, b) => String(b.last_verified).localeCompare(String(a.last_verified)) || byName(a, b));
  } else if (els.sort.value === "name" || !query) {
    filtered.sort(byName);
  } else {
    filtered.sort((a, b) => relevanceScore(b, query) - relevanceScore(a, query) || byName(a, b));
  }
}

function render() {
  els.list.innerHTML = filtered.map(card).join("");
  els.empty.hidden = filtered.length > 0;
  els.count.textContent = `${filtered.length} ${filtered.length === 1 ? "fonte encontrada" : "fontes encontradas"} · ${all.length} no catálogo`;
}

function renderActiveFilters() {
  const items = [];
  if (els.q.value.trim()) items.push({key: "q", label: `Busca: ${els.q.value.trim()}`});

  [
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

  els.activeFilters.hidden = items.length === 0;
  els.activeFilters.innerHTML = items.length ? `<span>Filtros ativos:</span>${items.map(item => `<button type="button" data-remove="${item.key}" aria-label="Remover ${esc(item.label)}">${esc(item.label)} <b aria-hidden="true">×</b></button>`).join("")}` : "";
  els.activeFilters.querySelectorAll("[data-remove]").forEach(button => button.addEventListener("click", () => {
    const key = button.dataset.remove;
    if (key === "q") els.q.value = "";
    else els[key].value = "";
    filter();
  }));
}

function writeUrl() {
  const params = new URLSearchParams();
  const values = {
    q: els.q.value.trim(),
    area: els.area.value,
    brazil: els.brazil.value,
    download: els.download.value,
    api: els.programmatic.value,
    coverage: els.coverage.value,
    format: els.format.value,
    evidence: els.evidence.value,
    sort: els.sort.value === "relevance" ? "" : els.sort.value
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
  $("#catalogo").scrollIntoView({behavior: "smooth", block: "start"});
}

function setQuery(value) {
  els.q.value = value;
  filter();
  goToCatalog();
}

function renderAreas() {
  const counts = countValues(all.flatMap(resource => split(resource.research_areas)));
  els.areaLinks.innerHTML = [...counts.entries()]
    .sort((a, b) => a[0].localeCompare(b[0], "pt-BR"))
    .map(([area, count]) => `<button class="area-card" type="button" data-area="${esc(area)}" aria-pressed="false"><strong>${esc(area)}</strong><span>${count} ${count === 1 ? "fonte" : "fontes"}</span></button>`)
    .join("");

  els.areaLinks.querySelectorAll("[data-area]").forEach(button => button.addEventListener("click", () => {
    els.area.value = button.dataset.area;
    filter();
    goToCatalog();
  }));
}

function populateFilters() {
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
    const response = await fetch("data/data_resources.json");
    if (!response.ok) throw Error("Não foi possível carregar os dados.");

    all = await response.json();
    populateFilters();
    renderAreas();
    readUrl();

    [els.q, els.area, els.brazil, els.download, els.programmatic, els.coverage, els.format, els.evidence, els.sort].forEach(element => element.addEventListener(element === els.q ? "input" : "change", () => filter()));
    els.heroSearch.addEventListener("submit", event => { event.preventDefault(); filter(); goToCatalog(); });
    document.querySelectorAll("[data-query]").forEach(button => button.addEventListener("click", () => setQuery(button.dataset.query)));
    $("#clear").addEventListener("click", () => {
      $("#filters").reset();
      els.q.value = "";
      els.sort.value = "relevance";
      els.advancedFilters.open = false;
      filter();
      els.q.focus();
    });
    window.addEventListener("popstate", () => { readUrl(); filter(false); });

    $("#n-total").textContent = all.length;
    $("#n-free").textContent = all.filter(resource => resource.free_download === "sim").length;
    $("#n-api").textContent = all.filter(resource => resource.programmatic_access === "sim").length;
    $("#n-br").textContent = all.filter(resource => ["sim", "parcial"].includes(resource.covers_brazil)).length;
    $("#updated").textContent = all.map(resource => resource.last_verified).filter(Boolean).sort().at(-1) || "não informada";
    filter(false);
  } catch (error) {
    els.list.innerHTML = `<div class="empty"><h3>Falha ao carregar o catálogo</h3><p>${esc(error.message)}</p></div>`;
  }
}

init();
