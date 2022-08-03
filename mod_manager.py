import os
import shutil

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



def delete_mod(path):
    shutil.rmtree(path, ignore_errors=True)


def get_all_current_mods():
    mods = []
    for folder_name in os.listdir("./Mods/"):
        print(folder_name)
        mods.append({"name": folder_name, "path": ('./Mods/'+folder_name)})
    return mods
