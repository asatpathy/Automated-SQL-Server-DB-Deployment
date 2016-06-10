# import subprocess
#
# subprocess.call('sqlcmd -S localhost -d newSQLPackage1 -i C:\\Users\\asatpathy\\Desktop\\localtestSQLServer\\NewTests\\insertNewSQLPackage1.sql', shell=True)

# from tkinter import *
# from tkinter import ttk
#
# root = Tk()
#
# tree = ttk.Treeview(root)
#
# tree["columns"] = ("one", "two")
# tree.column("one", width=100)
# tree.column("two", width=100)
# tree.heading("one", text="coulmn A")
# tree.heading("two", text="column B")
#
# tree.insert("", 0, text="Line 1", values=("1A", "1b"))
#
# id2 = tree.insert("", 1, "dir2", text="Dir 2")
# tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A", "2B"))
#
# ##alternatively:
# tree.insert("", 3, "dir3", text="Dir 3")
# tree.insert("dir3", 3, text=" sub dir 3", values=("3A", " 3B"))
#
# tree.pack()
# root.mainloop()


import string
import os
import sys
import wx
import wx.lib.agw.customtreectrl as CT

class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "CustomTreeCtrl Demo")

        custom_tree = CT.CustomTreeCtrl(self, agwStyle=wx.TR_DEFAULT_STYLE)
        root = custom_tree.AddRoot("The Root Item")

        for y in range(5):
            last = custom_tree.AppendItem(root, "item %d" % y)

            for z in range(5):
                item = custom_tree.AppendItem(last,  "item %d" % z, ct_type=1)

            self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.ItemChecked)

    def ItemChecked(self, event):
            print("Somebody checked something")
            print(event.GetSelections())

app = wx.PySimpleApp()
frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()
app.MainLoop()