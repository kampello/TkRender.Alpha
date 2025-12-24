class Camera:
    def __init__(self, view_w: int, view_h: int, world_w: int, world_h: int):
        self.view_w = view_w
        self.view_h = view_h
        self.world_w = world_w
        self.world_h = world_h

        self.x = 0.0
        self.y = 0.0

        # opcional: suavização (0 = trava no alvo, 0.1~0.2 = suave)
        self.smooth = 0.15

    def set_world_size(self, world_w: int, world_h: int):
        self.world_w = world_w
        self.world_h = world_h

    def _clamp(self, v, lo, hi):
        if v < lo: return lo
        if v > hi: return hi
        return v

    def follow(self, target_x: float, target_y: float):
        # centraliza target no meio da tela
        target_cam_x = target_x - self.view_w / 2
        target_cam_y = target_y - self.view_h / 2

        # clamp nos limites do mundo (impede mostrar “fora do mapa”)
        max_x = max(0, self.world_w - self.view_w)
        max_y = max(0, self.world_h - self.view_h)

        target_cam_x = self._clamp(target_cam_x, 0, max_x)
        target_cam_y = self._clamp(target_cam_y, 0, max_y)

        # suavização
        self.x += (target_cam_x - self.x) * self.smooth
        self.y += (target_cam_y - self.y) * self.smooth

    def world_to_screen(self, x: float, y: float):
        return x - self.x, y - self.y
