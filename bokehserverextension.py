from subprocess import Popen


def load_jupyter_server_extension(nbapp):
    """serve the jupiter_notebook directory with bokeh server"""
    Popen(["bokeh", "serve", "jupiter_notebook", "--allow-websocket-origin=*"])
