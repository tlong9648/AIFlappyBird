import pygame 
import os 

bg_img = pygame.transform.scale(pygame.image.load(os.path.join("images","bg.png")).convert_alpha(), (600, 700))

class Back_ground():
    VEL = 5
    WIDTH = bg_img.get_width()
    IMG = bg_img

    def __init__(self):
        self.y = 0
        self.x_start = 0
        self.x_end = self.WIDTH

    def move(self):
        #Làm cho background chuyển động từ phải qua trái một các liên tục
        self.x_start -= self.VEL
        self.x_end -= self.VEL
        if self.x_start + self.WIDTH <0:
            self.x_start = self.x_end + self.WIDTH
        
        if self.x_end + self.WIDTH <0:
            self.x_end = self.x_start + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x_start, self.y))
        win.blit(self.IMG, (self.x_end, self.y))