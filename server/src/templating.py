from os.path import dirname, join


templates_dir = join(dirname(dirname(__file__)), "templates")


def get_template_path(template_name):
    return join(templates_dir, template_name)
