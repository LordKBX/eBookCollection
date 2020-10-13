# EbookCollection
This application is designed for managing ebooks

## Features
- add Ebook in database
## Planed Features
- modify Ebook data
- modify Ebook storage dir if metadata updated
- open ebook
- synchronize ebook library with mobile terminal
    - incompatible terminal software would only have the ebook file copied
    - compatible terminal software would have
        - full metadata infos
        - bookmark
        - cover
        - tags


### Prerequisites

Require Python >= 3.5.x
Require the followin complements:
- PyQt5
- PyQtWebKit(optional)
- pysqlite3
- lxml
- six
- Beautifulsoup4
- pywin32(optional on windows)

### Installation
#### Windows installer: 
nothing for the moment

#### Manualy
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

### Usage
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
or use the sctipt start.sh

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details