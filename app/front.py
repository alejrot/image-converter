
import flet as ft

from image_card import ImageCard


def main(page: ft.Page):


    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()


    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.PALETTE),
        leading_width=40,
        title=ft.Text("AppBar Example"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.Icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item",checked=False, on_click=check_item_clicked
                    ),
                ]
            ),
        ],
    )


    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),
            ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Commute"),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                selected_icon=ft.Icons.BOOKMARK,
                label="Favorites",
            ),
        ]
    )


    cards_list = [
        # demo images - user folder
        ImageCard("img_demo/img01.webp"),
        ImageCard("img_demo/img02.webp"),
        ImageCard("img_demo/img03.webp"),
        ImageCard("img_demo/img04.webp"),
        # missing images - system folder
        ImageCard("/dev/shm/img01.jpg"),
        ImageCard("/dev/shm/img02.jpg"),
        ImageCard("/dev/shm/img03.jpg"),
        ImageCard("/dev/shm/img04.jpg"),
        ImageCard("/dev/shm/img05.jpg"),
    ]



    list_view = ft.ListView(
        # graphical column - renders elements selectively
        spacing=10,
        padding=20,
        width=800,
        auto_scroll=True,
    )

    cards_container = ft.Container(
        # transparent container - enables scrollbar
        content=list_view,
        height=700,
        # bgcolor=ft.Colors.GREEN_400
    )


    page.add(cards_container)
    list_view.controls = cards_list
    page.update()


    page.title = "MAQUETA"

    page.theme_mode = ft.ThemeMode.SYSTEM
    # page.theme_mode = ft.ThemeMode.DARK
    # page.theme_mode = ft.ThemeMode.LIGHT

    page.update()




ft.app(target=main)