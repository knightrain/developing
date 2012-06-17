#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import xml.etree.ElementTree as xml
from xml.dom import minidom 

def create_person(xml_file):
    with open(xml_file, 'r') as f:
        tree = xml.parse(f)
        
    rough_string = xml.tostring(tree.getroot(), 'utf-8')
    reparsed = minidom.parseString(rough_string)
    print reparsed.toprettyxml(indent="    ")

    root = tree.getroot()
    if root.tag != 'Person':
        return
    
    name = tree.find('./name').text
    person = Person(name)
    image_file = tree.find('./image').attrib.get('path')
    resources = pygame.image.load(image_file)
    resources.set_colorkey(0xffffff)
    print resources.get_colorkey()
    resources = resources.convert()

    for node in tree.findall('./state'):
        left = int(node.attrib.get('X'))
        top = int(node.attrib.get('Y'))
        width = int(node.attrib.get('width'))
        height = int(node.attrib.get('height'))
        num = int(node.attrib.get('num'))
        state = node.text
        person.load_state_images(state, resources, left, top, width, height, num)

    return person
    

class Person(pygame.sprite.Sprite):
    def __init__(self, name):
        self.name = name
        self.state = "still" 
        self.images = {}
        self.xspeed = 0
        self.yspeed = 0
        self.rect = None
        self.sound = None

    def load_state_images(self, state, resources, left, top, width, height, num):
        self.images[state] = [resources.subsurface(left+i*width, top, width, height)
                              for i in xrange(num)]

    def set_state(self, state):
        self.state = state
        self.order = 0
        self.curr_images = self.images[state]

    def update_speed(self, xspeed, yspeed):
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
