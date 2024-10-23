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
        top_level_arbitration(user_input, bike_db)
        #if user wants to exit, break the loop
    

#make choice for db
@handle_errors(custom_info="top_level_arbitration decision")
def top_level_arbitration(menu_obj, bike_db):
    #is input a db command?
    if menu_obj.user_selection_type() == "db":
        db_arbitration(menu_obj, bike_db)
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
def db_arbitration(menu_obj, bike_db):
    #is input a db command?
    user_sub_selection = menu_obj.get_submenu_options()[0]
    
    if user_sub_selection == "add_entry":
        table_name = menu_obj.get_selected_db_name()
        menu_obj.display_table_headers(table_name)
        new_row_data = menu_obj.get_entry_input(table_name)
        bike_db.add_row(table_name, new_row_data, "script")
        
    elif user_sub_selection == "view":
        #show table for selected db. display_table(get_table(user selection))
        table_name = menu_obj.get_selected_db_name()
        table_data = bike_db.get_all_rows(table_name)
        menu_obj.display_table(table_data)

    elif user_sub_selection == "delet_entry":
        table_name = menu_obj.get_selected_db_name()
        menu_obj.delete_menu(table_name)
        
    elif user_sub_selection == "adjust_entry":
        table_name = menu_obj.get_selected_db_name()
        menu_obj.edit_menu(table_name)
    
    elif user_sub_selection == "export_csv":
        table_name = menu_obj.get_selected_db_name()
        bike_db.export_table(table_name, f'{table_name}.csv')

    elif user_sub_selection == "import_csv":
        table_name = menu_obj.get_selected_db_name()
        print(table_name)
        bike_db.import_table(table_name, f'{table_name}.csv')

    elif user_sub_selection == "exit":
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
