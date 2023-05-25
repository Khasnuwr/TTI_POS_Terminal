import os
import sys
import logging
logging.disable(logging.CRITICAL)

from kivy.app import App
from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout
from staff import StaffWindow
from signin import SigninWindow
from invoices import InvoiceWindow
from admin import AdminWindow
from kivy.core.window import Window
Window.size = (1000,640)
Window.minimum_width, Window.minimum_height = Window.size


# if getattr(sys, 'frozen', False):
#     # running in a bundle
#     template_path = os.path.join(sys._MEIPASS, 'main.kv')
# else:
#     # running live
#     template_path = 'main.kv'

#Builder.load_file('main.kv')


class MainWindow(BoxLayout):
    staff_widget = StaffWindow()
    signin_widget = SigninWindow()
    invoices_widget = InvoiceWindow()
    admin_widget = AdminWindow()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.screen_sign_up.add_widget(self.signin_widget)
        self.ids.screen_staff.add_widget(self.staff_widget)
        self.ids.screen_invoices.add_widget(self.invoices_widget)
        self.ids.admin_panel.add_widget(self.admin_widget)

class MainApp(App):
    def build(self):
        self.icon = "icon.ico"
        self.title = "TTI POS"
        return MainWindow()

if __name__=="__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    MainApp().run()