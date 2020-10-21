import sys, os, io, traceback
from xml.dom import minidom
from PIL import Image
import base64
import zipfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import bdd
from common.common import *
from vars import *


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


def getEpubIfo(path: str):
    ret = {
        'guid': None,
        'title': None,
        'authors': None,
        'serie': None,
        'tags': None,
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
            try: ret['serie'] = mydoc.getElementsByTagName('dc:subject')[0].firstChild.data
            except Exception: {}

            metas = mydoc.getElementsByTagName('meta')
            cov_id = ''
            for meta in metas:
                if meta.attributes['name'].value == 'cover': cov_id = meta.attributes['content'].value
                if meta.attributes['name'].value == 'calibre:series': ret['serie'] = meta.attributes['content'].value

            items = mydoc.getElementsByTagName('item')
            spine = mydoc.getElementsByTagName('spine')[0].attributes['toc'].value

            for itm in items:
                if itm.attributes['id'].value == spine:
                    ret['toc'] = itm.attributes['href'].value
                if cov_id != '':
                    if itm.attributes['id'].value == cov_id:
                        filepath, ext = os.path.splitext(itm.attributes['href'].value)
                        tmpdir = appDir + '/tmp'  # create var for temporary file extraction
                        if os.path.isdir(tmpdir) is False:
                            os.makedirs(tmpdir)
                        mfile = myzip.extract(base+itm.attributes['href'].value, tmpdir)
                        ret['cover'] = create_thumbnail(mfile)
                        break
                else:
                    if itm.attributes['media-type'].value in ['image/jpeg', 'image/png']:
                        filepath, ext = os.path.splitext(itm.attributes['href'].value)
                        tmpdir = appDir + '/tmp'  # create var for temporary file extraction
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


def insertBook(tools: dict, database: bdd.BDD, file_name_template: str, file_name_separator: str, file: str):
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
        t = filepath.split('/')  # explode file path into a list
        filename = t[len(t) - 1]  # get file name without extension
        tmpdir = 'tmp/' + filename.replace(' ', '_')  # create var for temporary file extraction
        print('filename = ' + filename)
        print('ext = ' + tmp_format)
        if os.path.isdir(tmpdir) is True: shutil.rmtree(tmpdir)  # delete temp dir if already exist
        os.makedirs(tmpdir)  # make temp dir

        tab_mask = file_name_template.split(file_name_separator)
        tab_file = filename.split(file_name_separator)
        i = 0
        while i < len(tab_file):
            if tab_mask[i] == '%title%': tmp_title = tab_file[i]
            if tab_mask[i] == '%authors%': tmp_authors = tab_file[i]
            if tab_mask[i] == '%serie%': tmp_serie = tab_file[i]
            if tab_mask[i] == '%tags%': tmp_tags = tab_file[i]
            i += 1

        if ext in ['.epub', '.epub2', '.epub3']:  # section for EPUB files
            tmp_guid = uid()  # assign random guid for CBZ and CBR books
            infos = getEpubIfo(file)
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
            list_args = list()  # create list argument for external command execution
            list_args.append(tools['7zip'][os.name]['path'])  # insert executable path
            temp_args = tools['7zip'][os.name]['params_deflate'].split(' ')  # create table of raw command arguments
            for var in temp_args:  # parse table of raw command arguments
                # insert parsed param
                list_args.append(var.replace('%input%', file).replace('%output%', tmpdir))
            print(list_args)
            ret = subprocess.check_output(list_args, universal_newlines=True)  # execute the command
            print(ret)
            tmp_cover = create_thumbnail(listDir(tmpdir)[0])  # get path of the first image into temp dir

        else:
            print('Invalid file format')
            return

        # shutil.rmtree(tmpdir)  # delete temp dir

        # build final file path
        end_file = '../data/'
        if tmp_authors is not None:
            if tmp_authors != '': end_file += cleanStringForUrl(tmp_authors) + '/'
        if tmp_serie is not None:
            if tmp_serie != '': end_file += cleanStringForUrl(tmp_serie) + '/'
        # create final file dir path
        if os.path.isdir(end_file) is not True:
            os.makedirs(end_file)
        # copy file to the destination
        end_file += cleanStringForUrl(tmp_title) + ext
        print(end_file)
        shutil.copyfile(file, end_file)
        # insert data in database
        database.insertBook(tmp_guid, tmp_title, tmp_serie, tmp_authors, tmp_tags, get_file_size(end_file), tmp_format, end_file, tmp_cover)