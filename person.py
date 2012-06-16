#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import xml.etree.ElementTree as xml
from xml.dom import minidom 

def create_person(xml_file):
    with open(xml_file, 'rt') as f:
        tree = xml.parse(f)
        
    rough_string = xml.tostring(tree.getroot(), 'utf-8')
    reparsed = minidom.parseString(rough_string)
    print reparsed.toprettyxml(indent="    ")

    root = tree.getroot()
    if root.tag != 'Person':
        return
    
    name = tree.find('./name')
    print name.text
    person = Persion(name.text)
    image_file = tree.find('./images').attrib.get('path')
    resources = pygame.image.load(image_file)
    for node in tree.findall('./state'):
        width = image_info.image_width
        height = image_info.image_height
        state = image_info.state
        num = image_info.subimage_num
        person.load
        print node.text
    

class Person(pygame.sprite.Sprite):
    def __init__(self, name):
        self.name = name
        self.state = "still" 
        self.images = {}
        self.xspeed = 0
        self.yspeed = 0

    def load_images(self, images, im_type, num, width, height):
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

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((640, 480), 0, 32)
    create_person('test/mario.xml')
