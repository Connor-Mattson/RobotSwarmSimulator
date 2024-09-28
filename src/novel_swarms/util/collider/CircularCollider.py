import pygame
import numpy as np
import math

class CircularCollider:
    def __init__(self, x, y, r, angle = None, v = None,dx=None,dy=None,da=None,friction=None,old_collide=None):
        self.x = x
        self.y = y
        self.dx=dx
        self.dy=dy
        self.da=da
        self.robot_friction=friction
        self.theta = angle
        self.vel = v
        self.r = r
        self.old_collide_agent=old_collide
        self.v = np.array([x, y, 0])
        self.collision_flag = False

    def update(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.v = np.array([x, y, 0])

    def flag_collision(self):
        self.collision_flag = True

    def collision_then_correction(self, other):
        dist_between_radii = self.dist(other)
        dist_difference = (self.r + other.r) - dist_between_radii
        #collide_point = np.array([self.x + (other.x-self.x)/2, self.y +(other.y-self.y)/2])
        collide_point_vector= other.v - self.v
        correction_vector = None
        #print("emtry",self.old_collide_agent)
        if dist_difference < 0 and not self.old_collide_agent:
            return None,None,None
        if dist_difference > 0:
            correction_vector = ((other.v - self.v) / (dist_between_radii + 0.001)) * (dist_difference + 0.01)
        #print(correction_vector)
        #print("right")
        other_dir = 0#self.get_direction_angle_coeff(collide_point_vector,other)
        self_dir = self.get_direction_angle_coeff(collide_point_vector)
        other_mag =1# np.linalg.norm(np.array([other.dx,other.dy,0]))
        self_mag =1# np.linalg.norm(np.array([self.dx,self.dy,0]))
        if correction_vector is None:
            other_dir=0
            self_dir=0
        angle = self.da+self.da*(-other_dir-self_dir) #self.robot_friction*(((self_dir/(np.pi/2))*self_mag*1)-((other_dir/(np.pi/2))*other_mag*0.5)) # (equal and opp reaction) - (external reaction)
        #print(angle)
        #print("correct ang",self.da,other_dir,self_dir)
        if correction_vector is not None:
            self.old_collide_agent= False #changing this to false was not tested, but seems to work
            #print("here")
        else:
            self.old_collide_agent= True
        #print("check",self.old_collide_agent)
        return correction_vector,angle,self.old_collide_agent
    
    def get_direction_angle_coeff(self,collide_point_vector,agent=None):
        if agent!=None:
            
            if np.cross(-collide_point_vector,-np.array([agent.dx,agent.dy,0]))[2]>0:
                return np.cross(-collide_point_vector/np.linalg.norm(collide_point_vector),np.array([agent.dx,agent.dy,0])/np.linalg.norm(np.array([agent.dx,agent.dy,0])))[2]
                
            elif np.cross(-collide_point_vector,-np.array([agent.dx,agent.dy,0]))[2]<0:
                return np.cross(-collide_point_vector/np.linalg.norm(collide_point_vector),np.array([agent.dx,agent.dy,0])/np.linalg.norm(np.array([agent.dx,agent.dy,0])))[2]
                
            else:
                return 0.000000001  
        if agent==None:
            agent=self
           
            if np.cross(-collide_point_vector,-np.array([agent.dx,agent.dy,0]))[2]>0:
                
                return np.cross(-collide_point_vector/np.linalg.norm(collide_point_vector),np.array([agent.dx,agent.dy,0])/np.linalg.norm(np.array([agent.dx,agent.dy,0])))[2]
                
            elif np.cross(-collide_point_vector,-np.array([agent.dx,agent.dy,0]))[2]<0:
                return np.cross(-collide_point_vector/np.linalg.norm(collide_point_vector),np.array([agent.dx,agent.dy,0])/np.linalg.norm(np.array([agent.dx,agent.dy,0])))[2]
               
            else:
                return 0.000000001  
    
    
    def get_angle_between(self,a,b):
        return np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
  
    
    def get_frontal_point(self):
        """
        Returns the location on the circumference that represents the "front" of the robot
        """
        return math.cos(self.theta) * self.r, math.sin(self.theta) * self.r, 0
    
    def dist(self, other):
        return np.linalg.norm(other.v - self.v)

    def draw(self, screen, color=(0, 255, 0)):
        if self.collision_flag:
            color = (255, 0, 0)
        pygame.draw.circle(screen, color, (self.x, self.y), self.r, 3)
