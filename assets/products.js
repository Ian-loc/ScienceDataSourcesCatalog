const $ = selector => document.querySelector(selector);

const els = {
  q: $("#product-q"),
  source: $("#product-source"),
  area: $("#product-area"),
  brazil: $("#product-brazil"),
  kind: $("#product-kind"),
  format: $("#product-format"),
  protocol: $("#product-protocol"),
  auth: $("#product-auth"),
  status: $("#product-status"),
  origin: $("#product-origin"),
  sort: $("#product-sort"),
  list: $("#product-list"),
  empty: $("#product-empty"),
  count: $("#product-count"),
  activeFilters: $("#product-active-filters"),
  advancedFilters: $("#product-advanced-filters"),
  advancedCount: $("#product-advanced-count"),
  searchForm: $("#product-search"),
  catalogHeading: $("#product-catalog-heading"),
  compareBar: $("#compare-bar"),
  compareCount: $("#compare-count"),
  compareStatus: $("#compare-status"),
  compareDialog: $("#compare-dialog"),
  compareContent: $("#compare-content")
};

let all = [];
let filtered = [];
const selected = new Set();

const ENUM_ORDER = ["sim", "parcial", "não", "desconhecido", "não se aplica"];
const ENUM_LABELS = {
  "sim": "Sim",
  "parcial": "Parcial",
  "não": "Não",
  "desconhecido": "Desconhecido",
  "não se aplica": "Não se aplica"
};
const KIND_LABELS = {
  dataset: "Dataset",
  dataset_series: "Série de datasets",
  data_service: "Serviço de dados",
  catalog: "Catálogo",
  federated_catalog: "Catálogo federado"
};
const ORIGIN_LABELS = {
  primário: "Primário",
  derivado: "Derivado",
  agregador: "Agregador",
  serviço: "Serviço"
};
const SYNONYM_GROUPS = [
  ["biomassa", "biomass", "agb", "aboveground biomass"],
  ["desmatamento", "deforestation", "forest loss", "supressão de vegetação"],
  ["precipitação", "precipitation", "rainfall", "chuva"],
  ["uso da terra", "land use", "cobertura da terra", "land cover", "lulc"],
  ["fogo", "fire", "burned area", "área queimada", "hotspot", "foco de calor"],
  ["alerta", "alertas", "warning", "warnings"],
  ["vegetação secundária", "secondary vegetation", "regrowth", "regeneração"],
  ["sensoriamento remoto", "remote sensing", "satélite", "satellite"],
  ["vetor", "vector", "shapefile"],
  ["raster", "geotiff", "imagem"]
];

const split = value => String(value || "").split("|").map(item => item.trim()).filter(Boolean);
const norm = value => String(value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
const esc = value => String(value || "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[char]));
const validUrl = value => /^https:\/\//.test(String(value || ""));
const unique = values => [...new Set(values.filter(Boolean))];
const reducedMotion = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const domId = value => String(value || "product").replace(/[^a-zA-Z0-9_-]/g, "-");

function productFormats(product) {
  return unique(product.distributions.flatMap(distribution => split(distribution.format)));
}

function productProtocols(product) {
  return unique(product.distributions.map(distribution => distribution.access_protocol));
}

function aggregateEnum(values) {
  const clean = values.filter(Boolean);
  if (clean.includes("sim")) return "sim";
  if (clean.includes("parcial")) return "parcial";
  if (clean.length && clean.every(value => value === "não")) return "não";
  if (clean.includes("desconhecido")) return "desconhecido";
  return clean[0] || "desconhecido";
}

function searchableText(product) {
  const base = norm([
    product.product_name, product.product_acronym, product.product_family,
    product.product_kind, product.product_description, product.research_areas,
    product.keywords, product.geographic_coverage, product.spatial_support,
    product.spatial_resolution, product.temporal_coverage, product.temporal_resolution,
    product.update_frequency, product.product_status, product.version_or_collection,
    product.primary_or_derived, product.limitations,
    product.source.resource_name, product.source.acronym, product.source.official_identity,
    ...product.distributions.flatMap(distribution => [
      distribution.distribution_name, distribution.format, distribution.access_protocol,
      distribution.access_tool, distribution.access_conditions, distribution.license,
      distribution.subset_support, distribution.notes
    ])
  ].join(" "));
  const expansions = SYNONYM_GROUPS
    .map(group => group.map(norm))
    .filter(group => group.some(term => base.includes(term)))
    .flat();
  return `${base} ${expansions.join(" ")}`;
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

function distributionCard(distribution) {
  return `<article class="distribution">
    <header><h5>${esc(distribution.distribution_name)}</h5>${actionLink("Abrir acesso", distribution.access_url)}</header>
    <div class="distribution-grid">
      ${detail("Formato", distribution.format)}
      ${detail("Protocolo", distribution.access_protocol)}
      ${detail("Ferramenta", distribution.access_tool)}
      ${detail("Download gratuito", distribution.free_download)}
      ${detail("Autenticação", distribution.authentication_required)}
      ${detail("Recorte", distribution.subset_support)}
      ${detail("Licença", distribution.license)}
      ${detail("Condições", distribution.access_conditions)}
    </div>
    <p>${esc(distribution.notes)}</p>
  </article>`;
}

function productCard(product) {
  const cardId = `product-${domId(product.product_id)}`;
  const descriptionId = `${cardId}-description`;
  const areas = split(product.research_areas);
  const formats = productFormats(product);
  const free = aggregateEnum(product.distributions.map(item => item.free_download));
  const auth = aggregateEnum(product.distributions.map(item => item.authentication_required));
  const checked = selected.has(product.product_id) ? " checked" : "";
  const acronym = product.product_acronym ? `<span class="acronym">${esc(product.product_acronym)}</span>` : "";

  return `<article class="card product-card" role="listitem" aria-labelledby="${cardId}" aria-describedby="${descriptionId}">
    <header class="card-header">
      <div class="card-title">
        <p class="product-source"><a href="index.html?q=${encodeURIComponent(product.source.resource_name)}#catalogo">${esc(product.source.resource_name)}</a></p>
        <div class="title-line"><h3 id="${cardId}">${esc(product.product_name)}</h3>${acronym}</div>
        <p class="identity">${esc(product.product_family)} · ${esc(KIND_LABELS[product.product_kind] || product.product_kind)}</p>
      </div>
      <span class="verified-date">Verificado em ${esc(product.last_verified)}</span>
    </header>
    <p class="description" id="${descriptionId}">${esc(product.product_description)}</p>
    <div class="chips" aria-label="Áreas de pesquisa">${areas.map(area => `<span class="chip">${esc(area)}</span>`).join("")}</div>
    <div class="status-grid" aria-label="Resumo do produto">
      ${statusBadge("Dados para o Brasil", product.covers_brazil)}
      ${statusBadge("Algum download gratuito", free)}
      ${statusBadge("Alguma rota exige autenticação", auth)}
    </div>
    <div class="product-meta-grid">
      ${detail("Suporte espacial", product.spatial_support)}
      ${detail("Resolução espacial", product.spatial_resolution)}
      ${detail("Resolução temporal", product.temporal_resolution)}
      ${detail("Versão ou coleção", product.version_or_collection)}
    </div>
    <div class="highlight limitation product-limitation"><span>Principal limitação</span><p>${esc(product.limitations)}</p></div>
    <div class="chips product-format-chips" aria-label="Formatos e modalidades">${formats.map(format => `<span class="chip">${esc(format)}</span>`).join("")}</div>
    <div class="card-actions">
      ${actionLink("Página do produto", product.product_page_url, "action-primary")}
      ${actionLink("Metodologia", product.methodology_url)}
    </div>
    <label class="compare-toggle"><input type="checkbox" data-compare="${esc(product.product_id)}"${checked}><span>Selecionar para comparar</span></label>
    <details class="card-details">
      <summary aria-label="Ver detalhes e formas de acesso de ${esc(product.product_name)}">Ver detalhes e formas de acesso (${product.distributions.length})</summary>
      <div class="detail-groups">
        <section class="detail-group"><h4>Produto</h4><div class="detail-grid">
          ${detail("Cobertura geográfica", product.geographic_coverage)}
          ${detail("Cobertura temporal", product.temporal_coverage)}
          ${detail("Atualização", product.update_frequency)}
          ${detail("Estado", product.product_status)}
          ${detail("Origem", ORIGIN_LABELS[product.primary_or_derived] || product.primary_or_derived)}
          ${detail("Escopo de enumeração", product.enumeration_scope)}
          ${detail("Palavras-chave", product.keywords)}
          ${detail("Identificador", product.product_id)}
        </div></section>
        <section class="detail-group"><h4>Distribuições e acesso</h4><div class="product-distributions">${product.distributions.map(distributionCard).join("")}</div></section>
      </div>
    </details>
  </article>`;
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

function relevanceScore(product, query) {
  if (!query) return 0;
  const name = norm(product.product_name);
  const acronym = norm(product.product_acronym);
  let score = 0;
  if (name === query) score += 100;
  if (name.startsWith(query)) score += 50;
  if (name.includes(query)) score += 25;
  if (acronym === query) score += 40;
  if (acronym.includes(query)) score += 15;
  if (product._search.includes(query)) score += 5;
  return score;
}

function sortResults(query) {
  const byName = (a, b) => a.product_name.localeCompare(b.product_name, "pt-BR");
  if (els.sort.value === "verified") {
    filtered.sort((a, b) => String(b.last_verified).localeCompare(String(a.last_verified)) || byName(a, b));
  } else if (els.sort.value === "source") {
    filtered.sort((a, b) => a.source.resource_name.localeCompare(b.source.resource_name, "pt-BR") || byName(a, b));
  } else if (els.sort.value === "name" || !query) {
    filtered.sort(byName);
  } else {
    filtered.sort((a, b) => relevanceScore(b, query) - relevanceScore(a, query) || byName(a, b));
  }
}

function render() {
  els.list.setAttribute("aria-busy", "true");
  els.list.innerHTML = filtered.map(productCard).join("");
  els.empty.hidden = filtered.length > 0;
  els.count.textContent = `${filtered.length} ${filtered.length === 1 ? "produto encontrado" : "produtos encontrados"} · ${all.length} no piloto`;
  els.list.setAttribute("aria-busy", "false");
  els.list.querySelectorAll("[data-compare]").forEach(input => input.addEventListener("change", handleCompareChange));
}

function renderActiveFilters() {
  const items = [];
  if (els.q.value.trim()) items.push({key: "q", label: `Busca: ${els.q.value.trim()}`});
  [
    ["source", "Fonte", els.source],
    ["area", "Área", els.area],
    ["brazil", "Brasil", els.brazil],
    ["kind", "Tipo", els.kind],
    ["format", "Formato", els.format],
    ["protocol", "Protocolo", els.protocol],
    ["auth", "Autenticação", els.auth],
    ["status", "Estado", els.status],
    ["origin", "Origem", els.origin]
  ].forEach(([key, label, element]) => {
    if (element.value) items.push({key, label: `${label}: ${optionLabel(element)}`});
  });

  const advancedActive = [els.format, els.protocol, els.auth, els.status, els.origin].filter(element => element.value).length;
  els.advancedCount.textContent = advancedActive ? `(${advancedActive} ${advancedActive === 1 ? "ativo" : "ativos"})` : "";
  if (advancedActive) els.advancedFilters.open = true;

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
    source: els.source.value,
    area: els.area.value,
    brazil: els.brazil.value,
    kind: els.kind.value,
    format: els.format.value,
    protocol: els.protocol.value,
    auth: els.auth.value,
    status: els.status.value,
    origin: els.origin.value,
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
  setSelectFromParam(els.source, params.get("source"));
  setSelectFromParam(els.area, params.get("area"));
  setSelectFromParam(els.brazil, params.get("brazil"));
  setSelectFromParam(els.kind, params.get("kind"));
  setSelectFromParam(els.format, params.get("format"));
  setSelectFromParam(els.protocol, params.get("protocol"));
  setSelectFromParam(els.auth, params.get("auth"));
  setSelectFromParam(els.status, params.get("status"));
  setSelectFromParam(els.origin, params.get("origin"));
  setSelectFromParam(els.sort, params.get("sort"));
}

function productMatchesQuery(product, query) {
  if (!query) return true;
  return query.split(/\s+/).filter(Boolean).every(term => product._search.includes(term));
}

function filter(syncUrl = true) {
  const query = norm(els.q.value.trim());
  filtered = all.filter(product =>
    productMatchesQuery(product, query) &&
    (!els.source.value || product.source.resource_name === els.source.value) &&
    (!els.area.value || split(product.research_areas).includes(els.area.value)) &&
    (!els.brazil.value || product.covers_brazil === els.brazil.value) &&
    (!els.kind.value || product.product_kind === els.kind.value) &&
    (!els.format.value || productFormats(product).includes(els.format.value)) &&
    (!els.protocol.value || productProtocols(product).includes(els.protocol.value)) &&
    (!els.auth.value || product.distributions.some(item => item.authentication_required === els.auth.value)) &&
    (!els.status.value || product.product_status === els.status.value) &&
    (!els.origin.value || product.primary_or_derived === els.origin.value)
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

function populateFilters() {
  populateSelect(els.source, all.map(product => product.source.resource_name), "Todas as fontes");
  populateSelect(els.area, all.flatMap(product => split(product.research_areas)), "Todas as áreas");
  populateSelect(els.brazil, all.map(product => product.covers_brazil), "Qualquer situação", ENUM_ORDER, ENUM_LABELS);
  populateSelect(els.kind, all.map(product => product.product_kind), "Todos os tipos", null, KIND_LABELS);
  populateSelect(els.format, all.flatMap(productFormats), "Todos os formatos");
  populateSelect(els.protocol, all.flatMap(productProtocols), "Todos os protocolos");
  populateSelect(els.auth, all.flatMap(product => product.distributions.map(item => item.authentication_required)), "Qualquer situação", ENUM_ORDER, ENUM_LABELS);
  populateSelect(els.status, all.map(product => product.product_status), "Todos os estados");
  populateSelect(els.origin, all.map(product => product.primary_or_derived), "Primário ou derivado", null, ORIGIN_LABELS);
}

function handleCompareChange(event) {
  const productId = event.target.dataset.compare;
  if (event.target.checked && selected.size >= 3) {
    event.target.checked = false;
    els.compareStatus.textContent = "O limite é de três produtos por comparação.";
    return;
  }
  if (event.target.checked) selected.add(productId);
  else selected.delete(productId);
  renderCompareBar();
}

function renderCompareBar() {
  const count = selected.size;
  els.compareBar.hidden = count === 0;
  els.compareCount.textContent = `${count} ${count === 1 ? "produto selecionado" : "produtos selecionados"}`;
  els.compareStatus.textContent = count < 2 ? "Selecione mais um produto para comparar." : "Comparação pronta.";
}

function comparisonValue(product, key) {
  const free = aggregateEnum(product.distributions.map(item => item.free_download));
  const auth = aggregateEnum(product.distributions.map(item => item.authentication_required));
  const values = {
    source: product.source.resource_name,
    description: product.product_description,
    coverage: product.geographic_coverage,
    spatial: `${product.spatial_support} · ${product.spatial_resolution}`,
    temporal: `${product.temporal_coverage} · ${product.temporal_resolution}`,
    update: product.update_frequency,
    version: product.version_or_collection,
    origin: ORIGIN_LABELS[product.primary_or_derived] || product.primary_or_derived,
    formats: productFormats(product).join(" | "),
    protocols: productProtocols(product).join(" | "),
    free: ENUM_LABELS[free] || free,
    auth: ENUM_LABELS[auth] || auth,
    limitations: product.limitations,
    verified: product.last_verified
  };
  return values[key] || "Não informado";
}

function openComparison() {
  const products = [...selected].map(id => all.find(product => product.product_id === id)).filter(Boolean);
  if (products.length < 2) {
    els.compareStatus.textContent = "Selecione pelo menos dois produtos.";
    return;
  }
  const rows = [
    ["Fonte", "source"], ["Descrição", "description"], ["Cobertura", "coverage"],
    ["Suporte e resolução espacial", "spatial"], ["Cobertura e resolução temporal", "temporal"],
    ["Atualização", "update"], ["Versão ou coleção", "version"], ["Origem", "origin"],
    ["Formatos", "formats"], ["Protocolos", "protocols"], ["Download gratuito", "free"],
    ["Autenticação", "auth"], ["Limitações", "limitations"], ["Verificação", "verified"]
  ];
  els.compareContent.innerHTML = `<div class="compare-table-wrap"><table class="compare-table"><thead><tr><th scope="col">Dimensão</th>${products.map(product => `<th scope="col">${esc(product.product_name)}</th>`).join("")}</tr></thead><tbody>${rows.map(([label, key]) => `<tr><th scope="row">${esc(label)}</th>${products.map(product => `<td>${esc(comparisonValue(product, key))}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
  if (typeof els.compareDialog.showModal === "function") els.compareDialog.showModal();
  else els.compareDialog.setAttribute("open", "");
}

function clearComparison() {
  selected.clear();
  document.querySelectorAll("[data-compare]").forEach(input => { input.checked = false; });
  renderCompareBar();
  if (els.compareDialog.open) els.compareDialog.close();
}

async function init() {
  try {
    const response = await fetch("data/data_products.json");
    if (!response.ok) throw Error("Não foi possível carregar os produtos.");

    all = await response.json();
    all.forEach(product => { product._search = searchableText(product); });
    populateFilters();
    readUrl();

    [els.q, els.source, els.area, els.brazil, els.kind, els.format, els.protocol, els.auth, els.status, els.origin, els.sort]
      .forEach(element => element.addEventListener(element === els.q ? "input" : "change", () => filter()));
    els.searchForm.addEventListener("submit", event => { event.preventDefault(); filter(); goToCatalog(); });
    document.querySelectorAll("[data-product-query]").forEach(button => button.addEventListener("click", () => setQuery(button.dataset.productQuery)));
    $("#product-clear").addEventListener("click", () => {
      $("#product-filters").reset();
      els.q.value = "";
      els.sort.value = "relevance";
      els.advancedFilters.open = false;
      filter();
      els.q.focus();
    });
    $("#compare-open").addEventListener("click", openComparison);
    $("#compare-clear").addEventListener("click", clearComparison);
    $("#compare-close").addEventListener("click", () => els.compareDialog.close());
    els.compareDialog.addEventListener("click", event => {
      if (event.target === els.compareDialog) els.compareDialog.close();
    });
    window.addEventListener("popstate", () => { readUrl(); filter(false); });

    $("#p-total").textContent = all.length;
    $("#p-sources").textContent = new Set(all.map(product => product.resource_id)).size;
    $("#p-free").textContent = all.filter(product => product.distributions.some(item => item.free_download === "sim")).length;
    $("#p-formats").textContent = new Set(all.flatMap(productFormats)).size;
    filter(false);
  } catch (error) {
    els.list.setAttribute("aria-busy", "false");
    els.count.textContent = "Falha ao carregar os produtos";
    els.list.innerHTML = `<div class="empty"><h3>Falha ao carregar os produtos</h3><p>${esc(error.message)}</p></div>`;
  }
}

init();
