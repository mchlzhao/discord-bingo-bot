from datetime import datetime
from typing import Dict, List

game_store: List[Dict] = [{
    'server_id': '0',
    'time_started': datetime.now(),
    'time_finished': None,
    'events': [{
        'desc': 'Test Event',
        'index': 0,
        'is_hit': False
    }],
    'player_entries': [],
    'player_win_order': []
}]

sample_player_entry = {
    'player_id': '0',
    'combos': [{'event_index': 0}]
}
