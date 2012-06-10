#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pygame
from pygame.locals import *
import speak

def read_script(speaker):
    text = speaker.preprocess_str(u"我爱你")
    nsamps, channel = speaker.speak_words(pygame.mixer, text)
    sound_length = 1000*nsamps/speaker.framerate
    return channel
    #file_object = open('script.txt')
    #try:
    #    for line in file_object:
    #        process line
    #finally:
    #    file_object.close( )
    

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)

    background = pygame.image.load("mario/mario_background_01.png").convert()
    background = pygame.transform.smoothscale(background, (640, 480))
    screen.blit(background, (0, 0))

    resources = load_resource_image("mario/mario_01.jpg")
    mario = Mario(resources);
    mario.status = MOVING
    princess = Princess(resources);

    speaker = speak.Speaker()
    pygame.mixer.init(speaker.framerate, speaker.sampwidth*8, speaker.nchannels, 4096)

    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                return

        screen.blit(background, (0, 0))

        if  mario.status == MOVING and mario.rect.right >= princess.rect.left:
            mario.status = SPEAKING
            mario.sound = read_script(speaker)
        elif mario.status == SPEAKING and mario.speech_end == 1:
            mario.status == STILL

        mario.update()
        screen.blit(mario.image, mario.rect)
        princess.update()
        screen.blit(princess.image, princess.rect)

        pygame.display.update()

        clock.tick(30)

if __name__ == '__main__':
	main()
