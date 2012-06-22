#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pygame
from pygame.locals import *
import speak
import person

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
    
def build_name_tab(size, color, radius=10):
    tab = pygame.Surface(size)
    rect = tab.get_rect()
    colorkey = (255-color[0],255-color[1],255-color[2])
    tab.fill(colorkey)
    tab.set_colorkey(colorkey)
    pygame.draw.circle(tab, color, (radius, radius), radius)
    pygame.draw.circle(tab, color, (rect[2]-radius, radius), radius)
    pygame.draw.rect(tab, color,(radius, 0, rect[2]-(2*radius), radius))
    pygame.draw.rect(tab, color,(0, radius, rect[2], rect[3]-radius))
    tab.set_alpha(125)
    return tab

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)

    background = pygame.image.load("test/mario/mario_background.png").convert()
    screen_speed = 10
    screen_x = 0
    buf_scr = pygame.Surface(background.get_size())
    buf_scr.blit(background, (0, 0))

    mario = person.create_person('test/mario.xml')
    princess = person.create_person('test/princess.xml');

    mario.set_state('moving')
    mario.rect = Rect(100, 307, 90, 90)
    mario.update_speed(11, 0)

    princess.set_state('still')
    princess.rect = Rect(1200, 300, 90, 90)

    speaker = speak.Speaker()
    pygame.mixer.init(speaker.framerate, speaker.sampwidth*8, speaker.nchannels, 4096)

    portrait = None
    text_bg = pygame.Surface((640, 120))
    ar = pygame.PixelArray(text_bg)
    text_bg_color = (50, 50, 192)
    ar[:] = text_bg_color
    del ar
    text_bg.set_alpha(125)

    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                return

        buf_scr.blit(background, (0, 0))

        if  mario.state == 'moving' and mario.rect.right >= princess.rect.left:
            mario.update_speed(0, 0)
            mario.set_state('speaking')
            sound = read_script(speaker)
            portrait = mario.get_portrait();
            portrait = pygame.transform.smoothscale(portrait, (105,240))
        elif mario.state == 'speaking' and not sound.get_busy():
            mario.set_state('still')
            portrait = None

        mario.update()
        buf_scr.blit(mario.image, mario.rect)
        princess.update()
        buf_scr.blit(princess.image, princess.rect)

        if (screen_x < background.get_width() - 640) :
            screen_x += screen_speed
        screen.blit(buf_scr.subsurface((screen_x, 0, 640, 480)), (0, 0))

        if portrait != None:
            font = pygame.font.Font(None, 30)
            text = mario.name
            size = font.size(text)
            fr = font.render(text, 0, (255,255,255))
            tab = build_name_tab((size[0]+10, size[1]+5), text_bg_color)
            screen.blit(tab, (105, 360-tab.get_height()))
            screen.blit(fr, (110, 360-fr.get_height()-1))
            screen.blit(text_bg, (0, 360, 640, 120))
            screen.blit(portrait, (0, 240, 105, 240))
            font = pygame.font.Font(os.environ['SYSTEMROOT'] + '\\Fonts\\simkai.ttf', 30)
            fr = font.render(u'我爱你', 0, (255,255,255))
            screen.blit(fr, (110, 360+10))

        pygame.display.update()

        clock.tick(30)

if __name__ == '__main__':
	main()
