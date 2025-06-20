
import flet as ft

from components.menus import upper_bar
from components.menus import source_images_button, source_folder_button 

from image_card import list_view, cards_container
from image_card import create_cards




def choose_files_dialog(e: ft.FilePickerResultEvent):

    if e.files is not None:
        paths_list = []

        for file in e.files:
            paths_list.append(file.path)

        list_view.controls = create_cards(paths_list)
        cards_container.update()


def choose_folder_dialog(e: ft.FilePickerResultEvent):

    print(e.path)




files_picker   = ft.FilePicker(on_result=choose_files_dialog)
folder_picker = ft.FilePicker(on_result=choose_folder_dialog)


def choose_files(e):
    files_picker.pick_files(allow_multiple=True)

def choose_folder(e):
    folder_picker.get_directory_path()



source_folder_button.on_click = choose_folder
source_images_button.on_click = choose_files




def main(page: ft.Page):

    page.add(files_picker)    
    page.add(folder_picker)    



    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()


    page.appbar = upper_bar
    


    page.add(cards_container)
    page.update()


    page.title = "Image Converter"

    page.theme_mode = ft.ThemeMode.SYSTEM
    # page.theme_mode = ft.ThemeMode.DARK
    page.theme_mode = ft.ThemeMode.LIGHT

    page.update()




ft.app(target=main)