import sys, os, io, traceback, shutil, datetime, re, uuid
from xml.dom import minidom
from PIL import Image, ImageDraw, ImageFont
import base64
import zipfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import bdd
from common.common import *
from common.files import *
from common.archive import *
from vars import *
import lang

cover_width = 1200
cover_height = 1600


def create_thumbnail(path: str, resize: bool = True):
    img = Image.open(path)
    img.load()
    if resize is True:
        max_h = max_w = 600
        size = list(img.size)
        if size[0] > size[1]:
            size[1] = int(size[1] * max_h / size[0])
            size[0] = max_w
        elif size[0] < size[1]:
            size[0] = int(size[0] * max_w / size[1])
            size[1] = max_h
        else:
            size[0] = max_w
            size[1] = max_h
        img = img.resize(tuple(size), Image.ANTIALIAS)
    buffer = io.BytesIO()
    img.save(buffer, 'jpeg')
    return 'data:image/jpeg;base64,'+base64.b64encode(buffer.getvalue()).decode()


def create_cover(title: str, authors: str = None, series: str = None, volume_number: float = None,
                 file_name: str = app_directory+os.sep+'tmp'+os.sep+'cover.png', style=None):
    if style is None:
        style = {
            "background": "white",
            "pattern": "01",
            "Title": "black",
            "Series": "blue",
            "Authors": "black",
        }

    img = Image.new('RGB', (cover_width, cover_height), color=style['background'])

    top = __draw_text_on_image(img, title, 100, 100, "bold", style['Title'])

    if series is not None:
        if volume_number is None:
            volume_number = 1
        tx = series
        if volume_number != 0:
            if volume_number - volume_number.__int__() != 0:
                tx += " ({})".format(volume_number)
            else:
                tx += " ({})".format(volume_number.__int__())
        top = __draw_text_on_image(img, tx, top + 170, 80, "italic", style['Series'])
        ""

    if authors is not None:
        top = __draw_text_on_image(img, authors, 1400, 80, "regular", style['Authors'])

    img.save(file_name)


def __draw_text_on_image(img: Image, text: str, top: int, font_size: int, font_style: str, color: str):
    line_width = (cover_width / (font_size * 0.55).__round__()).__round__()
    pas = (font_size * 1.10).__int__()
    font = 'Regular'
    font_style = font_style.lower()
    if font_style == "bold":
        font = 'Bold'
    elif font_style == "italic":
        font = 'Italic'
    elif font_style == "bold&italic":
        font = 'Bold-Italic'
    font = ImageFont.truetype(app_directory + os.sep + 'ressources' + os.sep + 'fonts'
                              + os.sep + 'Arial' + os.sep + font + '.ttf', font_size)

    textes = []
    size = len(text)
    while size > line_width:
        chunk = text[0:line_width]
        try:
            index = chunk.rindex(" ")
        except ValueError:
            index = line_width
        textes.append(text[0:index])
        text = text[index:]
        size = len(text)
    textes.append(text)

    for texte in textes:
        d = ImageDraw.Draw(img)
        w, h = d.textsize(texte, font=font)
        d.text(((cover_width-w)/2, top), texte, fill=color, font=font)
        top += pas

    return top


def create_epub(title: str, authors: str = None, series: str = None, volume_number: float = None,
                file_name_template: str = '%title% - %serie% - %authors%',
                style=None
                ):
    if style is None:
        style = {
            "background": "white",
            "pattern": "01",
            "Title": "black",
            "Series": "blue",
            "Authors": "black",
        }
    try:
        local_lang = lang.Lang()
        creation_time = datetime.datetime.now().__str__().replace(' ', 'T')
        id_point = creation_time.index('.')
        creation_time = creation_time[0:id_point] + "+00:00"
        creation_uuid = uuid.uuid4().__str__()

        create_cover(title, authors, series, volume_number, app_directory+os.sep+'tmp'+os.sep+'cover.png', style)
        os.makedirs(app_directory+os.sep+'tmp'+os.sep+'fonts')
        os.makedirs(app_directory+os.sep+'tmp'+os.sep+'META-INF')
        os.makedirs(app_directory+os.sep+'tmp'+os.sep+'texte')

        font_dir = app_directory+os.sep+'ressources'+os.sep+'fonts'+os.sep+'Arial'
        font_tmp_dir = app_directory+os.sep+'tmp'+os.sep+'fonts'
        copyFile(font_dir+os.sep+'Bold.ttf', font_tmp_dir+os.sep+'Arial-Bold.ttf')
        copyFile(font_dir+os.sep+'Bold-Italic.ttf', font_tmp_dir+os.sep+'Arial-Bold-Italic.ttf')
        copyFile(font_dir+os.sep+'Italic.ttf', font_tmp_dir+os.sep+'Arial-Italic.ttf')
        copyFile(font_dir+os.sep+'Regular.ttf', font_tmp_dir+os.sep+'Arial-Regular.ttf')

        with open(app_directory+os.sep+'tmp'+os.sep+'META-INF'+os.sep+'container.xml', 'w', encoding="utf8") as file:
            file.write('<?xml version="1.0"?>'
                       '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                       '<rootfiles><rootfile full-path="metadata.opf" media-type="application/oebps-package+xml"/>'
                       '</rootfiles></container>')

        with open(app_directory+os.sep+'tmp'+os.sep+'style.css', 'w', encoding="utf8") as file:
            file.write('@charset utf-8;@font-face{font-family:"Arial";src:url(fonts/Arial-Regular.ttf)}'
                       '@font-face{font-family:"Arial";src:url(fonts/Arial-Italic.ttf);font-style:italic}'
                       '@font-face{font-family:"Arial";src:url(fonts/Arial-Bold-Italic.ttf);font-weight:bold;font-style:italic}'
                       '@font-face{font-family:"Arial";src:url(fonts/Arial-Bold.ttf);font-weight:bold}*{font-family:"Arial",sans-serif}'
                       'h1{text-align:center}h2{text-align:center}h3{text-align:center}img{max-width:100%;height:auto;display:block;margin:0 auto}'
                       '.elypsys{text-align:center;font-weight:bold}.block{text-align:left;margin-top:1em;margin-bottom:1em}'
                       '.italic{font-family:"Arial",sans-serif;font-style:italic}'
                       '.bitalic{font-family:"Arial",sans-serif;font-style:italic;font-weight:bold}.credits{position:fixed;bottom:10px;left:10px}')

        with open(app_directory+os.sep+'tmp'+os.sep+'mimetype', 'w', encoding="utf8") as file:
            file.write('application/epub+zip')

        with open(app_directory+os.sep+'tmp'+os.sep+'metadata.opf', 'w', encoding="utf8") as file:
            content = '<?xml version="1.0" encoding="UTF-8"?><package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">' \
                      '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">' \
                      '<dc:title>{{TITLE}}</dc:title><dc:creator opf:role="aut" opf:file-as="{{AUTHORS_FOLDER_NAME}}">{{AUTHORS}}</dc:creator>' \
                      '<dc:identifier opf:scheme="uuid" id="uuid_id">{{UUID}}</dc:identifier><dc:date>{{CREATION_TIME}}</dc:date>' \
                      '<dc:language>{{LANG}}</dc:language><meta content="{{SERIES}}" name="dc:series"/>' \
                      '<meta content="{{SERIES_INDEX}}" name="dc:series_index"/><meta name="cover" content="cover"/></metadata>' \
                      '<manifest><item href="texte/cover.xhtml" id="page_00" media-type="application/xhtml+xml"/>' \
                      '<item href="texte/ch01.xhtml" id="page_01" media-type="application/xhtml+xml"/>' \
                      '<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>' \
                      '<item href="styles.css" id="style" media-type="text/css"/>' \
                      '<item href="cover.png" id="cover" media-type="image/png"/>' \
                      '<item href="fonts/Arial-Bold-Italic.ttf" id="font_bi" media-type="application/x-font-truetype"/>' \
                      '<item href="fonts/Arial-Bold.ttf" id="font_b" media-type="application/x-font-truetype"/>' \
                      '<item href="fonts/Arial-Italic.ttf" id="font_i" media-type="application/x-font-truetype"/>' \
                      '<item href="fonts/Arial-Regular.ttf" id="font_r" media-type="application/x-font-truetype"/>' \
                      '</manifest><spine toc="ncx"><itemref idref="page_00"/><itemref idref="page_01"/></spine><guide/></package>'
            content = content.replace('{{LANG}}', local_lang.language)
            content = content.replace('{{TITLE}}', title)
            content = content.replace('{{UUID}}', creation_uuid)
            if authors is None or authors.strip() == '':
                content = content.replace('{{AUTHORS}}', 'UNKWON')
                content = content.replace('{{AUTHORS_FOLDER_NAME}}', 'UNKWON')
            else:
                content = content.replace('{{AUTHORS}}', authors)
                tmp_authors = re.sub('(?![!A-Za-z]).*', '', authors).strip()
                if tmp_authors == '':
                    tmp_authors = authors
                content = content.replace('{{AUTHORS_FOLDER_NAME}}', tmp_authors if tmp_authors else '')
            if series is None or authors.strip() == '':
                content = content.replace('<meta content="{{SERIES}}" name="dc:series"/>'
                                          '<meta content="{{SERIES_INDEX}}" name="dc:series_index"/>', '')
            else:
                content = content.replace('{{SERIES}}', series)
                if volume_number is None:
                    content = content.replace('{{SERIES_INDEX}}', "1.0")
                else:
                    content = content.replace('{{SERIES_INDEX}}', "{}".format(volume_number))

            file.write(content)

        with open(app_directory+os.sep+'tmp'+os.sep+'toc.ncx', 'w', encoding="utf8") as file:
            content = '<?xml version=\'1.0\' encoding=\'utf-8\'?>'\
                       '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="{{LANG}}"><head>'\
                       '<meta content="{{UUID}}" name="dtb:uid"/><meta content="2" name="dtb:depth"/>'\
                       '<meta content="{{APP_NAME}}" name="dtb:generator"/>'\
                       '<meta content="0" name="dtb:totalPageCount"/><meta content="0" name="dtb:maxPageNumber"/></head>'\
                       '<docTitle><text>{{TITLE}}</text></docTitle>'\
                       '<navMap><navPoint id="num_01" playOrder="1"><navLabel><text>{{COVER_NAME}}</text></navLabel>'\
                       '<content src="texte/cover.xhtml"/></navPoint><navPoint id="num_02" playOrder="2">'\
                       '<navLabel><text>{{CHAPTER1_NAME}}</text></navLabel><content src="texte/ch01.xhtml"/></navPoint>'\
                       '</navMap></ncx>'
            content = content.replace('{{LANG}}', local_lang.language)
            content = content.replace('{{TITLE}}', title)
            content = content.replace('{{UUID}}', creation_uuid)
            content = content.replace('{{APP_NAME}}', app_name)
            content = content.replace('{{COVER_NAME}}', local_lang['Home']['emptyBookCreation']['Cover'])
            content = content.replace('{{CHAPTER1_NAME}}', local_lang['Home']['emptyBookCreation']['Chapter1'])
            file.write(content)

        with open(app_directory+os.sep+'tmp'+os.sep+'texte'+os.sep+'cover.xhtml', 'w', encoding="utf8") as file:
            content = '<?xml version=\'1.0\' encoding=\'utf-8\'?>' \
                      '<html xmlns="http://www.w3.org/1999/xhtml" lang="{{LANG}}" xml:lang="{{LANG}}">' \
                      '<head><title>{{TITLE}}</title><link href="../style.css" rel="stylesheet" type="text/css"/></head>' \
                      '<body><h1>{{TITLE}}</h1><h2 class="italic">{{SERIES}}</h2><div class="credits"><b>{{AUTHORS_LABEL}}</b>{{AUTHORS}}</div></body></html>'
            content = content.replace('{{LANG}}', local_lang.language)
            content = content.replace('{{TITLE}}', title)
            if series is not None:
                tx = series
                if volume_number > 0:
                    tx += " ({})".format(volume_number)
                content = content.replace('{{SERIES}}', tx)
            else:
                content = content.replace('{{SERIES}}', '')
            if authors is None or authors.strip() == '':
                content = content.replace('{{AUTHORS}}', 'UNKWON')
                content = content.replace('{{AUTHORS_LABEL}}', local_lang['Home']['emptyBookCreation']['Author'])
            else:
                content = content.replace('{{AUTHORS}}', authors)
                if "," in authors or ";" in authors:
                    content = content.replace('{{AUTHORS_LABEL}}', local_lang['Home']['emptyBookCreation']['Authors'])
                else:
                    content = content.replace('{{AUTHORS_LABEL}}', local_lang['Home']['emptyBookCreation']['Author'])
            file.write(content)

        with open(app_directory+os.sep+'tmp'+os.sep+'texte'+os.sep+'ch01.xhtml', 'w', encoding="utf8") as file:
            content = '<?xml version=\'1.0\' encoding=\'utf-8\'?>' \
                      '<html xmlns="http://www.w3.org/1999/xhtml" lang="{{LANG}}" xml:lang="{{LANG}}">' \
                      '<head><title>{{CHAPTER1_NAME}}</title>' \
                      '<link href="../style.css" rel="stylesheet" type="text/css"/></head>' \
                      '<body><h1>{{CHAPTER1_NAME}}</h1>' \
                      '<div class="block">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam ultricies tempus lectus eu vulputate. Vivamus pharetra sit amet elit non interdum. Etiam urna magna, porttitor at dolor a, pulvinar interdum diam. Nulla et nisl vitae sem viverra varius vitae sed eros. Quisque commodo tempus iaculis. Vivamus eget euismod sem, eget ultricies tortor. Aenean tincidunt feugiat arcu. Nam nec sapien a leo semper rutrum. Nulla vitae tellus varius, congue ipsum vel, ornare augue. Duis augue urna, mattis quis congue iaculis, blandit vitae ipsum. Sed euismod a nunc sed pulvinar. Nullam feugiat egestas fermentum.</div>' \
                      '<div class="block">Quisque malesuada diam et urna commodo egestas. Donec tincidunt erat eget auctor convallis. Donec maximus ut ex vel tempor. Mauris vehicula felis est. Cras eu nunc diam. Sed non nibh ante. Phasellus rhoncus a ex vitae malesuada. Sed ac egestas nunc, quis scelerisque sem. Mauris id arcu elit. Cras non lacus bibendum, finibus dui quis, vehicula augue.</div>' \
                      '<div class="block">In consectetur tellus vel malesuada porttitor. Proin commodo molestie nisi, eu placerat nunc hendrerit eget. Proin nec tortor sed diam facilisis varius. Donec sed libero neque. Vestibulum non nulla felis. Fusce tempor, lectus consectetur laoreet auctor, neque dui bibendum ex, sed finibus erat neque non ipsum. Mauris sodales nisl sed est posuere pulvinar sed ut orci. Donec a blandit lectus. Suspendisse porttitor ut justo eget placerat. Proin lobortis est venenatis, viverra orci ac, ornare odio. Pellentesque ut scelerisque felis.</div>' \
                      '<div class="block">Duis ullamcorper ipsum vitae tellus auctor ullamcorper. Aenean ultrices egestas neque, sit amet aliquam erat malesuada id. Maecenas venenatis purus gravida urna luctus consequat. Donec posuere, ligula nec feugiat tristique, lectus elit ultrices nisi, ut mollis risus lacus in nisi. Ut auctor lectus sed orci scelerisque, nec pellentesque tellus aliquet. Curabitur nec faucibus urna. Vestibulum congue mattis libero, vel egestas est sodales in. Curabitur tortor felis, tempus ac dictum eu, dictum non metus. Cras molestie lacinia enim, vitae auctor justo laoreet et. Suspendisse nec ullamcorper ligula. Pellentesque feugiat hendrerit velit, et sagittis dui tristique sed. Etiam ex turpis, mollis et enim ut, dapibus tempus neque. Etiam interdum molestie nisl a condimentum. Nulla faucibus ante at lacus posuere, at consectetur nunc egestas.</div>' \
                      '</body></html>'
            content = content.replace('{{LANG}}', local_lang.language)
            content = content.replace('{{CHAPTER1_NAME}}', local_lang['Home']['emptyBookCreation']['Chapter1'])
            file.write(content)

        filename = file_name_template\
            .replace('%title%', title)\
            .replace('%serie%', series)\
            .replace('%authors%', authors)
        output = app_directory+os.sep+'tmp'+os.sep+filename+'.epub'
        deflate(app_directory+os.sep+'tmp'+os.sep+'*', output)
        return output
    except Exception:
        return None


def get_epub_info(path: str):
    ret = {
        'guid': None,
        'title': None,
        'authors': None,
        'serie': None,
        'tags': [],
        'cover': None,
        'toc': None,
        'chapters': list()
    }
    try:
        if os.path.isfile(path) is True:
            myzip = zipfile.ZipFile(path, 'r')

            myfile = myzip.open('META-INF/container.xml')
            mydoc = minidom.parseString(myfile.read())
            item = mydoc.getElementsByTagName('rootfile')[0]
            file2 = item.attributes['full-path'].value
            myfile.close()

            base = ''
            if '/' in file2:
                tab = file2.split('/')
                base = ''
                i = 0
                while i < len(tab) - 1:
                    if i > 0: base += '/'
                    base += tab[i]
                    i+=1
                base += '/'
            myfile = myzip.open(file2)
            mydoc = minidom.parseString(myfile.read())

            try: ret['guid'] = mydoc.getElementsByTagName('dc:identifier')[0].firstChild.data
            except Exception: {}
            try: ret['title'] = mydoc.getElementsByTagName('dc:title')[0].firstChild.data
            except Exception: {}
            try: ret['authors'] = mydoc.getElementsByTagName('dc:creator')[0].firstChild.data
            except Exception: {}
            try:
                subjects = mydoc.getElementsByTagName('dc:subject')
                for subject in subjects:
                    ret['tags'].append(subject.data)
            except Exception: {}

            metas = mydoc.getElementsByTagName('meta')
            cov_id = ''
            for meta in metas:
                if meta.attributes['name'].value == 'cover': cov_id = meta.attributes['content'].value
                if meta.attributes['name'].value == 'calibre:series': ret['serie'] = meta.attributes['content'].value
                if meta.attributes['name'].value == 'dc:series': ret['serie'] = meta.attributes['content'].value

            items = mydoc.getElementsByTagName('item')
            spine = mydoc.getElementsByTagName('spine')[0].attributes['toc'].value

            for itm in items:
                if itm.attributes['id'].value == spine:
                    ret['toc'] = itm.attributes['href'].value
                if cov_id != '':
                    if itm.attributes['id'].value == cov_id:
                        filepath, ext = os.path.splitext(itm.attributes['href'].value)
                        tmpdir = app_directory + '/tmp'  # create var for temporary file extraction
                        if os.path.isdir(tmpdir) is False:
                            os.makedirs(tmpdir)
                        mfile = myzip.extract(base+itm.attributes['href'].value, tmpdir)
                        ret['cover'] = create_thumbnail(mfile)
                        break
                else:
                    if itm.attributes['media-type'].value in ['image/jpeg', 'image/png']:
                        filepath, ext = os.path.splitext(itm.attributes['href'].value)
                        tmpdir = app_directory + '/tmp'  # create var for temporary file extraction
                        if os.path.isdir(tmpdir) is False:
                            os.makedirs(tmpdir)
                        mfile = myzip.extract(base+itm.attributes['href'].value, tmpdir)
                        ret['cover'] = create_thumbnail(mfile)
                        break
            myfile.close()

            myfile = myzip.open(base+ret['toc'])
            mydoc = minidom.parseString(myfile.read())
            itemrefs = mydoc.getElementsByTagName('navPoint')
            for ref in itemrefs:
                id = ref.attributes['id'].value
                ret['chapters'].append({
                    'id': ref.attributes['id'].value,
                    'name': ref.getElementsByTagName('text')[0].firstChild.data,
                    'src': base+ref.getElementsByTagName('content')[0].attributes['src'].value
                })
            myfile.close()

            myzip.close()
            return ret
    except Exception:
        traceback.print_exc()
    return None


def insert_book(database: bdd.BDD, file_name_template: str, file_name_separator: str, file: str):
    file = file.replace('/', os.sep)
    if os.path.isfile(file) is True:
        # list of var for future injection into database
        tmp_guid = ''
        tmp_cover = ''
        tmp_title = uid()
        tmp_serie = ''
        tmp_authors = ''
        tmp_tags = ''

        filepath, ext = os.path.splitext(file)  # Get file path and extension
        tmp_format = ext[1:].upper()  # assign file type into var for future injection into database
        t = filepath.split(os.sep)  # explode file path into a list
        filename = t[len(t) - 1]  # get file name without extension
        tmpdir = 'tmp' + os.sep + filename.replace(' ', '_')  # create var for temporary file extraction
        print('filename = ' + filename)
        print('ext = ' + tmp_format)
        if os.path.isdir(tmpdir) is True: shutil.rmtree(tmpdir)  # delete temp dir if already exist
        os.makedirs(tmpdir)  # make temp dir

        tab_mask = file_name_template.split(file_name_separator)
        tab_file = []
        try:
            tab_file = filename.split(file_name_separator)
        except Exception:
            tab_file.append(filename)
        i = 0
        try:
            while i < len(tab_file):
                if tab_mask[i] == '%title%': tmp_title = tab_file[i]
                if tab_mask[i] == '%authors%': tmp_authors = tab_file[i]
                if tab_mask[i] == '%serie%': tmp_serie = tab_file[i]
                if tab_mask[i] == '%tags%': tmp_tags = tab_file[i]
                i += 1
        except Exception:
            ""

        if ext in ['.epub', '.epub2', '.epub3']:  # section for EPUB files
            tmp_guid = uid()  # assign random guid for CBZ and CBR books
            infos = get_epub_info(file)
            print(infos)
            if infos['guid'] is not None: tmp_guid = infos['guid']
            tmp_title = infos['title']
            tmp_authors = infos['authors']
            tmp_serie = infos['serie']
            tmp_cover = infos['cover']

            if len(database.getBooks(tmp_guid)) > 0:
                tmp_guid = uid()

        elif ext in ['.cbz', '.cbr']:  # section for CBZ and CBR files
            tmp_guid = uid()  # assign random guid for CBZ and CBR books
            ret = inflate(file, tmpdir)
            print(ret)
            tmp_cover = create_thumbnail(listDir(tmpdir)[0])  # get path of the first image into temp dir

        else:
            print('Invalid file format')
            return

        # shutil.rmtree(tmpdir)  # delete temp dir

        # build final file path
        end_file = '../data/'
        if tmp_authors is not None:
            if tmp_authors != '': end_file += clean_string_for_url(tmp_authors) + '/'
        if tmp_serie is not None:
            if tmp_serie != '': end_file += clean_string_for_url(tmp_serie) + '/'
        # create final file dir path
        if os.path.isdir(end_file) is not True:
            os.makedirs(end_file)
        # copy file to the destination
        end_file += clean_string_for_url(tmp_title) + ext
        print(end_file)
        shutil.copyfile(file, end_file)
        # insert data in database
        database.insertBook(tmp_guid, tmp_title, tmp_serie, tmp_authors, tmp_tags, get_file_size(end_file), tmp_format, end_file, tmp_cover)