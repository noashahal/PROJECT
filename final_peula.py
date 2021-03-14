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


class ShowCapture(wx.Frame):
    def __init__(self, client, fps=15):
        wx.Frame.__init__(self, None)
        panel = wx.Panel(self, -1)
        self.client = client
        self.frame = cv2.cvtColor(None, cv2.COLOR_BGR2RGB)
        #create a grid sizer with 5 pix between each cell
        self.frame = None
        sizer = wx.GridBagSizer(5, 5)
        height, width = self.frame.shape[:2]
        self.orig_height = height
        self.orig_width = width
        self.bmp = wx.Bitmap.FromBuffer(width, height, self.frame)

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
        """
        receives video and shows
        """
        chunks = []
        start = False
        while len(chunks) < NUM_OF_CHUNKS:
            chunk = self.receive_chunk()
            if start:
                chunks.append(chunk)
            elif chunk.startswith(CODE):
                start = True

        byte_frame = b''.join(chunks)
        frame = np.frombuffer(
            byte_frame, dtype=np.uint8).reshape(HEIGHT, WIDTH, WID)

        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp.CopyFromBuffer(self.frame)
        self.ImgControl.SetBitmap(self.bmp)
        self.Update()

    def receive_chunk(self):
        """
        gets chunk from server
        """
        raw_chunk_size = b''
        raw_chunk_size_to_get = MAX_CHUNK_SIZE
        while len(raw_chunk_size) < raw_chunk_size_to_get:
            raw_chunk_size += self.client.receive_video_socket.recv(
                raw_chunk_size_to_get - len(raw_chunk_size))
        try:
            chunk_size = int(raw_chunk_size.decode())
        except Exception as e:
            print('raw chunk size is {} its length is {}'
                  .format(raw_chunk_size, len(raw_chunk_size)))
            print("exception receive chunk 1: {}".format(e))
        left = chunk_size
        chunk = b''
        try:
            while left > END:
                chunk += self.client.receive_video_socket.recv(left)
                left = left - len(chunk)
            return chunk
        except Exception as e:
            print("exception receive chunk 1: {}".format(e))
            self.client.receive_video_socket.close()


def show_video(client):
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