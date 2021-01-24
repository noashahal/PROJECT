import wx
from client_call_management import *
from simple_window_2 import *
WIDTH = 300
LENGTH = 250
START = 0
BORDER = 5


class GUI(wx.Frame):
    """
    initiates ui
    """
    def __init__(self):
        super(GUI, self).__init__(None, title="I Will Know What Im Doing",
                                  size=(WIDTH, LENGTH))
        # The combo box (dropdown menu)
        self.combo_box = None
        # The client object
        self.client = None
        # panel:
        self.pnl = wx.Panel(self)  # creates panel
        self.sb = wx.StaticBox(self.pnl)  # sequence of items
        self.sbs = wx.BoxSizer(wx.VERTICAL)  # boarder

        # menu:
        self.make_menu()

        # username:
        self.username_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text_user = wx.StaticText(self.pnl, label='Username')  # username text
        self.param_user = wx.TextCtrl(self.pnl)  # username panel
        self.username_sizer.Add(window=self.text_user, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        self.username_sizer.Add(window=self.param_user, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)

        # sign in button:
        self.btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sign_in_btn = wx.Button(self.pnl, label='Sign In')
        self.sign_in_btn.Bind(wx.EVT_BUTTON, self.on_signed_in)
        self.btn_sizer.Add(window=self.sign_in_btn, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)

        # size:
        self.sbs.Add(self.username_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        self.sbs.Add(self.btn_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        self.pnl.SetSizer(self.sbs)
        self.Centre()
        self.Show(True)

    def on_quit(self, e):
        """
        when the user presses the quit button,
        the function is called, ending the GUI loop
        """
        self.Close()

    def on_signed_in(self, e):
        """
        when the user presses the send button,
        this function is called, which in tur          n
        generates the query by combining all parameters
        given by the user, and displays the text inside a message box.
        """
        """
        # gets username
        name = self.param_user.GetValue()
        client = Client(name, True)
        self.Close(True)
        """
        w = Example2(None)
        w.Show()
        self.Close(True)


    def make_menu(self):
        """
        makes menu with quit
        """
        menu_bar = wx.MenuBar()  # creates a MenuBar
        file_menu = wx.Menu()  # adds menu
        menu_item = file_menu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menu_bar.Append(file_menu, 'Menu&')  # adds item to menu
        self.SetMenuBar(menu_bar)  # sets menu bar
        self.Bind(wx.EVT_MENU, self.on_quit, menu_item)  # binds quit function

def main():
    """
    begins an app loop,
    creates a GUI.
    when user quits, ends loop.
    """
    ex = wx.App()
    GUI()
    ex.MainLoop()


if __name__ == '__main__':
    main()
