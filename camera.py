# -*- coding: utf-8 -*-
import math

# Class for initialisation of the Camera
class Camera(object):
  
  def __init__(self, _e, _up, _c, _fov):
    self.e = _e  # viewpoint
    self.up = _up # Up-Vector
    self.c = _c # looks into point
    self. fov = _fov     # opening angle
    
    # Coordinate-System
    # Camera, positioned in origin, with look in direction -z returns the
    # Camera-Eye-Coordinate-System
    self.f = (self.c - self.e).normalized()
    self.s = self.f.cross(self.up).normalized() 
    self.u = self.s.cross(self.f)
    
    # Observer-geometry
    self.alpha = self.fov/2.
    self.height = 2.*math.tan(self.alpha)
    self.width = self.height * (imageWidth / imageHeight)
    self.pixelWidth = self.width / (imageWidth - 1)
    self.pixelHeight = self.height / (imageHeight - 1)
    
    print "Camera initialised"