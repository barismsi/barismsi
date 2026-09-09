from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'assets'
def f(s,b=False,m=False):
 return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/'+('DejaVuSansMono' if m else 'DejaVuSans-Bold' if b else 'DejaVuSans')+'.ttf',s)
BG='#060a12'; BLUE='#49a7ff'; WHITE='#eaf3ff'; MUTED='#8b9eb8'
def base(w,h):
 im=Image.new('RGB',(w,h),BG); d=ImageDraw.Draw(im)
 d.ellipse((w*.5,-h*.1,w*1.05,h*.95),fill='#102c56')
 return im.filter(ImageFilter.GaussianBlur(95))
frames=[]
for n in range(64):
 im=base(1200,580); d=ImageDraw.Draw(im)
 for x in range(700,1200,32):
  for y in range(90,490,32):d.point((x,y),fill='#345277')
 d.line((52,66,1148,66),fill='#263448')
 d.text((52,30),'B / S',font=f(20,True),fill=WHITE)
 d.text((156,34),'BARISMSI  /  PERSONAL WORKSPACE',font=f(13,m=True),fill=MUTED)
 d.ellipse((1008,37,1016,45),fill=BLUE)
 d.text((1028,31),'IN PROGRESS',font=f(12,m=True),fill=BLUE)
 d.text((52,104),'01  /  FROM PIXELS TO PROGRAMS',font=f(15,m=True),fill=BLUE)
 d.text((45,139),'Barış.',font=f(116,True),fill=WHITE)
 d.text((54,294),'A creative eye.',font=f(32,True),fill=WHITE)
 d.text((54,338),'A new chapter in code.',font=f(32,True),fill=BLUE)
 d.text((55,402),'Learning C# from the ground up.',font=f(19),fill=MUTED)
 d.text((55,432),'Building Blender tools with Python.',font=f(19),fill=MUTED)
 a=2*math.pi*n/64; pts=[]
 for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:
  xx=x*math.cos(a)+z*math.sin(a); zz=-x*math.sin(a)+z*math.cos(a)
  yy=y*.87-zz*.49; zz=y*.49+zz*.87; q=88/(1+zz*.15)
  pts.append((905+xx*q,286+yy*q))
 edges=[(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
 light=Image.new('RGB',im.size,'black'); ld=ImageDraw.Draw(light)
 for i,j in edges:ld.line((pts[i],pts[j]),fill='#228cff',width=7)
 im=ImageChops.add(im,light.filter(ImageFilter.GaussianBlur(12))); d=ImageDraw.Draw(im)
 for i,j in edges:d.line((pts[i],pts[j]),fill='#62b6ff',width=2)
 for x,y in pts:d.rectangle((x-3,y-3,x+3,y+3),fill='#dbf3ff')
 d.rounded_rectangle((850,255,960,315),10,fill=BG,outline='#348df4',width=2)
 d.text((873,265),'C#',font=f(32,True),fill=WHITE)
 d.text((791,456),'CREATE. LEARN. REPEAT.',font=f(15,m=True),fill=BLUE)
 d.line((52,508,1148,508),fill='#263448')
 d.text((53,533),'CURRENT FOCUS',font=f(12,m=True),fill=MUTED)
 d.text((190,530),'C# fundamentals',font=f(16),fill=WHITE)
 d.text((756,533),'CREATIVE SIDE',font=f(12,m=True),fill=MUTED)
 d.text((886,530),'Python / Blender',font=f(16),fill=WHITE)
 frames.append(im)
frames[8].save(A/'workspace.png')
palette=frames[0].quantize(colors=64)
frames=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
frames[0].save(A/'workspace.gif',save_all=True,append_images=frames[1:],duration=85,loop=0,optimize=True)
for filename,number,title,subtitle,tag in [('mineshader.png','01','MineShader','Blender material workflow','BLENDER / PYTHON'),('color-reveal.png','02','Color Reveal','Selective color. Creative control.','BLENDER / PYTHON')]:
 im=base(760,280);d=ImageDraw.Draw(im)
 d.rounded_rectangle((1,1,758,278),15,outline='#29496c',width=2)
 d.text((30,24),tag,font=f(14,m=True),fill=BLUE)
 d.text((29,73),title,font=f(43,True),fill=WHITE)
 d.text((32,141),subtitle,font=f(20),fill=MUTED)
 d.text((32,229),'EXPLORE REPOSITORY  >',font=f(14,m=True),fill=BLUE)
 d.text((627,198),number,font=f(44,True),fill='#38618d')
 im.save(A/filename)
print('Generated hero and project cards')
