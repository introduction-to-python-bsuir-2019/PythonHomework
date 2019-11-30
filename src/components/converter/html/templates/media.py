from jinja2 import Template

media = Template('''
    <div class="media">
        <img src="{{src}}" alt="{{alt}}">
    </div
''')
