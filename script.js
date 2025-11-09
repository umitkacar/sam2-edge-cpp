// ===== SMOOTH SCROLL FUNCTIONALITY =====
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});

// ===== NAVBAR SCROLL EFFECT =====
let lastScroll = 0;
const navbar = document.querySelector(".navbar");

window.addEventListener("scroll", () => {
  const currentScroll = window.pageYOffset;

  if (currentScroll <= 0) {
    navbar.style.transform = "translateY(0)";
    navbar.style.background = "rgba(15, 23, 42, 0.8)";
    return;
  }

  if (currentScroll > lastScroll && currentScroll > 100) {
    // Scrolling down
    navbar.style.transform = "translateY(-100%)";
  } else {
    // Scrolling up
    navbar.style.transform = "translateY(0)";
    navbar.style.background = "rgba(15, 23, 42, 0.95)";
  }

  lastScroll = currentScroll;
});

// ===== INTERSECTION OBSERVER FOR ANIMATIONS =====
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -100px 0px",
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = "1";
      entry.target.style.transform = "translateY(0)";
    }
  });
}, observerOptions);

// Observe all cards and sections
document
  .querySelectorAll(".feature-card, .demo-box, .install-step, .tech-item")
  .forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(20px)";
    el.style.transition = "opacity 0.6s ease, transform 0.6s ease";
    observer.observe(el);
  });

// ===== COPY CODE FUNCTIONALITY =====
function copyCode(button) {
  const codeBlock = button.parentElement;
  const code = codeBlock.querySelector("code").textContent;

  // Create temporary textarea to copy text
  const textarea = document.createElement("textarea");
  textarea.value = code;
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.select();

  try {
    document.execCommand("copy");

    // Visual feedback
    const originalHTML = button.innerHTML;
    button.innerHTML = '<i class="fas fa-check"></i>';
    button.style.background = "linear-gradient(135deg, #10b981, #059669)";

    setTimeout(() => {
      button.innerHTML = originalHTML;
      button.style.background = "";
    }, 2000);
  } catch (err) {
    console.error("Failed to copy:", err);
  }

  document.body.removeChild(textarea);
}

// ===== BUTTON RIPPLE EFFECT =====
document.querySelectorAll(".btn").forEach((button) => {
  button.addEventListener("click", function (e) {
    const ripple = document.createElement("span");
    const rect = this.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    ripple.style.width = ripple.style.height = size + "px";
    ripple.style.left = x + "px";
    ripple.style.top = y + "px";
    ripple.classList.add("ripple");

    this.appendChild(ripple);

    setTimeout(() => {
      ripple.remove();
    }, 600);
  });
});

// ===== ANIMATED COUNTER FOR STATS =====
function animateCounter(element, target, duration = 2000) {
  let start = 0;
  const increment = target / (duration / 16);

  const timer = setInterval(() => {
    start += increment;
    if (start >= target) {
      element.textContent = target;
      clearInterval(timer);
    } else {
      element.textContent = Math.floor(start);
    }
  }, 16);
}

// ===== PARALLAX EFFECT FOR HERO =====
window.addEventListener("scroll", () => {
  const scrolled = window.pageYOffset;
  const heroVisual = document.querySelector(".hero-visual");
  const heroContent = document.querySelector(".hero-content");

  if (heroVisual && heroContent) {
    heroVisual.style.transform = `translateY(${scrolled * 0.3}px)`;
    heroContent.style.transform = `translateY(${scrolled * 0.1}px)`;
  }
});

// ===== MOUSE MOVE EFFECT ON CARDS =====
document.querySelectorAll(".feature-card, .floating-card").forEach((card) => {
  card.addEventListener("mousemove", (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = (y - centerY) / 10;
    const rotateY = (centerX - x) / 10;

    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
  });

  card.addEventListener("mouseleave", () => {
    card.style.transform = "";
  });
});

// ===== TYPING EFFECT FOR HERO TITLE =====
function typeWriter(element, text, speed = 100) {
  let i = 0;
  element.textContent = "";

  function type() {
    if (i < text.length) {
      element.textContent += text.charAt(i);
      i++;
      setTimeout(type, speed);
    }
  }

  type();
}

// ===== CURSOR TRAIL EFFECT =====
const cursorTrail = [];
const trailLength = 20;

document.addEventListener("mousemove", (e) => {
  const trail = document.createElement("div");
  trail.className = "cursor-trail";
  trail.style.cssText = `
        position: fixed;
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        pointer-events: none;
        z-index: 9999;
        opacity: 0.6;
        left: ${e.clientX}px;
        top: ${e.clientY}px;
        transform: translate(-50%, -50%);
        transition: opacity 0.5s ease;
    `;

  document.body.appendChild(trail);
  cursorTrail.push(trail);

  if (cursorTrail.length > trailLength) {
    const oldTrail = cursorTrail.shift();
    oldTrail.style.opacity = "0";
    setTimeout(() => oldTrail.remove(), 500);
  }
});

// ===== DEMO ANIMATION =====
function startDemoAnimation() {
  const demoBoxes = document.querySelectorAll(".demo-box");
  let currentIndex = 0;

  setInterval(() => {
    demoBoxes.forEach((box, index) => {
      if (index === currentIndex) {
        box.style.transform = "scale(1.1)";
        box.style.borderColor = "var(--primary)";
      } else {
        box.style.transform = "";
        box.style.borderColor = "";
      }
    });

    currentIndex = (currentIndex + 1) % demoBoxes.length;
  }, 2000);
}

// ===== RANDOM PARTICLE EFFECT =====
function createParticle() {
  const particle = document.createElement("div");
  particle.className = "particle";
  particle.style.cssText = `
        position: fixed;
        width: 4px;
        height: 4px;
        border-radius: 50%;
        background: var(--primary);
        pointer-events: none;
        z-index: 1;
        opacity: 0;
        left: ${Math.random() * window.innerWidth}px;
        top: ${Math.random() * window.innerHeight}px;
    `;

  document.body.appendChild(particle);

  // Animate particle
  particle.animate(
    [
      { opacity: 0, transform: "scale(0)" },
      { opacity: 1, transform: "scale(1)" },
      { opacity: 0, transform: "scale(0)" },
    ],
    {
      duration: 3000,
      easing: "ease-in-out",
    },
  );

  setTimeout(() => particle.remove(), 3000);
}

// Create particles periodically
setInterval(createParticle, 500);

// ===== LOADING ANIMATION =====
window.addEventListener("load", () => {
  document.body.style.opacity = "0";
  setTimeout(() => {
    document.body.style.transition = "opacity 0.5s ease";
    document.body.style.opacity = "1";
  }, 100);

  // Start demo animation
  startDemoAnimation();
});

// ===== FLOATING CARDS INTERACTION =====
document.querySelectorAll(".floating-card").forEach((card) => {
  card.addEventListener("click", function () {
    this.style.animation = "none";
    setTimeout(() => {
      this.style.animation = "";
    }, 10);

    // Add a bounce effect
    this.animate(
      [
        { transform: "scale(1)" },
        { transform: "scale(1.2)" },
        { transform: "scale(1)" },
      ],
      {
        duration: 300,
        easing: "ease-in-out",
      },
    );
  });
});

// ===== GRADIENT TEXT ANIMATION =====
const gradientText = document.querySelector(".gradient-text");
if (gradientText) {
  let hue = 0;
  setInterval(() => {
    hue = (hue + 1) % 360;
    gradientText.style.filter = `hue-rotate(${hue}deg)`;
  }, 50);
}

// ===== SCROLL PROGRESS INDICATOR =====
const progressBar = document.createElement("div");
progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent));
    z-index: 10000;
    transition: width 0.1s ease;
`;
document.body.appendChild(progressBar);

window.addEventListener("scroll", () => {
  const winScroll =
    document.body.scrollTop || document.documentElement.scrollTop;
  const height =
    document.documentElement.scrollHeight -
    document.documentElement.clientHeight;
  const scrolled = (winScroll / height) * 100;
  progressBar.style.width = scrolled + "%";
});

// ===== MOBILE MENU TOGGLE =====
const createMobileMenu = () => {
  const menuBtn = document.createElement("button");
  menuBtn.innerHTML = '<i class="fas fa-bars"></i>';
  menuBtn.className = "mobile-menu-btn";
  menuBtn.style.cssText = `
        display: none;
        position: fixed;
        top: 1.5rem;
        right: 2rem;
        background: var(--glass);
        border: 1px solid var(--glass-border);
        border-radius: 8px;
        padding: 0.75rem;
        color: var(--light);
        font-size: 1.5rem;
        cursor: pointer;
        z-index: 1001;
        backdrop-filter: blur(20px);
    `;

  if (window.innerWidth <= 768) {
    menuBtn.style.display = "block";
  }

  document.body.appendChild(menuBtn);

  menuBtn.addEventListener("click", () => {
    const navLinks = document.querySelector(".nav-links");
    if (navLinks) {
      navLinks.style.display =
        navLinks.style.display === "flex" ? "none" : "flex";
      navLinks.style.position = "fixed";
      navLinks.style.top = "80px";
      navLinks.style.right = "2rem";
      navLinks.style.flexDirection = "column";
      navLinks.style.background = "rgba(15, 23, 42, 0.95)";
      navLinks.style.padding = "1rem";
      navLinks.style.borderRadius = "12px";
      navLinks.style.border = "1px solid var(--glass-border)";
    }
  });
};

window.addEventListener("resize", createMobileMenu);
createMobileMenu();

// ===== CONSOLE WELCOME MESSAGE =====
console.log(
  "%cEdgeSAM 🚀",
  "font-size: 40px; font-weight: bold; background: linear-gradient(135deg, #6366f1, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;",
);
console.log(
  "%cUltra-Modern AI Segmentation",
  "font-size: 16px; color: #818cf8;",
);
console.log(
  "%cBuilt with ❤️ using C++, ONNX Runtime & OpenCV",
  "font-size: 12px; color: #cbd5e1;",
);

// ===== EASTER EGG: KONAMI CODE =====
let konamiCode = [
  "ArrowUp",
  "ArrowUp",
  "ArrowDown",
  "ArrowDown",
  "ArrowLeft",
  "ArrowRight",
  "ArrowLeft",
  "ArrowRight",
  "b",
  "a",
];
let konamiIndex = 0;

document.addEventListener("keydown", (e) => {
  if (e.key === konamiCode[konamiIndex]) {
    konamiIndex++;
    if (konamiIndex === konamiCode.length) {
      // Activate secret mode
      document.body.style.filter = "hue-rotate(180deg)";
      alert("🎉 Secret mode activated! You found the easter egg!");
      setTimeout(() => {
        document.body.style.filter = "";
      }, 5000);
      konamiIndex = 0;
    }
  } else {
    konamiIndex = 0;
  }
});
