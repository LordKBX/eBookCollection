import os, sys, re, traceback, subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
import json.decoder
import json.encoder
import jsonschema
from common.json_shema import JSONSchemaGenerator
import common.archive
import common.files

app_editor = "LordKBX Workshop"
app_name = "eBookCollection"
app_id = 'lordkbx.ebook_collection'
app_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
app_user_directory = os.path.expanduser('~') + os.sep + app_name
app_icons = {
    'x16': 'ressources' + os.sep + 'icons' + os.sep + 'app_icon16x16.png',
    'x24': 'ressources' + os.sep + 'icons' + os.sep + 'app_icon24x24.png',
    'x32': 'ressources' + os.sep + 'icons' + os.sep + 'app_icon32x32.png',
    'x48': 'ressources' + os.sep + 'icons' + os.sep + 'app_icon48x48.png',
    'x256': 'ressources' + os.sep + 'icons' + os.sep + 'app_icon256x256.png'
}
__default_style = 'Dark'
debug = False
if "python" in sys.argv[0].lower():
    debug = True


def load_path_archiver():
    settings = QtCore.QSettings(app_editor, app_name)
    path_archiver = None
    path_archiver = settings.value('archiver_dir', None, str)
    if path_archiver is None or path_archiver == '':
        if os.name == 'nt':
            settings_7zip = QtCore.QSettings('HKEY_CURRENT_USER\\SOFTWARE\\7-Zip', QtCore.QSettings.NativeFormat)
            path_archiver = settings_7zip.value('Path', None)
            if path_archiver is None:
                if os.path.isdir(app_user_directory + os.sep + 'tools' + os.sep + '7zip') is True:
                    path_archiver = app_user_directory + os.sep + 'tools' + os.sep + '7zip'
        else:
            path_archiver = None
    else:
        if os.path.isdir(path_archiver) is False:
            path_archiver = None
    return path_archiver


env_vars = {
        'tools': {
            'poppler': {
                'nt': {
                    'path': app_directory + os.sep + 'tools' + os.sep + 'poppler' + os.sep + 'pdftoppm.exe',
                    'params_cover': '-singlefile -r 200 -scale-to 600 -hide-annotations -jpeg -jpegopt quality=92,progressive=y,optimize=y %input% %output%',
                    'params_full': '-r 200 -scale-to 1920 -hide-annotations -jpeg -jpegopt quality=92,progressive=y,optimize=y %input% %output%'
                }
            },
            'archiver': {
                'path': load_path_archiver(),
                'nt': {
                    'exe': '7z.exe',
                    'params_deflate': 'a -tzip %output% %input%',
                    'params_inflate': 'x %input% -o%output%'
                }
                # linux = p7zip, macos = keka
            }
        },
        'vars': {
            'import_file_template': {
                'default': '%title% - %series% - %authors%',
                'title_authors': '%title% - %authors%',
                'serie_title_authors': '%series% - %title% - %authors%',
                'title_serie_authors': '%title% - %series% - %authors%',
                'title_authors_tags': '%title% - %authors% - %tags%',
                'serie_title_authors_tags': '%series% - %title% - %authors% - %tags%',
                'title_serie_authors_tags': '%title% - %series% - %authors% - %tags%'
            },
            'import_file_separator': ' - ',
            'library': {
                'headers_size_policy': 'UserDefined',  # ResizeToContents, ResizeToContentsAndInteractive, Stretch, UserDefined
                'headers_size': '[100, 100, 100, 100, 100]'  # list of collumns size
                },
            'default_storage': os.path.expanduser('~') + os.sep + app_name + os.sep + 'data',
            'default_style': 'Dark',
            'default_language': 'auto',
            'default_cover': {
                'colors': [
                    '#000000', '#000033', '#000066', '#000099', '#0000cc', '#0000ff', '#003300', '#003333', '#003366',
                    '#003399', '#0033cc', '#0033ff', '#006600', '#006633', '#006666', '#006699', '#0066cc', '#0066ff',
                    '#009900', '#009933', '#009966', '#009999', '#0099cc', '#0099ff', '#00cc00', '#00cc33', '#00cc66',
                    '#00cc99', '#00cccc', '#00ccff', '#00ff00', '#00ff33', '#00ff66', '#00ff99', '#00ffcc', '#00ffff',
                    '#330000', '#330033', '#330066', '#330099', '#3300cc', '#3300ff', '#333300', '#333333', '#333366',
                    '#333399', '#3333cc', '#3333ff', '#336600', '#336633', '#336666', '#336699', '#3366cc', '#3366ff',
                    '#339900', '#339933', '#339966', '#339999', '#3399cc', '#3399ff', '#33cc00', '#33cc33', '#33cc66',
                    '#33cc99', '#33cccc', '#33ccff', '#33ff00', '#33ff33', '#33ff66', '#33ff99', '#33ffcc', '#33ffff',
                    '#660000', '#660033', '#660066', '#660099', '#6600cc', '#6600ff', '#663300', '#663333', '#663366',
                    '#663399', '#6633cc', '#6633ff', '#666600', '#666633', '#666666', '#666699', '#6666cc', '#6666ff',
                    '#669900', '#669933', '#669966', '#669999', '#6699cc', '#6699ff', '#66cc00', '#66cc33', '#66cc66',
                    '#66cc99', '#66cccc', '#66ccff', '#66ff00', '#66ff33', '#66ff66', '#66ff99', '#66ffcc', '#66ffff',
                    '#990000', '#990033', '#990066', '#990099', '#9900cc', '#9900ff', '#993300', '#993333', '#993366',
                    '#993399', '#9933cc', '#9933ff', '#996600', '#996633', '#996666', '#996699', '#9966cc', '#9966ff',
                    '#999900', '#999933', '#999966', '#999999', '#9999cc', '#9999ff', '#99cc00', '#99cc33', '#99cc66',
                    '#99cc99', '#99cccc', '#99ccff', '#99ff00', '#99ff33', '#99ff66', '#99ff99', '#99ffcc', '#99ffff',
                    '#cc0000', '#cc0033', '#cc0066', '#cc0099', '#cc00cc', '#cc00ff', '#cc3300', '#cc3333', '#cc3366',
                    '#cc3399', '#cc33cc', '#cc33ff', '#cc6600', '#cc6633', '#cc6666', '#cc6699', '#cc66cc', '#cc66ff',
                    '#cc9900', '#cc9933', '#cc9966', '#cc9999', '#cc99cc', '#cc99ff', '#cccc00', '#cccc33', '#cccc66',
                    '#cccc99', '#cccccc', '#ccccff', '#ccff00', '#ccff33', '#ccff66', '#ccff99', '#ccffcc', '#ccffff',
                    '#ff0000', '#ff0033', '#ff0066', '#ff0099', '#ff00cc', '#ff00ff', '#ff3300', '#ff3333', '#ff3366',
                    '#ff3399', '#ff33cc', '#ff33ff', '#ff6600', '#ff6633', '#ff6666', '#ff6699', '#ff66cc', '#ff66ff',
                    '#ff9900', '#ff9933', '#ff9966', '#ff9999', '#ff99cc', '#ff99ff', '#ffcc00', '#ffcc33', '#ffcc66',
                    '#ffcc99', '#ffcccc', '#ffccff', '#ffff00', '#ffff33', '#ffff66', '#ffff99', '#ffffcc', '#ffffff'
                ],
                'patterns': [],
                'background': '#ffffff',
                'pattern': '01',
                'pattern_color': '#000000',
                'title': '#000000',
                'series': '#000000',
                'authors': '#000000'
            }
        },
        'styles': {
            "Dark": {
                "icons": {
                    "align_center": "{APP_DIR}/ressources/icons/tmp/format-justify-center.png",
                    "align_justify": "{APP_DIR}/ressources/icons/tmp/format-justify-fill.png",
                    "align_left": "{APP_DIR}/ressources/icons/tmp/format-justify-left.png",
                    "align_right": "{APP_DIR}/ressources/icons/tmp/format-justify-right.png",
                    "back_color": "{APP_DIR}/ressources/icons/tmp/format-fill-color.png",
                    "bold": "{APP_DIR}/ressources/icons/tmp/format-text-bold.png",
                    "book_add": "{APP_DIR}/ressources/icons/white/book_add.png",
                    "book_del": "{APP_DIR}/ressources/icons/white/book_del.png",
                    "book_new": "{APP_DIR}/ressources/icons/white/book_new.png",
                    "checkpoint_create": "{APP_DIR}/ressources/icons/tmp/bookmarks.png",
                    "checkpoint_load": "{APP_DIR}/ressources/icons/tmp/catalog.png",
                    "close": "{APP_DIR}/ressources/icons/white/close.png",
                    "comment": "{APP_DIR}/ressources/icons/white/comment.png",
                    "content_table": "{APP_DIR}/ressources/icons/white/content_table.png",
                    "copy": "{APP_DIR}/ressources/icons/tmp/edit-copy.png",
                    "cut": "{APP_DIR}/ressources/icons/tmp/edit-cut.png",
                    "debug": "{APP_DIR}/ressources/icons/tmp/debug.png",
                    "edit": "{APP_DIR}/ressources/icons/white/edit.png",
                    "file": "{APP_DIR}/ressources/icons/white/file.png",
                    "file_manager": "{APP_DIR}/ressources/icons/tmp/tb_folder.png",
                    "folder": "{APP_DIR}/ressources/icons/white/folder.png",
                    "font": "{APP_DIR}/ressources/icons/tmp/font.png",
                    "full_screen": "{APP_DIR}/ressources/icons/white/full_screen.png",
                    "image": "{APP_DIR}/ressources/icons/tmp/view-image.png",
                    "info": "{APP_DIR}/ressources/icons/white/info.png",
                    "italic": "{APP_DIR}/ressources/icons/tmp/format-text-italic.png",
                    "link": "{APP_DIR}/ressources/icons/tmp/insert-link.png",
                    "list": "{APP_DIR}/ressources/icons/tmp/format-list-unordered.png",
                    "list_ordered": "{APP_DIR}/ressources/icons/tmp/format-list-ordered.png",
                    "lock": "{APP_DIR}/ressources/icons/white/lock.png",
                    "normal_screen": "{APP_DIR}/ressources/icons/white/normal_screen.png",
                    "page": "{APP_DIR}/ressources/icons/tmp/view.png",
                    "paste": "{APP_DIR}/ressources/icons/tmp/edit-paste.png",
                    "prettify": "{APP_DIR}/ressources/icons/tmp/beautify.png",
                    "redo": "{APP_DIR}/ressources/icons/tmp/edit-redo.png",
                    "save": "{APP_DIR}/ressources/icons/white/save.png",
                    "search": "{APP_DIR}/ressources/icons/tmp/search.png",
                    "settings": "{APP_DIR}/ressources/icons/white/settings.png",
                    "sort_down": "{APP_DIR}/ressources/icons/white/sort_down.png",
                    "sort_up": "{APP_DIR}/ressources/icons/white/sort_up.png",
                    "strike_through": "{APP_DIR}/ressources/icons/tmp/format-text-strikethrough.png",
                    "style": "{APP_DIR}/ressources/icons/tmp/lookfeel.png",
                    "sub": "{APP_DIR}/ressources/icons/tmp/format-text-subscript.png",
                    "sup": "{APP_DIR}/ressources/icons/tmp/format-text-superscript.png",
                    "text_color": "{APP_DIR}/ressources/icons/tmp/format-text-color.png",
                    "underline": "{APP_DIR}/ressources/icons/tmp/format-text-underline.png",
                    "undo": "{APP_DIR}/ressources/icons/tmp/edit-undo.png",
                    "unlock": "{APP_DIR}/ressources/icons/white/unlock.png",
                    "xml": "{APP_DIR}/ressources/icons/white/xml.png"
                },
                "QMainWindow": [
                    "QMainWindow { background-color: rgb(63, 63, 63); color:#ffffff; }",
                    "QMainWindow::separator { background: rgb(63, 63, 63); }",
                    "QMainWindow::separator:hover { background: rgb(120, 120, 120); }",
                    "QWidget{ background: rgb(63, 63, 63); color:white; }",
                    "QLabel[bold]{ font-weight:bold; font-size:12px; }",
                    "QPushButton, QToolButton { border:#000000 1px solid; background-color: rgb(80, 80, 80); }",
                    "QPushButton:hover, QToolButton:hover { background-color: rgb(120, 120, 120); }",
                    "QPushButton:pressed, QToolButton:pressed { background-color: rgb(120, 120, 120); }",
                    "QPushButton:checked, QToolButton:checked { background-color: rgb(150, 150, 150); }",
                    "QLineEdit { background-color: rgb(100, 100, 100); }"],
                "QDockWidget": [
                    "QDockWidget { ",
                    "    background-color: rgb(63, 63, 63) !important;",
                    "    titlebar-close-icon: url(\"../ressources/icons/white/close.png\") !important;",
                    "    titlebar-normal-icon: url(\"../ressources/icons/white/content_table.png\") !important;",
                    "}",
                    "QDockWidget::close-button, QDockWidget::float-button { background-color: #333333 !important; min-height:20px; min-width:20px; height:20px; width:20px; cursor:pointer; }",
                    "QDockWidget::close-button:hover, QDockWidget::float-button:hover { background-color: #666666 !important; cursor:pointer; }",
                    "QDockWidget::close-button:pressed, QDockWidget::float-button:pressed { background-color: #444444 !important; cursor:pointer;  }",
                    "QDockWidget::title { font: bold; text-align: left; background-color: #333333; padding: 0px; height:30px; }"
                ],
                "QMessageBox": [
                    "QMessageBox { background-color: rgb(62, 62, 62); color: rgb(255, 255, 255); }",
                    "QWidget{ background-color: rgb(62, 62, 62); color: rgb(255, 255, 255); }",
                    "QLabel{ color:#999999; font-size:15px; font-weight:bold; background: transparent; }",
                    "QPushButton{ background-color:#333333; color:#777777; border:#999999 2px solid; font-size:15px; padding:10px; }"
                ],
                "QMessageBoxBtnGeneric": "QPushButton{ background-color: rgb(90, 90, 90); color: rgb(255, 255, 255); }",
                "QMessageBoxBtnRed": "QPushButton{ background-color: rgb(234, 86, 86); color: rgb(255, 255, 255); }",
                "QMessageBoxBtnGreen": "QPushButton{ background-color: rgb(0, 153, 15); color: rgb(255, 255, 255); }",
                "QDialog": [
                    "*{ color:#FFFFFF; }",
                    "QDialog, QWidget{ background-color:#4B4B4B; }",
                    "QScrollArea{ background-color:#4B4B4B; }",
                    "QLabel{ color:#999999; font-size:15px; font-weight:bold; background: transparent; }",
                    "QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit, QDateEdit{ background-color:#333333; color:#777777; border:#999999 2px solid; font-size:15px; padding:10px; }",
                    "QPushButton, QToolButton { background-color:#333333; color:#777777; border:#999999 2px solid; font-size:15px; min-height:35px; height:35px; width:100%;}",
                    "QPushButton:hover, QToolButton:hover { background-color:#555555; color:#ffffff; border:#ffffff 2px solid; }",
                    "QPushButton:pressed, QToolButton:pressed, QPushButton:checked, QToolButton:checked { background-color:#999999; color:#000000; border:#ffffff 2px solid; }",
                    "#tab_metadata_import_filename_template_label{ margin:0px; }",
                    "#tab_metadata_import_filename_template_combo_box{ padding:5px; margin-bottom:5px; }",
                    "#tab_metadata_import_filename_separator_label{ padding-right:5px; }"
                ],
                "QDialogTextSizeAlt": [
                    "QLabel{ font-size:12px; }",
                    "QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit, QDateEdit{ font-size:12px; padding:5px; }",
                    "QPushButton, QToolButton { font-size:12px; min-height:25px; height:25px; }"
                ],
                "QComboBox": [
                    "background-color:#333333; color:#777777; border:#999999 2px solid; font-size:15px; padding:10px;"
                ],
                "QComboBoxAlt": [
                    "background-color:#333333; color:#777777; border:#999999 2px solid; font-size:12px; padding:5px;"
                ],
                "QTabWidgetHorizontal": [
                    "QTabWidget::tab-bar { background-color:#333333; color:#AAAAAA; }",
                    "QTabBar::tab { ",
                    "    background-color:#999999; cursor:pointer; padding: 10px; border: 1px solid #333333;",
                    "    border-bottom: 0px; border-top-left-radius: 10px; border-top-right-radius: 10px;",
                    "    border-bottom: 1px solid #999999;",
                    "    }",
                    "QTabBar::tab:selected{ background-color:#004DD3; color:#ffffff; }",
                    "QTabBar::tab:hover{ background-color:#196DFF; color:#ffffff; }",
                    "QTabWidget::pane QTabBar{ padding-top:5px; }",
                    "QTabBar::close-button {  border-image: none; image: url('{APP_DIR}/ressources/icons/white/close.png'); }",
                    "QTabBar::close-button:hover {  border-image: none; image: url('{APP_DIR}/ressources/icons/black/close.png'); }"
                ],
                "QTabWidgetVertical": [
                    "QTabWidget { background: none; }",
                    "QTabWidget::tab-bar { background-color:#333333; color:#AAAAAA; border-right: 0; }",
                    "QTabBar::tab { background-color:#999999; cursor:pointer; padding: 10px; border-bottom: 1px solid #ffffff; border-right: 1px solid #ffffff; }",
                    "QTabBar::tab:selected{ background-color:#004DD3; color:#ffffff; }",
                    "QTabBar::tab:hover{ background-color:#196DFF; color:#ffffff; }",
                    "QTabWidget::pane QTabBar{ /* border-bottom: 1px solid #999999; */ }"
                ],
                "sorting_block_search_area": "QGroupBox{ border: 1px solid rgb(255, 255, 255); }",
                "fullTreeView": [
                    "QTreeView{ background-color:#888888; }",
                    "QHeaderView::section { background-color:#4B4B4B; color:#ffffff; }",
                    "QTreeView::branch:has-siblings:!adjoins-item {}",
                    "QTreeView::branch:has-siblings:adjoins-item {}",
                    "QTreeView::branch:!has-children:!has-siblings:adjoins-item {}",
                    "QTreeView::branch:has-children:!has-siblings:closed, QTreeView::branch:closed:has-children:has-siblings",
                    "    { border-image: none; image: url('{APP_DIR}/ressources/icons/white/tree_closed.png'); }",
                    "QTreeView::branch:open:has-children:!has-siblings, QTreeView::branch:open:has-children:has-siblings",
                    "    { border-image: none; image: url('{APP_DIR}/ressources/icons/white/tree_opened.png'); }"
                ],
                "partialTreeView": [
                    "QTreeView{ background-color:  #888888; }",
                    "::section { background-color:  #4B4B4B; }",
                    "QTreeWidget::item { padding-left: 2px; }",
                    "QTreeWidget::item:hover, QTreeWidget::branch:hover{ color: rgb(43, 179, 246); cursor: pointer; }",
                    "QTreeWidget::item:selected { background-color: rgb(0, 85, 255); color: white; }"
                ],
                "QTableWidget": [
                    "QHeaderView{ background-color: #333333; color: black; border-color:#000000; }",
                    "QHeaderView::section { background-color: #333333; color: white; font-size: 12px; padding:3px; }",
                    "QHeaderView::down-arrow { image: url('{APP_DIR}/ressources/icons/white/sort_down.png'); width: 20px; height:20px; margin-right:5px; }",
                    "QHeaderView::up-arrow { image: url('{APP_DIR}/ressources/icons/white/sort_up.png'); width: 20px; height:20px; margin-right:5px; }",
                    "QTableWidget::item { padding: 0px; background-color: gray; color: black; }",
                    "QTableWidget::item:alternate { background-color: lightgray; }",
                    "QTableWidget::item:hover { background-color: skyblue; }",
                    "QTableWidget::item:selected { background-color: #0094FF; color: #FFFFFF; }"
                ],
                "partialTreeViewItemColorNew": "#0021C6",
                "partialTreeViewItemColorDel": "#D80020",
                "partialTreeViewItemColorMod": "#EFC91C",
                "defaultButton": [
                    "QPushButton, QToolButton { background-color:#333333; color:#777777; border:#999999 2px solid; font-size:15px; min-height:35px; height:35px; width:100%; }",
                    "QPushButton:hover, QToolButton:hover { background-color:#555555; color:#777777; border:#ffffff 2px solid; }",
                    "QPushButton:pressed, QToolButton:pressed, QPushButton:checked, QToolButton:checked { background-color:#999999; color:#000000; border:#ffffff 2px solid; }"
                ],
                "fullButton": [
                    "QPushButton { background-color: rgb(80, 80, 80); }",
                    "QPushButton:hover { background-color: rgb(120, 120, 120); }",
                    "QPushButton:pressed { background-color: rgb(120, 120, 120); }",
                    "QPushButton:checked { background-color: rgb(150, 150, 150); }"
                ],
                "fullAltButton": [
                    "* { background-color: #666666; color: #ffffff; font-size:15px; min-height:35px; height:35px; }",
                    "*:hover { background-color: rgb(120, 120, 120); }",
                    "*:pressed { background-color: rgb(120, 120, 120); }",
                    "*:checked { background-color: rgb(150, 150, 150); }"
                ],
                "invisibleButton": [
                    "QPushButton { background: transparent; }",
                    "QPushButton:hover { background: transparent; }",
                    "QPushButton:pressed { background: transparent; }",
                    "QPushButton:checked { background: transparent; }"
                ],
                "displayButton": [
                    "QPushButton { border:#000000 1px solid; background-color: rgb(80, 80, 80); }",
                    "QPushButton:hover { background-color: rgb(80, 80, 80); }",
                    "QPushButton:pressed { background-color: rgb(80, 80, 80); }",
                    "QPushButton:checked { background-color: rgb(80, 80, 80); }"
                ],
                "HomeLinkColor": "rgb(255, 255, 255)",
                "SettingsDialogBox": "QPushButton, QToolButton { min-height:20px; height:20px; width:100%; }",
                "SettingsQLineEditPrecise": [
                    "QLineEdit{ ",
                    "border-color:rgb(99, 99, 99);",
                    "border-width: 1px;",
                    "border-style:solid;",
                    "font-size:15px; padding:0px;",
                    " }"
                ],
                "SettingsQLineEditGood": [
                    "QLineEdit{ ",
                    "border-color:rgb(0, 153, 15);",
                    "border-width: 2px;",
                    "border-style:solid;",
                    " }"
                ],
                "SettingsQLineEditBad": [
                    "QLineEdit{ ",
                    "border-color:rgb(234, 86, 86);",
                    "border-width: 2px;",
                    "border-style:solid;",
                    " }"
                ],
                "SettingsQComboBoxArrow": "QComboBox::down-arrow { image:none; width:0px; }",
                "EditorQWebViewPreview": "body { background:#999999;color:#ffffff; }",
                "EditorCentralLabel": "QLabel { color: rgb(255, 255, 255); font-size: 30px; padding:20px; }",
                "EditorFileDialogAdditional": "QPushButton, QToolButton { height:70px;}",
                "EditorEditPaneButtons": [
                    "QPushButton, QToolButton { background: transparent; }",
                    "QPushButton:hover, QToolButton:hover { background-color: rgb(120, 120, 120); }",
                    "QPushButton:pressed, QToolButton:pressed { background-color: rgb(120, 120, 120); }",
                    "QPushButton:checked, QToolButton:checked { background-color: rgb(150, 150, 150); }"
                ],
                "EditorQsciFont": "{APP_DIR}/ressources/fonts/Arimo/Regular.ttf",
                "EditorQsciMarginsBackgroundColor": "#333333",
                "EditorQsciMarginsForegroundColor": "#ffffff",
                "EditorQsciMarkerBackgroundColor": "#ee1111",
                "EditorQsciFoldMarginColor1": "#cccccc",
                "EditorQsciFoldMarginColor2": "#333333",
                "EditorQsciCaretLineBackgroundColor": "#BBBBBB",
                "EditorQsciDefaultTextColor": "#ffffff",
                "EditorQsciDefaultBackgroundColor": "#A6A6A6",
                "EditorQsciXMLDefaultTextColor": "#ffffff",
                "EditorQsciXMLDefaultTagColor": "#ffffff",

                "EditorColorPicker": [
                    "QDialog{ background-color:#4B4B4B; }",
                    "QLabel{ color:#999999; font-size:15px; font-weight:bold; background: transparent; }",
                    "QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit{ background-color:#333333; color:#777777; border:#999999 2px solid; font-size:15px; padding:10px; }",
                    "QGroupBox::title{ color:#999999; padding:2px; }"
                ],
                "EditorColorPickerColorBtn": [
                    "*{ background-color:%1; color:%2; border-width:1px; }",
                    "*:hover, *:pressed{ border-color:#ffffff; border-style:inset;  }"
                ],
                "EditorColorPickerFullAltButton": [
                    "* { background-color: #666666; color: #ffffff; font-size:15px; min-height:30px; height:30px; width:100%; margin-right:1px; }",
                    "*:hover { background-color: rgb(120, 120, 120); }",
                    "*:pressed { background-color: rgb(120, 120, 120); }",
                    "*:checked { background-color: rgb(150, 150, 150); }"
                ],

                "TagsSearchBox": [
                    "* { background-image: url('{APP_DIR}/ressources/icons/tmp/search_30.png') 0 0 0 0 stretch stretch; ",
                    "background-position:top right; background-repeat: norepeat; }"
                ]
            }

        },
        'plugins': { }
    }


def load_patterns():
    global app_directory, env_vars
    directory = app_directory + os.sep + "ressources" + os.sep + "cover_patterns"
    ext = "png"
    env_vars['vars']['default_cover']['patterns'].clear()
    for root, directories, files in os.walk(directory, topdown=False):
        for name in files:
            if re.search("\\.({})$".format(ext), name) is None:
                continue
            else:
                nm = name.replace("." + ext, "")
                env_vars['vars']['default_cover']['patterns'].append(nm)


def load_styles():
    global app_directory, app_user_directory, env_vars
    try:
        directory = app_directory + os.sep + "ressources" + os.sep + "styles"
        directory2 = app_user_directory + os.sep + "imports" + os.sep + "styles"

        jssgenerator = JSONSchemaGenerator()
        encoder = json.encoder.JSONEncoder()
        tab = encoder.encode(env_vars['styles']['Dark'])
        jssgenerator.load(tab)
        schema = jssgenerator.generate()
        try:
            if debug is True:
                with open(app_directory + os.sep + "doc" + os.sep + "packages" + os.sep + "style" + os.sep + 'style.json_schema', 'wt', encoding='utf8') as file:
                    file.write(json.dumps(schema, indent=4))
        except Exception:
            traceback.print_exc()

        ext = "json"
        # env_vars['styles'].clear()
        print(directory2)
        for folder in [directory, directory2]:
            for root, directories, files in os.walk(folder, topdown=False):
                for name in files:
                    if re.search("\\.({})$".format(ext), name) is None:
                        continue
                    else:
                        try:
                            nm = name.replace("." + ext, "")
                            if nm in env_vars['styles']:
                                continue
                            fp = open(folder + os.sep + name, "r", encoding="utf8")
                            content = fp.read()
                            fp.close()

                            # test JSON validity
                            decoder = json.decoder.JSONDecoder()
                            tab = decoder.decode(content)
                            # test package JSON schema
                            jsonschema.validate(instance=tab, schema=schema)

                            env_vars['styles'][nm] = eval(
                                content.replace('{APP_DIR}', app_directory.replace(os.sep, '/'))
                                    .replace('[', '"\\n".join([').replace(']', '])')
                            )
                        except Exception:
                            traceback.print_exc()
    except Exception:
        traceback.print_exc()


def get_styles() -> list:
    global env_vars
    ret = []
    for style in env_vars['styles']:
        ret.append(style)
    return ret


def get_style(style: str):
    global env_vars, __default_style
    if style is None: return None
    if style.strip() == '': return None

    if style not in env_vars['styles']:
        style = __default_style
    if style not in env_vars['styles']:
        return None
    return env_vars['styles'][style]


def get_style_var(style: str = None, path: str = None):
    global env_vars, __default_style
    if style is None:
        style = __default_style
    if path is None: return None
    if style.strip() == '': return None
    if path.strip() == '': return None

    if style not in env_vars['styles']:
        style = __default_style
    if style not in env_vars['styles']:
        return None
    path_tab = path.split('/')
    try:
        base = env_vars['styles'][style]
        for obj in path_tab:
            if obj in base:
                if isinstance(base[obj], dict) is True:
                    base = base[obj]
                else:
                    if isinstance(base[obj], list) is True:
                        return "".join(base[obj]).replace('{APP_DIR}', app_directory.replace(os.sep, '/'))
                    else:
                        return base[obj].replace('{APP_DIR}', app_directory.replace(os.sep, '/'))
            else:
                return None
    except Exception:
        traceback.print_exc()
        return None


plugin_package_app_types = ['library', 'reader', 'editor']
plugin_package_schema = {
    "$id": "https://example.com/entry-schema",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "description": "JSON Schema for package file",
    "type": "object",
    "properties": {
        "context": {
            "type": "object",
            "properties": {
                "app": {"type": "string"},
                "archetype": {"type": "string"},
                "interfaces": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "properties": {
                            "archetype": {"type": "string"},
                            "target": {"type": "string"},
                            "restriction": {"type": "string"},
                            "label": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "lang": {"type": "string"},
                                        "content": {"type": "string"}
                                    },
                                    "required": ["lang", "content"]
                                }
                            }
                        },
                        "required": ["archetype", "target", "restriction", "label"]
                    },
                    "uniqueItems": True
                },
                "commands": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "array",
                        "minItems": 1,
                        "items": {"type": "string"},
                        "uniqueItems": True
                    },
                    "uniqueItems": True
                }
            },
            "required": ["app", "archetype", "interfaces", "commands"]
        },
        "settings": {
            "type": "array",
            "minItems": 0,
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "label": {
                        "type": "array",
                        "minItems": 0,
                        "items": {
                            "type": "object",
                            "properties": {
                                "lang": {"type": "string"},
                                "content": {"type": "string"}
                            },
                            "required": ["lang", "content"]
                        }
                    },
                    "archetype": {"type": "string"},
                    "value": {"type": ["string", "number", "boolean"]},
                    "min": {"type": "number"},
                    "max": {"type": "number"}
                },
                "required": ["name", "label", "archetype", "value"]
            },
            "uniqueItems": True
        },
        "manifest": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string"},
            "uniqueItems": True
        }
    },
    "required": ["context", "settings", "manifest"]
}


def load_plugins():
    global app_directory, app_user_directory, env_vars
    try:
        schema = plugin_package_schema
        settings = QtCore.QSettings(app_editor, app_name)
        directory = app_user_directory + os.sep + "imports" + os.sep + "plugins"

        try:
            if debug is True:
                with open(app_directory + os.sep + "doc" + os.sep + "packages" + os.sep + "plugin" + os.sep + 'example.package.json_schema', 'wt', encoding='utf8') as file:
                    file.write(json.dumps(schema, indent=4))
        except Exception:
            traceback.print_exc()

        ext = "json"
        env_vars['plugins'].clear()
        for root, directories, files in os.walk(directory, topdown=False):
            for name in directories:
                try:
                    print('plugin:', name)
                    dir = directory + os.sep + name
                    print('dir:', dir)
                    package_file = dir + os.sep + 'package.json'
                    print('package_file:', package_file)

                    if os.path.isfile(package_file) is True:
                        fp = open(package_file, "rt", encoding="utf8")
                        content = fp.read()
                        fp.close()
                        content = content.replace('{plugin_dir}', dir.replace(os.sep, os.sep + os.sep))\
                            .replace('{os.sep}', os.sep + os.sep)

                        # test id valid JSON
                        decoder = json.decoder.JSONDecoder()
                        tab = decoder.decode(content)
                        # test package JSON schema
                        jsonschema.validate(instance=tab, schema=schema)

                        data = eval(content)
                        # print(data)
                        env_vars['plugins'][name] = data
                        env_vars['plugins'][name]['name'] = name
                        for variable in data['settings']:
                            # print('VARIABLE: ', variable)
                            value = settings.value('plugins/'+name+'/'+variable['name'], None, str)
                            # print('VARIABLE VALUE: ', value)
                            if value is not None and value != '':
                                variable['value'] = value
                            else:
                                # print('SET VALUE: ', variable['value'])
                                settings.setValue('plugins/'+name+'/'+variable['name'], variable['value'])
                except Exception:
                    traceback.print_exc()
    except Exception:
        traceback.print_exc()


def list_plugins() -> list:
    return env_vars['plugins'].copy()


def get_plugin(name: str) -> dict:
    try:
        return env_vars['plugins'][name].copy()
    except Exception:
        traceback.print_exc()
        return None


def get_plugins(app: str = None, archetype: str = None, target: str = None, restriction: str = None) -> list:
    if app is None:
        return []
    if app.strip() == '':
        return []
    if archetype is not None:
        archetype = archetype.strip()
        if archetype == '':
            archetype = None
    ret = []
    if target is not None:
        target = target.strip()
        if target == '':
            target = None
    if restriction is not None:
        restriction = restriction.strip()
        if restriction == '':
            restriction = None
    for name in env_vars['plugins']:
        if env_vars['plugins'][name]['context']['app'] == app:
            for option in env_vars['plugins'][name]['context']['interfaces']:
                ok = True
                if archetype is not None:
                    ok = False
                    if option['archetype'] == archetype:
                        ok = True
                        if target is not None:
                            ok = False
                            if target == option['target']:
                                ok = True
                        if restriction is not None:
                            ok = False
                            if restriction == option['restriction']:
                                ok = True
                if ok is True:
                    ret.append({
                        'name': name,
                        'archetype': env_vars['plugins'][name]['context']['archetype'],
                        'commands': env_vars['plugins'][name]['context']['commands'],
                        'interface': option,
                        'setting': env_vars['plugins'][name]['settings']
                    })
    return ret


def plugin_exec(name: str = None, args: dict = None) -> str:
    print('plugin_exec')
    ret = ''
    try:
        if name is None: return
        if name.strip() == '': return
        if name not in env_vars['plugins']: return
        plug = env_vars['plugins'][name.strip()]
        settings = {}
        for opt in plug['settings']:
            settings[opt['name']] = opt['value']
        if args is not None:
            for id in args:
                if id in settings or id in ['input', 'output', 'output2']:
                    settings[id] = args[id]
        for cmdl in plug['context']['commands']:
            if [':eval:', ':makedir:', ':rmdir:', ':zip:', ':return:'].__contains__(cmdl[0]) is True:
                for line in range(1, len(cmdl)):
                    for opt in settings:
                        if opt in ['input', 'output', 'output2']:
                            cmdl[line] = cmdl[line].replace('%' + opt + '%', settings[opt])
                        else:
                            cmdl[line] = cmdl[line].replace('{' + opt + '}', settings[opt])
                if cmdl[0] == ':eval:':
                    print('start eval=', cmdl[1])
                    eval(cmdl[1])
                if cmdl[0] == ':makedir:':
                    print('start makedir=', cmdl[1])
                    os.makedirs(cmdl[1])
                if cmdl[0] == ':rmdir:':
                    print('start rmdir=', cmdl[1])
                    common.files.rmDir(cmdl[1])
                if cmdl[0] == ':zip:':
                    print('start zip=', cmdl[1])
                    common.archive.deflate(cmdl[1], cmdl[2])
                if cmdl[0] == ':return:':
                    print('return=', cmdl[1])
                    ret = cmdl[1]
            else:
                for line in range(0, len(cmdl)):
                    for opt in settings:
                        if opt in ['input', 'output', 'output2']:
                            cmdl[line] = cmdl[line].replace('%' + opt + '%', settings[opt])
                        else:
                            cmdl[line] = cmdl[line].replace('{' + opt + '}', settings[opt])
                print('cdm=', cmdl)
                return_code = subprocess.call(cmdl, shell=True)
            print('- end command')
    except Exception:
        traceback.print_exc()
    return ret


load_patterns()
load_styles()
load_plugins()
