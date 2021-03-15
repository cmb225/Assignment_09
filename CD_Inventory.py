#------------------------------------------#
# Title: CD_Inventory.py
# Desc: The CD Inventory App main Module
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# DBiesinger, 2030-Jan-02, Extended functionality to add tracks
# CBuffalow, 2021-Mar-13, Added sub-menu for CD Selection, tweaked print statements
# CBuffalow, 2021-Mar-13, Modified sub-menu for CD selection to add error handling
# CBuffalow, 2021-Mar-13, Added program header, added error handling in sub-menu
#------------------------------------------#

import ProcessingClasses as PC
import IOClasses as IO

lstFileNames = ['AlbumInventory.txt', 'TrackInventory.txt']
lstOfCDObjects = []
lstOfCDObjects = IO.FileIO.load_inventory(lstFileNames)
print('\n')
print('~'*60)
print(' |', ' '*54, '| ')
print(' |','The Magic CD Inventory'.center(54),'| ')
print(' |', ' '*54, '| ')
print('~'*60)
print('\n')

while True:
    IO.ScreenIO.print_menu()
    strChoice = IO.ScreenIO.menu_choice()
    if strChoice == 'x':
        break
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the inventory will be re-loaded from file.')
        strYesNo = input('Type \'yes\' to continue - otherwise reload will be cancelled.  ')
        if strYesNo.lower() == 'yes':
            print('Reloading...')
            lstOfCDObjects = IO.FileIO.load_inventory(lstFileNames)
            IO.ScreenIO.show_inventory(lstOfCDObjects)
        else:
            input('Cancelling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.ScreenIO.show_inventory(lstOfCDObjects)
        continue  # start loop back at top.
    elif strChoice == 'a':
        tplCdInfo = IO.ScreenIO.get_CD_info(lstOfCDObjects)
        PC.DataProcessor.add_CD(tplCdInfo, lstOfCDObjects)
        IO.ScreenIO.show_inventory(lstOfCDObjects)
        continue  # start loop back at top.
    elif strChoice == 'd':
        IO.ScreenIO.show_inventory(lstOfCDObjects)
        continue  # start loop back at top.
    elif strChoice == 'c':
        if lstOfCDObjects == []: #if no CDs, there is no need to enter sub-menu
            print('There are no CDs in the Inventory. Please add a CD first.')
            print('Returning to Main Menu.')
            continue
        IO.ScreenIO.show_inventory(lstOfCDObjects)
        try: #try loop to test to make sure cd_idx is valid entry (is int, exists)
            cd_idx = input('Select the CD / Album index: ') 
            cd = PC.DataProcessor.select_cd(lstOfCDObjects, cd_idx)
            print('You have chosen:', cd.cd_title, 'by', cd.cd_artist)
        except Exception as e:
            print('There has been an error.', e, e.__doc__, type(e), sep='\n')
            continue #returns to main loop
        while True:
            IO.ScreenIO.print_CD_menu()
            strCDChoice = IO.ScreenIO.menu_CD_choice()
            if strCDChoice == 'x':
                break
            if strCDChoice == 'a':
                print('Add Track:\n')
                tplTrkInfo = IO.ScreenIO.get_track_info()
                PC.DataProcessor.add_track(tplTrkInfo, cd)
                IO.ScreenIO.show_tracks(cd)
                continue #returns to sub-menu
            elif strCDChoice == 'd':
                print('Display CD/Album Details:')
                IO.ScreenIO.show_tracks(cd)
                continue #returns to sub-menu
            elif strCDChoice == 'r':
                print('Remove Track:')
                IO.ScreenIO.show_tracks(cd)
                if cd.cd_tracks != []: #test to see if there are any tracks to delete
                    track_idx = input('Select the Track: ')
                    cd.rmv_track(track_idx)
                else: 
                    print('There are no Tracks to delete.')
                continue #returns to sub-menu
            else: 
                print('General Error. Returning to Main Menu.')
                break #returns to main menu
    elif strChoice == 's':
        IO.ScreenIO.show_inventory(lstOfCDObjects)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        if strYesNo == 'y':
            IO.FileIO.save_inventory(lstFileNames, lstOfCDObjects)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    else:
        print('General Error')