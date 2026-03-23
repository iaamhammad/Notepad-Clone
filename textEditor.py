from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import showerror, askokcancel
from tkinter import font as tkfont
import re

# ── State ──────────────────────────────────────────────────────────────────────
filename     = None
dark_mode    = False
current_font = {"family": "Arial", "size": 12}

LIGHT = {"bg": "#ffffff", "fg": "#000000", "bar_bg": "#f0f0f0",
         "bar_fg": "#000000", "ln_bg": "#f5f5f5", "ln_fg": "#999999",
         "status_bg": "#e0e0e0", "status_fg": "#333333",
         "sel_bg": "#0078d7", "sel_fg": "#ffffff", "insert": "#000000"}
DARK  = {"bg": "#1e1e1e", "fg": "#d4d4d4", "bar_bg": "#2d2d2d",
         "bar_fg": "#cccccc", "ln_bg": "#252526", "ln_fg": "#858585",
         "status_bg": "#007acc", "status_fg": "#ffffff",
         "sel_bg": "#264f78", "sel_fg": "#ffffff", "insert": "#ffffff"}

def theme():
    return DARK if dark_mode else LIGHT

# ── File ops ───────────────────────────────────────────────────────────────────
def newFile():
    global filename
    if text.edit_modified():
        if not askokcancel("Unsaved changes", "Discard unsaved changes?"):
            return
    filename = None
    text.delete("1.0", END)
    text.edit_modified(False)
    root.title("Untitled - Editx")
    update_status()

def saveFile():
    global filename
    if not filename:
        saveAs()
    else:
        _write(filename)

def saveAs():
    global filename
    f = asksaveasfile(mode='w', defaultextension='.txt',
                      filetypes=[("Text files","*.txt"),("All files","*.*")])
    if f is None:
        return
    filename = f.name
    f.close()
    _write(filename)

def _write(path):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text.get("1.0", END).rstrip())
        text.edit_modified(False)
        root.title(f"{path} - Editx")
    except Exception as e:
        showerror("Save failed", str(e))
    update_status()

def openFile():
    global filename
    if text.edit_modified():
        if not askokcancel("Unsaved changes", "Discard unsaved changes?"):
            return
    f = askopenfile(mode='r', encoding='utf-8',
                    filetypes=[("Text files","*.txt"),("All files","*.*")])
    if f is None:
        return
    filename = f.name
    content = f.read()
    f.close()
    text.delete("1.0", END)
    text.insert("1.0", content)
    text.edit_modified(False)
    root.title(f"{filename} - Editx")
    update_line_numbers()
    update_status()

# ── Status bar ─────────────────────────────────────────────────────────────────
def update_status(event=None):
    line, col = text.index(INSERT).split(".")
    col = int(col) + 1
    content = text.get("1.0", END)
    chars = len(content) - 1
    words = len(content.split())
    statusbar.config(
        text=f"Ln {line}, Col {col}  |  {words} words  |  {chars} chars  |  UTF-8"
    )
    update_line_numbers()

# ── Line numbers ───────────────────────────────────────────────────────────────
def update_line_numbers(event=None):
    line_numbers.config(state=NORMAL)
    line_numbers.delete("1.0", END)
    total = int(text.index(END).split(".")[0]) - 1
    ln_text = "\n".join(str(i) for i in range(1, total + 1))
    line_numbers.insert("1.0", ln_text)
    line_numbers.config(state=DISABLED)
    line_numbers.yview_moveto(text.yview()[0])

def on_text_scroll(*args):
    scroll_y.set(*args)
    line_numbers.yview_moveto(text.yview()[0])

# ── Bold / Italic ──────────────────────────────────────────────────────────────
def make_bold():
    _toggle_tag("bold", (current_font["family"], current_font["size"], "bold"))

def make_italic():
    _toggle_tag("italic", (current_font["family"], current_font["size"], "italic"))

def _toggle_tag(tag, font_tuple):
    try:
        if tag in text.tag_names("sel.first"):
            text.tag_remove(tag, "sel.first", "sel.last")
        else:
            text.tag_add(tag, "sel.first", "sel.last")
            text.tag_configure(tag, font=font_tuple)
    except TclError:
        pass

# ── Font selector ──────────────────────────────────────────────────────────────
def open_font_dialog():
    dlg = Toplevel(root)
    dlg.title("Font")
    dlg.resizable(False, False)
    dlg.grab_set()
    t = theme()
    dlg.config(bg=t["bar_bg"])

    families = sorted(set(tkfont.families()))

    Label(dlg, text="Font family:", bg=t["bar_bg"], fg=t["bar_fg"]).grid(
        row=0, column=0, sticky=W, padx=10, pady=(10, 2))
    Label(dlg, text="Size:", bg=t["bar_bg"], fg=t["bar_fg"]).grid(
        row=0, column=1, sticky=W, padx=10, pady=(10, 2))

    family_lb = Listbox(dlg, listvariable=StringVar(value=families),
                        height=12, width=32, exportselection=False,
                        bg=t["bg"], fg=t["fg"], selectbackground=t["sel_bg"])
    family_lb.grid(row=1, column=0, padx=10, pady=(0, 10))
    if current_font["family"] in families:
        idx = families.index(current_font["family"])
        family_lb.selection_set(idx)
        family_lb.see(idx)

    size_var  = IntVar(value=current_font["size"])
    size_spin = Spinbox(dlg, from_=6, to=72, textvariable=size_var, width=6,
                        bg=t["bg"], fg=t["fg"])
    size_spin.grid(row=1, column=1, padx=10, sticky=N, pady=(0, 10))

    preview_lbl = Label(dlg, text="The quick brown fox", bg=t["bg"], fg=t["fg"],
                        font=(current_font["family"], current_font["size"]))
    preview_lbl.grid(row=2, column=0, columnspan=2, padx=10, pady=4)

    def refresh_preview(*_):
        sel = family_lb.curselection()
        fam = families[sel[0]] if sel else current_font["family"]
        try:
            sz = int(size_var.get())
        except:
            sz = current_font["size"]
        preview_lbl.config(font=(fam, sz))

    family_lb.bind("<<ListboxSelect>>", refresh_preview)
    size_spin.bind("<KeyRelease>", refresh_preview)

    def apply_font():
        sel = family_lb.curselection()
        fam = families[sel[0]] if sel else current_font["family"]
        try:
            sz = int(size_var.get())
        except:
            sz = current_font["size"]
        current_font["family"] = fam
        current_font["size"]   = sz
        f = (fam, sz)
        text.config(font=f)
        line_numbers.config(font=f)
        bold_btn.config(font=(fam, sz, "bold"))
        italic_btn.config(font=(fam, sz, "italic"))
        text.tag_configure("bold",   font=(fam, sz, "bold"))
        text.tag_configure("italic", font=(fam, sz, "italic"))
        dlg.destroy()

    Button(dlg, text="Apply", command=apply_font,
           bg="#0078d7", fg="white", relief=FLAT, padx=12, pady=4).grid(
           row=3, column=0, columnspan=2, pady=(4, 12))

# ── Find & Replace ─────────────────────────────────────────────────────────────
find_win = None

def open_find_replace():
    global find_win
    if find_win and find_win.winfo_exists():
        find_win.lift()
        return
    find_win = Toplevel(root)
    find_win.title("Find & Replace")
    find_win.resizable(False, False)
    t = theme()
    find_win.config(bg=t["bar_bg"])

    Label(find_win, text="Find:",    bg=t["bar_bg"], fg=t["bar_fg"]).grid(row=0, column=0, padx=10, pady=5, sticky=E)
    Label(find_win, text="Replace:", bg=t["bar_bg"], fg=t["bar_fg"]).grid(row=1, column=0, padx=10, pady=5, sticky=E)

    find_var    = StringVar()
    replace_var = StringVar()
    find_entry    = Entry(find_win, textvariable=find_var,    width=26,
                          bg=t["bg"], fg=t["fg"], insertbackground=t["insert"])
    replace_entry = Entry(find_win, textvariable=replace_var, width=26,
                          bg=t["bg"], fg=t["fg"], insertbackground=t["insert"])
    find_entry.grid(row=0, column=1, padx=10, pady=5)
    replace_entry.grid(row=1, column=1, padx=10, pady=5)
    find_entry.focus()

    match_case_var = BooleanVar()
    Checkbutton(find_win, text="Match case", variable=match_case_var,
                bg=t["bar_bg"], fg=t["bar_fg"], selectcolor=t["bg"],
                activebackground=t["bar_bg"]).grid(
                row=2, column=0, columnspan=2, sticky=W, padx=10)

    status_lbl = Label(find_win, text="", bg=t["bar_bg"], fg=t["bar_fg"])
    status_lbl.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 6))

    text.tag_configure("highlight", background="#ffff00", foreground="#000000")

    def _clear():
        text.tag_remove("highlight", "1.0", END)

    def find_all():
        _clear()
        needle = find_var.get()
        if not needle:
            return 0
        flags = 0 if match_case_var.get() else re.IGNORECASE
        content = text.get("1.0", END)
        count = 0
        for m in re.finditer(re.escape(needle), content, flags):
            text.tag_add("highlight", f"1.0+{m.start()}c", f"1.0+{m.end()}c")
            count += 1
        return count

    def do_find():
        n = find_all()
        status_lbl.config(text=f"{n} match(es) found" if n else "No matches")

    def do_replace():
        needle  = find_var.get()
        replace = replace_var.get()
        if not needle:
            return
        flags = 0 if match_case_var.get() else re.IGNORECASE
        content = text.get("1.0", END)
        new_content, n = re.subn(re.escape(needle), replace, content, flags=flags)
        if n:
            text.delete("1.0", END)
            text.insert("1.0", new_content)
            _clear()
        status_lbl.config(text=f"{n} replacement(s) made" if n else "No matches")
        update_line_numbers()
        update_status()

    find_entry.bind("<Return>", lambda e: do_find())

    def on_close():
        _clear()
        find_win.destroy()

    find_win.protocol("WM_DELETE_WINDOW", on_close)

    btn_frame = Frame(find_win, bg=t["bar_bg"])
    btn_frame.grid(row=3, column=0, columnspan=2, pady=6)
    for lbl, cmd in [("Find All", do_find), ("Replace All", do_replace)]:
        Button(btn_frame, text=lbl, command=cmd,
               bg="#0078d7", fg="white", relief=FLAT, padx=8, pady=3).pack(side=LEFT, padx=4)

# ── Dark mode ──────────────────────────────────────────────────────────────────
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
    t = theme()
    root.config(bg=t["bar_bg"])
    topbar.config(bg=t["bar_bg"])
    toolbar.config(bg=t["bar_bg"])
    for w in (file_mb, edit_mb, view_mb, format_mb):
        w.config(bg=t["bar_bg"], fg=t["bar_fg"],
                 activebackground=t["sel_bg"], activeforeground=t["sel_fg"])
    for w in (bold_btn, italic_btn, find_btn, font_btn, dark_btn):
        w.config(bg=t["bar_bg"], fg=t["bar_fg"],
                 activebackground=t["sel_bg"], activeforeground=t["sel_fg"])
    text.config(bg=t["bg"], fg=t["fg"], insertbackground=t["insert"],
                selectbackground=t["sel_bg"], selectforeground=t["sel_fg"])
    line_numbers.config(bg=t["ln_bg"], fg=t["ln_fg"])
    statusbar.config(bg=t["status_bg"], fg=t["status_fg"])
    text_frame.config(bg=t["bar_bg"])

# ── Root window ────────────────────────────────────────────────────────────────
root = Tk()
root.title("Untitled - Editx")
root.minsize(width=650, height=500)

# ── Menu bar ───────────────────────────────────────────────────────────────────
topbar = Frame(root, bg="#f0f0f0")
topbar.pack(side=TOP, fill=X)

file_mb  = Menubutton(topbar, text="File", relief=FLAT)
filemenu = Menu(file_mb, tearoff=0)
filemenu.add_command(label="New",       command=newFile,  accelerator="Ctrl+N")
filemenu.add_command(label="Open…",     command=openFile, accelerator="Ctrl+O")
filemenu.add_command(label="Save",      command=saveFile, accelerator="Ctrl+S")
filemenu.add_command(label="Save As…",  command=saveAs,   accelerator="Ctrl+Shift+S")
filemenu.add_separator()
filemenu.add_command(label="Quit",      command=root.quit)
file_mb.config(menu=filemenu)
file_mb.pack(side=LEFT, padx=(4, 2), pady=2)

edit_mb  = Menubutton(topbar, text="Edit", relief=FLAT)
editmenu = Menu(edit_mb, tearoff=0)
editmenu.add_command(label="Undo",       command=lambda: text.edit_undo(), accelerator="Ctrl+Z")
editmenu.add_command(label="Redo",       command=lambda: text.edit_redo(), accelerator="Ctrl+Y")
editmenu.add_separator()
editmenu.add_command(label="Cut",        command=lambda: text.event_generate("<<Cut>>"),   accelerator="Ctrl+X")
editmenu.add_command(label="Copy",       command=lambda: text.event_generate("<<Copy>>"),  accelerator="Ctrl+C")
editmenu.add_command(label="Paste",      command=lambda: text.event_generate("<<Paste>>"), accelerator="Ctrl+V")
editmenu.add_separator()
editmenu.add_command(label="Select All", command=lambda: text.tag_add(SEL, "1.0", END),    accelerator="Ctrl+A")
editmenu.add_separator()
editmenu.add_command(label="Find & Replace…", command=open_find_replace, accelerator="Ctrl+H")
edit_mb.config(menu=editmenu)
edit_mb.pack(side=LEFT, padx=2, pady=2)

format_mb  = Menubutton(topbar, text="Format", relief=FLAT)
formatmenu = Menu(format_mb, tearoff=0)
formatmenu.add_command(label="Font…",   command=open_font_dialog)
formatmenu.add_separator()
formatmenu.add_command(label="Bold",    command=make_bold,   accelerator="Ctrl+B")
formatmenu.add_command(label="Italic",  command=make_italic, accelerator="Ctrl+I")
format_mb.config(menu=formatmenu)
format_mb.pack(side=LEFT, padx=2, pady=2)

view_mb  = Menubutton(topbar, text="View", relief=FLAT)
viewmenu = Menu(view_mb, tearoff=0)
viewmenu.add_command(label="Toggle Dark Mode",  command=toggle_dark_mode,  accelerator="Ctrl+D")
viewmenu.add_separator()
viewmenu.add_command(label="Toggle Fullscreen", command=lambda: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
viewmenu.add_command(label="Exit Fullscreen",   command=lambda: root.attributes("-fullscreen", False))
view_mb.config(menu=viewmenu)
view_mb.pack(side=LEFT, padx=2, pady=2)

# ── Toolbar ────────────────────────────────────────────────────────────────────
toolbar = Frame(root, bg="#f0f0f0")
toolbar.pack(side=TOP, fill=X)

bold_btn   = Button(toolbar, text="B",       command=make_bold,          font=("Arial", 12, "bold"),   relief=FLAT, padx=6)
italic_btn = Button(toolbar, text="I",       command=make_italic,        font=("Arial", 12, "italic"), relief=FLAT, padx=6)
find_btn   = Button(toolbar, text="🔍 Find", command=open_find_replace,  font=("Arial", 10),           relief=FLAT, padx=6)
font_btn   = Button(toolbar, text="Font",    command=open_font_dialog,   font=("Arial", 10),           relief=FLAT, padx=6)
dark_btn   = Button(toolbar, text="🌙",      command=toggle_dark_mode,   font=("Arial", 10),           relief=FLAT, padx=6)

for btn in (bold_btn, italic_btn, find_btn, font_btn, dark_btn):
    btn.pack(side=LEFT, padx=2, pady=2)

# ── Editor area ────────────────────────────────────────────────────────────────
text_frame = Frame(root)
text_frame.pack(fill=BOTH, expand=True)

line_numbers = Text(text_frame, width=4, padx=6, takefocus=0, border=0,
                    state=DISABLED, wrap="none", font=("Arial", 12),
                    bg="#f5f5f5", fg="#999999")
line_numbers.pack(side=LEFT, fill=Y)

scroll_y = Scrollbar(text_frame, orient=VERTICAL)
scroll_y.pack(side=RIGHT, fill=Y)

text = Text(text_frame,
            wrap="word",         # word wrap ON — no horizontal scroll needed
            undo=True,
            font=("Arial", 12),
            yscrollcommand=on_text_scroll,
            padx=8, pady=4)
text.pack(side=LEFT, fill=BOTH, expand=True)

scroll_y.config(command=text.yview)

# ── Key bindings ───────────────────────────────────────────────────────────────
root.bind("<Control-n>", lambda e: newFile())
root.bind("<Control-o>", lambda e: openFile())
root.bind("<Control-s>", lambda e: saveFile())
root.bind("<Control-S>", lambda e: saveAs())
root.bind("<Control-h>", lambda e: open_find_replace())
root.bind("<Control-b>", lambda e: make_bold())
root.bind("<Control-i>", lambda e: make_italic())
root.bind("<Control-d>", lambda e: toggle_dark_mode())
root.bind("<Control-a>", lambda e: text.tag_add(SEL, "1.0", END))

text.bind("<KeyRelease>",      update_status)
text.bind("<ButtonRelease-1>", update_status)

# ── Status bar ─────────────────────────────────────────────────────────────────
statusbar = Label(root, text="Ln 1, Col 1  |  0 words  |  0 chars  |  UTF-8",
                  bd=0, anchor=W, padx=8, pady=3)
statusbar.pack(side=BOTTOM, fill=X)

# ── Init ───────────────────────────────────────────────────────────────────────
apply_theme()
update_line_numbers()

root.mainloop()