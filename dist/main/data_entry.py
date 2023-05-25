import gspread

gc = gspread.service_account(filename='credentials.json')
staff_sheet = gc.open('TTI_DOORS_SELLING').get_worksheet(0)
product_sheet = gc.open('TTI_DOORS_SELLING').get_worksheet(1)
invoice_sheet = gc.open('TTI_DOORS_SELLING').get_worksheet(2)

def verify_member(username, password):
    for staff in staff_sheet.get_all_records():
        print(staff['STAFF_USERNAME'])
        if staff['STAFF_USERNAME'] == str(username):
            if staff['PASSWORD'] == password:
                return staff
            elif staff['PASSWORD'] != password:
                return None
def add_staff(row_data):
    staff_sheet.append_row(row_data)
    return 'DATA RECORDED'
def add_invoice(row_data):
    invoice_sheet.append_row(row_data)
    return 'DATA RECORDED'
def add_product(row_data):
    product_sheet.append_row(row_data)
    return 'PRODUCT RECORD STORED'

def update_inventory(product_id, qty):
    count = 0
    for product in product_sheet.get_all_values():
        if product[0] == product_id:
            product_sheet.update_cell(count+1, 5, int(product[4]) - int(qty))
        count+=1

def update_invoice(invoice_number, status, paid_amount):
    count = 0
    for invoice in invoice_sheet.get_all_values():
        if invoice[0] == invoice_number:
            invoice_sheet.update_cell(count+1, 16, status)

            # subtract paid_amount from previous paid_amount
            paid_amount = float(paid_amount) + float(invoice[17])

            # if paid amount is greater than Total_Amount then make paid_amount = Total_Amount
            if float(paid_amount) > float(invoice[12]):
                # making paid_amount is equal to Total Amount
                paid_amount = float(invoice[12])
            # Update the Paid_Amount in the sheet
            invoice_sheet.update_cell(count+1, 18, str(paid_amount))
            
            # initializing due as 0.0
            due = 0.0
            # subtract updated paid-amount from the Total_Amount in the sheet
            due = float(invoice[12]) - float(paid_amount)

            # if the due is less than zero then enters the condition
            if due < 0:
                # makes the due to 0.0
                due = 0.0
            # Updates the Due_Amount in the sheet
            invoice_sheet.update_cell(count+1, 19, str(due))
            print(count+1)
            print(invoice)
            if invoice_sheet.get_all_records()[count-1]['DELIVERY_STATUS'] == 'TRUE':
                print(invoice_sheet.get_all_records()[count-1]['PRODUCTS_IDS'])
                print(invoice_sheet.get_all_records()[count-1]['QUANTITIES'])
                ids = str(invoice_sheet.get_all_records()[count-1]['PRODUCTS_IDS']).split()
                qties = str(invoice_sheet.get_all_records()[count-1]['QUANTITIES']).split()
                print(ids, qties)
                itr = 0
                for id in ids:
                    print(id, qties[itr])
                    if id != '' and qties[itr] != '':
                        update_inventory(id, qties[itr])
                    itr+=1
            break
        count+=1

# Updating Staff Credentials

def update_staff(row_data):
    count = 0
    print(row_data)
    for staff in staff_sheet.get_all_values():
        if str(staff[0]) == str(row_data[0]):
            print('matched')
            staff_sheet.update_cell(count+1, 1, row_data[1])
            staff_sheet.update_cell(count+1, 2, row_data[2])
            staff_sheet.update_cell(count+1, 3, row_data[3])
            staff_sheet.update_cell(count+1, 4, row_data[4])
            staff_sheet.update_cell(count+1, 5, row_data[5])
            staff_sheet.update_cell(count+1, 6, row_data[6])
            return 'DATA RECORDED'
        count+=1
def update_product(row_data):
    count=0
    for product in product_sheet.get_all_values():
        if str(product[0]) == str(row_data[0]):
            product_sheet.update_cell(count+1, 1, row_data[1])
            product_sheet.update_cell(count+1, 2, row_data[2])
            product_sheet.update_cell(count+1, 3, row_data[3])
            product_sheet.update_cell(count+1, 4, row_data[4])
            product_sheet.update_cell(count+1, 5, row_data[5])
            product_sheet.update_cell(count+1, 6, row_data[6])
            product_sheet.update_cell(count+1, 7, row_data[7])
            return 'DATA RECODED'
        count+=1
def delete_staff(staff_id):
    count = 0
    for staff in staff_sheet.get_all_values():
        if str(staff[0]) == str(staff_id):
            staff_sheet.delete_row(count+1)
            return 'DATA REMOVED'
        count+=1

def delete_product(product_id):
    count=0
    for product in product_sheet.get_all_values():
        if str(product[0]) == str(product_id):
            product_sheet.delete_row(count+1)
            return 'DATA REMOVED'
        count+=1