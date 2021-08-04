from datetime import datetime
from typing import Dict

game_store: Dict = {
    -1: {
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
    }
}
