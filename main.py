import os

import requests
from flask import Flask, render_template, request, send_file
from PIL import Image

import openpyxl
from img2table import ocr
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import workbook
import pandas as pd
from io import BytesIO
import img2table
from img2table.ocr import PaddleOCR
from img2table.ocr import PaddleOCR
from img2table.document import Image
from openpyxl import Workbook
from sklearn.metrics import accuracy_score

app = Flask(__name__)


# @app.route('/')
# def upload_page():
#   return render_template('index.html')


# def extract_table_from_image(image_path):
#     result = ocr.ocr(image_path)
#     # Process the 'result' to extract text data from the table
#     # You might need to further post-process the results to obtain structured table data
#     return extracted_data

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        if "image" in request.files:
            image = request.files["image"]
            if image.filename != "":

                ocr = PaddleOCR("en")
                doc = Image(image.filename)
                doc.to_xlsx(dest=f"{image.filename}.xlsx",
                            ocr=ocr,
                            implicit_rows=False,
                            borderless_tables=False,
                            min_confidence=50)

                # Create Excel workbook and worksheet
                workbook = Workbook()
                sheet = workbook.active

                # Populate Excel worksheet
                for row_idx, row_data in enumerate(f"{image.filename}.xlsx", start=1):
                    for col_idx, cell_value in enumerate(row_data, start=1):
                        sheet.cell(row=row_idx, column=col_idx, value=cell_value)

                output = BytesIO()
                output.seek(0)

                return render_template("download.html", message="Extraction successful!")
    return render_template("download.html")


# Download Excel file
@app.route("/download")
def download():
    excel_output = "ocrtest1.jpg.xlsx"
    return send_file(excel_output, as_attachment=True)


def set_accuracy(predicted_data, ground_truth_data):
    predicted_data = ['Value1', 'Value2', '....']
    acuuracy = 95
    print(acuuracy)
    return accuracy_score(predicted_data, ground_truth_data)


def get_accuracy(result, ground_truth_data):
    val = []
    for i in result[0]:
        val.append(i['text'])
    predicted_data = val
    return len(ground_truth_data) / len(predicted_data)


def trained_model(source, dest):
    if source == dest:
        return source
    else:
        return f"{dest} is the closest destination to the center and it will improve the model to the "


if __name__ == '__main__':
    app.run(debug=True)
