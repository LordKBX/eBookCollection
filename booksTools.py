import sys
import os
import io
import subprocess
import shutil
import traceback
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
        tmp_title = ''
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
            {}
        if ext in ['.cbz', '.cbr']:  # section for CBZ and CBR files
            tmp_guid = uid()  # assign random guid for CBZ and CBR books
            list_args = list()  # create list argument for external command execution
            list_args.append(tools['7zip'][os.name]['path'])  # insert executable path
            temp_args = tools['7zip'][os.name]['params_deflate'].split(
                ' ')  # create table of raw command arguments
            for var in temp_args:  # parse table of raw command arguments
                # insert parsed param
                list_args.append(var.replace('%input%', file).replace('%output%', tmpdir))
            print(list_args)
            ret = subprocess.check_output(list_args, universal_newlines=True)  # execute the command
            print(ret)
            tmp_cover = create_thumbnail(listDir(tmpdir)[0])  # get path of the first image into temp dir

        # shutil.rmtree(tmpdir)  # delete temp dir
        end_file = 'data/' + tmp_authors + '/'
        if tmp_serie is not None:
            if tmp_serie != '': end_file += tmp_serie + '/'
        if os.path.isdir(end_file) is not True:
            os.makedirs(end_file)
        end_file += tmp_title + ext
        shutil.copyfile(file, end_file)
        database.insertBook(tmp_guid, tmp_title, tmp_serie, tmp_authors, tmp_tags, get_file_size(end_file), tmp_format, end_file, tmp_cover)