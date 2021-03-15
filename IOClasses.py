#------------------------------------------#
# Title: IO Classes
# Desc: A Module for IO Classes
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# DBiesinger, 2030-Jan-02, Extended functionality to add tracks
# CBuffalow, 2021-Mar-13, Added save_inventory & load_inventory methods
# CBuffalow, 2021-Mar-14, Modified formatting of inventories (cd & tracks)
# CBuffalow, 2021-Mar-14, Modified formatting of menus (main & sub)
# CBuffalow, 2021-Mar 14, Modified get_cd_info method to accomodate cd_id generator
#------------------------------------------#

if __name__ == '__main__':
    raise Exception('This file is not meant to run by itself')

import DataClasses as DC
import ProcessingClasses as PC

class FileIO:
    """Processes data to and from file:

    properties:

    methods:
        save_inventory(file_names: list), lst_Inventory): -> None
        load_inventory(file_names: list): -> lst_Inventory (a list of CD objects)

    """
    @staticmethod
    def save_inventory(file_names: list, lst_inventory: list) -> None:
        """Saves data from current inventory into two txt files.
        
        CD info saved to file_name_CD (cd_id, cd_title, cd_artist).
        Track info saved to file_name_tracks (cd_id, track_position, track_title, track_length)
        Track info includes reference to the CD it came from via ID number.

        Args:
            file_names (list): list of file names [CD Inventory, Track Inventory] that hold the data.
            lst_Inventory (list): list of CD objects.

        Returns:
            None.

        """
        #separating files out from list
        file_name_CD = file_names[0]
        file_name_tracks = file_names[1]
        try:
            with open(file_name_CD, 'w') as file:
                for disc in lst_inventory:
                    file.write(disc.get_record())
            with open(file_name_tracks, 'w') as file:
                for disc in lst_inventory: #cycling through each CD
                    cd_id = disc.cd_id #save CD ID into variable
                    cd_tracks = disc.cd_tracks
                    for track in cd_tracks: #then cycle through each track on CD
                        if track is not None: #no need to save empty records...
                            file.write('{},{}'.format(cd_id,track.get_record()))
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n')

    @staticmethod
    def load_inventory(file_names: list) -> list:
        """Loads data from two text files into current inventory (list of CD objects).

        CD info comes from file_name_CD (cd_id, cd_title, cd_artist).
        Track info comes from file_name_tracks (cd_id, track_position, track_title, track_length)
        Track info includes reference to the CD it came from via ID number.

        Args:
            file_names (list): list of file names [CD Inventory, Track Inventory] that hold the data.

        Returns:
            list: list of CD objects.

        """
        #separating files out from list
        lst_Inventory = []
        file_name_CD = file_names[0]
        file_name_tracks = file_names[1]
        try:
            with open(file_name_CD, 'r') as file: #loading CD info
                for line in file:
                    data = line.strip().split(',')
                    row = DC.CD(data[0], data[1], data[2]) #creating cD object
                    lst_Inventory.append(row) #appending CD object to inventory list
            with open(file_name_tracks, 'r') as file: #loading track info
                for line in file:
                    data = line.strip().split(',')
                    cd_id = int(data[0]) #extracting CD ID from txt file
                    cd = PC.DataProcessor.select_cd(lst_Inventory, cd_id) #selecting CD obj
                    tplTrkInfo = (data[1], data[2], data[3]) #formatting track info into tuple
                    PC.DataProcessor.add_track(tplTrkInfo, cd) #adding track info to appropriate CD obj
        except FileNotFoundError as e:
            print('One or more data files is missing from the local folder!')
            print('Inventory not loaded.')
            print(e, e.__doc__, type(e), sep='\n')
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n')
        return lst_Inventory

class ScreenIO:
    """Handling Input / Output

    Methods:
        print_menu() -> None
        menu_choice() -> None
        print_CD_menu() -> None
        menu_CD_choice() -> None
        show_inventory(table) -> None
        show_tracks(cd obj) -> None
        get_CD_info(table: list) -> cdID (int), cdTitle (str), cdArtist(str)
        get_track_info() -> trkID (str), trkTitle (str), trkLength(str)
    
    """

    @staticmethod
    def print_menu() -> None:
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('\n')
        print('-'*30)
        print('Main Menu'.center(30))
        print('-'*30)
        print('[L] Load Inventory from file\n[A] Add CD / Album\n[D] Display Current Inventory')
        print('[C] Choose CD / Album\n[S] Save Inventory to file\n[X] Exit\n')

    @staticmethod
    def menu_choice() -> None:
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices L, A, D, C, S or X

        """
        choice = ' '
        while choice not in ['l', 'a', 'd', 'c', 's', 'x', 'L', 'A', 'D', 'C', 'S', 'X']:
            choice = input('Which operation would you like to perform? [L, A, D, C, S or X]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def print_CD_menu() -> None:
        """Displays a sub menu of choices for CD / Album to the user

        Args:
            None.

        Returns:
            None.
        """

        print('\n')
        print('-'*30)
        print('CD Sub Menu'.center(30))
        print('-'*30)
        print('[A] Add Track\n[D] Display CD / Album Details\n[R] Remove Track\n[X] Exit to Main Menu')

    @staticmethod
    def menu_CD_choice() -> None:
        """Gets user input for CD sub menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices A, D, R or X

        """
        choice = ' '
        while choice not in ['a', 'd', 'r', 'x', 'A', 'D', 'R', 'X']:
            choice = input('Which operation would you like to perform? [A, D, R or X]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table) -> None:
        """Displays current inventory table


        Args:
            table (list of obj): 2D data structure (list of obj) that holds the data during runtime.

        Returns:
            None.

        """
        print('\n')
        print(' The Current Inventory: '.center(60,'='))
        print('{:<10}{:<25}{:<25}'.format('ID', 'CD Title', 'Artist'))
        print('-'*60)
        for row in table:
            print(row)
        print('='*60)

    @staticmethod
    def show_tracks(cd) -> None:
        """Displays the Tracks on a CD / Album

        Args:
            cd (CD): CD object.

        Returns:
            None.

        """
        print(' Current CD / Album: '.center(60,'='))
        print('{:<10}{:<25}{:<25}'.format('ID', 'CD Title', 'Artist'))
        print('-'*60)
        print(cd)
        print('\n')
        print(' Tracks on this CD / Album: '.center(60,'='))
        print('{:<10}{:<25}{:<25}'.format('Pos.', 'Title', 'Length (MM:SS)'))
        print('-'*60)
        try:
            print(cd.get_tracks())
        except Exception as e:
            print(e)
        except:
            print('There was a general error!')
        print('='*60)

    @staticmethod
    def get_CD_info(table: list):
        """function to request CD information from User to add CD to inventory


        Returns:
            cdId (string): Holds the ID of the CD dataset.
            cdTitle (string): Holds the title of the CD.
            cdArtist (string): Holds the artist of the CD.

        """

        try:
            cdID = PC.DataProcessor.calculate_cd_id(table)
            cdTitle = input('What is the CD\'s title? ').strip()
            cdArtist = input('What is the Artist\'s name? ').strip()
            return cdID, cdTitle, cdArtist
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n')

    @staticmethod
    def get_track_info():
        """function to request Track information from User to add Track to CD / Album


        Returns:
            trkId (string): Holds the ID of the Track dataset.
            trkTitle (string): Holds the title of the Track.
            trkLength (string): Holds the length (time) of the Track.

        """

        try:
            trkId = input('Enter Position on CD / Album: ').strip()
            trkTitle = input('What is the Track\'s title? ').strip()
            trkLength = input('What is the Track\'s length? (MM:SS) ').strip()
            return trkId, trkTitle, trkLength
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n')
