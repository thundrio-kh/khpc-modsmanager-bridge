import sys, os, shutil, subprocess, json, time

helpstr = '''
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
'''
starttime = time.time()

class KingdomHearts1Patcher:
    def __init__(self, region):
        self.region = region
        self.name = "kh1"
        self.pkgs = ["kh1_first.pkg", "kh1_second.pkg", "kh1_third.pkg", "kh1_fourth.pkg", "kh1_fifth.pkg"]
    def translate_path(self, path):
        if path.startswith(os.sep):
            path = path[1:]
        return path

class KingdomHearts2Patcher:
    def __init__(self, region):
        self.region = region
        self.name = "kh2"
        self.pkgs = ["kh2_first.pkg", "kh2_second.pkg", "kh2_third.pkg", "kh2_fourth.pkg", "kh2_fifth.pkg", "kh2_sixth.pkg"]
    def translate_path(self, path):
        if path.startswith(os.sep):
            path = path[1:]
        if os.sep+"jp"+os.sep in path:
            path = path.replace(os.sep+"jp"+os.sep, os.sep+self.region+os.sep)
        if "ard" in path:
            if not "jp" in path and not self.region in path:
                path = path.replace("ard"+os.sep, "ard"+os.sep+self.region+os.sep)
        return path

class BirthBySleepPatcher:
    def __init__(self, region):
        self.region = region
        self.name = "bbs"
        self.pkgs = ["bbs_first.pkg", "bbs_second.pkg", "bbs_third.pkg", "bbs_fourth.pkg"]
    def translate_path(self, path):
        if path.startswith(os.sep):
            path = path[1:]
        return path

class KingdomHearts3DPatcher:
    def __init__(self, region):
        self.region = region
        self.name = "kh3d"
        self.pkgs = ["kh3d_first.pkg", "kh3d_second.pkg", "kh3d_third.pkg", "kh3d_fourth.pkg"]
    def translate_path(self, path):
        if path.startswith(os.sep):
            path = path[1:]
        return path

class RecomPatcher:
    def __init__(self, region):
        self.region = region
        self.name = "Recom"
        self.pkgs = ["Recom.pkg"]
    def translate_path(self, path):
        if path.startswith(os.sep):
            path = path[1:]
        return path

games = {
    "kh1": KingdomHearts1Patcher,
    "kh2": KingdomHearts2Patcher,
    "bbs": BirthBySleepPatcher,
    "kh3d": KingdomHearts3DPatcher,
    "Recom": RecomPatcher
}

MODDIR = os.environ["USE_OPENKH_MODS_DIR"]
PKGDIR = os.environ["USE_KH_PKG_DIR"]
IDXDIR = os.getcwd() if not "USE_OPENKH_IDX_DIR" in os.environ else os.environ["USE_OPENKH_IDX_DIR"]
IDXPATH = os.path.join(IDXDIR, "OpenKh.Command.IdxImg.exe")
DEFAULTREGION = "us"

args = {}
for arg in sys.argv:
    if "=" in arg:
        args[arg.split("=")[0].strip()] = arg.split("=")[1].strip()
    else:
        args[arg] = True

if "help" in args:
    print(helpstr)
elif "game" in args:
    game = args["game"]
    if not args["game"] in games:
        raise Exception("Game not found, possible options: {}".format(list(games.keys())))
    if not os.path.exists(MODDIR):
        raise Exception("Mod dir not found")
    if not os.path.exists(PKGDIR):
        raise Exception("PKG dir not found")
    if not os.path.exists(IDXPATH):
        raise Exception("OpenKh.Command.IdxImg.exe not found")
    region = args.get("region", DEFAULTREGION)
    game = games[args["game"]](region=region)
    patch = args.get("patch", False)
    backup = args.get("backup", False)
    restore = args.get("restore", False)
    keepkhbuild = args.get("keepkhbuild", False)
    ignoremissing = int(args.get("ignoremissing", 1))
    pkgmap = json.load(open("pkgmap.json")).get(game.name)
    if backup:
        print("Backing up")
        if not os.path.exists("backup_pkgs"):
            os.makedirs("backup_pkgs")
        for pkg in game.pkgs:
            sourcefn = os.path.join(PKGDIR, pkg)
            newfn = os.path.join("backup_pkgs", pkg)
            shutil.copy(sourcefn, newfn)
    if restore:
        print("Restoring from backup")
        if not os.path.exists("backup_pkgs"):
            raise Exception("Backup folder doesn't exist")
        for pkg in game.pkgs:
            newfn = os.path.join(PKGDIR, pkg)
            sourcefn = os.path.join("backup_pkgs", pkg)
            shutil.copy(sourcefn, newfn)
    if patch:
        print("Patching")
        if os.path.exists("khbuild"):
            shutil.rmtree("khbuild")
        os.makedirs("khbuild")
        for root, dirs, files in os.walk(MODDIR):
            path = root.split(os.sep)
            for file in files:
                fn = os.path.join(root, file)
                relfn = fn.replace(MODDIR, '')
                relfn_trans = game.translate_path(relfn)
                print("Translated Filename: {}".format(relfn_trans))
                pkgs = pkgmap.get(relfn_trans, "")
                if not pkgs:
                    print("WARNING: Could not find which pkg this path belongs: {} (original path {})".format(relfn_trans, relfn))
                    if not ignoremissing:
                        raise Exception("Exiting due to warning")
                    continue
                for pkg in pkgs:
                    newfn = os.path.join("khbuild", pkg, "original", relfn_trans)
                    new_basedir = os.path.dirname(newfn)
                    if not os.path.exists(new_basedir):
                        os.makedirs(new_basedir)
                    shutil.copy(fn, newfn)
        for pkg in os.listdir("khbuild"):
            pkgfile = os.path.join(PKGDIR, pkg+".pkg")
            modfolder = os.path.join("khbuild", pkg)
            if not os.path.exists(os.path.join(modfolder, "remastered")):
                os.makedirs(os.path.join(modfolder, "remastered"))
            if os.path.exists("pkgoutput"):
                shutil.rmtree("pkgoutput")
            print("Patching: {}".format(pkg))
            args = [IDXPATH, "hed", "patch", pkgfile, modfolder, "-o", "pkgoutput"]
            print(IDXPATH, "hed", "patch", '"{}"'.format(pkgfile), '"modfolder"', "-o", '"{}"'.format("pkgoutput"))
            try:
                output = subprocess.check_output(args, stderr=subprocess.STDOUT)
                print(output)
            except subprocess.CalledProcessError as err:
                output = err.output
                print(output.decode('utf-8'))
                raise Exception("Patch failed")
            shutil.copy(os.path.join("pkgoutput", pkg+".pkg"), os.path.join(PKGDIR, pkg+".pkg"))
        if not keepkhbuild:
            shutil.rmtree("khbuild")
    print("All done! Took {}s".format(time.time()-starttime))
else:
    print("Specify Game to Patch")
    print(helpstr)
# run build_from_mm game=kh2 patch keepkhbuild ignoremissing=0