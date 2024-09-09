#main program file for managing bike database

import utils
from error_handling import handle_errors

@handle_errors(custom_info="main")
def main():
    #create an instance of the database
    bike_db = utils.DatabaseUtils()
    #instance of logging
    logger = utils.LogUtils()
    
    
    #create an instance of the user input class
    user_input = utils.MenuUtils()
    #loop through asking for user input
    while True:
        #ask user for input
        user_input.get_user_input()
        top_level_arbitration(user_input)
        #if user wants to exit, break the loop
    

#make choice for db
@handle_errors(custom_info="top_level_arbitration decision")
def top_level_arbitration(menu_obj):
    #is input a db command?
    if menu_obj.user_selection_type() == "db":
        pass
    elif menu_obj.user_selection_type() == "stat":
        pass
    elif menu_obj.user_selection_type() == "exit":
        raise SystemExit
    else:
        #if not, display an error message
        raise ValueError("Invalid command. Please try again.")

#function to arbitrage db command execution
@handle_errors(custom_info="db_arbitration")
def db_arbitration(menu_obj):
    #is input a db command?
    if menu_obj.user_selection_type() == "add":
        pass
    elif menu_obj.user_selection_type() == "view":
        pass
    elif menu_obj.user_selection_type() == "delete":
        pass
    elif menu_obj.user_selection_type() == "update":
        pass
    elif menu_obj.user_selection_type() == "exit":
        raise SystemExit
    else:
        #if not, display an error message
        raise ValueError("Invalid command. Please try again.")

#function to arbitrage stat command execution
@handle_errors(custom_info="stat_arbitration")
def stat_arbitration(menu_obj):
    #is input a db command?
    if menu_obj.user_selection_type() == "view":
        pass
    elif menu_obj.user_selection_type() == "exit":
        raise SystemExit
    else:
        #if not, display an error message
        raise ValueError("Invalid command. Please try again.")

#function to view table entries

if __name__ == '__main__':
    main()
