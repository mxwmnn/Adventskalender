import flet as ft
from random import randint, choice, shuffle
from const import weihnachtsraetsel, weihnachtliche_erfolgsmeldungen, weihnachtliche_fehlermeldungen
import requests
import sys
from datetime import datetime

def days_until_christmas():
    # Der API-Endpunkt für die UTC-Zeit
    api_url = 'http://worldtimeapi.org/api/timezone/Etc/UTC'
    
    # Versuche den Request auszuführen
    try:
        # API-Request
        response = requests.get(api_url)
        # Überprüfung ob der Request erfolgreich war
        response.raise_for_status() # löst eine Ausnahme aus, wenn status_code kein 200 ist
    except requests.RequestException as e:
        # Bei Netzwerkfehler oder anderen Fehlern, zeige die Fehlermeldung an.
        print(f"Fehler bei der HTTP-Anfrage: {e}")
        return None

    # Lade die JSON-Daten aus der Response
    data = response.json()
    # Extrahiere den ISO-String für das Datum und die Uhrzeit
    utc_datetime_iso = data['utc_datetime'][:10]

    # Parse den ISO-String zum datetime-Objekt
    current_datetime = datetime.fromisoformat(utc_datetime_iso)
    # Definiere das Ziel-Datum für Weihnachten im selben Jahr
    christmas = datetime(year=current_datetime.year, month=12, day=24)

    # Falls das aktuelle Datum nach Weihnachten ist, nimm Weihnachten im nächsten Jahr
    if current_datetime > christmas:
        sys.exit(0)

    # Berechne die Differenz zwischen den Tagen
    delta = (christmas - current_datetime).days
    return current_datetime.day
    
    

def is_raetsel():
    return True if monk == 0 else False

    

def main(page: ft.Page):
    global monk
    monk = 0
    def load_raetsel(e):
        global monk
        global fee
        tuer = e
        if e <= 24 and days_until_christmas() >= e and is_raetsel():
            def check_answer(e):
                global monk
                column.visible = False
                antwort = answer.value
                wrong = ft.Text(f'{weihnachtliche_fehlermeldungen[randint(0,9)]}', color=ft.colors.RED)
                if antwort == weihnachtsraetsel[e]['Antwort']:
                    column.visible = False
                    page.add(ft.Text(f'{weihnachtliche_erfolgsmeldungen[randint(0, 9)]}', color=ft.colors.LIGHT_GREEN))
                    monk = 0
                elif antwort == '':
                    pass
                else:
                    monk = 0
                    page.add(wrong)
                    
            question = ft.Text(f'{weihnachtsraetsel[e]['Raetsel']}')
            answer = ft.TextField(label="Antwort", hint_text="Hinweis: Wenn du denkst du liegst richtig einfach mal ein Wort mit Weihnacht(s)' verknuepfen ;)")
            submit = ft.ElevatedButton(text="Abschicken", on_click=lambda e, num=tuer: check_answer(num))
            column = ft.Column(controls=[question, answer, submit])
            monk = 1
            page.add(column)
        elif monk == 1:
            pass
        else:
            def close_banner(e):
                page.banner.open = False
                page.update()

            banner = ft.Banner(
                bgcolor=ft.colors.AMBER_100,
                leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
                content=ft.Text(
                    f"Oops, Türen nicht vorher aufmachen!!einself! 🤥",
                    color=ft.colors.BLACK,
                ),
                actions=[
                    ft.TextButton("Okay, ich warte ja 🎄🎄🎄", on_click=close_banner),
                ],
            )
            page.banner = banner
            page.banner.open = True
            page.add(banner)
            
            
    page.title = "Adventskalender Rätsel"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    
    images = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )


    for i in range(1, 25):
        images.controls.append(
            ft.Stack(
                [
                    ft.Image(
                        src=f"tuer.png",
                        fit=ft.ImageFit.SCALE_DOWN,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                    ),
                    ft.TextButton(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Tür", size=20, color=ft.colors.LIGHT_GREEN, offset=(0,1)),
                                    ft.Text(value=f"{i}", size=30, color=ft.colors.WHITE, offset=(0,0.5)),
                                ],
                                # alignment=ft.alignment.top_center,
                                # spacing=5,
                            ),
                            # padding=ft.padding.all(10),
                            alignment=ft.alignment.top_center,
                            on_click=lambda e, num=i: load_raetsel(num),
                        ),
                        
                    ),
                ],
            ),
        )
    page.add(example())
    page.add(images)
    page.update()



def example():
    class BackgroundMusicControl(ft.Row):
        def __init__(self):
            super().__init__()
            music = ["Michael Bublé - It's Beginning to Look a Lot like Christmas.mp3", 'Shirley Horn - Winter Wonderland.mp3', 'Frank Sinatra - Jingle Bells - Remastered 1999.mp3']
            shuffle(music)
            self.audio1 = ft.Audio(
                src=music[0],
                autoplay=True,
            )

            def pause_audio(e):
                self.audio1.pause()
                self.controls[0].visible = True
                self.controls[1].visible = False
                self.page.update()

            def start_audio(e):
                self.audio1.resume()
                self.controls[0].visible = False
                self.controls[1].visible = True
                self.page.update()

            self.controls = [
                ft.ElevatedButton("Start playing", on_click=start_audio, visible=False),
                ft.ElevatedButton("Stop playing", on_click=pause_audio),
            ]
            
                    # happens when example is added to the page (when user chooses the Audio control from the grid)
        def did_mount(self):
            self.page.overlay.append(self.audio1)
            self.page.update()

        # happens when example is removed from the page (when user chooses different control group on the navigation rail)
        def will_unmount(self):
            self.page.overlay.remove(self.audio1)
            self.page.update()

    return BackgroundMusicControl()



ft.app(target=main, assets_dir="assets", name='', port=8555)
