from jinja2 import Template

layout = Template('''
    <html>
      <head>
        <meta charset="{{encoding}}">
        <title>{{title}}</title>
      </head>
      <body>
        <h1 style="text-align:center;margin-top:2rem">{{title}}</h1>
        <h2 style="text-align:center;margin-top:2rem">
            <a href="{{url}}">{{url}}</a>
        </h2>
        <div id="feeds">
        {% for entry in feeds_entries %}
            {{entry}}
        {% endfor %}
        </div>
      </body>
    </html>
''')
