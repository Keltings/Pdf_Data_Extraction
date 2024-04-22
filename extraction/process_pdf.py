from extraction.image import extract_trademarks_and_logos
from extraction.text import extract_data

def process_pdf(pdf_file,text_after_kenya):
    df_text = extract_data(pdf_file,text_after_kenya)
    df_image = extract_trademarks_and_logos(pdf_file)
    return df_text, df_image