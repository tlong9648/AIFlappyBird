import pygame
import os 
import random

pipe_image = pygame.transform.scale2x(pygame.image.load(os.path.join("images","pipe.png")).convert_alpha())

class Pipe():

    GAP = 210 #Khoảng cách mặc định giữa ống trên và dưới
    VEL = 5
    def __init__(self, x):

        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.pipe_top = pygame.transform.flip(pipe_image, False, True)
        #Lập ống để tạo ống trên.
        self.pipe_bottom = pipe_image

        self.passed = False
        self.set_height()

    def set_height(self):
        #Khởi tạo ống mới với giá trị ngẫu nhiên trong khoảng 50 - 300
        self.height = random.randrange(50,300)
        self.top = self.height -self.pipe_top.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.pipe_top, (self.x, self.top))
        win.blit(self.pipe_bottom, (self.x, self.bottom))

    def attack(self, bird):
        #Thực hiện kiểm tra bird có đụng ống hay không?
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask,top_offset)

        if bottom_point or top_point:
            return True

        return False