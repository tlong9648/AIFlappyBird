import pygame
import os
import numpy as np 

bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("images","bird" + str(x) + ".png"))) for x in range(1,4)]
def blitRotateCenter(win, image, coordinates, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = coordinates).center)

    win.blit(rotated_image, new_rect.topleft)

class Bird():

    MAX_ROTATION = 25
    IMGS = bird_images
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.image_count = 0
        self.image = self.IMGS[0]
        self.degree = 0
        self.tick_count = 0
        self.height = self.y
        self.tilt = 0

    def draw(self, win):
        self.image_count += 1

        if self.image_count <= self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.image_count <= self.ANIMATION_TIME*2:
            self.image = self.IMGS[1]
        elif self.image_count <= self.ANIMATION_TIME*3:
            self.image = self.IMGS[2]
        elif self.image_count <= self.ANIMATION_TIME*4:
            self.image = self.IMGS[1]
        elif self.image_count == self.ANIMATION_TIME*4 + 1:
            self.image = self.IMGS[0]
            self.image_count = 0

        
        if self.degree <= -80:
            self.image = self.IMGS[1]
            self.image_count = self.ANIMATION_TIME*2


        blitRotateCenter(win, self.image, (self.x, self.y), self.tilt)

    def jump(self):
        self.degree = -10.5
        self.tick_count = 0
        self.height = self.y
        
        

    def move(self):

        self.tick_count += 1

        shift = 1.5*(self.tick_count)**2 + self.degree*(self.tick_count)

        if shift >= 16:
            shift = (shift/ abs(shift)) * 16

        if shift < 0:
            shift -= 2

        self.y = self.y + shift

        if shift < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def get_mask(self):

        return pygame.mask.from_surface(self.image)


