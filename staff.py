import datetime
import os
import sys

from kivy.uix.button import Button
from num2words import num2words
from reportlab.lib import colors

from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
import subprocess

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.popup import Popup
from reportlab.platypus import SimpleDocTemplate, Image, TableStyle, Table

if getattr(sys, 'frozen', False):
    # running in a bundle
    template_path = os.path.join(sys._MEIPASS, 'staff.kv')
else:
    # running live
    template_path = 'staff.kv'

Builder.load_file(template_path)

import data_entry

class SubmitSuccessPopup(Popup):
    """Popup to show the use that the submission is successful."""
    pass

class StaffWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.generate_bill(14)
        self.cart = []
        self.pqty = []
        self.ptotal = 0.00

        self.products_ids = []
        self.products_dimensions = []
        self.products_in_basket = []
        self.per_product_quantities = []
        self.per_product_prices = []
        self.run_till_logged_in = True
    def get_product_list(self):
        products = []
        for product in data_entry.product_sheet.get_all_records():
            products.append(str(product['PRODUCT_NAME'])+' # '+str(product['SIZE']))
        return products
    def update_purchases(self):
        try:
            prdct = self.ids.id_input.text.split(' # ')

            if len(prdct) == 2:
                print('MODEL '+ prdct[0]+ ' SIZE: ' +prdct[1])

                if self.ids.qty_input.text == '':
                    self.ids.qty_input.text = '0'
                if self.ids.vat.text == '' or self.ids.vat.text == '0.00':
                    self.ids.vat.text = '0.0'
                if self.ids.discount.text == '' or self.ids.discount.text == '0.00':
                    self.ids.discount.text = '0.0'
                products_container = self.ids.products
                if int(self.ids.qty_input.text) > 0:
                    for product in data_entry.product_sheet.get_all_records():
                        if prdct[0] == str(product['PRODUCT_NAME']) and prdct[1] == str(product['SIZE']):
                            try:
                                self.ids.stock_remaining.text = str(product['STOCK'])

                                self.products_in_basket.append(str(product['PRODUCT_NAME']))
                                self.per_product_quantities.append(f"{self.ids.qty_input.text}")
                                self.per_product_prices.append(str(product['PRICE']))
                                self.products_ids.append(str(product['PRODUCT_ID']))
                                self.products_dimensions.append(str(product['SIZE']))
                                print(product['PRODUCT_NAME'])
                                details = BoxLayout(
                                    size_hint_y=None,
                                    height=30, pos_hint={"top": 1},
                                )
                                products_container.add_widget(details)
                                product_id = Label(
                                    text=str(product['PRODUCT_ID']),
                                    size_hint_x=0.2,
                                    color=(0.06, 0.45, 0.45, 1)
                                )
                                name = Label(
                                    text=f"{product['PRODUCT_NAME']}",
                                    size_hint_x=0.2,
                                    color=(0.06, 0.45, 0.45, 1)
                                )
                                qty = Label(
                                        text=f"{self.ids.qty_input.text}",
                                        size_hint_x=0.1,
                                        color=(0.06, 0.45, 0.45, 1)
                                    )
                                price = Label(
                                    text=f"{product['PRICE']}",
                                    size_hint_x=0.1,
                                    color=(0.06, 0.45, 0.45, 1)
                                )
                                dimension = Label(
                                    text=f"{product['SIZE']}",
                                    size_hint_x=0.2,
                                    color=(0.06, 0.45, 0.45, 1)
                                )
                                details.add_widget(product_id)
                                details.add_widget(name)
                                details.add_widget(dimension)
                                details.add_widget(qty)
                                details.add_widget(price)
                                # Update Preview
                                self.ids.receipt_preview.text += f"{product['PRODUCT_NAME']} {product['SIZE']}     x{self.ids.qty_input.text}     {product['PRICE']}\n\n"

                                self.ptotal += float(float(product['PRICE'])*int(self.ids.qty_input.text) + ((float(product['PRICE'])*int(self.ids.qty_input.text))*(float(self.ids.vat.text)/100.0)) - ((float(product['PRICE'])*int(self.ids.qty_input.text))*(float(self.ids.discount.text)/100.0)))
                                purchase_total = 'Total: '+str(self.ptotal)
                                self.ids.price_input.text = str(product['PRICE'])

                                self.ids.total_preview.text = str(purchase_total)
                            except:
                                pass
        except:
            pass
    def generate_bill(self, invoice_number):
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
    def new_invoice(self):
        ids = ''
        sizes = ''
        products = ''
        qties = ''
        prices = ''

        if float(self.ids.serv_charge.text) > 0.0 or self.ids.serv_charge.text=='':
            self.ptotal += (float(self.ids.serv_charge.text))
            self.ids.serv_charge.text = '0.0'
        
        print(self.ptotal)
        try:
            for id in self.products_ids:
                ids+= id+'\n'
            for size in self.products_dimensions:
                sizes+= size+'\n'
            for product in self.products_in_basket:
                products+= product+'\n'
            for qty in self.per_product_quantities:
                qties+= qty+'\n'
            for price in self.per_product_prices:
                prices+= price+'\n'
            # Check if any of the invoice fields are empty or not
            if self.ids.invoice_number.text != '' and self.ids.delivery_number.text != '' and self.ids.delivery_date.text != '' and self.ids.sold_to.text != '' and self.ids.address.text != '' and self.ids.contact_number.text != '' and ids != '' and products != '' and sizes != '' and qties != '' and prices != '' and self.ids.payment_method.text != '':
                response = data_entry.add_invoice([self.ids.invoice_number.text, str(datetime.date.today()), str(self.ids.delivery_number.text), str(self.ids.delivery_date.text), str(self.ids.sold_to.text), str(self.ids.address.text), str(self.ids.contact_number.text), str(ids), products, sizes, str(qties), prices, self.ptotal, self.ids.payment_method.text, self.ids.loggedin_user.text, 'FALSE', len(self.products_ids), '0.0', self.ptotal])
                if response == 'DATA RECORDED':
                    SubmitSuccessPopup().open()
                    self.generate_bill(self.ids.invoice_number.text)
                    # Empty or clean all the fields
                    self.cart = []
                    self.pqty = []
                    self.ptotal = 0.00

                    self.products_ids = []
                    self.products_dimensions = []
                    self.products_in_basket = []
                    self.per_product_quantities = []
                    self.per_product_prices = []

                    #self.ids.id_input.text = ''
                    self.ids.qty_input.text == 'Select Product'
                    self.ids.receipt_preview.text = ''
                    self.ids.stock_remaining.text = ''
                    self.ids.price_input.text = ''

                    self.ids.total_preview.text = ''
                    self.ids.products.clear_widgets()

                    self.ids.invoice_number.text = ''
                    self.ids.delivery_number.text = ''
                    self.ids.delivery_date.text = ''
                    self.ids.sold_to.text = ''
                    self.ids.address.text = ''
                    self.ids.contact_number.text = ''
                    self.ids.payment_method.text = ''
        except:
            pass
    def clear_fields(self):
        self.cart = []
        self.pqty = []
        self.ptotal = 0.00

        self.products_ids = []
        self.products_dimensions = []
        self.products_in_basket = []
        self.per_product_quantities = []
        self.per_product_prices = []

        self.ids.id_input.text = ''
        self.ids.qty_input.text = ''
        self.ids.receipt_preview.text = ''
        self.ids.stock_remaining.text = ''
        self.ids.price_input.text = ''
        self.ids.total_preview.text = ''
        self.ids.products.clear_widgets()

        self.ids.invoice_number.text = ''
        self.ids.delivery_number.text = ''
        self.ids.delivery_date.text = ''
        self.ids.sold_to.text = ''
        self.ids.address.text = ''
        self.ids.contact_number.text = ''
        self.ids.payment_method.text = ''
        self.ids.id_input.text = ''
        self.ids.serv_charge.text = '0.0'



    def reload_window(self, *args):
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
                    self.ids.staff_menu.add_widget(adminButton)
                    break
    def invoices_window(self):
        self.parent.parent.current = 'invoices'
        self.parent.parent.parent.ids.screen_invoices.children[0].ids.loggedin_user.text = self.ids.loggedin_user.text
        self.parent.parent.parent.ids.screen_invoices.children[0].reload_invoices()
    def create_invoice(self):
        self.parent.parent.current = 'staff'
    def admin(self, obj):
        self.parent.parent.current = 'admin'
        self.parent.parent.parent.ids.admin_panel.children[0].ids.loggedin_user.text = self.ids.loggedin_user.text
        self.parent.parent.parent.ids.admin_panel.children[0].reload_admin()
class StaffApp(App):
    def build(self):
        return StaffWindow()



if __name__ == "__main__":
    StaffApp().run()
