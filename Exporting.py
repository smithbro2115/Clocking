import openpyxl
from openpyxl import styles
from LocalFileHandling import get_app_data_folder, make_folder_if_it_does_not_exist
from datetime import datetime
from Company import Company
from PyQt5 import QtWidgets
import os


invoice_template_path = f"{get_app_data_folder('')}/Invoice.xlsx"
align = styles.Alignment(horizontal='left')
font = styles.Font(size=12)
default_company = Company(name='Brinkman Adventures', address='13939 N. Cedarburg Rd. Mequon, WI 53097',
                          phone_number='262-227-8621', email='ian@brinkmanadventures.com',
                          motto='“Inspiring the next generation of missionaries”')


def make_invoice_excel(user, categories, path=None):
    excel_path = make_new_excel_from_template(user, path)
    wb = openpyxl.load_workbook(excel_path)
    sheet = wb.active
    add_user_info_to_invoice(sheet, user)
    add_company_info_to_invoice(sheet, default_company)
    for category in categories:
        add_category_to_invoice(category, sheet)
    wb.save(excel_path)


def verify_path(path):
    file_path, file_extension = os.path.splitext(path)
    if file_extension is not '.xlsx':
        path = file_path + ".xlsx"
    return path


def add_user_info_to_invoice(df, user):
    date = datetime.now()
    df.cell(row=5, column=2).value = date.date()
    df.cell(row=7, column=2).value = f"{user.first_name.capitalize()} {user.last_name.capitalize()}"
    df.cell(row=11, column=2).value = user.address
    df.cell(row=13, column=2).value = user.phone_number
    df.cell(row=15, column=2).value = user.email
    for column in range(1, 5):
        for row in range(4, 15):
            cell = df.cell(row=row, column=column)
            cell.alignment = align
            cell.font = font


def add_company_info_to_invoice(df, company):
    df.cell(row=1, column=7).value = company.name
    df.cell(row=2, column=7).value = company.motto
    df.cell(row=7, column=7).value = company.name
    df.cell(row=9, column=7).value = company.address
    df.cell(row=13, column=7).value = company.phone_number
    df.cell(row=15, column=7).value = company.email
    for column in range(7, 10):
        for row in range(4, 15):
            cell = df.cell(row=row, column=column)
            cell.alignment = align
            cell.font = font


def add_category_to_invoice(category, df):
    for i in range(18, 28):
        if not df.cell(row=i, column=1).value:
            date = datetime.now()
            df.cell(row=i, column=1).value = date.date()
            df.cell(row=i, column=2).value = round(float(category.clock.total_monthly_time.seconds)/3600, 4)
            df.cell(row=i, column=3).value = category.category_number
            df.cell(row=i, column=4).value = category.description
            df.cell(row=i, column=8).value = category.wage
            return True
    return False


def make_new_excel_from_template(user, path=None):
    import shutil
    if path:
        new_path = path
    else:
        new_dir = f"{user.directory}/Invoices"
        make_folder_if_it_does_not_exist(user.directory, 'Invoices')
        new_path = f"{new_dir}/{get_file_invoice_name(user)}"
    new_path = verify_path(new_path)
    shutil.copy(invoice_template_path, new_path)
    return new_path


def get_file_invoice_name(user):
    date = datetime.now()
    return f"{user.first_name}_{user.last_name}_Invoice" \
        f"_{date.strftime('%B')}_{date.year}.xlsx"


class GetFileLocationDialog(QtWidgets.QFileDialog):
    def __init__(self, default_name):
        super(GetFileLocationDialog, self).__init__()
        self.default_name = default_name

    def get_save_path(self):
        result = self.getSaveFileName(directory=f'/{self.default_name}', caption='Export Invoice')[0]
        return result
