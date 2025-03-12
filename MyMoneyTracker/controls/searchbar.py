from flet import (
    Container,
    IconButton,
    Icon,
    Page,
    Column,
    Row,
    TextField,
    Text,
    MainAxisAlignment,
    SnackBar,
    AlertDialog,
    AudioRecorder,
    AudioEncoder,
    colors,
    icons)
from core import AppStyle
import speech_recognition as sr
from time import sleep


class UserSearchBar(Container):
    def __init__(self, func, page: Page):
        super().__init__(**AppStyle(page.route).search_bar())

        self.page = page
        self.login_error = SnackBar(
            Text("Couldn't recognize your voice command. Please try again.", color=colors.WHITE),
            bgcolor=colors.RED
        )

        self.audio_file = "data/record.wav"

        self.dlg = AlertDialog(
           title=Text("Listening..."),
        )
        self.audio_rec = AudioRecorder(
            audio_encoder=AudioEncoder.WAV,
            cancel_echo=True
        )

        self.content = Column([
            Row([
                IconButton(icon=icons.ARROW_BACK_ROUNDED, on_click=lambda e: self.view_search_close(),
                           ),
                TextField(
                    **AppStyle(self.page.route).search_bar_textfield(),
                    on_change=func,
                ),
                IconButton(icon=icons.CLOSE, icon_size=16, on_click=lambda e: self.clear_search_field(e, func)),
            ], spacing=0, visible=False
            ),
            Row([
                Container(
                    content=Row([
                        Icon(name=icons.SEARCH),
                        Text('Search...', size=18),
                    ], spacing=10),
                    expand=True,
                    on_click=lambda e: self.view_search()
                ),
                IconButton(icon=icons.MIC, icon_size=20,
                           on_click=lambda e: self.recognize_speech_from_microphone()),
            ]),
            self.audio_rec
        ], alignment=MainAxisAlignment.CENTER)

    def view_search(self):
        self.content.controls[0].visible = True
        self.content.controls[1].visible = False
        self.update()

    def view_search_close(self):
        self.content.controls[1].visible = True
        self.content.controls[0].visible = False
        self.update()

    def clear_search_field(self, e, func):
        self.content.controls[0].controls[1].value = ''
        self.content.controls[0].controls[1].focus()
        self.content.controls[0].controls[1].update()
        func(e)

    def recognize_speech_from_microphone(self):
        recognizer = sr.Recognizer()

        self.page.dialog = self.dlg

        self.audio_rec.start_recording(self.audio_file)
        self.dlg.open = True
        self.page.update()
        sleep(3)
        self.audio_rec.stop_recording()

        with sr.AudioFile(self.audio_file) as source:
            audio = recognizer.record(source)

        try:
            recognized_text = recognizer.recognize_google(audio)
            self.content.controls[0].visible = True
            self.content.controls[1].visible = False
            self.content.controls[0].controls[1].value = recognized_text
            self.dlg.open = False
            self.page.update()
        except sr.UnknownValueError:
            self.dlg.open = False
            self.login_error.open = True
            self.page.update()
        except sr.RequestError:
            self.dlg.open = False
            self.login_error.open = True
            self.page.update()
