# Welcome to PlankPacker!

PlankPacker is a simple program designed to speed up the process of creating order lists and packed cut lists for construction projects.

## User Guide

To generate a packed cut list with PlankPacker, you must first input a **cut list**, and optionally an **inventory list**.

- A **cut list** contains every measurement and quantity of plank needed for a project.

- An **inventory list** contains every measurement and quantity of plank currently available. This can be useful if you already have a large inventory of stock and would like to reuse it before ordering any more wood (or other materials). It is not required.

Both lists must be formatted in a specific way in order for PlankPacker to read them. Every line in a PlankPacker list must either indicate a new **category** of plank, or a new **measurement** of that type of plank. The formatting for each is as followed:

**Category:** A properly formatted category line at minimum must contain two numbers (indicating the nominal dimensions of the lumber) separated by an **"x"**, and punctuated with a **colon.** Category lines allow PlankPacker to pack different types of wood seperately.

Example category lines: `2x4:`, `1 x 3:`

**Measurement:** A properly formatted measurement line at minimum must contain a **quantity** and a **measurement** number seperated by an **"x"**. Measurement lines indicate what the packing algorithm has to work with.

Example measurement lines: `3x 48`, `1x96"`

**Note: As the examples indicate, all non-required characters, spaces, and indents in a line are automatically ignored by the program, but are okay to include for visual clarity!**

### Example PlankPacker list:
```
1x3:
  4x 96"
  7x 45"
  24x 36"

2x4:
  8x 72"
  3x 20"
  4x 48"
  8x 120"

4x4:
  2x 80"
```
As mentioned before, empty lines, indents, and unit symbols like " are ignored by PlankPacker when imported. ` 8x 120"` will be read as `8x120`.

Once PlankPacker is provided at least an input cut list to work with, the packing algorithm may be run. There are two parameters available before clicking "Pack": **Order Length** and **Overflow Increment**. Both values should be input as whole or decimal numbers, with no additional characters.

**Order Length** indicates the standard plank/material length to pack the cuts to. This can also be interpreted as "what length of plank are you ordering?"

**Overflow Increment** tells PlankPacker how to handle cuts in the input cut list which exceed the standard order length provided previously. When a cut exceeds that length, PlankPacker will place it in a new plank rounded to the nearest multiple of the provided **overflow increment** above the **order length**. For example, if the order length is set to 96", the overflow increment is set to 24", and a cut is listed as 105", the algorithm will place that cut in a new plank of length 120" (one multiple of 24" above 96"). Ideally, one should avoid including oversized planks in a cut list, but PlankPacker is still prepared to handle them. 

### Output
Once the desired lists are opened and the packing algorithm has been run, PlankPacker will output a text file containing an **order summary** and **cut list instructions**. 
- Order summary: How many additional planks are needed to create the desired cuts (after accounting for the inventory if provided).
- Cut list instructions: How to cut the planks indicated in the input cut list from the newly ordered planks (and inventory if provided).

This text file can be saved with the "Save" button in the upper right.
