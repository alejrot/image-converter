import flet as ft



# components

source_folder_button = ft.IconButton(
    icon=ft.Icons.FOLDER,
    )

source_images_button = ft.IconButton(
    icon=ft.Icons.IMAGE,
    )


upper_bar = ft.AppBar(
        # leading=ft.Icon(ft.Icons.PALETTE),
        # leading_width=40,
        # title=ft.Text("AppBar Example"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            source_images_button,
            source_folder_button,
            ft.Container(expand=True),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item",
                        checked=False,
                        # on_click=check_item_clicked
                    ),
                ]
            ),
        ],
    )




lower_bar = ft.BottomAppBar(
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.IconButton(icon=ft.Icons.MENU, icon_color=ft.Colors.WHITE),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.SEARCH, icon_color=ft.Colors.WHITE),
                ft.IconButton(icon=ft.Icons.FAVORITE, icon_color=ft.Colors.WHITE),
            ]
        ),
    )
