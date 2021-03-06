import unittest
from datetime import datetime
from typing import List
from unittest.mock import ANY, Mock

from src.core.game_engine import GameEngine
from src.core.game_engine_response import GameEngineResponse
from src.entities.combo import Combo
from src.entities.combo_set import ComboSet
from src.entities.entry import Entry
from src.entities.event import Event
from src.entities.game import Game


class TestGameEngine(unittest.TestCase):
    def setUp(self):
        self.event_repo = Mock()
        self.game_repo = Mock()
        self.player_repo = Mock()
        self.engine = GameEngine(self.event_repo, self.game_repo,
                                 self.player_repo)

        self.fake_server_id = 'server_id'
        self.fake_player_id = 'player_id'
        self.fake_game = Game(0, self.fake_server_id, datetime.now(), None)
        self.fake_entry = Entry(0, self.fake_game.game_id, self.fake_player_id,
                                None)
        self.fake_event = Event(0, self.fake_game.game_id, 'event', 0)
        self.fake_event2 = Event(1, self.fake_game.game_id, 'event2', 1)
        self.fake_combo = Combo(None, [self.fake_event], 0)
        self.fake_combo_set = ComboSet(self.fake_player_id, [self.fake_combo])

    def assertResponseDisplayErrorContains(self, response: GameEngineResponse,
                                           display_error: str):
        self.assertIn(display_error, response.display_error)

    def assertResponseHasKeys(self, response: GameEngineResponse,
                              keys: List[str]):
        self.assertIsNone(response.display_error)
        for key in keys:
            self.assertIn(key, response.response)

    def test_start_game(self):
        self.game_repo.read_active_game.return_value = None
        self.game_repo.create_game.return_value = self.fake_game
        self.assertResponseHasKeys(
            self.engine.start_game(self.fake_server_id, []),
            ['events'])
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.game_repo.create_game.assert_called_once_with(self.fake_server_id)
        self.event_repo.create_events.assert_called_once_with(
            self.fake_game.game_id, [])

    def test_start_game_game_running(self):
        self.game_repo.read_active_game.return_value = \
            Game(None, self.fake_server_id, datetime.now(), None)
        self.assertResponseDisplayErrorContains(
            self.engine.start_game(self.fake_server_id, []),
            'A game is already running.'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.game_repo.create_game.assert_not_called()
        self.event_repo.create_events.assert_not_called()

    def test_finish_game(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.player_repo.read_all_entries.return_value = []
        self.assertResponseHasKeys(
            self.engine.finish_game(self.fake_server_id),
            ['winning_entries', 'events'])

        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.game_repo.update_game.assert_called_once()
        self.player_repo.read_all_entries.assert_called_once_with(
            self.fake_game.game_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)

    def test_finish_game_no_game_running(self):
        self.game_repo.read_active_game.return_value = None
        self.assertResponseDisplayErrorContains(
            self.engine.finish_game(self.fake_server_id),
            'No game is currently running.'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.game_repo.update_game.assert_not_called()
        self.player_repo.read_all_entries.assert_not_called()
        self.event_repo.read_all_events.assert_not_called()

    def test_set_entry(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.event_repo.read_all_events.return_value = [self.fake_event]
        self.assertResponseHasKeys(
            self.engine.set_entry(self.fake_server_id, self.fake_player_id, []),
            []
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)
        self.player_repo.delete_entry.assert_called_once_with(
            self.fake_game.game_id, self.fake_player_id)
        self.player_repo.create_entry.assert_called_once_with(
            self.fake_game.game_id, ANY)

    def test_set_entry_no_game_running(self):
        self.game_repo.read_active_game.return_value = None
        self.assertResponseDisplayErrorContains(
            self.engine.set_entry(self.fake_server_id, self.fake_player_id, []),
            'No game is currently running.'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.read_all_events.assert_not_called()
        self.player_repo.delete_entry.assert_not_called()
        self.player_repo.create_entry.assert_not_called()

    def test_set_entry_event_already_hit(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.fake_event.is_hit = True
        self.event_repo.read_all_events.return_value = [self.fake_event]
        self.assertResponseDisplayErrorContains(
            self.engine.set_entry(self.fake_server_id, self.fake_player_id, []),
            'Cannot add/change entry as events have already been hit.'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)
        self.player_repo.delete_entry.assert_not_called()
        self.player_repo.create_entry.assert_not_called()

    def test_set_entry_invalid_event_index(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.event_repo.read_all_events.return_value = [self.fake_event]
        self.assertResponseDisplayErrorContains(
            self.engine.set_entry(self.fake_server_id, self.fake_player_id,
                                  [[1]]),
            'invalid event index'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)
        self.player_repo.delete_entry.assert_not_called()
        self.player_repo.create_entry.assert_not_called()

    def test_change_hit_hit_index(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.event_repo.read_all_events.return_value = [self.fake_event]
        self.assertResponseHasKeys(
            self.engine.change_hit(self.fake_server_id, True, index=0),
            ['event']
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)
        self.event_repo.update_event.assert_called_once_with(
            self.fake_game.game_id, self.fake_event)

    def test_change_hit_hit_desc(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.event_repo.read_all_events.return_value = [self.fake_event]
        self.assertResponseHasKeys(
            self.engine.change_hit(self.fake_server_id, True, desc='event'),
            ['event']
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)
        self.event_repo.update_event.assert_called_once_with(
            self.fake_game.game_id, self.fake_event)

    def test_change_hit_hit_desc_case_insensitive(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.event_repo.read_all_events.return_value = [self.fake_event]
        self.assertResponseHasKeys(
            self.engine.change_hit(self.fake_server_id, True, desc='EVENT'),
            ['event']
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)
        self.event_repo.update_event.assert_called_once_with(
            self.fake_game.game_id, self.fake_event)

    def test_change_hit_no_game_running(self):
        self.game_repo.read_active_game.return_value = None
        self.assertResponseDisplayErrorContains(
            self.engine.change_hit(self.fake_server_id, True, index=0),
            'No game is currently running.'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.update_event.assert_not_called()

    def test_change_hit_invalid_index(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.event_repo.read_all_events.return_value = [self.fake_event]
        self.assertResponseDisplayErrorContains(
            self.engine.change_hit(self.fake_server_id, True, index=1),
            'Invalid event index.'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)
        self.event_repo.update_event.assert_not_called()

    def test_change_hit_no_match_desc(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.event_repo.read_all_events.return_value = [self.fake_event]
        self.assertResponseDisplayErrorContains(
            self.engine.change_hit(self.fake_server_id, True, desc='event1'),
            'No event description matches'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)
        self.event_repo.update_event.assert_not_called()

    def test_change_hit_multiple_matches_desc(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.event_repo.read_all_events.return_value = [self.fake_event,
                                                        self.fake_event2]
        self.assertResponseDisplayErrorContains(
            self.engine.change_hit(self.fake_server_id, True, desc='event'),
            'More than one event description matches'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)
        self.event_repo.update_event.assert_not_called()

    def test_change_hit_hit_already_hit(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.fake_event.is_hit = True
        self.event_repo.read_all_events.return_value = [self.fake_event]
        self.assertResponseDisplayErrorContains(
            self.engine.change_hit(self.fake_server_id, True, index=0),
            'already been hit'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)
        self.event_repo.update_event.assert_not_called()

    def test_change_hit_unhit_already_unhit(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.event_repo.read_all_events.return_value = [self.fake_event]
        self.assertResponseDisplayErrorContains(
            self.engine.change_hit(self.fake_server_id, False, index=0),
            'already unhit'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)
        self.event_repo.update_event.assert_not_called()

    def test_bingo(self):
        self.fake_event.is_hit = True
        self.game_repo.read_active_game.return_value = self.fake_game
        self.player_repo.read_entry.return_value = self.fake_entry
        self.player_repo.read_combo_set.return_value = self.fake_combo_set
        self.assertResponseHasKeys(
            self.engine.bingo(self.fake_server_id, self.fake_player_id),
            []
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.player_repo.read_entry.assert_called_once_with(
            self.fake_game.game_id, self.fake_player_id)
        self.player_repo.read_combo_set.assert_called_once_with(
            self.fake_game.game_id, self.fake_player_id)
        self.player_repo.update_entry.assert_called_once_with(ANY)

    def test_bingo_no_game_running(self):
        self.game_repo.read_active_game.return_value = None
        self.assertResponseDisplayErrorContains(
            self.engine.bingo(self.fake_server_id, self.fake_player_id),
            'No game is currently running.'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.player_repo.read_entry.assert_not_called()
        self.player_repo.read_combo_set.assert_not_called()
        self.player_repo.update_entry.assert_not_called()

    def test_bingo_invalid_player(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.player_repo.read_entry.return_value = None
        self.player_repo.read_combo_set.return_value = self.fake_combo_set
        self.assertResponseDisplayErrorContains(
            self.engine.bingo(self.fake_server_id, self.fake_player_id),
            'not in the game'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.player_repo.read_entry.assert_called_once_with(
            self.fake_game.game_id, self.fake_player_id)
        self.player_repo.read_combo_set.assert_not_called()
        self.player_repo.update_entry.assert_not_called()

    def test_bingo_already_won(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.fake_entry.time_won = datetime.now()
        self.player_repo.read_entry.return_value = self.fake_entry
        self.player_repo.read_combo_set.return_value = self.fake_combo_set
        self.assertResponseDisplayErrorContains(
            self.engine.bingo(self.fake_server_id, self.fake_player_id),
            'already won'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.player_repo.read_entry.assert_called_once_with(
            self.fake_game.game_id, self.fake_player_id)
        self.player_repo.read_combo_set.assert_not_called()
        self.player_repo.update_entry.assert_not_called()

    def test_bingo_no_bingo(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.player_repo.read_entry.return_value = self.fake_entry
        self.player_repo.read_combo_set.return_value = self.fake_combo_set
        self.assertResponseDisplayErrorContains(
            self.engine.bingo(self.fake_server_id, self.fake_player_id),
            'not yet won'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.player_repo.read_entry.assert_called_once_with(
            self.fake_game.game_id, self.fake_player_id)
        self.player_repo.read_combo_set.assert_called_once_with(
            self.fake_game.game_id, self.fake_player_id)
        self.player_repo.update_entry.assert_not_called()

    def test_view_events(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.event_repo.read_all_events.return_value = [self.fake_event]
        self.assertResponseHasKeys(
            self.engine.view_events(self.fake_server_id),
            ['events']
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)

    def test_view_events_sort_by_index(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.event_repo.read_all_events.return_value = [self.fake_event2,
                                                        self.fake_event]
        response = self.engine.view_events(self.fake_server_id)
        self.assertResponseHasKeys(response, ['events'])
        self.assertEqual(response.response['events'],
                         [self.fake_event, self.fake_event2])
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)

    def test_view_events_no_game_running(self):
        self.game_repo.read_active_game.return_value = None
        self.assertResponseDisplayErrorContains(
            self.engine.view_events(self.fake_server_id),
            'No game is currently running.'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.event_repo.read_all_events.assert_not_called()

    def test_view_progress_not_started(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.player_repo.read_all_combo_sets.return_value = self.fake_combo_set
        self.event_repo.read_all_events.return_value = [self.fake_event]
        response = self.engine.view_progress(self.fake_server_id)
        self.assertResponseHasKeys(response, ['combo_sets', 'game_has_started'])
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.player_repo.read_all_combo_sets.assert_called_once_with(
            self.fake_game.game_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)
        self.assertFalse(response.response['game_has_started'])

    def test_view_progress_has_started(self):
        self.fake_event.is_hit = True
        self.game_repo.read_active_game.return_value = self.fake_game
        self.player_repo.read_all_combo_sets.return_value = self.fake_combo_set
        self.event_repo.read_all_events.return_value = [self.fake_event]
        response = self.engine.view_progress(self.fake_server_id)
        self.assertResponseHasKeys(response, ['combo_sets', 'game_has_started'])
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.player_repo.read_all_combo_sets.assert_called_once_with(
            self.fake_game.game_id)
        self.event_repo.read_all_events.assert_called_once_with(
            self.fake_game.game_id)
        self.assertTrue(response.response['game_has_started'])

    def test_view_progress_no_game_running(self):
        self.game_repo.read_active_game.return_value = None
        self.assertResponseDisplayErrorContains(
            self.engine.view_progress(self.fake_server_id),
            'No game is currently running.'
        )
        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.player_repo.read_all_combo_sets.assert_not_called()
        self.event_repo.read_all_events.assert_not_called()

    def test_view_winners(self):
        self.game_repo.read_active_game.return_value = self.fake_game
        self.player_repo.read_all_entries.return_value = []
        self.assertResponseHasKeys(
            self.engine.finish_game(self.fake_server_id),
            ['winning_entries'])

        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.player_repo.read_all_entries.assert_called_once_with(
            self.fake_game.game_id)

    def test_view_winners_no_game_running(self):
        self.game_repo.read_active_game.return_value = None
        self.assertResponseDisplayErrorContains(
            self.engine.finish_game(self.fake_server_id),
            'No game is currently running.'

        )

        self.game_repo.read_active_game.assert_called_once_with(
            self.fake_server_id)
        self.player_repo.read_all_entries.assert_not_called()
