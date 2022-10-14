import socket
import wx
import os


class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='FTP-Client mini v1')
        
        panel = wx.Panel(self)
        self.SetSize((1225,850))
        
        st1 = wx.StaticText(panel, label='Имя файла(File name)', pos=(5, 380))
        self.text_ctrl = wx.TextCtrl(panel, pos=(130, 375), size = (300, 22))
        
        client_btn = wx.Button(panel, label='Refresh user path', pos=(550, 75))
        client_btn.Bind(wx.EVT_BUTTON, self.on_press_client)
        
        list_btn = wx.Button(panel, label='Обновить(LIST)', pos=(550, 125))
        list_btn.Bind(wx.EVT_BUTTON, self.on_press_list)
        
        stor_btn = wx.Button(panel, label='<- Загрузить на сервер(STOR)', pos=(520, 175))
        stor_btn.Bind(wx.EVT_BUTTON, self.on_press_stor)
        
        retr_btn = wx.Button(panel, label='Скачать с сервера(RETR) ->', pos=(520, 225))
        retr_btn.Bind(wx.EVT_BUTTON, self.on_press_retr)
        
        st2 = wx.StaticText(panel, label='Папка сервера(Server path)', pos=(5, 20))
        self.text_s = wx.TextCtrl(panel,style = wx.TE_MULTILINE, pos = (5, 40), size = (480, 300))
        
        st3 = wx.StaticText(panel, label='Папка пользователя(User path)', pos=(730, 20))
        self.text_c = wx.TextCtrl(panel,style = wx.TE_MULTILINE, pos = (725, 40), size = (480, 300))
        
        st4 = wx.StaticText(panel, label='Консоль(Logs)', pos=(5, 480))
        self.text = wx.TextCtrl(panel,style = wx.TE_MULTILINE, pos = (5, 500), size = (1200, 300))
        self.Show()
        
    def on_press_list(self, event):
        data = stablish_connection("list", "")
        self.text_s.Clear()
        for item in data:
            self.text_s.AppendText(str(item) + '\n')
    
    def on_press_stor(self, event):
        filename = self.text_ctrl.GetValue()
        stablish_connection("stor", filename)
        
    def on_press_retr(self, event):
        filename = self.text_ctrl.GetValue()
        stablish_connection("retr", filename)
        
    def on_press_client(self, event):
        directory = os.listdir('./ClientPATH/')
        self.text_c.Clear()
        for item in directory:
            self.text_c.AppendText(str(item) + '\n')
            



def list_cmd(s):
    s.send("list".encode(FORMAT))
    frame.text.AppendText("[LIST]-> Запрос файлов с сервера . . .\n")
    data = s.recv(SIZE).decode(FORMAT).split()
    frame.text.AppendText("[LIST RECIEVED]-> Файлы успешно получены!\n")
    return data


def retr_cmd(s, filename):
    s.send("RETR {}".format(filename).encode(FORMAT))
    frame.text.AppendText("[RETR {}]-> отправка файла . . .\n".format(filename))
    data = s.recv(SIZE).decode(FORMAT)
    frame.text.AppendText("[DATA RECIEVED]-> Отправка завершина!\n")
    file = open('./ClientPATH/{}'.format(filename), 'w')
    file.write(data)
    file.close()


def stor_cmd(s, filename):
    s.send("STOR {}".format(filename).encode(FORMAT))
    frame.text.AppendText("[STOR {}]-> Загрузка файла на сервер . . .\n".format(filename))
    file = open('./ClientPATH/{}'.format(filename), 'r')
    data = file.read()
    s.send(data.encode(FORMAT))
    frame.text.AppendText("[DATA SENT]-> Файл успешно загружен\n")


def stablish_connection(func, filename):
    data = []
    frame.text.AppendText("\n")
    s = socket.socket()
    s.connect((IP, PORT))
    frame.text.AppendText("[CONNECTED]-> Клиент подключен к серверу.\n")
    if func == "list":
        data = list_cmd(s)
    elif func == "retr":
        retr_cmd(s, filename)
    elif func == "stor":
        stor_cmd(s, filename)
    s.close()
    frame.text.AppendText("[CONNECTION CLOSED]-> Соедининие закрыто\n")
    frame.text.AppendText("\n")
    return data



PORT = 12345
IP = '127.0.0.1'
FORMAT = 'utf-8'
SIZE = 1024
ClientPATHPATH = './ClientPATH/'



if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
    