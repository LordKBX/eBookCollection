import os
import sys
import re
import tempfile
import traceback
from xml.sax import handler, make_parser, SAXException, SAXParseException
import xml.dom.minidom


class TagHandler(handler.ContentHandler):
    def __init__(self):
        handler.ContentHandler.__init__(self)
        self.stack = []

    def startElement(self, name, attrs):
        self.stack.append(name)

    def endElement(self, name):
        # TODO: might want to just confirm that the element matches the top of the stack here
        self.stack.pop()

    def finish_document(self):
        return "\n".join(["</%s>" % tag for tag in reversed(self.stack)])


def parse(text: str):
    parser = make_parser()
    handler = TagHandler()
    parser.setContentHandler(handler)

    try:
        filePath = tempfile.gettempdir() + os.sep + 'xmlparse'
        with open(filePath, 'w', encoding="utf8") as file:
            file.write(text)
        parser.parse(filePath)
        return None
    except SAXParseException as error:
        print(error.getMessage())
        print(error.getException())
        print('{}:{}'.format(error.getLineNumber(), error.getColumnNumber()))
        return [error.getLineNumber(), error.getColumnNumber()]
    except:
        traceback.print_exc()
        return None


def prettify(text: str):
    text = text.replace('\t', '').replace('\r', '')
    text = re.sub('\n {2,}', '\n', text)
    text = text.replace('\n', '')
    text = re.sub(' {2,}', ' ', text)
    xmlt = xml.dom.minidom.parseString(text)
    uglyXml = xmlt.toprettyxml(indent="  ", newl="\n")
    text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)
    return text_re.sub('>\g<1></', uglyXml).replace('\r', '').replace('\n\n', '\n')


def prettifyCss(text: str):
    css = text
    newcss = ''

    # remove comments - this will break a lot of hacks :-P
    css = re.sub(r'\s*/\*\s*\*/', "$$HACK1$$", css)  # preserve IE<6 comment hack
    css = re.sub(r'/\*[\s\S]*?\*/', "", css)
    css = css.replace("$$HACK1$$", '/**/')  # preserve IE<6 comment hack

    # url() doesn't need quotes
    css = re.sub(r'url\((["\'])([^)]*)\1\)', r'url(\2)', css)

    # spaces may be safely collapsed as generated content will collapse them anyway
    css = re.sub(r'\s+', ' ', css)

    # shorten collapsable colors: #aabbcc to #abc
    css = re.sub(r'#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3(\s|;)', r'#\1\2\3\4', css)

    # fragment values can loose zeros
    css = re.sub(r':\s*0(\.\d+([cm]m|e[mx]|in|p[ctx]))\s*;', r':\1;', css)

    for rule in re.findall(r'([^{]+){([^}]*)}', css):

        # we don't need spaces around operators
        selectors = [re.sub(r'(?<=[\[\(>+=])\s+|\s+(?=[=~^$*|>+\]\)])', r'', selector.strip()) for selector in
                     rule[0].split(',')]

        # order is important, but we still want to discard repetitions
        properties = {}
        porder = []
        for prop in re.findall('(.*?):(.*?)(;|$)', rule[1]):
            key = prop[0].strip().lower()
            if key not in porder: porder.append(key)
            properties[key] = prop[1].strip()

        # output rule if it contains any declarations
        if properties:
            if newcss != '':
                newcss += '\n\n'
            newcss += "{}{}".format(','.join(selectors), '{'+''.join(["\n\t{}:{};".format(key, properties[key]) for key in porder])[:-1])+'\n}'
    return newcss
