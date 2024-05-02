from io import BytesIO
import fitz  # PyMuPDF
from PIL import Image as PILImage
import re
import pandas as pd
import concurrent.futures
from openpyxl import Workbook
from openpyxl.drawing.image import Image as ExcelImage

def extract_images(page):
    images = page.get_images(full=True)
    return sorted(images, key=lambda img: img[0])

def extract_trademarks_and_logos(pdf_file):
    # Open the PDF document
    doc = fitz.open(pdf_file)
    trademark_data = []
    trademark_data_madrid = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Extract trademarks and images in parallel
        futures = [executor.submit(extract_images, page) for page in doc]
        
        # Iterate through each page of the PDF
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            images = futures[page_num - 1].result()  # Get images from the corresponding future
            
            # Extract trademark numbers
            trademarks_210_151 = re.findall(r'(\d+)\s*\(151\)', text, re.DOTALL)
            trademarks_732 = re.findall(r'\(732\)\s*(?:[^:]*:\s*)?(.*?)(?=\(210\)|$)', text, re.DOTALL)
            trademarks_with_caps = []
            trademarks_without_caps = []
            
            # Process each trademark
            for trademark_210_151, trademark_732 in zip(trademarks_210_151, trademarks_732):
                # Check if the last word of the trademark is in capital letters
                last_word_caps = re.findall(r'([A-Z]+|\d+)$', trademark_732.strip())
                words_after_none = re.findall(r'None\s*(\w+)', trademark_732.strip())

                # Determine if the trademark has capitalized last words
                if last_word_caps or (words_after_none and len(words_after_none) > 0):
                    trademarks_with_caps.append(trademark_210_151)
                else:
                    trademarks_without_caps.append(trademark_210_151)

            image_index = 0
            # Assign images to trademarks without capitalized last words
            for trademark_number in trademarks_without_caps:
                if image_index < len(images):
                    try:
                        pix = fitz.Pixmap(doc, images[image_index][0])
                        pil_image = PILImage.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        pil_image = pil_image.resize((50, 50))  # Resize the image to 50x50
                        img_bytes = BytesIO()
                        pil_image.save(img_bytes, format="PNG")
                        img_bytes = img_bytes.getvalue()
                        
                        # Append the trademark number and image to the data list
                        trademark_data.append({'TrademarkNo': trademark_number, 'ImageData': img_bytes})
                        
                        image_index += 1
                    except Exception as e:
                        print(f"Error processing image: {e}")
                        trademark_data_madrid.append({'TrademarkNo': trademark_number, 'ImageData': None})
                else:
                    trademark_data_madrid.append({'TrademarkNo': trademark_number, 'ImageData': None})            

    # Create a new Excel workbook
    workbook = Workbook()
    worksheet = workbook.active

    # Write trademark data to the worksheet
    for row, data in enumerate(trademark_data, start=1):
        worksheet.append([data['TrademarkNo']])
        if data['ImageData']:
            img = PILImage.open(BytesIO(data['ImageData']))
            img.thumbnail((50, 50))  # Resize the image to fit in the cell
            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG')
            excel_img = ExcelImage(img_bytes)
            worksheet.add_image(excel_img, f'B{row}')

    # Save the workbook
    output_excel_path = f'output/trademarks_and_logos.xlsx'
    workbook.save(output_excel_path)

    print(f"Excel file created successfully.")

# Example usage
extract_trademarks_and_logos(r'text\2011\ip_journal_march_2011.pdf')
