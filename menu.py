#a python script containing class that manages console based user inputs

import os
import log_config
import json
import tabulate

from log_config import LogConfig
log_config = LogConfig()
logger = log_config.get_logger()

#the user input will provide the user with a left justified box with menu items
#exmple:
#--------------------------------
#| 1. Bike db                   |
#| 2. charging db               |
#| 3. expense db                |
#| 4. service db                |
#| 5. exit                      |
#--------------------------------
#the user will then enter a number to select the menu item
#
#
#
#

#A class that dynamicaly generates text based menus whose hierarchy is defined by a dictionary {menu_item: sub_menu, menu: {sub_menu: sub_menu}}
#for example
#menu = {
#    "1. Bike db": {
#        "1.1. Add bike": None,
#        "1.2. View bikes": None,
#        "1.3. Update bike": None,
#        "1.4. Delete bike": None
#    },
#The class will then generate a menu that looks like this:
#--------------------------------
#| 1. Bike db                   |
#| 2. charging db               |
#| 3. expense db                |
#| 4. service db                |
#| 5. exit                      |
#--------------------------------

class user_terminal_input:
    #initialise the class with a menu
    def __init__(self):
        self.menu_hierarchy = self.get_menu()
        self.menu_tracker = []
        self.menu_tracker_name = []
        self.return_word = 'back'


    #get menu hierarchy from json file config/menu_config.json
    def get_menu(self):
        with open('config/menu_config.json', 'r') as file:
            data = json.load(file)
        return data['menu']
    
    def set_tracker_name(self, list):
        self.menu_tracker_name = list
        
    def get_tracker_name(self):
        return self.menu_tracker_name

    def get_menu_hierarchy(self):
        return self.menu_hierarchy
    
    def is_primitive(self, data):
    #checks if list item is a primitive by checking if dictionary contains a key called 'submenus'
        if 'submenus' in data:
            return False
        else:
            return True

    def get_user_input(self):
        user_input = input('Enter a number to select a menu item: ')
        return user_input

    def draw_menu(self, list):
        print("--------------------------------")
        for number,menu_item in enumerate(list):
            print(f"| {number}. {menu_item['name']} ")
        print("--------------------------------")

    def cmd_navigate(self):
        #navigate the menu
        self.clear_navigation()
        self.menu_navigation(self.menu_hierarchy)
        return self.menu_tracker

    def clear_navigation(self):
        #clears the menu tracker
        self.menu_tracker = []
        self.menu_tracker_name = []

    def menu_navigation(self, menu):
        
        self.draw_menu(menu)
        menu_items = []
        for item in menu: 
            menu_items.append(item['name'])
        user_selection = int(self.get_user_input())
        self.menu_tracker.append(user_selection)
        self.print_navigation()

        if self.return_word == str.lower(menu_items[user_selection]):
            self.menu_tracker.pop()
            if len(self.menu_tracker) == 0:
                return 0
            return -1

        elif self.is_primitive(menu[user_selection]):
            print(f"Selected: {menu[user_selection]['name']}")
        else:
            if self.menu_navigation(menu[user_selection]['submenus']) ==-1:
                self.menu_tracker.pop()
                if self.menu_navigation(menu) == -1:
                    self.menu_tracker.pop()
                    return -1

    def print_navigation(self):
        list = []
        self.convert_val_to_name(self.menu_tracker, self.menu_hierarchy, list)
        print(list)

    def user_input_values(self):
        return self.menu_tracker

    def convert_val_to_name(self, menu_track, menu,list):
        #recursive function to get the menu item from the menu hierarchy
        if len(menu_track[1:]) == 0:
            list.append(menu[menu_track[0]]['name'])
            return list
        else:
            list.append(menu[menu_track[0]]['name'])
            self.convert_val_to_name(menu_track[1:], menu[menu_track[0]]['submenus'], list)        

    #display table
    def display_table(self, table_data):
        print(tabulate.tabulate(table_data,  headers='keys', tablefmt="grid"))

if __name__ == "__main__":
    #user_input = user_terminal_input()
    #user_input.get_user_input()
    #selected_menu = user_input.show_menu_item()
    #print(user_input.user_input_values())
    #print(selected_menu)
    pass