from libraries.library_app import app


def before_all(context):
    context.library = app
