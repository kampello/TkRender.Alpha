import math
import pygame
import engine.colisao as colide

# Tamanho do inimigo
w, h = 30, 30  # Ajusta conforme o tamanho do sprite

def mover_inimigo(inimigo, player, velocidade=2, mapa=None, obstaculos=None):
    # Calcula a diferença de posição entre inimigo e jogador
    dx = player.x - inimigo.x
    dy = player.y - inimigo.y
    distancia = math.hypot(dx, dy)

    if distancia != 0:
        # Normaliza a direção
        dx /= distancia
        dy /= distancia

        # Calcula nova posição
        nova_x = inimigo.x + dx * velocidade
        nova_y = inimigo.y + dy * velocidade

        # Cria uma hitbox para a nova posição
        hitbox = pygame.Rect(nova_x, nova_y, w, h)

        # Verifica colisões com objetos do mapa
        if mapa:
            for objeto in mapa.objects:
                if colide.detetar(hitbox, objeto.get_rect()):
                    return  # Interrompe o movimento

        # Verifica colisões com obstáculos adicionais
        if obstaculos:
            for obs in obstaculos:
                if colide.detetar(hitbox, obs.get_rect()):
                    return  # Interrompe o movimento

        # Move o inimigo se não houve colisão
        inimigo.x = nova_x
        inimigo.y = nova_y

