![PlankPacker Icon](https://github.com/heskettalex/PlankPacker/blob/main/Assets/icon.png)
# Welcome to PlankPacker!

PlankPacker is a simple program designed to speed up the process of creating order lists and packed cut lists for construction projects.

## User Guide

To generate a packed cut list with PlankPacker, you must first input a **cut list**, and optionally an **inventory list**.

- A **cut list** contains every measurement and quantity of plank needed for a project.

- An **inventory list** contains every measurement and quantity of plank currently available. This can be useful if you already have a large inventory of stock and would like to reuse it before ordering any more wood (or other materials). It is not required.

Both lists must be formatted in a specific way in order for PlankPacker to read them. Every line in a PlankPacker list must either indicate a new **category** of plank, or a new **measurement** of that type of plank. The formatting for each is as followed:

**Category:** Category lines allow PlankPacker to pack different types of wood seperately. A properly formatted category line at minimum must contain two numbers (indicating the nominal dimensions of the lumber) separated by an **"x"**, and punctuated with a **colon.** 
Example category lines: `2x4:`, `1 x 3:`

**Measurement:** Measurement lines indicate what the packing algorithm has to work with. A properly formatted measurement line at minimum must contain a **quantity** and a **measurement** number seperated by an **"x"**. Measurements can be written either as decimals or fractions, but will always be displayed as fractions in the editor. Additionally, a **note** may be added following the measurement to indicate any additional information. Notes must begin with a **"#"** to be recognized by PlankPacker, and will be displayed in all subsequent lists containing the cut.

Example measurement lines: `3x 48`, `1x 96 1/16" #45 degrees /==\, 2x72.5`

**Note: As the examples indicate, all non-required characters, spaces, and indents in a line are automatically ignored by the program, but are okay to include for visual clarity!**

### Example PlankPacker list:
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
As mentioned before, empty lines, indents, and unit symbols like " are ignored by PlankPacker when imported. ` 8x 120"` will be read as `8x120`.

Once PlankPacker has at least an input cut list to work with, the packing algorithm must be provided at least one standard **order length** for each type of stock. The order lengths for each category represent what lengths of wood are available to order for each category of plank. By default, each category is assigned an order length of 96 inches (the standard plank length for most planks), but additional lengths can be added or removed from each section as long as they are seperated by a comma.

### Output
Once the desired lists are opened and the packing algorithm has been run, PlankPacker will output a text file containing an **order summary** and **cut list instructions**. 
- Order summary: How many additional planks are needed to create the desired cuts (after accounting for the inventory if provided).
- Cut list instructions: How to cut the planks indicated in the input cut list from the newly ordered planks (and inventory if provided). Planks cut from an inventory item are tagged with a "*" and highlighted blue for clarity.

This information can be saved as a text file or as a formatted spreadsheet for further use.

### Visualization
To visualize how the cuts are spaced on each plank, check the "visualize cuts" checkbox in the upper right corner of the "packing output" panel. This visualization is only visible in the PlankPacker editor, and is not saved to the output.
