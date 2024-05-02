from extraction.image import extract_trademarks_and_logos
from extraction.text import extract_data

def process_pdf(pdf_file,text_after_kenya):
    df_text, df_madrid_text = extract_data(pdf_file,text_after_kenya)
    df_image,df_madrid = extract_trademarks_and_logos(pdf_file)
    return df_text, df_madrid_text, df_image, df_madrid