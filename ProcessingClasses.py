#------------------------------------------#
# Title: Processing Classes
# Desc: A Module for processing Classes
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# DBiesinger, 2030-Jan-02, Extended functionality to add tracks
# CBuffalow, 2021-Mar-13, Added select_CD & add_track methods
# CBuffalow, 2021-Mar-14, Added calculate_cd_id method
#------------------------------------------#

if __name__ == '__main__':
    raise Exception('This file is not meant to ran by itself')

import DataClasses as DC

class DataProcessor:
    """Processing the data in the application
    
    Methods:
        add_CD(CDInfo: tuple), table: list) -> None
        select_cd(table: list, cd_idx: int) -> DC.CD:
        add_track(track_info: tuple, cd: DC.CD) -> None
        calculate_cd_id(table) -> cd_id: int
    
    """
    @staticmethod
    def add_CD(CDInfo, table):
        """function to add CD info in CDinfo to the inventory table.


        Args:
            CDInfo (tuple): Holds information (ID, CD Title, CD Artist) to be added to inventory.
            table (list of obj): 2D data structure (list of obj) that holds the data during runtime.

        Returns:
            None.

        """

        cdId, title, artist = CDInfo
        try:
            cdId = int(cdId)
            row = DC.CD(cdId, title, artist)
            table.append(row)
        except ValueError:
            print('ID must be an Integer!')
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n')

    @staticmethod
    def select_cd(table: list, cd_idx: int) -> DC.CD:
        """selects a CD object out of table that has the ID cd_idx

        Args:
            table (list): Inventory list of CD objects.
            cd_idx (int): id of CD object to return

        Raises:
            Exception: If ID is not in list.

        Returns:
            row (DC.CD): CD object that matches cd_idx

        """
        CD_found = False #flag to determine if CD found
        try:
            for cd in table:
                if cd.cd_id == int(cd_idx): #if id number of object matches input id number
                    CD_found = True
                    return cd #returns CD object once found
            if CD_found == False: #if CD not found after for loop, raising Exception
                raise Exception('CD not found.')
        except ValueError as e:
            print('CD ID must be an Integer!', e, e.__doc__, type(e), sep='\n')
        except Exception as e:
            print(e, e.__doc__, type(e), sep='\n')


    @staticmethod
    def add_track(track_info: tuple, cd: DC.CD) -> None:
        """adds a Track object with attributes in track_info to cd


        Args:
            track_info (tuple): Tuple containing track info (position, title, Length).
            cd (DC.CD): cd object the tarck gets added to.

        Raises:
            Exception: If position is not an integer.

        Returns:
            None.

        """

        position, title, length = track_info
        try:
            position = int(position)
            track = DC.Track(position, title, length) #creating track object
            cd.add_track(track) #adding track object to cd object
        except ValueError:
            print('Position must be an Integer!\n')
        except Exception as e:
            print(e, e.__doc__, type(e), sep='\n')
        
    @staticmethod
    def calculate_cd_id(table):
        """Function to determine the appropriate ID number for the CD.

        The function finds the last row of data in the current inventory and reports 
        the ID number used in that row.  The function then adds 1 to the ID number
        to be used on the next CD.

        Args:
            table (list of dict): 2D data structure (list of dicts)

        Returns:
            cd_id (int): ID number for the CD
        """

        try: 
            tableIndex = len(table) -1 #getting index of final row of inventory
            cd = table[tableIndex] #returning CD object in final row of inventory
            cd_id = int(cd.cd_id) #returning ID number of this CD
            cd_id += 1 #generating next ID number
        except IndexError:  #the IndexError will occur any time the table is empty & is not alarming, so simply assigning cd_id = 1 (1st entry)
            cd_id = 1
        except Exception as e: #in case something weird happens - still handling by assigning cd_id = 1
            cd_id = 0
            print('There has been a ', type(e), ' error.')
        finally:
            return cd_id
