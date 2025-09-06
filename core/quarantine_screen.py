from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import os
import json

class QuarantineScreen(Screen):
    def on_pre_enter(self):
        self.ids.quarantine_list.clear_widgets()
        self.quarantined_files = self.get_quarantined_files()
        self.show_list()

    def get_quarantined_files(self):
        # Retrieve files in the quarantine folder
        quarantine_folder = "quarantine"
        if not os.path.exists(quarantine_folder):
            os.makedirs(quarantine_folder)
        return os.listdir(quarantine_folder)

    def show_list(self):
        for file in self.quarantined_files:
            box = BoxLayout(size_hint_y=None, height="40dp", spacing=10)
            label = Label(text=file, halign="left", valign="middle")
            label.bind(size=label.setter('text_size'))
            btn_restore = Button(text="Restore", size_hint_x=None, width=100)
            btn_delete = Button(text="Delete", size_hint_x=None, width=100)

            btn_restore.bind(on_press=lambda btn, f=file: self.restore(f))
            btn_delete.bind(on_press=lambda btn, f=file: self.delete(f))

            box.add_widget(label)
            box.add_widget(btn_restore)
            box.add_widget(btn_delete)

            self.ids.quarantine_list.add_widget(box)

    def restore(self, file_name):
        quarantine_folder = "quarantine"
        restore_folder = "restored"
        if not os.path.exists(restore_folder):
            os.makedirs(restore_folder)
        source_path = os.path.join(quarantine_folder, file_name)
        target_path = os.path.join(restore_folder, file_name)

        if os.path.exists(source_path):
            os.rename(source_path, target_path)
            self.ids.quarantine_list.clear_widgets()
            self.quarantined_files = self.get_quarantined_files()
            self.show_list()

    def delete(self, file_name):
        quarantine_folder = "quarantine"
        file_path = os.path.join(quarantine_folder, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            self.ids.quarantine_list.clear_widgets()
            self.quarantined_files = self.get_quarantined_files()
            self.show_list()


class QuarantineReportScreen(Screen):
    def on_pre_enter(self):
        self.ids.report_list.clear_widgets()
        self.reports = self.get_report_files()
        self.show_report_list()

    def get_report_files(self):
        log_folder = "logs"
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        # Return .json files only
        return [f for f in os.listdir(log_folder) if f.endswith(".json")]

    def show_report_list(self):
        for report in self.reports:
            box = BoxLayout(size_hint_y=None, height="40dp", spacing=10)
            label = Label(text=report, halign="left", valign="middle")
            label.bind(size=label.setter('text_size'))
            btn_show = Button(text="Show", size_hint_x=None, width=100)
            btn_delete = Button(text="Delete", size_hint_x=None, width=100)

            btn_show.bind(on_press=lambda btn, r=report: self.show_report(r))
            btn_delete.bind(on_press=lambda btn, r=report: self.delete_report(r))

            box.add_widget(label)
            box.add_widget(btn_show)
            box.add_widget(btn_delete)

            self.ids.report_list.add_widget(box)

    def show_report(self, report_name):
        log_folder = "logs"
        report_path = os.path.join(log_folder, report_name)
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                content = json.load(f)
            # Use a popup or separate screen to display the report
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            popup = Popup(title=f"{report_name} - Content", size_hint=(0.8, 0.8))
            popup.content = Label(text=json.dumps(content, indent=4), text_size=(popup.width*0.9, None), valign='top')
            popup.open()

    def delete_report(self, report_name):
        log_folder = "logs"
        report_path = os.path.join(log_folder, report_name)
        if os.path.exists(report_path):
            os.remove(report_path)
            self.ids.report_list.clear_widgets()
            self.reports = self.get_report_files()
            self.show_report_list()
