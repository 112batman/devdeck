import importlib
from operator import itemgetter


class DeckSettings:
    def __init__(self, config):
        self.config = config
        self.config['settings']['controls'] = sorted(self.config['settings']['controls'], key=itemgetter('key'))

    def serial_number(self):
        return self.config['serial_number']

    def settings(self):
        return self.config['settings']

    def deck_class(self):
        module_name, class_name = self.config['name'].rsplit(".", 1)
        return getattr(importlib.import_module(module_name), class_name)

    def match(self):
        return self.config['match']

    def priority(self):
        return self.config['priority']

    def set_identifier(self, index):
        self.config['identifier'] = self.serial_number() + '$' + str(index)

    def identifier(self):
        return self.config['identifier']