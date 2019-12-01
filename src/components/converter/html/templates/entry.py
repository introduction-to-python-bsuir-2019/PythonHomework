from jinja2 import Template

entry = Template('''
    <div style="">
        <h2>{{title}}</h2>
        <div style="">
            <div style="">
            {% for item in media %}
                {{item}}
            {% endfor %}
            </div>
            <div style="">
                <h4>{{date}}</h4>
                <p>
                    {{description}}
                </p>
                <b>Links</b>
                {% for link in links %}
                    <a href="{{link['href']}}" type="{{link['type']}}">{{link['href']}}</a><br>
                {% endfor %}
                <br>
                <b>Source: </b><a href="{{link}}">{{link}}</a>
            </div>
        </div>
    </div>
''')
