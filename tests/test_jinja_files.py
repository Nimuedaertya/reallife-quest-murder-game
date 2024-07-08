from jinja2 import Environment, FileSystemLoader


def test_load_jinja_files():
    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template('index.html')
    output_from_parsed_template = template.render(foo='Hello World!')
    print(output_from_parsed_template)
