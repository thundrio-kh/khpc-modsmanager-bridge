A python script to bridge the gap between the OpenKH Mods Manager (developed mostly by Xeeynamo) and the OpenKH EGS Patcher (developed mostly by Noxalus)

USAGE:
<Before Using> Package your selected mods using the "Run" -> "Build only" functionality of the mods manager
<Before Using> Set environment variable USE_OPENKH_MODS_DIR to the "mod" directory in the mods manager
<Before Using> Set environment variable USE_KH_PKG_DIR to the directory containing the kh pkg files
<Before Using> OPTIONAL: Set environment variable USE_OPENKH_IDX_DIR to the directory containing the IdxImg.exe, otherwise put this python file in that directory
python buid_from_mm.py <options>
possible options
  help - show this message
  game=<game> - should be "kh1" or "kh2" or "bbs" or "recom"
  patch - patch the games files with the contents of the mods manager "mods" directory
  backup - will backup the games PKG files to a new folder in this directory called "backup_pkgs" (warning, can take a lot of space)
  restore - will restore the games pkg files before applying the patch, using the pkgs found in "backup_pkgs"
  region=<region> - defaults to "us", needed to make sure the correct files are patched, as KH2FM PS2 mods use "jp" as the region
  keepkhbuild - will keep the intermediate khbuild folder from being deleted after the patch is applied
  ignoremissing=<1 or 0> - defaults to true. If true, prints a warning when a file can't be patched, rather than failing
