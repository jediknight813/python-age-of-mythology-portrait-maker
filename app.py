from gc import disable
from multiprocessing.sharedctypes import Value
import PySimpleGUI as sg
from mod_manager import create_new_mod_folder, check_if_mod_exists, get_all_current_mods, delete_mod
import re

sg.theme('DarkAmber')

a=get_all_current_mods()


# Define the window's contents
layout = [

        [sg.Text("AOM Portrait Maker")],
        *[[sg.Text(i['name']), sg.Button('Open'), sg.Button(("Delete "+i["name"]), key="delete_mod_name")] for i in (a)],
        [sg.Text("enter portrait mod name:"),sg.Input(key='mod_name'), sg.Button("Create", key="update_file_manager")],  

        ]

#        [sg.Button("test", key="open_faction_picker")]


layout_two = [

        [sg.Text("Faction Picker")],
        [sg.Input(key='-INPUT-')],
        [sg.Text(size=(40,1), key='-OUTPUT-')],
        [sg.Button('Ok'), sg.Button('Quit')]
    
        ]




window_layout = [[sg.Column(layout, visible=True, key='file_manager'), sg.Column(layout_two, visible=False, key='faction_picker')]]
window = sg.Window('Age of Mythology: Extended Edition Portrait Maker', window_layout,)



def refresh_mod_window():
    new_mod_name = values["mod_name"]
    a=get_all_current_mods()
    create_new_mod_folder(new_mod_name)
    layout = [

        [sg.Text("AOM Portrait Maker")],
        *[[sg.Text(i['name']), sg.Button('Open'), sg.Button(("Delete "+i["name"]), key="delete_mod_name")] for i in (a)],
        [sg.Text("enter portrait mod name:"),sg.Input(key='mod_name'), sg.Button("Create", key="update_file_manager")],    
    ]

    window1 = sg.Window('Window Title', location=window.Location).Layout(layout)
    return window1

pattern = r'[0-9]'
while True:
    event, values = window.read()


    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    if event == "open_faction_picker":
        window["file_manager"].update(visible=False)
        window["faction_picker"].update(visible=True)

    if event == "open_file_menu":
        window["file_manager"].update(visible=True)
        window["faction_picker"].update(visible=False)


    if event == "update_file_manager":
        window.Close()
        window = refresh_mod_window()
        window.Close()
        window = refresh_mod_window()


    if "delete_mod_name" == re.sub(pattern, '', event):
        mod_to_delete = window[event].get_text().replace("Delete ", "")
        delete_mod("./Mods/"+mod_to_delete)
        window.Close()
        window = refresh_mod_window()
        

    #window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")



window.close()