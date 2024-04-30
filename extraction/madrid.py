import re

def extract_madrid(block):
    # Regular expressions to extract information from the block
    trademark_number_match = re.search(r'(\d+)\s*\(151\)', block)
    filing_date_match = re.search(r'\(151\)[^:]*:?\s*(\d{1,2}/\d{1,2}/\d{2,4})', block)
    class_registration_match = re.search(r'\(511\)\s*\D*(\d.*?)\s*(?=\(\d{3}\)|$)', block, re.DOTALL)            
    representative_match = re.search(r'\(732\)\s*(?:[^:]*:\s*)?(.*?)(?=\(\d{3}\)|$)', block, re.DOTALL)                          

    trademark_number = trademark_number_match.group(1) if trademark_number_match else ''
    filing_date = filing_date_match.group(1) if filing_date_match else ''
    class_registration = class_registration_match.group(1).strip() if class_registration_match else ''
    representative = representative_match.group(1).strip() if representative_match else ''

    # Extracting data for Image/Mark column
    image_mark = ''

    if representative:
        words = representative.split()
        all_caps_words = []
        for word in reversed(words):
            if word.isupper():
                all_caps_words.insert(0, word)
            else:
                break
        if all_caps_words:
            # If there are uppercase words , move them to the Image/Mark column
            image_mark = ' '.join(all_caps_words)
            # Remove the all-uppercase words from the Representative column
            representative = ' '.join(words[:-len(all_caps_words)])
        
    return trademark_number, filing_date, class_registration, representative, image_mark