"use strict";

const REGISTRY_URL = "data/federated_layers.json";
const APP_VERSION = "0.2.0";

const state = {
  registry: null,
  map: null,
  order: [],
  visibility: new Map(),
  opacity: new Map(),
  status: new Map(),
};

const elements = {
  layerList: document.getElementById("layer-list"),
  layerEmpty: document.getElementById("layer-empty"),
  visibleCount: document.getElementById("visible-count"),
  attribution: document.getElementById("visible-attribution"),
  inspection: document.getElementById("inspection-content"),
  compatibility: document.getElementById("compatibility-summary"),
  mapStatus: document.getElementById("map-status"),
  share: document.getElementById("share-view"),
  manifest: document.getElementById("download-manifest"),
  reset: document.getElementById("reset-view"),
};

function escapeHTML(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function layerById(layerId) {
  return state.registry.layers.find((layer) => layer.layer_id === layerId);
}

function mapLayerId(layerId) {
  return `federated-layer-${layerId}`;
}

function sourceId(layerId) {
  return `federated-source-${layerId}`;
}

function visibleLayers() {
  return state.order
    .filter((layerId) => state.visibility.get(layerId))
    .map(layerById)
    .filter(Boolean);
}

function parseURLState() {
  const params = new URLSearchParams(window.location.search);
  const knownIds = new Set(state.registry.layers.map((layer) => layer.layer_id));

  const requestedOrder = (params.get("order") || "")
    .split(",")
    .map((value) => value.trim())
    .filter((value) => knownIds.has(value));
  const missing = state.registry.layers
    .map((layer) => layer.layer_id)
    .filter((value) => !requestedOrder.includes(value));
  state.order = [...requestedOrder, ...missing];

  const layerParameter = params.get("layers");
  const visibleIds = layerParameter === null
    ? new Set(state.registry.layers.filter((layer) => layer.default_visible).map((layer) => layer.layer_id))
    : new Set(layerParameter.split(",").filter((value) => knownIds.has(value)));

  const opacityValues = new Map();
  (params.get("opacity") || "").split(",").forEach((pair) => {
    const [layerId, rawValue] = pair.split(":");
    const numeric = Number(rawValue);
    if (knownIds.has(layerId) && Number.isFinite(numeric)) {
      opacityValues.set(layerId, Math.min(1, Math.max(0, numeric / 100)));
    }
  });

  state.registry.layers.forEach((layer) => {
    state.visibility.set(layer.layer_id, visibleIds.has(layer.layer_id));
    state.opacity.set(layer.layer_id, opacityValues.get(layer.layer_id) ?? layer.default_opacity);
    state.status.set(layer.layer_id, "pending");
  });
}

function updateURLState() {
  const url = new URL(window.location.href);
  const visible = state.order.filter((layerId) => state.visibility.get(layerId));
  const opacity = state.order.map((layerId) => `${layerId}:${Math.round((state.opacity.get(layerId) ?? 1) * 100)}`);

  url.searchParams.set("layers", visible.join(","));
  url.searchParams.set("opacity", opacity.join(","));
  url.searchParams.set("order", state.order.join(","));
  window.history.replaceState({}, "", url);
}

function link(label, url) {
  if (!url) return "";
  return `<a href="${escapeHTML(url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(label)}</a>`;
}

function layerCard(layer, index) {
  const visible = Boolean(state.visibility.get(layer.layer_id));
  const opacity = state.opacity.get(layer.layer_id) ?? layer.default_opacity;
  const status = state.status.get(layer.layer_id) || "pending";
  const statusLabel = status === "live" ? "carregada" : status === "error" ? "falhou" : "aguardando";
  const statusClass = status === "live" ? "is-live" : status === "error" ? "is-error" : "";
  const links = [
    link("Fonte oficial", layer.official_source_url),
    link("Produto", layer.product_url),
    link("Acessar dados", layer.data_access_url),
    link("Método", layer.methodology_url),
    link("Metadados", layer.metadata_url),
  ].filter(Boolean).join("");

  return `<article class="layer-card" role="listitem" data-layer-id="${escapeHTML(layer.layer_id)}" data-visible="${visible}" data-error="${status === "error"}">
    <div class="layer-card-header">
      <input type="checkbox" id="toggle-${escapeHTML(layer.layer_id)}" data-action="toggle" ${visible ? "checked" : ""} aria-label="Exibir ${escapeHTML(layer.title)}">
      <div><h3 class="layer-card-title">${escapeHTML(layer.short_title)}</h3><p class="layer-provider">${escapeHTML(layer.provider)}</p></div>
      <span class="layer-status ${statusClass}" data-status>${statusLabel}</span>
    </div>
    <label class="opacity-row" for="opacity-${escapeHTML(layer.layer_id)}"><span>Opacidade</span><input id="opacity-${escapeHTML(layer.layer_id)}" data-action="opacity" type="range" min="0" max="100" value="${Math.round(opacity * 100)}"><output>${Math.round(opacity * 100)}%</output></label>
    <div class="layer-controls">
      <button type="button" data-action="details" aria-expanded="false">Detalhes</button>
      <button type="button" data-action="up" ${index === 0 ? "disabled" : ""}>Subir</button>
      <button type="button" data-action="down" ${index === state.order.length - 1 ? "disabled" : ""}>Descer</button>
      ${link("Abrir na fonte", layer.product_url)}
    </div>
    <div class="layer-details" hidden>
      <dl>
        <dt>Produto</dt><dd>${escapeHTML(layer.product)}</dd>
        <dt>Período</dt><dd>${escapeHTML(layer.period)}</dd>
        <dt>Versão</dt><dd>${escapeHTML(layer.version)}</dd>
        <dt>Resolução</dt><dd>${escapeHTML(layer.spatial_resolution)}</dd>
        <dt>Licença</dt><dd>${escapeHTML(layer.license)}</dd>
        <dt>Compatibilidade</dt><dd>${escapeHTML(layer.compatibility_class)} — ${escapeHTML(layer.compatibility_label)}</dd>
        <dt>Teto de inferência</dt><dd>${escapeHTML(layer.inference_ceiling)}</dd>
        <dt>Uso analítico</dt><dd>${layer.analytical_use_allowed ? "permitido" : "não permitido"}</dd>
        <dt>Estado da evidência</dt><dd>${escapeHTML(layer.evidence_status)}</dd>
        <dt>Citação</dt><dd>${escapeHTML(layer.citation_text)}</dd>
      </dl>
      <p class="layer-warning"><strong>Atenção:</strong> ${escapeHTML(layer.scientific_warning)}</p>
      <div class="layer-links">${links}</div>
    </div>
  </article>`;
}

function renderLayerList() {
  elements.layerList.innerHTML = state.order.map((layerId, index) => layerCard(layerById(layerId), index)).join("");
  elements.layerList.setAttribute("aria-busy", "false");
  elements.layerEmpty.hidden = state.order.length > 0;
  updateSummary();
}

function updateSummary() {
  const visible = visibleLayers();
  elements.visibleCount.textContent = `${visible.length} ${visible.length === 1 ? "visível" : "visíveis"}`;
  elements.attribution.textContent = visible.length
    ? visible.map((layer) => layer.attribution).join(" · ")
    : "nenhuma camada científica";

  if (visible.length > 1) {
    elements.compatibility.className = "compatibility-summary is-warning";
    elements.compatibility.innerHTML = `<strong>Composição N0 de ${visible.length} camadas independentes</strong><span>Classe operacional C: apenas sobreposição visual. Nenhum cálculo, reamostragem, interseção, correlação ou validação cruzada foi realizado.</span>`;
  } else if (visible.length === 1) {
    elements.compatibility.className = "compatibility-summary";
    elements.compatibility.innerHTML = `<strong>Uma camada científica ativa — teto N0</strong><span>A visualização preserva a fonte original, não modifica os dados e não autoriza inferência analítica.</span>`;
  } else {
    elements.compatibility.className = "compatibility-summary";
    elements.compatibility.innerHTML = `<strong>Nenhuma camada científica ativa</strong><span>O mapa-base serve apenas como referência cartográfica.</span>`;
  }
}

function addMapLayer(layer) {
  const source = {
    type: "raster",
    tiles: layer.tiles,
    tileSize: layer.tile_size,
    minzoom: layer.min_zoom,
    maxzoom: layer.max_zoom,
    attribution: layer.attribution,
  };
  state.map.addSource(sourceId(layer.layer_id), source);
  state.map.addLayer({
    id: mapLayerId(layer.layer_id),
    type: "raster",
    source: sourceId(layer.layer_id),
    layout: {visibility: state.visibility.get(layer.layer_id) ? "visible" : "none"},
    paint: {"raster-opacity": state.opacity.get(layer.layer_id) ?? layer.default_opacity},
  });
}

function reorderMapLayers() {
  if (!state.map || !state.map.loaded()) return;
  [...state.order].reverse().forEach((layerId) => {
    const id = mapLayerId(layerId);
    if (state.map.getLayer(id)) state.map.moveLayer(id);
  });
}

function updateLayerVisibility(layerId) {
  if (!state.map?.getLayer(mapLayerId(layerId))) return;
  state.map.setLayoutProperty(mapLayerId(layerId), "visibility", state.visibility.get(layerId) ? "visible" : "none");
}

function updateLayerOpacity(layerId) {
  if (!state.map?.getLayer(mapLayerId(layerId))) return;
  state.map.setPaintProperty(mapLayerId(layerId), "raster-opacity", state.opacity.get(layerId));
}

function markLayerStatus(layerId, status) {
  if (!state.status.has(layerId) || state.status.get(layerId) === status) return;
  state.status.set(layerId, status);
  const card = elements.layerList.querySelector(`[data-layer-id="${CSS.escape(layerId)}"]`);
  if (!card) return;
  card.dataset.error = String(status === "error");
  const badge = card.querySelector("[data-status]");
  badge.className = `layer-status ${status === "live" ? "is-live" : status === "error" ? "is-error" : ""}`;
  badge.textContent = status === "live" ? "carregada" : status === "error" ? "falhou" : "aguardando";
}

function moveLayer(layerId, direction) {
  const index = state.order.indexOf(layerId);
  const target = direction === "up" ? index - 1 : index + 1;
  if (index < 0 || target < 0 || target >= state.order.length) return;
  [state.order[index], state.order[target]] = [state.order[target], state.order[index]];
  renderLayerList();
  reorderMapLayers();
  updateURLState();
}

function handleLayerPanel(event) {
  const card = event.target.closest("[data-layer-id]");
  const action = event.target.dataset.action;
  if (!card || !action) return;
  const layerId = card.dataset.layerId;

  if (action === "toggle") {
    state.visibility.set(layerId, event.target.checked);
    card.dataset.visible = String(event.target.checked);
    updateLayerVisibility(layerId);
    updateSummary();
    updateURLState();
  } else if (action === "opacity") {
    const value = Number(event.target.value) / 100;
    state.opacity.set(layerId, value);
    card.querySelector("output").textContent = `${Math.round(value * 100)}%`;
    updateLayerOpacity(layerId);
    updateURLState();
  } else if (action === "details") {
    const details = card.querySelector(".layer-details");
    details.hidden = !details.hidden;
    event.target.setAttribute("aria-expanded", String(!details.hidden));
    event.target.textContent = details.hidden ? "Detalhes" : "Ocultar detalhes";
  } else if (action === "up" || action === "down") {
    moveLayer(layerId, action);
  }
}

function inspectLocation(lngLat) {
  const visible = visibleLayers();
  const coordinate = `${lngLat.lat.toFixed(5)}, ${lngLat.lng.toFixed(5)}`;
  const list = visible.length
    ? `<ul class="inspection-layers">${visible.map((layer) => `<li><strong>${escapeHTML(layer.short_title)}</strong> — ${escapeHTML(layer.provider)}. <a href="${escapeHTML(layer.product_url)}" target="_blank" rel="noopener noreferrer">Abrir produto original</a></li>`).join("")}</ul>`
    : "<p>Nenhuma camada científica está visível.</p>";
  elements.inspection.innerHTML = `<p>Coordenadas: <span class="inspection-coordinate">${coordinate}</span></p>${list}<p><small>Esta consulta registra contexto e proveniência. Ela não executa GetFeatureInfo, não interpreta valores de pixel e permanece em N0.</small></p>`;

  new maplibregl.Popup({closeButton: true, maxWidth: "320px"})
    .setLngLat(lngLat)
    .setHTML(`<h3>Local consultado</h3><p>${coordinate}</p>${visible.length ? `<ul>${visible.map((layer) => `<li>${escapeHTML(layer.short_title)}</li>`).join("")}</ul>` : "<p>Sem camadas científicas ativas.</p>"}`)
    .addTo(state.map);
}

function manifestData() {
  const center = state.map.getCenter();
  const visible = visibleLayers();
  return {
    manifest_version: "1.1.0",
    application: "Simbioscópio — Explorador Federado",
    application_version: APP_VERSION,
    generated_at: new Date().toISOString(),
    visualization_type: "federated_visualization",
    operation_mode: state.registry.operation_mode,
    inference_ceiling: state.registry.inference_ceiling,
    analytical_use_allowed: state.registry.analytical_use_allowed,
    evidence_status: state.registry.evidence_status,
    scientific_policy: state.registry.scientific_policy,
    analytical_harmonization_performed: false,
    operations: ["visual_overlay", "opacity_adjustment", "layer_ordering", "viewport_selection"],
    warning: state.registry.disclaimer,
    view: {
      longitude: Number(center.lng.toFixed(6)),
      latitude: Number(center.lat.toFixed(6)),
      zoom: Number(state.map.getZoom().toFixed(3)),
      bearing: Number(state.map.getBearing().toFixed(2)),
      pitch: Number(state.map.getPitch().toFixed(2)),
    },
    base_map: state.registry.base_map,
    inputs: visible.map((layer) => ({
      layer_id: layer.layer_id,
      resource_id: layer.resource_id,
      product: layer.product,
      provider: layer.provider,
      period: layer.period,
      version: layer.version,
      opacity: state.opacity.get(layer.layer_id),
      layer_type: layer.layer_type,
      operation_scope: layer.operation_scope,
      compatibility_class: layer.compatibility_class,
      inference_ceiling: layer.inference_ceiling,
      analytical_use_allowed: layer.analytical_use_allowed,
      evidence_status: layer.evidence_status,
      official_source_url: layer.official_source_url,
      product_url: layer.product_url,
      data_access_url: layer.data_access_url,
      methodology_url: layer.methodology_url,
      metadata_url: layer.metadata_url,
      license: layer.license,
      citation: layer.citation_text,
      attribution: layer.attribution,
      scientific_warning: layer.scientific_warning,
    })),
    shared_url: window.location.href,
  };
}

function downloadManifest() {
  const blob = new Blob([JSON.stringify(manifestData(), null, 2)], {type: "application/json"});
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `simbioscope-visualization-provenance-${new Date().toISOString().slice(0, 10)}.json`;
  document.body.append(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
  showToast("Manifesto de proveniência e inferência gerado.");
}

async function shareView() {
  updateURLState();
  try {
    await navigator.clipboard.writeText(window.location.href);
    showToast("Link da visualização copiado.");
  } catch {
    window.prompt("Copie o link da visualização:", window.location.href);
  }
}

function showToast(message) {
  let toast = document.querySelector(".toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.className = "toast";
    toast.setAttribute("role", "status");
    document.body.append(toast);
  }
  toast.textContent = message;
  toast.hidden = false;
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => { toast.hidden = true; }, 2800);
}

function resetView() {
  const url = new URL(window.location.href);
  url.search = "";
  url.hash = "";
  window.location.assign(url);
}

function initializeMap() {
  if (typeof maplibregl === "undefined") {
    elements.mapStatus.textContent = "Biblioteca cartográfica indisponível.";
    elements.mapStatus.classList.add("is-error");
    return;
  }

  const view = state.registry.default_view;
  state.map = new maplibregl.Map({
    container: "map",
    style: state.registry.base_map.style_url,
    center: view.center,
    zoom: view.zoom,
    bearing: view.bearing,
    pitch: view.pitch,
    hash: true,
    attributionControl: true,
  });
  state.map.addControl(new maplibregl.NavigationControl({showCompass: true}), "top-right");
  state.map.addControl(new maplibregl.ScaleControl({unit: "metric"}), "bottom-left");

  state.map.on("load", () => {
    [...state.order].reverse().forEach((layerId) => addMapLayer(layerById(layerId)));
    reorderMapLayers();
    elements.mapStatus.textContent = "Mapa pronto. Serviços externos podem variar em disponibilidade.";
  });

  state.map.on("sourcedata", (event) => {
    if (!event.sourceId?.startsWith("federated-source-") || !event.isSourceLoaded) return;
    markLayerStatus(event.sourceId.replace("federated-source-", ""), "live");
  });

  state.map.on("error", (event) => {
    const source = event.sourceId || event.error?.sourceId;
    if (source?.startsWith("federated-source-")) {
      markLayerStatus(source.replace("federated-source-", ""), "error");
    }
    elements.mapStatus.textContent = "Um recurso externo falhou ou respondeu lentamente; consulte o estado da camada.";
    elements.mapStatus.classList.add("is-error");
  });

  state.map.on("click", (event) => inspectLocation(event.lngLat));
  state.map.on("moveend", updateURLState);
}

async function initialize() {
  try {
    const response = await fetch(REGISTRY_URL, {cache: "no-store"});
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.registry = await response.json();
    parseURLState();
    renderLayerList();
    initializeMap();
  } catch (error) {
    elements.layerList.setAttribute("aria-busy", "false");
    elements.layerList.innerHTML = `<div class="empty"><h3>Não foi possível carregar o registro de camadas</h3><p>${escapeHTML(error.message)}</p></div>`;
    elements.mapStatus.textContent = "Registro de camadas indisponível.";
    elements.mapStatus.classList.add("is-error");
  }
}

elements.layerList.addEventListener("input", handleLayerPanel);
elements.layerList.addEventListener("click", handleLayerPanel);
elements.share.addEventListener("click", shareView);
elements.manifest.addEventListener("click", downloadManifest);
elements.reset.addEventListener("click", resetView);

initialize();
