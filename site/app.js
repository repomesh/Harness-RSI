/* Project page behaviour: navigation, reveal, the taxonomy and reading-list
   explorer built from site/corpus.js, the audit charts (article Figure 6),
   and small affordances (lightbox, BibTeX copy, cursor trail). */
(function () {
  "use strict";

  var CORPUS = window.CORPUS || { groups: [], entries: [], blurbs: {} };
  var GROUP_COLOR = {
    interpreted: "#5498d0", executable: "#e68a43", evaluation: "#6b925f", theory: "#9a70ba",
    precursors: "#64748b", risks: "#c2410c", products: "#0f766e", surveys: "#475569"
  };
  var CLAIM_NAMES = ["Selection", "Activation", "Attribution", "Improvement"];
  var VERDICT_WORD = { C: "full", O: "partial", N: "not supported" };

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function el(tag, attrs, html) {
    var node = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { node.setAttribute(k, attrs[k]); });
    if (html !== undefined) node.innerHTML = html;
    return node;
  }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }

  /* ---------- navigation ---------- */
  var toggle = $(".nav-toggle"), menu = $("#nl");
  function setMenu(open) {
    menu.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close navigation menu" : "Open navigation menu");
  }
  toggle.addEventListener("click", function () { setMenu(!menu.classList.contains("open")); });
  $all("#nl a").forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { setMenu(false); closeLightbox(); }
    if (e.key === "/" && document.activeElement !== $("#q")) { e.preventDefault(); $("#q").focus(); }
  });

  var progress = $(".progress");
  var navLinks = $all('#nl a[href^="#"]');
  var sections = navLinks.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
  function onScroll() {
    var max = document.documentElement.scrollHeight - innerHeight;
    progress.style.width = (max > 0 ? (scrollY / max) * 100 : 0) + "%";
    var current = -1;
    sections.forEach(function (s, i) { if (s && s.getBoundingClientRect().top < 120) current = i; });
    navLinks.forEach(function (a, i) { a.classList.toggle("on", i === current); });
  }
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (CORPUS.entries.length) $("#entryCount").textContent = CORPUS.entries.length;

  /* ---------- reveal ---------- */
  var onReveal = [];
  function whenVisible(node, fn) { onReveal.push([node, fn]); }
  var io = "IntersectionObserver" in window ? new IntersectionObserver(function (items) {
    items.forEach(function (it) {
      if (!it.isIntersecting) return;
      it.target.classList.add("in");
      onReveal.forEach(function (pair) { if (pair[0] === it.target) pair[1](); });
      io.unobserve(it.target);
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }) : null;

  /* ---------- taxonomy ---------- */
  function tree(groupKey) {
    var subs = [];
    CORPUS.entries.forEach(function (e) {
      if (e.group !== groupKey) return;
      var sub = subs.filter(function (s) { return s.name === e.sub; })[0];
      if (!sub) { sub = { name: e.sub, nodes: [] }; subs.push(sub); }
      var node = sub.nodes.filter(function (n) { return n.name === e.node; })[0];
      if (!node) { node = { name: e.node, count: 0 }; sub.nodes.push(node); }
      node.count++;
    });
    return subs;
  }
  // Subsection numbers follow the article: §3.2-3.4, §4.1-4.3, §6.2-6.3.
  var BRANCHES = [
    { key: "interpreted", cls: "int", num: "§3", first: [3, 2], title: "Interpreted update targets",
      gloss: "Model-readable content and coordination state read by a fixed host. Behavioral: an instruction shifts tendencies but cannot impose a runtime invariant." },
    { key: "executable", cls: "exe", num: "§4", first: [4, 1], title: "Executable update targets",
      gloss: "Implementations the host invokes directly: tools, component files, control programs, plugins. Enforceable: the revision runs." },
    { key: "evaluation", cls: "eva", num: "§6", first: [6, 2], title: "Evaluation & benchmarks",
      gloss: "Works whose own contribution is an evaluation protocol or an audit, placed under the claim their protocol enforces." }
  ];
  function renderBranch(b, host) {
    var subs = tree(b.key);
    var total = subs.reduce(function (a, s) { return a + s.nodes.reduce(function (x, n) { return x + n.count; }, 0); }, 0);
    host.className = "branch " + b.cls + " reveal";
    host.innerHTML = '<div class="branch-head"><h3>' + b.title + '</h3><span class="count">' + b.num + " · " + total + " works</span></div>" +
      '<p class="gloss">' + b.gloss + "</p>";
    subs.forEach(function (s, i) {
      var box = el("div", { "class": "subsec" });
      box.innerHTML = '<h4><span class="sn">§' + b.first[0] + "." + (b.first[1] + i) + "</span>" + escapeHtml(s.name) + "</h4>";
      var mechs = el("div", { "class": "mechs" });
      s.nodes.forEach(function (n) {
        var gloss = CORPUS.blurbs[n.name] ? CORPUS.blurbs[n.name].replace(/<[^>]+>/g, "") : "";
        var btn = el("button", { "class": "mech", type: "button", title: gloss }, escapeHtml(n.name || s.name) + " <b>" + n.count + "</b>");
        btn.addEventListener("click", function () { focusNode(b.key, n.name || s.name); });
        mechs.appendChild(btn);
      });
      box.appendChild(mechs);
      host.appendChild(box);
    });
  }
  var branchesHost = $("#branches");
  BRANCHES.slice(0, 2).forEach(function (b) { var h = el("div"); branchesHost.appendChild(h); renderBranch(b, h); });
  renderBranch(BRANCHES[2], $("#branch-eva"));

  /* ---------- reading-list explorer ---------- */
  var state = { q: "", group: "all", node: "" };
  var groupLabel = {};
  CORPUS.groups.forEach(function (g) { groupLabel[g.key] = g.label; });
  var groupChips = [{ key: "all", label: "All" }].concat(CORPUS.groups).map(function (g) {
    var n = CORPUS.entries.filter(function (e) { return g.key === "all" || e.group === g.key; }).length;
    var chip = el("button", { "class": "chip", type: "button", "data-group": g.key }, escapeHtml(g.label) + ' <span class="n">' + n + "</span>");
    chip.addEventListener("click", function () { state.group = g.key; state.node = ""; render(); });
    $("#groupFilters").appendChild(chip);
    return chip;
  });
  var qInput = $("#q"), timer = null;
  qInput.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(function () { state.q = qInput.value.trim().toLowerCase(); render(); }, 90);
  });
  $("#resetFilters").addEventListener("click", function () {
    state = { q: "", group: "all", node: "" }; qInput.value = ""; render();
  });
  function focusNode(group, node) {
    state = { q: "", group: group, node: node }; qInput.value = "";
    render();
    document.getElementById("explorer").scrollIntoView({ behavior: "smooth" });
    $("#results").scrollTop = 0;
  }

  function highlight(html, q) {
    if (!q) return html;
    var safe = q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    // Only touch text between tags so markup inside the sentence survives.
    return html.replace(/(^|>)([^<]+)/g, function (m, lead, text) {
      return lead + text.replace(new RegExp("(" + safe + ")", "ig"), "<mark>$1</mark>");
    });
  }
  function matches(e) {
    if (state.group !== "all" && e.group !== state.group) return false;
    if (state.node && e.node !== state.node && e.sub !== state.node) return false;
    if (state.q) {
      var hay = (e.name + " " + e.venue + " " + e.desc.replace(/<[^>]+>/g, "") + " " + e.node + " " + e.sub).toLowerCase();
      if (hay.indexOf(state.q) < 0) return false;
    }
    return true;
  }
  function row(e) {
    var links = e.links.map(function (l) {
      return '<a href="' + escapeHtml(l[1]) + '" target="_blank" rel="noopener">' + escapeHtml(l[0]) + "</a>";
    }).join("");
    var verdict = "";
    if (e.verdict && e.verdict !== "XXXX") {
      var title = CLAIM_NAMES.map(function (n, i) { return n + ": " + VERDICT_WORD[e.verdict[i]]; }).join(" · ");
      verdict = '<span class="verdict" title="' + title + '" aria-label="' + title + '">' +
        e.verdict.split("").map(function (v) { return '<span class="' + v + '"></span>'; }).join("") + "</span>";
    }
    return '<div class="row"><div><span class="nm">' + highlight(escapeHtml(e.name), state.q) + "</span>" +
      (e.venue ? '<span class="venue">' + escapeHtml(e.venue) + "</span>" : "") +
      (e.node ? '<span class="node">' + escapeHtml(e.node) + "</span>" : "") +
      '<span class="desc">' + highlight(e.desc, state.q) + "</span></div>" +
      '<div class="side">' + verdict + links + "</div></div>";
  }
  function render() {
    groupChips.forEach(function (c) { c.classList.toggle("on", c.getAttribute("data-group") === state.group); });
    var list = CORPUS.entries.filter(matches);
    var html = "", lastGroup = null;
    list.forEach(function (e) {
      if (e.group !== lastGroup) {
        var n = list.filter(function (x) { return x.group === e.group; }).length;
        html += '<div class="group-head" style="--gc:' + GROUP_COLOR[e.group] + '">' + escapeHtml(groupLabel[e.group]) + "<span>" + n + "</span></div>";
        lastGroup = e.group;
      }
      html += row(e).replace('class="row"', 'class="row" style="--gc:' + GROUP_COLOR[e.group] + '"');
    });
    $("#results").innerHTML = html || '<p class="empty">No entry matches. Try a broader search or reset.</p>';
    var parts = [list.length + " of " + CORPUS.entries.length + " entries"];
    if (state.node) parts.push(state.node);
    $("#resultCount").textContent = parts.join(" · ");
  }
  render();

  /* ---------- audit charts (article Figure 6) ---------- */
  var SCORED = 94;
  var AUDIT = [
    { name: "Selection", C: 41, O: 19, N: 34 },
    { name: "Activation", C: 14, O: 80, N: 0 },
    { name: "Attribution", C: 24, O: 68, N: 2 },
    { name: "Improvement", C: 54, O: 18, N: 22 }
  ];
  var barsHost = $("#claimBars .bars");
  AUDIT.forEach(function (r) {
    var line = el("div", { "class": "bar-row" });
    var segs = ["C", "O", "N"].map(function (k) {
      if (!r[k]) return "";
      var label = r[k] >= 5 ? r[k] : "";
      return '<span class="' + k + '" data-w="' + r[k] + '" title="' + r[k] + " " + ({ C: "full", O: "partial", N: "not supported" })[k] + '">' + label + "</span>";
    }).join("");
    line.innerHTML = '<div class="nm">' + r.name + '</div><div class="stack-bar">' + segs + "</div>";
    barsHost.appendChild(line);
  });
  whenVisible($("#claimBars"), function () {
    $all("#claimBars .stack-bar span").forEach(function (s) { s.style.width = (100 * s.getAttribute("data-w") / SCORED) + "%"; });
  });

  var JOINT = [
    { k: "None", v: 24, c: "#dde3ec" }, { k: "One", v: 20, c: "#b4c2d9" }, { k: "Two", v: 37, c: "#8399bb" },
    { k: "Three", v: 13, c: "#4f6a94" }, { k: "Four", v: 0, c: "#1e3a8a" }
  ];
  (function donut() {
    var host = $("#donut");
    var R = 80, C = 2 * Math.PI * R, acc = 0;
    var rings = JOINT.filter(function (j) { return j.v; }).map(function (j) {
      var len = (j.v / SCORED) * C;
      var circle = '<circle cx="100" cy="100" r="' + R + '" stroke="' + j.c + '" stroke-dasharray="0 ' + C + '" data-len="' + len + '" stroke-dashoffset="' + (-acc) + '" transform="rotate(-90 100 100)"><title>' + j.k + ": " + j.v + "</title></circle>";
      acc += len;
      return circle;
    }).join("");
    host.innerHTML = '<svg class="donut" viewBox="0 0 200 200" role="img" aria-label="Scored reports by number of claims at full evidence">' + rings +
      '<text class="small" x="100" y="96" text-anchor="middle">94 scored</text><text class="small" x="100" y="113" text-anchor="middle">reports</text></svg>' +
      '<div class="joint">' + JOINT.map(function (j) { return "<div><b>" + j.v + "</b>" + j.k + '<i style="background:' + j.c + '"></i></div>'; }).join("") + "</div>";
    whenVisible(host.closest(".panel"), function () {
      $all("circle[data-len]", host).forEach(function (c) {
        var len = +c.getAttribute("data-len");
        c.setAttribute("stroke-dasharray", len + " " + (C - len));
      });
    });
  })();

  $all(".reveal").forEach(function (node, i) {
    node.style.transitionDelay = (Math.min(i % 4, 3) * 60) + "ms";
    if (io) io.observe(node);
    else { node.classList.add("in"); onReveal.forEach(function (p) { if (p[0] === node) p[1](); }); }
  });

  /* ---------- math ---------- */
  function renderMath() {
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, {
        delimiters: [{ left: "\\(", right: "\\)", display: false }, { left: "\\[", right: "\\]", display: true }],
        throwOnError: false
      });
    }
  }
  if (document.readyState === "complete") renderMath(); else addEventListener("load", renderMath);

  /* ---------- lightbox ---------- */
  var box = $("#lightbox"), boxImg = $("#lightbox img");
  function closeLightbox() { box.classList.remove("open"); document.body.style.overflow = ""; }
  $all(".figure img, details.fold img").forEach(function (img) {
    img.addEventListener("click", function () {
      boxImg.src = img.currentSrc || img.src; boxImg.alt = img.alt;
      box.classList.add("open"); document.body.style.overflow = "hidden";
    });
  });
  box.addEventListener("click", closeLightbox);

  /* ---------- BibTeX ---------- */
  $("#cbtn").addEventListener("click", function () {
    var btn = this, raw = $("#bib").innerText;
    function done(ok) {
      btn.classList.toggle("done", ok); btn.textContent = ok ? "Copied ✓" : "Copy failed";
      setTimeout(function () { btn.classList.remove("done"); btn.textContent = "Copy BibTeX"; }, 1800);
    }
    if (navigator.clipboard && window.isSecureContext) { navigator.clipboard.writeText(raw).then(function () { done(true); }, function () { done(false); }); return; }
    var area = el("textarea"); area.value = raw; area.style.position = "fixed"; area.style.opacity = "0";
    document.body.appendChild(area); area.select();
    try { done(document.execCommand("copy")); } catch (err) { done(false); }
    area.remove();
  });

  /* ---------- cursor trail ---------- */
  (function trail() {
    if (!matchMedia("(hover:hover) and (pointer:fine)").matches) return;
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var canvas = $(".trail"), ctx = canvas.getContext("2d");
    var pts = [], raf = 0, x = 0, y = 0;
    function size() {
      var r = Math.min(devicePixelRatio || 1, 2);
      canvas.width = innerWidth * r; canvas.height = innerHeight * r; ctx.setTransform(r, 0, 0, r, 0, 0);
    }
    function draw() {
      raf = 0;
      ctx.clearRect(0, 0, innerWidth, innerHeight);
      pts.forEach(function (p) { p.life *= 0.9; });
      pts = pts.filter(function (p) { return p.life > 0.04; });
      for (var i = 1; i < pts.length; i++) {
        var a = pts[i - 1], b = pts[i];
        ctx.strokeStyle = "rgba(37,99,235," + (b.life * 0.3).toFixed(3) + ")";
        ctx.lineWidth = 2 + b.life * 3; ctx.lineCap = "round";
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
      }
      if (pts.length) raf = requestAnimationFrame(draw);
    }
    size(); addEventListener("resize", size, { passive: true });
    addEventListener("pointermove", function (e) {
      x = e.clientX; y = e.clientY;
      pts.push({ x: x, y: y, life: 1 });
      if (pts.length > 24) pts.shift();
      if (!raf) raf = requestAnimationFrame(draw);
    }, { passive: true });
  })();
})();
