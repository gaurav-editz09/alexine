/* =========================================================
   EMBER & SPICE — 3D atmosphere
   Two real Three.js particle fields:
   1. a close, slow field over the hero photograph
   2. a deep, scroll-driven field behind the dark sections
   Both fail silently. Reduced-motion users get the still page.
   ========================================================= */

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = window.matchMedia('(pointer: fine)').matches;
const heroCanvas = document.getElementById('embers');
const sceneCanvas = document.getElementById('scene-canvas');

if (heroCanvas && !reduceMotion && window.innerWidth >= 900 && finePointer) {
  initHeroField(heroCanvas).catch(function () {});
}

if (sceneCanvas && !reduceMotion && window.innerWidth >= 480) {
  initScrollField(sceneCanvas).catch(function () {});
}

/* ---------- shared helpers ---------- */

function makeEmberTexture(THREE) {
  const size = 128;
  const c = document.createElement('canvas');
  c.width = size;
  c.height = size;
  const ctx = c.getContext('2d');
  const gradient = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
  gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
  gradient.addColorStop(0.2, 'rgba(255, 244, 224, 0.94)');
  gradient.addColorStop(0.52, 'rgba(255, 206, 146, 0.3)');
  gradient.addColorStop(1, 'rgba(255, 168, 88, 0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, size, size);
  const texture = new THREE.CanvasTexture(c);
  texture.colorSpace = THREE.SRGBColorSpace;
  return texture;
}

function makeEmberMaterial(THREE, sprite) {
  return new THREE.ShaderMaterial({
    uniforms: {
      uMap: { value: sprite },
      uSizeScale: { value: 300 }
    },
    vertexShader: [
      'attribute vec3 aColor;',
      'attribute float aSize;',
      'attribute float aAlpha;',
      'uniform float uSizeScale;',
      'varying vec3 vColor;',
      'varying float vAlpha;',
      'void main() {',
      '  vec4 mv = modelViewMatrix * vec4(position, 1.0);',
      '  gl_PointSize = aSize * uSizeScale / max(0.6, -mv.z);',
      '  gl_Position = projectionMatrix * mv;',
      '  vColor = aColor;',
      '  vAlpha = aAlpha;',
      '}'
    ].join('\n'),
    fragmentShader: [
      'uniform sampler2D uMap;',
      'varying vec3 vColor;',
      'varying float vAlpha;',
      'void main() {',
      '  float mask = texture2D(uMap, gl_PointCoord).a;',
      '  float a = mask * vAlpha;',
      '  if (a < 0.004) discard;',
      '  gl_FragColor = vec4(vColor * a, a);',
      '}'
    ].join('\n'),
    transparent: true,
    depthWrite: false,
    depthTest: true,
    blending: THREE.CustomBlending,
    blendEquation: THREE.AddEquation,
    blendSrc: THREE.OneFactor,
    blendDst: THREE.OneFactor
  });
}

function emberColor(THREE, pale) {
  const hue = pale ? 0.075 + Math.random() * 0.02 : 0.035 + Math.random() * 0.055;
  const sat = pale ? 0.34 + Math.random() * 0.2 : 0.82 + Math.random() * 0.16;
  const light = pale ? 0.72 + Math.random() * 0.14 : 0.48 + Math.random() * 0.2;
  return new THREE.Color().setHSL(hue, sat, light);
}

/* ---------- 1. hero field (over the photograph) ---------- */

async function initHeroField(canvas) {
  const THREE = await import('./vendor/three.module.min.js');
  const hero = canvas.closest('.hero');
  if (!hero) return;

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      alpha: true,
      antialias: false,
      powerPreference: 'low-power'
    });
  } catch (error) {
    return;
  }

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 30);
  camera.position.set(0, 0, 6.5);

  const dpr = Math.min(window.devicePixelRatio || 1, 1.75);
  renderer.setPixelRatio(dpr);
  renderer.setClearColor(0x000000, 0);
  renderer.outputColorSpace = THREE.LinearSRGBColorSpace;

  const sprite = makeEmberTexture(THREE);
  const COUNT = 110;
  const positions = new Float32Array(COUNT * 3);
  const colors = new Float32Array(COUNT * 3);
  const sizes = new Float32Array(COUNT);
  const alphas = new Float32Array(COUNT);
  const particles = [];
  const halfFov = Math.tan((camera.fov * Math.PI) / 360);

  function resetParticle(p, initial) {
    const z = -3.6 + Math.random() * 5.2;
    const depth = camera.position.z - z;
    const halfH = halfFov * depth;
    const halfW = halfH * camera.aspect;

    p.x = (Math.random() - 0.5) * halfW * 2;
    p.y = initial
      ? (Math.random() - 0.5) * halfH * 2
      : -halfH - Math.random() * 0.8;
    p.z = z;
    p.vy = 0.1 + Math.random() * 0.22;
    p.drift = 0.06 + Math.random() * 0.2;
    p.phase = Math.random() * Math.PI * 2;
    p.twinkle = 0.6 + Math.random() * 1.8;
    p.size = 0.035 + Math.random() * 0.085;
    p.alpha = 0.26 + Math.random() * 0.6;
    const color = emberColor(THREE, Math.random() > 0.86);
    p.r = color.r;
    p.g = color.g;
    p.b = color.b;
  }

  for (let i = 0; i < COUNT; i += 1) {
    const p = {
      x: 0, y: 0, z: 0, vy: 0, drift: 0, phase: 0,
      twinkle: 1, size: 0.05, alpha: 0.5,
      r: 1, g: 0.6, b: 0.3
    };
    resetParticle(p, true);
    particles.push(p);
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('aColor', new THREE.BufferAttribute(colors, 3));
  geometry.setAttribute('aSize', new THREE.BufferAttribute(sizes, 1));
  geometry.setAttribute('aAlpha', new THREE.BufferAttribute(alphas, 1));

  const material = makeEmberMaterial(THREE, sprite);
  const points = new THREE.Points(geometry, material);
  points.frustumCulled = false;
  scene.add(points);

  function measure() {
    const width = canvas.clientWidth || 1;
    const height = canvas.clientHeight || 1;
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    material.uniforms.uSizeScale.value = renderer.domElement.height / 2;
  }

  measure();

  const target = { x: 0, y: 0 };
  const current = { x: 0, y: 0 };

  hero.addEventListener('pointermove', function (event) {
    const rect = hero.getBoundingClientRect();
    target.x = ((event.clientX - rect.left) / rect.width - 0.5) * 2;
    target.y = ((event.clientY - rect.top) / rect.height - 0.5) * 2;
  }, { passive: true });

  hero.addEventListener('pointerleave', function () {
    target.x = 0;
    target.y = 0;
  });

  let inView = true;
  let running = false;
  let raf = 0;
  let last = 0;
  let elapsed = 0;

  function frame(now) {
    if (!running) return;
    raf = window.requestAnimationFrame(frame);

    if (!last) last = now;
    const dt = Math.min((now - last) / 1000, 0.05);
    last = now;
    elapsed += dt;

    current.x += (target.x - current.x) * 0.045;
    current.y += (target.y - current.y) * 0.045;
    camera.position.x = current.x * 0.34;
    camera.position.y = -current.y * 0.24;
    camera.lookAt(0, 0, 0);

    for (let i = 0; i < COUNT; i += 1) {
      const p = particles[i];
      p.y += p.vy * dt;
      p.x += Math.sin(elapsed * p.twinkle + p.phase) * p.drift * dt;

      const depth = camera.position.z - p.z;
      const halfH = halfFov * depth;
      const halfW = halfH * camera.aspect;

      if (p.y > halfH + 0.6) resetParticle(p, false);

      const edge = Math.min(
        1,
        Math.max(0, (p.y + halfH) / (halfH * 0.55)),
        Math.max(0, (halfH - p.y) / (halfH * 0.55))
      );
      const flicker = 0.62 + 0.38 * Math.sin(elapsed * p.twinkle * 1.6 + p.phase);

      positions[i * 3] = p.x;
      positions[i * 3 + 1] = p.y;
      positions[i * 3 + 2] = p.z;
      colors[i * 3] = p.r;
      colors[i * 3 + 1] = p.g;
      colors[i * 3 + 2] = p.b;
      sizes[i] = p.size;
      alphas[i] = p.alpha * edge * flicker;
    }

    geometry.attributes.position.needsUpdate = true;
    geometry.attributes.aColor.needsUpdate = true;
    geometry.attributes.aSize.needsUpdate = true;
    geometry.attributes.aAlpha.needsUpdate = true;

    renderer.render(scene, camera);
  }

  function start() {
    if (running || !inView || document.hidden) return;
    running = true;
    last = 0;
    raf = window.requestAnimationFrame(frame);
    canvas.classList.add('is-ready');
  }

  function stop() {
    running = false;
    if (raf) window.cancelAnimationFrame(raf);
    raf = 0;
  }

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        inView = entry.isIntersecting;
        if (inView) start();
        else stop();
      });
    }, { rootMargin: '80px 0px', threshold: 0 }).observe(hero);
  } else {
    start();
  }

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) stop();
    else start();
  });

  let resizeTimer = 0;
  window.addEventListener('resize', function () {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(measure, 140);
  }, { passive: true });

  canvas.addEventListener('webglcontextlost', function (event) {
    event.preventDefault();
    stop();
    canvas.classList.remove('is-ready');
  });

  renderer.render(scene, camera);
}

/* ---------- 2. scroll field (behind the dark sections) ---------- */

async function initScrollField(canvas) {
  const THREE = await import('./vendor/three.module.min.js');

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      alpha: true,
      antialias: false,
      powerPreference: 'low-power'
    });
  } catch (error) {
    return;
  }

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(55, 1, 0.1, 60);
  camera.position.set(0, 0, 9);

  const mobile = window.innerWidth < 900;
  const dpr = Math.min(window.devicePixelRatio || 1, mobile ? 1.5 : 1.75);
  renderer.setPixelRatio(dpr);
  renderer.setClearColor(0x000000, 0);
  renderer.outputColorSpace = THREE.LinearSRGBColorSpace;

  const sprite = makeEmberTexture(THREE);
  const COUNT = mobile ? 260 : 620;
  const positions = new Float32Array(COUNT * 3);
  const colors = new Float32Array(COUNT * 3);
  const sizes = new Float32Array(COUNT);
  const alphas = new Float32Array(COUNT);
  const particles = [];
  const halfFov = Math.tan((camera.fov * Math.PI) / 360);

  function resetParticle(p, initial) {
    p.z = -24 + Math.random() * 27;
    const depth = camera.position.z - p.z;
    const halfH = halfFov * depth;
    const halfW = halfH * camera.aspect;

    p.x = (Math.random() - 0.5) * halfW * 2.2;
    p.y = initial
      ? (Math.random() - 0.5) * halfH * 2.2
      : camera.position.y - halfH - Math.random() * 2;
    p.vy = 0.05 + Math.random() * 0.2;
    p.drift = 0.04 + Math.random() * 0.16;
    p.phase = Math.random() * Math.PI * 2;
    p.twinkle = 0.4 + Math.random() * 1.4;
    p.size = 0.055 + Math.random() * 0.11;
    p.alpha = 0.12 + Math.random() * 0.34;
    const color = emberColor(THREE, Math.random() > 0.8);
    p.r = color.r;
    p.g = color.g;
    p.b = color.b;
  }

  for (let i = 0; i < COUNT; i += 1) {
    const p = {
      x: 0, y: 0, z: 0, vy: 0, drift: 0, phase: 0,
      twinkle: 1, size: 0.08, alpha: 0.3,
      r: 1, g: 0.6, b: 0.3
    };
    resetParticle(p, true);
    particles.push(p);
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('aColor', new THREE.BufferAttribute(colors, 3));
  geometry.setAttribute('aSize', new THREE.BufferAttribute(sizes, 1));
  geometry.setAttribute('aAlpha', new THREE.BufferAttribute(alphas, 1));

  const material = makeEmberMaterial(THREE, sprite);
  const points = new THREE.Points(geometry, material);
  points.frustumCulled = false;
  scene.add(points);

  /* One very soft heat bloom, far behind the particles. */
  const glow = (function () {
    const c = document.createElement('canvas');
    c.width = 256;
    c.height = 256;
    const ctx = c.getContext('2d');
    const g = ctx.createRadialGradient(128, 128, 0, 128, 128, 128);
    g.addColorStop(0, 'rgba(255, 176, 96, 0.34)');
    g.addColorStop(0.45, 'rgba(201, 138, 86, 0.11)');
    g.addColorStop(1, 'rgba(201, 138, 86, 0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 256, 256);
    const texture = new THREE.CanvasTexture(c);
    texture.colorSpace = THREE.SRGBColorSpace;
    const mat = new THREE.SpriteMaterial({
      map: texture,
      transparent: true,
      depthWrite: false,
      depthTest: false,
      blending: THREE.AdditiveBlending,
      opacity: 0.55
    });
    const s = new THREE.Sprite(mat);
    s.scale.set(26, 26, 1);
    s.position.set(3, 0, -20);
    scene.add(s);
    return s;
  })();

  function measure() {
    const width = window.innerWidth;
    const height = window.innerHeight;
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    material.uniforms.uSizeScale.value = renderer.domElement.height / 2;
  }

  measure();

  /* Pointer parallax. */
  const pointer = { x: 0, y: 0 };
  const smooth = { x: 0, y: 0, scroll: 0, roll: 0 };

  if (finePointer) {
    window.addEventListener('pointermove', function (event) {
      pointer.x = (event.clientX / window.innerWidth - 0.5) * 2;
      pointer.y = (event.clientY / window.innerHeight - 0.5) * 2;
    }, { passive: true });
  }

  function progress() {
    const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    return Math.min(1, Math.max(0, window.scrollY / max));
  }

  let targetScroll = progress();
  window.addEventListener('scroll', function () {
    targetScroll = progress();
  }, { passive: true });

  /* Pause while the opaque cream menu fills the screen. */
  const menu = document.getElementById('menu');
  let covered = false;
  let coverTicking = false;

  function checkCover() {
    coverTicking = false;
    if (!menu) return;
    const r = menu.getBoundingClientRect();
    covered = r.top <= 1 && r.bottom >= window.innerHeight - 1;
    if (covered) stop();
    else start();
  }

  if (menu) {
    window.addEventListener('scroll', function () {
      if (coverTicking) return;
      coverTicking = true;
      window.requestAnimationFrame(checkCover);
    }, { passive: true });
  }

  let running = false;
  let raf = 0;
  let last = 0;
  let elapsed = 0;

  function frame(now) {
    if (!running) return;
    raf = window.requestAnimationFrame(frame);

    if (!last) last = now;
    const dt = Math.min((now - last) / 1000, 0.05);
    last = now;
    elapsed += dt;

    smooth.scroll += (targetScroll - smooth.scroll) * 0.055;
    smooth.x += (pointer.x - smooth.x) * 0.04;
    smooth.y += (pointer.y - smooth.y) * 0.04;
    smooth.roll += (targetScroll * 0.055 - smooth.roll) * 0.05;

    const camY = smooth.scroll * 13;
    camera.position.set(smooth.x * 0.55, camY - smooth.y * 0.35, 9);
    camera.rotation.set(0, 0, smooth.roll);

    glow.position.y = camY - 1;
    glow.position.x = 3 + smooth.x * 0.8;
    glow.material.opacity = 0.4 + 0.14 * Math.sin(elapsed * 0.22);

    for (let i = 0; i < COUNT; i += 1) {
      const p = particles[i];
      p.y += p.vy * dt;
      p.x += Math.sin(elapsed * p.twinkle * 0.5 + p.phase) * p.drift * dt;

      const depth = camera.position.z - p.z;
      const halfH = halfFov * depth;
      const halfW = halfH * camera.aspect;

      /* Recycle relative to the moving camera so the field is endless. */
      if (p.y - camera.position.y > halfH + 2) p.y -= halfH * 2 + 4;
      if (p.y - camera.position.y < -halfH - 2) p.y += halfH * 2 + 4;
      if (p.x - camera.position.x > halfW + 2) p.x -= halfW * 2 + 4;
      if (p.x - camera.position.x < -halfW - 2) p.x += halfW * 2 + 4;

      const relY = p.y - camera.position.y;
      const edge = Math.min(
        1,
        Math.max(0, (relY + halfH) / (halfH * 0.6)),
        Math.max(0, (halfH - relY) / (halfH * 0.6))
      );
      const flicker = 0.58 + 0.42 * Math.sin(elapsed * p.twinkle + p.phase);

      positions[i * 3] = p.x;
      positions[i * 3 + 1] = p.y;
      positions[i * 3 + 2] = p.z;
      colors[i * 3] = p.r;
      colors[i * 3 + 1] = p.g;
      colors[i * 3 + 2] = p.b;
      sizes[i] = p.size;
      alphas[i] = p.alpha * edge * flicker;
    }

    geometry.attributes.position.needsUpdate = true;
    geometry.attributes.aColor.needsUpdate = true;
    geometry.attributes.aSize.needsUpdate = true;
    geometry.attributes.aAlpha.needsUpdate = true;

    renderer.render(scene, camera);
  }

  function start() {
    if (running || covered || document.hidden) return;
    running = true;
    last = 0;
    raf = window.requestAnimationFrame(frame);
    canvas.classList.add('is-ready');
  }

  function stop() {
    running = false;
    if (raf) window.cancelAnimationFrame(raf);
    raf = 0;
  }

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) stop();
    else start();
  });

  let resizeTimer = 0;
  window.addEventListener('resize', function () {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(function () {
      measure();
      targetScroll = progress();
      checkCover();
    }, 140);
  }, { passive: true });

  canvas.addEventListener('webglcontextlost', function (event) {
    event.preventDefault();
    stop();
    canvas.classList.remove('is-ready');
  });

  renderer.render(scene, camera);
  checkCover();
  start();
}
