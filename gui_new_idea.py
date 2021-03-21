# import wx
#
# import win32ui
# import win32con
# from client_call_management import *
# #from simple_window_2 import *
# WIDTH = 300
# LENGTH = 250
# START = 0
# BORDER = 5
#
#
# class GuiAll(wx.Frame):
#     """
#     """
#     def __init__(self, e, title):
#         super().__init__(e, title=title)
#         self.SetSize((WIDTH, LENGTH))
#         #self.Centre()
#         self.lock = threading.Lock()
#         # The combo box (drop down menu)
#         self.combo_box = None
#         # The client object
#         self.client = None
#
#         # panel:
#         self.pnl = wx.Panel(self)  # creates panel
#         self.sb = wx.StaticBox(self.pnl)  # sequence of items
#         self.sbs = wx.BoxSizer(wx.VERTICAL)  # boarder
#
#         # menu:
#         self.make_menu()
#
#     def make_menu(self):
#         """
#         makes menu with quit
#         """
#         menu_bar = wx.MenuBar()  # creates a MenuBar
#         file_menu = wx.Menu()  # adds menu
#         menu_item = file_menu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
#         menu_bar.Append(file_menu, 'Menu&')  # adds item to menu
#         self.SetMenuBar(menu_bar)  # sets menu bar
#         self.Bind(wx.EVT_MENU, self.on_quit, menu_item)  # binds quit function
#
#     def on_quit(self, e):
#         """
#         when the user presses the quit button,
#         the function is called, ending the GUI loop
#         """
#         self.Close()
#
#     def start(self):
#         """
#         sets sizer and shows
#         """
#         self.SetSizer(self.sbs)
#         self.Centre()
#         self.Show(True)
#
#     def close(self):
#         self.Close(True)
#
#
# class GuiRandom(wx.Frame):
#     """
#     window in which waits for answer
#     """
#     def __init__(self):
#         super().__init__(None, title="Wait Window")
#         self.SetSize((WIDTH, LENGTH))
#         # self.Centre()
#         self.lock = threading.Lock()
#         # The combo box (drop down menu)
#         self.combo_box = None
#         # The client object
#         self.client = None
#
#         # panel:
#         self.pnl = wx.Panel(self)  # creates panel
#         self.sb = wx.StaticBox(self.pnl)  # sequence of items
#         self.sbs = wx.BoxSizer(wx.VERTICAL)  # boarder
#
#         # menu:
#         self.make_menu()
#         self.init_ui()
#
#     def make_menu(self):
#         """
#         makes menu with quit
#         """
#         menu_bar = wx.MenuBar()  # creates a MenuBar
#         file_menu = wx.Menu()  # adds menu
#         menu_item = file_menu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
#         menu_bar.Append(file_menu, 'Menu&')  # adds item to menu
#         self.SetMenuBar(menu_bar)  # sets menu bar
#         self.Bind(wx.EVT_MENU, self.on_quit, menu_item)  # binds quit function
#
#     def on_quit(self, e):
#         """
#         when the user presses the quit button,
#         the function is called, ending the GUI loop
#         """
#         self.Close()
#
#     def init_ui(self):
#         print("here mf")
#         text_sizer = wx.BoxSizer(wx.HORIZONTAL)
#         wait_text = wx.StaticText(self.pnl, label='thread works bitch....')
#         text_sizer.Add(window=wait_text, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
#         self.sbs.Add(text_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
#         self.SetSizer(self.sbs)
#         self.Centre()
#         print("im here you suck")
#         self.Show(True)
#         #print("got here start crying")
#         #self.start()
#
#
# class GuiSignIn(GuiAll):
#     """
#     initiates ui
#     """
#     def __init__(self):
#         super().__init__(None, "Sign In")
#         self.param_user = wx.TextCtrl(self.pnl)  # username panel
#         self.init_ui()
#
#     def init_ui(self):
#         # username:
#         username_sizer = wx.BoxSizer(wx.HORIZONTAL)
#         text_user = wx.StaticText(self.pnl, label='Username')  # username text
#         username_sizer.Add(window=text_user, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
#         username_sizer.Add(window=self.param_user, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
#
#         # sign in button:
#         btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
#         sign_in_btn = wx.Button(self.pnl, label='Sign In')
#         sign_in_btn.Bind(wx.EVT_BUTTON, self.on_signed_in)
#         btn_sizer.Add(window=sign_in_btn, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
#
#         # size:
#         self.sbs.Add(username_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
#         self.sbs.Add(btn_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
#
#         self.start()
#
#     def on_signed_in(self, e):
#         """
#         when the user presses the send button,
#         this function is called, which in turn
#         generates the query by combining all parameters
#         given by the user, and displays the text inside a message box.
#         """
#         username = self.param_user.GetValue()
#         print(username)
#         #self.Close(True)
#         thread = threading.Thread(target=self.open)
#         thread.start()
#
#     def open(self):
#         #self.lock.acquire()
#         #thread = threading.Thread(target=GuiRandom)
#         #thread.start()
#         if win32ui.MessageBox("dude", "someone is calling", win32con.MB_YESNOCANCEL) == win32con.IDYES:
#             print("hey")
#         else:
#             print("not hey")
#         #self.lock.release()
#
#
# def main():
#     """
#     begins an app loop,
#     creates a GUI.
#     when user quits, ends loop.
#     """
#     ex = wx.App()
#     GuiSignIn()
#     #GuiRandom()
#     ex.MainLoop()
#     #del ex
#
#
# if __name__ == '__main__':
#     main()

print(1000. / 15)
