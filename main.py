import sys
import PyPDF2

# Get the file name from the command line
if len(sys.argv) < 2:
    print('Usage: python main.py <file_name>')
    sys.exit(1)
else:
    file_name = sys.argv[1]

pdf_name = file_name.split("/")[-1].split(".")[0]
pdf_path = "/".join(file_name.split("/")[:-1])

# Open the PDF file in a with indentation
with open(file_name, 'rb') as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    # Get the number of pages
    num_pages = len(pdf_reader.pages)
    
    # Get the page object
    page_obj = pdf_reader.pages[21]
    
    # Get the text from the page object
    text = page_obj.extract_text()
    
    to_save = []
    already_done = set()
    
    for i in range(num_pages-1, -1, -1):
        page_obj = pdf_reader.pages[i]
        
        text = page_obj.extract_text()
        
        page_xOvery = text.split("|")[-1].strip()
        
        if "/" in page_xOvery:
            
            page_xOvery = int(page_xOvery.split("/")[0].strip())
            if page_xOvery not in already_done:
                to_save.append(page_obj)
                already_done.add(page_xOvery)
        
        else:
            
            to_save.append(page_obj)
            
    to_save = to_save[::-1]
    
    #save to_save as a pdf
    pdf_writer = PyPDF2.PdfWriter()
    for page in to_save:
        pdf_writer.add_page(page)
    with open(f'{pdf_path}/{pdf_name}(condensed).pdf', 'wb') as out:
        pdf_writer.write(out)
