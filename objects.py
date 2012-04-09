# -*- coding: utf-8 -*-
import math
import geometry


# Ray class
# A ray is defined with his origin and is normalised direction
class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin # point
        self.direction = direction.normalized() # vector

    def __repr__(self):
        return 'Ray(%s,%s)' % (repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + self.direction.scale(t)



#Sphere class
class Sphere(object):
    def __init__(self, center, radius, color, material):
        self.center = center # point
        self.radius = radius # scalar
        self.color = color
        self.material = material
        print "Object added: %s" % self

    def __repr__(self):
        return 'Sphere(%s, R(%s), Color(%s)' % (repr(self.center), self.radius, self.color)

    def intersectionParameter(self, ray):
        
        co = self.center - ray.origin
        v = co.dot(ray.direction)
        discriminant = (self.radius * self.radius) - (co.dot(co) - v*v)
        if discriminant < 0:
            return None
        else:
            return (v - math.sqrt(discriminant), self)

    # returns color of the sphere
    def getColor(self):
      return self.color

    def normalAt(self, p):
        return (p - self.center).normalized()
        
# Plane class
class Plane(object):
    def __init__(self, point, normal, color):
        self.point = point # point
        self.normal = normal.normalized() # vector
        self.color = color
        print "Object added: %s" % self

    def __repr__(self):
        return 'Plane(%s,%s)' % (repr(self.point), repr(self.normal))

    def intersectionParameter(self, ray):
        op = ray.origin - self.point
        a = op.dot(self.normal)
        b = ray.direction.dot(self.normal)
        if b:
            return -a/b
        else:
            return None

    # Returns color of the plane
    def normalAt(self, p):
        return self.normal
        
    def getColor(self):
      return self.color


# Triangle class
class Triangle(object):
    def __init__(self, a, b, c, color):
        self.a = a # point
        self.b = b # point
        self.c = c # point
        self.u = self.b - self.a # direction vector
        self.v = self.c - self.a # direction vector
        self.color = color
        print "Object added: %s" % self

    def __repr__(self):
        return 'Triangle(%s,%s,%s)' % (repr(self.a), repr(self.b), repr(self.c))

    def intersectionParameter(self, ray):
        w = ray.origin - self.a
        dv = ray.direction.cross(self.v)
        dvu = dv.dot(self.u)
        if dvu == 0.0:
            return None
        wu = w.cross(self.u)
        r = dv.dot(w) / dvu
        s = wu.dot(ray.direction) / dvu
        if 0<=r and r<=1 and 0<=s and s<=1 and r+s <=1:
            return wu.dot(self.v) / dvu
        else:
            return None
         
    def normalAt(self, p):
        return self.u.cross(self.v).normalized()
        
    def getColor(self):
      return self.color



class CheckerboardMaterial(object):
    def __init__(self):
        self.baseColor = (1,1,1)
        self.otherColor = (0,0,0)
        self.ambientCoefficient = 1.0 
        self.diffuseCoefficient =  0.6
        self.specularCoefficient = 0.2
        self.checkSize = 1

    def baseColourAt(self, p):
        v = Vector(p)
        v.scale(1.0 / self.checkSize)
        if (int(abs(v.x) + 0.5) + int(abs(v.y) + 0.5) + int(abs(v.z) + 0.5)) % 2:
            return self.otherColour
        return self.baseColour
