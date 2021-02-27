import os
from PyQt5 import QtCore, QtGui, QtWidgets

app_directory = os.path.dirname(os.path.realpath(__file__))
app_name = "EbookCollection"

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
            'home_central_table_header_sizes': '[100, 100, 100, 100, 100]'  # list of collumns size
        },
        'styles': {
            'black': {
                'icons': {
                    'folder': app_directory.replace(os.sep, '/') + '/icons/white/folder.png',
                    'file': app_directory.replace(os.sep, '/') + '/icons/white/file.png',
                    'lock': app_directory.replace(os.sep, '/') + '/icons/white/lock.png',
                    'unlock': app_directory.replace(os.sep, '/') + '/icons/white/unlock.png'
                },
                'dialog': """
                    QDialog{ background-color:#4B4B4B; }
                    QScrollArea{ background-color:#4B4B4B; }
                    QLabel{ 
                        color:#999999;
                        font-size:15px;
                        font-weight:bold;
                        background: transparent;
                    }
                    QSpinBox, QDoubleSpinBox, QLineEdit, QComboBox{ 
                        background-color:#333333;
                        color:#777777;
                        border:#999999 2px solid;
                        font-size:15px;
                    }
                 """,
                'QTabWidget': """
                    QTabWidget {
                    }
                    QTabWidget::tab-bar {
                        background-color:#333333;
                        color:#AAAAAA;
                    }
                    QTabBar::tab {
                        background-color:#999999;
                        cursor:pointer;
                        padding: 10px;
                        border-bottom: 1px solid #ffffff;
                        border-right: 1px solid #ffffff;
                    }
                    QTabBar::tab:selected
                    {
                        background-color:#004DD3;
                        color:#ffffff;
                    }
                    QTabBar::tab:hover 
                    {
                        background-color:#196DFF;
                        color:#ffffff;
                    }
                    QTabWidget::pane {
                        background-color:#ff0000;
                    }
                 """,
                'fullTreeView': """
                    ::section{
                        background-color:#4B4B4B;
                        color:#ffffff;
                    }
                    QTreeView::branch:has-siblings:!adjoins-item { }
                    QTreeView::branch:has-siblings:adjoins-item { }
                    QTreeView::branch:!has-children:!has-siblings:adjoins-item { }
                    
                    QTreeView::branch:has-children:!has-siblings:closed, QTreeView::branch:closed:has-children:has-siblings {
                        border-image: none;
                        image: url('""" + app_directory.replace(os.sep, '/') + """/icons/white/tree_closed.png');
                    }
        
                    QTreeView::branch:open:has-children:!has-siblings,
                    QTreeView::branch:open:has-children:has-siblings  {
                        border-image: none;
                        image: url('""" + app_directory.replace(os.sep, '/') + """/icons/white/tree_opened.png');
                    }
                    """,
                'partialTreeView': """
                    ::section{
                        background-color:#4B4B4B;
                    }
                    QTreeWidget::item { 
                        padding-left:2px;
                    }
                    QTreeWidget::item:hover, QTreeWidget::branch:hover
                    {
                        color: rgb(43, 179, 246);
                        cursor: pointer;
                    }
                    QTreeWidget::item:selected { 
                        background-color: rgb(0, 85, 255);
                        color:white; 
                    }
                    """,
                'partialTreeViewItemColorNew': "#5972FF",
                'partialTreeViewItemColorDel': "#FF324E",
                'partialTreeViewItemColorMod': "#EFC91C",
                'defaultButton': """
                    QPushButton{ background:transparent; }
                    QPushButton:hover{ background-color:rgb(120, 120, 120); }
                    QPushButton:pressed{ background-color:rgb(120, 120, 120); }
                    QPushButton:checked{ background-color:rgb(150, 150, 150); }
                    """,
                'defaultAltButton': """
                    QToolButton{ background:transparent; }
                    QToolButton:hover{ background-color:rgb(120, 120, 120); }
                    QToolButton:pressed{ background-color:rgb(120, 120, 120); }
                    QToolButton:checked{ background-color:rgb(150, 150, 150); }
                    """,
                'fullButton': """
                    QPushButton{ background-color:rgb(80, 80, 80); }
                    QPushButton:hover{ background-color:rgb(120, 120, 120); }
                    QPushButton:pressed{ background-color:rgb(120, 120, 120); }
                    QPushButton:checked{ background-color:rgb(150, 150, 150); }
                    """,
                'fullAltButton': """
                    *{ background-color:rgb(80, 80, 80); color:#ffffff; }
                    *:hover{ background-color:rgb(120, 120, 120); }
                    *:pressed{ background-color:rgb(120, 120, 120); }
                    *:checked{ background-color:rgb(150, 150, 150); }
                    """,
                'invisibleButton': """
                    QPushButton{ background:transparent; }
                    QPushButton:hover{ background:transparent; }
                    QPushButton:pressed{ background:transparent; }
                    QPushButton:checked{ background:transparent; }
                    """,
                'displayButton': """
                    QPushButton{ border:#000000 1px solid; background-color:rgb(80, 80, 80); }
                    QPushButton:hover{ background-color:rgb(80, 80, 80); }
                    QPushButton:pressed{ background-color:rgb(80, 80, 80); }
                    QPushButton:checked{ background-color:rgb(80, 80, 80); }
                    """,
                'border': """
                    QWidget{ border:#000000 1px solid; }
                    """
            }
        }
    }