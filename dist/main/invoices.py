import os
import subprocess
import sys

from num2words import num2words
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

from reportlab.lib.units import inch
from reportlab.platypus import TableStyle, SimpleDocTemplate, Image, Table


if getattr(sys, 'frozen', False):
    # running in a bundle
    template_path = os.path.join(sys._MEIPASS, 'invoices.kv')
else:
    # running live
    template_path = 'invoices.kv'

Builder.load_file(template_path)


import data_entry
from functools import partial


class UpdateInvoiceSuccessPopup(Popup):
    """Popup to show the use that the submission is successful."""
    pass

class InvoiceWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.invoice_number = 0

    def show_invoice(self, invoice_number):
        self.invoice_number = invoice_number
        for inv in data_entry.invoice_sheet.get_all_records():
            if str(inv['INVOICE_NUMBER']) == str(invoice_number):
                self.ids.ind_invoice0.clear_widgets()
                # self.ids.ind_invoice1.clear_widgets()
                # self.ids.ind_invoice2.clear_widgets()
                # self.ids.ind_invoice3.clear_widgets()
                # self.ids.ind_invoice4.clear_widgets()
                details0 = BoxLayout(
                    size_hint_y=None,
                    height=30, pos_hint={"top": 1},
                )
                details1 = BoxLayout(
                    size_hint_y=None,
                    height=30, pos_hint={"top": 1},
                )
                details11 = BoxLayout(
                    size_hint_y=None,
                    height=30, pos_hint={"top": 1},
                )
                details12 = BoxLayout(
                    size_hint_y=None,
                    height=30, pos_hint={"top": 1},
                )
                details13 = BoxLayout(
                    size_hint_y=None,
                    height=30, pos_hint={"top": 1},
                )
                details2 = BoxLayout(
                    size_hint_y=None,
                    height=30, pos_hint={"top": 1},
                )

                details3 = BoxLayout(
                    size_hint_y=None,
                    height=int(30 * int(inv['PRODUCT_NUMBERS'])),
                    pos_hint={"top": 1}
                )
                details4 = BoxLayout(
                    size_hint_y=None,
                    height=30,
                    pos_hint={"top": 1}
                )
                self.ids.ind_invoice0.add_widget(details0)
                self.ids.ind_invoice0.add_widget(details1)
                self.ids.ind_invoice0.add_widget(details11)
                self.ids.ind_invoice0.add_widget(details12)
                self.ids.ind_invoice0.add_widget(details13)
                self.ids.ind_invoice0.add_widget(details2)
                self.ids.ind_invoice0.add_widget(details3)
                self.ids.ind_invoice0.add_widget(details4)
                details0.add_widget(
                    Label(
                        text=f"INVOICE NUMBER: {inv['INVOICE_NUMBER']}",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )
                details0.add_widget(
                    Label(
                        text=f"INVOICE DATE: {inv['INVOICE_DATE']}",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )
                details0.add_widget(
                    Label(
                        text=f"DELIVERY NUMBER: {inv['DELIVERY_NUMBER']}",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )
                details0.add_widget(
                    Label(
                        text=f"DELIVERY DATE: {inv['DELIVERY_DATE']}",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )

                details1.add_widget(
                    Label(
                        text=f"NAME                       :",
                        size_hint_x=0.15,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )
                details1.add_widget(
                    TextInput(
                        text=f"{inv['SOLD_TO']}",
                        size_hint_x=0.85,
                        multiline=False,
                        readonly=True
                    )
                )

                details11.add_widget(
                    Label(
                        text=f"CONTACT NUMBER  :",
                        size_hint_x=0.15,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )
                details11.add_widget(
                    TextInput(
                        text=f"{inv['CONTACT_NUMBER']}",
                        size_hint_x=0.85,
                        multiline=False,
                        readonly=True
                    )
                )
                
                details12.add_widget(
                    Label(
                        text=f"ADDRESS                  :",
                        size_hint_x=0.15,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )
                details12.add_widget(
                    TextInput(
                        text=f"{inv['ADDRESS']}",
                        size_hint_x=0.85,
                        multiline=False,
                        readonly=True
                    )
                )

                details13.add_widget(
                    Label(
                        text=f"REMARKS                  :",
                        size_hint_x=0.15,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )
                details13.add_widget(
                    TextInput(
                        text=f"{inv['PAYMENT_METHOD']}",
                        size_hint_x=0.85,
                        multiline=False,
                        readonly=True
                    )
                )

                details2.add_widget(
                    Label(
                        text=f"PRODUCT MODEL",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )
                details2.add_widget(
                    Label(
                        text=f"DIMENSION",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )
                details2.add_widget(
                    Label(
                        text=f"QUANTITY",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )
                details2.add_widget(
                    Label(
                        text=f"PRICE",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )
                details3.add_widget(
                    Label(
                        text=f"{inv['PRODUCTS']}",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )
                details3.add_widget(
                    Label(
                        text=f"{inv['PRODUCTS_DIMENSIONS']}",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )
                details3.add_widget(
                    Label(
                        text=f"{inv['QUANTITIES']}",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )
                details3.add_widget(
                    Label(
                        text=f"{inv['PRICES']}",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1)
                    )
                )
                details4.add_widget(
                    Label(
                        text=f"TOTAL: {inv['AMOUNT']}",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1),
                        
                    )
                )
                
                details4.add_widget(
                    Label(
                        text=f"DELIVERY STATUS: {inv['DELIVERY_STATUS']}",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1),
                        
                    )
                )
                
                details4.add_widget(
                    Label(
                        text=f"DUE AMOUNT: {inv['DUE_AMOUNT']}",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1),
                        
                    )
                )

                details4.add_widget(
                    Label(
                        text=f"PAID AMOUNT: {inv['PAID_AMOUNT']}",
                        size_hint_x=0.05,
                        color=(0.06, 0.45, 0.45, 1),
                        
                    )
                )

                self.ids.invoice_number.text = str(inv['INVOICE_NUMBER'])
                self.ids.paid_amount.text = str(inv['PAID_AMOUNT'])
                self.ids.del_status.text = str(inv['DELIVERY_STATUS'])

    def search_invoice(self):
        self.show_invoice(self.ids.invoice_number.text)
    def update_invoice(self):
        data_entry.update_invoice(self.ids.invoice_number.text, str(self.ids.del_status.text).upper(), int(self.ids.paid_amount.text))
        UpdateInvoiceSuccessPopup().open()
        self.reload_invoices()
    def reload_menu(self, *args):
        for staff in data_entry.staff_sheet.get_all_records():
            if str(staff['STAFF_NAME']) == str(self.ids.loggedin_user.text):
                if str(staff['IS_ADMIN']) == 'TRUE':
                    adminButton = Button(
                        text="Admin",
                        on_release=self.admin,
                        background_normal='',
                        background_color=(0.06, 0.32, 0.32, 1),
                        size_hint_x=0.33,
                    )
                    self.ids.invoices_menu.add_widget(adminButton)
                    break
    def reload_invoices(self):
        self.ids.invoice.clear_widgets()
        for invoice in data_entry.invoice_sheet.get_all_records():
            details = BoxLayout(
                size_hint_y=None,
                height=30, pos_hint={"top": 1},
            )
            self.ids.invoice.add_widget(details)
            details.add_widget(
                Label(
                    text=f"{invoice['INVOICE_NUMBER']}",
                    size_hint_x=0.08,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{invoice['INVOICE_DATE']}",
                    size_hint_x=0.08,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{invoice['DELIVERY_NUMBER']}",
                    size_hint_x=0.08,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{invoice['SOLD_TO']}",
                    size_hint_x=0.08,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{invoice['AMOUNT']}",
                    size_hint_x=0.08,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{invoice['DELIVERY_STATUS']}",
                    size_hint_x=0.08,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            view_button = Button(
                text="View",
                size_hint_x=0.04,
                background_color=(0.06, 0.32, 0.32, 1)
            )
            # Use partial to pass the invoice number as an argument to the method
            view_button.on_release = partial(self.show_invoice, invoice['INVOICE_NUMBER'])
            details.add_widget(view_button)
    def gen_pdf(self):
        self.generate_bill(self.invoice_number)
    def generate_bill(self, invoice_number):
        try:
            # Create the PDF document object using A4 page size
            if not os.path.exists(f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS"):
                os.makedirs(f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS")
            doc = SimpleDocTemplate(f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS\\Bill_{invoice_number}.pdf", pagesize=A4)
            logo = Image("logo.png", width=2 * inch, height=0.4 * inch)
            logo.hAlign = "CENTER"
            address_table = [
                ["House-272(1st flr.), Lane-19, Lake Road, New DOHS, Mohakhali, Dhaka-1206, Bangladesh."],
                ["P: +880-2-9886149, 9889841, Mob: +88 0171-680047, +88 0171-844303"],
                ["Email: ttibd100@gmail.com"],
                ['']
                ]

            table_address = Table(address_table)

            table_address.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
                ('TOPPADDING', (0, 0), (-1, 0), 0),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
            ]))

            # Create a list of text lines
            text_lines = []
            text_lines.append(["",""])

            sign_part = []
            sign_part.append(
                ["", "", "", "", ""])
            sign_part.append(
                ["", "", "", "", ""])
            sign_part.append(
                ["", "", "", "", ""])
            sign_part.append(["________________", "_______________", "____________", "___________", "_______________"])
            sign_part.append(["Customer Signature", "Manager Signature", "GM Signature", "HO Signature", "Corporate Director"])

            # in words
            table_words = []
            # Create the table data
            table_data = [
                ["MODEL", "DIMENSION", "QTY", "PRICE", "TOTAL"],
            ]
            for invoice in data_entry.invoice_sheet.get_all_records():
                if str(invoice['INVOICE_NUMBER']) == str(invoice_number):
                    text_lines.append([f"INVOICE NUMBER:", f"{invoice['INVOICE_NUMBER']}"])
                    text_lines.append([f"INVOICE DATE:",f"{invoice['INVOICE_DATE']}"])
                    text_lines.append([f"DELIVERY NUMBER:", f"{invoice['DELIVERY_NUMBER']}"])
                    text_lines.append([f"DELIVERY DATE:",f"{invoice['DELIVERY_DATE']}"])
                    text_lines.append([f"NAME:", f"{invoice['SOLD_TO']}"])
                    text_lines.append([f"CONTACT:", f"{invoice['CONTACT_NUMBER']}"])
                    text_lines.append([f"ADDRESS:", f"{invoice['ADDRESS']}"])
                    text_lines.append(["",""])
                    product_names = invoice['PRODUCTS'].split()
                    product_dimensions = invoice['PRODUCTS_DIMENSIONS'].split('\n')
                    product_qties = str(invoice['QUANTITIES']).split()
                    product_prices = str(invoice['PRICES']).split()
                    for itr in range(len(product_names)):
                        table_data.append([f"{product_names[itr]}", f"{product_dimensions[itr]}", f"{product_qties[itr]}", f"{product_prices[itr]}", f"{int(product_qties[itr])*float(product_prices[itr])}"])


                    table_data.append(["", "", "", f"TOTAL AMOUNT:     ", f"{invoice['AMOUNT']}"])
                    table_data.append(["", "", "", f"DUE AMOUNT:        ", f"{invoice['DUE_AMOUNT']}"])
                    table_data.append(["", "", "", f"PAID AMOUNT:        ", f"{invoice['PAID_AMOUNT']}"])
                    table_words.append([f"IN WORDS: {str(self.number_to_words(int(invoice['AMOUNT']))).capitalize()} TAKA"])
                    table_data.append(["", "", "", f"PAYMENT METHOD:", f"{invoice['PAYMENT_METHOD']}"])






            # Create the table and set its style
            table = Table(table_data)


            table0 = Table(text_lines)
            table0.hAlign='LEFT'

            table0.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('LEFTPADDING', (0, 0), (-1, -1),0),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
            ]))

            #Sign Part
            table_sign = Table(sign_part, vAlign='BOTTOM')
            table_sign.Align = 'BOTTOM'
            table_sign.vAlign = 'BOTTOM'
            table_sign.setStyle(
                TableStyle([
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
                    ('FONTSIZE', (0, 1), (-1, -1), 11),
                    ('VALIGN', (0, 1), (-1, -1), 'BOTTOM'),
                ])
            )


            # table words style
            table_words = Table(table_words)
            table_words.hAlign = 'LEFT'
            table_words.setStyle(
                TableStyle([
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),

                ])
            )

            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                #('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ]))

            # Add the text lines and table to the document
            receipt = []
            receipt.append(logo)
            receipt.append(table_address)
            receipt.append(table0)
            receipt.append(table)
            receipt.append(table_words)
            receipt.append(table_sign)




            # Build and save the PDF document to a specific drive
            print('pdf_gen')
            doc.build(receipt)
            subprocess.Popen([f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS\\Bill_{invoice_number}.pdf"], shell=True)
        except:
            pass


    def number_to_words(self, number):
        if number < 1000:
            return num2words(number)
        elif number < 1000000:
            thousands = number // 1000
            remainder = number % 1000
            if remainder == 0:
                return num2words(thousands) + " thousand"
            else:
                return num2words(thousands) + " thousand " + num2words(remainder)
        else:
            millions = number // 1000000
            remainder = number % 1000000
            if remainder == 0:
                return num2words(millions) + " million"
            else:
                return num2words(millions) + " million " + num2words(remainder)

    def invoices_window(self):
        self.parent.parent.current = 'invoices'
        self.parent.parent.parent.ids.screen_invoices.children[0].ids.loggedin_user.text = self.ids.loggedin_user.text
        self.parent.parent.parent.ids.screen_invoices.children[0].reload_invoices()
    def create_invoice(self):
        self.parent.parent.current = 'staff'
        self.parent.parent.parent.ids.screen_staff.children[0].ids.loggedin_user.text = self.ids.loggedin_user.text
    def admin(self, obj):
        self.parent.parent.current = 'admin'
        self.parent.parent.parent.ids.admin_panel.children[0].ids.loggedin_user.text = self.ids.loggedin_user.text
        self.parent.parent.parent.ids.admin_panel.children[0].reload_admin()
class InvoiceApp(App):
    def build(self):
        return InvoiceWindow()


if __name__ == "__main__":
    InvoiceApp().run()
