from pydoc import text
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import showerror

filename = None

def newFile():
    global filename
    filename = "Untitled"
    text.delete(0.0, END)
    update_status()

def saveFile():
    global filename
    if not filename:
        saveAs()
    else:
        t = text.get(0.0, END)
        with open(filename, 'w') as f:
            f.write(t)
    update_status()

def saveAs():
    global filename
    f = asksaveasfile(mode='w', defaultextension='.txt')
    if f is None:
        return
    filename = f.name
    t = text.get(0.0, END)
    try:
        f.write(t.rstrip())
        f.close()
    except:
        showerror(title="Oops!", message="Unable to save file...")
    update_status()

def openFile():
    global filename
    f = askopenfile(mode='r')
    if f is None:
        return
    filename = f.name
    t = f.read()
    text.delete(0.0, END)
    text.insert(0.0, t)
    f.close()
    update_status()

def update_status(event=None):
    line, col = text.index(INSERT).split(".")
    chars = len(text.get(0.0, END)) - 1
    statusbar.config(
        text=f"Ln {line}, Col {col} | {chars} characters | UTF-8 | Plain text"
    )

root = Tk()
root.title("Editx")
root.minsize(width=400, height=400)

frame = Frame(root)
frame.pack(fill=BOTH, expand=True)

scroll_y = Scrollbar(frame, orient=VERTICAL)
scroll_x = Scrollbar(frame, orient=HORIZONTAL)

text = Text(frame, wrap="none", undo=True,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set)

scroll_y.config(command=text.yview)
scroll_y.pack(side=RIGHT, fill=Y)

scroll_x.config(command=text.xview)
scroll_x.pack(side=BOTTOM, fill=X)

text.pack(fill=BOTH, expand=True)

# update status bar when typing/moving cursor
text.bind("<KeyRelease>", update_status)
text.bind("<ButtonRelease-1>", update_status)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label="New", command=newFile)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_command(label="Save As", command=saveAs)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

# Status bar at the bottom
statusbar = Label(root, text="Ln 1, Col 0 | 0 characters | UTF-8 | Plain text", bd=1, relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

root.config(menu=menubar)
root.mainloop()