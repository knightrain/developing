#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pygame
from pygame.locals import *
import xml.etree.ElementTree as xml

def load_resource_image(file):
    #try:
    resource = pygame.image.load(file).convert_alpha()
    #except pygame.error:
    #    raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return resource

def load_image(resource, pos_x, pox_y, width, height, number):
    return [resource.subsurface(
        Rect((pos_x + i * width, pox_y), (width, height))
        ) for i in xrange(number)]

def prepare_test_marios_info():
    width = 39
    height = 39
    resources = load_resource_image("mario/mario_01.jpg")
    still_image = load_image(resources, 0, 39*2, 39, 39, 1)[0]
    running_images = load_image(resources, 0, 39*2, 39, 39, 3)
    speaking_images = load_image(resources, 39*3, 39*2, 39, 39, 1)
    new_resources = pygame.Surface((width*3, height*2))
    color = pygame.Color("0xffffffff")
    new_resources.fill(color)
    for i in xrange(len(running_images)):
        new_resources.blit(running_images[i], (i*width, 0))
    for i in xrange(len(speaking_images)):
        new_resources.blit(speaking_images[i], (i*width, height))
    pygame.image.save(new_resources, "mario/marios.png")

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((640, 480), 0, 32)
    prepare_test_marios_info()

