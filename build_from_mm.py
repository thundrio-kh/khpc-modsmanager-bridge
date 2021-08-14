import sys, os, shutil, subprocess, json, time, argparse
from gooey import Gooey, GooeyParser


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
DEFAULTREGION = "us"
DEFAULTGAME = "kh2"

@Gooey
def main():
    starttime = time.time()

    default_config = {
        "game": DEFAULTGAME,
        "openkh_path": "",
        "extracted_games_path": "",
        "khgame_path": "",
        "region": DEFAULTREGION
    }
    if os.path.exists("config.json"):
        default_config = json.load(open("config.json"))

    parser = GooeyParser()

    parser.add_argument("-game", choices=list(games.keys()), default=default_config.get("game"), help="Which game to operate on", required=True)

    parser.add_argument("-openkh_path", help="Path to openKH folder", default=default_config.get("openkh_path"), widget='DirChooser')
    parser.add_argument("-extracted_games_path", help="Path to folder containing extracted games", default=default_config.get("extracted_games_path"), widget='DirChooser')
    parser.add_argument("-khgame_path", help="Path to the kh_1.5_2.5 folder", default=default_config.get("khgame_path"), widget='DirChooser')

    parser.add_argument("-region", choices=["jp", "us", "uk", "it", "sp", "gr", "fr"], default=default_config.get("region", ""), help="defaults to 'us', needed to make sure the correct files are patched, as KH2FM PS2 mods use 'jp' as the region")

    parser.add_argument("-restore", action="store_true", default=True, help="Will restore the games pkg files before applying the patch, using the pkgs found in 'backup_pkgs'")
    parser.add_argument("-patch", action="store_true", default=True, help="Patch the games files with the contents of the Mods Manager 'mod' directory")

    parser.add_argument("-backup", action="store_true", default=False, help="Will backup the games PKG files to a new folder in this directory called 'backup_pkgs' (warning, can take a lot of space)")
    parser.add_argument("-extract", action="store_true", default=False, help="Will extract the games PKG files to be used by Mods Manger")


    parser.add_argument("-keepkhbuild", action="store_true", default=False, help="Will keep the intermediate khbuild folder from being deleted after the patch is applied")

    parser.add_argument('-ignoremissing', type=int, default=1, help="If true, prints a warning when a file can't be patched, rather than failing")

    # Parse and print the results
    args = parser.parse_args()

    config_to_write = {
        "game": args.game,
        "openkh_path": args.openkh_path,
        "extracted_games_path": args.extracted_games_path,
        "khgame_path": args.khgame_path,
        "region": args.region
    }

    json.dump(config_to_write, open("config.json", "w"))

    MODDIR = os.path.join(args.openkh_path, "mod")
    PKGDIR = os.path.join(args.khgame_path, "Image", "en")
    IDXDIR =args.openkh_path
    IDXPATH = os.path.join(IDXDIR, "OpenKh.Command.IdxImg.exe")


    gamename = args.game
    if not args.game in games:
        raise Exception("Game not found, possible options: {}".format(list(games.keys())))
    if not os.path.exists(MODDIR):
        raise Exception("Mod dir not found")
    if not os.path.exists(PKGDIR):
        raise Exception("PKG dir not found")
    if not os.path.exists(IDXPATH):
        raise Exception("OpenKh.Command.IdxImg.exe not found")
    region = args.region
    game = games[gamename](region=region)
    patch = args.patch
    backup = args.backup
    extract = args.extract
    restore = args.restore
    keepkhbuild = args.keepkhbuild
    ignoremissing = args.ignoremissing

    print("CONFIG TO RUN")
    print("patch", patch)
    print("backup", backup)
    print("extract", args.extract)
    print("restore", args.restore)
    print("keepkhbuild", args.keepkhbuild)
    print("ignoremissing", args.ignoremissing)
    pkgmap = json.load(open("pkgmap.json")).get(game.name)
    if extract:
        print("Extracting {}".format(game.name))
        if not os.path.exists(args.extracted_games_path):
            raise Exception("Path does not exist to extract games to! {}".format(args.extracted_games_path))
        pkglist = [os.path.join(PKGDIR,p) for p in os.listdir(PKGDIR) if game.name in p and p.endswith(".pkg")]
        if os.path.exists("extractedout"):
            shutil.rmtree("extractedout")
        os.makedirs("extractedout")
        EXTRACTED_GAME_PATH = os.path.join(args.extracted_games_path, game.name)
        if os.path.exists(EXTRACTED_GAME_PATH):
            shutil.rmtree(EXTRACTED_GAME_PATH)
        os.makedirs(EXTRACTED_GAME_PATH)
        for pkgfile in pkglist:
            args = [IDXPATH, "hed", "extract", pkgfile, "-o", "extractedout"]
            print(IDXPATH, "hed", "extract", '"{}"'.format(pkgfile), "-o", '"{}"'.format("extractedout"))
            try:
                output = subprocess.check_output(args, stderr=subprocess.STDOUT)
                print(output)
                original_path = os.path.join("extractedout")
                for root, dirs, files in os.walk(os.path.join)
            except subprocess.CalledProcessError as err:
                output = err.output
                print(output.decode('utf-8'))
                raise Exception("Extract failed")
    if backup:
        print("Backing up")
        if not os.path.exists("backup_pkgs"):
            os.makedirs("backup_pkgs")
        for pkg in game.pkgs:
            sourcefn = os.path.join(PKGDIR, pkg)
            newfn = os.path.join("backup_pkgs", pkg)
            shutil.copy(sourcefn, newfn)
            shutil.copy(sourcefn.split(".pkg")[0]+".hed", newfn.split(".pkg")[0]+".hed")
    if restore:
        print("Restoring from backup")
        if not os.path.exists("backup_pkgs"):
            raise Exception("Backup folder doesn't exist")
        for pkg in game.pkgs:
            newfn = os.path.join(PKGDIR, pkg)
            sourcefn = os.path.join("backup_pkgs", pkg)
            shutil.copy(sourcefn, newfn)
            shutil.copy(sourcefn.split(".pkg")[0]+".hed", newfn.split(".pkg")[0]+".hed")
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
            #print(IDXPATH, "hed", "patch", '"{}"'.format(pkgfile), '"modfolder"', "-o", '"{}"'.format("pkgoutput"))
            try:
                print(args)
                output = subprocess.check_output(args, stderr=subprocess.STDOUT)
                print(output)
            except subprocess.CalledProcessError as err:
                output = err.output
                print(output.decode('utf-8'))
                raise Exception("Patch failed")
            shutil.copy(os.path.join("pkgoutput", pkg+".pkg"), os.path.join(PKGDIR, pkg+".pkg"))
            shutil.copy(os.path.join("pkgoutput", pkg+".hed"), os.path.join(PKGDIR, pkg+".hed"))
        if not keepkhbuild:
            shutil.rmtree("khbuild")
    print("All done! Took {}s".format(time.time()-starttime))


main()