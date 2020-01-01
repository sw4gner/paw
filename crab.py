from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
font = ImageFont.truetype("/home/fia4awagner/mysite/img/20db.otf", 25)
def createOutPng(text):
    with Image.open("/home/fia4awagner/mysite/img/silence.png") as img:
        draw = ImageDraw.Draw(img)
        draw.text((22, 35), text ,(255,255,255),font=font)
        img.save('/home/fia4awagner/mysite/img/out.png')