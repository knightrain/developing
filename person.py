#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

def load_infos(xml):
    pass

class Person(pygame.sprite.Sprite):
    def __init__(self, name):
        self.name = name
        self.state = "still" 
        self.images = {}
        self.xspeed = 0
        self.yspeed = 0

    def load_images(self, im_type, num, width, height):
        return [images.subsurface(i*width, 0, width, height)
                for i in xrange(num)]

    def load_resouces(self, info):
        for image_info in info.images_info:
            width = image_info.image_width
            height = image_info.image_height
            state = image_info.state
            num = image_info.subimage_num

            self.images[state] = [image_info.images.subsurface(i*width, 0, width, height)
                                  for i in xrange(num)]

    def set_status(self, state):
        self.state = state
        self.curr_images = self.images[state]

    def updage_speed(self, xspeed, yspeed):
        self.xspeed = xspeed
        self.yspeed = yspeed

    def update(self):
        self.rect.left += self.xspeed
        self.rect.top += self.yspeed
        self.order += 1
       	if self.order >= len(self.curr_images):
            self.order = 0 
        self.image = self.curr_images[self.order]


