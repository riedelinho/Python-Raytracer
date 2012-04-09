# -*- coding: utf-8 -*-
from PIL import Image
from objects import *
from geometry import *
from material import *
from light import *
from camera import *
import math
import sys

# Imagedetails
BACKGROUND_COLOR = Color(0, 0, 0)
imageWidth = 320
imageHeight = 240
imageFormat = "PNG"
imageMode = "RGB"
imageName = "raytracing.png"
if len(sys.argv) == 2 and sys.argv[1].endswith(".png"):
  imageName = sys.argv[1]
else:
  imageName = "raytracing.png"

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

# Class for raytracing of the image
class Raytracer(object):
  
  def __init__(self, _cam, _light):
    self.cam = _cam
    self.light = _light
    self.objectlist = []

  # Adds object to the objectlist
  def addObj(self, obj):
    self.objectlist.append(obj)
    
    
  # Raytraces and generates image
  def traceImage(self):
    print "Tracing image..."
    image = Image.new(imageMode, (imageWidth, imageHeight))

    
    for x in range(imageWidth):
      for y in range(imageHeight):
	
	ray = self.calcRay(x, y)
	y = imageHeight - y - 1
	color = BACKGROUND_COLOR
	maxdist = float('inf')
	for obj in self.objectlist:
	  hitdist = obj.intersectionParameter(ray)
	  
	  if hitdist:
	    if hitdist < maxdist:
	      maxdist = hitdist
	      
	      # Rest of objects
	      otherobjects = self.objectlist[:]
	      otherobjects.remove(obj)
	      
	      point = ray.pointAtParameter(hitdist)
	      directionToLight = self.light.pos - point
	      normal = obj.normalAt(point)
	      
	      #if self.light.shadowHit(ray, hitdist, otherobjects):
		#color = Color(128, 128, 128)
	      #else:
	      color += obj.material.calculateColor(directionToLight, normal, self.light.intensity, ray)
	      
	      
	      # reflektierendes objekt
	      #reflectedRay = Ray(point, ray.direction.reflect(normal))
	      #for reflectobj in otherobjects:
		#(reflecthitdist, hitobj) = reflectobj.intersectionParameter(reflectedRay)
		#if reflecthitdist:
		  #reflectColor = reflectobj.material.color
		  #color += reflectcolor
	
	image.putpixel((x,y), color.getTuple())
    print "...completed"
    image.save(imageName, imageFormat)
    image.show()
    
  
  # Calculates direction of the ray
  def calcRay(self, x, y):
    xcomp = self.cam.s.scale((x*self.cam.pixelWidth) - (self.cam.width/2))
    ycomp = self.cam.u.scale((y*self.cam.pixelHeight) - (self.cam.height/2))
    return Ray(self.cam.e, self.cam.f + xcomp + ycomp)
    

  def renderColor(self, maxdist, obj, ray):
    
    _maxdist = maxdist
    hitdist = obj.intersectionParameter(ray)
    
    if hitdist:
      if hitdist < _maxdist:
	_maxdist = hitdist
	
	otherobjects = self.objectlist[:]
	otherobjects.remove(obj)
	
	point = ray.pointAtParameter(hitdist)
	directionToLight = self.light.pos - point
	normal = obj.normalAt(point)
	color = obj.material.color * obj.material.ambient
	color += obj.material.calculateColor(directionToLight, normal, self.light.intensity, ray)
    else:
      color = BACKGROUND_COLOR
      
    return (color, _maxdist)

if __name__=="__main__":
  
  print "#############START#############"
  # Image informations
  print "Imagesize: %sx%s" % (imageWidth, imageHeight)
  print "Imageformat: %s" % imageFormat
  print "Imagename: %s" % imageName
  print "ImageMode: %s" % imageMode
  
  #----- Objects START
  
  # Red sphere
  redcenter = Point(2.5, 3, -10)
  redradius = 1
  redcolor = Color(255, 0, 0)
  redmaterial = Material(0.3, 0.8, 0.1, 0.05, redcolor)
  redsphere = Sphere(redcenter, redradius, redcolor, redmaterial)
  
  # Green sphere
  greencenter = Point(-2.5, 3, -10)
  greenradius = 1.5
  greencolor = Color(0, 255, 0)
  greenmaterial = Material(0.3, 0.8, 0.1, 0.05, greencolor)
  greensphere = Sphere(greencenter, greenradius, greencolor, greenmaterial)
  
  # Blue sphere
  bluecenter = Point(0,7,-10)
  blueradius = 2
  bluecolor = Color(0, 0, 255)
  bluematerial = Material(0.3, 0.8, 0.1, 0.05, bluecolor)
  bluesphere = Sphere(bluecenter, blueradius, bluecolor, bluematerial)
  
  # Gray Plane
  #planepoint = Point(0, 0, 0)
  #planenormal = Vector(10, 0, 0)
  #planecolor = Color(128, 128, 128)
  #planematerial = Material(1, 0.5, 0.5, 0.05, planecolor)
  #plane = Plane(planepoint, planenormal, planecolor)
  
  # Yellow Triangle
  #yellowpoints = [Point(3, 2, 0), Point(3, 5, 0), Point(6, 4, 2)]
  #yellowcolor = (255, 255, 0)
  #yellowtriangle = Triangle(yellowpoints[0], yellowpoints[1], yellowpoints[2], yellowcolor)
  
  #----- Objects END
  
  # Light & camera-initialization
  lightpos = Point(30, 30, 10)
  lightintensity = 0.5
  light = Light(lightpos, lightintensity)
  cam = Camera(Vector(0, 1.8, 10), Vector(0, 1, 0), Vector(0, 3, 0), math.pi/4.)
  raytracer = Raytracer(cam, light)
  
  # Creating objects
  #raytracer.addObj(plane)
  raytracer.addObj(redsphere)
  raytracer.addObj(greensphere)
  raytracer.addObj(bluesphere)
  #raytracer.addObj(yellowtriangle)
  
  # Tracing image with added objects
  raytracer.traceImage()
  
  print "###############END###############"
