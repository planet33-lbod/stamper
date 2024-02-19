from flask import Flask, request, send_file
import fitz  # PyMuPDF
import io

app = Flask(__name__)

@app.route('/stamp-pdf', methods=['POST'])
def stamp_pdf():
    # Retrieve PDF file from the request
    pdf_file = request.data  # Get binary data directly
    
    # Hardcode the stamp image path
    image_path = 'gebucht.png'
    
    # Hardcode the coordinates for the stamp
    x_coord, y_coord = (200, 100)
    
    # Apply stamp logic with hardcoded coordinates and image
    stamped_pdf_bytes = add_image_to_pdf(pdf_bytes=io.BytesIO(pdf_file), image_path=image_path, x_coord=x_coord, y_coord=y_coord)
    
    # Return the stamped PDF
    stamped_pdf_bytes.seek(0)  # Rewind to the beginning of the file before sending
    return send_file(stamped_pdf_bytes, attachment_filename='stamped.pdf', as_attachment=True)

def add_image_to_pdf(input_pdf_bytes, image_path, x_coord, y_coord):
    doc = fitz.open(stream=input_pdf_bytes, filetype='pdf')
    page = doc[0]  # Assuming stamping the first page
    
    # Define the rectangle where the image will be placed
    img_rect = fitz.Rect(x_coord, y_coord, x_coord + 100, y_coord + 100)
    
    # Insert the image
    page.insert_image(img_rect, filename=image_path)
    
    # Save the stamped PDF to a BytesIO object and return it
    output_pdf_bytes = io.BytesIO()
    doc.save(output_pdf_bytes)
    doc.close()  # It's important to close the document to free resources
    return output_pdf_bytes

if __name__ == '__main__':
    app.run(debug=True, port=55100)