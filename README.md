![PlankPacker Icon](https://github.com/heskettalex/PlankPacker/blob/main/Assets/icon.png)
# Welcome to PlankPacker!

PlankPacker is a simple program designed to speed up the process of creating order lists and packed cut lists for construction projects.

# User Guide

To generate a packed cut list with PlankPacker, you must first input a **cut list**, and optionally an **inventory list**. Plankpacker accepts lists as both **excel spreadsheets** and **text files**.

- A **cut list** contains every measurement and quantity of plank needed for a project.

- An **inventory list** contains every measurement and quantity of plank currently available. This can be useful if you already have a large inventory of stock and would like to reuse it before ordering any more wood (or other materials). It is not required.

Examples of each can be found in the **example lists folder**.

## Importing Excel Spreadsheets
In order to be read by PlankPacker, a spreadhseet must be divided into subsections for each category of plank. The upper left cell of each category list indicates the **category title** and must lie on the top row of the spreadsheet.

**Category Titles**: Two numbers indicating the nominal dimensions of the lumber separated by an **"x"**.
Example category title cells: `2x4`, `1 x 3`

A subsection for a given category takes up three columns, indicating a **measurement** (in inches), **quantity**, and optional **note** in that exact order. Rows containing text may be included to label each column, but will be ignored by PlankPacker in the importing process.

Example Spreadsheet List:

![image](https://github.com/user-attachments/assets/adbf48a1-5232-4174-a80f-d881950b7301)


## Importing Text Lists
Text lines must either indicate a new **category** of plank, or a new **measurement** of that type of plank. The formatting for each is as followed:

**Category:** Same as excel spreasheets, but punctuated with a colon.
Example category lines: `2x4:`, `1 x 3:`

**Measurement:** **Quantity** and a **measurement** number seperated by an **"x"**. Measurements can be written either as decimals or fractions, but will always be displayed as fractions in the editor. A **note** may be added following the measurement beginning with a **"#"**.
Example measurement lines: `3x 48`, `1x 96 1/16" #45 degrees /==\, 2x72.5`

**Note: As the examples indicate, all non-required characters, spaces, and indents in a line are automatically ignored by the program, but are okay to include for visual clarity!**

### Example Text List:
```
1x3:
  4x 96" #Railings
  7x 45 1/2"
  24x 36 7/16"

2x4:
  8x 72"
  3x 20 3/4"
  4x 48" #45 degrees /==\
  8x 120"

4x4:
  2x 80"
```

## Order Lengths
Once PlankPacker has at least an input cut list to work with, the packing algorithm must be provided at least one standard **order length** for each type of stock.

The order lengths for each category represent what lengths of wood are available to order for each category of plank. By default, each category is assigned an order length of 96 inches (the standard plank length for most planks), but additional lengths can be added or removed from each section as long as they are seperated by a comma.

## Output
Once the desired lists are opened and the packing algorithm has been run, PlankPacker will output a text file containing an **order summary** and **cut list instructions**. 
- Order summary: How many additional planks are needed to create the desired cuts (after accounting for the inventory if provided).
- Cut list instructions: How to cut the planks indicated in the input cut list from the newly ordered planks (and inventory if provided). Planks cut from an inventory item are tagged with a "*" and highlighted blue for clarity.

This information can be saved as a text file or as a formatted spreadsheet for further use.

## Visualization
To visualize how the cuts are spaced on each plank, check the "visualize cuts" checkbox in the upper right corner of the "packing output" panel. This visualization is only visible in the PlankPacker editor, and is not saved to the output.

![image](https://github.com/user-attachments/assets/1f24122f-367b-475b-b0de-d9210a111039)

