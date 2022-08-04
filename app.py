from email.policy import default
from multiprocessing import Value
from optparse import Values
from tkinter import HORIZONTAL
import PySimpleGUI as sg
from mod_manager import create_new_mod_folder, check_if_mod_exists, get_all_current_mods, delete_mod, get_read_publishinfo_file_description, update_publishinfo_file_description, get_god_portrait_as_png, create_new_portrait_image
import re
from PIL import Image
import json
from index import convert_to_bytes


app_title = "Age of Mythology: Extended Edition Portrait Maker"
sg.theme('DarkAmber')
a=get_all_current_mods()
pattern = r'[0-9]'
current_mod_opened = ""
current_civilization = ""

current_god_being_editied = ""
current_ui_frame = ""

image_x = int(0)
image_y = int(0)
image_width = int(0)
image_height = int(0)


file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("PNG (*.png)", "*.png")]


layout = [

        [sg.Text("AOM Portrait Maker", font=("Verdana",20))],
        *[[sg.Text(i['name']), sg.Button(("Open "+i["name"]), key="open_mod_name"), sg.Button(("Delete "+i["name"]), key="delete_mod_name")] for i in (a)],
        [sg.Text("enter portrait mod name:"),sg.Input(key='mod_name'), sg.Button("Create", key="update_file_manager")],  

        ]


def return_json_file_data(file_path):
    f = open(file_path)
    data = json.load(f)
    return data


workshop_image_layout = [

            [sg.Text("Workshop Image")],
            [sg.Image(source="./card_background.png")],
            [sg.Button("change image")],

            ]

layout_two = [

            [sg.Text(current_mod_opened, font=("Verdana",30))],
            [sg.Column([[sg.Text("Workshop Discrption")], [sg.Multiline(size=(50, 18), key='mod_description', default_text=get_read_publishinfo_file_description(current_mod_opened))], [sg.Button("Save", key="save_mod_description")]]), sg.Column([[sg.Text("Workshop Image")],
            [sg.Image(size=(290, 290), key="workshop_image")],
            [sg.Button("change image")], ])],
            [sg.Text("Factions", font=("Times New Roman",20))]

            ]

edit_god_portait_layout = [


]



window_layout = [[sg.Column(layout, visible=True, key='file_manager'), sg.Column(layout_two, visible=False, key='faction_picker')]]
window = sg.Window(app_title, window_layout)


def refresh_mod_window():
    a=get_all_current_mods()
    layout = [

        [sg.Text("AOM Portrait Maker", font=("Verdana",20))],
        *[[sg.Text(i['name']), sg.Button(("Open "+i["name"]), key="open_mod_name"), sg.Button(("Delete "+i["name"]), key="delete_mod_name")] for i in (a)],
        [sg.Text("enter portrait mod name:"),sg.Input(key='mod_name'), sg.Button("Create", key="update_file_manager")],  

        ]   
    window1 = sg.Window(app_title, location=window.Location).Layout(layout)
    return window1


def edit_current_civilization_portaits():
    civilization_data = return_json_file_data("./data/CivilizationData.json")["Civilizations"][current_civilization]
    edit_god_portait_layout = [

        [sg.Text(current_civilization, font=("Verdana",25))],
        [sg.Text("Ui Gods", font=("Verdana",20), pad=(20, 20))],
        [sg.Column([ [sg.Image(data=convert_to_bytes(get_god_portrait_as_png(current_mod_opened, text, "ui_gods"), (110, 110)))], [sg.Text(text, font=("Verdana",12))], [sg.Button("Edit", key=text+"_ui_gods", font=("Verdana",12)), sg.Button("Reset",  key="reset_"+text+"_ui_gods", font=("Verdana",12))] ], element_justification="C", pad=(5,5)) for text in civilization_data["ui_gods"]],
        [sg.Column([ [sg.Image(data=convert_to_bytes(get_god_portrait_as_png(current_mod_opened, text, "major_gods"), (110, 110)))], [sg.Text(text, font=("Verdana",12))], [sg.Button("Edit", key=text+"_major_gods", font=("Verdana",12)), sg.Button("Reset",  key="reset_"+text+"_major_gods", font=("Verdana",12))] ], element_justification="C", pad=(5,5)) for text in civilization_data["major_gods"]],
        [sg.Button("Finished", pad=(20, 20), font=("Verdana", 15), key="Finished_with_civilization_layout")]
        ]   
    window1 = sg.Window(app_title, location=window.Location, element_justification="C").Layout(edit_god_portait_layout)
    return window1


def edit_god_image_layout():
    make_custom_god_portrait_layout = [

        [sg.Text(current_god_being_editied, font=("Verdana",30))],
        [sg.Image(data=convert_to_bytes(get_god_portrait_as_png(current_mod_opened, current_god_being_editied, "ui_gods"), (256, 256)), key="currently_editing_god_image")],
        [sg.Text("Import New Image:"), sg.FileBrowse(file_types=file_types, key="portrait_image_file")],
        [sg.Text("image x coordinates"), sg.Slider(range=(-500, 500), default_value=image_x, size=(35, 10), orientation=HORIZONTAL, key="image_x_cord")],
        [sg.Text("image y coordinates"), sg.Slider(range=(-500, 500), default_value=image_y, size=(35, 10), orientation=HORIZONTAL, key="image_y_cord")],
        [sg.Text("image width"), sg.Slider(range=(10, 400), default_value=image_width, size=(35, 10), orientation=HORIZONTAL, key="image_width")],
        [sg.Text("image height"), sg.Slider(range=(10, 400), default_value=image_height, size=(35, 10), orientation=HORIZONTAL, key="image_height")],
        [sg.Button("Update Image", key="change_character_image")],
        [sg.Button("Finished", key="close_edit_god_image_layout")]

    ]
    window1 = sg.Window(app_title, location=window.Location, element_justification="C").Layout(make_custom_god_portrait_layout)
    return window1



def refresh_open_faction_picker_layout():
    layout_two = [
        [sg.Text(current_mod_opened, font=("Verdana",30))],
        [sg.Column([[sg.Text("Workshop Discrption")], [sg.Multiline(size=(50, 15.5), key='mod_description', default_text=get_read_publishinfo_file_description(current_mod_opened))], [sg.Button("Save", key="save_mod_description")]]), sg.Column([[sg.Text("Workshop Image")],
        [sg.Image(data=convert_to_bytes("./Mods/"+current_mod_opened+"/workshop-preview-icon.jpg", (256, 256)), key="workshop_image")],
        [sg.FileBrowse(file_types=file_types, key="workshop_image_file"), sg.Button("update image")] ])],
        [sg.Text("Edit Civilization Portraits", font=("Times New Roman",20))],
        [sg.Button("Greeks", pad=(10, 10)), sg.Button("Egyptians", pad=(10, 10)), sg.Button("Norse", pad=(10, 10)), sg.Button("Atlanteans", pad=(10, 10)), sg.Button("Chinese", pad=(10, 10))],
        [sg.Button("Export Mod", pad=(20, 20), font=("Verdana",12))]
        ]
    window1 = sg.Window(app_title, location=window.Location, element_justification="C").Layout(layout_two)
    return window1


while True:
    event, values = window.read()

    print(event)

    if event == "change_character_image" and values["portrait_image_file"] != "":
        #default slider settings for ui
        #print(values["image_x_cord"],values["image_y_cord"],values["image_height"],values["image_width"])
        new_image_path = create_new_portrait_image(current_ui_frame, current_god_being_editied, values["portrait_image_file"], values["image_x_cord"],values["image_y_cord"],values["image_width"],values["image_height"], current_mod_opened)
        image_data = convert_to_bytes(new_image_path)
        window['currently_editing_god_image'].update(data=image_data)


    if "ui_gods" in event:
        if "reset" not in event and "ui_gods" in event:
            god = event.replace("_ui_gods", "")
            ui_type = event.replace(god, "")
            #print(god, ui_type)
            current_god_being_editied = god 
            current_ui_frame = ui_type
            image_x = 46
            image_y = 50
            image_width = 160
            image_height = 158
            window.close()
            window = edit_god_image_layout()



    if event in return_json_file_data("./data/CivilizationData.json")["Civilizations"].keys():
        current_civilization = event
        window.Close()
        window = edit_current_civilization_portaits()


    if event == "close_edit_god_image_layout":
        current_god_being_editied = ""
        window.Close()
        window = edit_current_civilization_portaits()


    if event == "update image":
        if values["workshop_image_file"] != "":
            image = Image.open(values["workshop_image_file"])
            workshop_image_size = 512, 512
            image = image.resize(workshop_image_size)
            image.save("./Mods/"+current_mod_opened+"/workshop-preview-icon.jpg")

            #workshop_image_size = 256, 256
            #image = image.resize(workshop_image_size)
            #image.save("./Mods/"+current_mod_opened+"/workshop-preview-icon256.png")
            #window.close()
            #window = refresh_open_faction_picker_layout()


    if event == "save_mod_description":
        update_publishinfo_file_description(current_mod_opened, values["mod_description"])


    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break


    if event == "Finished_with_civilization_layout":
        window.close()
        window = refresh_open_faction_picker_layout()


    if event == "update_file_manager":
        new_mod_name = values["mod_name"]
        create_new_mod_folder(new_mod_name.strip())
        window.Close()
        window = refresh_mod_window()


    if "delete_mod_name" == re.sub(pattern, '', event):
        mod_to_delete = window[event].get_text().replace("Delete ", "")
        delete_mod("./Mods/"+mod_to_delete)
        window.Close()
        window = refresh_mod_window()
        

    if "open_mod_name" == re.sub(pattern, '', event):
        current_mod_opened = window[event].get_text().replace("Open ", "")
        window.close()
        window = refresh_open_faction_picker_layout()


    #window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")
    #[sg.Text("Major Gods", font=("Verdana",20), pad=(20, 20))],
    #[ sg.Column([ [sg.Text(text, font=("Verdana",12))], [sg.Button("Edit", key=text+"_major_gods", font=("Verdana",12))] ], element_justification="C", pad=(5,5)) for text in civilization_data["major_gods"]],
    #[sg.Text("Minor Gods", font=("Verdana",20), pad=(20, 20))],
    #[ sg.Column([ [sg.Text(text, font=("Verdana",12))], [sg.Button("Edit", key=text+"_minor_gods", font=("Verdana",12))] ], element_justification="C", pad=(5,5)) for text in civilization_data["minor_gods"]],
    #[sg.Button("Finished", pad=(20, 20), font=("Verdana", 15), key="Finished_with_civilization_layout")]


window.close()