import engine.render
from engine.render import Renderer, Camera
from engine.teclado import pressionado
from time import sleep

# Inicializa o render
Renderer.iniciar(800, 600, "Teste simples")


camera = Camera(3840, 3840)

# UI (fica em cima de tudo e se move com a câmera)
pt_txt = Renderer.draw_text(400, 0, "0", (255, 0, 0), 64)
camera.UI(pt_txt)  # UI que se move com a câmera

# Adicionando um gif (movível pela câmera)
gif = Renderer.draw_image("img/planet.gif", 600, 300, 32, 32)
texto = Renderer.draw_text(100, 100, "press (w) to play audio")
def evento(evento):
    if pressionado("w"):
        camera.y -= 10  # Move a câmera para cima
    if pressionado("s"):
        camera.y += 10  # Move a câmera para baixo
    if pressionado("a"):
        camera.x -= 10  # Move a câmera para a esquerda
    if pressionado("d"):
        camera.x += 10  # Move a câmera para a direita

# Passando a função normal para o loop
Renderer.executar(evento, camera)
