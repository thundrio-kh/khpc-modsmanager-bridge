# python build_from_mm.py <options>

A python script to bridge the gap between the OpenKH Mods Manager (developed mostly by Xeeynamo) and the OpenKH EGS Patcher (developed mostly by Noxalus)


## USAGE:

<Before Using> Package your selected mods using the "Run" -> "Build only" functionality of the mods manager  
<Before Using> Set environment variable USE_OPENKH_MODS_DIR to the "mod" directory in the mods manager  
<Before Using> Set environment variable USE_KH_PKG_DIR to the directory containing the kh pkg files  
<Before Using> OPTIONAL: Set environment variable USE_OPENKH_IDX_DIR to the directory containing the IdxImg.exe, otherwise put this python file in that directory  
 
usage: build_from_mm.py [-h] [-patch] [-backup] [-restore] [-keepkhbuild] [-region {jp,us,uk,it,sp,gr,fr}]
                        [-ignoremissing IGNOREMISSING]
                        {kh1,kh2,bbs,kh3d,Recom}