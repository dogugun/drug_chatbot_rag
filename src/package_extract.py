import os
import shutil
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fpdf import FPDF
from bs4 import BeautifulSoup
import pdfkit

from variables import CURRENT_SPL_FOLDER

BASEDIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ZIP_FOLDER_PATH = os.path.join(BASEDIR, "data", CURRENT_SPL_FOLDER, "prescription")
EXTRACTED_LOC = os.path.join(BASEDIR, "data", "prescriptions")
EXTRACTED_LOC_XML = os.path.join(BASEDIR, "data", "prescriptions", "xml")
EXTRACTED_LOC_PDF = extracted_loc_xml = os.path.join(BASEDIR, "data", "prescriptions", "pdf")

def initialize_folders():
    shutil.rmtree(os.path.join(EXTRACTED_LOC))
    os.makedirs(extracted_loc_xml, exist_ok=True)
    os.makedirs(EXTRACTED_LOC_PDF, exist_ok=True)


def xml_file_to_pdf_old(xml_file_path, output_pdf):
    with open(xml_file_path, "r") as xml_file:
        xml_data = xml_file.read()

    c = canvas.Canvas(output_pdf, pagesize=letter)
    c.drawString(100, 750, xml_data)  # Replace this with your XML data processing logic
    c.save()


def xml_to_pdf(xml_path, output_pdf):
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'XML to PDF', align='C', ln=True)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', align='C')

    with open(xml_path, "r") as xml_file:
        xml_data = xml_file.read()
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, xml_data)  # Replace this with your XML data processing logic
    pdf.output(output_pdf)

def xml_to_html(xml_path, pdf_path):
    with open(xml_path, "r") as xml_file:
        xml_data = xml_file.read()
    soup = BeautifulSoup(xml_data, 'lxml')

    # Convert the parsed XML to HTML
    html = soup.prettify()
    pdfkit.from_string(html, pdf_path)
    return html


def fetch_pdfs():
    pdf_list = []
    all_pdf_files = os.listdir(EXTRACTED_LOC_PDF)
    for pdf_f in all_pdf_files:
        name, ext = os.path.splitext(pdf_f)
        if ext == ".pdf":
            pdf_list.append(os.path.join(EXTRACTED_LOC_PDF, pdf_f))
    return pdf_list




def convert_all_xml_files_to_pdf():
    initialize_folders()
    all_zip_files = os.listdir(ZIP_FOLDER_PATH)
    all_zip_files = [zfile for zfile in all_zip_files if ".zip" in zfile]
    for zip_file in all_zip_files:
        zip_path = os.path.join(ZIP_FOLDER_PATH, zip_file)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            xml_filename = [file_obj.filename for file_obj in zip_ref.filelist if ".xml" in file_obj.filename][0]
            zip_ref.extract(xml_filename, os.path.join(EXTRACTED_LOC, xml_filename))

            extracted_file = os.listdir(os.path.join(EXTRACTED_LOC, xml_filename))[0]
            shutil.move(os.path.join(EXTRACTED_LOC, xml_filename, extracted_file), os.path.join(extracted_loc_xml, xml_filename))
        shutil.rmtree(os.path.join(EXTRACTED_LOC, xml_filename))



    all_zip_files = os.listdir(extracted_loc_xml)
    for zip_file in all_zip_files:
        xml_path = os.path.join(extracted_loc_xml, zip_file)
        pdf_path = os.path.join(EXTRACTED_LOC_PDF, zip_file.replace(".xml", ".pdf"))
        xml_to_html(xml_path, pdf_path)

