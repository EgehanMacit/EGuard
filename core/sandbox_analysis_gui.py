# screens/sandbox_analysis_screen.py

from kivy.uix.screenmanager import Screen
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.lang import Builder
from core.sandbox_analysis import run_in_sandbox

Builder.load_file("ui/modules/sandbox_analysis.kv")

class SandboxAnalysisScreen(Screen):
    analysis_result = StringProperty("No analysis performed yet.")

    def select_file(self):
        box = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView()
        box.add_widget(filechooser)

        btn_layout = BoxLayout(size_hint_y=None, height="48dp", spacing=10)
        start_btn = Button(text="Start Analysis")
        cancel_btn = Button(text="Cancel")
        btn_layout.add_widget(start_btn)
        btn_layout.add_widget(cancel_btn)

        box.add_widget(btn_layout)

        popup = Popup(title="Select File", content=box, size_hint=(0.9, 0.9))

        def start_analysis(instance):
            if filechooser.selection:
                selected = filechooser.selection[0]
                result = run_in_sandbox(selected)
                self.analysis_result = result
                popup.dismiss()

        def cancel_analysis(instance):
            popup.dismiss()

        start_btn.bind(on_press=start_analysis)
        cancel_btn.bind(on_press=cancel_analysis)
        popup.open()

def open_filechooser(self):
    import os  # <-- add if not imported at the top

    box = BoxLayout(orientation='vertical')
    filechooser = FileChooserListView()
    filechooser.path = os.path.expanduser("~")  # Avoid system folders causing errors
    box.add_widget(filechooser)

    btn = Button(text="Start Analysis", size_hint_y=None, height="48dp")
    box.add_widget(btn)

    popup = Popup(title="Select File", content=box, size_hint=(0.9, 0.9))

    def start_analysis(instance):
        if filechooser.selection:
            selected = filechooser.selection[0]
            result = run_in_sandbox(selected)
            self.ids.analysis_result.text = result
            popup.dismiss()

    btn.bind(on_press=start_analysis)
    popup.open()
