# PLR TXT to PDF converter
# Author: M.T.B.N. (https://github.com/waptug)
# Date: 2021-08-29
# Version: 1.0.0
# Usage: python txt2pdf.py
# Description: This script converts all .txt files in a folder and its subfolders to .pdf files.
#              It also creates an index.html file in the destination folder with links to the converted files.
# License: GPLv3
# References:
#   https://stackoverflow.com/questions/57354700/how-to-convert-txt-file-to-pdf-file-using-python

import os
import glob
import chardet
import textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Frame, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from tqdm import tqdm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# Register a new font
pdfmetrics.registerFont(TTFont('Courier', 'COUR.TTF'))

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def convert_to_utf8(input_file, output_file):
    original_encoding = detect_encoding(input_file)

    try:
        with open(input_file, 'r', encoding=original_encoding) as f_in:
            content = f_in.read()

        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.write(content)

    except FileNotFoundError:
        print(f"{input_file} not found.")
    except UnicodeDecodeError:
        print(f"Error decoding {input_file} with {original_encoding} encoding.")

def text_to_pdf(text_file, pdf_file):
    c = canvas.Canvas(pdf_file, pagesize=letter)

    try:
        with open(text_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        total_lines = len(lines)

        y = 750
        progress_bar = tqdm(total=total_lines, ncols=60, unit=' lines')

        for line in lines:
            # Wrap text
            wrapped_lines = textwrap.wrap(line, width=80)

            for wrapped_line in wrapped_lines:
                # Set font
                c.setFont('Courier', 12)

                # Write text
                c.drawString(30, y, wrapped_line.strip())
                y -= 15

                # Add a new page if necessary
                if y < 30:
                    c.showPage()
                    y = 750

            # Add a blank line between paragraphs
            if line.strip() == '':
                y -= 15

            progress_bar.update(1)
            progress_bar.set_postfix(file=text_file)

        progress_bar.close()

        # Save the pdf with name .pdf
        c.save()

    except FileNotFoundError:
        print(f"{text_file} not found.")

def convert_files_in_folder(source_folder, dest_folder):
    converted_files = []

    # Traverse directory recursively
    for dirpath, dirs, files in os.walk(source_folder):
        # Get the corresponding destination subfolder
        dest_subfolder = os.path.join(dest_folder, os.path.relpath(dirpath, source_folder))

        # Create the destination subfolder if it doesn't exist
        os.makedirs(dest_subfolder, exist_ok=True)

        # Find all .txt files in directory
        txt_files = glob.iglob(os.path.join(dirpath, '*.[tT][xX][tT]'), recursive=True)

        total_files = len(list(txt_files))

        progress_bar = tqdm(total=total_files, ncols=60, unit=' files')

        for filename in glob.iglob(os.path.join(dirpath, '*.[tT][xX][tT]'), recursive=True):
            # Convert to UTF-8 if necessary
            utf8_filename = os.path.join(dest_subfolder, os.path.basename(filename[:-4] + '_utf8.txt'))
            convert_to_utf8(filename, utf8_filename)

            # Convert .txt to .pdf
            pdf_filename = os.path.join(dest_subfolder, os.path.basename(filename[:-4] + '.pdf'))
            text_to_pdf(utf8_filename, pdf_filename)
            converted_files.append(pdf_filename)

            # Delete the intermediate UTF-8 file if it exists
            if os.path.exists(utf8_filename):
                os.remove(utf8_filename)

            progress_bar.update(1)
            progress_bar.set_postfix(file=filename)

        progress_bar.close()

    return converted_files

def create_html_index(dest_folder, files):
    html = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "    <title>Index of PDF Converted Files</title>",
        "</head>",
        "<body>",
        "    <h1>Index of PDF Converted Files</h1>",
        "    <ul>",
    ]

    for file in files:
        relative_path = os.path.relpath(file, dest_folder)
        html.append(f"        <li><a href='{relative_path}'>{relative_path}</a></li><br/>")

    html.extend([
        "    </ul>",
        "</body>",
        "</html>",
    ])

    with open(os.path.join(dest_folder, "index.html"), 'w') as f:
        f.write('\n'.join(html))

def add_header(canvas, document_path):
    folder_name = os.path.basename(os.path.dirname(document_path))
    file_name = os.path.basename(document_path)
    header_text = [
        "MTBN.NET PLR Library",
        f"Category: {folder_name} File: {file_name}",
        "Text and Word PLR Article Packs available at PLRImporter.Com"
    ]

    # Set header parameters
    header_height = .5 * inch
    header_font_size = 10

    # Create a frame for the header
    frame = Frame(
        x1=inch,
        y1=letter[1] - header_height,
        width=letter[0] - 2 * inch,
        height=header_height,
        leftPadding=0,
        bottomPadding=0,
        rightPadding=0,
        topPadding=0,
        id='header_frame',
    )

    # Create header styles
    styles = getSampleStyleSheet()
    header_style = styles['Normal']
    header_style.fontSize = header_font_size
    header_style.alignment = 1  # Center alignment

    # Create header paragraphs
    header_paragraphs = []
    for line in header_text:
        paragraph = Paragraph(line, header_style)
        header_paragraphs.append(paragraph)

    # Add paragraphs to the frame
    frame.addFromList(header_paragraphs, canvas)

    # Draw a black border around the header
    canvas.setStrokeColor(colors.black)
    canvas.rect(inch, letter[1] - header_height, letter[0] - 2 * inch, header_height)


def text_to_pdf_with_header(text_file, pdf_file):
    c = canvas.Canvas(pdf_file, pagesize=letter)

    try:
        with open(text_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        total_lines = len(lines)

        y = 690  # Adjust the starting y-position to accommodate the header
        progress_bar = tqdm(total=total_lines, ncols=60, unit=' lines')

        for line in lines:
            # Wrap text
            wrapped_lines = textwrap.wrap(line, width=80)

            for wrapped_line in wrapped_lines:
                # Set font
                c.setFont('Courier', 12)

                # Write text
                c.drawString(30, y, wrapped_line.strip())
                y -= 15

                # Add a new page if necessary
                if y < 60:  # Adjust the y-coordinate to accommodate the header
                    add_header(c, os.path.abspath(text_file))
                    c.showPage()
                    y = 690  # Adjust the y-coordinate to accommodate the header

            # Add a blank line between paragraphs
            if line.strip() == '':
                y -= 15

            progress_bar.update(1)
            progress_bar.set_postfix(file=text_file)

        # Add the header to the last page
        add_header(c, os.path.abspath(text_file))

        progress_bar.close()

        # Save the pdf with name .pdf
        c.save()

    except FileNotFoundError:
        print(f"{text_file} not found.")

def convert_files_in_folder_with_header(source_folder, dest_folder):
    converted_files = []

    # Traverse directory recursively
    for dirpath, dirs, files in os.walk(source_folder):
        # Get the corresponding destination subfolder
        dest_subfolder = os.path.join(dest_folder, os.path.relpath(dirpath, source_folder))

        # Create the destination subfolder if it doesn't exist
        os.makedirs(dest_subfolder, exist_ok=True)

        # Find all .txt files in directory
        txt_files = glob.iglob(os.path.join(dirpath, '*.[tT][xX][tT]'), recursive=True)

        total_files = len(list(txt_files))

        progress_bar = tqdm(total=total_files, ncols=60, unit=' files')

        for filename in glob.iglob(os.path.join(dirpath, '*.[tT][xX][tT]'), recursive=True):
            # Convert to UTF-8 if necessary
            utf8_filename = os.path.join(dest_subfolder, os.path.basename(filename[:-4] + '_utf8.txt'))
            convert_to_utf8(filename, utf8_filename)

            # Convert .txt to .pdf with header
            pdf_filename = os.path.join(dest_subfolder, os.path.basename(filename[:-4] + '.pdf'))
            text_to_pdf_with_header(utf8_filename, pdf_filename)
            converted_files.append(pdf_filename)

            # Delete the intermediate UTF-8 file if it exists
            if os.path.exists(utf8_filename):
                os.remove(utf8_filename)

            progress_bar.update(1)
            progress_bar.set_postfix(file=filename)

        progress_bar.close()

    return converted_files

# Use the functions
source_folder = input("Please enter the path to the source folder: ")
dest_folder = input("Please enter the path to the destination folder: ")

# Create the destination folder if it doesn't exist
os.makedirs(dest_folder, exist_ok=True)

converted_files = convert_files_in_folder_with_header(source_folder, dest_folder)
create_html_index(dest_folder, converted_files)



