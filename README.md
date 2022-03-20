# python build_from_mm.py <options>

A python script to bridge the gap between the OpenKH Mods Manager (developed mostly by Xeeynamo) and the OpenKH EGS Patcher (developed mostly by Noxalus)

Note: When using GOA Rom edition, must use the openkh mod for GOA Rom, rather than the .kh2pcpatch

## Usage

1 - Download the latest release, and run the exe to open up the config

1.5 - Configure all the paths in the "Setup" section properly (these will be saved when you run the program)

2.5 - If you have not extracted khpc do that by checking the "extract" option and running it for the game you want to extract (it will crash afterwards that is fine)

3 - After that rerun the mod manager setup wizard and make sure to select the PC extracted version of the game instead of the PS2

4 - Select the mods you want in the mod manager and "build only". you can close the mod manager window now

5 - in build_from_mm gui, make sure patch is the mode selected. Then click start

6 - Once that is complete you can load up the game

## Compiling to exe

pyinstaller build_from_mm.py --add-data pkgmap*.json;. -F