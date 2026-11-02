from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random, math
P=Path(__file__).parent/'public'/'assets'; P.mkdir(exist_ok=True,parents=True)
random.seed(24)

def rect(d, box, color): d.rectangle(box,fill=color)
def pximg(w,h): return Image.new('RGBA',(w,h),(0,0,0,0))
def save_scaled(img, filename, scale=3):
    img=img.resize((img.width*scale,img.height*scale),Image.Resampling.NEAREST); img.save(P/filename)

# Backdrops at 480 x 270, upscale 2x. Each original composition.
def bg(i,name):
    im=Image.new('RGB',(480,270)); d=ImageDraw.Draw(im)
    palettes=[('#74c8fb','#afe5fe','#e4f6fd'),('#19143c','#433260','#8e5473'),('#2b2b66','#574e88','#df91a0')]
    cols=palettes[i]
    for y in range(270):
        t=y/270; c1=tuple(int(cols[0][k:k+2],16) for k in (1,3,5)); c2=tuple(int(cols[1][k:k+2],16) for k in (1,3,5))
        col=tuple(int(c1[j]*(1-t)+c2[j]*t) for j in range(3));d.line((0,y,480,y),fill=col)
    if i==0:
        d.ellipse((364,23,426,85),fill='#fff7b3'); d.ellipse((373,32,420,79),fill='#ffdd7c')
        for x,y,s in [(31,46,1.0),(160,66,.75),(299,37,.9),(414,99,.85)]:
            d.ellipse((x,y,x+40*s,y+19*s),fill='#e9fcff');d.ellipse((x+11*s,y-10*s,x+33*s,y+13*s),fill='#fff');d.rectangle((x+6*s,y+8*s,x+57*s,y+18*s),fill='#e8fbff')
        mountains=[(0,174,80,88),(70,180,130,110),(182,189,105,86),(285,179,110,104),(379,182,100,75)]
        for x,y,w,h in mountains:
            d.polygon([(x,y+h),(x+w*.55,y-h*.42),(x+w,y+h)],fill='#81b8df')
            d.polygon([(x+w*.55,y-h*.42),(x+w*.74,y+h*.1),(x+w*.37,y+h*.02)],fill='#a5d6e7')
        d.ellipse((-96,173,210,345),fill='#60b9a0');d.ellipse((115,179,373,342),fill='#65c9a2');d.ellipse((294,175,602,365),fill='#4ca88f')
        for x,y in [(26,207),(79,221),(187,207),(249,231),(363,222),(449,208)]:
            d.rectangle((x,y-28,x+9,y+34),fill='#2d8b6e')
            d.ellipse((x-18,y-51,x+30,y-9),fill='#228d69');d.ellipse((x-11,y-59,x+18,y-22),fill='#36b882')
            d.rectangle((x+3,y-44,x+5,y-31),fill='#71d5a2')
    elif i==1:
        d.ellipse((348,29,420,103),fill='#c785aa');d.ellipse((363,36,419,92),fill='#f8beaf')
        for x in range(0,480,64):
            top=random.randrange(16,53);d.polygon([(x,0),(x+57,0),(x+39,top),(x+27,top+28)],fill='#282143')
            d.polygon([(x,0),(x+19,0),(x+34,top+16)],fill='#38305e')
        for x in range(0,480,54):
            base=random.randrange(185,241)
            d.polygon([(x,269),(x+17,base-52),(x+42,269)],fill='#33264c')
            d.polygon([(x+16,base-33),(x+17,base-52),(x+22,base-19)],fill='#7f5892')
        for x,y in [(62,120),(181,154),(316,125),(425,158)]:
            d.polygon([(x,y+22),(x+13,y-35),(x+30,y+21)],fill='#35cbbd');d.polygon([(x+13,y-35),(x+30,y+21),(x+13,y+19)],fill='#177b9c')
        d.rectangle((0,235,480,270),fill='#281d3c')
    else:
        d.ellipse((350,24,421,95),fill='#ffd89e');d.ellipse((366,24,436,91),fill='#8e7094')
        for x in range(0,480,72):
            h=[95,115,83,132,104,106,86][x//72]
            d.rectangle((x,270-h,x+54,269),fill='#36365e')
            d.rectangle((x+17,270-h-30,x+39,270-h+5),fill='#36365e')
            d.rectangle((x+4,270-h-10,x+12,270-h+11),fill='#36365e')
            for yy in range(270-h+12,267,29):
                d.line((x+4,yy,x+52,yy),fill='#4c486f',width=2)
                for xx in (x+16,x+39):d.line((xx,yy,xx,yy+12),fill='#4c486f',width=2)
            for yy in range(270-h+18,256,40):
                d.rectangle((x+22,yy,x+30,yy+11),fill='#ecc77d')
        d.rectangle((0,237,480,270),fill='#242542')
    save_scaled(im,name,2)
for i,n in enumerate(['forest-bg.png','cave-bg.png','castle-bg.png']): bg(i,n)

# 16-bit pixel sprite textures created as individual frames with native nearest-neighbor scaling.
def player(frame):
    im=pximg(24,32); d=ImageDraw.Draw(im)
    outline='#243054'; skin='#f6bd82'; blue='#386bd2'; blue2='#234ba7'; red='#e95b5a'; hair='#2a314a'
    # backpack
    rect(d,(17,12,22,24),'#b68b5b');rect(d,(18,14,21,20),'#f2cc7b')
    # legs run poses
    if frame==1:
        rect(d,(5,24,10,28),blue2);rect(d,(13,22,17,25),blue2);rect(d,(3,28,10,30),outline);rect(d,(14,25,21,28),outline)
    elif frame==2:
        rect(d,(7,23,12,28),blue2);rect(d,(14,21,17,27),blue2);rect(d,(5,29,13,31),outline);rect(d,(15,27,21,29),outline)
    elif frame==3:
        rect(d,(6,23,12,26),blue2);rect(d,(15,24,20,26),blue2);rect(d,(3,26,12,29),outline);rect(d,(16,27,22,29),outline)
    else:
        rect(d,(6,23,11,28),blue2);rect(d,(14,23,19,28),blue2);rect(d,(4,28,12,31),outline);rect(d,(14,28,21,31),outline)
    # torso and scarf
    rect(d,(5,13,19,24),outline);rect(d,(6,14,18,23),blue);rect(d,(8,14,16,17),'#6f9bf5')
    rect(d,(12,15,18,17),red); rect(d,(17,17,21,20),red)
    # moving arms
    if frame%2==1:
        rect(d,(1,17,5,23),skin);rect(d,(18,14,22,19),skin)
    else:
        rect(d,(2,15,6,21),skin);rect(d,(18,19,22,24),skin)
    # face / cap
    rect(d,(6,4,19,14),outline);rect(d,(7,5,18,13),skin)
    rect(d,(8,4,19,7),hair);rect(d,(8,3,17,5),'#343e62'); rect(d,(6,7,7,12),hair)
    rect(d,(15,9,16,10),outline); rect(d,(18,11,19,12),'#dd8d6a')
    # blue hat
    rect(d,(5,1,17,5),blue2);rect(d,(3,5,19,7),blue);rect(d,(12,2,15,3),'#9cc6f8')
    save_scaled(im,f'explorer-{frame}.png',2)
for frame in range(4):player(frame)

def ground(theme):
    im=pximg(24,24);d=ImageDraw.Draw(im)
    if theme==0: top='#67d777'; top2='#a6ee91'; body='#8c513e'; accents=['#b4764d','#61413e','#d19159']
    elif theme==1:top='#8c74c0';top2='#c5a5f2';body='#47405f';accents=['#6b5c8d','#312b46','#8d77aa']
    else:top='#cc90ac';top2='#f6bdc1';body='#574463';accents=['#7e5873','#39314b','#ad7990']
    rect(d,(0,0,23,23),body);rect(d,(0,0,23,4),top);rect(d,(0,0,23,1),top2)
    for x,y in [(3,8),(13,12),(8,18),(18,6),(20,19)]:rect(d,(x,y,x+4,y+2),random.choice(accents))
    d.line((0,12,13,12),fill=accents[1]);d.line((14,11,23,11),fill=accents[0]);d.line((10,11,10,23),fill=accents[1])
    save_scaled(im,f'ground-{theme}.png',2)
for i in range(3):ground(i)

def questionbox():
    for used in (False,True):
        im=pximg(24,24);d=ImageDraw.Draw(im)
        rect(d,(0,0,23,23),'#482e42' if not used else '#3a4056');rect(d,(2,2,21,21),'#fbbd4b' if not used else '#6a7388')
        d.line((3,3,20,3),fill='#ffe49a' if not used else '#909bae',width=2)
        d.line((3,20,20,20),fill='#d17942' if not used else '#515c6d',width=2)
        for x in (4,19):
            for y in (5,18):rect(d,(x,y,x+1,y+1),'#ae6642' if not used else '#434b60')
        if not used:
            rect(d,(9,6,16,8),'#fff5c5');rect(d,(14,9,17,12),'#fff5c5');rect(d,(11,12,15,14),'#fff5c5');rect(d,(11,17,14,19),'#fff5c5')
            rect(d,(7,7,9,10),'#fff5c5')
        else:rect(d,(9,11,14,12),'#a8afc1')
        save_scaled(im,'block-used.png' if used else 'block-question.png',2)
questionbox()

def coin():
    im=pximg(16,20);d=ImageDraw.Draw(im)
    d.ellipse((2,0,13,19),fill='#9f5c25');d.ellipse((3,1,12,17),fill='#ffcd58');d.ellipse((5,3,10,14),fill='#ffeb95'); d.line((7,5,7,12),fill='#e8983d',width=2)
    save_scaled(im,'coin.png',2)
coin()

def enemy():
    im=pximg(23,18);d=ImageDraw.Draw(im)
    d.ellipse((1,2,21,16),fill='#293454');d.ellipse((2,1,21,14),fill='#ae5fd8')
    d.rectangle((4,4,18,13),fill='#c57deb');d.rectangle((7,7,9,11),fill='#2d2848');d.rectangle((14,7,16,11),fill='#2d2848')
    d.rectangle((4,14,8,17),fill='#47365b');d.rectangle((15,14,19,17),fill='#47365b')
    d.rectangle((6,3,10,4),fill='#e3b4ff')
    save_scaled(im,'slime.png',2)
enemy()

def boss():
    im=pximg(62,71);d=ImageDraw.Draw(im)
    dark='#342a51'; stone='#8877ad'; light='#ae9bc7'; gold='#efbd63'; glow='#7be2f1'
    d.polygon([(3,19),(12,5),(24,13),(31,1),(39,12),(52,4),(60,21)],fill=dark)
    d.polygon([(6,17),(12,8),(23,16),(31,4),(40,16),(51,8),(56,17)],fill=gold)
    d.rectangle((14,19,48,53),fill=dark);d.rectangle((17,19,45,52),fill=stone)
    d.rectangle((7,26,16,47),fill=dark);d.rectangle((46,26,55,47),fill=dark)
    d.rectangle((10,28,15,42),fill=stone);d.rectangle((47,28,52,42),fill=stone)
    d.rectangle((18,53,30,68),fill=dark);d.rectangle((34,53,46,68),fill=dark)
    d.rectangle((21,54,29,65),fill=stone);d.rectangle((35,54,43,65),fill=stone)
    d.rectangle((21,26,29,32),fill=glow);d.rectangle((35,26,43,32),fill=glow)
    d.rectangle((27,40,38,43),fill=dark);d.rectangle((29,47,35,49),fill=gold)
    d.line((18,37,43,37),fill=light,width=2)
    d.rectangle((9,22,11,24),fill=light);d.rectangle((49,23,51,25),fill=light)
    save_scaled(im,'king-ratio.png',2)
boss()
print('assets',len(list(P.glob('*.png'))))

# V1.1 texture repair: use independent seamless below-ground and shallow platform
# textures so repeated vertical blocks never show a second layer of green grass.
def core_and_platform(theme):
    palettes=[
        ('#8c513e','#b4764d','#61413e','#d19159','#67d777','#a6ee91'),
        ('#47405f','#6b5c8d','#312b46','#8d77aa','#8c74c0','#c5a5f2'),
        ('#574463','#7e5873','#39314b','#ad7990','#cc90ac','#f6bdc1')
    ]
    soil,stone,shadow,light,grass,grass_light=palettes[theme]
    im=pximg(24,24);d=ImageDraw.Draw(im)
    rect(d,(0,0,23,23),soil)
    for x,y,w in [(2,3,5),(14,7,4),(7,12,6),(18,16,4),(3,20,5)]:
        rect(d,(x,y,x+w,y+2),stone)
        rect(d,(x+1,y+3,x+w+2,y+3),shadow)
    d.line((0,10,11,10),fill=shadow)
    d.line((12,10,23,10),fill=stone)
    d.line((11,10,11,23),fill=shadow)
    rect(d,(16,20,20,21),light)
    save_scaled(im,f'ground-core-{theme}.png',2)

    # 24x10 pixel platform (48x20 displayed), top and underbody drawn at real height
    im=pximg(24,10);d=ImageDraw.Draw(im)
    rect(d,(0,0,23,9),soil)
    rect(d,(0,0,23,2),grass)
    rect(d,(0,0,23,0),grass_light)
    rect(d,(2,3,10,3),stone)
    rect(d,(15,5,22,6),stone)
    rect(d,(0,7,23,9),shadow)
    rect(d,(1,7,9,7),light)
    rect(d,(13,8,19,8),stone)
    save_scaled(im,f'platform-{theme}.png',2)

for theme in range(3):core_and_platform(theme)
print('texture repair: 6 additional sprites')
