import os
import pandas as pd
import glob
import pathlib
from fpdf import FPDF


def generate(invoices_path, pdfs_path, image_path, company_name, product_id,
             product_name, amount_purchased, price_per_unit, total_price):
    """
    This function converts invoice Excel files into PDF invoices
    :param invoices_path:
    :param pdfs_path:
    :param image_path:
    :param company_name:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """

    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        # Defininitions
        filename = pathlib.Path(filepath).stem
        invoice_nr, date = filename.split("-")

        # Add Invoice Number
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_nr}", ln=1)

        # Add Date
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Date {date}", ln=1)

        # Information Table
        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        # Add Header
        columns = df.columns
        columns = [item.replace("_", " ").title() for item in columns]
        pdf.set_font(family="Arial", size=10, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=60, h=8, txt=columns[1], border=1)
        pdf.cell(w=40, h=8, txt=columns[2], border=1)
        pdf.cell(w=30, h=8, txt=columns[3], border=1)
        pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

        # Add Rows and Data
        for index, row in df.iterrows():
            pdf.set_font(family="Arial", size=10, style="")
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=60, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=40, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)

        # Calculate final total
        fin_total = df[total_price].sum()
        pdf.set_font(family="Arial", size=10, style="")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=60, h=8, txt="", border=1)
        pdf.cell(w=40, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt=f"{fin_total}", border=1, ln=1)

        pdf.set_text_color(0, 0, 0)

        # Add total sum in sentence
        pdf.set_font(family="Arial", size=10, style="B")
        pdf.cell(w=30, h=8, txt=f"The total price is {fin_total} USD", ln=1)

        # Add company name and logo
        pdf.set_font(family="Arial", size=14, style="B")
        pdf.cell(w=20, h=8, txt=company_name)
        pdf.image(image_path, w=10)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/{filename}.pdf")