// Client-side form handler: intercepts submit and POSTs to configured endpoint
(function(){
    function showMessage(form, type, text) {
        let box = form.querySelector('.form-message');
        if (!box) {
            box = document.createElement('div');
            box.className = 'form-message';
            box.style.margin = '12px 0';
            form.prepend(box);
        }
        box.textContent = text;
        box.style.padding = '12px';
        box.style.borderRadius = '8px';
        box.style.fontWeight = '600';
        if (type === 'success') {
            box.style.background = '#e6ffed';
            box.style.color = '#0b6623';
            box.style.border = '1px solid #b7f0c6';
        } else if (type === 'error') {
            box.style.background = '#ffeef0';
            box.style.color = '#8a1f2d';
            box.style.border = '1px solid #f5c6cb';
        } else {
            box.style.background = '#fff7e6';
            box.style.color = '#6a4a00';
            box.style.border = '1px solid #ffe8a8';
        }
    }

    async function handleSubmit(e){
        e.preventDefault();
        const form = e.currentTarget;
        const endpoint = form.dataset.endpoint || form.action || '';
        if (!endpoint) {
            showMessage(form, 'error', 'Aucun endpoint configuré pour l’envoi du formulaire.');
            return;
        }

        const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
        if (submitBtn) { submitBtn.disabled = true; }

        const formData = new FormData(form);

        try {
            const res = await fetch(endpoint, {
                method: 'POST',
                body: formData,
                headers: { 'Accept': 'application/json' }
            });

            if (res.ok) {
                showMessage(form, 'success', 'Merci — votre message a été envoyé.');
                form.reset();
            } else {
                let msg = 'Erreur lors de l’envoi. Réessayez.';
                try { const json = await res.json(); if (json && json.error) msg = json.error; } catch(_){}
                showMessage(form, 'error', msg);
            }
        } catch (err) {
            showMessage(form, 'error', 'Impossible de contacter le serveur. Vérifiez votre connexion.');
        } finally {
            if (submitBtn) { submitBtn.disabled = false; }
        }
    }

    function init() {
        const forms = document.querySelectorAll('form[data-endpoint], form[data-handle="true"]');
        forms.forEach(f => {
            f.addEventListener('submit', handleSubmit);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else { init(); }
})();
