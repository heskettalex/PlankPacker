import tkinter as tk
from tkinter import Frame, Button, BooleanVar, Label, Entry, RAISED, END, Canvas, Scrollbar, Checkbutton
import tkinter.font as tkfont
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
    
    order = CutListAnalyzer.summary(packedList)
    instructions = CutListAnalyzer.printCuts(packedList)
    
    txt_order.configure(state="normal")
    txt_order.delete("1.0", END)
    txt_order.insert(END, order)

    txt_instructions.configure(state="normal")
    txt_instructions.delete("1.0", END)
    txt_instructions.insert(END, instructions)

    txt_instructions.tag_configure("inventory", background= "LightCyan")
    start_idx = 1.0
    for line in instructions.splitlines():
        if "*" in line:
            line_start = f"{int(start_idx)}.0"
            line_end = f"{int(start_idx)}.end"
            txt_instructions.tag_add("inventory", line_start, line_end)
        start_idx = int(start_idx) + 1

    txt_instructions.configure(state="disabled")
    btn_save.config(state= "normal")
    visualize()


def visualize():
    cnvs_vis.delete("all")
    row = 30
    padding = 5
    bar_indent = 90
    bar_scale = 8
    bar_thickness = 0
    for category in packedList:
        thickness, width = category
        row += bar_thickness / 2 + padding + 25
        bar_thickness = width * bar_scale
        cnvs_vis.create_text(20, row, text=f"{thickness}x{width}:", anchor="w")
        plank_counter = Counter(packedList[category]).most_common()
        plank_counter = sorted(plank_counter, key=lambda x: x[0].inventory)
        first = True
        for plank, count in plank_counter:
            if first:
                row += bar_thickness / 2 + padding + 15
                first = False
            else:
                row += bar_thickness + padding
            cnvs_vis.create_text(
                80, 
                row, 
                text=f"{count}x {value_to_frac(plank.length)}\"", 
                anchor="e")
            offset = 0
            if plank.inventory:
                cut_color = "Wheat"
                outline_color = "DarkCyan"
                waste_color = "LightCyan"
            else:
                cut_color = "NavajoWhite"
                outline_color = "DimGrey"
                waste_color = "Gainsboro"
            for cut in plank.cuts:
                width = cut * bar_scale
                cnvs_vis.create_rectangle(
                    bar_indent + offset, 
                    row - bar_thickness / 2, 
                    bar_indent + offset + width, 
                    row + bar_thickness / 2, 
                    fill= cut_color, 
                    outline= outline_color,
                    width = 2
                    )
                cnvs_vis.create_text(
                    bar_indent + offset + width / 2,
                    row,
                    text=f"{value_to_frac(cut)}\"",
                    anchor="center"
                )
                offset += width
            cnvs_vis.create_rectangle(
                bar_indent + offset, 
                row - bar_thickness / 2, 
                bar_indent + offset + plank.freeStock() * bar_scale, 
                row + bar_thickness / 2, 
                fill= waste_color, 
                outline= outline_color,
                width = 2,
                )

    bounds = cnvs_vis.bbox("all")
    cnvs_vis.config(scrollregion= (0, bounds[1] - 25, bounds[2], bounds[3] + 5))

def save():
    filepath = asksaveasfilename(filetypes=[("Text Files", ".txt"), ("All Files", "*.*")])
    if not filepath:
        return
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        output_file.write(stringOutput)

def toggle_visualize():
    if checkbox_visualize.get():
        frm_vis.grid(column=1, row=0, sticky="nsew")
    else:
        frm_vis.grid_forget()

def main():
    global cutList, inventoryList, packedList, stringOutput, btn_pack, txt_order, txt_instructions, frm_vis, checkbox_visualize, cnvs_vis, lbl_error, ent_length, ent_overflow, lbl_stats, btn_save
    cutList = {}
    inventoryList = {}
    packedList = {}
    stringOutput = ""
    
    window = tk.Tk()
    window.title("PlankPacker")

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

    frm_list = Frame(master=frm_output, relief="raised", bd=3)

    frm_listTitle = Frame(master=frm_list)
    lbl_output = Label(
        master= frm_listTitle,
        text="Packing Output",
        bd=5
    )

    lbl_check = Label(master= frm_listTitle, text="Visualize Cuts")

    checkbox_visualize = BooleanVar(value=False)
    checkBtn_vis = Checkbutton(
        master= frm_listTitle,
        text="",
        variable= checkbox_visualize,
        command= toggle_visualize
    )

    txt_order = st.ScrolledText(frm_list, width=50, height=12)
    txt_order.configure(state= "disabled")

    txt_instructions = st.ScrolledText(frm_list, width=50)
    txt_instructions.configure(state= "disabled")

    btn_save = Button(
        master= frm_list,
        text= "Save",
        command = save,
        padx=20,
        bg= "PaleGreen"
    )

    btn_save.config(state= "disabled")

    frm_vis = Frame(master= frm_output, relief="raised", bd=3)

    lbl_vis = Label(
        master= frm_vis,
        text= "Cut Visualization",
        bd=5
    )

    frm_cnvs = Frame(master= frm_vis)
    cnvs_vis = Canvas(frm_cnvs, bg= "white", width=500, bd=1, relief="sunken")
    vsb = Scrollbar(frm_cnvs, orient="vertical", command= cnvs_vis.yview)
    hsb = Scrollbar(frm_cnvs, orient="horizontal", command= cnvs_vis.xview)
    cnvs_vis.configure(yscrollcommand=vsb.set)
    cnvs_vis.configure(xscrollcommand=hsb.set)
    cnvs_vis.yview_moveto(0)
    cnvs_vis.xview_moveto(0)

    def _on_mousewheel(event):
        cnvs_vis.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _bind_mousewheel(event):
        cnvs_vis.bind_all("<MouseWheel>", _on_mousewheel)
        cnvs_vis.bind_all("<Button-4>", lambda event: cnvs_vis.yview_scroll(-1, "units"))
        cnvs_vis.bind_all("<Button-5>", lambda event: cnvs_vis.yview_scroll(1, "units"))

    def _unbind_mousewheel(event):
        cnvs_vis.unbind_all("<MouseWheel>")
        cnvs_vis.unbind_all("<Button-4>")
        cnvs_vis.unbind_all("<Button-5>")

    cnvs_vis.bind("<Enter>", _bind_mousewheel)
    cnvs_vis.bind("<Leave>", _unbind_mousewheel)
    
    window.columnconfigure(0, minsize=150)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, minsize=650, weight=1)

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

    frm_output.grid(column=1, row=0, sticky="nsew")
    frm_output.columnconfigure(0, weight=0)
    frm_output.columnconfigure(1, weight=1)
    frm_output.rowconfigure(0, weight=1)

    frm_list.grid(column=0, row=0, sticky="nsew")
    frm_list.rowconfigure(0, weight=0)
    frm_list.rowconfigure(1, weight=0)
    frm_list.rowconfigure(2, weight=1)
    frm_list.columnconfigure(0, weight=1)
    
    frm_listTitle.grid(row=0, column=0, sticky="ew")
    frm_listTitle.columnconfigure(0, weight=1)
    frm_listTitle.columnconfigure(1, weight=1)
    lbl_output.grid(column=0, row=0, columnspan=2, sticky="ew")
    lbl_check.grid(column=1, row=0, sticky="e")
    checkBtn_vis.grid(column=2, row=0, sticky="e", padx=(0, 5))

    txt_order.grid(column=0, row=1, sticky="nsew")
    txt_instructions.grid(column=0, row=2, sticky="nsew", pady=10)
    btn_save.grid(column=0, row=3, sticky= "e", padx=15, pady=(0, 8))

    frm_vis.rowconfigure(1, weight=1)
    frm_vis.columnconfigure(0, weight=1)

    lbl_vis.grid(column=0, row=0)
    frm_cnvs.grid(column=0, row=1, sticky="nsew")
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    cnvs_vis.pack(side="left", fill="both", expand=True) 

    window.mainloop()

if __name__ == "__main__":
    main()