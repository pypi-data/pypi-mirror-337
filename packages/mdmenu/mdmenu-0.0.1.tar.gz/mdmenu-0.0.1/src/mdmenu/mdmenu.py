

# TODO - Footer
# TODO - Title
# TODO - Tests

import textwrap


# """
# Create a string for the footer of the menu. If footer_content is defined, it is formatted and included in the
# string returned as the footer.

# :param param1: this is a first param
# :param param2: this is a second param
# :returns: this is a description of what is returned
# :raises keyError: raises an exception
# """


class Menu(object):
    menu_items = {}
    menu_name = "Menu"
    menu_character = "#"
    menu_width = 80
    menu_hold_last = True
    title = True
    title_border = True
    title_padding = " "
    title_preface = None
    footer = True
    footer_content = None

    def __init__(self, menu_items: dict[int, tuple] | None = None) -> None:
        if menu_items is None:
            self.menu_items = {1: ("Exit", exit)}
        else:
            self.menu_items = menu_items

    def __str__(self) -> str:
        """
        Creates a representation of the menu to be displayed to the console.

        :returns str: Formatted menu test of the menu
        """
        output: str = ""

        if self.title:
            output += self.create_title()

        for key in sorted(self.menu_items.keys()):
            # TODO - Add Left and right padding to key
            # TODO - Add Left padding to item
            output += f"{key} : {self.menu_items[key][0]}\n"

        if self.footer:
            output += self.create_footer()

        return output

    def create_footer(self) -> str:
        """
        Creates a string for the footer of the menu. If footer_content is defined, its formatted and included in the
        footer.

        :returns str: Formatted menu footer text
        """
        if self.footer_content is None:
            return self.create_border()

        return self.create_border() + self.format_content(self.footer_content) + self.create_border()

    def format_content(self, content: str) -> str:
        """
        Creates string formatted to the length specified by of self.menu_width long.

        :param content str: A string to be formatted to the width of the menu.

        :returns str: Formatted text
        """
        lines = textwrap.wrap(content, width=self.menu_width)
        # Backslashes are not allowed in the {} portion of f-strings
        newline = "\n"
        return f"{newline.join(lines)}\n"

    def create_title(self) -> str:
        """
        Creates title string of self.menu_name. When self.title_border is true the title sting is wrapped in a border
        string of self.menu_character that is self.menu_width characters long.

        :returns str: Formatted menu title text
        """
        output: str = ""
        if self.title_border:
            output += self.create_border()

        output += f"{self.menu_name:{self.title_padding}^{self.menu_width}}\n"

        if self.title_border:
            output += self.create_border()

        if self.title_preface is not None:
            output += self.format_content(self.title_preface) + self.create_border()

        return output

    def create_border(self) -> str:
        """
        Creates a border string of self.menu_character that is self.menu_width characters long.

        :returns str: A border string self.menu_width characters long
        """
        return f"{self.menu_width * self.menu_character}\n"

    def add_menu_item(self, item: tuple, key: int = None,) -> None:
        """
        Add a new menu item to the menu. If no key is given for the menu item the next available key is allocated. When
        self.menu_hold_last is True, the last item, typically an exit option, is renumbered to remain as the last item
        in the menu.

        :param item tuple: A tuple of the Menu item. (item_name, item_function)
        :param key int: The key to add the menu item with

        :raises ValueError: A ValueError is raised when a key which already exist is added.
        """
        # TODO - Add the ability to not hold the lst item with menu_hold_last
        # Get the exit menu item
        max_key = max(list(self.menu_items.keys()))
        last = self.menu_items.pop(max_key)

        if key is None:
            # When no key is specified get the next lowest key that is not already being used
            key = next(
                (i for i in range(1, max(list(self.menu_items.keys()))) if i not in self.menu_items.keys()), max_key)

        # Verify that the key to be added is not already in use
        if self.menu_items.get(key) is not None:
            # TODO: log a message if this throws an error
            max_key = max(list(self.menu_items.keys()))
            self.menu_items[max_key + 1] = last
            raise ValueError

        # Add the new key to the menu
        self.menu_items[key] = item
        # Reinsert the exit option to the end of the menu
        max_key = max(list(self.menu_items.keys()))
        self.menu_items[max_key + 1] = last

    def remove_menu_item(self, key: int) -> tuple:
        """
        Removes a menu item from the menu with the specified key.

        :param key int: The key of the menu item to remove.

        :returns tuple: The key and value removed from the menu

        :raises KeyError: A keyError is raised when a key which does not exist is removed from the menu
        """
        # TODO: log a message if this throws an error
        return self.menu_items.pop(key)


def invalid():
    print("INVALID CHOICE!")


if __name__ == "__main__":
    print("Running")

    def hello(my_str: str = ""):
        print(f"hello {my_str}")

    my_menu = Menu()
    print(my_menu)
    my_menu.add_menu_item(("Hello", hello), 3)

    print(my_menu)
    my_menu.add_menu_item(("Hello 2nd", hello))

    print(my_menu)
    my_menu.add_menu_item(("Hello 3nd", hello))

    print(my_menu)
    my_menu.add_menu_item(("Hello 4nd", hello))

    print(my_menu)
    my_menu.add_menu_item(("Hello 5nd", hello))

    print(my_menu)
    try:
        my_menu.add_menu_item(("Hello", hello), 3)
    except ValueError as e:
        print(e)

    print(my_menu)
    my_menu.remove_menu_item(3)

    print(my_menu)
    try:
        my_menu.remove_menu_item(3)
    except KeyError as e:
        print(e)

    my_menu.footer_content = "this is a big string "*20
    my_menu.title_preface = "this is a big string "*20

    print(my_menu)
    ans = input("Make A Choice")
    # my_menu.get(ans,[None,invalid])[1]()
    print(my_menu.menu_items.get(int(ans)))
    function_name, function_called = my_menu.menu_items.get(int(ans), [None, invalid])

    function_called("wold")
