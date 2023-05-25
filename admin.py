import datetime
import os
import sys

import pandas as pd
from functools import partial

from kivy.uix.button import Button
import subprocess

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.popup import Popup


if getattr(sys, 'frozen', False):
    # running in a bundle
    template_path = os.path.join(sys._MEIPASS, 'admin.kv')
else:
    # running live
    template_path = 'admin.kv'

Builder.load_file(template_path)


import data_entry

class SuccessPopup(Popup):
    """Popup to show the use that the submission is successful."""
    pass
class DeleteSuccessPopup(Popup):
    """Popup to show the use that the submission is successful."""
    pass

class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.staffid = ''
        self.productid = ''
    def show_staff(self, staff_id):
        self.staffid = staff_id
        self.ids.staff_id.text = ''
        self.ids.staff_name.text = ''
        self.ids.staff_username.text = ''
        self.ids.is_staff.text = ''
        self.ids.is_admin.text = ''
        self.ids.password.text = ''
        for staff in data_entry.staff_sheet.get_all_records():
            if str(staff['STAFF_ID']) == str(staff_id):
                self.ids.staff_id.text = str(staff['STAFF_ID'])
                self.ids.staff_name.text = str(staff['STAFF_NAME'])
                self.ids.staff_username.text = str(staff['STAFF_USERNAME'])
                self.ids.is_staff.text = str(staff['IS_STAFF'])
                self.ids.is_admin.text = str(staff['IS_ADMIN'])
                self.ids.password.text = str(staff['PASSWORD'])
    def update_staff(self):
        RES_MSG = data_entry.update_staff([self.staffid, self.ids.staff_id.text, self.ids.staff_name.text, self.ids.staff_username.text, self.ids.is_staff.text.upper(), self.ids.is_admin.text.upper(), self.ids.password.text])
        self.staffid = self.ids.staff_id.text
        if RES_MSG == 'DATA RECORDED':
            self.parent.parent.parent.ids.admin_panel.children[0].reload_admin()
            SuccessPopup().open()
    def add_staff(self):
        if self.ids.staff_id.text !="" and self.ids.staff_name.text !="" and self.ids.staff_username.text !="" and self.ids.is_staff.text != '' and self.ids.is_admin.text !='' and self.ids.password.text != '':
            if self.ids.is_staff.text.upper() == 'TRUE' or self.ids.is_staff.text.upper() == 'FALSE' or self.ids.is_admin.text.upper() == 'TRUE' or self.ids.is_admin.text.upper() == 'FALSE':
                res_msg = data_entry.add_staff([self.ids.staff_id.text, self.ids.staff_name.text, self.ids.staff_username.text, self.ids.is_staff.text.upper(), self.ids.is_admin.text.upper(), self.ids.password.text])
                if res_msg == 'DATA RECORDED':
                    SuccessPopup().open()
                    self.ids.staff_id.text=''
                    self.ids.staff_name.text=''
                    self.ids.staff_username.text=''
                    self.ids.is_staff.text=''
                    self.ids.is_admin.text=''
                    self.ids.password.text=''
                    self.parent.parent.parent.ids.admin_panel.children[0].reload_admin()
    def remove_staff(self):
        res_msg = data_entry.delete_staff(self.staffid)
        if res_msg == 'DATA REMOVED':
            self.staffid = ''
            self.ids.staff_id.text = ''
            self.ids.staff_name.text = ''
            self.ids.staff_username.text = ''
            self.ids.is_staff.text = ''
            self.ids.is_admin.text = ''
            self.ids.password.text = ''
            self.parent.parent.parent.ids.admin_panel.children[0].reload_admin()
            DeleteSuccessPopup().open()
    def show_product(self, product_id):
        self.productid = product_id
        self.ids.product_id.text = ''
        self.ids.product_name.text = ''
        self.ids.product_size.text = ''
        self.ids.product_price.text = ''
        self.ids.product_stock.text = ''
        for product in data_entry.product_sheet.get_all_records():
            if str(product['PRODUCT_ID']) == str(product_id):
                self.ids.product_id.text = str(product['PRODUCT_ID'])
                self.ids.product_name.text = str(product['PRODUCT_NAME'])
                self.ids.product_size.text = str(product['SIZE'])
                self.ids.product_price.text = str(product['PRICE'])
                self.ids.product_stock.text = str(product['STOCK'])
    def add_product(self):
        if self.ids.product_id.text != '' and self.ids.product_name.text != '' and self.ids.product_size.text != '' and self.ids.product_price.text != '' and self.ids.product_stock.text != '':
            res_msg = data_entry.add_product([self.ids.product_id.text,
                                    self.ids.product_name.text,
                                    self.ids.product_size.text,
                                    self.ids.product_price.text,
                                    self.ids.product_stock.text,
                                    self.ids.loggedin_user.text,
                                    str(datetime.date.today())])
            if res_msg == 'PRODUCT RECORD STORED':
                # self.productid = ''
                self.ids.product_id.text = ''
                self.ids.product_name.text = ''
                self.ids.product_size.text = ''
                self.ids.product_price.text = ''
                self.ids.product_stock.text = ''
                self.parent.parent.parent.ids.admin_panel.children[0].reload_admin()
                SuccessPopup().open()
    def remove_product(self):
        res_msg = data_entry.delete_product(self.productid)
        if res_msg == 'DATA REMOVED':
            self.productid = ''
            self.ids.product_id.text = ''
            self.ids.product_name.text = ''
            self.ids.product_size.text = ''
            self.ids.product_price.text = ''
            self.ids.product_stock.text = ''
            self.parent.parent.parent.ids.admin_panel.children[0].reload_admin()
            DeleteSuccessPopup().open()
    def update_product(self):
        res_msg = data_entry.update_product([self.productid,
                                             self.ids.product_id.text,
                                             self.ids.product_name.text,
                                             self.ids.product_size.text,
                                             self.ids.product_price.text,
                                             self.ids.product_stock.text,
                                             self.ids.loggedin_user.text,
                                             str(datetime.date.today())])
        if res_msg == 'DATA RECODED':
            self.productid = self.ids.product_id.text
            self.parent.parent.parent.ids.admin_panel.children[0].reload_admin()
            SuccessPopup().open()
    def reload_admin(self):
        self.ids.staff_list.clear_widgets()
        for staff in data_entry.staff_sheet.get_all_records():
            details = BoxLayout(
                size_hint_y=None,
                height=30, pos_hint={"top": 1},
            )
            self.ids.staff_list.add_widget(details)
            details.add_widget(
                Label(
                    text=f"{staff['STAFF_ID']}",
                    size_hint_x=0.08,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{staff['STAFF_NAME']}",
                    size_hint_x=0.08,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{staff['STAFF_USERNAME']}",
                    size_hint_x=0.08,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{staff['IS_STAFF']}",
                    size_hint_x=0.08,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{staff['IS_ADMIN']}",
                    size_hint_x=0.08,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{staff['PASSWORD']}",
                    size_hint_x=0.08,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            view_button = Button(
                text="View",
                size_hint_x=0.04,
                background_color=(0.06, 0.32, 0.32, 1)
            )

            # Using partial to pass the invoice number as an argument to the method

            view_button.on_release = partial(self.show_staff, staff['STAFF_ID'])
            details.add_widget(view_button)
        self.ids.product_list.clear_widgets()
        for product in data_entry.product_sheet.get_all_records():
            details = BoxLayout(
                size_hint_y=None,
                height=30, pos_hint={"top": 1},
            )
            self.ids.product_list.add_widget(details)
            details.add_widget(
                Label(
                    text=f"{product['PRODUCT_ID']}",
                    size_hint_x=0.04,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{product['PRODUCT_NAME']}",
                    size_hint_x=0.04,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{product['SIZE']}",
                    size_hint_x=0.12,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{product['PRICE']}",
                    size_hint_x=0.04,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{product['STOCK']}",
                    size_hint_x=0.04,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{product['ADDED_BY']}",
                    size_hint_x=0.08,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            details.add_widget(
                Label(
                    text=f"{product['ADDED_ON']}",
                    size_hint_x=0.06,
                    color=(0.06, 0.45, 0.45, 1)
                )
            )
            view_button = Button(
                text="View",
                size_hint_x=0.04,
                background_color=(0.06, 0.32, 0.32, 1)
            )

            # Using partial to pass the invoice number as an argument to the method
            view_button.on_release = partial(self.show_product, product['PRODUCT_ID'])
            details.add_widget(view_button)
    def generate_sales_report(self):
        delivery_number = []
        invoice_number = []
        invoice_date = []
        models = []
        sizes = []
        qties = []
        prices = []
        totals = []
        price_totals = []
        status = []
        due_dates = []
        paid_amount = []
        due_amount = []
        for invoice in data_entry.invoice_sheet.get_all_records():
            
            mdls = str(invoice['PRODUCTS']).split()
            prces = str(invoice['PRICES']).split()
            qt = str(invoice['QUANTITIES']).split()
            sizs = str(invoice['PRODUCTS_DIMENSIONS']).split('\n')
            tot = ''
            for itr in range(len(mdls)):
                invoice_number.append(invoice['INVOICE_NUMBER'])
                delivery_number.append(invoice['DELIVERY_NUMBER'])
                invoice_date.append(invoice['INVOICE_DATE'])
                price_totals.append(invoice['AMOUNT'])
                models.append(mdls[itr])
                sizes.append(sizs[itr])
                qties.append(qt[itr])
                prices.append(prces[itr])
                totals.append(float(prces[itr])*int(qt[itr]))
                
                status.append(invoice['DELIVERY_STATUS'])
                paid_amount.append(invoice['PAID_AMOUNT'])
                due_amount.append(invoice['DUE_AMOUNT'])
                if float(invoice['DUE_AMOUNT']) > 0.0:
                    invc_date = str(invoice['INVOICE_DATE']).split('-')
                    cur_date = str(datetime.date.today()).split('-')
                    due_dates.append(f"{int(cur_date[0])-int(invc_date[0])} years {int(cur_date[1])-int(invc_date[1])} months {int(cur_date[2])-int(invc_date[2])} days")
                else:
                    due_dates.append("")

        INVOICE_REPORT = pd.DataFrame({
            "INVOICE NUMBER": invoice_number,
            "DELIVERY NUMBER": delivery_number,
            "INVOICE DATE": invoice_date,
            "MODEL(s)": models,
            "SIZE(s)": sizes,
            "QUANTITIES": qties,
            "PRICE": prices,
            "TOTAL PRICE(s)": totals,
            "TOTAL AMOUNT": price_totals,
            "PAID AMOUNT": paid_amount,
            "DUE AMOUNT": due_amount,
            "DELIVERY STATUS": status,
            "DUE DATE": due_dates
        })

        if not os.path.exists(f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS"):
            os.makedirs(f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS")
        try:
            # writing the xlsx file
            data_frame_to_excel = pd.ExcelWriter(f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS\\Sales_Report_{datetime.date.today()}.xlsx")

            # writing data from dataframe to excel
            INVOICE_REPORT.to_excel(data_frame_to_excel)

            # save the Excel sheet
            data_frame_to_excel.close()

            # open the Excel after saving
            subprocess.Popen([f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS\\Sales_Report_{datetime.date.today()}.xlsx"], shell=True)
        except:
            pass
        del delivery_number
        del invoice_number
        del invoice_date
        del models
        del sizes
        del qties
        del prices
        del totals
        del price_totals
        del status
        del due_dates
        del paid_amount
        del due_amount

        print("Memory Ops Complete")

    def generate_roster(self):
        if not os.path.exists(f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS"):
            os.makedirs(f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS")

        staffids = []
        staffnames = []
        staffunames = []
        isstaff = []
        isadmin = []
        password = []
        for staff in data_entry.staff_sheet.get_all_records():
            staffids.append(staff['STAFF_ID'])
            staffnames.append(staff['STAFF_NAME'])
            staffunames.append(staff['STAFF_USERNAME'])
            isstaff.append(staff['IS_STAFF'])
            isadmin.append(staff['IS_ADMIN'])
            password.append(staff['PASSWORD'])
        ROSTER = pd.DataFrame({
            "STAFF ID": staffids,
            "STAFF NAME": staffnames,
            "STAFF USERNAME": staffunames,
            "IS STAFF": isstaff,
            "IS ADMIN": isadmin,
            "PASSWORD": password
        })

        try:
            # writing the xlsx file
            data_frame_to_excel = pd.ExcelWriter(
                f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS\\Staff_Roster_{datetime.date.today()}.xlsx")

            # writing data from dataframe to excel
            ROSTER.to_excel(data_frame_to_excel)

            # save the Excel sheet
            data_frame_to_excel.close()

            # open the Excel after saving
            subprocess.Popen([f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS\\Staff_Roster_{datetime.date.today()}.xlsx"],
                         shell=True)
        except:
            pass
        del staffids
        del staffnames
        del staffunames
        del isstaff
        del isadmin
        del password

        print("Memory Ops Complete")

    def generate_product_sheet(self):
        productid = []
        productname =[]
        size =[]
        price = []
        stock = []
        addedby = []
        addedon = []
        if not os.path.exists(f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS"):
            os.makedirs(f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS")

        for product in data_entry.product_sheet.get_all_records():
            productid.append(product['PRODUCT_ID'])
            productname.append(product['PRODUCT_NAME'])
            size.append(product['SIZE'])
            price.append(product['PRICE'])
            stock.append(product['STOCK'])
            addedby.append(product['ADDED_BY'])
            addedon.append(product['ADDED_ON'])

        PRODUCT = pd.DataFrame({
            "PRODUCT ID": productid,
            "MODEL": productname,
            "SIZE": size,
            "PRICE": price,
            "STOCK": stock,
            "ADDED BY": addedby,
            "ADDED ON": addedon
        })
        try:
            # writing the xlsx file
            data_frame_to_excel = pd.ExcelWriter(
                f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS\\Product_Sheet_{datetime.date.today()}.xlsx")
            PRODUCT.to_excel(data_frame_to_excel)

            # save the Excel sheet
            data_frame_to_excel.close()

            # open the Excel after saving
            subprocess.Popen(
                [f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS\\Product_Sheet_{datetime.date.today()}.xlsx"],
                shell=True)
        except:
            pass

        
        del productid
        del productname
        del size
        del price
        del stock
        del addedby
        del addedon

        print("Memory Ops Complete")

    def invoices_window(self):
        self.parent.parent.current = 'invoices'
        self.parent.parent.parent.ids.screen_invoices.children[0].ids.loggedin_user.text = self.ids.loggedin_user.text
        self.parent.parent.parent.ids.screen_invoices.children[0].reload_invoices()
    def create_invoice(self):
        self.parent.parent.current = 'staff'
        self.parent.parent.parent.ids.screen_staff.children[0].ids.loggedin_user.text = self.ids.loggedin_user.text
    def admin(self):
        self.parent.parent.current = 'admin'
        self.parent.parent.parent.ids.admin_panel.children[0].ids.loggedin_user.text = self.ids.loggedin_user.text
        self.parent.parent.parent.ids.admin_panel.children[0].reload_admin()
class AdminApp(App):
    def build(self):
        return AdminWindow()


if __name__ == "__main__":
    AdminApp().run()






# def generate_sales_report(self):
#         delivery_number = []
#         invoice_number = []
#         invoice_date = []
#         models = []
#         sizes = []
#         qties = []
#         prices = []
#         totals = []
#         price_totals = []
#         status = []
#         due_dates = []
#         paid_amount = []
#         due_amount = []
#         for invoice in data_entry.invoice_sheet.get_all_records():
#             invoice_number.append(invoice['INVOICE_NUMBER'])
#             delivery_number.append(invoice['DELIVERY_NUMBER'])
#             invoice_date.append(invoice['INVOICE_DATE'])
#             models.append(invoice['PRODUCTS'])
#             sizes.append(invoice['PRODUCTS_DIMENSIONS'])
#             qties.append(invoice['QUANTITIES'])
#             prices.append(invoice['PRICES'])
#             length = str(invoice['PRODUCTS']).split()
#             prces = str(invoice['PRICES']).split()
#             qt = str(invoice['QUANTITIES']).split()
#             tot = ''
#             for itr in range(len(length)):
#                 tot+= str(float(prces[itr])*int(qt[itr]))+'\n'
#             totals.append(tot)
#             price_totals.append(invoice['AMOUNT'])
#             status.append(invoice['DELIVERY_STATUS'])
#             paid_amount.append(invoice['PAID_AMOUNT'])
#             due_amount.append(invoice['DUE_AMOUNT'])
#             if float(invoice['DUE_AMOUNT']) > 0.0:
#                 invc_date = str(invoice['INVOICE_DATE']).split('-')
#                 cur_date = str(datetime.date.today()).split('-')
#                 due_dates.append(f"{int(cur_date[0])-int(invc_date[0])} years {int(cur_date[1])-int(invc_date[1])} months {int(cur_date[2])-int(invc_date[2])} days")
#             else:
#                 due_dates.append("")

#         INVOICE_REPORT = pd.DataFrame({
#             "INVOICE NUMBER": invoice_number,
#             "DELIVERY NUMBER": delivery_number,
#             "INVOICE DATE": invoice_date,
#             "MODEL(s)": models,
#             "SIZE(s)": sizes,
#             "QUANTITIES": qties,
#             "PRICE": prices,
#             "TOTAL PRICE(s)": totals,
#             "TOTAL AMOUNT": price_totals,
#             "PAID AMOUNT": paid_amount,
#             "DUE AMOUNT": due_amount,
#             "DELIVERY STATUS": status,
#             "DUE DATE": due_dates
#         })

#         if not os.path.exists(f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS"):
#             os.makedirs(f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS")
#         # writing the xlsx file
#         data_frame_to_excel = pd.ExcelWriter(f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS\\Sales_Report_{datetime.date.today()}.xlsx")

#         # writing data from dataframe to excel
#         INVOICE_REPORT.to_excel(data_frame_to_excel)

#         # save the Excel sheet
#         data_frame_to_excel.save()

#         # open the Excel after saving
#         subprocess.Popen([f"C:\\Users\\{os.getlogin()}\\Desktop\\TTI_POS\\Sales_Report_{datetime.date.today()}.xlsx"], shell=True)

#         del delivery_number
#         del invoice_number
#         del invoice_date
#         del models
#         del sizes
#         del qties
#         del prices
#         del totals
#         del price_totals
#         del status
#         del due_dates
#         del paid_amount
#         del due_amount

#         print("Memory Ops Complete")