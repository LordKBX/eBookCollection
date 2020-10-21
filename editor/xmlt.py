import os
import re
import tempfile
import traceback
from xml.sax import handler, make_parser, SAXParseException
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
