#main program file for managing bike database

import utils

def main():
    #create an instance of the database
    bike_db = utils.DatabaseUtils()
    
    #create an instance of the user input class
    user_input = utils.MenuUtils()


    #loop through asking for user input
    
    #ask user for input
    user_input.get_user_input()

    #is input a db command?
    if user_input.is_db_command():
        

    else:
        #if not, display an error message
        print("Invalid command. Please try again.")

    

#function to view table entries
def db_action

if __name__ == '__main__':
    main()
