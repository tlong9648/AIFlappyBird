import pygame
import os 

base_image = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'base.png')).convert_alpha())

class Base():
    VEL = 5
    WIDTH = base_image.get_width()
    IMG = base_image

    def __init__(self, y):

        self.y = y 
        self.x_start = 0
        self.x_end = self.WIDTH

    def move(self):
        #Làm cho base chuyển động từ phải qua trái một các liên tục
        self.x_start -= self.VEL
        self.x_end -= self.VEL
        if self.x_start + self.WIDTH <0:
            self.x_start = self.x_end + self.WIDTH
        
        if self.x_end + self.WIDTH <0:
            self.x_end = self.x_start + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x_start, self.y))
        win.blit(self.IMG, (self.x_end, self.y))

