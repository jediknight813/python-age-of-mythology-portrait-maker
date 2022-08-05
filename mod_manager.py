from ast import Str
import os
from re import T
import shutil
from index import create_workshop_image
parent_dir = "./Mods/"
from PIL import Image
import tempfile
import time


def check_if_mod_exists(name):
    for folder_name in os.listdir("./Mods/"):
        if folder_name == name:
            return True
    return False


def delete_god_portrait(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def create_new_portrait_image(ui_type, god_name, user_image, image_x, image_y, image_width, image_height, current_mod_opened, current_civilization):
    print(int(image_x), int(image_y), int(image_width), int(image_height))
    if ui_type == "_ui_gods":
            card_size = int(image_width), int(image_height)
            img = Image.new('RGBA', (256, 256))
            cb = Image.open("./GodPortraitFrames/"+"ui_god_"+current_civilization+".png")
            ci = Image.open(user_image)
            ci = ci.resize(card_size)
            img.paste(ci, (int(image_x), int(image_y)))
            img.paste(cb, (0, 0), cb)   
            img.save("./Mods/"+current_mod_opened+"/textures/ui/ui god "+god_name+" 256x256.tga")
            return ("./Mods/"+current_mod_opened+"/textures/ui/ui god "+god_name+" 256x256.tga")


    if ui_type == "_major_gods":
            card_size = int(image_width), int(image_height)
            img = Image.new('RGBA', (64, 64))
            cb = Image.open("blank_icon.png")
            ci = Image.open(user_image)
            ci = ci.resize(card_size)
            img.paste(ci, (int(image_x), int(image_y)))
            img.paste(cb, (0, 0), cb)  
            img.save("./Mods/"+current_mod_opened+"/textures/icons/god major "+god_name+" icons 64.tga")
            return ("./Mods/"+current_mod_opened+"/textures/icons/god major "+god_name+" icons 64.tga")


    if ui_type == "_minor_gods":
            card_size = int(image_width), int(image_height)
            img = Image.new('RGBA', (256, 256))
            cb = Image.open("./GodPortraitFrames/"+current_civilization+"_card_background.png")
            ci = Image.open(user_image)
            ci = ci.resize(card_size)
            img.paste(ci, (int(image_x), int(image_y)))
            img.paste(cb, (0, 0), cb)   
            img.save("./Mods/"+current_mod_opened+"/textures/god minor portrait "+current_civilization.lower()+" "+god_name+".tga")
            return ("./Mods/"+current_mod_opened+"/textures/god minor portrait "+current_civilization.lower()+" "+god_name+".tga")



#"./Mods/atlantean_portraits_replacer/textures\ui\ui god gaia 256x256.tga"
def get_god_portrait_as_png(current_mod_opened, god_name, god_type, current_civilization):
    #print("./Mods/"+current_mod_opened+"/textures/"+"ui/"+"ui god "+god_name +" 256x256.tga")
    if (god_type == "_ui_gods"):
        if os.path.exists(("./Mods/"+current_mod_opened+"/textures/ui/ui god "+god_name+" 256x256.tga")) == True:
            return("./Mods/"+current_mod_opened+"/textures/ui/ui god "+god_name+" 256x256.tga")
        else:
            return ("./GodPortraitFrames/"+"ui_god_"+current_civilization+".png")
    
    if (god_type == "_major_gods"):
        if os.path.exists(("./Mods/"+current_mod_opened+"/textures/icons/god major "+god_name+" icons 64.tga")) == True:
            return("./Mods/"+current_mod_opened+"/textures/icons/god major "+god_name+" icons 64.tga")
        else:
            return "blank_icon.png"
    
    if (god_type == "_minor_gods"):
        if os.path.exists(("./Mods/"+current_mod_opened+"/textures/god minor portrait "+current_civilization.lower()+" "+god_name+".tga")) == True:
            return("./Mods/"+current_mod_opened+"/textures/god minor portrait "+current_civilization.lower()+" "+god_name+".tga")
        else:
            return ("./GodPortraitFrames/"+current_civilization+"_card_background.png")


def create_new_mod_folder(name):
    if check_if_mod_exists(name) == False and name != "":
        #create parent mod folder
        path = os.path.join(parent_dir, name) 
        os.mkdir(path) 
        create_read_publishinfo_file(name)
        #print(parent_dir, name + "textures")
        #create texture folder

        path = os.path.join(parent_dir, name + "/textures") 
        os.mkdir(path) 

        #add icons folder to texures
        path = os.path.join(parent_dir, name + "/textures/icons") 
        os.mkdir(path) 

        #add ui to textures

        path = os.path.join(parent_dir, name + "/textures/ui") 
        os.mkdir(path)
        
        create_workshop_image(name)


def delete_mod(path):
    shutil.rmtree(path, ignore_errors=True)


def get_all_current_mods():
    mods = []
    for folder_name in os.listdir("./Mods/"):
        #print(folder_name)
        mods.append({"name": folder_name, "path": ('./Mods/'+folder_name)})
    return mods


def create_read_publishinfo_file(mod_name):
    if check_if_mod_exists(mod_name) == True:
        f = open(('./Mods/'+mod_name+"/_publishinfo.txt"),"w+")
        f.write("Visibility=Public\n")
        f.write("Description=\n")
        f.close


def get_read_publishinfo_file_description(mod_name):   
    if check_if_mod_exists(mod_name) == True: 
        f = open(('./Mods/'+mod_name+"/_publishinfo.txt"),"r")
        content = f.read()
        #print(content.replace("Visibility=Public", "").replace("Description=", ""))
        return content.replace("Visibility=Public", "").replace("Description=", "")


def update_publishinfo_file_description(mod_name, description):
    #print(mod_name, description)
    file = open(('./Mods/'+mod_name+"/_publishinfo.txt"),"r+")
    file.truncate(0)
    file.close()

    f = open(('./Mods/'+mod_name+"/_publishinfo.txt"),"w+")
    f.write("Visibility=Public\n")
    f.write("Description="+description.strip()+"\n")
    f.close
