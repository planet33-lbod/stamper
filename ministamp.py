from flask import Flask, request, send_file
import fitz  # PyMuPDF
import io

app = Flask(__name__)

@app.route('/stamp-pdf', methods=['POST'])
def stamp_pdf():
    # Retrieve PDF file from the request
    pdf_file = request.data  # Get binary data directly
    
    # Apply stamp logic with hardcoded coordinates and image inside the function
    stamped_pdf_bytes = add_image_to_pdf(io.BytesIO(pdf_file))
    
    # Return the stamped PDF
    stamped_pdf_bytes.seek(0)  # Rewind to the beginning of the file before sending
    return send_file(stamped_pdf_bytes, download_name='stamped.pdf', as_attachment=True)

def add_image_to_pdf(input_pdf_bytes):
    # Hardcode the stamp image path
    image_path = 'gebucht.png'
    
    # Hardcode the coordinates for the stamp
    x_coord, y_coord = (200, 100)
    
    doc = fitz.open(stream=input_pdf_bytes, filetype='pdf')
    page = doc[0]  # Assuming stamping the first page
    
    # Define the rectangle where the image will be placed (hardcoded size)
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