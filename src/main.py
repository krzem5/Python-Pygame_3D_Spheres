import math
import os
import pygame
import sys



def rotate2d(pos,rad):x,y=pos;s,c=math.sin(rad),math.cos(rad);return x*c-y*s,y*c+x*s
class Camera:
	def __init__(self,pos=(0,0,0),rot=(0,0)):self.pos,self.rot=list(pos),list(rot)
	def events(self,event):
		if event.type==pygame.MOUSEMOTION:
			x,y=event.rel
			x/=900;y/=900
			self.rot[0]+=y;self.rot[1]+=x
	def update(self,direction,key):
		s=direction*10
		if key[pygame.K_SPACE]:self.pos[1]-=s
		if key[pygame.K_LSHIFT]:self.pos[1]+=s
		x,y=s*math.sin(self.rot[1]),s*math.cos(self.rot[0])
		if key[pygame.K_w]:self.pos[0]+=x;self.pos[2]+=y
		if key[pygame.K_s]:self.pos[0]-=x;self.pos[2]-=y
		if key[pygame.K_a]:self.pos[0]-=y;self.pos[2]+=x
		if key[pygame.K_d]:self.pos[0]+=y;self.pos[2]-=x

A,B=10,18
points=[(0,-1,0)]
for zRot in range(A,180,A):
	X,y=rotate2d((0,-1),zRot/180*math.pi)
	for yRot in range(0,360,B):
		z,x=rotate2d((0,X),yRot/180*math.pi)
		points+=[(x,y,z)]
points+=[(0,1,0)]
a=len(range(A,180,A)); b=len(range(0,360,B))
n=len(points)-1; n2=b*(a-1)
po=[]
for i in range(1,b+1):
	if i==b: po+=[(0,i,1)]
	else: po+=[(0,i,i+1)]
for j in range(0,(a-1)*b,b):
	for i in range(1,b+1):
		if i==b: po+=[(i+j,i+b+j,i+1+j,1+j)]
		else: po+=[(i+j,i+b+j,i+b+1+j,i+1+j)]
for i in range(1,b+1):
	if i==b: po+=[(n,i+n2,1+n2)]
	else: po+=[(n,i+n2,i+1+n2)]
class Sphere:
	vertices=points
	faces=po
	colors=(0,0,0),(255,255,0)
	def __init__(self,pos=(0,0,0)):
		x,y,z=pos
		self.verts=[(x+X/2,y+Y/2,z+Z/2) for X,Y,Z in self.vertices]
pygame.init()
w,h=800,600;fov=min(w,h)
os.environ['SDL_VIDEO_CENTERED']= '1'
pygame.display.set_caption('3D blocks')
scr=pygame.display.set_mode((w,h))
clock=pygame.time.Clock()
cam=Camera((0,0,-5))
pygame.event.get;pygame.mouse.get_rel()
pygame.mouse.set_visible(0);pygame.event.set_grab(1)
spheres=[]
spheres=[Sphere((x,0,z)) for x,z in ((-1,0),(0,0),(1,0))]
rot=0
while True:
	dt=clock.tick()/1000
	rot+=math.pi*dt*0.5
	for evt in pygame.event.get():
		if evt.type==pygame.QUIT:pygame.quit();sys.exit()
		if evt.type==pygame.KEYDOWN:
			if evt.key==pygame.K_ESCAPE:pygame.quit();sys.exit();
		cam.events(evt)
	scr.fill((128,128,128))
	face_l=[];face_color=[];depth=[]
	for obj in spheres:
		vrt_l=[];screen_crds=[]
		for x,y,z in obj.verts:
			x,z=rotate2d((x,z),rot)
			x-=cam.pos[0]; y-=cam.pos[1]; z-=cam.pos[2]
			x,z=rotate2d((x,z),cam.rot[1])
			y,z=rotate2d((y,z),cam.rot[0])
			vrt_l+=[(x,y,z)]
			f=fov/z if z else fov; x,y=x*f,y*f
			screen_crds+=[(w//2+int(x),h//2+int(y))]
		for f in range(len(obj.faces)):
			face=obj.faces[f]
			on_screen=False
			for i in face:
				x,y=screen_crds[i]
				if vrt_l[i][2]>0 and x>0 and x<w and y>0 and y<h:on_screen=True;break
			if on_screen:
				coords=[screen_crds[i] for i in face]
				face_l+=[coords]
				face_color+=[obj.colors[f%2]]
				depth+=[sum(vrt_l[i][2] for i in face)/len(face)]
	order=sorted(range(len(face_l)),key=lambda i:depth[i],reverse=1)
	for i in order:
		try:pygame.draw.polygon(scr,face_color[i],face_l[i])
		except:pass
	pygame.display.flip()
	key=pygame.key.get_pressed()
	cam.update(dt,key)
