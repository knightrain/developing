#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pygame
from pygame.locals import *
import xml.etree.ElementTree as xml
from xml.dom import minidom

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

def prepare_test_marios_info():
    width = 39
    height = 39
    resources = load_resource_image("test/mario/mario_01.jpg")
    still_image = load_image(resources, 0, 39*2, 39, 39, 1)[0]
    running_images = load_image(resources, 0, 39*2, 39, 39, 3)
    speaking_images = load_image(resources, 39*3, 39*2, 39, 39, 1)
    new_resources = pygame.Surface((width*3, height*3))
    color = pygame.Color("0xffffffff")
    new_resources.fill(color)
    new_resources.blit(still_image, (0, 0))
    for i in xrange(len(running_images)):
        new_resources.blit(running_images[i], (i*width, height))
    for i in xrange(len(speaking_images)):
        new_resources.blit(speaking_images[i], (i*width, height*2))
    pygame.image.save(new_resources, "test/mario/marios.png")

    # build persion xml
    root = xml.Element("Person")
    node_name = xml.SubElement(root, "name")
    node_name.text = "Mario"
    node_image = xml.SubElement(root, "image")
    node_image.set("path", "test/mario/marios.png")
    node_states = xml.SubElement(root, "states")

    tree = xml.ElementTree(root)
    tree.write("test/page.xml")

    rough_string = xml.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    print reparsed.toprettyxml(indent="    ")
    

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((640, 480), 0, 32)
    prepare_test_marios_info()

