#a python script containing class that manages console based user inputs

import os
import log_config
import json

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


    #get menu hierarchy from json file config/menu_config.json
    def get_menu(self):
        with open('config/menu_config.json', 'r') as file:
            data = json.load(file)
        return data['menu']
    
    def get_menu_hierarchy(self):
        return self.menu_hierarchy
    
    def is_primitive(self, data):
    #checks if list item is a primitive by checking if dictionary contains a key called 'submenus'
        if 'submenus' in data:
            return False
        else:
            return True

    def menu_crawl(self, list):
        self.draw_menu(list)
        user_selection = int(input('Enter a number to select a menu item: '))
        if self.is_primitive(list[user_selection]):
            print(f"Selected: {list[user_selection]['name']}")
            self.menu_tracker.append(user_selection)
        else:
            self.menu_tracker.append(user_selection)
            self.menu_crawl(list[user_selection]['submenus'])   

    def draw_menu(self, list):
        print("--------------------------------")
        for number,menu_item in enumerate(list):
            print(f"| {number}. {menu_item['name']} ")
        print("--------------------------------")

    def get_user_input(self):
        self.menu_crawl(self.menu_hierarchy)

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
    
if __name__ == "__main__":
    user_input = user_terminal_input()
    user_input.get_user_input()
    selected_menu = user_input.show_menu_item()
    print(user_input.user_input_values())
    print(selected_menu)


    
    
        