from io import BytesIO
import fitz  # PyMuPDF
from PIL import Image as PILImage
import re
import pandas as pd
import concurrent.futures

def extract_images(page):
    images = page.get_images(full=True)
    return sorted(images, key=lambda img: img[0])

def extract_logos(pdf_file):
    # Open the PDF document
    doc = fitz.open(pdf_file)
    trademark_data = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Extract trademarks and images in parallel
        futures = [executor.submit(extract_images, page) for page in doc]
        
        # Iterate through each page of the PDF
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            images = futures[page_num - 1].result()  # Get images from the corresponding future
            
            # Extract trademark numbers
            trademarks_210_220 = re.findall(r'(\d+)\s*\(220\)', text, re.DOTALL)
            trademarks_740 = re.findall(r'\(730\)\s*(?:[^:]*:\s*)?(.*?)(?=\(210\)|$)', text, re.DOTALL)
            trademarks_with_caps = []
            trademarks_without_caps = []
            
            # Process each trademark
            for trademark_210_220, trademark_740 in zip(trademarks_210_220, trademarks_740):
                # Check if the last word of the trademark is in capital letters
                last_word_caps = re.findall(r'([A-Z]+|\d+)$', trademark_740.strip())
                words_after_none = re.findall(r'None\s*(\w+)', trademark_740.strip())

                # Determine if the trademark has capitalized last words
                if last_word_caps or (words_after_none and len(words_after_none) > 0):
                    trademarks_with_caps.append(trademark_210_220)
                else:
                    trademarks_without_caps.append(trademark_210_220)

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
                        trademark_data.append({'TrademarkNo': trademark_number, 'ImageData': img_bytes})
                        image_index += 1
                    except Exception as e:
                        print(f"Error processing image: {e}")
                        trademark_data.append({'TrademarkNo': trademark_number, 'ImageData': None})
                else:
                    trademark_data.append({'TrademarkNo': trademark_number, 'ImageData': None})

    # Create a DataFrame from the extracted trademark data
    df_image = pd.DataFrame(trademark_data)
    return df_image

def extract_madrid_logos(pdf_file):
    # Open the PDF document
    doc = fitz.open(pdf_file)
    trademark_data = []

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
            for trademark_210_151, trademark_740 in zip(trademarks_210_151, trademarks_732):
                # Check if the last word of the trademark is in capital letters
                last_word_caps = re.findall(r'([A-Z]+|\d+)$', trademark_740.strip())
                words_after_none = re.findall(r'None\s*(\w+)', trademark_740.strip())

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
                        trademark_data.append({'TrademarkNo': trademark_number, 'ImageData': img_bytes})
                        image_index += 1
                    except Exception as e:
                        print(f"Error processing image: {e}")
                        trademark_data.append({'TrademarkNo': trademark_number, 'ImageData': None})
                else:
                    trademark_data.append({'TrademarkNo': trademark_number, 'ImageData': None})

    # Create a DataFrame from the extracted trademark data
    df_madrid = pd.DataFrame(trademark_data)
    return df_madrid

def extract_trademarks_and_logos(pdf_file):
    # Call the two functions to get dataframes
    df_image = extract_logos(pdf_file)
    df_madrid = extract_madrid_logos(pdf_file)
    
    # Return the two dataframes
    return df_image, df_madrid

# Example usage
#df_image, df_madrid = extract_trademarks_and_logos(r'C:\Users\KELIDA\Desktop\ILab24\-copy\extraction\ip_journal_march_2011.pdf')
