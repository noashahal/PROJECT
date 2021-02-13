import wx
from client_call_management import *
# from simple_window_2 import *
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
        # self.Centre()

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

        self.start()

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
        self.username = username
        self.start_client(username)
        self.options = self.client.connected
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
        wait_btn = wx.Button(self.pnl, label="wait for call")
        wait_btn.Bind(wx.EVT_BUTTON, self.on_wait)
        # size
        call_btn_sizer.Add(window=call_btn, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        call_btn_sizer.Add(window=wait_btn, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        self.sbs.Add(call_btn_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)

        self.start()

    def on_call(self, e):
        # self.client.initiate_calling()
        # self.options = self.client.connected
        print("call or wait options: {}".format(self.options))
        GuiCallOptions(self.client, self.username)
        self.Close(True)

    def on_wait(self, e):
        print("waiting")
        while not self.client.being_called:
            time.sleep(TIME_SLEEP)
            print("waiting for call")
        GuiGettingCalled(self.client, self.username)
        self.close()

        # wait_for_call_thread = threading.Thread(target=self.check_if_call)
        # wait_for_call_thread.start()
        # self.Close(True)

    def check_if_call(self, e):
        while self.client.being_called:
            GuiGettingCalled(self.client, self.username)


class GuiCallOptions(GuiAll):

    def __init__(self, client, username):
        super().__init__(None, "Options Window")
        # self.text = wx.TextCtrl(self.pnl, style=wx.TE_MULTILINE)
        self.client = client
        self.username = username
        options = self.client.connected
        if self.username in options:
            options.remove(self.username)
        print("call options, options: {}".format(options))
        self.options_lstbox = wx.ListBox(self.pnl, choices=options, style=wx.LB_SINGLE, name="contacts")
        self.init_ui()

    def init_ui(self):
        # call options
        options_sizer = wx.BoxSizer(wx.HORIZONTAL)
        call_btn = wx.Button(self.pnl, label='Call')
        call_btn.Bind(wx.EVT_BUTTON, self.on_call)
        options_sizer.Add(window=self.options_lstbox, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        options_sizer.Add(window=call_btn, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        self.sbs.Add(options_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        self.start()

    def on_call(self, e):
        """
        when one option clicked
        """
        calling = self.options_lstbox.GetString(self.options_lstbox.GetSelection())
        print(calling)
        GuiWait()
        #self.client.initiate_calling(calling)
        answered_thread = threading.Thread(target=self.answered_call)
        answered_thread.start()
        self.Close(True)

    def answered_call(self):
        """
        checks if client answered
        """
        while not self.client.answered_call:
            time.sleep(TIME_SLEEP)
            print("waiting for answer")
        if self.client.answer:
            self.client.initiate_calling()
        else:
            GuiCallOrWait(self.username)


class GuiWait(GuiAll):
    """
    window in which waits for answer
    """
    def __init__(self):
        super().__init__(None, "Wait Window")
        self.init_ui()

    def init_ui(self):
        text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        wait_text = wx.StaticText(self.pnl, label='Waiting For Answer....')
        text_sizer.Add(window=wait_text, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        self.sbs.Add(text_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)

        self.start()


class GuiGettingCalled(GuiAll):
    """
    window which opens when getting called
    """
    def __init__(self, client, username):
        super().__init__(None, title="BRINGGGGG")
        self.username = username
        self.client = client
        # person calling this user
        self.person_calling = self.client.person_calling

        # text:
        text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = str(self.person_calling) + " is calling"
        wait_text = wx.StaticText(self.pnl, label=label)
        text_sizer.Add(window=wait_text, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        # buttons:
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # call button
        answer_btn = wx.Button(self.pnl, label="answer")
        answer_btn.Bind(wx.EVT_BUTTON, self.on_answer)
        # wait for call button
        dont_answer_btn = wx.Button(self.pnl, label="dont")
        dont_answer_btn.Bind(wx.EVT_BUTTON, self.on_dont_answer)
        btn_sizer.Add(window=answer_btn, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        btn_sizer.Add(window=dont_answer_btn, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        # sizers:
        self.sbs.Add(text_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        self.sbs.Add(btn_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)

        self.start()

    def on_answer(self, e):
        """
        when answer clicked
        """
        self.Close(True)
        self.client.answer()
        # GuiEnd(self.client)

    def on_dont_answer(self, e):
        """
        when dont answer clicked
        """
        self.close()
        GuiCallOrWait(self.username)
        self.client.dont_answer()


class GuiEnd(GuiAll):
    """
       window which opens when getting called
       """

    def __init__(self, client):
        super().__init__(None, title="call")

        self.client = client
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        end_btn = wx.Button(self.pnl, label="end call")
        end_btn.Bind(wx.EVT_BUTTON, self.on_end)
        btn_sizer.Add(window=end_btn, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)
        self.sbs.Add(btn_sizer, proportion=START, flag=wx.ALL | wx.CENTER, border=BORDER)

        self.start()

    def on_end(self, e):
        """
        when wants to end call
        """
        self.client.end_call()


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
