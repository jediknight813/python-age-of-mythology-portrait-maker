from PIL import Image, ImageDraw
import os
import glob

img = Image.new('RGBA', (256, 256))
character_image = "characterImage.PNG"
card_background = "card_background.png"


rootdir = './character_images/'
save_folder = "./minor-god-portrait-tgas"


def clear_directory(directory):
    files = glob.glob(directory+'/*')
    for f in files:
        os.remove(f)


def create_minor_god_portrait_tgas(directory, save_folder):
    clear_directory(save_folder)
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            card_size = 180, 240
            img = Image.new('RGBA', (256, 256))
            ci = Image.open("./character_images/"+file)
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


#create_major_god_portrait_tgas(rootdir, "./major_god_portrait_tgas/")
#create_minor_god_portrait_tgas(rootdir, save_folder)

