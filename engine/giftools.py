from PIL import Image
import pygame
import os

_frame_cache = {}

def carregar_gif_em_frames(path_gif):
    if path_gif in _frame_cache:
        return _frame_cache[path_gif]

    imagem = Image.open(path_gif)
    frames = []
    frame_folder = os.path.splitext(path_gif)[0] + "_frames"

    if not os.path.exists(frame_folder):
        os.makedirs(frame_folder)

    for i in range(imagem.n_frames):
        imagem.seek(i)
        frame_path = os.path.join(frame_folder, f"frame_{i}.png")
        if not os.path.exists(frame_path):
            imagem.convert("RGBA").save(frame_path)
        frames.append(pygame.image.load(frame_path).convert_alpha())

    _frame_cache[path_gif] = frames
    return frames
