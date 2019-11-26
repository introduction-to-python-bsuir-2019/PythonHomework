"""
This module provides HTML templates for converting news to HTML format
"""

from jinja2 import Template

news = Template('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title style="align-self: center;">{{title}}</title>
</head>
<body style="display: flex; flex-direction: column; background-color: rgb(193, 229, 253);">
<h1 style="margin: 20px;">
    {{title}}
</h1>
{% for item in news %}
    {{item}}
{% endfor %}
</body>
</html>
''')

news_item = Template('''
<div style="display: flex; flex-direction: column; margin: 10px; padding: 10px; background-color: white;">
    <h2>{{title}}</h2>
    <div style="display: flex; flex-direction: column;">
        <div style="display: flex;">
        {% for img in images %}
            {{img}}
        {% endfor %}
        </div>
        <div style="word-wrap: break-word;">
            <h4>{{date}}</h4>
            <p>
                {{text}}
            </p>
            <b>Links</b><br><br>
            {% for link in links %}
                <a>{{link}}</a><br>
            {% endfor %}
            <br>
            <b>Source: </b><a>{{link}}</a>
        </div>
    </div>
</div>
''')

img = Template('<img src="{{src}}" alt="{{alt}}" height="300">')
