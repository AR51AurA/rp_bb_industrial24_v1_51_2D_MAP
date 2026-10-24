# rp_bb_industrial24_v1_51_2D_MAP
A 2D map overview of rp_bb_industrial24_v1_51 with editable districts, and exportable json files

# Setup
Extract to a separate folder
install python for hot-saving functionality
OR run via html file.

# readme.txt
City 24i Map
============

A zoomable top-down map of the city in rp_bb_industrial24, with coloured
district outlines you can rename, recolour and reshape.

Running it
----------
Double-click "Run City Map.bat". A console window opens and the map opens in
your browser. Leave the console open while you use the map; close it to stop.
Every time you press Save, your districts are written to districts.json in
this folder (the previous version is kept as districts.json.bak).

It needs Python 3, which you already have for the s1tos2 toolset.
You can also start it yourself:   python citymap_server.py

No Python? Open index.html directly in your browser. Everything works, but
Save keeps your edits inside that browser only. Use Export to write a
districts.json file, and Import to load one back.

Depth levels
------------
The Depth panel (top right) picks a level. Picking one brings it into view and
hides the levels above it:
  City level          streets and rooftops
  Sewers              canals, tunnels and basements under the streets
  Nexus underground   Nexus basement, firing range, rail tunnel
The underground levels are floor plans built from the VMF brushes: walkable
floors that have a ceiling over them, walls drawn as pale lines, solid ground dark.
Where one floor sits over another (a walkway above a canal, say), the upper
floor is drawn half see-through with diagonal hatching, so the passage under it
still shows; its walls stay crisp and the lower floor's walls are dimmer.
Tick "Show level above" to see the next level up faintly.
PageUp / PageDown (or [ and ]) also change level.
Brushes and entities in hidden visgroups (like sewer rework > new_area) are left out.
Each district belongs to one level and only shows there. Select a district
and use its level menu to move it to another level.

Using the map
-------------
- Drag to pan, scroll (or pinch) to zoom. + / - / 0 on the keyboard also zoom and fit.
- Click a district to select it. Rename it by typing in the list on the right,
  or double-click it on the map.
- Pick a colour from the swatches under the selected district, or click its colour square.
- "Edit shapes": drag corners, click a dashed dot to add a corner, Delete removes
  the picked corner. Drag inside the selected district to move it. Corners snap to 8 units.
- "+ District" adds a new outline in the middle of the view.
- "Copy JSON" copies every outline in Hammer x/y units (the same numbers getpos
  shows in game), ready to use in code.
- The bottom-left corner shows the Hammer coordinates under your cursor.

Files
-----
index.html            the map (opens on its own too)
t??.webp              city level render, 3 Hammer units per pixel
s??/n??.webp          sewers / nexus underground floor plans
districts.json        your districts (edit by hand if you like; points are Hammer x, y,
                      "level" is city, sewers or nexus)
citymap_server.py     the local launcher (listens on 127.0.0.1 only)
