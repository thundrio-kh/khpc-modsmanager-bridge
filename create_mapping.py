import json, os

x = {}

for root, dirs, files in os.walk("extracted_pkgs"):
    if "remastered" in root:
        continue
    path = root.split(os.sep)
    if not len(path) > 1:
        print("skipping {}".format(path))
        continue
    pkg = path[1]
    game = pkg.split("_")[0]
    if not game in x:
        x[game] = {}
    for file in files:
        relpath = os.path.join(*path[3:],file)
        if relpath not in x[game]:
            x[game][relpath] = []
        x[game][relpath].append(pkg)

json.dump(x, open("pkgmap.json", "w"))
