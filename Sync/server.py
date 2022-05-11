import os
import time
import datetime
import urllib
from threading import Thread

from PyQt5 import QtCore, QtNetwork
import traceback, asyncio
import base64

from common.common import *
import common.bdd
import json
import Sync.book
import Sync.list
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import ssl


class Server(QtCore.QObject):
    user = None
    password = None
    bddd = None
    Session_Max_Time = 864000  # 86400 = 24h
    Sessions = {"test": {"Token": "24", "Expire": 1956528000}}  # 1956528000 = 01/01/2032
    CookiesNames = {"Session": "SyncSession", "Token": "SyncToken"}
    httpd = None
    serverName = "EbookCollection"
    thread: Thread = None

    def __init__(self, ip: str, port: int, user: str, password: str, bddd: common.bdd.BDD):
        QtCore.QObject.__init__(self)
        addr = QtNetwork.QHostAddress(ip)
        self.user = user
        self.password = password
        self.bddd = bddd
        self.ip = ip
        self.port = port

        app_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        print(app_directory+"\Sync\openssl.key")
        self.httpd = HTTPServer((ip, port), MyRequestHandler)
        try:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(app_directory+'\\Sync\\fullchain.pem', app_directory+"\\Sync\\privkey.pem")
            self.httpd.socket = ssl_context.wrap_socket(self.httpd.socket, server_side=True)

            loop = asyncio.new_event_loop()
            self.thread = Thread(target=self.Run, args=(loop, ip, port))
            self.thread.start()
        except:
            traceback.print_exc()

    def Run(self, loop, ip, port):
        print("Ho!", ip, port)
        asyncio.set_event_loop(loop)
        self.httpd.parent = self
        try:
            self.httpd.serve_forever()
        except:
            traceback.print_exc()

    def Close(self):
        self.httpd.server_close()


class MyRequestHandler(BaseHTTPRequestHandler):
    session_id = None
    session_token = None
    session_status = 0

    @staticmethod
    def parse_cookies(raw: str):
        if raw is None:
            return None
        cookies = {}
        tab = raw.split('; ')
        for cookie in tab:
            sep = cookie.split('=')
            if len(sep) > 1:
                cookies[sep[0]] = urllib.parse.unquote(sep[1])
            else:
                cookies[sep[0]] = ''
        return cookies
    
    @staticmethod
    def build_cookie_header(name: str, value: str, expire: str):
        date_time = datetime.datetime.fromtimestamp(expire)
        return {
                "name": "Set-Cookie",
                "value": name+"="+value+"; path=/; expires=" + date_time.strftime("%a, %d %b %Y %H:%M:%S")+" GMT"
            }

    def testSession(self):
        self.session_id = None
        self.session_token = None
        self.session_status = 0
        cookies = self.parse_cookies(self.headers['Cookie'])
        if cookies is not None:
            if is_in(cookies, [self.server.parent.CookiesNames["Session"]]):
                self.session_id = cookies[self.server.parent.CookiesNames["Session"]]
            if is_in(cookies, [self.server.parent.CookiesNames["Token"]]):
                self.session_token = cookies[self.server.parent.CookiesNames["Token"]]
        if self.session_id is not None:
            if is_in(self.server.parent.Sessions, [self.session_id]):
                session_data = self.server.parent.Sessions[self.session_id]
                if session_data["Expire"] <= int(time.time()):
                    self.session_status = 2
                    del self.server.parent.Sessions[self.session_id]
                elif self.session_token != session_data["Token"]:
                    self.session_status = 0
                else:
                    self.session_status = 1
            else:
                self.session_id = None
        print("Session status=> {}".format(self.session_status))
        print("Session id=> {}".format(self.session_id))

    def write(self, msg: str, error_code: int = 200, error_label: str = "OK", extra_headers: list = []):
        self.writeV2(msg, error_code, error_label, extra_headers)

    def writeV1(self, msg: str, error_code: int = 200, error_label: str = "OK", extra_headers: list = []):
        self.server_version = self.server.parent.serverName
        self.sys_version = ""
        self.send_response(error_code, error_label)
        self.send_header('Content-Type', "text/plain; charset=utf-8")
        self.send_header('Access-Control-Allow-Origin', '*')
        for header in extra_headers:
            try:
                self.send_header(header["name"], header["value"])
            except:
                traceback.print_exc()
        self.end_headers()
        self.wfile.write(msg.encode('UTF-8'))

    def writeV2(self, msg: str, error_code: int = 200, error_label: str = "OK", extra_headers: list = []):
        endMsg = msg.encode('UTF-8')
        self.server_version = self.server.parent.serverName
        self.sys_version = ""
        self.send_response(error_code, error_label)
        self.send_header('Connection', 'Keep-Alive')
        self.send_header('Keep-Alive', 'timeout=5, max=500')
        self.send_header('Content-Type', "text/plain; charset=utf-8")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', "{}".format(len(endMsg)))
        for header in extra_headers:
            try:
                self.send_header(header["name"], header["value"])
            except:
                traceback.print_exc()
        self.end_headers()
        self.wfile.write(endMsg)
        self.finish()

    @staticmethod
    def error404():
        return {"Code": 1, "Label": "Function do not exist"}, 404, "Not Found"

    @staticmethod
    def error403():
        return {"Code": 6, "Label": "Function require valid session"}, 403, "Access Forbidden"

    def do_GET(self):
        print("- - - - - - - - - - - - - - - - - -")
        print(self.server.parent.Sessions)
        print("Connexion =>", self.client_address, self.path)
        self.testSession()

        data_array = {
            "SessionStatus": self.session_status,
            "Error": {"Code": 0, "Label": "OK"}
        }
        http_error_code = 200
        http_error_label = "OK"
        headers_array = []

        request_parts = self.path.strip().strip('/').strip().split('/')
        if self.path == "/" or self.path == "/status":
            rez1 = self.server.parent.bddd.get_books()
            rez2 = self.server.parent.bddd.get_series()
            rez3 = self.server.parent.bddd.get_authors()
            data_array["Books"] = rez1.__len__()
            data_array["Series"] = rez2.__len__()
            data_array["Authors"] = rez3.__len__()
            data = json.JSONEncoder().encode(data_array)
        elif request_parts[0] in ["list", "book"]:
            data_array["Section"] = request_parts[0]
            data_array["Params"] = request_parts[1:]
            data_array["Data"] = {}
            if self.session_status == 1 or self.session_id is not None:
                if request_parts[0] == "list":
                    if request_parts.__len__() == 1:
                        data_array["Data"], data_array["Error"]["Code"], data_array["Error"]["Label"] = Sync.list.list_books(self)
                    elif request_parts[1] == "books" or request_parts[1].strip() == "":
                        if request_parts.__len__() > 2:
                            data_array["Data"], data_array["Error"]["Code"], data_array["Error"]["Label"] = Sync.list.list_books(self, request_parts[2])
                        else:
                            data_array["Data"], data_array["Error"]["Code"], data_array["Error"]["Label"] = Sync.list.list_books(self)
                    elif request_parts[1] == "authors":
                        data_array["Data"], data_array["Error"]["Code"], data_array["Error"]["Label"] = Sync.list.list_authors(self)
                    elif request_parts[1] == "series":
                        data_array["Data"], data_array["Error"]["Code"], data_array["Error"]["Label"] = Sync.list.list_series(self)
                    else:
                        data_array["Error"], http_error_code, http_error_label = self.error404()
                if request_parts[0] == "book":
                    if request_parts.__len__() > 2:
                        if request_parts[1] == "cover":
                            data_array["Data"], data_array["Error"]["Code"], data_array["Error"]["Label"] \
                                = Sync.book.get_book_cover(self, request_parts[2])
                        elif request_parts[1] == "files":
                            data_array["Data"], data_array["Error"]["Code"], data_array["Error"]["Label"] \
                                = Sync.book.get_book_files_info(self, request_parts[2])
                        elif request_parts.__len__() > 3 and request_parts[1] == "file":
                            print("HI 1")
                            try:
                                data, data_array["Error"]["Code"], data_array["Error"]["Label"] \
                                    = Sync.book.get_book_file(self, request_parts[2], request_parts[3])
                                if data is not None:

                                    self.server_version = self.server.parent.serverName
                                    self.sys_version = ""
                                    self.send_response(200)
                                    self.send_header('Connection', 'Keep-Alive')
                                    self.send_header('Keep-Alive', 'timeout=5, max=30000')
                                    self.send_header('Content-Disposition', 'attachment; filename="' + data["name"] + '"')
                                    self.send_header('Content-Type', 'application/octet-stream')
                                    self.send_header('Access-Control-Allow-Origin', '*')
                                    self.send_header('Content-Length', "{}".format(os.path.getsize(data["link"])))
                                    self.end_headers()

                                    file = open(data["link"], "rb")
                                    debug = False
                                    byte = file.read(1024)
                                    self.wfile.write(byte)
                                    while len(byte) > 0:
                                        byte = file.read(1024)
                                        self.wfile.write(byte)
                                    self.wfile.write(byte)
                                    file.close()
                                    self.finish()
                                    return
                            except Exception as err:
                                traceback.print_exc()
                            return
                        else:
                            data_array["Error"], http_error_code, http_error_label = self.error404()
                    else:
                        data_array["Error"], http_error_code, http_error_label = self.error404()
            else:
                data_array["Error"], http_error_code, http_error_label = self.error403()
            data = json.JSONEncoder().encode(data_array)
        else:
            data_array["Error"], http_error_code, http_error_label = self.error404()

        data = json.JSONEncoder().encode(data_array)
        self.write(data, http_error_code, http_error_label, headers_array)

    def do_POST(self):
        print("- - - - - - - - - - - - - - - - - -")
        print(self.server.parent.Sessions)
        print("Connexion =>", self.client_address, self.path)
        print("Headers =>", self.headers)
        self.testSession()
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print("Data =>", body)

        data_array = {
            "SessionStatus": self.session_status,
            "Error": {"Code": 0, "Label": "OK"}
        }
        http_error_code = 200
        http_error_label = "OK"
        headers_array = []

        data_body = None
        try:
            data_body = json.JSONDecoder().decode(body.decode('UTF-8'))
        except Exception as err:
            traceback.print_exc()

        request_parts = self.path.strip().strip('/').strip().split('/')
        print(request_parts)
        if request_parts[0] == "login":
            if self.session_status == 1 or self.session_id is not None:
                data_array["Error"] = {"Code": 1, "Label": "Session already active"}
            else:
                if data_body is not None:
                    if common.common.is_in(data_body, ["user", "password"]):
                        if self.server.parent.user == data_body["user"] and self.server.parent.password == data_body["password"]:
                            expire_time = int(time.time()) + self.server.parent.Session_Max_Time
                            session_id = common.common.uid()
                            session_token = common.common.uid(True) + common.common.uid(True)

                            date_time = datetime.datetime.fromtimestamp(expire_time)
                            headers_array.append(self.build_cookie_header(self.server.parent.CookiesNames["Session"], session_id, expire_time))
                            headers_array.append(self.build_cookie_header(self.server.parent.CookiesNames["Token"], session_token, expire_time))
                            self.server.parent.Sessions[session_id] = {"Token": session_token, "Expire": expire_time}
                            data_array["SessionStatus"] = 1
                        else:
                            data_array["Error"] = {"Code": 4, "Label": "Invalid Authentification Data"}
                    else:
                        data_array["Error"] = {"Code": 3, "Label": "Query Data Incomplete"}
                else:
                    data_array["Error"] = {"Code": 9, "Label": "Data body Invalid"}
        elif self.session_status == 1 or self.session_id is not None:
            if request_parts.__len__() > 2:
                if request_parts[0] == "erase":
                    if request_parts[1] == "book":
                        bookID = request_parts[2]
                        try:
                            rez = self.server.parent.bddd.delete_book(bookID)
                        except Exception as error:
                            traceback.print_exc()
                            data_array["Error"] = {"Code": 10, "Label": "Error processing request"}
                    else:
                        data_array["Error"], http_error_code, http_error_label = self.error404()
                elif request_parts[0] == "update":
                    if request_parts[1] == "book":
                        bookID = request_parts[2]
                        if request_parts.__len__() > 3:
                            fileID = request_parts[3]

                        else:
                            if data_body is not None:
                                if common.common.is_in(data_body, ["title", "authors", "series", "series_vol", "tags", "synopsis", "cover"]):
                                    try:
                                        rez = self.server.parent.bddd.update_book(bookID, "title", data_body["title"])
                                        rez = self.server.parent.bddd.update_book(bookID, "authors", data_body["authors"])
                                        rez = self.server.parent.bddd.update_book(bookID, "series", data_body["series"])
                                        rez = self.server.parent.bddd.update_book(bookID, "series_vol", data_body["series_vol"])
                                        rez = self.server.parent.bddd.update_book(bookID, "tags", data_body["tags"])
                                        rez = self.server.parent.bddd.update_book(bookID, "synopsis", data_body["synopsis"])
                                        rez = self.server.parent.bddd.update_book(bookID, "cover", data_body["cover"])
                                    except Exception as error:
                                        traceback.print_exc()
                                        data_array["Error"] = {"Code": 10, "Label": "Error processing request"}
                                else:
                                    data_array["Error"] = {"Code": 3, "Label": "Query Data Incomplete"}
                            else:
                                data_array["Error"] = {"Code": 9, "Label": "Data body Invalid"}
                    else:
                        data_array["Error"], http_error_code, http_error_label = self.error404()
                elif request_parts[0] == "insert":
                    if request_parts[1] == "book":
                        ""
                    ""
            else:
                data_array["Error"], http_error_code, http_error_label = self.error404()
        else:
            data_array["Error"], http_error_code, http_error_label = self.error403()

        data = json.JSONEncoder().encode(data_array)
        self.write(data, http_error_code, http_error_label, headers_array)
