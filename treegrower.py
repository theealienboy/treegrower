#!/usr/bin/python
#
#       Copyright (C) 2013 Stephen M. Cameron
#       Author: Stephen M. Cameron
#
#       This file is part of treegrower.
#
#       treegrower is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       treegrower is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with treegrower; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

import pygame
import time
import os, sys
import random
import math
import time

screen_width = 1350 
screen_height = 750
niterations = 500
first_branch_chance = 100 # out of 1000
second_branch_chance = 80 # out of 1000
second_branch_max_age = 10
branch_angle = 10 
draw_every_nth_frame = 1
max_growth_age = 300
first_branch_max_age = 30
size_growth_rate = 0.02
size_growth_age_limit = 300
cell_offset = 2.0
max_age = 300 

black = (100, 100, 100)
white = (255, 255, 255)

screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.update()

def rotate_point(p, c, angle):
   x = p[0];
   y = p[1];
   cx = c[0];
   cy = c[1];
   rx = (x - cx) * math.cos(angle) - (y - cy) * math.sin(angle);
   ry = (x - cx) * math.sin(angle) + (y - cy) * math.cos(angle);
   return (rx + cx, ry + cy);

def hypot(p1, p2):
   return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) +
			(p1[1] - p2[1]) * (p1[1] - p2[1]));

def translate_point(p, x, y):
   return (p[0] + x, p[1] + y);

def deg_to_rad(angle):
   return angle * math.pi / 180.0;

cellindex = 0;

class cell:
   def __init__(self, x, y, size, angle, parent):
      global cellindex;
      self.x = x;
      self.y = y;
      self.age = 0;
      self.size = size;
      self.angle = angle;
      self.parent = parent;
      self.nchildren = 0;
      self.index = cellindex;
      cellindex = cellindex + 1;
   def draw(self):
      p1 = rotate_point((-1 * self.size, -1 * self.size), (0, 0), self.angle);
      p2 = rotate_point((-1 * self.size, 1 * self.size), (0, 0), self.angle);
      p3 = rotate_point((1 * self.size, 1 * self.size), (0, 0), self.angle);
      p4 = rotate_point((1 * self.size, -1 * self.size), (0, 0), self.angle);

      p1 = translate_point(p1, self.x, self.y);
      p2 = translate_point(p2, self.x, self.y);
      p3 = translate_point(p3, self.x, self.y);
      p4 = translate_point(p4, self.x, self.y);
      pygame.draw.line(screen, black, p1, p2, 1);
      pygame.draw.line(screen, black, p2, p3, 1);
      pygame.draw.line(screen, black, p3, p4, 1);
      pygame.draw.line(screen, black, p4, p1, 1);
   def grow(self):
      if (self.age > max_age):
         return;
      if (self.age < size_growth_age_limit):
         self.size += size_growth_rate;
      if (self.age < first_branch_max_age or self.age < second_branch_max_age):
         chance = random.randint(0, 1000);
         if ((chance < second_branch_chance and self.nchildren < 2 and self.age < second_branch_max_age) or (chance < first_branch_chance and self.nchildren < 1 and self.age < first_branch_max_age)):
	    random_angle = self.angle + deg_to_rad(-branch_angle + random.randint(0, branch_angle * 2));
	    tx = self.x + math.sin(self.angle) * self.size * cell_offset;
	    ty = self.y + -math.cos(self.angle) * self.size * cell_offset;
            newcell = cell(tx, ty, 1, random_angle, self.index);
	    add_cell(newcell);
            self.nchildren = self.nchildren + 1;
      if (self.parent >= 0):
         p = cells[self.parent];
         self.x = p.x + math.sin(p.angle) * p.size * cell_offset;
         self.y = p.y + -math.cos(p.angle) * p.size * cell_offset;
      self.age = self.age + 1;

cells = [];

def add_cell(newcell):
   cells.append(newcell);

def draw_cells():
   for c in cells:
      c.draw();

def grow_cells():
   for c in cells:
      c.grow();

screen.fill(white);   

add_cell(cell(screen_width / 2.0, screen_height * 0.9, 0.05, 0.0, -1));
add_cell(cell(screen_width / 4.0, screen_height * 0.9, 0.05, 0.0, -1));
add_cell(cell(3.0 * screen_width / 4.0, screen_height * 0.9, 0.05, 0.0, -1));

lastcell = cells[0];

for i in range(0, niterations):
   grow_cells();
   if ((i % draw_every_nth_frame) == 0):
      screen.fill(white);   
      draw_cells();
      pygame.display.update();

time.sleep(10);

