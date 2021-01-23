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
        super(GUI, self).__init__(None, title="I Dont Know What Im Doing",
                                  size=(WIDTH, LENGTH))
        # The combo box (dropdown menu)
        self.combo_box = None
        # The client object
        self.client = None
        # panel:
        self.pnl = wx.Panel(self)  # creates panel
        sb = wx.StaticBox(self.pnl)  # sequence of items
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)  # boarder
        self.pnl.SetSizer(sbs)
        # username:
        self.username_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text_user = wx.StaticText(self.pnl, label='Username', pos=(10, 20))  # username text
        self.param_user = wx.TextCtrl(self.pnl, pos=(80, 20))  # username panel
        GUI.init_ui(self)

    def init_ui(self):
        """
        initiates UI of
        graphic UI
        """
        #self.title = ""
        #self.size = (START, START)

        self.make_menu()
        # sbs.Add(text_user)
        #sbs.Add(self.name, flag=wx.CENTRE, border=BORDER)

        self.position_all()

        cbtn = wx.Button(self.pnl, label='Call', pos=(500, 300))
        # Binds a certain method to the button, will be called when pressed
        cbtn.Bind(wx.EVT_BUTTON, self.on_call)
        wbtn = wx.Button(self.pnl, label='WAIT', pos=(700, 300))
        # Binds a certain method to the button, will be called when pressed
        wbtn.Bind(wx.EVT_BUTTON, self.wait_for_call)
        #self.client = Client("Noa")
        self.Centre()
        self.Show(True)

    def position_all(self):
        """
        position all buttons
        """
        self.username_sizer.Add(window=self.text_user, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        self.username_sizer.Add(window=self.param_user, proportion=0, flag=wx.ALL | wx.CENTER, border=10)

    def on_quit(self, e):
        """
        when the user presses the quit button,
        the function is called, ending the GUI loop
        """
        self.Close()

    def on_call(self, e):
        """
        when the user presses the send button,
        this function is called, which in tur          n
        generates the query by combining all parameters
        given by the user, and displays the text inside a message box.
        """
        # gets username
        name = self.param_user.GetValue()
        client = Client(name, True)
        self.Close(True)

    def wait_for_call(self, e):
        """
        when doesn't want to call
        """
        name = self.param_user.GetValue()
        client = Client(name, False)
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
