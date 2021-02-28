# eBookCollection
This application is designed for managing eBooks

## formats support
type | support | planed
------ | ------ | ------
epub 1/2/3 | X | 
cbz | X | 
cbr | X | 
pdf |  | X
mobi |  | X
txt |  | X
rtf |  | X
doc |  | X
docx |  | X

## Features
- add eBook in database
- open eBook
- modify eBook
- modify eBook metadata(support for title, series and authors)
- modify eBook storage directory if metadata updated

## Planed Features
- File conversion
- Settings window
    - Global
        - change language (implemented, unstable)
        - change style (implemented, unstable)
        - import language pack
        - import style pack
        - modify library folder
    - Metadata
        - change default eBook cover style
        - change file name eBook import template
    - Conversion
        - default module CBZ to EPUB
        - import Conversion module
        - modify parameters of Conversion modules
    - About
        - use language translation on tab content

- synchronize eBook library with mobile terminal (in a far future)
    - incompatible terminal software would only have the eBook file copied
    - compatible terminal software would have
        - full metadata information's
        - bookmark
        - cover
        - tags


## Prerequisites

Require Python >= 3.5.x
Require the following complements:
- PyQt5
- PyQtWebKit(optional)
- pysqlite3
- lxml
- six
- Beautifulsoup4
- pywin32(optional on windows)

## Installation
### Windows installer: 
Go to the Release page [Here](https://github.com/LordKBX/EbookCollection/releases), contains:
- executable with all dependencies (full version) 
- executable without dependencies (light version)

### Manualy
#### On Windows and Mac
1. Install Python >=3.5.x which you can find [here](https://www.python.org/downloads/ "Python Download Link"). Do not forget the PATH inclusion(checked by default)
2. Run
```
pip install -r [path of the application files]requirements.txt
```
#### On Linux(Ubuntu)
1. Run 
```
sudo apt-get install python3
```
2. Run
```
sudo pip3 install -r [path of the application files]requirements.txt
```

## Usage
Use the start.bat file. 
```
[path of the application files]start.bat
```
Or Run
```
python [path of the application files]main.py
```
##### If Python dir not in the PATH variable then remplace "python" by "[path of the python dir]python.exe"


#### On Linux and MacOs
```
python3 main.py
```
or use the script start.sh

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

Third party references => [here](./README-third_party.md)