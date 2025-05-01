'''versao aprimorada do movement'''

import pygame
import engine.colisao as colide
import engine.teclado as teclado

# Direções e deslocamentos associados
DESLOCAMENTOS = {
    "cima": (0, -1),
    "baixo": (0, 1),
    "esquerda": (-1, 0),
    "direita": (1, 0),
}
w = 30
h = 30

def pode_mover_para(player, direcao, mapa=None, obstaculos=None, velocidade=5):
    """
    Verifica se o jogador pode mover-se na direção especificada sem colidir.
    """
    dx, dy = DESLOCAMENTOS.get(direcao, (0, 0))
    futura_x = player.x + dx * velocidade
    futura_y = player.y + dy * velocidade

    # Cria uma hitbox temporária na nova posição
    hitbox = pygame.Rect(futura_x, futura_y, w, h)

    # Verificar colisão com objetos do mapa
    if mapa:
        for objeto in mapa.objects:
            if colide.detetar(hitbox, objeto.get_rect()):
                return False

    # Verificar colisão com obstáculos
    if obstaculos:
        for obs in obstaculos:
            if colide.detetar(hitbox, obs.get_rect()):
                return False

    return True


def simulatecontrol(player, direcao, imagens, velocidade):
    """
    Move o jogador na direção indicada e atualiza a animação.
    """
    dx, dy = DESLOCAMENTOS.get(direcao, (0, 0))

    # Atualiza GIF somente se necessário
    '''if player.get_gif() != imagens[direcao]:
        player.set_gif(imagens[direcao])'''

    # Move o jogador
    player.x += dx * velocidade
    player.y += dy * velocidade


def atualizar_movimento(player, imagens, velocidade, mapa=None, obstaculos=None):
    """
    Move o jogador com possibilidade de diagonais, desde que não haja colisão.
    """
    dx_total = 0
    dy_total = 0
    nova_direcao = None

    teclas_direcoes = {
        "w": "cima",
        "s": "baixo",
        "a": "esquerda",
        "d": "direita"
    }

    for tecla, direcao in teclas_direcoes.items():
        if teclado.pressionado(tecla):
            dx, dy = DESLOCAMENTOS[direcao]
            dx_total += dx
            dy_total += dy
            nova_direcao = direcao  # última direção usada para definir o GIF

    if dx_total != 0 or dy_total != 0:
        futura_x = player.x + dx_total * velocidade
        futura_y = player.y + dy_total * velocidade
        hitbox = pygame.Rect(futura_x, futura_y, 30, 30)

        # Verifica colisão antes de mover
        colisao = False
        if mapa:
            for objeto in mapa.objects:
                if colide.detetar(hitbox, objeto.get_rect()):
                    colisao = True
                    break

        if not colisao and obstaculos:
            for obs in obstaculos:
                if colide.detetar(hitbox, obs.get_rect()):
                    colisao = True
                    break

        if not colisao:
           if nova_direcao and player.get_gif() != imagens[nova_direcao]:
                player.set_gif(imagens[nova_direcao])
           player.x += dx_total * velocidade
           player.y += dy_total * velocidade
