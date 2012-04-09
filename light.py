# -*- coding: utf-8 -*-
from objects import *

# Class of the lighting
class Light(object):
  
  def __init__(self, _pos, _intencity):
    self.pos = _pos # point
    self.intensity = _intencity
    
  # Check, wheather the ray from object to lighting hits another object
  def shadowHit(self, ray, hitdist, objectlist):
    point = ray.pointAtParameter(hitdist)
    directionToLight = self.pos - point
    
    for obj in objectlist:
      ray = Ray(point, directionToLight)
      hit = obj.intersectionParameter(ray)
      
      if hit:
	return True
    return False
      
