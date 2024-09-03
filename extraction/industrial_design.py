import re

def extract_industrial_design(block):
    # Regular expressions to extract information from the block
    application_number_match = re.search(r'(\d+)\s*\(22\)', block)
    filing_date_match = re.search(r'\(22\)[^:]*:?\s*(\d{1,2}/\d{1,2}/\d{2,4})', block)
    class_registration_match = re.search(r'\(51\)\s*\D*(\d.*?)\s*(?=\(\d{2}\)|$)', block, re.DOTALL)            
    # creator_match = re.search(r'\(72\)\s*(?:[^:]*:\s*)?(.*?)(?=\(\d{2}\)|$)', block, re.DOTALL) 
    creator_match = re.search(r'\(72\)\s*(?:Creator\(s\):\s*)?(.*?)(?=\(\d{2}\)|$)', block, re.DOTALL)

    # applicant_match = re.search(r'\(73\)\s*(?:[^:]*:\s*)?(.*?)(?=\(\d{2}\)|$)', block, re.DOTALL) 
    applicant_match = re.search(r'\(73\)\s*(?:Applicant\(s\):\s*)?(.*?)(?=\(\d{2}\)|$)', block, re.DOTALL)

    title_match = re.search(r'\(54\)\s*(?:[^:]*:\s*)?(.*?)(?=\(\d{2}\)|$)', block, re.DOTALL)                          
    
    application_number_ = application_number_match.group(1) if application_number_match else ''
    filing_date = filing_date_match.group(1) if filing_date_match else ''
    class_registration = class_registration_match.group(1).strip() if class_registration_match else ''
    creator = creator_match.group(1).strip() if creator_match else ''
    applicant = applicant_match.group(1).strip() if applicant_match else ''
    title = title_match.group(1).strip() if title_match else ''

    # Extracting data for Image/Mark column
    image_mark = ''
       
    return application_number_, filing_date, class_registration, creator, applicant, title, image_mark