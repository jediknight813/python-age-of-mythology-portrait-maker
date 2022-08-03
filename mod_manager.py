import os
import shutil
from index import create_workshop_image
parent_dir = "./Mods/"


def check_if_mod_exists(name):
    for folder_name in os.listdir("./Mods/"):
        if folder_name == name:
            return True
    return False


def create_new_mod_folder(name):
    if check_if_mod_exists(name) == False and name != "":
        #create parent mod folder
        path = os.path.join(parent_dir, name) 
        os.mkdir(path) 
        create_read_publishinfo_file(name)
        print(parent_dir, name + "textures")
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
        print(folder_name)
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
        print(content.replace("Visibility=Public", "").replace("Description=", ""))
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
