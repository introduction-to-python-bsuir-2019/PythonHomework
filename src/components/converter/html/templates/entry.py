from jinja2 import Template

entry = Template('''
    <div style="">
        <h2>{{title}}</h2>
        <div style="">
            <div style="">
            # {% for img in images %}
            #     {{img}}
            # {% endfor %}
            </div>
            <div style="">
                <h4>{{date}}</h4>
                <p>
                    {{description}}
                </p>
                <b>Links</b>
                {% for link in links %}
                    <a href="{{link}}">{{link}}</a>
                {% endfor %}
                <br>
                <b>Source: </b><a href="{{link}}">{{link}}</a>
            </div>
        </div>
    </div>
''')
