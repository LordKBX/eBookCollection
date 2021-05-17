import uuid

from PyQt5 import QtCore, QtNetwork
import traceback, asyncio
import common.bdd
from contextlib import suppress
import base64
import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, _serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import common.bdd
import json
import zlib

protocols = ['HTTPS', 'TCP LINK']

class Server(QtCore.QObject):
    __threads = []
    user = None
    password = None
    BDD = None

    def __init__(self, ip: str, port: int, user: str, password: str, bddd: common.bdd.BDD):
        QtCore.QObject.__init__(self)
        addr = QtNetwork.QHostAddress(ip)
        self.user = user
        self.password = password
        self.bddd = bddd

        self.server = QtNetwork.QTcpServer()
        self.server.newConnection.connect(self.on_newConnection)
        if self.server.listen(address=addr, port=port):
            print("Server is listening on port: {}".format(port))

    def on_newConnection(self):
        while self.server.hasPendingConnections():
            print("Incoming Connection...")
            th = ThreadTCPLink(self, self.server.nextPendingConnection())
            self.__threads.append(th)


class ThreadTCPLink(QtCore.QObject):
    parent = None
    socket = None
    loop = None
    loged = False
    private_key = None
    public_key = None
    key_padding = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )

    def __init__(self, server: Server, socket: QtNetwork.QTcpSocket):
        QtCore.QObject.__init__(self)
        self.parent = server
        try:
            self.socket = socket
            self.socket.setSocketOption(QtNetwork.QTcpSocket.KeepAliveOption, QtCore.QVariant(1))
            print("Client Connected from IP {}".format(self.socket.peerAddress().toString()))
            asyncio.run(self.start())
        except Exception:
            traceback.print_exc()

    async def start(self):
        print("start")
        #self.write('|||' + protocols[1] + ' ON|||')

        while self.socket.state() == QtNetwork.QAbstractSocket.ConnectedState:
            self.socket.waitForReadyRead(300)
            msg = self.socket.readAll()
            if len(msg) > 0:
                try: msg = str(msg, 'utf-8')
                except Exception: ''
                lines = msg.split("\r\r")
                print("Client Message:", lines)
                for line in lines:
                    if len(line) <=1: continue
                    tab = line
                    print("Read <=", tab)
                    with suppress(ValueError): tab = line[line.index(':')+1:]
                    if line.startswith('ANNOUNCE:') is True:
                        self.private_key = load_pem_private_key(tab.encode('utf-8'), None, default_backend())
                        self.public_key = self.private_key.public_key()
                        self.write("KEY:OK")
                    else:
                        decrypted = self.private_key.decrypt(base64.decodebytes(line.encode('UTF-8')), self.key_padding)
                        line = decrypted.decode('UTF-8')
                        with suppress(ValueError): tab = line[line.index(':')+1:]
                        print("decrypted =", decrypted.decode('UTF-8'))

                        token = uuid.uuid4().hex.upper().replace('\n', '')
                        token_crypted = self.crypt_token(token)
                        print('token =>', token)
                        print('token_crypted =>', token_crypted)

                        if line.startswith('LOGIN:') is True:
                            js = eval(tab)
                            print("Login <=", js)
                            self.loged = False
                            if 'user' in js and 'password' in js:
                                if js['user'] == self.parent.user and js['password'] == self.parent.password:
                                    self.loged = True
                                    self.write("LOGIN:OK")
                                    continue
                            self.write("LOGIN:ERROR")
                        elif line.startswith('LIST:') is True:
                            if self.loged is False:
                                self.write("SESSION:ERROR")
                                continue
                            try:
                                data = '[]'
                                if tab == 'ALL':
                                    data = json.dumps(self.parent.bddd.get_books(no_file_path=True))
                                else:
                                    data = json.dumps(self.parent.bddd.get_books(search=tab.replace('|', ':'), no_file_path=True))
                                if len(data) == 0:
                                    self.write("LIST:ERROR")
                                else:
                                    wrl = "LIST:" + token_crypted + ':'
                                    to_enc = tab + ':' + data
                                    wrl += self.crypt(to_enc, token)
                                    self.write(wrl)
                            except Exception:
                                traceback.print_exc()
                        elif line.startswith('GET:') is True:
                            if self.loged is False:
                                self.write("SESSION:ERROR")
                                continue
                            try:
                                data = []
                                if ',' in tab:
                                    tab = tab.split(',')
                                data = self.parent.bddd.get_books(guid=tab)
                                if len(data) == 0:
                                    self.write("GET:ERROR")
                                else:
                                    wrl = "GET:" + token_crypted + ':'
                                    tdata = {
                                        'guid': data[0]['guid'],
                                        'title': data[0]['title'],
                                        'authors': data[0]['authors'],
                                        'series': data[0]['series'],
                                        'series_vol': data[0]['series_vol'],
                                        'tags': data[0]['tags'],
                                        'synopsis': data[0]['synopsis'],
                                        'cover': data[0]['cover'],
                                        'files': []
                                    }
                                    for obj in data[0]['files']:
                                        tdata['files'].append({
                                            'guid': obj['guid'],
                                            'size': obj['size'],
                                            'format': obj['format'],
                                            'editors': obj['editors'],
                                            'publication_date': obj['publication_date'],
                                            'lang': obj['lang'],
                                            'bookmark': obj['bookmark']
                                        })
                                    to_enc = tab + ':' + json.dumps(tdata)
                                    for obj in data[0]['files']:
                                        file_data = open(obj['link'], "rb").read()
                                        to_enc += ':' + base64.b64encode(file_data).decode('UTF-8')
                                    wrl += self.crypt(to_enc, token)
                                    self.write(wrl)
                            except Exception:
                                traceback.print_exc()
                        elif line.startswith('ECHO:') is True:
                            self.write("ECHO:"+self.crypt_token(line))

                        if self.loged is True:
                            ''

        print("end")

    def crypt_token(self, input_text: str):
        out = self.public_key.encrypt(input_text.encode('UTF-8'), self.key_padding)
        return base64.encodebytes(out).decode('UTF8').replace("\n", "")

    def crc_token(self, token: str):
        crc = 0
        table = {
            '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
            '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15
        }
        for letter in token:
            crc += table[letter]
        return (int)(crc / len(token))

    def crypt(self, input_text: str, token: str):
        controlT = "ABCDEF0123456789"
        controlE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

        end_token = base64.encodebytes(token.encode('UTF-8')).decode('UTF8').replace('\n', '')
        for i in range(0, len(token)):
            if token[i] not in controlT:
                print(token)
                return None

        crc_token = self.crc_token(token)
        sub_key = ""
        ctrl_size = len(controlE)
        for i in range(0, ctrl_size):
            pos = i + crc_token
            while pos >= ctrl_size:
                pos = pos - ctrl_size
                if pos < ctrl_size:
                    break
            sub_key += controlE[pos]
        print("sub_key =>", sub_key)

        pre_text = base64.encodebytes(input_text.encode('UTF-8')).decode('UTF8')
        result = ""
        for letter in pre_text:
            if letter in controlE:
                result += sub_key[controlE.find(letter)]
            else:
                result += letter

        return result.replace("\n", "")

    def write(self, msg: str, auto_flush: bool = True):
        if len(msg) <= 0: return
        if len(msg) > 99: print("Write =>", msg[0:100]+'...')
        else: print("Write =>", msg[0:100])
        try:
            if auto_flush is True:
                msg += "\r\r"
            msg = QtCore.QByteArray(msg.encode('UTF-8'))
        except Exception:
            traceback.print_exc()
        self.socket.write(msg)
