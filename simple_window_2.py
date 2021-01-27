from gui_sign_in import *
import wx
WIDTH = 300
LENGTH = 250
START = 0
BORDER = 5


class GuiCall(GuiSignIn):

    def __init__(self):
        super(GuiSignIn, self).__init__()
        self.init_ui()

    def init_ui(self):
        pnl = wx.Panel(self)
        call_btn = wx.Button(pnl, label=self.name, pos=(20, 20))
        call_btn.Bind(wx.EVT_BUTTON, self.OnClose)

        #self.SetSize((WIDTH, LENGTH))
        self.SetTitle('Call Window')
        self.Centre()

    def OnClose(self, e):

        self.Close(True)


def main():
    app = wx.App()
    ex = GuiCall()
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
