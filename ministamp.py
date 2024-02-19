from flask import Flask, request, send_file
import fitz  # PyMuPDF
import io
from datetime import datetime

app = Flask(__name__)

# Common function to add an image to a PDF, parameterized for flexibility
def add_image_to_pdf(input_pdf_bytes, image_path, x_coord, y_coord):
    doc = fitz.open(stream=input_pdf_bytes, filetype='pdf')
    page = doc[0]  # Assuming stamping the first page
    
    # Define the rectangle where the image will be placed (hardcoded size)
    img_rect = fitz.Rect(x_coord, y_coord, x_coord + 100, y_coord + 100)
    
    # Insert the image
    page.insert_image(img_rect, filename=image_path)
    
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    # Define the position for the date text, 50px below the stamp
    text_x = x_coord
    text_y = y_coord + 100  # Adjusted for 50px below the image assuming the image is 100px in height
    
    # Insert the date text
    page.insert_text((text_x, text_y), current_date, fontsize=11, color=(0, 0, 0))
    
    # Save the stamped PDF to a BytesIO object and return it
    output_pdf_bytes = io.BytesIO()
    doc.save(output_pdf_bytes)
    doc.close()  # It's important to close the document to free resources
    return output_pdf_bytes

@app.route('/gebucht', methods=['POST'])
def stamp_pdf_gebucht():
    pdf_file = request.data
    stamped_pdf_bytes = add_image_to_pdf(io.BytesIO(pdf_file), 'gebucht.png', 300, 80)
    stamped_pdf_bytes.seek(0)
    return send_file(stamped_pdf_bytes, download_name='stamped.pdf', as_attachment=True)

@app.route('/berechnet', methods=['POST'])
def stamp_pdf_berechnet():
    pdf_file = request.data
    stamped_pdf_bytes = add_image_to_pdf(io.BytesIO(pdf_file), 'berechnet.png', 300, 120)  # Adjust coordinates if needed
    stamped_pdf_bytes.seek(0)
    return send_file(stamped_pdf_bytes, download_name='stamped.pdf', as_attachment=True)

@app.route('/controlled', methods=['POST'])
def stamp_pdf_controlled():
    pdf_file = request.data
    stamped_pdf_bytes = add_image_to_pdf(io.BytesIO(pdf_file), 'controlled.png', 300, 160)  # Adjust coordinates if needed
    stamped_pdf_bytes.seek(0)
    return send_file(stamped_pdf_bytes, download_name='stamped.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=55100)
