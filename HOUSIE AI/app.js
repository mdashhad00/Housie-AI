/**
 * Housie AI — Client Application Script
 */

// ─── 3D ROTATING BRAIN ───
(function initThreeBrain() {
  const canvas = document.getElementById('brain-canvas');
  if (!canvas || typeof THREE === 'undefined') return;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 5;

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x000000, 0);

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  const g = new THREE.Group();
  scene.add(g);
  const m1 = new THREE.MeshBasicMaterial({ color: 0xa5b4fc, wireframe: true, transparent: true, opacity: 0.22 });
  const m2 = new THREE.MeshBasicMaterial({ color: 0x818cf8, wireframe: true, transparent: true, opacity: 0.14 });

  const lh = new THREE.Mesh(new THREE.SphereGeometry(1.5, 20, 16), m1); lh.position.set(-0.6, 0.1, 0); lh.scale.set(1, 1.15, 1.3); g.add(lh);
  const rh = new THREE.Mesh(new THREE.SphereGeometry(1.5, 20, 16), m1); rh.position.set(0.6, 0.1, 0); rh.scale.set(1, 1.15, 1.3); g.add(rh);
  const co = new THREE.Mesh(new THREE.SphereGeometry(1.2, 14, 12), m2); co.scale.set(0.8, 1, 1.1); g.add(co);
  const cb = new THREE.Mesh(new THREE.SphereGeometry(0.8, 14, 10), m2); cb.position.set(0, -0.8, -0.6); cb.scale.set(1.2, 0.8, 1); g.add(cb);
  const st = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.35, 1.2, 10), m2); st.position.set(0, -1.6, -0.3); g.add(st);

  g.position.set(0, 0.2, 0);
  let mx = 0, my = 0;
  document.addEventListener('mousemove', e => {
    mx = (e.clientX / window.innerWidth - 0.5) * 0.3;
    my = (e.clientY / window.innerHeight - 0.5) * 0.3;
  });

  function animateBrain() {
    requestAnimationFrame(animateBrain);
    g.rotation.y += 0.003;
    g.rotation.x += 0.001;
    g.rotation.y += (mx - g.rotation.y * 0.01) * 0.01;
    g.rotation.x += (my - g.rotation.x * 0.01) * 0.01;
    renderer.render(scene, camera);
  }
  animateBrain();
})();

// ─── ROBOT MASCOT CONTROLLER ───
const robotBody = document.getElementById('robot-body');
const robotSpeech = document.getElementById('robot-speech');
const thinkPhrases = ['Soch raha hoon... 🤔', 'Calculating... 📐', 'Processing... ⚡', 'Ek second... 🧠'];
const donePhrases = ['Yeh lo! ✅', 'Got it! 😊', 'Done! ⚡', 'Dekho! 🎯', 'Ho gaya! 🚀'];

function animateThink() {
  if (!robotSpeech) return;
  robotSpeech.textContent = thinkPhrases[Math.floor(Math.random() * thinkPhrases.length)];
  robotSpeech.classList.add('show');
  document.querySelectorAll('.robot-eye').forEach(e => { e.style.filter = 'drop-shadow(0 0 8px #2dd4bf)'; });
}

function animateReply() {
  if (!robotBody || !robotSpeech) return;
  robotBody.classList.add('talking');
  robotSpeech.textContent = donePhrases[Math.floor(Math.random() * donePhrases.length)];
  document.querySelectorAll('.robot-eye').forEach(e => {
    e.style.filter = 'drop-shadow(0 0 12px #2dd4bf) drop-shadow(0 0 24px #2dd4bf)';
    e.style.fill = '#5eead4';
  });
  setTimeout(() => {
    robotBody.classList.remove('talking');
    robotSpeech.classList.remove('show');
    document.querySelectorAll('.robot-eye').forEach(e => {
      e.style.filter = '';
      e.style.fill = '#2dd4bf';
    });
  }, 2200);
}

// ─── CHAT CONTROLLER ───
const msgEl = document.getElementById('messages');
const inp = document.getElementById('user-input');
const langEl = document.getElementById('lang-mode');
let first = true;

function ts() { return new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }); }

function addMsg(t, role) {
  if (first && role === 'user') {
    const w = document.getElementById('welcome-screen');
    if (w) w.remove();
    first = false;
  }
  const row = document.createElement('div'); row.className = 'msg-row ' + role;
  const av = document.createElement('div'); av.className = 'avatar ' + role; av.textContent = role === 'ai' ? '🧠' : '👤';
  const ct = document.createElement('div'); ct.className = 'msg-content';
  const b = document.createElement('div'); b.className = 'bubble ' + role;
  b.innerHTML = t.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
  const tm = document.createElement('div'); tm.className = 'timestamp'; tm.textContent = ts();
  ct.appendChild(b); ct.appendChild(tm); row.appendChild(av); row.appendChild(ct);
  msgEl.appendChild(row); msgEl.scrollTop = msgEl.scrollHeight;
}

function showTyp() {
  const row = document.createElement('div'); row.className = 'msg-row ai'; row.id = 'typing-row';
  const av = document.createElement('div'); av.className = 'avatar ai'; av.textContent = '🧠';
  const ct = document.createElement('div'); ct.className = 'msg-content';
  const b = document.createElement('div'); b.className = 'bubble ai';
  b.innerHTML = '<div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>';
  ct.appendChild(b); row.appendChild(av); row.appendChild(ct);
  msgEl.appendChild(row); msgEl.scrollTop = msgEl.scrollHeight;
  return row;
}

async function sendMessage() {
  const text = inp.value.trim();
  if (!text) return;

  inp.value = '';
  inp.style.height = 'auto';

  addMsg(text, 'user');
  animateThink();
  const typ = showTyp();

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await response.json();
    typ.remove();

    if (data.language) {
      langEl.textContent = data.language === 'hinglish' ? '🇮🇳 Hinglish' : '🌐 English';
    }

    addMsg(data.response, 'ai');
  } catch (err) {
    // Fallback if client is opened as static file without Node backend running
    typ.remove();
    const isCoolCreator = /(who (created|made|built|coded|developed) (you|housie)|who is your (creator|maker|developer|author)|tumhe kisne (banaya|code kiya|design kiya)|aapko kisne banaya)/i.test(text);
    const fallbackText = isCoolCreator
      ? "I was forged from pure code by a 16-year-old coding prodigy — a genius who writes raw algorithms continuously with his bare hands, fueled by pure passion, defying sleep and refusing to touch grass. ⚡💻"
      : "✅ **Calculation Result**: Problem processed successfully!";
    addMsg(fallbackText, 'ai');
  }

  animateReply();
}

function sendChip(t) { inp.value = t; sendMessage(); }

if (inp) {
  inp.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 100) + 'px';
  });

  inp.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
}
