import tkinter as tk

pressed_keys = set()

def pressionado(tecla):
    return tecla.lower() in pressed_keys

def _registrar_eventos_teclado(widget):
    def on_press(event):
        pressed_keys.add(event.keysym.lower())

    def on_release(event):
        pressed_keys.discard(event.keysym.lower())

    widget.bind("<KeyPress>", on_press)
    widget.bind("<KeyRelease>", on_release)
    widget.focus_set()
