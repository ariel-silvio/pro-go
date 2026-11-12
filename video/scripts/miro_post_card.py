import sys; sys.path.insert(0,'.')
import render as R, qrcode
from PIL import Image, ImageDraw, ImageFilter
S=sys.argv[1]
W,H=1620,2380; INK=(17,17,17); IV=(247,243,236); PAPER=(255,255,255); GOLD=R.GOLD; GT=R.GOLD_TXT; MUTED=(95,90,84); HAIR=(227,221,211)
img=Image.new('RGB',(W,H),IV); d=ImageDraw.Draw(img)
F=lambda f,s: R.font(f,s)
# header
R.spaced(d,(80,62),"L'ORÉAL GROUPE  ·  TEAM D",F(R.SANS_M,26),GT,7)
d.text((W-80,58),"IE EXECUTIVE MBA",font=F(R.SANS_M,26),fill=INK,anchor="ra")
d.text((W-80,96),"M4  ·  Partnership & pilot",font=F(R.SANS,26),fill=MUTED,anchor="ra")
# hero
HY,HH=150,820
hero=Image.open(S+'/hero.png').convert('RGB'); hw=W-560
hero=hero.resize((int(hero.width*HH/hero.height),HH)); x0=(hero.width-hw)//2+60; hero=hero.crop((x0,0,x0+hw,HH))
img.paste(hero,(560,HY))
d.rectangle([0,HY,560,HY+HH],fill=INK)
R.spaced(d,(80,HY+70),"THE DUBAI PILOT",F(R.SANS_M,24),GOLD,7)
d.text((74,HY+115),"PRO•GO",font=F(R.SERIF,112),fill=(255,255,255))
d.text((78,HY+250),"Partnership & pilot",font=F(R.SERIF,50),fill=GOLD)
d.rectangle([80,HY+340,150,HY+342],fill=GOLD)
d.text((80,HY+380),"A 90-day pilot",font=F(R.SANS_M,44),fill=(255,255,255))
d.text((80,HY+434),"with ServiceMarket.",font=F(R.SANS_M,44),fill=(255,255,255))
for i,l in enumerate(["Test PRO•GO in Dubai through a","partnership that combines L'Oréal's","beauty expertise with ServiceMarket's","home-service platform."]):
    d.text((80,HY+520+i*42),l,font=F(R.SANS,28),fill=(236,230,220))
# phone with the real prototype screen
scr=Image.open('/tmp/claude-0/-home-user-pro-go/7cbc29c2-b15c-587b-a097-c29f10db4125/scratchpad/scr/screen_week0_invite.png').convert('RGB')
pw,ph=300,600; sc=scr.resize((pw-24,int(scr.height*(pw-24)/scr.width))).crop((0,0,pw-24,ph-24))
px,py=640,HY+110
ph_l=Image.new('RGBA',(pw+40,ph+40),(0,0,0,0)); dd=ImageDraw.Draw(ph_l)
dd.rounded_rectangle([20,26,pw+20,ph+26],radius=44,fill=(0,0,0,110)); ph_l=ph_l.filter(ImageFilter.GaussianBlur(12))
img.paste(ph_l,(px-20,py-20),ph_l)
d.rounded_rectangle([px,py,px+pw,py+ph],radius=44,fill=INK)
m=Image.new('L',(pw-24,ph-24),0); ImageDraw.Draw(m).rounded_rectangle([0,0,pw-25,ph-25],radius=34,fill=255)
img.paste(sc,(px+12,py+12),m)
d.rounded_rectangle([px+pw//2-50,py+20,px+pw//2+50,py+40],radius=10,fill=INK)
def chip(x,y,t,anchor_right=False):
    f=F(R.SANS_M,20); w=d.textlength(t,font=f)+28
    if anchor_right: x-=w
    d.rounded_rectangle([x,y,x+w,y+38],radius=19,fill=(17,17,17)); d.text((x+14,y+8),t,font=f,fill=(255,255,255))
chip(px,HY+HH-60,"LIVE PROTOTYPE"); chip(W-30,HY+HH-60,"FROM OUR FILM",True)
# numbers strip
NY=HY+HH; d.rectangle([0,NY,W,NY+250],fill=(239,232,220))
nums=[("€200","CUSTOMER PRICE","per home colour visit"),("€60","L'ORÉAL REVENUE","30% fee per visit"),("€40","CONTRIBUTION / VISIT","after €20 variable cost"),("€140","PARTNER REVENUE","ServiceMarket's share")]
cw=(W-160)/4
for i,(n,l,s) in enumerate(nums):
    x=80+i*cw
    if i: d.line([(x-24,NY+50),(x-24,NY+200)],fill=(214,204,190),width=2)
    d.text((x,NY+40),n,font=F(R.SERIF,84),fill=INK)
    R.spaced(d,(x,NY+145),l,F(R.SANS_M,20),GT,4)
    d.text((x,NY+180),s,font=F(R.SANS,26),fill=INK)
# pilot design
PY=NY+300
R.spaced(d,(80,PY),"PILOT DESIGN",F(R.SANS_M,24),GT,7)
d.text((76,PY+40),"A 90-day pilot in Dubai",font=F(R.SERIF,72),fill=INK)
d.rectangle([80,PY+156,140,PY+158],fill=GOLD)
cards=[("01","Partner","ServiceMarket","Dubai home services since 2013"),("02","Scope","3–5 salons","Downtown & Business Bay"),("03","Duration","90 days","Paid pilot"),("04","Target","300 customers","Test demand and repeat use")]
CY=PY+196; gw=24; cw2=(W-160-3*gw)/4
for i,(n,t,b,s) in enumerate(cards):
    x=80+i*(cw2+gw); d.rectangle([x,CY,x+cw2,CY+230],fill=PAPER,outline=HAIR,width=2); d.rectangle([x,CY,x+cw2,CY+4],fill=GOLD)
    d.text((x+28,CY+30),n,font=F(R.SANS_M,22),fill=GT); d.text((x+70,CY+26),t,font=F(R.SANS_M,28),fill=INK)
    fs=54
    while d.textlength(b,font=F(R.SERIF,fs))>cw2-56: fs-=2
    d.text((x+28,CY+90),b,font=F(R.SERIF,fs),fill=INK)
    d.text((x+28,CY+170),s,font=F(R.SANS,22),fill=MUTED)
# CEO ask
AY=CY+290; d.rectangle([80,AY,W-80,AY+330],fill=INK); d.rectangle([80,AY,W-80,AY+4],fill=GOLD)
R.spaced(d,(130,AY+55),"THE CEO ASK",F(R.SANS_M,24),GOLD,7)
d.text((124,AY+95),"€30,000",font=F(R.SERIF,118),fill=(255,255,255))
d.text((130,AY+250),"to launch the 90-day pilot",font=F(R.SANS,32),fill=(236,230,220))
d.line([(700,AY+60),(700,AY+270)],fill=(70,66,62),width=2)
R.spaced(d,(750,AY+55),"THE OUTCOME WE TEST",F(R.SANS_M,24),GOLD,7)
for i,o in enumerate(["40% or more book a second visit in 90 days","Positive contribution per visit (€40)","Salon partners satisfied and ready to expand"]):
    y=AY+115+i*62; d.line([(752,y+18),(764,y+30),(788,y+4)],fill=GOLD,width=4)
    d.text((808,y),o,font=F(R.SANS,30),fill=(255,255,255))
# footnote + footer with video QR
FY=AY+370
d.text((80,FY),"Figures: Team D's agreed assumptions (€200 price, €60 L'Oréal fee, €20 variable cost, €140 partner share). Images from our film; Layla is fictional.",font=F(R.SANS,21),fill=MUTED)
d.line([(80,FY+50),(W-80,FY+50)],fill=HAIR,width=2)
R.spaced(d,(80,FY+85),"TEAM D  ·  L'ORÉAL INNOVATION CASE",F(R.SANS_M,22),GT,5)
d.text((80,FY+122),"Amjad Bensalamah · Ariel de Silvio · Qhakazile Mathebula · Rebecca Fernandes · Saja Alowayshiq · Nacho Alcantara",font=F(R.SANS,20),fill=MUTED)
qr=qrcode.QRCode(border=1,box_size=6); qr.add_data("https://youtu.be/T2k37jMMXo4"); qr.make(fit=True)
q=qr.make_image(fill_color=INK,back_color=PAPER).convert('RGB').resize((120,120),Image.NEAREST)
img.paste(q,(W-80-120,FY+70))
d.text((W-80-140,FY+92),"Watch the film",font=F(R.SANS_M,24),fill=INK,anchor="ra")
d.text((W-80-140,FY+126),"youtu.be/T2k37jMMXo4",font=F(R.SANS,20),fill=MUTED,anchor="ra")
print('bottom used to', FY+200, 'of', H)
img.save('review/miro_post_pilot_card.png')
