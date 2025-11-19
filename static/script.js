/* ============================================================
   script.js — InovaTech v32.0 (Versão Completa Expandida)
   
   FUNCIONALIDADES INCLUÍDAS:
   1. Autenticação e Segurança
   2. Navegação SPA (Single Page Application)
   3. Painel do Aluno (Gráficos, Uploads, Notas)
   4. Painel do Professor (Dashboard, Gestão, Gráficos)
   5. Inteligência Artificial (InoAI) - Com Cronograma Visual
   6. Chatbot com Voz (Acessibilidade)
   7. Melhorias UX: Dark Mode, Notificações, Toast
============================================================ */

(function () {
    // ========================================================
    // 1. HELPERS E UTILITÁRIOS GERAIS
    // ========================================================
    const $ = (sel, root = document) => root.querySelector(sel);
    const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  
    // Formatador de Data (ISO para PT-BR)
    const fmtDate = (iso) => {
        if (!iso) return "-";
        try {
            const d = new Date(iso);
            return Number.isNaN(d.getTime()) 
                ? iso 
                : d.toLocaleDateString("pt-BR", {timeZone: 'UTC'});
        } catch {
            return iso;
        }
    };
  
    // Recupera o usuário logado do LocalStorage
    const getUser = () => {
        try { return JSON.parse(localStorage.getItem("InovaTechUser") || "null"); }
        catch { return null; }
    };
  
    // Verificadores de Tipo de Usuário
    const isAluno = () => {
        const u = getUser();
        return (u && u.role && u.role.toLowerCase() === "aluno");
    };
    
    const isProfessor = () => {
        const u = getUser();
        return (u && u.role && u.role.toLowerCase() === "professor");
    };
  
    // Sistema de Notificação Visual (Toast)
    const showToast = (message) => {
        let toast = $("#toast");
        if (!toast) { 
            toast = document.createElement("div"); 
            toast.id = "toast"; 
            document.body.appendChild(toast);
        }
        toast.textContent = message;
        toast.className = "show";
        setTimeout(() => { toast.className = toast.className.replace("show", ""); }, 3000);
    };
  
    // Guarda de Rotas (Segurança)
    const guardRoute = () => {
        const u = getUser();
        const isLoginPage = document.body.classList.contains("login-body");
        if (!isLoginPage && !u) {
            window.location.replace("/");
        }
    };
  
    // Configuração do Logout
    const setupLogout = () => {
        const btn = $("#logout");
        if (btn) {
            btn.addEventListener("click", (e) => {
                e.preventDefault();
                localStorage.removeItem("InovaTechUser");
                window.location.replace("/");
            });
        }
    };
  
    // ========================================================
    // 2. FUNCIONALIDADES UX (VISUAL)
    // ========================================================
  
    function setupDarkMode() {
        const toggle = $("#toggleDark");
        const body = document.body;
        
        if (localStorage.getItem("darkMode") === "true") {
            body.classList.add("dark-mode");
            if (toggle) toggle.innerHTML = '<i class="fas fa-sun"></i> Modo Claro';
        }
  
        if (toggle) {
            toggle.addEventListener("click", (e) => {
                e.preventDefault();
                body.classList.toggle("dark-mode");
                const isDark = body.classList.contains("dark-mode");
                localStorage.setItem("darkMode", isDark);
                toggle.innerHTML = isDark ? '<i class="fas fa-sun"></i> Modo Claro' : '<i class="fas fa-moon"></i> Modo Escuro';
            });
        }
    }
  
    function setupNotifications() {
        const bell = $("#notifBtn");
        const dropdown = $("#notifDropdown");
        const badge = $(".notification-badge");
        
        if (bell && dropdown) {
            bell.addEventListener("click", (e) => {
                e.preventDefault();
                const isVisible = dropdown.style.display === "block";
                dropdown.style.display = isVisible ? "none" : "block";
                if (!isVisible && badge) badge.style.display = "none";
            });
            document.addEventListener("click", (e) => {
                if (!bell.contains(e.target) && !dropdown.contains(e.target)) {
                    dropdown.style.display = "none";
                }
            });
        }
    }
  
    function setupForgotPassword() {
        const link = $("#linkEsqueciSenha");
        const modal = $("#modalSenha");
        const close = $("#closeModal");
        const btnSend = $("#btnRecuperar");
        const inputEmail = $("#emailRecuperacao");
  
        if (link && modal) {
            link.addEventListener("click", (e) => {
                e.preventDefault();
                modal.style.display = "flex";
                setTimeout(() => modal.classList.add("active"), 10);
            });
            const fechar = () => {
                modal.classList.remove("active");
                setTimeout(() => modal.style.display = "none", 300);
            };
            if (close) close.addEventListener("click", fechar);
            if (btnSend) {
                btnSend.addEventListener("click", () => {
                    if (inputEmail.value.includes("@")) {
                        fechar();
                        showToast(`📧 Link enviado para: ${inputEmail.value}`);
                        inputEmail.value = "";
                    } else { alert("E-mail inválido!"); }
                });
            }
        }
    }
  
    // ========================================================
    // 3. SISTEMA DE NAVEGAÇÃO (SPA)
    // ========================================================
    function setupNavigation() {
        const links = $$(".sidebar-menu a, .dashboard-card");
        const sections = $$(".content-section");
        const title = $("#pageTitle");
  
        if (!sections.length) return;
  
        const titles = {
            "inicio": "Início",
            "minhas-atividades": "Minhas Atividades",
            "minhas-notas": "Minhas Notas",
            "minha-frequencia": "Minha Frequência",
            "calendario": "Calendário Acadêmico",
            "ia-assistente": "Central de Inteligência Artificial",
            "gerenciar-alunos": "Gerenciar Alunos",
            "lancar-notas": "Lançar Notas",
            "lancar-frequencia": "Lançar Frequência",
            "criar-atividade": "Criar Nova Atividade",
            "consultar-entregas": "Consultar Entregas",
            "calendario-professor": "Calendário Acadêmico",
            "relatorio-ia-prof": "Central IA Docente"
        };
  
        const showSection = (id) => {
            sections.forEach((s) => {
                s.style.display = (s.id === id) ? "block" : "none";
            });
            links.forEach((a) => {
                const t = a.getAttribute("data-target");
                if (t) {
                    a.classList.toggle("active", t === id);
                }
            });
            if (title && titles[id]) {
                title.textContent = titles[id];
            }
            // Hooks de Inicialização
            if (id === "calendario") initCalendarioAluno();
            if (id === "calendario-professor") initCalendarioProfessor();
            if (id === "inicio" && isProfessor()) initProfessorChart();
            if (id === "inicio" && isAluno()) initStudentChart();
        };
  
        links.forEach((a) => {
            const t = a.getAttribute("data-target");
            if (!t) return;
            a.addEventListener("click", (e) => {
                e.preventDefault();
                showSection(t);
            });
        });
  
        if ($("#inicio")) showSection("inicio");
    }
  
    // ========================================================
    // 4. MÓDULO ALUNO
    // ========================================================
    
    let studentChart = null;
    function initStudentChart() {
        const ctx = $("#alunoChart");
        if (!ctx || !window.Chart) return;
        if (studentChart) studentChart.destroy();
  
        studentChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Notas', 'Frequência', 'Entregas', 'Participação', 'Pontualidade'],
                datasets: [{
                    label: 'Meu Desempenho',
                    data: [8.5, 9.0, 10.0, 7.5, 9.0],
                    fill: true,
                    backgroundColor: 'rgba(0, 122, 204, 0.2)',
                    borderColor: '#007acc',
                    pointBackgroundColor: '#007acc'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { title: { display: true, text: 'Análise de Competências 360°' }, legend: {display: false} },
                scales: { r: { angleLines: { display: false }, suggestedMin: 0, suggestedMax: 10 } }
            }
        });
    }
  
    function setupAlunoPDF() {
        const btn = $(".btn-pdf");
        if (btn) {
            btn.addEventListener("click", () => {
                alert("🌱 Boletim gerado digitalmente! Você economizou papel.\n\nO arquivo foi enviado para seu e-mail institucional.");
            });
        }
    }
  
    async function loadAtividadesAluno() {
        const u = getUser();
        const wrap = $("#areaAtividadesAluno");
        const proxBox = $("#proximaAtividadeContainer");
        const progressoSpan = $(".progresso-circulo span");
        const circle = $(".progresso-circulo");
        
        if (!u || !wrap) return;
        wrap.innerHTML = "<p>Carregando...</p>";
        
        try {
            const r = await fetch(`/atividades?aluno_id=${u.aluno_id}`);
            const data = await r.json();
            
            if (!data.length) {
                wrap.innerHTML = "<p>Nenhuma atividade.</p>";
                if (proxBox) proxBox.innerHTML = "<p>Sem atividades.</p>";
                return;
            }
            
            const rows = data.map(a => `
                <tr>
                    <td>${a.titulo}</td>
                    <td>${a.disciplina || "-"}</td>
                    <td>${fmtDate(a.data_entrega)}</td>
                    <td>${a.status_envio === "Enviado" ? "<span style='color:green;font-weight:bold'>Enviado</span>" : "Pendente"}</td>
                    <td>${a.status_envio === "Enviado" ? "✅" : `<div id="upload-${a.id}"></div>`}</td>
                </tr>`
            ).join("");
  
            wrap.innerHTML = `<table class="table"><thead><tr><th>Título</th><th>Matéria</th><th>Entrega</th><th>Status</th><th>Ação</th></tr></thead><tbody>${rows}</tbody></table>`;
  
            // Injeta Forms de Upload
            const tpl = $("#uploadTemplate")?.content;
            if (tpl) {
                data.forEach(a => {
                    if (a.status_envio !== "Enviado") {
                        const slot = $(`#upload-${a.id}`);
                        if (slot) {
                            const form = tpl.cloneNode(true);
                            form.querySelector("input[name='atividade_id']").value = a.id;
                            setupUploadForm(form.querySelector("form"));
                            slot.appendChild(form);
                        }
                    }
                });
            }
            if (proxBox) {
                const hoje = new Date().toISOString().split("T")[0];
                const prox = data.filter(a => a.data_entrega >= hoje).sort((a,b) => a.data_entrega.localeCompare(b.data_entrega))[0];
                proxBox.innerHTML = prox 
                    ? `<strong>${prox.titulo}</strong><br>${fmtDate(prox.data_entrega)}<br><span style='font-size:0.8em;color:#666'>${prox.disciplina}</span>` 
                    : "Tudo em dia! 🎉";
            }
            if (progressoSpan && circle) {
                const total = data.length;
                const env = data.filter(a => a.status_envio === "Enviado").length;
                const perc = total ? Math.round((env/total)*100) : 0;
                progressoSpan.textContent = `${perc}%`;
                circle.style.background = `conic-gradient(#007acc ${perc * 3.6}deg, #e6edf5 0deg)`;
            }
        } catch (e) { console.error(e); wrap.innerHTML = "Erro ao carregar."; }
    }
  
    function setupUploadForm(form) {
        if (!form) return;
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const u = getUser();
            const fd = new FormData(form);
            fd.append("aluno_id", u.aluno_id);
            const msg = form.querySelector(".msg");
            msg.textContent = "Enviando...";
            try {
                const r = await fetch("/upload", { method: "POST", body: fd });
                const d = await r.json();
                if (d.success) { 
                    msg.textContent = "✅ Sucesso!"; 
                    showToast("Atividade entregue!"); 
                    setTimeout(loadAtividadesAluno, 1000); 
                } else { throw new Error(d.message); }
            } catch (err) { msg.textContent = "Erro"; }
        });
    }
  
    async function loadNotasAluno() {
        const u = getUser();
        const wrap = $("#areaNotasAluno");
        if (!u || !wrap) return;
        try {
            const r = await fetch(`/notas/aluno/${u.aluno_id}`);
            const d = await r.json();
            wrap.innerHTML = d.length ? `<table class="table"><thead><tr><th>Disciplina</th><th>Nota</th><th>Data</th></tr></thead><tbody>${d.map(n => `<tr><td>${n.disciplina}</td><td>${n.nota}</td><td>${fmtDate(n.data)}</td></tr>`).join("")}</tbody></table>` : "<p>Nenhuma nota lançada.</p>";
        } catch { wrap.innerHTML = "Erro."; }
    }
  
    async function loadFrequenciaAluno() {
        const u = getUser();
        const wrap = $("#areaFrequenciaAluno");
        if (!u || !wrap) return;
        try {
            const r = await fetch(`/frequencia/aluno/${u.aluno_id}`);
            const d = await r.json();
            wrap.innerHTML = d.length ? `<table class="table"><thead><tr><th>Data</th><th>Disciplina</th><th>Status</th></tr></thead><tbody>${d.map(f => `<tr><td>${fmtDate(f.data_aula)}</td><td>${f.disciplina}</td><td>${f.status}</td></tr>`).join("")}</tbody></table>` : "<p>Sem frequência.</p>";
        } catch { wrap.innerHTML = "Erro."; }
    }
  
    // ========================================================
    // 5. CENTRAL IA ALUNO (COM CRONOGRAMA VISUAL)
    // ========================================================
    function setupCentralIAAluno() {
        const u = getUser();
        if (!u) return;
        
        const btnRisco = $("#gerarRelatorio");
        const outRisco = $("#resultadoIA");
        
        if (btnRisco && outRisco) {
            btnRisco.addEventListener("click", async () => {
                outRisco.classList.add("show"); 
                outRisco.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analisando com Machine Learning...';
                try {
                    const r = await fetch(`/ia/risco/aluno/${u.aluno_id}`); 
                    const d = await r.json();
                    outRisco.innerHTML = `
                        <div style="padding:15px; border-left:4px solid #007acc; background:var(--bg-body); border-radius:4px;">
                            <h3 style="color:#007acc; margin-top:0;">${d.nivel}</h3>
                            <p><b>Média Global:</b> ${d.media}</p>
                            <p><b>Total de Faltas:</b> ${d.faltas}</p>
                        </div>`;
                } catch { outRisco.textContent = "Erro IA."; }
            });
        }
  
        async function loadIAContent(type) {
            const resDiv = $("#iaResumo"); 
            const recList = $("#iaRecomendacoes ul"); 
            const cronDiv = $("#cronogramaConteudo");
            
            try {
                const r = await fetch(`/ia/assistente/aluno/${u.aluno_id}`); 
                const d = await r.json();
                
                if (type === "resumo") { 
                    resDiv.classList.add("show"); 
                    resDiv.innerHTML = `<p>${d.resumo}</p><p><b>${d.mensagem}</b></p>`;
                    if (recList) {
                        recList.innerHTML = d.recomendacoes.map(i => `<li>${i}</li>`).join(""); 
                        $("#iaRecomendacoes").classList.add("show");
                    }
                }
                
                // CRONOGRAMA VISUAL (NOVIDADE)
                if (type === "cronograma") {
                    cronDiv.classList.add("show");
                    let html = '<div class="cronograma-grid">';
                    
                    if (d.cronograma && d.cronograma.length) {
                        d.cronograma.forEach(c => {
                            // Cores dinâmicas baseadas na matéria
                            let borderStyle = c.tag_class === 'tag-python' ? 'border-left: 5px solid #ffc107;' : 
                                              c.tag_class === 'tag-redes' ? 'border-left: 5px solid #28a745;' : 
                                              c.tag_class === 'tag-etica' ? 'border-left: 5px solid #dc3545;' : 
                                              'border-left: 5px solid #007acc;';
  
                            html += `
                            <div class="crono-card" style="${borderStyle}">
                                <div class="crono-dia">
                                    ${c.dia} <span class="crono-tag ${c.tag_class || ''}">${c.materia}</span>
                                </div>
                                <div style="font-weight:bold; font-size:0.95em; margin-bottom:5px; color:var(--text-main);">
                                    <i class="fas fa-bullseye" style="color:#f0ad4e"></i> ${c.foco}
                                </div>
                                ${c.tarefas.map(t => `
                                    <div class="crono-tarefa">
                                        <i class="fas fa-check-square" style="color:#ccc"></i> ${t}
                                    </div>
                                `).join('')}
                                <div class="crono-tempo">
                                    <i class="fas fa-stopwatch"></i> Tempo: ${c.tempo}
                                </div>
                            </div>`;
                        });
                    } else {
                        html += '<p>Nenhum cronograma gerado.</p>';
                    }
                    
                    html += '</div>'; // Fecha grid
                    cronDiv.innerHTML = html;
                }
            } catch { console.log("Erro na IA."); }
        }
  
        const btnResumo = $("#btnGerarResumo");
        if (btnResumo) btnResumo.addEventListener("click", () => { 
            $("#iaResumo").textContent = "Gerando resumo..."; 
            loadIAContent("resumo"); 
        });
  
        const btnCron = $("#gerarPlano7");
        if (btnCron) btnCron.addEventListener("click", () => { 
            $("#cronogramaConteudo").textContent = "Montando cronograma..."; 
            loadIAContent("cronograma"); 
        });
    }
  
    // ========================================================
    // 6. MÓDULO PROFESSOR (INTERATIVO)
    // ========================================================
    async function loadDashboardProfessor() {
       $("#totalAlunos").textContent = "3"; 
       $("#totalTurmas").textContent = "1";
       try { 
          const r = await fetch("/atividades"); const d = await r.json(); 
          $("#totalAtividades").textContent = `${d.length}`; 
       } catch { $("#totalAtividades").textContent = "0"; }
    }
  
    let chartProf = null;
    function initProfessorChart() {
        const ctx = $("#turmaChart"); if (!ctx || !window.Chart) return;
        if (chartProf) chartProf.destroy();
        chartProf = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Web', 'Banco de Dados', 'Eng. Software', 'Redes', 'Ética'],
                datasets: [{
                    label: 'Média da Turma',
                    data: [8.5, 7.2, 6.8, 9.0, 7.5],
                    backgroundColor: ['#007acc', '#28a745', '#ffc107', '#17a2b8', '#6610f2'],
                    borderRadius: 5
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, max: 10 } } }
        });
    }
  
    function setupProfessorActions() {
        $$(".btn-save").forEach(btn => {
            btn.addEventListener("click", () => showToast("✅ Dados salvos com sucesso!"));
        });
        const btnPdf = $(".btn-pdf"); 
        if (btnPdf) {
            btnPdf.addEventListener("click", () => {
                alert("📄 Diário de Classe assinado digitalmente e gerado em PDF! \n\n(Economia de papel: 100% 🌳)");
            });
        }
    }
  
    // --- CENTRAL IA DOCENTE (Novidades: Radar + Gerador) ---
    function setupProfessorIA() {
       // 1. Análise Geral
       const btn = $("#gerarRelatorioProfessor");
       const out = $("#resultadoRelatorioProfessor");
       if (btn && out) {
          btn.addEventListener("click", async () => {
             out.classList.add("show"); out.textContent = "Analisando turmas...";
             try {
                const r = await fetch("/ia/relatorio/professor"); const d = await r.json();
                out.innerHTML = `<p><b>Média Global:</b> ${d.media}</p><p><b>Total Faltas:</b> ${d.risco}</p><p><b>Análise:</b> ${d.nivel}</p>`;
             } catch { out.textContent = "Erro."; }
          });
       }
  
       // 2. Radar de Risco (Botão Toggle)
       const btnRadar = $("#btnRadarRisco");
       const listaRisco = $("#listaRisco");
       if (btnRadar && listaRisco) {
           btnRadar.addEventListener("click", () => {
               if (listaRisco.style.display === "block") {
                   listaRisco.style.display = "none";
               } else {
                   listaRisco.style.display = "block";
                   listaRisco.classList.add("show");
               }
           });
       }
  
       // 3. Gerador de Questões (Simulação)
       const btnQuestao = $("#btnGerarQuestao");
       const inputTema = $("#temaQuestao");
       const boxQuestao = $("#resultadoQuestao");
       const textoQuestao = $("#textoQuestao");
  
       if (btnQuestao) {
           btnQuestao.addEventListener("click", () => {
               const tema = inputTema.value.trim();
               if (!tema) { alert("Digite um tema!"); return; }
               
               boxQuestao.style.display = "block";
               textoQuestao.innerHTML = `Gerando questão...`;
               
               // Simula delay da IA
               setTimeout(() => {
                   textoQuestao.innerHTML = `
                      <strong>Questão Sugerida sobre ${tema}:</strong><br><br>
                      "Explique o conceito fundamental de <em>${tema}</em> e dê dois exemplos práticos de aplicação no mercado atual."
                      <br><br><em>(Nível: Intermediário | Tempo: 10 min)</em>
                   `;
               }, 1200);
           });
       }
    }
  
    // ========================================================
    // 7. CALENDÁRIOS
    // ========================================================
    function initCalendarioAluno() { 
        const el = $("#calendarAluno"); 
        if (el && window.FullCalendar) new FullCalendar.Calendar(el, { initialView: 'dayGridMonth', locale: 'pt-br', events: '/api/calendario', eventColor: '#007acc' }).render(); 
    }
    function initCalendarioProfessor() { 
        const el = $("#calendarProfessor"); 
        if (el && window.FullCalendar) new FullCalendar.Calendar(el, { initialView: 'dayGridMonth', locale: 'pt-br', events: '/api/calendario' }).render(); 
    }
  
    // ========================================================
    // 8. CHATBOT GLOBAL (COM VOZ)
    // ========================================================
    function setupChat() {
        const btn = $("#chatBtn"); 
        const win = $("#chatWindow"); 
        const close = $("#closeChat"); 
        const send = $("#chatSend"); 
        const input = $("#chatInput"); 
        const body = $("#chatBody");
        const voiceBtn = $("#toggleVoice");
  
        let isVoiceActive = false;
  
        if (!btn || !win) return;
  
        if (voiceBtn) {
            voiceBtn.addEventListener("click", () => {
                isVoiceActive = !isVoiceActive;
                voiceBtn.className = isVoiceActive ? "fas fa-volume-up" : "fas fa-volume-mute";
                voiceBtn.style.opacity = isVoiceActive ? "1" : "0.5";
                if(isVoiceActive) speak("Voz ativada."); else window.speechSynthesis.cancel();
            });
        }
  
        const speak = (text) => {
            if (!isVoiceActive) return;
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const u = new SpeechSynthesisUtterance(text); 
                u.lang = 'pt-BR'; u.rate = 1.1; 
                window.speechSynthesis.speak(u);
            }
        };
  
        btn.addEventListener("click", () => {
            win.style.display = (win.style.display === "flex") ? "none" : "flex";
            if (win.style.display === "flex") input.focus();
        });
        close.addEventListener("click", () => { win.style.display = "none"; window.speechSynthesis.cancel(); });
  
        const sendMessage = async () => {
            const txt = input.value.trim();
            if (!txt) return;
  
            const user = getUser();
            const alunoId = (user && user.role === 'aluno') ? user.aluno_id : null;
  
            body.innerHTML += `<div class="chat-msg user">${txt}</div>`;
            input.value = ""; 
            body.scrollTop = body.scrollHeight;
  
            const loadingId = "loading-" + Date.now();
            body.innerHTML += `<div id="${loadingId}" class="chat-msg bot">...</div>`;
            body.scrollTop = body.scrollHeight;
  
            try {
                const res = await fetch('/api/chat', { 
                    method: 'POST', 
                    headers: { 'Content-Type': 'application/json' }, 
                    body: JSON.stringify({ message: txt, aluno_id: alunoId }) 
                });
                const data = await res.json();
                document.getElementById(loadingId).remove();
                
                body.innerHTML += `<div class="chat-msg bot">${data.reply}</div>`;
                body.scrollTop = body.scrollHeight;
                
                const textToRead = data.reply.replace(/([\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF])/g, '');
                speak(textToRead);
            } catch { 
                document.getElementById(loadingId).remove(); 
                body.innerHTML += `<div class="chat-msg bot">Erro.</div>`; 
            }
        };
        
        send.addEventListener("click", sendMessage);
        input.addEventListener("keypress", (e) => { if (e.key === "Enter") sendMessage(); });
    }
  
    // ========================================================
    // 9. INICIALIZAÇÃO
    // ========================================================
    document.addEventListener("DOMContentLoaded", () => {
      setupDarkMode(); 
      setupForgotPassword();
      
      if (document.body.classList.contains("login-body")) return;
  
      guardRoute(); 
      setupLogout(); 
      setupNavigation(); 
      setupChat(); 
      setupNotifications();
  
      // INICIALIZAÇÃO CONDICIONAL (ALUNO)
      if (isAluno()) {
         const info = $("#userInfo");
         if(info) info.textContent = `${getUser().name} - Aluno`;
         
         loadAtividadesAluno();
         loadNotasAluno();
         loadFrequenciaAluno();
         setupCentralIAAluno();
         setupAlunoPDF();
         initStudentChart();
      }
      
      // INICIALIZAÇÃO CONDICIONAL (PROFESSOR)
      if (isProfessor()) {
         setupProfessorIA(); // <-- Agora inclui o Radar e Gerador
         loadDashboardProfessor();
         initProfessorChart();
         setupProfessorActions();
         
         const form = $("#formNovaAtividade");
         if(form) {
            form.addEventListener("submit", async e => {
               e.preventDefault();
               const msg = $("#msgAtividade"); 
               msg.textContent = "Salvando...";
               try {
                  const r = await fetch('/atividades', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({
                     titulo: $("#titulo").value, disciplina: $("#disciplina").value, data_entrega: $("#data_entrega").value
                  })});
                  const d = await r.json();
                  if(d.success) { 
                      msg.textContent = "✅ Salvo!"; 
                      form.reset(); 
                      showToast("Atividade publicada com sucesso!"); 
                  } else throw new Error(d.message);
               } catch(err) { msg.textContent = "❌ Erro: " + err.message; }
            });
         }
      }
    });
  })();