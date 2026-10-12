// =====================================================
// EFEITOS VISUAIS — só aparência, nenhuma lógica do site depende daqui.
// fica dentro de uma IIFE pra não colidir com as variáveis globais do script.js
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
  // atualiza --mx/--my, que o CSS usa no radial-gradient do ::before/::after
  // =====================================================
  const temMouse = window.matchMedia("(hover: hover)").matches;

  if (temMouse) {
    document.querySelectorAll(".service-card, .contact-card, .escolha-card").forEach((card) => {
      card.addEventListener("pointermove", (e) => {
        const r = card.getBoundingClientRect();
        card.style.setProperty("--mx", `${e.clientX - r.left}px`);
        card.style.setProperty("--my", `${e.clientY - r.top}px`);
      });
    });
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
})();
