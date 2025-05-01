from engine.render import Renderer
import pygame


class Objecto:
    def __init__(self, x, y, largura, altura, imagem, layer=0):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.imagem = imagem
        self.layer = layer
        self.objeto = Renderer.draw_image(imagem, x, y, largura, altura, layer)

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.objeto.set_position(x, y)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)
