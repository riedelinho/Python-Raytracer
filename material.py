# -*- coding: utf-8 -*-
import math

# Color class
class Color(object):
  
  def __init__(self, _r, _g, _b):
    self.r = _r
    self.g = _g
    self.b = _b
    
  def __repr__(self):
    return 'RGB(%s, %s, %s)' % (self.r, self.g, self.b)
    
  def __add__(self, other):
    return Color(self.r + other.r, self.g + other.g, self.b + other.b)
    
  def __mul__(self, fac):
    return Color(self.r * fac, self.g * fac, self.b * fac)
    
  # Returns RGB as tuple
  def getTuple(self):
    return (int(self.r), int(self.g), int(self.b))

# Class for the material of the object
class Material(object):
  
  def __init__(self, _ambient, _diffus, _specular, _n, _color):
    self.ambient = _ambient
    self.diffus = _diffus
    self.specular = _specular
    self.n = _n
    self.color = _color
  
  # calculates color of point on object
  # more details: http://de.wikipedia.org/wiki/Phong-Beleuchtungsmodell
  # more datails: Folie 2 Seite 18
  def calculateColor(self, directionToLight, normal, lightIntensity, rayToPoint):
    
    #ambientPart = self.color * self.ambient
    diffusPart = self.color * (self.diffus * directionToLight.normalized().dot(normal.normalized())) * lightIntensity
    specularPart = self.color * ((self.n+2)/(2*math.pi)) * (directionToLight.normalized().reflect(normal.normalized()).dot(rayToPoint.direction.normalized() * -1)**self.n * self.specular) * lightIntensity
    
    colorout = diffusPart + specularPart
    return colorout    