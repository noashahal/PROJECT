import wx
from wx.lib import statbmp
import cv2
from client_backup import *
CODE = b'start'
WID = 3
BUF = 512
WIDTH = 640
HEIGHT = 480
NUM_OF_CHUNKS = WIDTH * HEIGHT * WID / BUF
PANEL = -1
TIMER = 1000.

class ShowCapture(wx.Frame):
    def __init__(self, client, frame, fps=15):
        wx.Frame.__init__(self, None)

        panel = wx.Panel(self, PANEL)
        self.client = client
        self.frame = frame

        #create a grid sizer with 5 pix between each cell
        sizer = wx.GridBagSizer(5, 5)
        height, width = self.frame.shape[:2]
        self.orig_height = height
        self.orig_width = width
        self.bmp = wx.Bitmap.FromBuffer(width, height, self.frame)

        self.dummy_element = wx.TextCtrl(panel, PANEL, '')
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
        self.timer.Start(TIMER/self.fps)

        #bind timer events to the handler
        self.Bind(wx.EVT_TIMER, self.next_frame)

    def next_frame(self, event):
        """
        receives video and shows
        """
        self.frame = self.client.get_frame()
        self.bmp.CopyFromBuffer(self.frame)
        self.ImgControl.SetBitmap(self.bmp)
        self.Update()


def show_video(client, frame):
    app = wx.App()
    frame2 = ShowCapture(client, frame)
    frame2.Show()
    app.MainLoop()


def main():
    """
    check my methods
    """
    pass


if __name__ == '__main__':
    main()
