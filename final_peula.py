import wx
from wx.lib import statbmp
import cv2
from gui_sign_in import *
import client_call_management
from client_backup import *
CODE = b'start'
WID = 3
BUF = 512
WIDTH = 640
HEIGHT = 480
NUM_OF_CHUNKS = WIDTH * HEIGHT * WID / BUF
PANEL = -1
TIMER = 1000.
GRID = 5  # FOR GRID SIZE
DIVIDE = 2  # FOR FRAME SHAPE
START = 0
BORDER = 5


class ShowCapture(wx.Frame):
    def __init__(self, client, frame,
                 username, call_name, client_manage, fps=15):
        wx.Frame.__init__(self, None)
        print("got to show capture in final peula")
        panel = wx.Panel(self, PANEL)
        self.client = client
        self.client_manage = client_manage
        self.frame = frame
        self.username = username
        self.call_name = call_name
        # create a grid sizer with 5 pix between each cell
        sizer = wx.GridBagSizer(GRID, GRID)
        height, width = self.frame.shape[:DIVIDE]
        self.orig_height = height
        self.orig_width = width
        self.bmp = wx.Bitmap.FromBuffer(width, height, self.frame)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        end_btn = wx.Button(panel, -1, 'End Call')
        end_btn.Bind(wx.EVT_BUTTON, self.end_button)
        btn_sizer.Add(end_btn, 0)
        # create image display widgets

        self.ImgControl = statbmp.GenStaticBitmap(panel, wx.ID_ANY, self.bmp)

        # add widgets to the sizer grid
        sizer.Add(btn_sizer, (0, 7), wx.DefaultSpan,
                  wx.EXPAND | wx.CENTER, wx.ALIGN_CENTER)
        # sizer.Add(self.ImgControl,
        # (3, 0), (1, 4), wx.EXPAND | wx.CENTER | wx.LEFT | wx.BOTTOM, GRID)
        sizer.Add(self.ImgControl,
                  (3, 0), (1, 4), wx.EXPAND | wx.CENTER, GRID)

        # set the sizer and tell the Frame about the best size
        panel.SetSizer(sizer)
        sizer.SetSizeHints(self)
        panel.Layout()
        panel.SetFocus()

        self.timer = wx.Timer(self)
        self.fps = fps
        self.timer.Start(TIMER/self.fps)

        # bind timer events to the handler
        self.Bind(wx.EVT_TIMER, self.next_frame)

    def next_frame(self, event):
        """
        receives video and shows
        """
        if self.client.call_ended:
            print("final peula - call ended")
            self.timer.Stop()
            new_client = client_call_management.ClientManage(self.username)
            self.end_call(new_client)
        else:
            self.frame = self.client.get_frame()
            self.bmp.CopyFromBuffer(self.frame)
            self.ImgControl.SetBitmap(self.bmp)
            self.Update()

    def end_button(self, event):
        """
        helper because of event handler, calls end_call()
        """
        self.timer.Stop()
        self.end_call(self.client_manage)

    def end_call(self, client_manage):
        """
        call ends, gives option to go back to main window
        """
        if win32ui.MessageBox(
                "call ended. Go back to main window?",
                "call over",
                win32con.MB_YESNO) == win32con.IDYES:

            self.client.close_all()
            self.Close(True)

            # new_client = client_call_management.ClientManage(self.username)
            start_again(self.username, client_manage)
            # start_again(self.username, self.client_manage)
        else:
            self.client.close_all()
            self.Close(True)
            # sys.exit(EXIT)


def show_video(client, frame, username, call_name, client_manage):
    print("got to show video in final peula")
    app = wx.App()
    frame2 = ShowCapture(client, frame, username, call_name, client_manage)
    frame2.Show()
    app.MainLoop()


def main():
    """
    check my methods
    """
    pass


if __name__ == '__main__':
    main()
