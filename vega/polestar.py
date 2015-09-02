import os
import json
import cgi
import codecs

from IPython import display


JS = ['static/polestar/scripts/vendor-6292494709.js',
      'static/polestar/scripts/app-ddc64cf3e9.js']
CSS = ['static/polestar/scripts/vendor-5779b264ab.css',
       'static/polestar/styles/app-767140e98a.css']
TEAMPLATE = 'static/index.html'

IFRAME_STYLE = 'border: none; width: 100%; min-height: 580px;'


def publish(dataframe):
    """Create and immediately display even if it is not the last line."""
    display.display(create(dataframe))


def create(dataframe):
    """Creates polestar from a dataframe"""
    return Polestar(dataframe.columns, dataframe.values)


class Polestar():
    """Defines Polestar widget"""

    def __init__(self, columns, data):
        """Constructor

        Args:
            columns: a list of column names

            data: list of rows"""

        self.data = data
        self.columns = columns

    def __get_content(self, path):
        abs_path = os.path.abspath(path)
        with codecs.open(abs_path, encoding='utf-8') as f:
            return f.read()

    def __styles(self, paths):
        out = []
        for path in paths:
            out.append(
                u'<style>/*# sourceURL={path} */\n{body}</style>'.format(
                    path=path, body=self.__get_content(path)))
        return u'\n'.join(out)

    def __scripts(self, paths):
        out = []
        for path in paths:
            out.append((u'<script type="text/javascript">//@ sourceURL={path}'
                       '\n{body}</script>').format(
                       path=path, body=self.__get_content(path)))
        return u'\n'.join(out)

    def __data(self):
        res = []
        for row in self.data.tolist():
            res.append({k: v for k, v in zip(self.columns, row)})
        return res

    def __escape(self, body):
        return cgi.escape(body, quote=True)

    def _repr_html_(self):
        """Used by the frontend to show html for polestar."""
        template = self.__get_content(TEAMPLATE)
        body = template.format(
            styles=self.__styles(CSS),
            scripts=self.__scripts(JS),
            spec={},
            data=json.dumps(self.__data()))
        output = u'<iframe srcdoc="{srcdoc}" style="{style}"></iframe>'.format(
            srcdoc=self.__escape(body), style=IFRAME_STYLE)
        return output