import tkinter as tk
from tkinter import Frame, Button, BooleanVar, Label, Entry, RAISED, END, Canvas, Scrollbar, Checkbutton, PanedWindow
import tkinter.font as tkfont
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.scrolledtext as st
import CutListImporter
import PackingAlgorithm
import CutListAnalyzer
from Plank import Plank
from collections import Counter
from Utils import value_to_frac
import os

class List_Import(Frame):
    def open_list(self, open_command):
        filepath = askopenfilename(filetypes=[("Text Files", ".txt"), ("All Files", "*.*")])
        if not filepath:
            return
        self.list_variable.clear()
        try:
            self.list_variable.update(CutListImporter.readCutList(filepath))
            self.lbl_error.grid_remove()
            self.frm_txt.grid()
            self.btn_open.grid_remove()
            self.txt_list.configure(state="normal")
            self.txt_list.delete("1.0", END)
            cutListText = ""
            for category in self.list_variable:
                cutListText += f"{category[0]}x{category[1]}:\n"
                cut_counter = Counter(self.list_variable[category])
                for (length, note), count in cut_counter.items():
                    if note == "":
                        cutListText += f" - {count}x {value_to_frac(length)}\"\n"
                    else:
                        cutListText += f" - {count}x {value_to_frac(length)} ({note})\"\n"
            self.txt_list.insert(END, cutListText)


            self.lbl_title['text'] = os.path.basename(filepath)
            self.txt_list.configure(state="disabled")
            
            if open_command is not None:
                open_command()

        except Exception as e:
            print(e)
            self.lbl_error.grid()

    def clear_list(self, clear_command):
        self.frm_txt.grid_remove()
        self.btn_open.grid()
        self.list_variable.clear()

        if clear_command is not None:
            clear_command()

    def __init__(self, parent, list_variable: dict, open_command=None, clear_command=None, text="", width=38, height=10, button_fg = "Black", button_bg = "White", title_fg = "Black", title_bg = "White", list_fg= "Black", list_bg = "White"):
        Frame.__init__(self, parent)

        self.list_variable = list_variable
        self.open_command = open_command

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.frm_button = Frame(self)
        self.btn_open = Button(
            master= self.frm_button, 
            text= text, 
            command= lambda: self.open_list(open_command),
            fg = button_fg,
            bg = button_bg
        )
        self.lbl_error = Label(
            master= self.frm_button,
            text= "Error: list formatted incorrectly!",
            fg="red"
        )

        self.frm_txt = Frame(master= self, relief= RAISED, bd= 3)

        self.txt_list = st.ScrolledText(
            master= self.frm_txt,
            width= width,
            height= height,
            fg= list_fg,
            bg = list_bg
        )

        self.frm_label = Frame(
            master= self.frm_txt, 
            bg= title_bg
        )
        
        self.btn_close = Button(
            master= self.frm_label, 
            text= "X", 
            padx=4,
            bg="LightPink",
            command= lambda: self.clear_list(clear_command)
        )

        self.lbl_title = Label(
            master= self.frm_label,
            text= "",
            fg = title_fg,
            bg = title_bg
        )

        self.frm_button.grid(row=0, sticky="w")
        self.btn_open.grid(row=0, sticky="w")
        self.lbl_error.grid(row=1, sticky="w")
        self.lbl_error.grid_remove()

        self.frm_txt.grid(row=0, sticky="ew")
        self.frm_txt.grid_remove()
        self.frm_txt.rowconfigure(1, weight=1)
        self.frm_txt.columnconfigure(0, weight=1)
        
        self.frm_label.grid(row=0, sticky= "ew")
        self.btn_close.grid(column=0, row=0, sticky="w")
        self.lbl_title.grid(column=1, row=0, sticky="w")
        self.txt_list.grid(row=1, sticky= "nsew")
            
        self.txt_list.configure(state= "disabled")

def open_cutList():
    btn_pack.config(state = "normal")

def clear_cutList():
    btn_pack.config(state = "disabled")

def pack():
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

    txt_instructions.tag_configure("inventory", foreground= "DarkCyan")
    start_idx = 1.0
    for line in instructions.splitlines():
        if "*" in line:
            line_start = f"{int(start_idx)}.{line.find("- ") + 2}"
            line_end = f"{int(start_idx)}.{line.find(" =")}"
            txt_instructions.tag_add("inventory", line_start, line_end)
        start_idx = int(start_idx) + 1

    txt_instructions.configure(state="disabled")
    btn_save_spreadsheet.config(state= "normal")
    btn_save.config(state= "normal")
    visualize()

def get_fitting_font(canvas, text, max_width, max_size=9, min_size=5, font_family="Segoe UI"):
    size = max_size
    font = tkfont.Font(family=font_family, size=size)
    while size > min_size and font.measure(text) > max_width:
        size -= 1
        font = tkfont.Font(family=font_family, size=size)
    return font

def visualize():
    cnvs_vis.delete("all")
    label = checkbox_visLabel.get()
    row = 30
    padding = 5
    bar_indent = 90
    bar_scale = 5
    bar_thickness = 0
    bar_thickness = 25
    for category in packedList:
        thickness, width = category
        row += bar_thickness / 2 + padding + 25
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
            
            if plank.inventory:
                cut_color = "Wheat"
                outline_color = "DarkCyan"
                waste_color = "LightCyan"
                text_color = "DarkCyan"
            else:
                cut_color = "NavajoWhite"
                outline_color = "DimGrey"
                waste_color = "Gainsboro"
                text_color = "Black"
            
            if plank.note == "":
                cnvs_vis.create_text(
                    80, 
                    row, 
                    text=f"{count}x {value_to_frac(plank.length)}\"", 
                    anchor="e",
                    fill= text_color
                    )
            else:
                cnvs_vis.create_text(
                    80, 
                    row, 
                    text=f"{count}x {value_to_frac(plank.length)}\" ({plank.note})", 
                    anchor="e",
                    fill= text_color
                    )
            offset = 0
            for cut in plank.cuts:
                width = cut[0] * bar_scale
                cnvs_vis.create_rectangle(
                    bar_indent + offset, 
                    row - bar_thickness / 2, 
                    bar_indent + offset + width, 
                    row + bar_thickness / 2, 
                    fill= cut_color, 
                    outline= outline_color,
                    width = 2
                    )
                
                if label:
                    if cut[1] == "":
                        label_text = f"{value_to_frac(cut[0])}\""
                        font = get_fitting_font(cnvs_vis, label_text, width)
                        cnvs_vis.create_text(
                            bar_indent + offset + width / 2,
                            row,
                            text=label_text,
                            anchor="center",
                            font= font,
                        )
                    else:
                        label_text = f"{value_to_frac(cut[0])}\" ({cut[1]})"
                        font = get_fitting_font(cnvs_vis, label_text, width)
                        cnvs_vis.create_text(
                            bar_indent + offset + width / 2,
                            row,
                            text=label_text,
                            anchor="center",
                            font=font
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

def save_txt():
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", ".txt"), ("All Files", "*.*")],
        initialfile= f"{fileName[0:fileName.index(".")]}_Instructions.txt"
        )
    if not filepath:
        return
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        output_file.write(stringOutput)

def save_spreadsheet():
    filepath = asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files", ".xlsx"), ("All Files", "*.*")],
        initialfile= f"{fileName[0:fileName.index(".")]}_Instructions.xlsx"
        )
    if not filepath:
        return
    
    CutListAnalyzer.generate_spreadsheet(packedList, filepath)

def toggle_visualize():
    global last_vis_size
    if checkbox_vis.get():
        output_paned.add(frm_vis, minsize=50)
        if window.state() != "zoomed":
            output_paned.sash_place(0, frm_list.winfo_width(), 0)
        window.update_idletasks()
        req_height = window.winfo_reqheight()
        window.geometry(f"{window.winfo_width() + last_vis_size}x{req_height}")
    else:
        req_height = window.winfo_reqheight()
        last_vis_size = frm_vis.winfo_width()
        window.geometry(f"{window.winfo_width() - frm_vis.winfo_width()}x{req_height}")
        output_paned.forget(frm_vis)
        window.update_idletasks()

def main():
    global fileName, cutList, inventoryList, packedList, stringOutput, window, btn_pack, txt_order, txt_instructions, frm_list, frm_vis, output_paned, checkbox_vis, checkbox_visLabel, cnvs_vis, lbl_error, ent_length, ent_overflow, lbl_stats, btn_save, btn_save_spreadsheet, last_vis_size
    cutList = {}
    inventoryList = {}
    packedList = {}
    stringOutput = ""
    last_vis_size = 600
    fileName = ""
    
    window = tk.Tk()
    window.title("PlankPacker")
    paned = PanedWindow(window, orient="horizontal")

    frm_input = Frame(
        master=paned, 
        relief=RAISED, 
        width = 350,
        bd=5, 
        padx=5, 
        pady=5, 
        )

    lbl_input = Label(
                    frm_input, 
                    text= "Pack Settings", 
                    )

    import_cutList = List_Import(
        frm_input, 
        list_variable = cutList,
        open_command = open_cutList,
        clear_command = clear_cutList,
        text= "Add Cut List"
    )
    import_inventory = List_Import(
        frm_input, 
        list_variable = inventoryList,
        text= "Add Inventory List (Optional)",
        title_bg= "LightCyan",
        list_fg= "DarkCyan"
    )
    cnvs_settings = Canvas(frm_input)

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
        text="\n"
    )

    frm_output = Frame(master=paned)
    output_paned = PanedWindow(frm_output, orient="horizontal")

    frm_list = Frame(master=frm_output, relief="raised", bd=3)
    list_paned = PanedWindow(master=frm_list, orient="vertical")
    frm_order = Frame(master=frm_list)

    lbl_output = Label(
        master= frm_order,
        text="Packing Output",
        bd=6
    )
    
    txt_order = st.ScrolledText(frm_order, width=50, height=12)
    txt_order.configure(state= "disabled")

    frm_instructions = Frame(master=frm_list)
    txt_instructions = st.ScrolledText(frm_instructions, width=50)
    txt_instructions.configure(state= "disabled")

    frm_save = Frame(master=frm_list)
    btn_save_spreadsheet = Button(
        master= frm_save,
        text= "Save as Spreadsheet",
        command = save_spreadsheet,
        padx=10,
        bg= "PaleGreen"
    )
    btn_save_spreadsheet.config(state= "disabled")
    
    btn_save = Button(
        master= frm_save,
        text= "Save as .txt",
        command = save_txt,
        padx=10,
        bg= "White"
    )

    btn_save.config(state= "disabled")

    checkbox_vis = BooleanVar(value=False)
    checkBtn_vis = Checkbutton(
        master= frm_save,
        text="Visualize Cuts",
        variable= checkbox_vis,
        command= toggle_visualize
    )

    frm_vis = Frame(master= frm_output, relief="raised", bd=3)

    frm_visTitle = Frame(master= frm_vis)
    lbl_vis = Label(
        master= frm_visTitle,
        text= "Cut Visualization",
        bd=5
    )
    lbl_checkVisLabel = Label(
        master= frm_visTitle,
        text= "Label Cuts"
    )
    checkbox_visLabel = BooleanVar(value=True)
    checkBtn_visLabel = Checkbutton(
        master= frm_visTitle,
        text="",
        variable= checkbox_visLabel,
        command= visualize
    )

    frm_cnvs = Frame(master= frm_vis)
    cnvs_vis = Canvas(frm_cnvs, bg= "white", width=600, bd=1, relief="sunken")
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

    paned.grid(row=0, column=0, columnspan=2, sticky="nsew")
    paned.add(frm_input, minsize=300)
    paned.add(frm_output, minsize=100)

    window.columnconfigure(0, minsize=150)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, minsize=650, weight=1)

    frm_input.columnconfigure(0, weight=1)
    frm_input.rowconfigure([1,2], weight=1)
    lbl_input.grid(column=0, row=0, sticky="n")
    import_cutList.grid(column=0, row=1, sticky= "ew", pady=(0, 5))
    import_inventory.grid(column=0, row=2, sticky= "ew", pady=(0, 5))
    #cnvs_settings.grid(column=0, row=3, sticky= "w", pady=(0, 5))

    lbl_error.grid(column=0, row=4, sticky="s")
    btn_pack.grid(column=0, row=5, sticky="s", pady=10)
    lbl_stats.grid(column=0, row=6, sticky="s", pady=10)

    lbl_error.grid_remove()

    frm_output.columnconfigure(0, weight=1)
    frm_output.rowconfigure(0, weight=1)

    output_paned.grid(row=0, column=0, sticky="nsew")
    output_paned.add(frm_list, minsize=50)

    list_paned.grid(row=0, column=0, sticky="nsew")
    frm_list.rowconfigure(0, weight=1)
    frm_list.columnconfigure(0, weight=1)
    list_paned.add(frm_order, minsize= 50)
    list_paned.add(frm_instructions, minsize= 50)
    frm_order.rowconfigure(1, weight=1)
    frm_order.columnconfigure(0, weight=1)
    lbl_output.grid(column=0, row=0, columnspan=3, sticky="ew")
    txt_order.grid(row=1, column=0, sticky="nsew")
    frm_instructions.rowconfigure(0, weight=1)
    frm_instructions.rowconfigure(1, weight=0)
    frm_instructions.columnconfigure(0, weight=1)
    txt_instructions.grid(row=0, column=0, sticky="nsew")

    frm_save.grid(row=1, column=0, sticky="ew")
    frm_save.columnconfigure(0, weight=1)
    frm_save.columnconfigure(1, weight=1)

    checkBtn_vis.grid(column=0, row=0, sticky="w", padx=(0, 5))
    btn_save_spreadsheet.grid(row=0, column=3, sticky="e", padx=5, pady=5)
    btn_save.grid(row=0, column=4, sticky="e", padx=5, pady=5)
    

    frm_vis.rowconfigure(1, weight=1)
    frm_vis.columnconfigure(0, weight=1)

    frm_visTitle.grid(column=0, row=0, sticky="ew")
    frm_visTitle.columnconfigure(0, weight=1)
    frm_visTitle.columnconfigure(1, weight=1)
    lbl_vis.grid(column=0, row=0, columnspan=3, sticky="ew")
    lbl_checkVisLabel.grid(column=1, row=0, sticky="e")
    checkBtn_visLabel.grid(column=2, row=0, sticky="e", padx=(0, 5))
    frm_cnvs.grid(column=0, row=1, sticky="nsew")
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    cnvs_vis.pack(side="left", fill="both", expand=True) 

    
    window.mainloop()

if __name__ == "__main__":
    main()