document.addEventListener('DOMContentLoaded', () => {
  console.log('form-handler.js chargé');
  const form = document.getElementById('form-devenir-membre');
  if (!form) return;

  // --- debug UI (visible) ---
  let debugBox = document.getElementById('fh-debug-box');
  if (!debugBox) {
    debugBox = document.createElement('div');
    debugBox.id = 'fh-debug-box';
    debugBox.style.position = 'fixed';
    debugBox.style.right = '12px';
    debugBox.style.top = '12px';
    debugBox.style.zIndex = '9999';
    debugBox.style.background = 'rgba(255,255,255,0.98)';
    debugBox.style.border = '1px solid #e2e8f0';
    debugBox.style.padding = '10px 12px';
    debugBox.style.borderRadius = '8px';
    debugBox.style.boxShadow = '0 6px 20px rgba(2,6,23,0.08)';
    debugBox.style.fontSize = '13px';
    debugBox.style.color = '#0f172a';
    debugBox.innerHTML = `<div style="font-weight:700; margin-bottom:6px">Form handler</div><div id="fh-endpoint" style="font-size:12px;color:#374151;max-width:260px;word-break:break-all"></div><div style="margin-top:8px;display:flex;gap:8px"><button id="fh-test-send" style="background:#0ea5e9;border:none;color:white;padding:6px 8px;border-radius:6px;cursor:pointer">Test send</button><button id="fh-hide" style="background:#f1f5f9;border:none;padding:6px 8px;border-radius:6px;cursor:pointer">Cacher</button></div><div id="fh-last" style="margin-top:8px;font-size:12px;color:#374151"></div>`;
    document.body.appendChild(debugBox);
  }
  const fhEndpointEl = document.getElementById('fh-endpoint');
  const fhLastEl = document.getElementById('fh-last');
  const fhTestBtn = document.getElementById('fh-test-send');
  const fhHideBtn = document.getElementById('fh-hide');

  // show detected endpoint for debugging
  try {
    const detected = (form.dataset.endpoint || form.action || '').trim() || '(aucun)';
    if (fhEndpointEl) fhEndpointEl.textContent = detected;
  } catch (e) { console.error('Erreur en affichage endpoint', e); }

  // surface uncaught errors into the debug box to help diagnosis
  window.addEventListener('error', (ev) => {
    const msg = ev && ev.message ? ev.message : String(ev);
    if (fhLastEl) fhLastEl.textContent = `Erreur JS: ${msg}`;
    console.error('Global error captured by form-handler debug:', ev);
  });

  // use explicit button click to avoid native form POST
  const submitBtn = document.getElementById('submit-devenir');

  async function sendPayload(payload, endpoint) {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      mode: 'cors'
    });
    const text = await res.text().catch(() => '');
    let json = {};
    try { json = text ? JSON.parse(text) : {}; } catch (e) { json = {}; }
    return { res, text, json };
  }

  // fallback: post via hidden iframe to avoid CORS blocking for form endpoints
  function postViaIframe(payload, endpoint, onLoadCallback) {
    const iframeName = 'fh-hidden-iframe';
    let iframe = document.getElementById(iframeName);
    if (!iframe) {
      iframe = document.createElement('iframe');
      iframe.style.display = 'none';
      iframe.id = iframeName;
      iframe.name = iframeName;
      document.body.appendChild(iframe);
    }
    // Some Google Apps Script webapps only implement doGet and return 501 on POST.
    // Use GET (query string) for script.google.com endpoints to avoid 501.
    if (/script\.google\.com/.test(endpoint)) {
      const params = new URLSearchParams();
      for (const k in payload) params.append(k, payload[k]);
      const sep = endpoint.includes('?') ? '&' : '?';
      // attach a one-time load listener to confirm the submission
      if (onLoadCallback && typeof onLoadCallback === 'function') {
        const handler = () => {
          try {
            console.log('fh-hidden-iframe loaded for endpoint', endpoint, 'params', params.toString());
            onLoadCallback();
          } catch (e) { console.error(e); }
          finally { iframe.removeEventListener('load', handler); }
        };
        iframe.addEventListener('load', handler);
      }
      iframe.src = endpoint + sep + params.toString();
      return;
    }

    const f = document.createElement('form');
    f.method = 'POST';
    f.action = endpoint;
    f.target = iframeName;
    f.style.display = 'none';

    for (const k in payload) {
      const inp = document.createElement('input');
      inp.type = 'hidden';
      inp.name = k;
      inp.value = payload[k];
      f.appendChild(inp);
    }

    // attach load listener if provided
    if (onLoadCallback && typeof onLoadCallback === 'function') {
      const handler = () => {
        try {
          console.log('fh-hidden-iframe loaded for endpoint', endpoint);
          onLoadCallback();
        } catch (e) { console.error(e); }
        finally { iframe.removeEventListener('load', handler); }
      };
      iframe.addEventListener('load', handler);
    }

    document.body.appendChild(f);
    f.submit();
    // cleanup
    setTimeout(() => { document.body.removeChild(f); }, 1500);
  }

  const handleSubmit = async (e) => {
    if (e && e.preventDefault) e.preventDefault();

    // Prevent submission when required fields are empty
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const endpoint = (form.dataset.endpoint || form.action || '').trim();

    // collect form data into an object
    const fd = new FormData(form);
    const payload = {};
    for (const [k, v] of fd.entries()) payload[k] = v;

    // ensure message container exists
    let msg = form.querySelector('.form-message');
    if (!msg) {
      msg = document.createElement('div');
      msg.className = 'form-message';
      msg.style.marginTop = '20px';
      msg.style.padding = '14px';
      msg.style.borderRadius = '8px';
      msg.style.display = 'none';
      msg.style.fontWeight = '600';
      form.appendChild(msg);
    }

    // helper to show messages
    function showMessage(text, type = 'success') {
      msg.textContent = text;
      msg.style.display = 'block';
      if (type === 'success') {
        msg.style.background = '#ecfdf5';
        msg.style.color = '#065f46';
        msg.style.border = '1px solid #10b981';
      } else if (type === 'error') {
        msg.style.background = '#fff1f2';
        msg.style.color = '#991b1b';
        msg.style.border = '1px solid #ef4444';
      } else {
        // neutral / in-progress style made more visible
        msg.style.background = '#e6f0ff';
        msg.style.color = '#1e3a8a';
        msg.style.border = '1px solid #93c5fd';
      }
    }

    if (!endpoint) { 
      showMessage('Point de terminaison non configuré.', 'error'); 
      return; 
    } 

    try {
      console.log('Début envoi vers', endpoint, payload);
      if (submitBtn) submitBtn.disabled = true;
      showMessage('Envoi en cours...', 'neutral');

      // If endpoint looks like Google Apps Script (common CORS issues), use iframe fallback
      if (/script\.google\.com/.test(endpoint)) {
        postViaIframe(payload, endpoint, () => {
          showMessage('Votre candidature sera examinée par le bureau du mouvement. Vous recevrez une confirmation par email et serez contacté dans les 48 heures pour finaliser votre adhésion.', 'success');
          try { form.reset(); } catch (e) {}
          if (submitBtn) submitBtn.disabled = false;
        });
        return;
      }

      const { res, json } = await sendPayload(payload, endpoint);
      if (!res.ok || (json && json.success === false)) {
        const errMsg = (json && json.error) ? json.error : (`HTTP ${res.status}`);
        throw new Error(errMsg);
      }

      showMessage('Votre candidature sera examinée par le bureau du mouvement. Vous recevrez une confirmation par email et serez contacté dans les 48 heures pour finaliser votre adhésion.', 'success');
      form.reset();
      if (submitBtn) submitBtn.disabled = false;
    } catch (err) {
      console.error('Envoi du formulaire échoué', err);
      showMessage("Erreur d'envoi — cliquez pour réessayer.", 'error'); 
      if (submitBtn) submitBtn.disabled = false; 
      msg.style.cursor = 'pointer'; 

      const tryAgain = async () => {
        msg.style.cursor = '';
        msg.removeEventListener('click', tryAgain);
        showMessage('Réessai en cours...', 'neutral');
        try {
          const { res, json } = await sendPayload(payload, endpoint);
          if (!res.ok || (json && json.success === false)) throw new Error((json && json.error) ? json.error : (`HTTP ${res.status}`));
          showMessage('Votre candidature sera examinée par le bureau du mouvement. Vous recevrez une confirmation par email et serez contacté dans les 48 heures pour finaliser votre adhésion.', 'success');
          form.reset();
          if (submitBtn) submitBtn.disabled = false;
        } catch (e2) {
          console.error('Retry failed', e2);
          showMessage('Toujours une erreur. Veuillez réessayer plus tard.', 'error');
        }
      };

      msg.addEventListener('click', tryAgain);
    }
  };

  // Attach handler to both the explicit submit button and the form submit event
  if (submitBtn) submitBtn.addEventListener('click', handleSubmit);
  form.addEventListener('submit', (e) => { if (e && e.preventDefault) e.preventDefault(); handleSubmit(e); });
});
