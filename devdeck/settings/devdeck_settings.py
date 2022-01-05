import yaml
from cerberus import Validator
import re

from devdeck.settings.deck_settings import DeckSettings
from devdeck.settings.validation_error import ValidationError

schema = {
    'decks': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'serial_number': {
                    'type': 'string',
                    'required': True
                },
                'name': {
                    'type': 'string',
                    'required': True
                },
                'priority': {
                    'type': 'number',
                    'required': True
                },
                'match': {
                    'type': 'list',
                    'required': True,
                    'schema': {
                        'type': 'string'
                    }
                },
                'settings': {
                    'type': 'dict',
                    'required': True
                }
            }
        }
    }
}

def priorityKey(val):
    return val.priority()


class DevDeckSettings:
    def __init__(self, settings):
        self.settings = settings

    def deck(self, serial_number, window_title):
        if window_title is None:
            window_title = ''

        deck_settings = self.decks()

        settings_for_deck = None
        for index, deck_setting in enumerate(deck_settings):
            if deck_setting.serial_number() == serial_number[0:12]:
                #regex = re.compile(deck_setting.match(), re.IGNORECASE)
                for match in deck_setting.match():
                    if match in window_title.lower():
                        deck_setting.set_identifier(index)
                        settings_for_deck = deck_setting
                        break
            if settings_for_deck is not None:
                break

        if settings_for_deck is not None:
            return settings_for_deck
        return None

    def decks(self):
        deck_settings = [DeckSettings(deck_setting) for deck_setting in self.settings['decks']]
        deck_settings.sort(key=priorityKey)
        return deck_settings

    @staticmethod
    def load(filename):
        with open(filename, 'r') as stream:
            settings = yaml.safe_load(stream)

            validator = Validator(schema)
            if validator.validate(settings, schema):
                return DevDeckSettings(settings)
            raise ValidationError(validator.errors)

    @staticmethod
    def generate_default(filename, serial_numbers):
        default_configs = []
        for serial_number in serial_numbers:
            deck_config = {
                'serial_number': serial_number,
                'name': 'devdeck.decks.single_page_deck_controller.SinglePageDeckController',
                'match': [
                    ''
                ],
                'prority': 0,
                'settings': {
                    'controls': [
                        {
                            'name': 'devdeck.controls.clock_control.ClockControl',
                            'key': 0
                        }
                    ]
                }
            }
            default_configs.append(deck_config)
        with open(filename, 'w') as f:
            yaml.dump({'decks': default_configs}, f)
