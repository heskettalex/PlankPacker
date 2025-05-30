import tkinter as tk
from tkinter import Frame, Button, Label, Entry, RAISED, END
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.scrolledtext as st
import CutListImporter
import PackingAlgorithm
import CutListAnalyzer
from collections import Counter
from Utils import value_to_frac
import os

def open_cutList(cutList, panel, button, txt, label, error, isRequired):
    filepath = askopenfilename(filetypes=[("Text Files", ".txt"), ("All Files", "*.*")])
    if not filepath:
        return
    cutList.clear()
    try:
        cutList.update(CutListImporter.readCutList(filepath))
        error.grid_remove()
        panel.grid()
        button.grid_remove()
        txt.configure(state="normal")
        txt.delete("1.0", END)
        cutListText = ""
        for category in cutList:
            cutListText += f"{category[0]}x{category[1]}:\n"
            cut_counter = Counter(cutList[category])
            for cut, count in cut_counter.items():
                cutListText += f" - {count}x {value_to_frac(cut)}\"\n"
        txt.insert(END, cutListText)
        txt.configure(state="disabled")
        label['text'] = os.path.basename(filepath)

        if isRequired:
            btn_pack.config(state="normal")
    except Exception as e:
        print(e)
        error.grid()

def clear_cutList(cutList, panel, button, isRequired):
    panel.grid_remove()
    button.grid()
    cutList.clear()

    if isRequired:
        btn_pack.config(state="disabled")

def list_import_panel(master, title, output_list, isRequired=False, width=20, height=10, color="white"):
    frm_panel = Frame(master= master, pady=5)
    
    frm_button = Frame(master= frm_panel)
    btn_open = Button(
        master= frm_button, 
        text= title, 
        command= lambda: open_cutList(output_list, frm_txt, frm_button, txt_list, label, lbl_error, isRequired)
    )
    lbl_error = Label(
        master= frm_button,
        text= "Error: list formatted incorrectly!",
        fg="red"
    )

    frm_txt = Frame(master= frm_panel, relief= RAISED, bd= 3)

    txt_list = st.ScrolledText(
        master= frm_txt,
        width= width,
        height= height,
    )
    txt_list.configure(state= "disabled")

    frm_label = Frame(
        master= frm_txt, 
        bg=color
    )
    
    btn_close = Button(
        master= frm_label, 
        text= "X", 
        padx=4,
        bg="LightPink",
        command= lambda: clear_cutList(output_list, frm_txt, frm_button, isRequired)
    )

    label = Label(
        master= frm_label,
        text= "",
        bg=color
    )

    frm_button.grid(row=0, sticky="w")
    btn_open.grid(row=0, sticky="w")
    lbl_error.grid(row=1, sticky="w")
    lbl_error.grid_remove()

    frm_txt.grid(row=1, sticky="ew")
    frm_txt.grid_remove()
    frm_label.grid(row=0, sticky= "ew")
    btn_close.grid(column=0, row=0, sticky="w")
    label.grid(column=1, row=0, sticky="w")
    txt_list.grid(row=1, sticky= "nsew")

    return frm_panel

def pack():
    global stringOutput
    try:
        orderLength = float(ent_length.get())
        overflow = float(ent_overflow.get())
        lbl_error.pack_forget()
    except Exception as e:
        lbl_error.pack(side="bottom")
        print(e)
        return

    packedList.clear()
    packedList.update(PackingAlgorithm.packCuts(cutList, orderLength, overflow, inventoryList))
    
    stats = CutListAnalyzer.stats(packedList, orderLength, overflow)
    lbl_stats["text"] = stats
    
    stringOutput = f"{CutListAnalyzer.summary(packedList)}\n{CutListAnalyzer.printCuts(packedList)}"
    
    txt_outputList.configure(state="normal")
    txt_outputList.delete("1.0", END)
    txt_outputList.insert(END, stringOutput)

    txt_outputList.tag_configure("inventory", background= "LightCyan")
    start_idx = 1.0
    for line in stringOutput.splitlines():
        if "*" in line:
            line_start = f"{int(start_idx)}.0"
            line_end = f"{int(start_idx)}.end"
            txt_outputList.tag_add("inventory", line_start, line_end)
        start_idx = int(start_idx) + 1

    txt_outputList.configure(state="disabled")
    btn_save.config(state= "normal")

def save():
    filepath = asksaveasfilename(filetypes=[("Text Files", ".txt"), ("All Files", "*.*")])
    if not filepath:
        return
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        output_file.write(stringOutput)



def main():
    global cutList, inventoryList, packedList, stringOutput, btn_pack, txt_outputList, lbl_error, ent_length, ent_overflow, lbl_stats, btn_save
    cutList = {}
    inventoryList = {}
    packedList = {}
    stringOutput = ""
    
    window = tk.Tk()
    window.title("PlankPacker")


    window.columnconfigure(1, weight=1)
    window.columnconfigure(0, minsize=200)
    window.rowconfigure(0, minsize=700, weight=1)

    frm_input = Frame(
        master=window, 
        relief=RAISED, 
        width = 215,
        bd=5, 
        padx=5, 
        pady=5, 
        )
    frm_input.pack_propagate(False)

    Label(
        frm_input, 
        text= "Pack Settings", 
        ).pack()

    frm_cutList = list_import_panel(frm_input, "Add Cut List", cutList, True)
    frm_inventory = list_import_panel(frm_input, "Add Inventory List (Optional)", inventoryList, color="LightCyan")

    frm_length = Frame(master= frm_input, pady=5)
    ent_length = Entry(master= frm_length, width=10, border=2)
    ent_length.insert(0, "96")
    lbl_length = Label(master= frm_length, text= "Order Length")

    frm_overflow = Frame(master= frm_input, pady=5)
    ent_overflow = Entry(master= frm_overflow, width=10, border=2)
    ent_overflow.insert(0, "24")
    lbl_overflow = Label(master= frm_overflow, text= "Overflow Increment")

    lbl_error = Label(
        master = frm_input,
        text= "Error: invalid settings!",
        fg= "red"
    )

    btn_pack = Button(
        master= frm_input,
        text= "Pack",
        command= pack,
        padx=10,
        pady=5,
        bd=4,
        bg= "NavajoWhite"
    )
    btn_pack.config(state= "disabled")

    lbl_stats = Label(
        master=frm_input,
        text="\n\n\n"
    )

    frm_output = Frame(master=window)
    frm_output.columnconfigure(0, weight=1)
    frm_output.rowconfigure(1, weight=1)

    frm_save = Frame(master=frm_output)
    frm_save.columnconfigure(0, weight=1)
    lbl_output = Label(
        master= frm_save,
        text="Packing Output"
    )
    btn_save = Button(
        master= frm_save,
        text= "Save",
        command = save,
        padx=20,
        bg= "PaleGreen"
    )
    btn_save.config(state= "disabled")

    txt_outputList = st.ScrolledText(frm_output, width=50)
    txt_outputList.configure(state= "disabled")

    frm_input.grid(column=0, sticky="nsew")
    frm_cutList.pack(anchor="w")
    frm_inventory.pack(anchor="w")

    lbl_stats.pack(side="bottom")
    btn_pack.pack(side="bottom", pady=10)
    lbl_error.pack()
    lbl_error.pack_forget()

    frm_overflow.pack(side="bottom", anchor="e")
    lbl_overflow.grid(column=0, row=0, sticky="e")
    ent_overflow.grid(column=1, row=0, sticky="e")

    frm_length.pack(side="bottom", anchor="e")
    lbl_length.grid(column=0, row=0, sticky="e")
    ent_length.grid(column=1, row=0, sticky="e")

    frm_output.grid(row=0, column=1, sticky="nsew")
    frm_save.grid(row=0, sticky="ew", padx=5, pady=5)
    lbl_output.grid(column=0, row=0, columnspan=2, sticky="ew")
    btn_save.grid(column=1, row=0, sticky= "e", padx=10)
    txt_outputList.grid(row=1, sticky="nsew")

    window.mainloop()

if __name__ == "__main__":
    main()