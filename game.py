import pygame
pygame.init()
pygame.mixer.init()  # Inicia o mixer para músicas

# Pega a resolução da tela do PC
info_tela = pygame.display.Info()
largura_tela = info_tela.current_w
altura_tela = info_tela.current_h

# Define a janela com o tamanho da tela
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Sistema de Fases")


# Tamanho da janela em tela cheia
largura, altura = pygame.display.Info().current_w, pygame.display.Info().current_h
tela = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)
pygame.display.set_caption("Prison Realms")

# Posição e tamanho do jogador
largura_q, altura_q = 50, 50
x, y = largura // 2 - largura_q // 2, altura // 2 - altura_q // 2

# Variáveis dos projéteis
projetil_largura, projetil_altura = 30, 15
projetil_cor = (255, 255, 255)
projetil_velocidade = 15
projetil_lista = []
cooldown_tiro = 500  # tempo mínimo entre tiros (em ms)
ultimo_tiro = 0
direcao_jogador = "direita"  # Direção inicial


# Cor dos olhos
cor_olho = (255, 0, 255)
cor_inimigo = (255, 0, 0)

# Velocidade de movimento
velocidade = 6

# Lista de inimigos com HP
inimigo_largura = 50
inimigo_altura = 50
inimigos = [
    {"rect": pygame.Rect(largura * 0.1, altura * 0.1, inimigo_largura, inimigo_altura), "hp": 3},
    {"rect": pygame.Rect(largura * 0.5, altura * 0.3, inimigo_largura, inimigo_altura), "hp": 3},
    {"rect": pygame.Rect(largura * 0.8, altura * 0.7, inimigo_largura, inimigo_altura), "hp": 3},
    {"rect": pygame.Rect(largura * 0.2, altura * 0.8, inimigo_largura, inimigo_altura), "hp": 3},
    {"rect": pygame.Rect(largura * 0.7, altura * 0.2, inimigo_largura, inimigo_altura), "hp": 3}
]


# HP do jogador
hp = 100
max_hp = 100

# Variável para controlar o menu
menu = True

# Função de colisão com inimigos
def colisao_com_inimigos(rect_teste):
    for inimigo in inimigos:
        if rect_teste.colliderect(inimigo["rect"]):
            return True
    return False

# Função para desenhar a barra de HP
def desenhar_barra_hp(tela, x, y, hp, max_hp):
    largura_barra = 200
    altura_barra = 25
    cor_fundo = (50, 50, 50)
    cor_preenchimento = (255, 0, 0) if hp <= 0 else (255 - int(255 * (hp / max_hp)), int(255 * (hp / max_hp)), 0)
    pygame.draw.rect(tela, cor_fundo, (x, y, largura_barra, altura_barra))
    pygame.draw.rect(tela, cor_preenchimento, (x, y, (largura_barra * hp) / max_hp, altura_barra))

# Função para desenhar o menu com música
def desenhar_menu(tela):
    tela.fill((70, 30, 80))  # Cor de fundo

    fonte_titulo = pygame.font.SysFont('Arial Black', 72)
    fonte_texto = pygame.font.SysFont('Arial', 40)

    titulo = fonte_titulo.render("Começe", True, (255, 255, 255))
    sombra = fonte_titulo.render("Começe", True, (100, 0, 150))
    iniciar_texto = fonte_texto.render("Pressione ENTER para começar", True, (255, 255, 255))

    # Sombra e título
    tela.blit(sombra, (largura // 2 - titulo.get_width() // 2 + 4, altura // 4 + 4))
    tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, altura // 4))

    # Botão
    botao_largura = 500
    botao_altura = 80
    botao_x = largura // 2 - botao_largura // 2
    botao_y = altura // 2 - botao_altura // 2

    botao_rect = pygame.Rect(botao_x, botao_y, botao_largura, botao_altura)
    pygame.draw.rect(tela, (100, 40, 150), botao_rect, border_radius=20)
    pygame.draw.rect(tela, (180, 80, 255), botao_rect, 5, border_radius=20)  # Borda

    # Texto centralizado no botão
    texto_x = largura // 2 - iniciar_texto.get_width() // 2
    texto_y = botao_y + botao_altura // 2 - iniciar_texto.get_height() // 2
    tela.blit(iniciar_texto, (texto_x, texto_y))

    # Cubo do jogador (à esquerda do botão)
    cubo_tamanho = 50
    cubo_x = botao_x - cubo_tamanho - 30  # Espaço à esquerda
    cubo_y = botao_y + botao_altura // 2 - cubo_tamanho // 2

    # Corpo do cubo
    cubo_rect = pygame.Rect(cubo_x, cubo_y, cubo_tamanho, cubo_tamanho)
    pygame.draw.rect(tela, (255, 255, 255), cubo_rect)  # cubo branco

    # Olhinhos roxos
    olho_raio = 10
    olho1_x = cubo_x + 12
    olho2_x = cubo_x + cubo_tamanho - 12
    olho_y = cubo_y + 18

    pygame.draw.circle(tela, (160, 70, 255), (olho1_x, olho_y), olho_raio)
    pygame.draw.circle(tela, (160, 70, 255), (olho2_x, olho_y), olho_raio)

    pygame.display.flip()

# Carregar e tocar música de fundo no menu
# Carregar e tocar música de fundo no menu
pygame.mixer.music.load(r"C:\Users\_MARCOS\Downloads\menumusic (1) (1).mp3")
pygame.mixer.music.play(-1, 0.0)  # Toca a música em loop (-1)

# Música de gameplay será carregada quando o jogo começar (após o menu)
#pygame.mixer.music.load(r"C:\Users\_MARCOS\Downloads\musicgame\gameplaymusic.mp3")

# Loop principal
rodando = True
ultimo_dano = pygame.time.get_ticks()
intervalo_dano = 600

# Clock para controlar FPS
clock = pygame.time.Clock()

# Função de seguir o jogador (já estava boa)
def inimigo_seguir_jogador(inimigo, jogador_x, jogador_y, velocidade):
    # Calcula a direção do jogador
    dx = jogador_x - inimigo.x
    dy = jogador_y - inimigo.y
    distancia = (dx ** 2 + dy ** 2) ** 0.5  # Calculando a distância diretamente

    # Normaliza a direção do inimigo
    if distancia != 0:
        dx /= distancia
        dy /= distancia

        # Atualiza a posição do inimigo
        inimigo.x += dx * velocidade
        inimigo.y += dy * velocidade

# Loop principal
rodando = True
ultimo_dano = pygame.time.get_ticks()
intervalo_dano = 1000

# Clock para controlar FPS
clock = pygame.time.Clock()

while rodando:
    clock.tick(60)
    tela.fill((70, 30, 80))

    if menu:
        desenhar_menu(tela)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    menu = False
                    pygame.mixer.music.load(r"C:\Users\_MARCOS\Downloads\gameplaymusic (2).mp3")
                    pygame.mixer.music.play(-1, 0.0)
    else:
        # Captura de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Movimento do jogador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            x -= velocidade
            direcao_jogador = "esquerda"
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            x += velocidade
            direcao_jogador = "direita"
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            y -= velocidade
            direcao_jogador = "cima"
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            y += velocidade
            direcao_jogador = "baixo"

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            x -= velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            x += velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            y -= velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            y += velocidade
        
                      # Disparo (com cooldown)
        agora = pygame.time.get_ticks()
        if teclas[pygame.K_SPACE] and agora - ultimo_tiro >= cooldown_tiro:
            if direcao_jogador == "direita":
                novo_proj = {
                    "rect": pygame.Rect(x + largura_q, y + altura_q // 2 - projetil_altura // 2, projetil_largura, projetil_altura),
                    "dx": projetil_velocidade, "dy": 0
                }
            elif direcao_jogador == "esquerda":
                novo_proj = {
                    "rect": pygame.Rect(x - projetil_largura, y + altura_q // 2 - projetil_altura // 2, projetil_largura, projetil_altura),
                    "dx": -projetil_velocidade, "dy": 0
                }
            elif direcao_jogador == "cima":
                novo_proj = {
                    "rect": pygame.Rect(x + largura_q // 2 - projetil_altura // 2, y - projetil_largura, projetil_altura, projetil_largura),
                    "dx": 0, "dy": -projetil_velocidade
                }
            elif direcao_jogador == "baixo":
                novo_proj = {
                    "rect": pygame.Rect(x + largura_q // 2 - projetil_altura // 2, y + altura_q, projetil_altura, projetil_largura),
                    "dx": 0, "dy": projetil_velocidade
                }

            projetil_lista.append(novo_proj)
            ultimo_tiro = agora


         # Limitação de bordas da tela
        if x < 0:
            x = 0
        if x > largura - largura_q:
            x = largura - largura_q
        if y < 0:
            y = 0
        if y > altura - altura_q:
            y = altura - altura_q

        # Criação do retângulo do jogador
        jogador_rect = pygame.Rect(x, y, largura_q, altura_q)
        pygame.draw.rect(tela, (255, 255, 255), jogador_rect)

        # Olhos do jogador
        
        pygame.draw.circle(tela, cor_olho, (x + largura_q - 12, y + 18), 8)
        pygame.draw.circle(tela, cor_olho, (x + 12, y + 18), 8)
                # Atualiza e desenha inimigos
        for inimigo in inimigos:
            inimigo_seguir_jogador(inimigo["rect"], x, y, 2)
            pygame.draw.rect(tela, cor_inimigo, inimigo["rect"])

            # Olhos pretos do inimigo
            olho_raio = 6
            olho1_x = int(inimigo["rect"].x + 12)
            olho2_x = int(inimigo["rect"].x + inimigo["rect"].width - 12)
            olho_y = int(inimigo["rect"].y + 18)

            pygame.draw.circle(tela, (0, 0, 0), (olho1_x, olho_y), olho_raio)
            pygame.draw.circle(tela, (0, 0, 0), (olho2_x, olho_y), olho_raio)

        # Checar colisão e diminuir HP
        agora = pygame.time.get_ticks()
        if colisao_com_inimigos(jogador_rect) and agora - ultimo_dano >= intervalo_dano:
            hp -= 15
            ultimo_dano = agora

      
        if hp <= 0:
            rodando = False
            
        desenhar_barra_hp(tela, 20, 20, hp, max_hp)

        for projetil in projetil_lista[:]:
            projetil["rect"].x += projetil["dx"]
            projetil["rect"].y += projetil["dy"]
            pygame.draw.rect(tela, projetil_cor, projetil["rect"])

            # Colisão com inimigos
            for inimigo in inimigos[:]:
                if projetil["rect"].colliderect(inimigo["rect"]):
                    inimigo["hp"] -= 1
                    if projetil in projetil_lista:
                        projetil_lista.remove(projetil)
                    if inimigo["hp"] <= 0:
                        inimigos.remove(inimigo)
                    break

               
             
        # Remove projéteis fora da tela
        projetil_lista = [p for p in projetil_lista if 0 <= p["rect"].x <= largura and 0 <= p["rect"].y <= altura]

     
        pygame.display.flip()