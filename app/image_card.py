import flet as ft
from pathlib import Path


class ImageCard(ft.Card):
    def __init__(self, image_path: str):
        super().__init__(self)

        # file path processing
        self.source_path = Path(image_path).absolute()

        if self.source_path.is_relative_to(Path.home()) is True:
            self.display_path = self.source_path.relative_to(Path.home())
        else:
            self.display_path = self.source_path

        self.content = ft.Container(
            content=ft.Row([
                ft.ListTile(
                    leading=ft.Container(
                        height=40,
                        width=60,
                        bgcolor=ft.Colors.YELLOW_500,
                        border_radius=10,
                        content=ft.Image(
                            src=self.source_path,
                            width=200,
                            height=200,
                            fit=ft.ImageFit.FIT_HEIGHT,
                            repeat=ft.ImageRepeat.NO_REPEAT,
                            border_radius=ft.border_radius.all(10),
                        ) if self.source_path.is_file() else None
                    ),
                    title=ft.Text(
                        self.source_path.name
                    ),
                    subtitle=ft.Text(
                        self.display_path
                    ),
                    bgcolor=ft.Colors.GREY_400,
                    adaptive=False,
                    expand=2,
                ),
                # (more elements there)
            ]),
            # width=1200,
            padding=10,
        )
        self.shadow_color=ft.Colors.ON_SURFACE_VARIANT,



## Demo example
def main(page: ft.Page):
    page.title = "Card Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.theme_mode = ft.ThemeMode.DARK
    # page.theme_mode = ft.ThemeMode.SYSTEM

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
        spacing=10,
        padding=20,
        width=800,
        auto_scroll=True,
    )


    cards_container = ft.Container(
        # transparent container - enables scrollbar
        content=list_view,
        height=700,
    )

    page.add(cards_container)

    list_view.controls = cards_list

    page.update()



if __name__=="__main__":
    
    ft.app(main)
