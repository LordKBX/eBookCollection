import sys
import os
import io
import subprocess
import shutil
import traceback
from xml.dom import minidom
import bdd
from common import *
import PIL
from PIL import Image
import base64


def create_thumbnail(path: str):
    max_h = max_w = 600
    img = Image.open(path)
    img.load()
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
            list_args = list()  # create list argument for external command execution
            list_args.append(tools['7zip'][os.name]['path'])  # insert executable path
            temp_args = tools['7zip'][os.name]['params_deflate'].split(' ')  # create table of raw command arguments
            for var in temp_args:  # parse table of raw command arguments
                # insert parsed param
                list_args.append(var.replace('%input%', file).replace('%output%', tmpdir))
            print(list_args)
            process = subprocess.Popen(list_args, shell=False)  # execute the command
            process.wait()
            # print(process.returncode)

            try:
                metainfo_file = tmpdir + '/META-INF/container.xml'
                mydoc = minidom.parse(metainfo_file)
                item = mydoc.getElementsByTagName('rootfile')[0]
                print( item.attributes['full-path'].value )

                metadata_file = tmpdir + '/' + item.attributes['full-path'].value
                mydoc = minidom.parse(metadata_file)
                try: tmp_guid = mydoc.getElementsByTagName('dc:identifier')[0].firstChild.data
                except Exception: {}
                try: tmp_title = mydoc.getElementsByTagName('dc:title')[0].firstChild.data
                except Exception: {}
                try: tmp_authors = mydoc.getElementsByTagName('dc:creator')[0].firstChild.data
                except Exception: {}
                try: tmp_serie = mydoc.getElementsByTagName('dc:subject')[0].firstChild.data
                except Exception: {}
                metas = mydoc.getElementsByTagName('meta')
                cov_id = ''
                for meta in metas:
                    if meta.attributes['name'].value == 'cover':
                        cov_id = meta.attributes['content'].value
                    if meta.attributes['name'].value == 'calibre:series':
                        tmp_serie = meta.attributes['content'].value
                print("cov_id = ".format(cov_id))

                items = mydoc.getElementsByTagName('item')
                for itm in items:
                    if itm.attributes['id'].value == cov_id:
                        print('cover = {}'.format(itm.attributes['href'].value))
                        tmp_cover = create_thumbnail(tmpdir + '/' + itm.attributes['href'].value)
            except Exception:
                traceback.print_exc()

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
        end_file = 'data/'
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