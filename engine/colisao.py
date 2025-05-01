import pygame

def detetar(obj1, obj2):
    # Se for um pygame.Rect, usa width/height
    if isinstance(obj1, pygame.Rect):
        retangulo_este = obj1
    else:
        retangulo_este = pygame.Rect(obj1.x, obj1.y, obj1.largura, obj1.altura)

    if isinstance(obj2, pygame.Rect):
        retangulo_outro = obj2
    else:
        retangulo_outro = pygame.Rect(obj2.x, obj2.y, obj2.largura, obj2.altura)

    return retangulo_este.colliderect(retangulo_outro)


