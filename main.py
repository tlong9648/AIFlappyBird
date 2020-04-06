'''
// Người viết: Nguyễn Thành Long
// Ngày 5/4/2020
'''
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
#Hàm vẽ các giá trị trên cửa sổ trò chơi 
def draw_win(win, birds, pipes, base, background, score, generation):
    if generation == 0:
        generation = 1
    background.draw(win)
    for pipe in pipes:
        pipe.draw(win)

    for bird in birds:
        bird.draw(win)
    base.draw(win)
    score_text = "Score: {}".format(score)
    text = START_FONT.render(score_text, 1, (255,255,255))
    win.blit(text, (WIN_SIZE[0] -10 - text.get_width(), 15))

    info_text = "Generations: {}".format(generation-1)
    text = START_FONT.render(info_text, 1, (0,0,0))
    win.blit(text, (15, WIN_SIZE[1] -10 - text.get_height()))

    info_text = "Alive: {}".format(len(birds))
    text = START_FONT.render(info_text, 1, (0,0,0))
    win.blit(text, (WIN_SIZE[0] -10 - text.get_width(),
             WIN_SIZE[1] -10 - text.get_height()))
    
    pygame.display.update()


def main_play(genomes, config):

    global Win, generation
    win = Win
    generation += 1

    nets = []
    birds = []
    gen = []

    for gen_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(200, 320))
        gen.append(genome)
    BGround = Back_ground()
    
    base = Base(FLOOR)
    pipes = [Pipe(650)]
    run = True
    clock = pygame.time.Clock()
    scores = 0
    
    while run and len(birds) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # bird.move()
            
            # if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
            #     bird.jump()
            #     bird.y -=90
        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width():
                pipe_index = 1

        for index, bird in enumerate(birds):
            gen[index].fitness += 0.1
            bird.move()

            output = nets[birds.index(bird)].activate((bird.y, 
                                                        abs(bird.y - pipes[pipe_index].height),
                                                        abs(bird.y - pipes[pipe_index].bottom)))

            if output[0] > 0.5:
                bird.jump()


        BGround.move()
        base.move()                                            
        disappear = []
        addPipe = False
        for pipe in pipes:
            pipe.move()
            for bird in birds:
                if pipe.attack(bird):
                    ip = birds.index(bird)
                    gen[ip].fitness -= 1
                    nets.pop(ip)
                    gen.pop(ip)
                    birds.pop(ip)
            if pipe.x + pipe.pipe_top.get_width() < 0:
                disappear.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                addPipe = True

        if addPipe:
            scores += 1
            for genome in gen:
                genome.fitness +=5
            pipes.append(Pipe(500))

        for pipe_remove in disappear:
            pipes.remove(pipe_remove)
        for bird in birds:
            if bird.y + bird.image.get_height() -10 >= FLOOR or bird.y < 0:
                ip = birds.index(bird)
                nets.pop(ip)
                gen.pop(ip)
                birds.pop(ip)
        
        draw_win(Win, birds, pipes, base, BGround, scores, generation)

        # if scores > 30:
        #     pickle.dump(nets[0], open("best_nets.pickle", 'wb'))
        #     break
def run(config_file):

    config = neat.config.Config(genome_type=neat.DefaultGenome,
                    reproduction_type=neat.DefaultReproduction,
                    species_set_type= neat.DefaultSpeciesSet,
                    stagnation_type=neat.DefaultStagnation,
                    filename=config_file)
    p_net = neat.Population(config)
    p_net.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p_net.add_reporter(stats)

    winners = p_net.run(main_play, 5)
    print('\nBest genome: \n {!s}'.format(winners))
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_file=config_path)
