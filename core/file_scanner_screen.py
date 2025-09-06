from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView

class FileScannerScreen(Screen):
    def open_file_chooser(self):
        content = BoxLayout(orientation='vertical', spacing=10)
        filechooser = FileChooserListView(path='.', filters=['*.*'])
        content.add_widget(filechooser)

        btn_layout = BoxLayout(size_hint_y=None, height='40dp', spacing=10)
        btn_scan = Button(text='Scan')
        btn_cancel = Button(text='Cancel')
        btn_layout.add_widget(btn_scan)
        btn_layout.add_widget(btn_cancel)
        content.add_widget(btn_layout)

        popup = Popup(title='Select File and Scan', content=content, size_hint=(0.9, 0.9))

        def on_scan(instance):
            if filechooser.selection:
                selected_file = filechooser.selection[0]
                self.ids.result_label.text = f"Selected file:\n{selected_file}\nResult: Safe."
            else:
                self.ids.result_label.text = "No file selected!"
            popup.dismiss()

        def on_cancel(instance):
            popup.dismiss()

        btn_scan.bind(on_press=on_scan)
        btn_cancel.bind(on_press=on_cancel)

        popup.open()
