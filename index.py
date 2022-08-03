from operator import mod
from tkinter import font
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os
import glob
import os.path
from io import BytesIO


img = Image.new('RGBA', (256, 256))
god_ui_background = "alentean_god_ui_background.png"
card_background = "card_background.png"

god_ui_mask = "god_ui_image_mask.png"


rootdir = './character_images/'
save_folder = "./minor-god-portrait-tgas"


def clear_directory(directory):
    files = glob.glob(directory+'/*')
    for f in files:
        os.remove(f)


def create_workshop_image(mod_name):
    #print("./Mods/"+mod_name+"/workshop-preview-icon.jpg")
    text = mod_name
    if os.path.exists("./Mods/"+mod_name+"/workshop-preview-icon.jpg") == False:
        W, H = (512, 512)
        img = Image.new('RGB', (512, 512), color="blue")
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(mod_name)

        file = open("fonts/Silver.ttf", "rb")
        bytes_font = BytesIO(file.read())
        font = ImageFont.truetype(bytes_font, 64)

        draw.text(((W-w)/2-(len(text)*6),(H-h)/2), text, fill="black", font=font)

        
        img.save("./Mods/"+mod_name+"/workshop-preview-icon.png")


        W, H = (256, 256)
        img = Image.new('RGB', (256, 256), color="blue")
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(mod_name)

        file = open("fonts/Silver.ttf", "rb")
        bytes_font = BytesIO(file.read())
        font = ImageFont.truetype(bytes_font, 32)

        draw.text(((W-w)/2-(len(text)*1.6),(H-h)/2), text, fill="black", font=font)

        img.save("./Mods/"+mod_name+"/workshop-preview-icon256.png")



def create_minor_god_portrait_tgas(directory, save_folder):
    clear_directory(save_folder)
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            card_size = 180, 240
            img = Image.new('RGBA', (256, 256))
            ci = Image.open(directory+file)
            cb = Image.open(card_background)
            ci = ci.resize(card_size)
            img.paste(ci, (0, 26))
            img.paste(cb, (0, 0), cb)   
            file = file.replace(".PNG", "")
            img.save(save_folder+file+".tga")


def create_major_god_portrait_tgas(directory, save_folder):
    clear_directory(save_folder)
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            card_size = 64, 64
            ci = Image.open(directory+file)
            ci = ci.resize(card_size)
            file = file.replace(".PNG", "")
            ci.save(save_folder+file+".tga")


def create_god_ui_portrait(directory, save_folder, background):
    clear_directory(save_folder)
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            card_size = 168, 160
            img = Image.new('RGBA', (256, 256))
            ci = Image.open(directory+file)
            cb = Image.open(background)
            ci = ci.resize(card_size)
            img.paste(ci, (46, 50), ci)
            img.paste(cb, (0, 0), cb)   
            file = file.replace(".PNG", "")
            img.save(save_folder+file+".tga")



#create_major_god_portrait_tgas(rootdir, "./major_god_portrait_tgas/")
#create_god_ui_portrait(rootdir, "./god_ui_portrait_tgas/", god_ui_background)
#create_minor_god_portrait_tgas(rootdir, save_folder)

