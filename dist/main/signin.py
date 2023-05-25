from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import sys
import os

if getattr(sys, 'frozen', False):
    # running in a bundle
    template_path = os.path.join(sys._MEIPASS, 'signin.kv')
else:
    # running live
    template_path = 'signin.kv'

Builder.load_file(template_path)

# Database Connection imports
import data_entry


class SigninWindow(BoxLayout):
    def __int__(self, **kwargs):
        super().__int__(**kwargs)
    def validate_user(self):

        info = self.ids.info
        if data_entry.verify_member(str(self.ids.username_field.text), str(self.ids.password_field.text)):
            print(data_entry.verify_member(str(self.ids.username_field.text), str(self.ids.password_field.text))['STAFF_NAME'])
            info.text = '[color=#00FF00]Logged In[/color]'
            self.parent.parent.current = 'staff'
            self.parent.parent.parent.ids.screen_staff.children[0].ids.loggedin_user.text = data_entry.verify_member(str(self.ids.username_field.text), str(self.ids.password_field.text))['STAFF_NAME']
            self.parent.parent.parent.ids.screen_invoices.children[0].ids.loggedin_user.text = \
            self.parent.parent.parent.ids.screen_staff.children[0].ids.loggedin_user.text
            self.parent.parent.parent.ids.screen_staff.children[0].reload_window()
            self.parent.parent.parent.ids.screen_invoices.children[0].reload_menu()
        else:
            info.text = '[color=#FF0000]Wrong Username OR Password[/color]'


class SigninApp(App):
    def build(self):
        return SigninWindow()

if __name__ == "__main__":
    SigninApp().run()