#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pygame
from pygame.locals import *

def load_resource_image(file):
    try:
        resource = pygame.image.load(file).convert_alpha()
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return resource

def load_image(resource, pos_x, pox_y, width, height, number):
    return [resource.subsurface(
        Rect((pos_x + i * width, pox_y), (width, height))
        ) for i in xrange(number)]

def prepare_test_person_info():
    resources = load_resource_image("mario/mario_01.jpg")
