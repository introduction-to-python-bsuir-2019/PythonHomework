from fpdf import FPDF, HTMLMixin
 
class HTML2PDF(FPDF, HTMLMixin):
    pass
 
def html2pdf():
    html = ''
    with open('rss_reader_news.html', 'r', encoding='UTF-8') as f:
        html = f.read()
    pdf = HTML2PDF()
    pdf.add_page()
    pdf.write_html(html)
    pdf.output('html2pdf.pdf')
 
html2pdf()