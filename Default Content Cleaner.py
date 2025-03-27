import sys, os
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

TEXTRED, TEXTGREEN, TEXTNOCOLOR = "\033[31m", "\033[32m", "\033[0m"

DefaultGameContent = [ "contents/source.txt", "contents/gmod.txt", "contents/css.txt" ] # because we need order

def LoadContentList(listfile):
    listname = os.path.basename(listfile)
    newlist = {}
    with open(listfile, 'r') as file:
        for line in file:
            newlist[line.strip()] = listname

    return newlist

def RemoveDefaultContent(contentpath):
    global DefaultGameContent
    excludefiles = []

    try:
        for flist in DefaultGameContent:
            excludefiles.append(LoadContentList(flist))
    except:
        print("Fail to load default content lists!")
        return

    print(f"Content path: {contentpath}")

    removed = 0
    for root, _, files in os.walk(contentpath):
        for file in files:
            gpath = os.path.join(root, file)
            lpath = gpath.replace(contentpath, '').replace('\\', '/')
            for cntlist in excludefiles:
                if lpath in cntlist:
                    print("Deleted", gpath)
                    os.remove(gpath)
                    removed += 1
                    break

    print(f"Done. {removed} files deleted.")

app = QApplication(sys.argv)
print("Select the directory with the extracted content from BSP.")
directory = QFileDialog.getExistingDirectory(None, "Select Directory", options= QFileDialog.Options() | QFileDialog.ShowDirsOnly)

msg_box = QMessageBox()
msg_box.setIcon(QMessageBox.Warning)
msg_box.setWindowTitle("Warning!")
msg_box.setText(f"Make sure you have selected the correct directory!\n{directory}\nAre you sure to delete the useless files?")
msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
msg_box.setDefaultButton(QMessageBox.No)

response = msg_box.exec_()
if response == QMessageBox.Yes:
    RemoveDefaultContent(directory + '/')

os.system("pause")