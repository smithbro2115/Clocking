import pandas as pd
import xlwt
from pandas import ExcelFile, ExcelWriter
from LocalFileHandling import get_app_data_folder, make_folder_if_it_does_not_exist
import shutil
from datetime import datetime


invoice_template_path = f"{get_app_data_folder('')}/Invoice.xlsx"


def make_invoice_excel(user, categories):
    excel_path = make_new_excel_from_template(user)
    wb = xlwt.Workbook(excel_path)
    df = pd.read_excel(excel_path, header=None)
    add_user_info_to_invoice(df, user)
    for category in categories:
        add_category_to_invoice(category, df)
    print(df)


def add_user_info_to_invoice(df, user):
    date = datetime.now()
    df[1][3] = date.date()
    df[1][5] = f"{user.first_name.capitalize()} {user.last_name.capitalize()}"
    df[1][7] = user.address
    df[1][11] = user.phone_number
    df[1][13] = user.email


def add_category_to_invoice(category, df):
    for i in range(17, 27):
        print(df[0][i] == None)
        if df[0][i] == 'nan':
            date = datetime.now()
            df[0][i] = date.date()
            df[1][i] = category.clock.total_monthly_time
            df[2][i] = category.category_number
            df[2][i] = category.description
            df[3][i] = category.wage


def make_new_excel_from_template(user):
    date = datetime.now()
    new_dir = f"{user.directory}/Invoices"
    make_folder_if_it_does_not_exist(user.directory, 'Invoices')
    new_path = f"{new_dir}/{user.first_name}_{user.last_name}_Invoice" \
        f"_{date.strftime('%B')}_{date.year}.xlsx"
    shutil.copy(invoice_template_path, new_path)
    return new_path
