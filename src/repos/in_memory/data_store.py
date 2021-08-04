from datetime import datetime
from typing import Dict

game_store: Dict = {
    -1: {
        'server_id': '0',
        'time_started': datetime.now(),
        'time_finished': None
    }
}


def get_game_store():
    global game_store
    return game_store


def clear_game_store():
    global game_store
    game_store = {}


def read_game(game_id):
    return game_store[game_id]


def write_game(game_id, game_dict):
    game_store[game_id] = game_dict


event_store: Dict = {
    -1: []
}


def get_events_from_game(game_id):
    return event_store[game_id]


def add_events_to_game(game_id, events):
    event_store[game_id].extend(events)


def update_event_by_index(game_id, event):
    event_store[game_id][event.index] = event
