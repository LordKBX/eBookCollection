import os, re
from PyQt5 import QtCore, QtGui, QtWidgets

app_directory = os.path.dirname(os.path.realpath(__file__))
app_name = "eBookCollection"

env_vars = {
        'tools': {
            'poppler': {
                'nt': {
                    'path': app_directory + os.sep + 'tools' + os.sep + 'poppler' + os.sep + 'pdftoppm.exe',
                    'params_cover': '-singlefile -r 200 -scale-to 600 -hide-annotations -jpeg -jpegopt quality=92,progressive=y,optimize=y %input% %output%',
                    'params_full': '-r 200 -scale-to 1920 -hide-annotations -jpeg -jpegopt quality=92,progressive=y,optimize=y %input% %output%'
                }
            },
            '7zip': {
                'nt': {
                    'path': app_directory + os.sep + 'tools' + os.sep + '7zip' + os.sep + '7z.exe',
                    'params_deflate': 'a -tzip %output% %input%',
                    'params_inflate': 'x %input% -o%output%'
                }
                # linux = p7zip, macos = keka
            }
        },
        'vars': {
            'import_file_template': {
                'default': '%title% - %serie% - %authors%',
                'title_authors': '%title% - %authors%',
                'serie_title_authors': '%serie% - %title% - %authors%',
                'title_serie_authors': '%title% - %serie% - %authors%',
                'title_authors_tags': '%title% - %authors% - %tags%',
                'serie_title_authors_tags': '%serie% - %title% - %authors% - %tags%',
                'title_serie_authors_tags': '%title% - %serie% - %authors% - %tags%'
            },
            'import_file_separator': ' - ',
            'home_central_table_header_size_policy': 'UserDefined',  # ResizeToContents, ResizeToContentsAndInteractive, Stretch, UserDefined
            'home_central_table_header_sizes': '[100, 100, 100, 100, 100]',  # list of collumns size
            'default_style': 'Dark',
            'default_language': 'auto',
            'default_cover': {
                'colors': [
                    '#ffffff',
                    '#000000',
                ],
                'patterns': [],
                'background': '#ffffff',
                'pattern': '01',
                'title': '#000000',
                'series': '#000000',
                'authors': '#000000'
            }
        },
        'styles': { }
    }

directory = os.path.dirname(os.path.realpath(__file__)) + os.sep + "ressources" + os.sep + "cover_patterns"
ext = "png"
for root, directories, files in os.walk(directory, topdown=False):
    for name in files:
        if re.search("\\.({})$".format(ext), name) is None:
            continue
        else:
            nm = name.replace("."+ext, "")
            env_vars['vars']['default_cover']['patterns'].append(nm)

directory = os.path.dirname(os.path.realpath(__file__)) + os.sep + "ressources" + os.sep + "styles"
ext = "json"
for root, directories, files in os.walk(directory, topdown=False):
    for name in files:
        if re.search("\\.({})$".format(ext), name) is None:
            continue
        else:
            nm = name.replace("."+ext, "")
            fp = open(directory + os.sep + name, "r", encoding="utf8")
            content = fp.read()
            fp.close()
            env_vars['styles'][nm] = eval(content.replace('{APP_DIR}', app_directory.replace(os.sep, '/')))
