/* ============================================
   ADJ – Main JavaScript
   Scroll spy, FAQ accordion, counters, reveals
   ============================================ */

document.addEventListener("DOMContentLoaded", () => {
  initScrollSpy();
  initStickyNav();
  initFAQ();
  initCounters();
  initReveal();
  initStatsBars();
  initDatesCarousel();
});

/* ---------- Scroll Spy (Intersection Observer) ---------- */
function initScrollSpy() {
  const nav = document.querySelector(".anchor-nav");
  if (!nav) return;

  const links = nav.querySelectorAll(".anchor-nav__link");
  const sections = [];

  links.forEach((link) => {
    const id = link.getAttribute("href")?.replace("#", "");
    const section = id && document.getElementById(id);
    if (section) sections.push({ el: section, link });
  });

  if (!sections.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const item = sections.find((s) => s.el === entry.target);
        if (!item) return;

        if (entry.isIntersecting) {
          links.forEach((l) => l.classList.remove("is-active"));
          item.link.classList.add("is-active");

          // Scroll active link into view on mobile
          if (window.innerWidth < 768) {
            item.link.scrollIntoView({
              behavior: "smooth",
              block: "nearest",
              inline: "center",
            });
          }
        }
      });
    },
    {
      rootMargin: "-20% 0px -60% 0px",
      threshold: 0,
    }
  );

  sections.forEach((s) => observer.observe(s.el));
}

/* ---------- Sticky Nav shadow ---------- */
function initStickyNav() {
  const nav = document.querySelector(".anchor-nav");
  if (!nav) return;

  const hero = document.querySelector(".hero");
  if (!hero) return;

  const observer = new IntersectionObserver(
    ([entry]) => {
      nav.classList.toggle("is-stuck", !entry.isIntersecting);
    },
    { threshold: 0 }
  );

  observer.observe(hero);
}

/* ---------- FAQ Accordion ---------- */
function initFAQ() {
  const items = document.querySelectorAll(".faq-item");

  items.forEach((item) => {
    const btn = item.querySelector(".faq-item__q");
    const answer = item.querySelector(".faq-item__a");
    if (!btn || !answer) return;

    btn.addEventListener("click", () => {
      const isOpen = item.classList.contains("is-open");

      // Close all others
      items.forEach((other) => {
        if (other !== item) {
          other.classList.remove("is-open");
          const a = other.querySelector(".faq-item__a");
          if (a) a.style.maxHeight = "0";
        }
      });

      // Toggle current
      item.classList.toggle("is-open", !isOpen);
      answer.style.maxHeight = isOpen ? "0" : answer.scrollHeight + "px";
    });
  });
}

/* ---------- Counter Animation ---------- */
function initCounters() {
  const counters = document.querySelectorAll("[data-counter]");
  if (!counters.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        if (el.dataset.counted) return;
        el.dataset.counted = "true";
        animateCounter(el);
        observer.unobserve(el);
      });
    },
    { threshold: 0.3 }
  );

  counters.forEach((c) => observer.observe(c));
}

function animateCounter(el) {
  const target = parseFloat(el.dataset.counter);
  const suffix = el.dataset.suffix || "";
  const prefix = el.dataset.prefix || "";
  const decimals = (target.toString().split(".")[1] || "").length;
  const duration = 1800;
  const start = performance.now();

  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    // Ease out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = eased * target;

    el.textContent = prefix + current.toFixed(decimals).replace(".", ",") + suffix;

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

/* ---------- Stats Bars Animation ---------- */
function initStatsBars() {
  const bars = document.querySelectorAll(".stats-bar__fill");
  if (!bars.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        if (el.dataset.animated) return;
        el.dataset.animated = "true";
        el.style.width = el.dataset.width;
        observer.unobserve(el);
      });
    },
    { threshold: 0.5 }
  );

  bars.forEach((b) => observer.observe(b));
}

/* ---------- Scroll Reveal ---------- */
function initReveal() {
  const reveals = document.querySelectorAll(".reveal");
  if (!reveals.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.1,
      rootMargin: "0px 0px -40px 0px",
    }
  );

  reveals.forEach((r) => observer.observe(r));
}

/* ---------- Dates Carousel ---------- */
function initDatesCarousel() {
  const track = document.querySelector(".dates-carousel__track");
  if (!track) return;

  const prevBtn = document.querySelector(".dates-carousel__arrow--prev");
  const nextBtn = document.querySelector(".dates-carousel__arrow--next");
  const cards = track.querySelectorAll(".date-card");

  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      track.scrollBy({ left: -200, behavior: "smooth" });
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      track.scrollBy({ left: 200, behavior: "smooth" });
    });
  }

  const dateDisplay = document.getElementById("selectedDate");

  cards.forEach((card) => {
    card.addEventListener("click", (e) => {
      e.preventDefault();
      cards.forEach((c) => c.classList.remove("is-active"));
      card.classList.add("is-active");
      if (dateDisplay) {
        const dateText = card.querySelector(".date-card__date");
        if (dateText) dateDisplay.textContent = dateText.textContent;
      }
    });
  });
}
