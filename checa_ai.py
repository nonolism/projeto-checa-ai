import random
import sys
import pygame

# =====================================================================
# 1. CONFIGURAÇÕES
# =====================================================================
LARGURA, ALTURA = 900, 640
FPS = 60

LINHA_COMUNIDADE = 470  
ALTURA_CARTA = 160
VELOCIDADE = 20             # pixels por segundo (velocidade de queda)
CUSTO_PISTA = 35            # quantos pixels a carta desce cada vez que você investiga

CONFIANCA_INICIAL = 50
MENSAGENS_POR_PARTIDA = 8 

# Mudanças na Confiança
GANHO_BOATO_BARRADO = 4         # você desmentiu um boato
GANHO_VERDADE_CONFIRMADA = 5    # você confirmou uma verdade
GANHO_VERDADE_CIRCULOU = 2      # uma verdade chegou à comunidade
PERDA_BOATO_CHEGOU = 20         # um boato chegou à comunidade
PERDA_VERDADE_DERRUBADA = 20    # você desmentiu uma verdade (erro!)
PERDA_BOATO_CONFIRMADO = 25     # você confirmou um boato (erro grave!)

# Cores
COR_FUNDO = (20, 28, 48)
COR_PAINEL = (30, 40, 66)
COR_CARTA = (245, 246, 250)
COR_TEXTO = (236, 240, 250)
COR_TEXTO_ESCURO = (30, 34, 48)
COR_SUAVE = (160, 172, 198)
COR_VERDE = (62, 190, 124)
COR_VERMELHO = (234, 76, 88)
COR_AMARELO = (255, 200, 64)
COR_AZUL = (84, 156, 255)

# =====================================================================
# 2. CONTEÚDO DO JOGO
# =====================================================================

INTRO_TEXTO = (
    "Os seus vizinhos usam o grupo de mensagens do bairro para se informar. "
    "Mas recentemente varios boatos e golpes circulam mais rápido que a verdade. "
    "Com sua experiencia e conhecimento na internet,"
    "você se disponibilizou a ser a pessoa em quem eles podem confiar para perguntar: isso é verdade? "
)

# Cada mensagem tem:
#   remetente    -> quem mandou
#   texto        -> a mensagem que aparece na carta
#   falsa        -> True = boato  |  False = informação verdadeira
#   pistas       -> 3 pistas, cada uma com (texto, "ruim" ou "boa")
#   consequencia -> (só boato) o que acontece se ele CHEGAR à comunidade
#   salvou       -> (só boato) o que acontece se você DESMENTIR
#   bom          -> (só verdade) o que acontece quando ela circula
NOTICIAS = [
    
    {"remetente": "Tio Zé", "falsa": True,
     "texto": "URGENTE!!! Água com limão em jejum CURA diabetes em 7 dias! COMPARTILHE!",
     "pistas": [("Ninguém assina a mensagem: 'vi num grupo'.", "ruim"),
                ("CAIXA ALTA e pressão para compartilhar já.", "ruim"),
                ("Promete cura milagrosa, sem médico nem estudo.", "ruim")],
     "consequencia": "Seu Antônio largou o remédio da diabetes e passou mal.",
     "salvou": "Seu Antônio manteve o tratamento. Susto evitado!"},

    {"remetente": "Prima Rita", "falsa": True,
     "texto": "Você ganhou R$ 2.000 do governo! Clique no link e digite CPF e senha do banco.",
     "pistas": [("O link termina em '.xyz': não é site oficial.", "ruim"),
                ("Pede senha do banco. Nenhum órgão pede isso.", "ruim"),
                ("Dinheiro fácil e com pressa: isca de golpe.", "ruim")],
     "consequencia": "Dona Lúcia digitou a senha e perdeu a aposentadoria.",
     "salvou": "Dona Lúcia quase caiu no golpe, mas você avisou a tempo."},

    {"remetente": "Colega Dani", "falsa": True,
     "texto": "Tubarão na rua alagada da cidade! Foto de hoje. Compartilhe antes que APAGUEM!",
     "pistas": [("A mesma foto circula há anos, de outro país.", "ruim"),
                ("Sem local, data nem jornal que confirme.", "ruim"),
                ("'Compartilhe antes que apaguem' é apelo de boato.", "ruim")],
     "consequencia": "O pânico lotou o telefone da Defesa Civil com chamadas falsas.",
     "salvou": "Você evitou o pânico e a Defesa Civil ficou livre para casos reais."},

    {"remetente": "Tia Neide", "falsa": True,
     "texto": "O aplicativo vai cobrar mensalidade amanhã! Repasse para 10 contatos e continue grátis.",
     "pistas": [("Nenhum comunicado oficial do aplicativo.", "ruim"),
                ("Corrente: 'repasse para 10 contatos'.", "ruim"),
                ("O mesmo boato circula há anos e nunca se confirmou.", "ruim")],
     "consequencia": "Os contatos foram inundados de correntes e spam.",
     "salvou": "A corrente morreu aqui. Ninguém foi incomodado!"},

    {"remetente": "Prefeitura", "falsa": False,
     "texto": "Campanha de vacinação infantil começa segunda nas unidades de saúde. Leve a caderneta.",
     "pistas": [("Publicada no site oficial da prefeitura (.gov.br).", "boa"),
                ("Informa data, local e documento necessário.", "boa"),
                ("Tom calmo, sem exigir que você compartilhe.", "boa")],
     "bom": "Dona Lúcia levou o neto para vacinar a tempo."},

    {"remetente": "Defesa Civil", "falsa": False,
     "texto": "Alerta de chuva forte à tarde. Evite áreas de alagamento e ruas inundadas.",
     "pistas": [("Vem do perfil verificado da Defesa Civil.", "boa"),
                ("Traz dia, horário e região do alerta.", "boa"),
                ("As orientações batem com o site oficial.", "boa")],
     "bom": "Vários moradores voltaram para casa antes da chuva forte."},

    {"remetente": "Banco", "falsa": False,
     "texto": "Seu banco nunca pede senha por telefone, mensagem ou e-mail. Na dúvida, ligue para o número do cartão.",
     "pistas": [("Aparece no aplicativo e no site oficial do banco.", "boa"),
                ("Todos os bancos dão essa mesma orientação.", "boa"),
                ("Não pede dados nem clique em link.", "boa")],
     "bom": "Seu Joaquim desligou na cara de um golpista. Dinheiro salvo!"},

    {"remetente": "Escola Municipal", "falsa": False,
     "texto": "Reunião de pais será sábado, às 9h, no pátio da escola. Aviso no mural e no site.",
     "pistas": [("Publicado no site e no mural da escola.", "boa"),
                ("Traz dia, horário e local.", "boa"),
                ("Dá para confirmar ligando para a secretaria.", "boa")],
     "bom": "Os pais foram à reunião e ficaram bem informados."},
    
    {"remetente": "Seu João da padaria", "falsa": True,
         "texto": "URGENTE!!! Elnino vai vai trazer temporal nos proximos 3 dias, alagamentos eminentes! COMPARTILHE!",
         "pistas": [("Não existe nenhum tipo de fonte comprovando a informação.", "ruim"),
                    ("CAIXA ALTA e pressão para compartilhar já.", "ruim"),
                    ("Usa pedaços de verdade para espalhar o medo", "ruim")],
         "consequencia": "Dona Maria deixou de ir ao trabalho por medo da chuva e perdeu o emprego.",
         "salvou": "Dona Maria continuou indo ao trabalho normalmente. Emprego Salvo!"},
    
    {"remetente": "Companhia de Energia", "falsa": False,
         "texto": "Tarifa social: famílias de baixa renda inscritas no CadÚnico podem pedir desconto na conta de luz.",
         "pistas": [("A regra está no site oficial da companhia e do governo.", "boa"),
                    ("Critérios claros e inscrição gratuita.", "boa"),
                    ("Não pede dinheiro nem senha para dar o desconto.", "boa")],
         "bom": "Famílias do bairro conseguiram desconto na conta de luz."},
]

SINAIS_DE_ALERTA = [
    "Urgência, CAIXA ALTA e 'compartilhe já'",
    "Ninguém assina / fonte desconhecida",
    "Promessa milagrosa (cura, dinheiro fácil)",
    "Pede senha, código ou dados pessoais",
    "Link ou site parecido com o oficial",
]


# =====================================================================
# 3. FUNÇÕES DE APOIO
# =====================================================================
def escrever(tela, texto, tamanho, cor, pos, ancora="topleft"):
    """Escreve um texto na tela. 'ancora' diz qual ponto do texto fica em 'pos'."""
    imagem = pygame.font.Font(None, tamanho).render(texto, True, cor)
    retangulo = imagem.get_rect()
    setattr(retangulo, ancora, pos)
    tela.blit(imagem, retangulo)


def quebrar_texto(tamanho, texto, largura_max):
    """Divide um texto longo em linhas que cabem em 'largura_max' pixels."""
    fonte = pygame.font.Font(None, tamanho)
    linhas, atual = [], ""
    for palavra in texto.split(" "):
        teste = (atual + " " + palavra).strip()
        if fonte.size(teste)[0] <= largura_max or not atual:
            atual = teste
            
        else:
            linhas.append(atual)
            atual = palavra
            
    if atual:
        linhas.append(atual)
        
    return linhas


def escrever_bloco(tela, texto, tamanho, cor, x, y, largura, espaco, max_linhas=10, centro=False):
    """Escreve um texto com várias linhas. Devolve o próximo y livre."""
    for i, linha in enumerate(quebrar_texto(tamanho, texto, largura)[:max_linhas]):
        if centro:
            escrever(tela, linha, tamanho, cor, (x + largura // 2, y + i * espaco), "midtop")
        
        else:
            escrever(tela, linha, tamanho, cor, (x, y + i * espaco))
    return y + min(len(quebrar_texto(tamanho, texto, largura)), max_linhas) * espaco



# =====================================================================
# 4. REGRAS DO JOGO
# =====================================================================

def novo_estado():
    return {
        "rodando": True,
        "tela": "intro",        # "intro", "jogando" ou "fim"
        "confianca": CONFIANCA_INICIAL,
        "pontos": 0,
        "combo": 0,             # acertos seguidos
        "fila": [],             # mensagens que ainda vão cair
        "carta": None,          # a mensagem que está na tela agora (ou None)
        "numero": 0,            # quantas mensagens já apareceram
        "total": 0,             # quantas mensagens a partida tem
        "espera": 0.0,          # pausa curtinha entre uma mensagem e outra
        "feedback": ("", COR_TEXTO, 0.0),   # (texto, cor, segundos restantes)
        "venceu": False,
    }


def iniciar_partida(estado):
    """Zera tudo e sorteia as mensagens da partida."""
    estado.update(novo_estado())
    estado["tela"] = "jogando"
    quantas = min(MENSAGENS_POR_PARTIDA, len(NOTICIAS))
    estado["fila"] = random.sample(NOTICIAS, quantas)
    estado["total"] = quantas
    proxima_carta(estado)


def proxima_carta(estado):
    """Coloca a próxima mensagem no topo da tela. Se acabaram, termina o jogo."""
    if estado["fila"]:
        item = estado["fila"].pop()
        estado["numero"] += 1
        estado["carta"] = {"item": item, "y": 80.0, "pistas_reveladas": 0}
        
    else:
        estado["venceu"] = True
        estado["tela"] = "fim"


def mostrar_feedback(estado, texto, cor):
    """Mostra uma frase na tela por 3 segundos (é o 'feedback' para o jogador)."""
    estado["feedback"] = (texto, cor, 3.0)


def resolver_carta(estado):
    """A mensagem atual terminou (decidida ou chegou). Some e espera um pouquinho."""
    estado["carta"] = None
    estado["espera"] = 0.9

def multiplicador(estado):
    valor_inicial = 1
    valor_combo = min(estado["combo"], 10)
    multiplicador = 0.1 * valor_combo
    return  valor_inicial + multiplicador 


def investigar(estado):
    """ESPAÇO: revela a próxima pista. Investigar CUSTA tempo: a carta desce."""
    carta = estado["carta"]
    if carta is not None and carta["pistas_reveladas"] < 3:
        carta["pistas_reveladas"] += 1
        carta["y"] += CUSTO_PISTA


def dar_veredito(estado, palpite):
    """D ou C: o jogador decidiu. 'palpite' é "falsa" ou "verdadeira"."""
    carta = estado["carta"]
    if carta is None:
        return
    
    item = carta["item"]
    pistas = carta["pistas_reveladas"] # quantas pistas o jogador investigou

    if item["falsa"] and palpite == "falsa":
        # CASO 1 você desmentiu um boato. Acertou!
        estado["pontos"] += int((100 + 20 * pistas) * multiplicador(estado))
        estado["combo"] += 1
        estado["confianca"] += GANHO_BOATO_BARRADO
        mostrar_feedback(estado, item["salvou"], COR_VERDE)

    elif not item["falsa"] and palpite == "verdadeira":
        # CASO 2 você confirmou uma verdade. Acertou!
        estado["pontos"] += int((60 + 20 * pistas) * multiplicador(estado))
        estado["combo"] += 1
        estado["confianca"] += GANHO_VERDADE_CONFIRMADA
        mostrar_feedback(estado, item["bom"], COR_VERDE)

    elif not item["falsa"] and palpite == "falsa":
        # CASO 3: você desmentiu uma verdade. ERRO!
        estado["pontos"] -= 50
        estado["pontos"] = max(0, estado["pontos"])
        estado["combo"] = 0
        estado["confianca"] -= PERDA_VERDADE_DERRUBADA
        mostrar_feedback(estado, "Você derrubou uma informação verdadeira! Desconfiar de tudo também prejudica.",COR_AMARELO)        

    else:
        # CASO 4: você confirmou um boato. ERRO GRAVE!
        estado["pontos"] -= 50
        estado["pontos"] = max(0, estado["pontos"])
        estado["combo"] = 0
        estado["confianca"] -= PERDA_BOATO_CONFIRMADO
        mostrar_feedback(estado, "Selo de verificado num boato! " + item["consequencia"], COR_VERMELHO)        

    resolver_carta(estado)


def mensagem_chegou(estado):
    """A mensagem encostou na linha da comunidade sem o jogador decidir."""
    item = estado["carta"]["item"]
    if item["falsa"]:
        # O BOATO CHEGOU À COMUNIDADE!
        estado["confianca"] -= PERDA_BOATO_CHEGOU
        estado["combo"] = 0
        mostrar_feedback(estado, item["consequencia"], COR_VERMELHO)
    
    else:
        # Uma verdade que circula faz bem à comunidade.
        estado["confianca"] += GANHO_VERDADE_CIRCULOU
        estado["pontos"] += 10
        mostrar_feedback(estado, item["bom"], COR_AMARELO)
        
    resolver_carta(estado)


# =====================================================================
# 5. INPUT
# =====================================================================
def processar_eventos(estado):
    """Lê o teclado e a janela. Só 'recebe' o que o jogador fez; a lógica fica nas regras."""
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            estado["rodando"] = False
        elif evento.type == pygame.KEYDOWN:
            tecla = evento.key
            if tecla == pygame.K_ESCAPE:
                estado["rodando"] = False
            elif estado["tela"] in ("intro", "fim"):
                if tecla in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    iniciar_partida(estado)
            elif estado["tela"] == "jogando":
                if tecla == pygame.K_SPACE:
                    investigar(estado)
                elif tecla == pygame.K_d:
                    dar_veredito(estado, "falsa")
                elif tecla == pygame.K_c:
                    dar_veredito(estado, "verdadeira")


# =====================================================================
# 6. UPDATE  (segundo passo do game loop)
# =====================================================================
def atualizar(estado, dt):
    """Muda o estado do jogo. 'dt' é o tempo (em segundos) desde o último quadro."""
    if estado["tela"] != "jogando":
        return

    # Mantém a Confiança entre 0 e 100 e verifica se o jogador perdeu.
    estado["confianca"] = max(0, min(100, estado["confianca"]))
    if estado["confianca"] <= 0:
        estado["venceu"] = False
        estado["tela"] = "fim"
        return

    # O texto de feedback some com o tempo.
    texto, cor, restante = estado["feedback"]
    estado["feedback"] = (texto, cor, max(0.0, restante - dt))

    carta = estado["carta"]
    if carta is None:
        # Sem mensagem na tela: espera um pouquinho e chama a próxima.
        estado["espera"] -= dt
        if estado["espera"] <= 0:
            proxima_carta(estado)
        return

    # A carta cai: posição nova = posição antiga + velocidade * dt
    carta["y"] += VELOCIDADE * dt
    if carta["y"] + ALTURA_CARTA >= LINHA_COMUNIDADE:
        mensagem_chegou(estado)


# =====================================================================
# 7. DRAW
# =====================================================================
def desenhar(tela, estado):
    tela.fill(COR_FUNDO)
    if estado["tela"] == "intro":
        desenhar_intro(tela)
    elif estado["tela"] == "jogando":
        desenhar_jogo(tela, estado)
    else:
        desenhar_fim(tela, estado)
    pygame.display.flip()


def desenhar_intro(tela):
    escrever(tela, "CHECA AÍ!", 110, COR_AMARELO, (LARGURA // 2, 70), "midtop")
    escrever(tela, "Antes de compartilhar, verifique.", 36, COR_TEXTO, (LARGURA // 2, 175), "midtop")
    escrever_bloco(tela, INTRO_TEXTO, 30, COR_TEXTO, 100, 250, LARGURA - 200, 34, centro=True)
    controles = ["ESPAÇO = investigar (revela uma pista, mas a mensagem desce)",
                 "D = desmentir (é FALSA)        C = confirmar (é VERDADEIRA)"]
    for i, linha in enumerate(controles):
        escrever(tela, linha, 28, COR_SUAVE, (LARGURA // 2, 440 + i * 34), "midtop")
    escrever(tela, "Aperte ENTER para começar   (ESC sai)", 34, COR_VERDE, (LARGURA // 2, 560), "midtop")


def desenhar_hud(tela, estado):
    """Barra de cima: número da mensagem, Confiança e pontos."""
    pygame.draw.rect(tela, COR_PAINEL, (0, 0, LARGURA, 56))
    escrever(tela, "Mensagem %d/%d" % (estado["numero"], estado["total"]), 26, COR_TEXTO, (20, 18))
    # barra de Confiança
    conf = int(estado["confianca"])
    escrever(tela, "CONFIANÇA DA COMUNIDADE", 18, COR_SUAVE, (300, 3))
    pygame.draw.rect(tela, (12, 16, 30), (300, 24, 300, 24), border_radius=6)
    cor = COR_VERDE if conf >= 50 else (COR_AMARELO if conf >= 25 else COR_VERMELHO)
    pygame.draw.rect(tela, cor, (300, 24, int(300 * conf / 100), 24), border_radius=6)
    escrever(tela, "%d%%" % conf, 22, (255, 255, 255), (450, 36), "center")
    # pontos e combo
    escrever(tela, "Pontos: %d" % estado["pontos"], 28, COR_AMARELO, (LARGURA - 20, 6), "topright")
    if estado["combo"] >= 2:
        escrever(tela, "Combo x%.1f" % multiplicador(estado), 22, COR_VERDE, (LARGURA - 20, 34), "topright")


def desenhar_carta(tela, carta):
    retangulo = pygame.Rect(40, int(carta["y"]), 540, ALTURA_CARTA)
    pygame.draw.rect(tela, COR_CARTA, retangulo, border_radius=12)
    pygame.draw.rect(tela, (214, 224, 244), (retangulo.x, retangulo.y, retangulo.w, 30),
                     border_top_left_radius=12, border_top_right_radius=12)
    escrever(tela, "de: " + carta["item"]["remetente"], 22, (50, 64, 100), (retangulo.x + 14, retangulo.y + 8))
    escrever_bloco(tela, carta["item"]["texto"], 28, COR_TEXTO_ESCURO,
                   retangulo.x + 14, retangulo.y + 42, retangulo.w - 28, 28, max_linhas=4)


def desenhar_pistas(tela, carta):
    """Painel da direita com as 3 pistas (bloqueadas até o jogador investigar)."""
    escrever(tela, "PISTAS  (ESPAÇO)", 26, COR_AMARELO, (610, 74))
    reveladas = carta["pistas_reveladas"] if carta else 0
    for i in range(3):
        caixa = pygame.Rect(610, 106 + i * 118, 270, 108)
        if carta and i < reveladas:
            texto, tipo = carta["item"]["pistas"][i]
            cor = COR_VERMELHO if tipo == "ruim" else COR_VERDE
            rotulo = "ALERTA" if tipo == "ruim" else "OK"
            pygame.draw.rect(tela, COR_PAINEL, caixa, border_radius=10)
            pygame.draw.rect(tela, cor, caixa, 3, border_radius=10)
            escrever(tela, rotulo, 22, cor, (caixa.x + 12, caixa.y + 8))
            escrever_bloco(tela, texto, 22, COR_TEXTO, caixa.x + 12, caixa.y + 32, caixa.w - 24, 22, max_linhas=3)
        else:
            pygame.draw.rect(tela, (26, 36, 60), caixa, border_radius=10)
            pygame.draw.rect(tela, (60, 76, 112), caixa, 1, border_radius=10)
            escrever(tela, "pista %d: bloqueada" % (i + 1), 22, (96, 110, 146), caixa.center, "center")


# ---------------------------------------------------------------------
# >>> TODO 6 <<<  (DESAFIO) OS MORADORES DO BAIRRO
# Desenhe 5 bolinhas (moradores) na faixa de baixo da tela. Quanto menor a
# Confiança, mais moradores ficam "enganados" (vermelhos). Os outros ficam verdes.
# Para não depender só da cor, escreva "!" nos enganados e "ok" nos informados.
#   Ideias:  n_enganados = round((100 - estado["confianca"]) / 20)
#            for i in range(5):  x = 120 + i * 160   (y = 575)
#            pygame.draw.circle(tela, cor, (x, 575), 26)
# ---------------------------------------------------------------------
def desenhar_moradores(tela, estado):
    n_enganados = round((100 - estado["confianca"]) / 20)
    for i in range(5):
        x = 120 + i * 160
        enganado = i < n_enganados
        cor = COR_VERMELHO if enganado else COR_VERDE
        pygame.draw.circle(tela, cor, (x, 575), 26)
        escrever(tela, "!" if enganado else "ok", 30, (255, 255, 255), (x, 575), "center")

def desenhar_jogo(tela, estado):
    desenhar_hud(tela, estado)
    
    # faixa da comunidade (parte de baixo)
    pygame.draw.rect(tela, (24, 32, 56), (0, LINHA_COMUNIDADE, LARGURA, ALTURA - LINHA_COMUNIDADE))
    for x in range(0, LARGURA, 24):
        pygame.draw.line(tela, COR_VERMELHO, (x, LINHA_COMUNIDADE), (x + 12, LINHA_COMUNIDADE), 3)
        
    escrever(tela, "A COMUNIDADE (mensagens que encostam aqui chegam a todos)", 20, COR_SUAVE,
             (LARGURA // 2, LINHA_COMUNIDADE + 6), "midtop")
    
    # a carta, as pistas e os moradores
    if estado["carta"] is not None:
        desenhar_carta(tela, estado["carta"])
        
    desenhar_pistas(tela, estado["carta"])
    desenhar_moradores(tela, estado)
    # feedback (frase que aparece depois de cada decisão)
    texto, cor, restante = estado["feedback"]
    if restante > 0:
        escrever_bloco(tela, texto, 26, cor, 30, LINHA_COMUNIDADE + 30, LARGURA - 60, 26, max_linhas=2, centro=True)
        
    escrever(tela, "ESPAÇO = investigar     D = desmentir (falsa)     C = confirmar (verdadeira)", 22, COR_SUAVE,
             (LARGURA // 2, ALTURA - 10), "midbottom")


def desenhar_fim(tela, estado):
    if estado["venceu"]:
        escrever(tela, "O BAIRRO APRENDEU A CHECAR!", 64, COR_VERDE, (LARGURA // 2, 50), "midtop")
        escrever(tela, "Você manteve a confiança da comunidade.", 32, COR_TEXTO, (LARGURA // 2, 130), "midtop")
        
    else:
        escrever(tela, "A CONFIANÇA ACABOU", 70, COR_VERMELHO, (LARGURA // 2, 50), "midtop")
        escrever(tela, "Os boatos venceram desta vez. Tente de novo!", 32, COR_TEXTO, (LARGURA // 2, 130), "midtop")
        
    escrever(tela, "Pontos: %d" % estado["pontos"], 44, COR_AMARELO, (LARGURA // 2, 200), "midtop")
    escrever(tela, "Confiança final: %d%%" % int(estado["confianca"]), 30, COR_TEXTO, (LARGURA // 2, 255), "midtop")
    escrever(tela, "LEMBRE DOS SINAIS DE ALERTA:", 30, COR_VERMELHO, (LARGURA // 2, 320), "midtop")
    for i, sinal in enumerate(SINAIS_DE_ALERTA):
        escrever(tela, "- " + sinal, 28, COR_TEXTO, (LARGURA // 2, 360 + i * 32), "midtop")
        
    escrever(tela, "ENTER = jogar de novo     ESC = sair", 32, COR_VERDE, (LARGURA // 2, 580), "midtop")


# =====================================================================
# 8. MAIN — o GAME LOOP
# =====================================================================
def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Checa Aí")
    relogio = pygame.time.Clock()
    estado = novo_estado()

    while estado["rodando"]:
        dt = relogio.tick(FPS) / 1000.0

        processar_eventos(estado)
        atualizar(estado, dt)
        desenhar(tela, estado)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
