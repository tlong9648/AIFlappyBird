import pygame
import os 
import time
import sys
import neat
import pickle


pygame.font.init()

WIN_SIZE = (500, 700)

FLOOR = 620

START_FONT = pygame.font.SysFont("comicsans", 30)
END_FONT = pygame.font.SysFont("comicsans", 50)

Win = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("AI Flappy Bird with Log10200")

from bird import Bird
from pipe import Pipe
from base import Base
from BG import Back_ground

generation = 0
# bg_img = pygame.transform.scale(pygame.image.load(os.path.join("images","bg.png")).convert_alpha(), (600, 700))

def draw_win(win, birds, pipes, base, background, score, generation):
    if generation == 0:
        generation = 1
    background.draw(win)
    for pipe in pipes:
        pipe.draw(win)

    birds.draw(win)
    base.draw(win)
    score_text = "Score: {}".format(score)
    text = START_FONT.render(score_text, 1, (255,255,255))
    win.blit(text, (WIN_SIZE[0] -10 - text.get_width(), 15))

    info_text = "Generations: {}".format(generation-1)
    text = START_FONT.render(info_text, 1, (0,0,0))
    win.blit(text, (15, WIN_SIZE[1] -10 - text.get_height()))

    # info_text = "Alive: {}".format(len(birds))
    # text = START_FONT.render(info_text, 1, (0,0,0))
    # win.blit(text, (WIN_SIZE[0] -10 - text.get_width(),
    #          WIN_SIZE[1] -10 - text.get_height()))
    
    pygame.display.update()


def main_play():

    global Win, generation
    win = Win
    generation += 1

    bird = Bird(200,320)

    BGround = Back_ground()
    
    base = Base(FLOOR)
    pipes = [Pipe(650)]
    run = True
    clock = pygame.time.Clock()
    scores = 0
    
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # bird.move()
            
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                bird.jump()
                bird.y -=15
                

        bird.move()

        BGround.move()
        base.move()                                            
        disappear = []
        addPipe = False
        for pipe in pipes:
            pipe.move()
            if pipe.attack(bird):
                run = False
            
            if pipe.x + pipe.pipe_top.get_width() < 0:
                disappear.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                addPipe = True

        if addPipe:
            scores += 1
            pipes.append(Pipe(500))

        for pipe_remove in disappear:
            pipes.remove(pipe_remove)
        if bird.y + bird.image.get_height() -10 >= FLOOR or bird.y < 0:
            run = False
        
        draw_win(Win, bird, pipes, base, BGround, scores, generation)

        # if scores > 30:
        #     pickle.dump(nets[0], open("best_nets.pickle", 'wb'))
        #     break
if __name__ == "__main__":
    main_play()
