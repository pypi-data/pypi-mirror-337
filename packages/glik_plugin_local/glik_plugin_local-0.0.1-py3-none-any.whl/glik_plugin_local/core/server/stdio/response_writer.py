import sys

from glik_plugin_local.core.server.__base.response_writer import ResponseWriter


class StdioResponseWriter(ResponseWriter):
    def write(self, data: str):
        sys.stdout.write(data)
        sys.stdout.flush()

    def done(self):
        pass
