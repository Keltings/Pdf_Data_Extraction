import re

def extract_info(block,text_after_kenya):
    # Regular expressions to extract information from the block
    trademark_number_match = re.search(r'(\d+)\s*\(220\)', block)
    filing_date_match = re.search(r'\(220\)[^:]*:?\s*(\d{1,2}/\d{1,2}/\d{2,4})', block)
    class_registration_match = re.search(r'\(511\)\s*\D*(\d.*?)\s*(?=\(\d{3}\)|$)', block, re.DOTALL)              
    proprietor_match = re.search(r'\(730\)\s*(?:[^:]*:\s*)?(.*?)(?=\(\d{3}\)|$)', block, re.DOTALL)                          
    representative_match = re.search(r'\(740\)\s*(?:[^:]*:\s*)?(.*?)(?=\(\d{3}\)|$)', block, re.DOTALL)

    trademark_number = trademark_number_match.group(1) if trademark_number_match else ''
    filing_date = filing_date_match.group(1) if filing_date_match else ''
    class_registration = class_registration_match.group(1).strip() if class_registration_match else ''
    proprietor = proprietor_match.group(1).strip() if proprietor_match else ''
    representative = representative_match.group(1).strip() if representative_match else ''

    # Extracting data for Image/Mark column
    image_mark = ''

    # Function to split text after "Kenya" and move capitalized words to Image/Mark column
    def move_words_after_kenya(text,text_after_kenya):
        # Find all occurrences of "Kenya" in the text
        kenya_matches = list(re.finditer(r'K\s*e\s*n\s*y\s*a', text, re.IGNORECASE))
        if kenya_matches:
            kenya_match = kenya_matches[-1] # Select the last occurrence of "Kenya"
            kenya_index = kenya_match.end()
            kenya_part = text[:kenya_index].strip()  # Include "Kenya" and preceding text
            words_after_kenya = text[kenya_index:].strip()

            if text_after_kenya:
                if words_after_kenya:
                    image_mark = words_after_kenya
                    return kenya_part, image_mark
            else:
                if words_after_kenya.isupper():
                    image_mark = words_after_kenya
                    return kenya_part, image_mark

        return text, ""


    if representative:
        # Apply the move_words_after_kenya function to the Representative/Applicant (740) column
        representative, image_mark = move_words_after_kenya(representative,text_after_kenya)


        # Move words after "None" to the Image/Mark column
        if "None" in representative:
            words_after_none = representative.split("None", 1)[-1].strip()
            if words_after_none:
                image_mark = words_after_none
                representative = representative.replace(words_after_none, "").strip()
        else:
            # Check from the end if the words are all uppercase (excluding "NAIROBI")
            words = representative.split()
            all_caps_words = []
            nairobi_found = False
            for word in reversed(words):
                if word.upper() == "NAIROBI":
                    nairobi_found = True
                    continue
                if word.isupper():
                    all_caps_words.insert(0, word)
                else:
                    break
            if all_caps_words:
                # If there are uppercase words (excluding "NAIROBI"), move them to the Image/Mark column
                image_mark = ' '.join(all_caps_words)
                # Remove the all-uppercase words from the Representative column
                representative = ' '.join(words[:-len(all_caps_words)])
            elif nairobi_found:
                # If "NAIROBI" is found but there are no other all-caps words, leave the representative column unchanged
                pass
            
    # If representative is empty but proprietor is not
    if not representative and proprietor:
         # Move last words that are all caps in proprietor to image/mark
        all_caps_words = []
        # Check each word in reverse order
        words = proprietor.split() 
        for word in reversed(words):
            if word.isupper():
                all_caps_words.insert(0, word)
            else:
                break  # Exit loop if a word is encountered that is not all caps
        if all_caps_words:
            image_mark = ' '.join(all_caps_words)
            proprietor = ' '.join(words[:-len(all_caps_words)])

    return trademark_number, filing_date, class_registration, proprietor, representative, image_mark
