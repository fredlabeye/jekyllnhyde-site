/* Jekyll N' Hyde — scripts (aucune dépendance) */
(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Menu mobile */
  var burger = document.querySelector(".burger");
  var nav = document.querySelector(".nav");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* Machine à écrire de l'accueil : fait tourner les derniers mots */
  var typed = document.querySelector(".typed");
  if (typed && !reduce) {
    var words = (typed.getAttribute("data-words") || "").split("|");
    var wi = 0, ci = words[0].length, deleting = true;
    var tick = function () {
      var w = words[wi];
      if (deleting) {
        ci--;
        typed.textContent = w.slice(0, ci);
        if (ci === 0) { deleting = false; wi = (wi + 1) % words.length; }
        setTimeout(tick, 50);
      } else {
        w = words[wi]; ci++;
        typed.textContent = w.slice(0, ci);
        if (ci === w.length) { deleting = true; setTimeout(tick, 2200); }
        else setTimeout(tick, 90);
      }
    };
    setTimeout(tick, 2500);
  }

  /* Lecteur Vimeo (chargé seulement au clic : rien de tiers avant) */
  function vimeoSrc(id) {
    return "https://player.vimeo.com/video/" + id + "?autoplay=1&dnt=1&title=0&byline=0&portrait=0";
  }
  function vimeoFrame(id, title) {
    var f = document.createElement("iframe");
    f.src = vimeoSrc(id);
    f.title = title || "Vidéo";
    f.allow = "autoplay; fullscreen; picture-in-picture";
    f.allowFullscreen = true;
    return f;
  }

  /* Showreel en ligne */
  document.querySelectorAll(".player[data-vimeo]").forEach(function (p) {
    var btn = p.querySelector(".player-btn");
    if (!btn) return;
    btn.addEventListener("click", function () {
      p.innerHTML = "";
      p.appendChild(vimeoFrame(p.getAttribute("data-vimeo"), p.getAttribute("data-title")));
    });
  });

  /* Visionneuse (photos + vidéos) */
  var lb = document.querySelector(".lightbox");
  if (lb) {
    var stage = lb.querySelector(".lb-stage");
    var cap = lb.querySelector(".lb-cap");
    var items = [], idx = 0, last = null;
    var show = function () {
      var it = items[idx];
      stage.innerHTML = "";
      if (it.vimeo) {
        var box = document.createElement("div");
        box.className = "lb-video";
        box.appendChild(vimeoFrame(it.vimeo, it.title));
        stage.appendChild(box);
      } else {
        var img = new Image();
        img.src = it.src; img.alt = it.alt || "";
        stage.appendChild(img);
        if (items[idx + 1] && !items[idx + 1].vimeo) { new Image().src = items[idx + 1].src; }
      }
      cap.innerHTML = it.cap || "";
      lb.querySelector(".lb-prev").hidden = lb.querySelector(".lb-next").hidden = items.length < 2;
    };
    var open = function (list, i, trigger) {
      items = list; idx = i; last = trigger;
      show();
      lb.classList.add("open");
      document.body.style.overflow = "hidden";
      lb.querySelector(".lb-close").focus();
    };
    var close = function () {
      lb.classList.remove("open");
      stage.innerHTML = "";
      document.body.style.overflow = "";
      if (last) last.focus();
    };
    var step = function (d) { idx = (idx + d + items.length) % items.length; show(); };
    lb.querySelector(".lb-close").addEventListener("click", close);
    lb.querySelector(".lb-prev").addEventListener("click", function () { step(-1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { step(1); });
    lb.addEventListener("click", function (e) { if (e.target === lb || e.target === stage) close(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") step(-1);
      if (e.key === "ArrowRight") step(1);
    });
    var sx = null;
    lb.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1);
      sx = null;
    });

    var links = Array.prototype.slice.call(document.querySelectorAll(".gallery a"));
    var photos = links.map(function (a) {
      var fc = a.querySelector("figcaption");
      return { src: a.getAttribute("href"), alt: a.querySelector("img").alt, cap: fc ? fc.innerHTML.replace(/<br>/g, " ") : "" };
    });
    links.forEach(function (a, i) {
      a.addEventListener("click", function (e) { e.preventDefault(); open(photos, i, a); });
    });

    var vids = Array.prototype.slice.call(document.querySelectorAll("[data-lb-vimeo]"));
    vids.forEach(function (b) {
      b.addEventListener("click", function () {
        open([{ vimeo: b.getAttribute("data-lb-vimeo"), title: b.getAttribute("aria-label") }], 0, b);
      });
    });
  }

  /* Carrousel des coulisses (défilement auto, pause au survol) */
  var bs = document.querySelector(".backstage");
  if (bs) {
    var track = bs.querySelector(".backstage-track");
    var n = track.children.length, pos = 0, timer = null;
    var perView = function () { var w = window.innerWidth; return w <= 767 ? 1 : w <= 1024 ? 2 : 4; };
    var go = function () {
      var pv = perView();
      pos = (pos + 1) % (n - pv + 1);
      track.style.transform = "translateX(" + (-pos * 100 / pv) + "%)";
    };
    var start = function () { if (!reduce && !timer) timer = setInterval(go, 5000); };
    var stop = function () { clearInterval(timer); timer = null; };
    bs.addEventListener("mouseenter", stop);
    bs.addEventListener("mouseleave", start);
    window.addEventListener("resize", function () { pos = -1; go(); });
    start();
  }
})();
