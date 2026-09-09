from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math

ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'assets'
BG='#050912'; PANEL='#08111f'; BLUE='#43a5ff'; WHITE='#eef6ff'; MUTED='#8da3bd'; LINE='#294765'
def font(size,bold=False,mono=False):
    name='DejaVuSansMono' if mono else 'DejaVuSans-Bold' if bold else 'DejaVuSans'
    return ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/{name}.ttf',size)
def save(frames,path):
    palette=frames[0].quantize(colors=72)
    frames=[x.quantize(palette=palette,dither=Image.Dither.NONE) for x in frames]
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=90,loop=0,optimize=True)

frames=[]
cards=[('C#','LEARNING','FOUNDATIONS'),('PY','BUILDING','BLENDER TOOLS'),('3D','CREATING','MOTION & VISUALS')]
for n in range(54):
    im=Image.new('RGB',(1200,270),BG)
    glow=Image.new('RGB',im.size,'black'); gd=ImageDraw.Draw(glow)
    gx=150+(n/53)*900
    gd.ellipse((gx-180,-100,gx+180,370),fill='#0a3970')
    im=ImageChops.add(im,glow.filter(ImageFilter.GaussianBlur(75))); d=ImageDraw.Draw(im)
    d.text((32,21),'CREATIVE.STACK',font=font(13,mono=True),fill=BLUE)
    d.text((1015,21),'LIVE',font=font(12,mono=True),fill=BLUE)
    d.ellipse((1069,25,1077,33),fill=BLUE if n<28 else '#16446e')
    for i,(symbol,state,label) in enumerate(cards):
        x=30+i*390; y=58
        lift=int(5*math.sin(n/54*math.pi*2+i*1.5))
        d.rounded_rectangle((x,y+lift,x+360,y+lift+175),15,fill=PANEL,outline=BLUE if i==(n//18)%3 else LINE,width=2)
        d.rounded_rectangle((x+20,y+lift+21,x+91,y+lift+92),12,fill='#0d2038',outline='#286da9',width=2)
        box=d.textbbox((0,0),symbol,font=font(27,bold=True))
        d.text((x+55-(box[2]-box[0])/2,y+lift+39),symbol,font=font(27,bold=True),fill=WHITE)
        d.text((x+112,y+lift+27),state,font=font(12,mono=True),fill=BLUE)
        d.text((x+112,y+lift+55),label,font=font(17,bold=True),fill=WHITE)
        d.line((x+21,y+lift+119,x+338,y+lift+119),fill=LINE)
        width=int((100+220*((n+i*12)%54)/53)) if i==(n//18)%3 else 92+i*35
        d.rounded_rectangle((x+21,y+lift+143,x+21+width,y+lift+149),3,fill=BLUE)
        d.text((x+279,y+lift+135),'ACTIVE',font=font(10,mono=True),fill=MUTED)
    frames.append(im)
frames[9].save(A/'stack.png')
save(frames,A/'stack.gif')
print('Generated animated C# / Python / Blender stack')
