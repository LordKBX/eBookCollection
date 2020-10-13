# This Python file uses the following encoding: utf-8

# sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from bdd import *
from lang import *
from home.home import *

if __name__ == "__main__":
    app = QApplication([])
    bdd = BDD()
    translation = Lang()
    env_vars = {
        'tools': {
            'poppler': {
                'nt': {
                    'path': 'tools/poppler/pdftoppm.exe',
                    'params_cover': '-singlefile -r 200 -scale-to 600 -hide-annotations -jpeg -jpegopt quality=92,progressive=y,optimize=y %input% %output%',
                    'params_full': '-r 200 -scale-to 1920 -hide-annotations -jpeg -jpegopt quality=92,progressive=y,optimize=y %input% %output%'
                }
            },
            '7zip': {
                'nt': {
                    'path': 'tools/7zip/7z.exe',
                    'params_zip': 'a -tzip %input% %output%',
                    'params_deflate': 'x %input% -o%output%'
                }
                # linux = p7zip, macos = keka
            }
        },
        'vars': {
            'import_file_template': {
                'default': '%title% - %authors%',
                'title_authors': '%title% - %authors%',
                'serie_title_authors': '%serie% - %title% - %authors%',
                'title_authors_tags': '%title% - %authors% - %tags%',
                'serie_title_authors_tags': '%serie% - %title% - %authors% - %tags%'
            },
            'import_file_separator': ' - ',
            'home_central_table_header_size_policy': 'UserDefined',  # ResizeToContents, ResizeToContentsAndInteractive, Stretch, UserDefined
            'home_central_table_header_sizes': '[100, 100, 100, 100, 100]'  # list of collumns size
        }
    }
    ret = bdd.getParam('home_central_table_header_size_policy')
    if ret is not None: env_vars['vars']['home_central_table_header_size_policy'] = ret
    ret = bdd.getParam('home_central_table_header_sizes')
    if ret is not None: env_vars['vars']['home_central_table_header_sizes'] = ret

    Home = HomeWindow(bdd, translation, env_vars)
    Home.show()
    sys.exit(app.exec_())
