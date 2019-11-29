"""
this module provides tools for converting news to html and pdf formats
"""

import os
import shutil
import requests
from fpdf import FPDF

def break_lines(text):
    """
    this function replaces '\n' to <br> tags
    """
    i = 0
    while True:
        try:
            while text[i] != '\n':
                i += 1
            text = text[:i] + "<br>" + text[i + 1:]
            i += 4
        except IndexError:
            break

    return text

def to_html(news, filepath):
    """
    this function prints news in html format to file
    """
    with open(filepath, "w", encoding='utf-8') as f:
        f.write('''
<html lang="en" dir="ltr">
  <head>
    <title>rss_reader</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    	<style>
    		ul>li{
    			list-style: none;
    			border: 1px solid;
    			margin-top: 20px;
    			padding: 10px;
    		}
    		ul>li>p:nth-child(1){
    			font-size: 35px;
    		}

    		ul>li{
    			border-radius: 10px;
    			box-shadow: 1px 1px 10px black;
    		}
    	</style>
  </head>
  <body>
    <div class="container">
    <h1 style="text-align: center">Actual News</h1>
    <ul>''')
        for post in news:
            f.write(f'''
      <li>
        <p>Feed: {post['feed']}</p>
        <p>Title: {post['title']}</p>
        <p>Publication date: {post['pub_date']}</p>
        <p>Link: <a href = "{post['link']}">{post['link']}</a></p>
        <p>{break_lines(post['description'])}</p>
        <p>Links:</p>
        <ol>''')
            for tpl in post['hrefs']:
                if not tpl[1] == 'image':
                    f.write(f'''
          <li>
            <p><a href = "{tpl[0]}">{tpl[0]}</a></p>
          </li>''')
                else:
                    f.write(f'''
          <li>
            <p>{tpl[2]}<br><a href = "{tpl[0]}"><img src = "{tpl[0]}"></a></p>
          </li>''')
            f.write('''
        </ol>
      </li>''')
        f.write('''
    </ul>
    </div>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
  </body>
</html>''')

class user_FPDF(FPDF):
    """
    a small inherited class providing an ability to enumerate pages
    """
    def footer(self):
        self.set_y(-15)
        self.cell(0, 10, txt=f"{self.page_no()}", align='R')

def download_image(url, dest_filepath):
    """
    this function downloads an image from url and saves it in file
    """
    with open(dest_filepath, 'wb') as f:
        response = requests.get(url, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            f.write(block)

def to_pdf(news, filepath):
    """
    this function prints news in pdf format to file
    """
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, "tmp_files")
    if not os.path.exists(final_directory):
        os.mkdir(final_directory)

    pdf_obj= user_FPDF()
    font_dir = os.path.join(final_directory, 'DejaVuSansCondensed.ttf')
    with open(font_dir, "wb") as f:
        f.write(requests.get("https://raw.github.com/prague15031939/font_storage/master/DejaVuSansCondensed.ttf").content)
    pdf_obj.add_font('DejaVu', '', font_dir, uni=True)
    image_id = 0

    for ind, post in enumerate(news):
        pdf_obj.add_page()
        if ind == 0:
            pdf_obj.set_font('Arial', style='B', size=16)
            pdf_obj.cell(200, 15, txt='ACTUAL NEWS', align='C', ln=1)
        pdf_obj.set_font('DejaVu', '', 12)
        pdf_obj.cell(5, 5, txt="#")
        pdf_obj.cell(180, 5, txt=f"Feed: {(post['feed'])}", ln=1)
        pdf_obj.cell(200, 5, ln=1)
        pdf_obj.cell(5, 5)
        pdf_obj.multi_cell(180, 5, txt=f"Title: {(post['title'])}")
        pdf_obj.cell(5, 5)
        pdf_obj.cell(200, 5, txt=f"Publication date: {post['pub_date']}", ln=1)
        pdf_obj.cell(5, 5)
        pdf_obj.cell(10, 5, txt='Link: ')
        pdf_obj.set_font('Arial', style='I', size=12)
        pdf_obj.multi_cell(180, 5, txt=f"{post['link']}")
        pdf_obj.set_font('DejaVu', '', 12)
        pdf_obj.cell(200, 5, ln=1)
        pdf_obj.cell(5, 5)
        pdf_obj.multi_cell(200, 5, txt=f"{post['description']}")
        pdf_obj.cell(200, 5, ln=1)
        pdf_obj.cell(5, 5)
        pdf_obj.cell(200, 5, txt=f"Links:", ln=1)

        for index, tpl in enumerate(post['hrefs']):
            pdf_obj.cell(10, 5)
            if not tpl[1] == 'image':
                pdf_obj.set_font('DejaVu', '', 12)
                pdf_obj.cell(7, 5, txt=f"[{index + 1}] ")
                pdf_obj.set_font('Arial', style='I', size=12)
                pdf_obj.multi_cell(170, 5, txt=f"{tpl[0]}")
            else:
                pdf_obj.set_font('DejaVu', '', 12)
                pdf_obj.multi_cell(170, 5, txt=f"[{index + 1}] {tpl[2]}")
                try:
                    img_dir = os.path.join(final_directory, f"{image_id}.jpeg")
                    download_image(tpl[0], img_dir)
                    pdf_obj.image(img_dir, x=22, y=pdf_obj.get_y()+5, link=tpl[0])
                    image_id += 1
                except RuntimeError:
                    pass

    pdf_obj.output(filepath)
    shutil.rmtree(final_directory)
