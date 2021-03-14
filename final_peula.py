import wx
from wx.lib import statbmp
import cv2
from rec_video_client import *


class ShowCapture(wx.Frame):
    def __init__(self, client, fps=15):
        wx.Frame.__init__(self, None)
        panel = wx.Panel(self, -1)
        self.client = client
        self.frame2 = cv2.cvtColor(self.client.frame["frame"], cv2.COLOR_BGR2RGB)
        #create a grid sizer with 5 pix between each cell
        sizer = wx.GridBagSizer(5, 5)
        height, width = client.frame["frame"].shape[:2]
        self.orig_height = height
        self.orig_width = width
        self.bmp = wx.Bitmap.FromBuffer(width, height, self.frame2)

        self.dummy_element = wx.TextCtrl(panel, -1, '')
        self.dummy_element.Hide()

        #create image display widgets
        self.ImgControl = statbmp.GenStaticBitmap(panel, wx.ID_ANY, self.bmp)

        #add image widgets to the sizer grid
        sizer.Add(self.ImgControl, (3, 0), (1, 4), wx.EXPAND|wx.CENTER|wx.LEFT|wx.BOTTOM, 5)

        #set the sizer and tell the Frame about the best size
        panel.SetSizer(sizer)
        sizer.SetSizeHints(self)
        panel.Layout()
        panel.SetFocus()

        self.timer = wx.Timer(self)
        self.fps = fps
        self.timer.Start(1000./self.fps)

        #bind timer events to the handler
        self.Bind(wx.EVT_TIMER, self.next_frame)

    def next_frame(self, event):
        #print("hey")
        self.frame2 = cv2.cvtColor(self.client.frame["frame"], cv2.COLOR_BGR2RGB)
        #self.Show()
        self.bmp.CopyFromBuffer(self.frame2)
        self.ImgControl.SetBitmap(self.bmp)
        self.Update()


def show(client):
    app = wx.App()
    frame2 = ShowCapture(client)
    frame2.Show()
    app.MainLoop()


def main():
    """
    check my methods
    """


if __name__ == '__main__':
    main()