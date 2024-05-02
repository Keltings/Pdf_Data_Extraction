import PyPDF2
import re
import pandas as pd
from extraction.pattern import extract_info
from extraction.madrid import extract_madrid

def extract_data(file_path,text_after_kenya):
    data = {
        "Trademark Number (210)": [],
        "Application Filing Date (220)": [],
        "Class of registration (511)": [],
        "Proprietor/Owner (730)": [],
        "Representative/Applicant (740)": [],
        "Image/Mark": []
    }

    madrid_data = {
        "Trademark Number (210)": [],
        "Application Filing Date (151)": [],
        "Class of registration (511)": [],
        "Representative/Applicant (732)": [],
        "Image/Mark": []
    }

    try:
        # Open the PDF file
        with open(file_path, 'rb') as file:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)

            block = ''  # Initialize block
            madrid_block = ''
            # Iterate over pages
            for page_idx in range(num_pages):
                # Extract text content from page
                page = pdf_reader.pages[page_idx]
                page_content = page.extract_text()

                # Split page content into lines
                lines = [line.strip() for line in page_content.split('\n')]

                # Function to check if a line is a header
                def is_header(line):
                    header_patterns = [
                        r'Industrial Property Journal',  
                        r'\(19\) KE - Industrial Property Journal - No\. \d{4}/\d{2} \d{2}/\d{2}/\d{4}', 
                        r'\(19\) KE - Industrial\s*Pr\s*operty Journal - No\.\s*\d{4}/\d{2}\s+\d{2}/\d{2}\s+/\s*\d{4}',  
                        r'\(\d+\) KE - Industrial Property Journal - No\. \d+/\d+ \d+/\d+/\d+',  
                    ]
                    return any(re.search(pattern, line) for pattern in header_patterns)

                # Filter out lines that are headers, consist of only digits, contain "Page",
                # or consist of only underscores
                lines = [re.sub(r'_+', '', line) for line in lines if not is_header(line) 
                        and not line.isdigit() 
                        and "Page" not in line 
                        and not all(c == '_' for c in line.strip())]

                # Iterate over filtered lines
                for line in lines:
                    if '210' in line or '2 10' in line or '21 0' in line:
                        # If a new block starts, extract info from the previous block
                        if block:
                            info = extract_info(block,text_after_kenya)
                            if info:
                                for i, key in enumerate(data.keys()):
                                    data[key].append(info[i])
                        # Start a new block
                        block = line

                        if madrid_block:
                            info = extract_madrid(madrid_block)
                            if info:
                                for i,key in enumerate(madrid_data.keys()):
                                    madrid_data[key].append(info[i])
                        madrid_block = line

                    else:
                        # Append line to the current block
                        block += ' ' + line
                        madrid_block += ' ' + line

            # Extract info from the last block on the last page
            if block:
                info = extract_info(block,text_after_kenya)
                if info:
                    for i, key in enumerate(data.keys()):
                        data[key].append(info[i])
            
            if madrid_block:
                info = extract_madrid(madrid_block)
                if info:
                    for i,key in enumerate(madrid_data.keys()):
                        madrid_data[key].append(info[i])

    except Exception as e:
        print(f"Error occurred: {e}")

    if not data:
        print("No data found within the specified page range.")

    if not madrid_data:
        print("No Madrid System data found within the specified page range.")

    # Function to remove commas from the Image/Mark column
    def remove_commas_and_fullstops(text):
        return text.replace(',', '').replace('.', '')
    
    data["Image/Mark"] = [remove_commas_and_fullstops(text) for text in data["Image/Mark"]]

    df_image = pd.DataFrame(data)
    df_image.replace('', pd.NA, inplace=True)

    df_madrid = pd.DataFrame(madrid_data)
    df_madrid.replace('', pd.NA, inplace=True)

    # Drop rows with missing data
    df_madrid.dropna(subset=['Trademark Number (210)', 'Application Filing Date (151)', 'Representative/Applicant (732)'], inplace=True)


    return df_image, df_madrid
