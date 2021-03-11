import wx

class StaticTextFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Static Text Example', size=(400, 300))
        panel = wx.Panel(self, -1)
        wx.StaticText(panel, -1, "This is an example of static text", (100, 10))
        center = wx.StaticText(panel, -1, "align center", (100, 50), (160, -1), wx.ALIGN_CENTER)
        center.SetForegroundColour('white')
        center.SetBackgroundColour('black')


app = wx.PySimpleApp()
frame = StaticTextFrame()
frame.Show()
app.MainLoop()