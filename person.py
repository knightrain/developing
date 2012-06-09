#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

STILL = 0
MOVING = 1
SPEAKING = 2

def load_infos(xml):
    pass

class Person(pygame.sprite.Sprite):
    def __init__(self, name):
        self.name = name
        self.status = STILL
        self.xspeed = 0
        self.yspeed = 0

    def load_images(self, im_type, num, width, height):
        self.images[im_type] = [images.subsurface(i*width, 0, width, height)
                                for i in xrange(num)]

    def load_resouces(self, info):
        nums = info.image_nums
        width = info.image_width
        height = info.image_height

        for i in xrange(3):
            load_images(self, i, nums[i], width, height)

