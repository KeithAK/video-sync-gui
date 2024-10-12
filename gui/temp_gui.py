import tkinter as tk
from tkinter import filedialog

root=tk.Tk()    

def browsefunc():
    filename =filedialog.askopenfilename()
    if filename:
        ent1.delete(0, tk.END) # clear any prev entries
        ent1.insert(tk.END, filename) # add this

ent1=tk.Entry(root,font=40)
ent1.grid(row=2,column=2)

b1=tk.Button(root,text="DEM",font=40,command=browsefunc)
b1.grid(row=2,column=4)

root.mainloop()

