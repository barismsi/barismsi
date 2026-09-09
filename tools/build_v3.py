from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assets'; A.mkdir(exist_ok=True)
BG='#050912'; PANEL='#08111f'; BLUE='#43a5ff'; WHITE='#eef6ff'; MUTED='#8da3bd'; LINE='#294765'
def font(size,bold=False,mono=False):
    name='DejaVuSansMono' if mono else 'DejaVuSans-Bold' if bold else 'DejaVuSans'
    return ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/{name}.ttf',size)
def canvas(w,h):
    im=Image.new('RGB',(w,h),BG)
    glow=Image.new('RGB',(w,h),'black'); gd=ImageDraw.Draw(glow)
    gd.ellipse((w*.42,-h*.55,w*1.08,h*1.25),fill='#12396d')
    return ImageChops.add(im,glow.filter(ImageFilter.GaussianBlur(95)))
def save_gif(frames,path,duration=90):
    pal=frames[0].quantize(colors=72)
    frames=[im.quantize(palette=pal,dither=Image.Dither.NONE) for im in frames]
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=duration,loop=0,optimize=True)

frames=[]
steps=[('01','FOUNDATIONS','ACTIVE'),('02','CONTROL FLOW','NEXT'),('03','METHODS','NEXT'),('04','FIRST PROJECT','NEXT')]
xs=[126,430,736,1040]
for n in range(48):
    im=canvas(1200,300); d=ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,1198,298),18,fill=PANEL,outline=LINE,width=2)
    d.text((34,26),'LEARNING.LOG',font=font(14,mono=True),fill=BLUE)
    d.text((34,58),'One concept at a time.',font=font(30,bold=True),fill=WHITE)
    d.text((786,67),'STATUS  /  BUILDING THE FOUNDATION',font=font(13,mono=True),fill=MUTED)
    d.line((126,178,1040,178),fill=LINE,width=3)
    pulse=(math.sin(n/48*math.pi*2)+1)/2
    travel=(n%48)/47
    px=126+(430-126)*travel
    d.line((126,178,px,178),fill=BLUE,width=4)
    for idx,((num,label,state),x) in enumerate(zip(steps,xs)):
        active=idx==0
        r=12+int(4*pulse) if active else 10
        if active:
            glow=Image.new('RGB',im.size,'black');g=ImageDraw.Draw(glow)
            g.ellipse((x-r-12,178-r-12,x+r+12,178+r+12),fill='#086bc9')
            im=ImageChops.add(im,glow.filter(ImageFilter.GaussianBlur(18))); d=ImageDraw.Draw(im)
        d.ellipse((x-r,178-r,x+r,178+r),fill=BLUE if active else BG,outline=BLUE if active else '#49647d',width=3)
        d.text((x-18,125),num,font=font(14,mono=True),fill=BLUE if active else MUTED)
        box=d.textbbox((0,0),label,font=font(13,bold=True))
        d.text((x-(box[2]-box[0])/2,213),label,font=font(13,bold=True),fill=WHITE if active else MUTED)
        box=d.textbbox((0,0),state,font=font(11,mono=True))
        d.text((x-(box[2]-box[0])/2,245),state,font=font(11,mono=True),fill=BLUE if active else '#587087')
    frames.append(im)
save_gif(frames,A/'learning.gif')

projects=[
 ('mineshader.gif','01','MineShader Enhancer','Blender material workflow tool','PYTHON / BLENDER','ADJUST · REFINE · CREATE'),
 ('color-reveal.gif','02','Color Reveal','Selective color. Creative control.','PYTHON / BLENDER','MASK · REVEAL · ANIMATE')
]
for filename,num,title,subtitle,tag,verbs in projects:
    frames=[]
    for n in range(42):
        im=canvas(760,310); d=ImageDraw.Draw(im)
        d.rounded_rectangle((1,1,758,308),18,fill=PANEL,outline=LINE,width=2)
        d.text((30,25),tag,font=font(13,mono=True),fill=BLUE)
        dot=90+int(150*(math.sin(n/42*math.pi*2)+1)/2)
        d.ellipse((700,27,709,36),fill=(35,dot,255))
        d.text((30,76),title,font=font(38,bold=True),fill=WHITE)
        d.text((31,137),subtitle,font=font(19),fill=MUTED)
        d.text((31,181),verbs,font=font(12,mono=True),fill='#5e81a5')
        scan=225+(n/41)*32
        glow=Image.new('RGB',im.size,'black');gd=ImageDraw.Draw(glow)
        gd.rectangle((20,scan-10,740,scan+10),fill='#0b4c91')
        im=ImageChops.add(im,glow.filter(ImageFilter.GaussianBlur(16))); d=ImageDraw.Draw(im)
        d.line((26,scan,734,scan),fill=BLUE,width=1)
        for j in range(8):
            x=565+((j*31+n*5)%150); y=78+((j*43+n*3)%100)
            d.rectangle((x,y,x+3+(j%3)*2,y+3+(j%3)*2),fill=['#1b6eb8','#43a5ff','#9bd3ff'][j%3])
        d.text((31,263),'OPEN PROJECT  >',font=font(13,mono=True),fill=BLUE)
        d.text((657,240),num,font=font(40,bold=True),fill='#31577d')
        frames.append(im)
    save_gif(frames,A/filename,100)

frames=[]
for n in range(48):
    im=canvas(1200,190); d=ImageDraw.Draw(im)
    d.line((50,20,1150,20),fill=LINE)
    d.text((50,49),'GOOD THINGS START WITH CURIOSITY.',font=font(25,bold=True),fill=WHITE)
    d.text((51,91),'The profile grows as the work grows.',font=font(16),fill=MUTED)
    phase=n/48*math.pi*2
    for j in range(22):
        x=780+j*16; y=103+22*math.sin(phase+j*.45)
        d.rectangle((x,y,x+5,y+5),fill=['#164c7d','#2589d8','#65baff'][j%3])
    d.text((50,139),'barismsi@github:~$ still_building',font=font(14,mono=True),fill=BLUE)
    d.rectangle((376,141,385,157),fill=BLUE if n<24 else PANEL)
    frames.append(im)
save_gif(frames,A/'footer.gif')
print('Generated animated learning, project and footer assets')
