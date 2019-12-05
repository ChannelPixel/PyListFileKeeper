# Write an interactive program that maintains lists of strings in files.
# When the program is run it should create a list of all the files in the current directory that have the .lst extension.
# Use os.listdir(".") to get all the files and filter out those that don’t have the .lst extension.
# If there are no matching files the program should prompt the user to enter a filename adding the .lst extension if the
# user doesn’t enter it.
# If there are one or more .lst files they should be printed as a numbered list starting from 1.
# The user should be asked to enter the number of the file they want to load, or 0, in which case they should be asked
# to give a filename for a new file.
# If an existing file was specified its items should be read.
# If the file is empty, or if a new file was specified, the program should show a message, “no items are in the list”.
# If there are no items, two options should be offered: “Add” and “Quit”.
# Once the list has one or more items, the list should be shown with each item numbered from 1, and the options
# offered should be “Add”, “Delete”, “Save” (unless already saved), and “Quit”.
# If the user chooses “Quit” and there are unsaved changes they should be given the chance to save.

# Keep the main() function fairly small (less than 30 lines) and use it to provide the program’s main loop.
# Write a function to get the new or existing filename (and in the latter case to load the items), and a function to
# present the options and get the user’s choice of option.
# Also write functions to add an item, delete an item, print a list (of either items or filenames), load the list, and
# save the list.

import os

# Sanitizes strings for variables that aren't allowed in filenames and the string's length
def IsLegalStringInputFilename(variable):
        try:
            # variable string contains an illegal character
            if "\\" in variable \
                    or "/" in variable \
                    or ":" in variable \
                    or ":" in variable \
                    or "*" in variable \
                    or "?" in variable \
                    or "<" in variable \
                    or ">" in variable \
                    or "|" in variable :
                        raise ValueError
            # Check Max & Min Length
            elif len(str(variable)) >= 260 or len(str(variable)) <= 0:
                raise IndexError
            #
            else:
                return True

        except TypeError:
            print("ERROR: The variable suppled for sanitization was not a string")
            return False
        except ValueError:
            print("ERROR: Filenames can't contain:\n"+
                  "\\ / : * ? < > |")
            return False
        except IndexError:
            print("ERROR: Filename must be >0 AND <260 characters")
            return False

# Used to create a new .lst file in current directory
def CreateNewList():
    print("--.LST-CREATION-OPTIONS---")
    while True:
        filename = input("Please provide a filename for a new .lst file \n"
                         ">>> ")
        if IsLegalStringInputFilename(filename):
            try:
                file = open(filename+".lst","x")
                print("Filename accepted.")
                file.close()
                break
            except IOError:
                print("ERROR: Filename already exists")
                continue
        else:
            continue

# Returns a list of the .lst files in the current directory
def ScanCurrentLstFiles():
    while True:
        CurrentLstFiles = []
        AtLeastOneLst = False

        for file in os.listdir("."):
            if file.endswith(".lst"):
                CurrentLstFiles.append(file)
                AtLeastOneLst = True

        if not AtLeastOneLst:
            print("No .lst files were found in the current directory.")
            CreateNewList()
            continue
        else:
            return CurrentLstFiles

def SelectLstFileFromList():
    while True:
        tempList = ScanCurrentLstFiles()
        print("==.LST=EXTENSION=FILES====")
        fileCounter = 1
        for file in tempList:
            print("["+str(fileCounter)+"]"+file)
            fileCounter = fileCounter + 1

        print("")
        print("--.LST-SELECTION-OPTIONS--")
        print("Enter [#] to select a .lst file\n"
              "Enter [0] to create a new .lst file.\n"
              "Enter [X] to exit application.")
        selectionInput = input(">>> ")
        print()

        try:
            if selectionInput == "x":
                break
            selectionInputInt = int(selectionInput)
            if selectionInputInt > fileCounter-1 or selectionInputInt < 0:
                raise ValueError
            elif selectionInputInt == 0:
                CreateNewList()
                continue
            else:
                SelectedLstFileOptions(tempList[selectionInputInt-1])
                continue

        except ValueError:
            print("ERROR: selection entered was not a number or is out of bounds")
            continue

def ReturnItemsFromLstFile(lstFileName):
    file = open(lstFileName, "rt")
    returnItems = []
    for line in file.read().splitlines():
        returnItems.append(line)
    file.close()
    return returnItems

def SelectedLstFileOptions(lstFileName):
    changed = False
    itemsChanged = 0
    returnedItems = None
    while True:
        deleteOption = False
        if returnedItems is None:
            returnedItems = ReturnItemsFromLstFile(lstFileName)
        if len(returnedItems) > 0:
            deleteOption = True

        returnedItems.sort()

        print("=="+lstFileName+"=ITEMS==")
        itemCounter = 1
        for item in returnedItems:
            print("["+str(itemCounter)+"]"+item)
            itemCounter = itemCounter + 1
        if itemCounter == 1:
            print("**NO ITEMS**")
        print()
        print("--.LST-OPTIONS-----------")
        print("Enter [A] to add an item")
        if deleteOption:
            print("Enter [D] to delete an item")
        if changed:
            print("Enter [S] to save changes")
        print("Enter [Q] to return to .lst files")
        selectionInput = input(">>> ")
        print()

        if selectionInput == "a" or selectionInput == "A":
            print("Enter the new item's name")
            returnedItems.append(input(">>> "))
            changed = True
            itemsChanged = itemsChanged + 1
            print()

        elif (selectionInput == "d" or selectionInput == "D") and deleteOption:
            while True:
                print("Enter an item's [#] to delete it.")
                deleteInput = input(">>> ")
                try:
                    if int(deleteInput) > itemCounter - 1 or int(deleteInput) <= 0:
                        raise ValueError
                    returnedItems.pop(int(deleteInput)-1)
                    break
                except ValueError:
                    print("ERROR: Invalid number or item out of bounds")
                    continue

            changed = True
            itemsChanged = itemsChanged + 1
            print()

        elif (selectionInput == "s" or selectionInput == "S") and changed:
            file = open(lstFileName, "w")
            file.writelines("\n".join(returnedItems))
            file.close()
            print("Changes saved")
            changed = False
            itemsChanged = 0
            returnedItems = None
            print()

        elif selectionInput == "q" or selectionInput == "Q":
            if changed:
                while True:
                    print("You've made some unsaved changes. Save changes? [Y/N]")
                    saveInput = input(">>>")
                    print()

                    if saveInput == "y" or saveInput == "Y":
                        file = open(lstFileName, "w")
                        file.writelines("\n".join(returnedItems))
                        file.close()
                        print("Changes saved")
                        print()
                        break
                    elif saveInput == "n" or saveInput == "N":
                        break
                    else:
                        print("ERROR: Invalid option")
                        continue
            break

        else:
            print("ERROR: Invalid option")
            print()

def Main():
    SelectLstFileFromList()

Main()