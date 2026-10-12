// =====================================================
// EFEITOS VISUAIS — só aparência, nenhuma lógica do site depende daqui.
// usado no index.html e no central.html (cada bloco checa se o elemento existe).
// fica dentro de uma IIFE pra não colidir com as variáveis globais do script.js/central.js
// =====================================================
(function () {
  const reduzirMovimento = window.matchMedia("(prefers-reduced-motion: reduce)");

  // =====================================================
  // NAVBAR — transparente no topo, vidro ao rolar
  // =====================================================
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

  // =====================================================
  // BRILHO QUE SEGUE O MOUSE NOS CARDS
  // atualiza --mx/--my, que o CSS usa no radial-gradient do ::before/::after.
  // delegação no document: pega também os cards que o central.js cria depois
  // =====================================================
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

  // =====================================================
  // LUZ DO MOUSE — brilho vermelho bem suave seguindo o cursor
  // =====================================================
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

  // =====================================================
  // VÍDEO DO HERO — só no celular
  // o src só é colocado em tela pequena, pra não baixar o vídeo no computador.
  // as fotos do carrossel só somem quando o vídeo de fato começa a tocar.
  // =====================================================
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
    // play() pode ser bloqueado (modo economia de dados etc.) — aí só continuam as fotos
    const tentativa = video.play();
    if (tentativa) tentativa.catch(() => {});
  }

  prepararVideo();
  telaPequena.addEventListener("change", prepararVideo);

  // =====================================================
  // PAINEL — sidebar recolhível no celular
  // =====================================================
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
    // ao escolher uma tela no menu, fecha (o onclick do link continua fazendo a troca de view)
    document.querySelectorAll(".sidebar .nav-item").forEach((item) => {
      item.addEventListener("click", () => definirSidebar(false));
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") definirSidebar(false);
    });
    telaPequena.addEventListener("change", () => definirSidebar(false));
  }

  // =====================================================
  // PAINEL — redesenha o gráfico quando o tema muda,
  // pra ele pegar as cores do tema novo (as cores vêm das variáveis CSS)
  // =====================================================
  if (typeof renderizarGraficoFinanceiro === "function") {
    let claroAntes = document.body.classList.contains("light-mode");
    new MutationObserver(() => {
      const claro = document.body.classList.contains("light-mode");
      if (claro === claroAntes) return; // outra classe mudou (ex: sidebar abrindo)
      claroAntes = claro;
      if (typeof graficoFinanceiro !== "undefined" && graficoFinanceiro) renderizarGraficoFinanceiro();
    }).observe(document.body, { attributes: true, attributeFilter: ["class"] });
  }
})();
