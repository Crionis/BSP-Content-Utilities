import sys, os, zipfile
from io import BytesIO

from PyQt5.QtWidgets import QApplication, QFileDialog
from valvebsp.bsp import *
from valvebsp.constants import *

TEXTRED, TEXTGREEN, TEXTNOCOLOR = "\033[31m", "\033[32m", "\033[0m"

DefaultGameContent = [ "contents/source.txt", "contents/gmod.txt", "contents/css.txt" ] # because we need order

def LoadContentList(listfile):
    listname = os.path.basename(listfile)
    newlist = {}
    with open(listfile, 'r') as file:
        for line in file:
            newlist[line.strip()] = listname

    return newlist

def CheckMap(bpspath):
    global DefaultGameContent
    excludefiles = []

    try:
        for flist in DefaultGameContent:
            excludefiles.append(LoadContentList(flist))
    except:
        print("Fail to load default content lists!")
        return
    
    print(f"BSP File: {bpspath}")
    
    # BSP processing    
    bsp = Bsp(bpspath)

    packfile = bsp._get_lump_header(LUMP_PAKFILE)
    with open(bpspath, 'rb') as f:
        f.seek(packfile['fileofs'])
        bsppack_zip = BytesIO(f.read(packfile['filelen']))

    zip_ref = zipfile.ZipFile(bsppack_zip, 'r')
    pakedfiles = zip_ref.namelist()

    founded = {}
    for pkfl in pakedfiles:
        for cntlist in excludefiles:
            if pkfl in cntlist and not pkfl in founded:
                founded[pkfl] = True
                print(f"Useless file (from {cntlist[pkfl]}): {pkfl}")

    found = len(founded)
    if found > 0:
        print(f"{TEXTRED}Map contain {found} files of default content!{TEXTNOCOLOR}")
    else:
        print(f"{TEXTGREEN}Default content not found.{TEXTNOCOLOR}")


app = QApplication(sys.argv)
ofd_filepath, _ = QFileDialog.getOpenFileName(None, 'Open File', '', 'BSP (*.bsp);;All Files (*)')
CheckMap(ofd_filepath)
os.system("pause")