const year = document.getElementById("year");

if (year) {
  year.textContent = new Date().getFullYear();
}

const header = document.querySelector("[data-site-header]");

if (header) {
  const updateHeader = () => {
    header.classList.toggle("is-scrolled", window.scrollY > 18);
  };

  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });
}

const navigationLinks = [...document.querySelectorAll('.site-header nav a[href^="#"]')];
const navigationSections = navigationLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

if ("IntersectionObserver" in window && navigationSections.length) {
  if ("matchMedia" in window && window.matchMedia("(prefers-reduced-motion: no-preference)").matches) {
    const artworkObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-entering");
            artworkObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 },
    );

    document.querySelectorAll(".project-visual").forEach((visual) => artworkObserver.observe(visual));
  }

  const visibleSections = new Set();
  const navigationObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          visibleSections.add(entry.target);
        } else {
          visibleSections.delete(entry.target);
        }
      });

      const currentSection = navigationSections.filter((section) => visibleSections.has(section)).pop();

      navigationLinks.forEach((link) => {
        if (currentSection && link.getAttribute("href") === `#${currentSection.id}`) {
          link.setAttribute("aria-current", "location");
        } else {
          link.removeAttribute("aria-current");
        }
      });
    },
    { rootMargin: "-72px 0px -40% 0px", threshold: 0 },
  );

  navigationSections.forEach((section) => navigationObserver.observe(section));
}
