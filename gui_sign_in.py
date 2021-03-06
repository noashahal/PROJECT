import wx
import random
import win32ui
import win32con
import pathlib
from client_call_management import *
WIDTH = 300
LENGTH = 250
START = 0
COLOR_END = 17
BORDER = 5
FILE_PATH = str(pathlib.Path().absolute())
COLORS = ['SLATE BLUE', 'AQUAMARINE', 'FOREST GREEN', 'SALMON',
          'MEDIUM ORCHID', 'SEA GREEN', 'BLUE VIOLET',
          'GOLDENROD', 'SKY BLUE', 'CORAL', 'CYAN',
          'TURQUOISE', 'PINK', 'MEDIUM AQUAMARINE', 'PLUM',
          'MEDIUM BLUE', 'PURPLE', 'YELLOW GREEN']


class GuiAll(wx.Frame):
    """
    """
    def __init__(self, e, title):
        super().__init__(e, title=title)
        self.SetSize((WIDTH, LENGTH))
        # self.Centre()
        self.lock = threading.Lock()
        # The combo box (drop down menu)
        self.combo_box = None
        # The client object
        self.client = None

        self.pnl = wx.Panel(self)  # creates
        self.SetIcon(wx.Icon(FILE_PATH + r"\Pic.png"))
        color = COLORS[random.randint(START, COLOR_END)]
        self.pnl.SetBackgroundColour(wx.Colour(color))
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
        self.client = ClientManage(username)

    def start(self):
        """
        sets sizer and shows
        """
        self.SetSizer(self.sbs)
        self.Centre()
        self.Show(True)

    def close(self):
        self.Close(True)


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
        username_sizer.Add(window=text_user, proportion=START,
                           flag=wx.ALL | wx.CENTER, border=BORDER)
        username_sizer.Add(window=self.param_user, proportion=START,
                           flag=wx.ALL | wx.CENTER, border=BORDER)

        # sign in button:
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sign_in_btn = wx.Button(self.pnl, label='Sign In')
        sign_in_btn.Bind(wx.EVT_BUTTON, self.on_signed_in)
        btn_sizer.Add(window=sign_in_btn, proportion=START,
                      flag=wx.ALL | wx.CENTER, border=BORDER)

        # size:
        self.sbs.Add(username_sizer, proportion=START,
                     flag=wx.ALL | wx.CENTER, border=BORDER)
        self.sbs.Add(btn_sizer, proportion=START,
                     flag=wx.ALL | wx.CENTER, border=BORDER)

        self.start()

    def on_signed_in(self, e):
        """
        when the user presses the send button,
        this function is called, which in turn
        generates the query by combining all parameters
        given by the user, and displays the text inside a message box.
        """
        username = self.param_user.GetValue()
        self.start_client(username)
        GuiCallOrWait(username, self.client)
        self.Close(True)


class GuiCallOrWait(GuiAll):

    def __init__(self, username, client):
        super().__init__(None, "Call Window")
        self.username = username
        self.client = client
        self.options = self.client.connected
        self.timer = wx.Timer(self)
        # self.options = self.client.connected
        self.init_ui()

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
        # wait_btn = wx.Button(self.pnl, label="wait for call")
        # wait_btn.Bind(wx.EVT_BUTTON, self.on_wait)
        # size
        call_btn_sizer.Add(window=call_btn, proportion=START,
                           flag=wx.ALL | wx.CENTER, border=BORDER)
        # call_btn_sizer.Add(window=wait_btn, proportion=START,
        # flag=wx.ALL | wx.CENTER, border=BORDER)
        self.sbs.Add(call_btn_sizer, proportion=START,
                     flag=wx.ALL | wx.CENTER, border=BORDER)
        # wait_for_call_thread = threading.Thread(target=self.on_wait)
        # wait_for_call_thread.start()

        self.Bind(wx.EVT_TIMER, self.on_wait)
        self.timer.Start(1000)

        print("GOT HERE")
        self.start()

    def on_call(self, e):
        # self.client.initiate_calling()
        # self.options = self.client.connected
        print("call or wait options: {}".format(self.options))
        GuiCallOptions(self.client, self.username)
        self.Close(True)

    def on_wait(self, e):
        """
        waits for someone to call
        """
        print("waiting")
        if self.client.being_called:

            self.timer.Stop()
            self.client.being_called = False  # for next call
            self.getting_called()
            self.Close(True)

    def getting_called(self):
        """
        when gets a call
        """
        # self.timer.Stop()
        person_calling = self.client.person_calling
        if win32ui.MessageBox(
                "{} is calling you. Do you want to answer?"
                .format(self.client.person_calling),
                "Bringgggg", win32con.MB_YESNO) == win32con.IDYES:
            self.on_answer()
        else:
            self.on_dont_answer()

    def on_answer(self):
        """
        when answer clicked
        """
        # self.Close(True)
        self.client.answer()
        self.Close(True)

    def on_dont_answer(self):
        """
        when dont answer clicked
        """
        # self.Close(True)
        self.client.dont_answer()
        GuiCallOrWait(self.username, self.client)
        # GuiCallOrWait(self.username)


class GuiCallOptions(GuiAll):

    def __init__(self, client, username):
        super().__init__(None, "Options Window")
        # self.text = wx.TextCtrl(self.pnl, style=wx.TE_MULTILINE)
        self.username = username
        self.client = client
        self.options = self.client.connected
        if self.username in self.options:
            self.options.remove(self.username)
        print("call options, options: {}".format(self.options))
        self.options_lstbox = wx.ListBox(
            self.pnl, choices=self.options,
            style=wx.LB_SINGLE, name="contacts")
        self.init_ui()

    def init_ui(self):
        # call options
        options_sizer = wx.BoxSizer(wx.HORIZONTAL)
        call_btn = wx.Button(self.pnl, label='Call')
        call_btn.Bind(wx.EVT_BUTTON, self.on_call)
        options_sizer.Add(window=self.options_lstbox, proportion=START,
                          flag=wx.ALL | wx.CENTER, border=BORDER)
        options_sizer.Add(window=call_btn, proportion=START,
                          flag=wx.ALL | wx.CENTER, border=BORDER)
        self.sbs.Add(options_sizer, proportion=START,
                     flag=wx.ALL | wx.CENTER, border=BORDER)
        self.start()

    def on_call(self, e):
        """
        when one option clicked
        """
        calling = self.options_lstbox.GetString(
            self.options_lstbox.GetSelection())
        print(calling)
        self.client.initiate_calling(calling)
        self.Close(True)
        GuiWait(self.username, self.client)


class GuiWait(GuiAll):
    """
    window in which waits for answer
    """
    def __init__(self, username, client):
        super().__init__(None, "Wait Window")
        self.username = username
        self.client = client
        self.timer = wx.Timer(self)
        self.init_ui()

    def init_ui(self):
        text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        wait_text = wx.StaticText(self.pnl, label='Waiting For Answer....')
        text_sizer.Add(window=wait_text, proportion=START,
                       flag=wx.ALL | wx.CENTER, border=BORDER)
        self.sbs.Add(text_sizer, proportion=START,
                     flag=wx.ALL | wx.CENTER, border=BORDER)
        # wait_for_answer_thread =
        # threading.Thread(target=self.on_wait_for_answer)
        # wait_for_answer_thread.start()

        self.Bind(wx.EVT_TIMER, self.on_wait_for_answer)
        self.timer.Start(1000)
        self.start()

    def on_wait_for_answer(self, e):
        """
        waits for someone to call
        """
        print("waiting")
        if not self.client.answered_call:
            print("waiting for answer")
        else:
            # print('this is the error :)')
            self.client.answered_call = False  # for next call
            self.timer.Stop()
            self.Close(True)
            if self.client.answered:  # if answered, starts call
                self.client.start_call(self.client.chosen_contact)
            else:
                self.didnt_answer_window()

    def didnt_answer_window(self):
        """
        if user didnt answer, gives 2 options
        back to main window or disconnect
        """
        if win32ui.MessageBox(
                "{} didnt answer :( go back to main window?".format(self.client.chosen_contact),
                "didnt answer!!", win32con.MB_YESNO) == win32con.IDYES:

            GuiCallOrWait(self.username, self.client)
        else:
            self.client.close()
            self.Close(True)


def start_again(username, client):
    """
    starts again after ending call
    """
    GuiCallOrWait(username, client)
    print("starts again")


def main():
    """
    begins an app loop,
    creates a GUI.
    when user quits, ends loop.
    """
    ex = []
    ex = wx.App(None)
    # ex = wx.App()
    GuiSignIn()
    ex.MainLoop()
    # del ex


if __name__ == '__main__':
    main()
