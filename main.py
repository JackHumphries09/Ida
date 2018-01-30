from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

override = False
currentOpen = None

# Window Settings

root = Tk("Text Editor")
root.title("Ida - Untitled")
root.iconbitmap(r"logo.ico")
root.minsize(width=640, height=480)

# Main Text Object
text = ScrolledText(root)
text.pack(fill=BOTH, expand=True)

# ============================== Functions ===================================

def open():
    if messagebox.askokcancel('Open', ' Do you really want to open a file! All unsaved progress will be lost!'):
        file = filedialog.askopenfile(parent=root, mode='rb', title='Select a file to open',
                                      filetypes=(("Text files", "*.txt"),
                                                 ("Python files", "*.py;*.pyw"),
                                                 ("HTML files", "*.html;*.htm"),
                                                 ("Javascript files", "*.js"),
                                                 ("CSS files", "*.css"),
                                                 ("Ruby files", "*.rb"),
                                                 ('Perl code files', '*.pl;*.pm'),
                                                 ('Java code files', '*.java'),
                                                 ('C++ code files', '*.cpp;*.h'),
                                                 ("All files", "*.*")))

        if file != None:
            contents = file.read()
            text.delete('1.0', END)
            text.insert('1.0', contents)
            file.close()
            currentOpen = file.name
            root.title("[" + str(file.name) + "] - Ida")

def saveas():
    file = filedialog.asksaveasfile(mode='w', title='Select where to save your file.',
                                    filetypes=(  ("Text files", "*.txt"),
                                                 ("Python files", "*.py;*.pyw"),
                                                 ("HTML files", "*.html;*.htm"),
                                                 ("Javascript files", "*.js"),
                                                 ("CSS files", "*.css"),
                                                 ("Ruby files", "*.rb"),
                                                 ('Perl code files', '*.pl;*.pm'),
                                                 ('Java code files', '*.java'),
                                                 ('C++ code files', '*.cpp;*.h'),
                                                 ("All files", "*.*")))

    if file != None:
        data = text.get('1.0', END+'-1c')
        file.write(data)
        file.close()
        currentOpen = file.name
        root.title("[" + str(file.name) + "] - Ida")

def save():
    if currentOpen != None:
        data = text.get('1.0', END+'-1c')
        file = open(currentOpen, 'w')
        file.write(data)
        file.close()
    else:
        saveas()

def donothing():
    print("Error 201")
    messagebox.showerror("Error", "Currently not supported!")

def quit():
    if not override:
        if messagebox.askokcancel('Quit', ' Do you really want to quit! All unsaved progress will be lost!'):
            root.destroy()
    else:
        print("Commands Overridden")
        root.destroy()

def console():
    donothing()
    console = Tk()
    console.title(str(currentOpen) + " - Ida Console")

    text = ScrolledText(console)
    text.pack(fill=BOTH, expand=True)

    text.config(bg="black", fg="white")

    console.mainloop()

# MENU BAR ======================================================================

menubar = Menu(root)

""" ==== Menubar Cascades =====
    =========================== """

_windowmenu = Menu(menubar, tearoff=0)
_windowmenu.add_command(label="Console", command=console)

""" ====== File Bar ===========
    =========================== """
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=open)
filemenu.add_command(label="Save", command=save)
filemenu.add_command(label="Save as...", accelerator="Ctrl+S", command=saveas)
filemenu.add_command(label="Close", command=quit)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=quit)

""" ===== Edit Menu ==========
    ========================== """

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", accelerator="Ctrl+Z", command=lambda: root.focus_get().event_generate('<<Undo>>'))
editmenu.add_command(label="Redo", accelerator="Ctrl+Y", command=lambda: root.focus_get().event_generate('<<Redo>>'))
editmenu.add_separator()
editmenu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: root.focus_get().event_generate('<<Cut>>'))
editmenu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: root.focus_get().event_generate('<<Copy>>'))
editmenu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: root.focus_get().event_generate('<<Paste>>'))
editmenu.add_command(label="Delete", accelerator="Delete", command=lambda: root.focus_get().event_generate('<<Delete>>'))
editmenu.add_command(label="Select All", accelerator="Ctrl+A", command=lambda: root.focus_get().event_generate('<<SelectAll>>'))

""" ===== View Menu =========
    =========================== """

viewmenu = Menu(menubar, tearoff=0)
viewmenu.add_cascade(label="Windows...", menu=_windowmenu)

""" ===== Help Menu ===========
    =========================== """

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)

""" ===== MOUSE MENU ========
    ========================= """

mousemenu = Menu(root, tearoff=0)
mousemenu.add_command(label="Undo", command=donothing)
mousemenu.add_command(label="Redo", command=donothing)

mousemenu.add_separator()

mousemenu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: root.focus_get().event_generate('<<Cut>>'))
mousemenu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: root.focus_get().event_generate('<<Copy>>'))
mousemenu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: root.focus_get().event_generate('<<Paste>>'))
mousemenu.add_command(label="Delete", command=donothing)
mousemenu.add_command(label="Select All", accelerator="Ctrl+A", command=lambda: root.focus_get().event_generate('<<SelectAll>>')) #==!

mousemenu.add_separator()

mousemenu.add_command(label="Help Index", command=donothing)
mousemenu.add_command(label="About...", command=donothing)
""" ===== Production ========
    ========================= """

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Edit", menu=editmenu)
menubar.add_cascade(label="View", menu=viewmenu)
menubar.add_cascade(label="Help", menu=helpmenu)

def popup(event):
    mousemenu.post(event.x_root, event.y_root)

text.bind("<Button-3>", popup)

root.protocol("WM_DELETE_WINDOW", quit)
root.config(menu=menubar)
root.mainloop()
