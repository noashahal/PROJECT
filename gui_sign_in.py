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
        #self.Centre()

        # The combo box (drop down menu)
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

    def start_client(self, username):
        """
        starts client when signs in
        """
        self.client = Client(username)


class GuiSignIn(GuiAll):
    """
    initiates ui
    """
    def __init__(self):
        super().__init__(None, "Sign In")
        self.param_user = wx.TextCtrl(self.pnl)  # username panel
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

        self.SetSizer(self.sbs)
        self.Centre()
        self.Show(True)

    def on_signed_in(self, e):
        """
        when the user presses the send button,
        this function is called, which in turn
        generates the query by combining all parameters
        given by the user, and displays the text inside a message box.
        """
        username = self.param_user.GetValue()
        GuiCallOrWait(username)
        self.Close(True)


class GuiCallOrWait(GuiAll):

    def __init__(self, username):
        super().__init__(None, "Call Window")
        self.start_client(username)
        self.init_ui()
        self.options = []

    def init_ui(self):
        """
        call window
        options for calling or waiting for a call
        """
        # buttons
        call_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # call button
        call_btn = wx.Button(self.pnl, label="make call")
        call_btn.Bind(wx.EVT_BUTTON, self.on_call)
        # wait for call button
        wait_btn = wx.Button(self.pnl, label="wait for call")
        wait_btn.Bind(wx.EVT_BUTTON, self.on_wait)
        # size
        call_btn_sizer.Add(window=call_btn, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        call_btn_sizer.Add(window=wait_btn, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        self.sbs.Add(call_btn_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)

        self.SetSizer(self.sbs)
        self.Centre()
        self.Show(True)

    def on_call(self, e):
        self.client.initiate_calling()
        self.options = self.client.connected
        GuiCallOptions(self.options)
        self.Close(True)

    def on_wait(self, e):
        self.Close(True)


class GuiCallOptions(GuiAll):

    def __init__(self, options):
        super().__init__(None, "Options Window")
        self.text = wx.TextCtrl(self.pnl, style=wx.TE_MULTILINE)
        self.init_ui(options)

    def init_ui(self, options):
        # call options
        options_sizer = wx.BoxSizer(wx.HORIZONTAL)
        options_lstbox = wx.ListBox(self.pnl, size=(100, -1), choices=options, style=wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.on_list_box, options_lstbox)
        options_sizer.Add(window=options_lstbox, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        options_sizer.Add(window=self.text, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        self.sbs.Add(options_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        self.SetSizer(self.sbs)
        self.Centre()
        self.Show(True)

    def on_list_box(self, e):
        self.text.AppendText("Current selection:"+e.GetEventObject().GetStringSelection()+"\n")


def main():
    """
    begins an app loop,
    creates a GUI.
    when user quits, ends loop.
    """
    ex = wx.App()
    GuiSignIn()
    ex.MainLoop()


if __name__ == '__main__':
    main()
