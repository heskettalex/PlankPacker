import math
import xlsxwriter
from Plank import Plank
from Utils import value_to_frac
from collections import Counter

    
def stats(cuts):
    totalLength = 0.0
    totalWaste = 0.0
    totalCuts = 0
    inventoryCuts = 0

    if isinstance(cuts, list):
        for plank in cuts:
            totalLength += plank.length
            totalWaste += plank.freeStock()
            if plank.inventory:
                inventoryCuts += len(plank.cuts)
            totalCuts += len(plank.cuts)
    else:
        for category in cuts:
            for plank in cuts[category]:
                totalLength += plank.length
                totalWaste += plank.freeStock()
                if plank.inventory:
                    inventoryCuts += len(plank.cuts)
                totalCuts += len(plank.cuts)

    return f"{totalWaste / totalLength * 100:.1f}% waste\n{inventoryCuts / totalCuts * 100:.1f}% from inventory"


def get_order(cuts):
    order = {}
    for category in cuts:
        planks = []
        for plank in cuts[category]:
            if not plank.inventory:
                planks.append((plank.length, plank.note))
        plank_counter = Counter(planks).items()
        if len(plank_counter) > 0:
            order[category] = plank_counter
    return order

def get_instructions(cuts):
    output = {}
    for category in cuts:
        
        plank_counter = Counter(cuts[category]).most_common()
        inventory = []
        order = []
        for plank, count in plank_counter:
            stock = f"{count}x {value_to_frac(plank.length)}\""
            if plank.note != "":
                stock += f" ({plank.note})"
            cut_result = ""

            if len(plank.cuts) == 1:
                cut, note = plank.cuts[0]
                if note == "":
                    cut_result = f"{count}x {value_to_frac(cut)}\""
                else:
                    cut_result = f"{count}x {value_to_frac(cut)}\" ({note})"
            else:
                if count > 1:
                    cut_result = f"{count}x ({plank})"
                else:
                    cut_result = f"{plank}"

            if plank.inventory:
                stock = "*" + stock
                inventory.append((stock, cut_result))
            else:
                order.append((stock, cut_result))
        output[category] = order + inventory
    return output

def summary(cuts):
    order = "Additional Stock Needed:\n"

    order_dict = get_order(cuts)
    if len(order_dict) == 0:
        return "No additional stock needed."
    else:
        for category in order_dict:
            order += f"{category[0]}x{category[1]}:\n"
            for (length, note), count in order_dict[category]:
                order += f" - {count}x {value_to_frac(length)}\""
                if note != "":
                    order += f" ({note})"
                order += "\n"  
        return order

def printCuts(cuts):
    output = "Cut List Instructions:\n(* = from inventory)\n"
    instructions_dict = get_instructions(cuts)
    for category in instructions_dict:
        thickness, width = category
        output += f"{thickness}x{width}:\n"
        for stock, cut_result in instructions_dict[category]:
            output += f" - {stock} => {cut_result}\n"
    return output

def colnum_to_letter(n):
    result = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result

def generate_spreadsheet(list, filepath):
    workbook = xlsxwriter.Workbook(filepath)
    highlight = workbook.add_format({'font_color': '#008B8B', 'text_wrap': True, 'valign': 'top'})
    wrap = workbook.add_format({'text_wrap': True, 'valign': 'top'})
    bold = workbook.add_format({'bold': True})

    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 2, 13)
    y = 0
    x = 0

    order_dict = get_order(list)
    if len(order_dict) > 0:

        worksheet.write(y, x, "Order Summary", bold)
        y += 1

        table_start_row = y
        x = 0
    
        for category in order_dict:
            worksheet.write(y, x, f"{category[0]}x{category[1]}\n")
            for (length, note), count in order_dict[category]:
                length = f"{value_to_frac(length)}\""
                if note != "":
                    length += f" ({note})"
                worksheet.write(y, x + 1, length)
                worksheet.write(y, x + 2, count)
                worksheet.set_row(y, None, None, {'level': 1})
                y += 1
        worksheet.add_table(table_start_row, 0, y-1, 2, {
            'name': 'Order_Summary',
            'style': 'Table Style Medium 15',
            'columns': [{'header': 'Type'},
                        {'header': 'Length'},
                        {'header': 'Quantity'}],
            'banded_rows': False
        })

    x = 0
    y += 1

    worksheet.write(y, x, "Cut List Instructions", bold)
    y += 1
    
    instructions_y = y
    instructions_dict = get_instructions(list)
    for i, category in enumerate(instructions_dict):
        worksheet.set_column(x, x+1, 13)
        worksheet.write(y, x, f"{category[0]}x{category[1]}", wrap)
        y += 1

        table_start_row = y
        y += 1
        
        for stock, cut_result in instructions_dict[category]:
            if "*" in stock:
                worksheet.write(y, x, stock, highlight)
            else:
                worksheet.write(y, x, stock, wrap)
            worksheet.write(y, x+1, cut_result, wrap)
            worksheet.set_row(y, None, None, {'level': 1})
            y += 1
        
        worksheet.add_table(table_start_row, x, y-1, x+1, {
            'name': f"Instructions_{colnum_to_letter(i+1)}",
            'style': 'Table Style Medium 15',
            'columns': [{'header': 'Stock'},
                        {'header': 'Cut Result'},],
            'banded_rows': False,
        })
        y = instructions_y
        x += 3


    workbook.close()