import random
import re

from .mc import mc

class PrettyColors:

    def __init__(self):
        self.color_dict = mc
        self.reset_available_colors()

    def color_names(self):
        """
        Returns the color class names without any numbers
        """
        return sorted(list(set([re.sub(r'(A?\d+)$', '', key) for key, _ in self.color_dict.items()])))

    def __getattr__(self, name):
        """
        A simple way to access colors from the PrettyColors class.

        Usage: c.RED or c.RED900
        This method allows you to access colors as attributes of the class.

        Args:
            name (str): The name of the attribute being accessed.

        Returns:
            Any: The value associated with the resolved attribute name in `color_dict`.

        Raises:
            AttributeError: If the resolved attribute name is not found in `color_dict`.
        """

        if name not in self.color_dict and not bool(re.search(r'\d{2,3}$', name)):
            name += "500"

        if name in self.color_dict:
            return self.get(name)

        raise AttributeError(f"'PrettyColors' object has no attribute '{name}'")

    def __getitem__(self, key):
        return getattr(self, key)

    def reset_available_colors(self):
        """
        Resets the list of available colors to all color keys.
        Call this if you want to start over with unique selections.
        """
        self._available_colors = list(self.color_dict.keys())

    def get(self, name):
        """
        Retrieve the hex code for a given color name.
        If the provided color name does not include a dash (indicating a shade),
        the default shade '-500' is appended.

        Examples:
            "red" becomes "red-500"
            "red-100" stays "red-100"
            "red-a100" stays "red-a100"

        Args:
            color_name (str): The name of the color (e.g., "red" or "red-500").

        Returns:
            str or None: The hex code if found, otherwise None.
        """
        if not bool(re.search(r'\d{2,3}$', name)):
            name += "500"

        return self.color_dict.get(name)

    def list_colors(self):
        """
        Returns a list of all available color keys as defined in the JSON file.

        Returns:
            list: A list of color names (e.g., "red-50", "red-100", ...)
        """
        return list(self.color_dict.keys())

    def random(self, repeat=False):
        """
        Returns a random color's hex code from the dictionary.

        Args:
            repeat (bool): If True, the same color may be picked multiple times.

        Returns:
            str: A random hex code from the color dictionary.
        """
        if repeat:
            return self.__get_random_color()
        return self.__get_random_color_no_repeat()


    def __get_random_color(self):
        """
        Returns a random color's hex code from the dictionary (duplicates possible).

        Returns:
            str: A random hex code from the color dictionary.
        """
        key = random.choice(list(self.color_dict.keys()))
        return self.color_dict[key]

    def __get_random_color_no_repeat(self):
        """
        Returns a random color's hex code from the dictionary,
        ensuring that the same color is not picked twice until all colors have been used.

        Returns:
            str: A random hex code from the color dictionary.

        Raises:
            ValueError: If no more unique colors are available.
        """
        if not self._available_colors:
            raise ValueError("No more unique colors available. Consider resetting available colors.")
        key = random.choice(self._available_colors)
        self._available_colors.remove(key)
        return self.color_dict[key]

    def __dir__(self):
        default_dir = super().__dir__()
        additional = self.color_names()
        return sorted(set(default_dir + additional))

colors = PrettyColors()
