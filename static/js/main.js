// ============================================================
// SpongeFactory — Asosiy JavaScript
// ============================================================

document.addEventListener('DOMContentLoaded', function () {

  // ---------- Loading animatsiyasini yashirish ----------
  const loader = document.getElementById('page-loader');
  if (loader) {
    setTimeout(() => {
      loader.style.opacity = '0';
      setTimeout(() => loader.remove(), 500);
    }, 250);
  }

  // ---------- Hamburger menu (mobil navigatsiya) ----------
  const hamburgerBtn = document.getElementById('hamburger-btn');
  const mobileMenu = document.getElementById('mobile-menu');

  if (hamburgerBtn && mobileMenu) {
    hamburgerBtn.addEventListener('click', function () {
      const isOpen = !mobileMenu.classList.contains('hidden');
      mobileMenu.classList.toggle('hidden');
      hamburgerBtn.classList.toggle('is-open');
      hamburgerBtn.setAttribute('aria-expanded', String(!isOpen));
    });

    // Menyudagi havolaga bosilganda menyuni yopish
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.add('hidden');
        hamburgerBtn.classList.remove('is-open');
        hamburgerBtn.setAttribute('aria-expanded', 'false');
      });
    });

    // Ekran kengaytirilganda (lg breakpoint) mobil menyuni avtomatik yopish
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 1024 && !mobileMenu.classList.contains('hidden')) {
        mobileMenu.classList.add('hidden');
        hamburgerBtn.classList.remove('is-open');
      }
    });
  }

  // ---------- Xabarlar (messages) avtomatik yopilishi ----------
  document.querySelectorAll('[role="alert"]').forEach(function (alertBox) {
    setTimeout(() => {
      alertBox.style.transition = 'opacity 0.5s ease';
      alertBox.style.opacity = '0';
      setTimeout(() => alertBox.remove(), 500);
    }, 6000);
  });

  // ---------- Scroll bilan header soyasi ----------
  const header = document.querySelector('header');
  if (header) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 10) {
        header.classList.add('shadow-md');
      } else {
        header.classList.remove('shadow-md');
      }
    });
  }

  // ---------- Scroll-reveal (elementlar ko'rinishga kirganda yumshoq paydo bo'ladi) ----------
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach((el) => observer.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('is-visible'));
  }

});
