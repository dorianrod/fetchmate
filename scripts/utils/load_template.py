from flask import render_template_string


def load_template(file):
    if not file.endswith(".tmpl"):
        raise ValueError("Invalid template file extension")

    with open(file, 'r') as tmpl_file:
        return tmpl_file.read()


def render_template(file, context):
    template_str = load_template(file)
    return render_template_string(template_str, **context)
