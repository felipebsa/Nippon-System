// efeitos visuais do site e do painel (cada parte checa se o elemento existe na página)
(function () {
  const reduzirMovimento = window.matchMedia("(prefers-reduced-motion: reduce)");

  // navbar vira vidro ao rolar
  const navbar = document.querySelector(".navbar");

  function atualizarNavbar() {
    const rolou = window.scrollY > 24;
    navbar.classList.toggle("navbar--rolada", rolou);
    document.body.classList.toggle("pagina-rolada", rolou); // encolhe o logo flutuante
  }

  if (navbar) {
    window.addEventListener("scroll", atualizarNavbar, { passive: true });
    atualizarNavbar();
  }

  // brilho dos cards seguindo o mouse (no document pra pegar os cards criados depois)
  const temMouse = window.matchMedia("(hover: hover)").matches;
  const CARDS_COM_BRILHO = ".service-card, .contact-card, .escolha-card, .item-card";

  if (temMouse) {
    document.addEventListener("pointermove", (e) => {
      const card = e.target.closest && e.target.closest(CARDS_COM_BRILHO);
      if (!card) return;
      const r = card.getBoundingClientRect();
      card.style.setProperty("--mx", `${e.clientX - r.left}px`);
      card.style.setProperty("--my", `${e.clientY - r.top}px`);
    }, { passive: true });
  }

  // luz do mouse
  if (temMouse) {
    const luz = document.createElement("div");
    luz.className = "cursor-luz";
    luz.setAttribute("aria-hidden", "true");
    document.body.appendChild(luz);

    window.addEventListener("pointermove", (e) => {
      luz.style.setProperty("--cx", `${e.clientX}px`);
      luz.style.setProperty("--cy", `${e.clientY}px`);
      luz.classList.add("ligada");
    }, { passive: true });
    document.documentElement.addEventListener("pointerleave", () => luz.classList.remove("ligada"));
  }

  // vídeo do hero só no celular; as fotos somem quando ele começa a tocar
  const hero = document.querySelector(".hero");
  const video = document.getElementById("hero-video");
  const telaPequena = window.matchMedia("(max-width: 767px)");

  function prepararVideo() {
    if (!hero || !video) return;
    if (!telaPequena.matches || reduzirMovimento.matches) return;

    if (!video.getAttribute("src")) {
      video.addEventListener("playing", () => hero.classList.add("com-video"), { once: true });
      video.src = video.dataset.src;
    }
    // se o navegador bloquear o autoplay, ficam as fotos
    const tentativa = video.play();
    if (tentativa) tentativa.catch(() => {});
  }

  prepararVideo();
  telaPequena.addEventListener("change", prepararVideo);

  // modal só fecha pelo fundo se o mouse foi apertado E solto no fundo
  // (apertar dentro e soltar fora disparava o click no fundo e fechava)
  let apertouNoFundo = false;
  let soltouNoFundo = false;
  const ehFundoDoModal = (el) => el && el.classList && el.classList.contains("modal-overlay");

  document.addEventListener("pointerdown", (e) => { apertouNoFundo = ehFundoDoModal(e.target); }, true);
  document.addEventListener("pointerup", (e) => { soltouNoFundo = ehFundoDoModal(e.target); }, true);
  document.addEventListener("click", (e) => {
    if (ehFundoDoModal(e.target) && !(apertouNoFundo && soltouNoFundo)) {
      e.stopPropagation();
    }
  }, true);

  // painel: sidebar recolhível no celular
  const btnSidebar = document.getElementById("sidebar-toggle");
  const fundoSidebar = document.getElementById("sidebar-fundo");

  function definirSidebar(aberta) {
    document.body.classList.toggle("sidebar-aberta", aberta);
    if (btnSidebar) {
      btnSidebar.setAttribute("aria-expanded", String(aberta));
      btnSidebar.querySelector(".ti").className = aberta ? "ti ti-x" : "ti ti-menu-2";
    }
  }

  if (btnSidebar) {
    btnSidebar.addEventListener("click", () => {
      definirSidebar(!document.body.classList.contains("sidebar-aberta"));
    });
    if (fundoSidebar) fundoSidebar.addEventListener("click", () => definirSidebar(false));
    // fecha ao escolher uma tela
    document.querySelectorAll(".sidebar .nav-item").forEach((item) => {
      item.addEventListener("click", () => definirSidebar(false));
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") definirSidebar(false);
    });
    telaPequena.addEventListener("change", () => definirSidebar(false));
  }

  // painel: redesenha o gráfico quando troca o tema, pra pegar as cores novas
  if (typeof renderizarGraficoFinanceiro === "function") {
    let claroAntes = document.body.classList.contains("light-mode");
    new MutationObserver(() => {
      const claro = document.body.classList.contains("light-mode");
      if (claro === claroAntes) return;
      claroAntes = claro;
      if (typeof graficoFinanceiro !== "undefined" && graficoFinanceiro) renderizarGraficoFinanceiro();
    }).observe(document.body, { attributes: true, attributeFilter: ["class"] });
  }
})();
