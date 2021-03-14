import wx
from wx.lib import statbmp
import cv2
import numpy as np
import os
import traceback


class ShowCapture(wx.Frame):
    def __init__(self, capture, fps=15):
        wx.Frame.__init__(self, None)
        panel = wx.Panel(self, -1)

        #create a grid sizer with 5 pix between each cell
        sizer = wx.GridBagSizer(5, 5)
        self.capture = capture
        ret, frame = self.capture.read()

        height, width = frame.shape[:2]
        self.orig_height = height
        self.orig_width = width

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.bmp = wx.BitmapFromBuffer(width, height, frame)

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

        #start a timer that's handler grabs a new frame and updates the image widgets
        self.timer = wx.Timer(self)
        self.fps = fps
        self.timer.Start(1000./self.fps)

        #bind timer events to the handler
        self.Bind(wx.EVT_TIMER, self.NextFrame)

    def NextFrame(self, event):
        ret, self.orig_frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(self.orig_frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.ImgControl.SetBitmap(self.bmp)


capture = cv2.VideoCapture(0)  # video capture
app = wx.App()
frame = ShowCapture(capture)
frame.Show()
app.MainLoop()