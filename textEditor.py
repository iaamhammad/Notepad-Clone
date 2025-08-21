from pydoc import text
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import showerror

filename = None
DEFAULT_FONT = ("Arial", 12)

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
root.minsize(width=600, height=600)

topbar = Frame(root, bg="#f0f0f0")
topbar.pack(side=TOP, fill=X)

# File menu as Menubutton
file_mb = Menubutton(topbar, text="File", relief=FLAT)
filemenu = Menu(file_mb, tearoff=0)
filemenu.add_command(label="New", command=newFile)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_command(label="Save As", command=saveAs)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=root.quit)
file_mb.config(menu=filemenu)
file_mb.pack(side=LEFT, padx=(4,2), pady=2)

# Edit menu as Menubutton
edit_mb = Menubutton(topbar, text="Edit", relief=FLAT)
editmenu = Menu(edit_mb, tearoff=0)
editmenu.add_command(label="Undo", command=lambda: text.edit_undo())
editmenu.add_command(label="Redo", command=lambda: text.edit_redo())
editmenu.add_separator()
editmenu.add_command(label="Cut", command=lambda: text.event_generate("<<Cut>>"))
editmenu.add_command(label="Copy", command=lambda: text.event_generate("<<Copy>>"))
editmenu.add_command(label="Paste", command=lambda: text.event_generate("<<Paste>>"))
editmenu.add_cascade(label="Edit", menu=editmenu)
edit_mb.config(menu=editmenu)
edit_mb.pack(side=LEFT, padx=2, pady=2)

# View menu as Menubutton
view_mb = Menubutton(topbar, text="View", relief=FLAT)
viewmenu = Menu(view_mb, tearoff=0)
viewmenu.add_command(label="Toggle Fullscreen", command=lambda: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
viewmenu.add_command(label="Exit Fullscreen", command=lambda: root.attributes("-fullscreen", False))
view_mb.config(menu=viewmenu)
view_mb.pack(side=LEFT, padx=2, pady=2)

# Toolbar (just for buttons)
toolbar = Frame(root, bg="#f0f0f0")
toolbar.pack(side=TOP, fill=X)

def make_bold():
    try:
        current_tags = text.tag_names("sel.first")
        if "bold" in current_tags:
            text.tag_remove("bold", "sel.first", "sel.last")
        else:
            text.tag_add("bold", "sel.first", "sel.last")
            text.tag_configure("bold", font=(DEFAULT_FONT[0], DEFAULT_FONT[1], "bold"))
    except:
        pass

bold_btn = Button(toolbar, text="B", command=make_bold, font=(DEFAULT_FONT[0], DEFAULT_FONT[1], "bold"), bg="#2d2d2d", fg="white")
bold_btn.pack(side=LEFT, padx=2, pady=2)

def make_italic():
    try:
        current_tags = text.tag_names("sel.first")
        if "italic" in current_tags:
            text.tag_remove("italic", "sel.first", "sel.last")
        else:
            text.tag_add("italic", "sel.first", "sel.last")
            text.tag_configure("italic", font=(DEFAULT_FONT[0], DEFAULT_FONT[1], "italic"))
    except:
        pass

italic_btn = Button(toolbar, text="I", command=make_italic, font=(DEFAULT_FONT[0], DEFAULT_FONT[1], "italic"), bg="#2d2d2d", fg="white")
italic_btn.pack(side=LEFT, padx=2, pady=2)

# Text area + scrollbars (in a separate frame)
text_frame = Frame(root)
text_frame.pack(fill=BOTH, expand=True)

scroll_y = Scrollbar(text_frame, orient=VERTICAL)
scroll_x = Scrollbar(text_frame, orient=HORIZONTAL)

text = Text(text_frame, wrap="none", undo=True,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            font=DEFAULT_FONT
        )
scroll_y.config(command=text.yview)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_x.config(command=text.xview)
scroll_x.pack(side=BOTTOM, fill=X)
text.pack(fill=BOTH, expand=True)

# update status bar when typing/moving cursor
text.bind("<KeyRelease>", update_status)
text.bind("<ButtonRelease-1>", update_status)

# Status bar at the bottom
statusbar = Label(root, text="Ln 1, Col 0 | 0 characters | UTF-8 | Plain text", bd=1, relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

root.mainloop()