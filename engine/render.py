import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from engine.teclado import _registrar_eventos_teclado


# Classe para representar elementos fixos de UI
class UIElemento:
    def __init__(self, canvas, x, y, img_id, camada=0):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.img_id = img_id
        self.camada = camada  # Adiciona a camada ao elemento

    def update(self):
        pass  # UIElementos não precisam de atualização, apenas posicionamento


class Camera:
    def __init__(self, largura_mundo, altura_mundo):
        self.x = 0
        self.y = 0
        self.largura_mundo = largura_mundo
        self.altura_mundo = altura_mundo
        self.ui_elementos = []

    def aplicar(self, objeto):
        # Aplica a transformação de câmera apenas em objetos não UI
        if isinstance(objeto, UIElemento):
            return objeto.x, objeto.y  # Elementos UI não são afetados pela câmera
        return (objeto.x - self.x, objeto.y - self.y)

    def UI(self, elemento):
        # Adiciona elementos fixos à UI
        self.ui_elementos.append(elemento)

    def aplicar_ui(self, elemento):
        # Retorna a posição do elemento de UI sem aplicar a câmera
        return elemento.x, elemento.y


class Renderer:
    objetos = []
    ui_elementos = []  # Lista para elementos da UI
    tela = None
    root = None
    canvas = None
    relogio = 60
    largura = 800
    altura = 600
    titulo = ""
    camera = None

    @classmethod
    def iniciar(cls, largura=800, altura=600, titulo="TkRenderEngine"):
        cls.largura = largura
        cls.altura = altura
        cls.titulo = titulo
        cls.root = tk.Tk()
        cls.root.title(titulo)
        cls.canvas = tk.Canvas(cls.root, width=largura, height=altura, bg="black")
        cls.canvas.pack()
        _registrar_eventos_teclado(cls.canvas)

    @classmethod
    def draw_image(cls, caminho, x, y, w, h, camada=0):
        # Verifica se é GIF ou imagem estática e escolhe a classe apropriada
        try:
            img = ImagemAnimadaTk(cls.canvas, caminho, x, y, w, h)  # Usando ImagemAnimadaTk para GIFs
            cls.objetos.append(img)
            img.camada = camada  # Adiciona a camada ao objeto
            return img
        except:
            img = ImagemTk(cls.canvas, caminho, x, y, w, h)  # Para imagens estáticas
            cls.objetos.append(img)
            img.camada = camada  # Adiciona a camada ao objeto
            return img

    @classmethod
    def draw_text(cls, x, y, texto, cor=(255, 255, 255), fonte_tamanho=16, camada=0):
        r, g, b = cor
        color_hex = f"#{r:02x}{g:02x}{b:02x}"
        texto_id = cls.canvas.create_text(x, y, text=texto, fill=color_hex, font=("Arial", fonte_tamanho), anchor="nw")
        texto = UIElemento(cls.canvas, x, y, texto_id, camada)

        if camada == 0:  # Se for UI (camada 0), o texto não será afetado pela câmera
            cls.ui_elementos.append(texto)

        return texto

    @classmethod
    def UI(cls, elemento):
        # Adiciona elementos UI fixos
        cls.ui_elementos.append(elemento)

    @classmethod
    def executar(cls, callback, camera=None, nome=None):
        cls.camera = camera

        def loop():
            if callback:
                callback(None)

            # Atualiza objetos de fundo (movíveis)
            for obj in cls.objetos:
                obj.update()

            # Atualiza elementos da UI (fixos)
            for ui in cls.ui_elementos:
                # Aplica a posição da câmera a objetos que não são UI
                x, y = camera.aplicar_ui(ui)
                cls.canvas.coords(ui.img_id, x, y)  # Mantém a UI fixa

            # Ordena os objetos pela camada (camadas menores ficam atrás)
            cls.objetos.sort(key=lambda obj: obj.camada)

            # Atualiza a posição de objetos no cenário
            for obj in cls.objetos:
                x, y = camera.aplicar(obj)
                cls.canvas.coords(obj.img_id, x, y)

            cls.root.after(int(1000 / cls.relogio), loop)

        loop()
        cls.root.mainloop()


class ImagemTk:
    def __init__(self, canvas, caminho_imagem, x, y, largura, altura):
        self.canvas = canvas
        self.x = x
        self.y = y
        img = Image.open(caminho_imagem)
        self.animado = getattr(img, "is_animated", False)

        if self.animado:
            raise ValueError("For GIFs, use ImagemAnimadaTk instead of ImagemTk.")
        self.img = ImageTk.PhotoImage(img.resize((largura, altura)))
        self.img_id = self.canvas.create_image(x, y, image=self.img, anchor="nw")
        self.camada = 0  # Definindo a camada padrão

    def update(self):
        pass


class ImagemAnimadaTk:
    def __init__(self, canvas, caminho_gif, x, y, largura, altura):
        self.canvas = canvas
        self.frames = [ImageTk.PhotoImage(frame.copy().resize((largura, altura)))
                       for frame in ImageSequence.Iterator(Image.open(caminho_gif))]
        self.index = 0
        self.x = x
        self.y = y
        self.img_id = self.canvas.create_image(x, y, image=self.frames[0], anchor="nw")
        self.camada = 0  # Definindo a camada padrão

    def update(self):
        self.index = (self.index + 1) % len(self.frames)
        self.canvas.itemconfig(self.img_id, image=self.frames[self.index])



