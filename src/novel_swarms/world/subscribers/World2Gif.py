import pygame
import numpy as np
import time
from PIL import Image

class World2Gif:
    def __init__(self, duration=800, every_ith_frame=10, time_per_frame=150):
        self.duration = duration
        self.time_per_frame = time_per_frame
        self.every_ith_frame = every_ith_frame
        self.snips = []
        self.total_steps = 0
        self.saved = False

        print("Saving World Gif... Please do not close the window until prompted")

    def notify(self, world, screen):
        if self.total_steps > self.duration:
            if self.saved:
                return
            self.saved = True
            self.gif_n_save()
        if self.total_steps % self.every_ith_frame == 0:
            self.save_frame(screen)
        self.total_steps += 1

    def save_frame(self, screen):
        frame = pygame.surfarray.array3d(screen)
        pil_img = Image.fromarray(np.uint8(frame))
        pil_img = pil_img.transpose(Image.FLIP_LEFT_RIGHT)
        pil_img = pil_img.rotate(90, expand=True)
        self.snips.append(pil_img)

    def gif_n_save(self):
        first_frame = self.snips[0]
        name = f'{int(time.time())}.gif'
        first_frame.save(name, format="GIF", append_images=self.snips, save_all=True,
                         duration=self.time_per_frame, loop=0)
        print(f"Gif saved as {name}. You may now exit the window.")