import wx
from client_call_management import *
#from simple_window_2 import *
WIDTH = 300
LENGTH = 250
START = 0
BORDER = 5


class GuiAll(wx.Frame):
    """

    """
    def __init__(self, e, title):
        super().__init__(e, title=title)
        self.SetSize((WIDTH, LENGTH))
        #self.SetTitle(title)
        self.Centre()

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

    def on_quit(self, e):
        """
        when the user presses the quit button,
        the function is called, ending the GUI loop
        """
        self.Close()


class GuiSignIn(GuiAll):
    """
    initiates ui
    """
    def __init__(self):
        super().__init__(None, "Sign In")
        self.param_user = wx.TextCtrl(self.pnl)  # username panel
        self.name = "not this"
        self.init_ui()

    def init_ui(self):
        # username:
        username_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text_user = wx.StaticText(self.pnl, label='Username')  # username text

        username_sizer.Add(window=text_user, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        username_sizer.Add(window=self.param_user, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)

        # sign in button:
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sign_in_btn = wx.Button(self.pnl, label='Sign In')
        sign_in_btn.Bind(wx.EVT_BUTTON, self.on_signed_in)
        btn_sizer.Add(window=sign_in_btn, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)

        # size:
        self.sbs.Add(username_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        self.sbs.Add(btn_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        self.pnl.SetSizer(self.sbs)
        self.Centre()
        self.Show(True)

    def on_signed_in(self, e):
        """
        when the user presses the send button,
        this function is called, which in tur          n
        generates the query by combining all parameters
        given by the user, and displays the text inside a message box.
        """
        self.name = self.param_user.GetValue()
        GuiCall()
        self.Close(True)


class GuiCall(GuiAll):

    def __init__(self, name):
        super().__init__(None, "Call")
        self.name = name
        self.init_ui()

    def init_ui(self):
        """
        call window
        options for calling
        """

        #
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        call_btn = wx.Button(self.pnl, label=self.name)
        call_btn.Bind(wx.EVT_BUTTON, self.on_close)

        # size
        btn_sizer.Add(window=call_btn, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        self.sbs.Add(btn_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)

        self.Centre()
        self.Show(True)


    def on_close(self, e):
        self.Close(True)


def main():
    """
    begins an app loop,
    creates a GUI.
    when user quits, ends loop.
    """
    ex = wx.App()
    #GuiAll(None, "sup bitch")
    GuiSignIn()
    ex.MainLoop()


if __name__ == '__main__':
    main()
