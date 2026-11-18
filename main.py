        <script>
            const urlParams = new URLSearchParams(window.location.search);
            const userPhone = urlParams.get('phone');
            let currentCredits = 50.0;
            function goDashboard() { window.location.href = '/dashboard?phone=' + encodeURIComponent(userPhone || ''); }
            function sendPrompt() {
                const inputField = document.getElementById('user-prompt');
                const promptText = inputField.value.trim();
                const chatContainer = document.getElementById('chat-container');
                if (!promptText) { alert("Veuillez entrer un prompt."); return; }
                if (currentCredits < 5.0) { alert("Crédits insuffisants !"); return; }
                
                currentCredits -= 5.0;
                document.getElementById('user-credits').innerText = currentCredits.toFixed(1);
                
                const userMsg = document.createElement('div');
                userMsg.className = 'message user';
                userMsg.innerText = promptText;
                chatContainer.appendChild(userMsg);
                inputField.value = '';
                chatContainer.scrollTop = chatContainer.scrollHeight;

                // Étape 1 : File d'attente
                setTimeout(() => {
                    const aiMsg = document.createElement('div');
                    aiMsg.className = 'message ai';
                    aiMsg.innerText = "⚡ Synthèse neurale active... Génération des frames cinématiques.";
                    chatContainer.appendChild(aiMsg);
                    chatContainer.scrollTop = chatContainer.scrollHeight;

                    // Étape 2 : Succès instantané du rendu
                    setTimeout(() => {
                        const successMsg = document.createElement('div');
                        successMsg.className = 'message ai';
                        successMsg.innerHTML = "✅ <b>Génération réussie !</b> Votre flux audiovisuel est prêt.<br><span style='color: #00f2fe; cursor: pointer;' onclick='alert(\"Téléchargement du média HD initié...\")'>📥 Télécharger le rendu HD</span>";
                        chatContainer.appendChild(successMsg);
                        chatContainer.scrollTop = chatContainer.scrollHeight;
                    }, 1500);
                }, 800);
            }
        </script>
