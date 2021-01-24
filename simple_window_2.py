
import wx


class Example2(wx.Frame):

    def __init__(self, *args, **kw):
        super(Example2, self).__init__(*args, **kw)

        self.init_ui()

    def init_ui(self):

        pnl = wx.Panel(self)
        callButton = wx.Button(pnl, label='Call', pos=(20, 20))

        callButton.Bind(wx.EVT_BUTTON, self.OnClose)

        self.SetSize((350, 250))
        self.SetTitle('wx.Button 2')
        self.Centre()

    def OnClose(self, e):

        self.Close(True)


def main():

    app = wx.App()
    ex = Example2(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()  