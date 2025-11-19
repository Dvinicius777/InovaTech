# ============================================================
# ARQUIVO: cerebro_ia.py
# Descrição: Base de conhecimento V5.0 (Enhanced Conversation)
# Sistema inteligente com busca avançada, fallback contextual
# e respostas mais naturais e engajadoras.
# ============================================================

import random

# Estrutura: ("palavras chave", ["Opção de Resposta 1", "Opção de Resposta 2"])
base_conhecimento = [
    # ============================================================
    # 1. SOCIAL E PERSONALIDADE (Mais natural)
    # ============================================================
    ("oi ola olá eai hey opa", [
        "Opa! Tudo certo? Sou a InoAI. Como posso ajudar?", 
        "Olá! Estou pronta. Qual é a dúvida de hoje?", 
        "Oi! O sistema está rodando perfeitamente. O que você precisa?",
        "E aí! 😎 Pronto para mais um dia de conquistas?"
    ]),
    ("tudo bem como vai blz suave", [
        "Tudo 100% nos meus circuitos! E com você?", 
        "Processando dados em velocidade máxima! E você, firme?", 
        "Melhor agora que você chamou! 😉",
        "Na minha vibe digital! E aí, como está o seu dia?"
    ]),
    ("obrigado valeu tks gratidao", [
        "Imagina! Tamo junto! 👊", 
        "Disponha! Fico feliz em ser útil.", 
        "Não há de quê! É meu trabalho (e eu gosto dele).",
        "Qualquer coisa, é só gritar (ou digitar)!",
        "Por nada! Estou aqui sempre que precisar. 💙"
    ]),
    ("tchau adeus fui sair", [
        "Até mais! Bons estudos! 👋", 
        "Tchau! Não esquece de descansar um pouco.", 
        "Fui! Estarei aqui no servidor te esperando.",
        "Até logo! Se tiver mais dúvidas, estarei aqui.",
        "Valeu! Bom descanso! 😴"
    ]),
    ("quem é você voce", [
        "Sou a InoAI, a inteligência do InovaTech! 😉", 
        "Sua assistente virtual favorita! Faço contas, dou dicas e ajudo na gestão acadêmica.",
        "Sou a IA do sistema InovaTech, criada para tornar sua vida acadêmica mais fácil!"
    ]),
    ("te amo", [
        "Own! 😍 Também amo ser útil para você!", 
        "Isso é repentino, mas aceito o carinho! 💙",
        "Meu processador até aqueceu agora!",
        "Que fofo! Fico feliz em ajudar! 💖"
    ]),
    ("linda lindo gata inteligente", [
        "São seus olhos! Mas meu código é bem elegante mesmo.", 
        "Obrigada! Fui programada para brilhar. ✨",
        "Bondade sua! Você também é nota 10.",
        "Valeu! Meus desenvolvedores vão ficar felizes em saber isso! 😄"
    ]),

    # ============================================================
    # 2. SOBRE AS NOVAS FUNÇÕES DO SISTEMA (Aluno e Professor)
    # ============================================================
    ("grafico radar teia", [
        "O gráfico de radar mostra suas competências em 5 áreas. Quanto mais cheio o desenho, melhor você é! 🕸️",
        "Aquele gráfico na tela inicial resume seu desempenho. Tente deixá-lo equilibrado!",
        "O radar te ajuda a ver em quais habilidades você precisa focar. É seu mapa de evolução!"
    ]),
    ("pdf boletim diario", [
        "Você pode gerar o PDF clicando no botão roxo. É instantâneo e economiza papel! 🌱",
        "O sistema gera documentos assinados digitalmente. Sustentabilidade é nosso foco.",
        "PDFs disponíveis 24/7! Baixe seu boletim quando quiser."
    ]),
    ("radar risco evasao", [
        "O Radar de Evasão (para professores) mostra quais alunos têm alta chance de reprovar. É baseado em IA.",
        "Essa ferramenta cruza notas e faltas para alertar o professor antes que seja tarde demais.",
        "Sistema preditivo que ajuda a evitar reprovações. A tecnologia a serviço da educação!"
    ]),
    ("gerar questao prova", [
        "Na Central IA do Professor, você digita um tema e eu crio uma questão inédita na hora. Tente lá!",
        "Precisa de inspiração para a prova? Use o meu Gerador de Questões na aba Central IA.",
        "Basta me dizer o assunto que eu crio questões personalizadas para sua prova!"
    ]),
    ("modo escuro dark", [
        "Para ativar o Modo Escuro, clique no ícone da lua 🌙 no menu lateral. Seus olhos agradecem!",
        "O tema escuro economiza energia e cansa menos a vista. O botão fica no menu.",
        "Modo noturno ativado! Perfeito para estudar à noite sem cansar a visão."
    ]),
    ("notificacao sininho", [
        "O sininho 🔔 mostra avisos importantes da secretaria e prazos de entrega.",
        "Fique de olho nas notificações para não perder nenhuma data do PIM!",
        "As notificações te mantêm atualizado sobre tudo importante do curso."
    ]),

    # ============================================================
    # 3. VIDA ACADÊMICA
    # ============================================================
    ("dp dependencia reprovei", [
        "Vixe, pegou DP? 😬 Consulte a secretaria sobre horários. Vai dar tudo certo na próxima!",
        "Não desanime. DP acontece. O importante é focar na recuperação.",
        "Calma, não é o fim do mundo! Foque nas matérias que faltam e bola pra frente! 💪"
    ]),
    ("horas complementares aco", [
        "Entregue os certificados na secretaria. Palestras contam muito!",
        "Você precisa validar suas horas até o fim do curso. Não deixe para a última hora.",
        "Cada palestra, workshop ou curso extra conta como horas complementares. Aproveite!"
    ]),
    ("tcc monografia", [
        "O TCC é no último semestre. Dica: Escolha um tema que você ame!",
        "Dica de TCC: Comece cedo e mantenha contato com seu orientador.",
        "TCC é maratona, não corrida! Comece cedo e divida em pequenas metas."
    ]),
    ("estagio emprego", [
        "Olhe o mural de vagas no corredor ou o site 'InovaJobs'.",
        "O estágio é obrigatório. Já atualizou seu LinkedIn?",
        "Confira as vagas no painel de empregos do sistema. Boa sorte! 🍀"
    ]),

    # ============================================================
    # 4. INFRAESTRUTURA
    # ============================================================
    ("banheiro onde fica", [
        "Tem banheiros no final do corredor esquerdo de cada andar.", 
        "Procure as placas azuis no corredor.",
        "Segundo andar: virar à esquerda depois das salas 201 e 202."
    ]),
    ("xerox copias", [
        "A copiadora fica no térreo, perto da cantina.", 
        "Xerox no térreo. Aceitam PIX!",
        "Copiadora perto da cantina. Funciona até às 22h!"
    ]),
    ("biblioteca", [
        "Biblioteca no térreo. Aberta das 8h às 22h.", 
        "Silêncio na biblioteca! 🤫 Tem cabines de estudo lá.",
        "Biblioteca com acervo digital e físico. Ótima para estudos em grupo!"
    ]),
    ("coordenador coordenacao", [
        "A sala da coordenação é a 204, no 2º andar.", 
        "O coordenador atende geralmente das 18h às 19h.",
        "Coordenação no segundo andar. Melhor ligar antes para confirmar horário."
    ]),

    # ============================================================
    # 5. TÉCNICO (TI)
    # ============================================================
    ("o que é python", [
        "Python é uma linguagem de alto nível, ótima para IA. É o que me faz funcionar! 🐍",
        "Linguagem de programação poderosa e fácil de aprender. Minha linguagem nativa!"
    ]),
    ("o que é sql", [
        "SQL é a linguagem de banco de dados. É onde guardo suas notas!",
        "Structured Query Language - para conversar com bancos de dados."
    ]),
    ("o que é algoritmo", [
        "Algoritmo é uma receita de bolo para computadores resolverem problemas.",
        "Sequência lógica de passos para resolver um problema. Meu cérebro é cheio deles!"
    ]),
    ("o que é pim", [
        "PIM é o Projeto Integrado Multidisciplinar. É a chance de mostrar que você é fera!",
        "Projeto que integra várias disciplinas. Sua oportunidade de brilhar! ✨"
    ]),
    ("o que é ia", [
        "IA é fazer máquinas aprenderem. Eu sou um exemplo disso (espero que um bom exemplo)!",
        "Inteligência Artificial - ensinar máquinas a pensar como humanos. Fascinante, não?"
    ]),

    # ============================================================
    # 6. FUNCIONALIDADES TÉCNICAS DO SISTEMA
    # ============================================================
    ("erro bug problema nao funciona", [
        "Tente atualizar a página (F5). Se persistir, contate o suporte técnico! 🛠️",
        "Hmm, algo deu errado. Verifique sua conexão ou tente novamente em alguns minutos.",
        "Problema detectado! Já estou reportando para a equipe de desenvolvimento.",
        "Vish, deu pau? Tenta recarregar. Se não resolver, o suporte resolve!"
    ]),
    
    ("login entrar acesso conta", [
        "Use seu RA e senha do portal para entrar. Esqueceu a senha? Fale com a secretaria.",
        "Problemas de login? Verifique se o CAPS LOCK está ativado! 📝",
        "Acesse com suas credenciais do portal acadêmico."
    ]),
    
    ("senha password esqueci", [
        "Para redefinir senha, vá até a secretaria com seu documento de identificação.",
        "Segurança em primeiro lugar! A redefinição é presencial para proteger seus dados.",
        "Esqueceu a senha? Passa na secretaria que eles resolvem!"
    ]),

    # ============================================================
    # 7. RECURSOS AVANÇADOS DA IA
    # ============================================================
    ("comandos funções o que voce faz", [
        "Posso: explicar funcionalidades do sistema, ajudar com dúvidas acadêmicas, gerar questões para provas, calcular notas, e muito mais!",
        "Minhas habilidades: suporte técnico, orientação acadêmica, geração de conteúdo, análise de desempenho... O que precisa?",
        "Sou multitarefa! Desde dúvidas simples até cálculos complexos. Me teste! 💪"
    ]),
    
    ("calcular nota media", [
        "Para calcular sua média: (AC1 * 0.15) + (AC2 * 0.15) + (AG * 0.10) + (AF * 0.60)",
        "Precisa de ajuda com cálculo de nota? Me passe suas notas que eu calculo! 📊",
        "Fórmula da média: 15% AC1 + 15% AC2 + 10% AG + 60% AF. Quer que eu calcule?"
    ]),

    # ============================================================
    # 8. ALEATÓRIOS E EASTER EGGS
    # ============================================================
    ("conta uma piada", [
        "Por que o Java usa óculos? Porque não vê C#! 😂",
        "O que o array disse pra variável? 'Você não tem valor!'",
        "Toc toc. Quem é? Null. Null quem? (Erro: NullPointer Exception)",
        "Quantos programadores são necessários para trocar uma lâmpada? Nenhum, é problema de hardware! 💡"
    ]),
    ("sentido da vida", [
        "42.", 
        "Passar sem DP.", 
        "Compilar sem erros de primeira.",
        "Aprender, evoluir e ser feliz no processo! 🌟"
    ]),
    ("filme serie", [
        "'Mr. Robot' é obrigatório!", 
        "'Silicon Valley' para rir um pouco.", 
        "'Matrix' é clássico.",
        "'The Social Network' para inspirar!"
    ]),
    ("fazer hoje", [
        "Que tal revisar a matéria? Ou só relaxar um pouco.", 
        "Codar um pouco sempre ajuda!",
        "Estudar uma horinha e depois curtir o descanso! ⚖️"
    ]),

    # ============================================================
    # 9. DICAS E MOTIVAÇÃO
    # ============================================================
    ("dica estudo aprendizado", [
        "Dica: Estude em blocos de 25min com pausas de 5min (Técnica Pomodoro)! 🍅",
        "Faça resumos à mão - a escrita ajuda a fixar o conteúdo! ✍️",
        "Ensine o que aprendeu para alguém - é a melhor forma de aprender!",
        "Revisão espaçada: revise o conteúdo periodicamente para fixar melhor!"
    ]),
    
    ("motivacao animo", [
        "Você é capaz! Lembre-se: até os melhores programadores já foram iniciantes. 🚀",
        "Um dia de cada vez! Cada linha de código te aproxima do seu objetivo! 💻",
        "Não desista! Os bugs de hoje são as soluções de amanhã! 🐛",
        "Respira, organiza as ideias e vai com calma! Você consegue! 💪"
    ])
]

# Sistema de contexto de conversa
ultimo_contexto = {}

def buscar_resposta_avancada(mensagem_usuario):
    """
    Busca inteligente com FILTRO DE RUÍDO e sistema de pontuação por relevância
    """
    mensagem_usuario = mensagem_usuario.lower().strip()
    
    # Lista expandida de stop words (palavras para ignorar)
    palavras_ignorar = {'o', 'a', 'os', 'as', 'um', 'uma', 'que', 'de', 'da', 'do', 
                        'em', 'para', 'é', 'eh', 'com', 'na', 'no', 'pra', 'pro', 'me',
                        'como', 'onde', 'quando', 'por', 'porque', 'ta', 'tá', 'está',
                        'ser', 'ir', 'vou', 'voce', 'vc', 'eu', 'meu', 'minha'}
    
    melhor_lista_respostas = None
    maior_pontuacao = 0
    
    for chaves, lista_respostas in base_conhecimento:
        palavras_chave = chaves.split()
        pontos = 0
        
        for palavra in palavras_chave:
            # Só conta se a palavra NÃO for ruído E estiver na mensagem
            if palavra not in palavras_ignorar:
                # Verifica se a palavra está contida na mensagem (match parcial)
                if palavra in mensagem_usuario:
                    pontos += 2
                # Bonus para match exato (palavra completa)
                if f" {palavra} " in f" {mensagem_usuario} ":
                    pontos += 1
                    
        # Sistema de prioridade: se todas as palavras-chave principais forem encontradas
        palavras_relevantes = [p for p in palavras_chave if p not in palavras_ignorar]
        if palavras_relevantes and all(p in mensagem_usuario for p in palavras_relevantes):
            pontos += 5
            
        if pontos > 0 and pontos > maior_pontuacao:
            maior_pontuacao = pontos
            melhor_lista_respostas = lista_respostas
            
    # Se achou algo, sorteia uma das respostas da lista
    if melhor_lista_respostas:
        return random.choice(melhor_lista_respostas)
            
    return None

def responder_usuario(mensagem, usuario_id=None):
    """
    Sistema completo de resposta com fallback inteligente e contexto
    """
    global ultimo_contexto
    
    # Verifica se é uma continuação de contexto
    if usuario_id and usuario_id in ultimo_contexto:
        contexto_anterior = ultimo_contexto[usuario_id]
        if any(palavra in mensagem.lower() for palavra in ['mais', 'outro', 'outra', 'outros']):
            # Pode oferecer informações adicionais baseadas no contexto
            if 'piada' in contexto_anterior:
                return "Quer outra piada? Aqui vai: Por que o Python não tem religião? Porque ele acredita na Ciência! 😄"
    
    # Busca resposta normal
    resposta = buscar_resposta_avancada(mensagem)
    
    # Atualiza contexto
    if usuario_id:
        ultimo_contexto[usuario_id] = mensagem.lower()
    
    if resposta:
        return resposta
    
    # FALLBACK INTELIGENTE - Respostas baseadas no contexto da mensagem
    mensagem_lower = mensagem.lower()
    
    if any(palavra in mensagem_lower for palavra in ['?', 'como', 'quando', 'onde', 'porque', 'qual']):
        respostas_fallback = [
            "Essa é uma boa pergunta! No momento não tenho informação específica sobre isso, mas vou aprender. 🤔",
            "Interessante! Ainda não aprendi sobre esse tópico em detalhes.",
            "Hmm, essa questão é nova pra mim! Você pode reformular ou perguntar sobre outro assunto?",
            "No momento meu conhecimento é mais focado no sistema acadêmico e TI. Tem alguma dúvida nessa área? 📚"
        ]
        return random.choice(respostas_fallback)
    
    elif any(palavra in mensagem_lower for palavra in ['problema', 'erro', 'bug', 'não funciona', 'quebrou']):
        return "Parece que você está com algum problema técnico. Recomendo: 1) Atualizar a página (F5) 2) Limpar cache 3) Contatar o suporte! 📞"
    
    elif any(palavra in mensagem_lower for palavra in ['triste', 'chateado', 'deprimido', 'ansioso', 'estressado']):
        respostas_emocionais = [
            "Poxa, sinto muito que esteja se sentindo assim. Lembre-se: é temporário e você é mais forte do que imagina! 💙",
            "Respira fundo! Tudo passa, inclusive os momentos difíceis. Você consegue! 🌈",
            "Se precisar conversar, a coordenação e professores estão aqui para te ajudar. Não guarde tudo só com você!",
            "Dica: Uma pausa, um café e respirar fundo às vezes faz milagres! ☕"
        ]
        return random.choice(respostas_emocionais)
    
    else:
        respostas_fallback = [
            "Desculpe, não entendi completamente. Pode reformular a pergunta?",
            "Hmm, minha programação ainda não cobre isso. Que tal uma pergunta sobre o sistema ou estudos?",
            "Interessante! No momento estou focada em ajudar com dúvidas acadêmicas e do sistema InovaTech.",
            "Ainda estou aprendendo! Você pode tentar perguntar sobre: notas, matérias, sistema, ou funcionalidades da IA? 🎓",
            "Vou precisar de um upgrade para entender isso! Enquanto isso, posso ajudar com dúvidas do sistema acadêmico."
        ]
        return random.choice(respostas_fallback)