from datetime import datetime
from typing import List, Optional

from src.core.displayable_error import DisplayableError
from src.entities.combo import Combo
from src.entities.combo_set import ComboSet
from src.entities.entry import Entry
from src.entities.event import Event
from src.entities.game import Game
from src.repos.abstract.ievent_repo import IEventRepo
from src.repos.abstract.igame_repo import IGameRepo
from src.repos.abstract.iplayer_repo import IPlayerRepo


class GameEngine:
    def __init__(self, event_repo: IEventRepo, game_repo: IGameRepo,
                 player_repo: IPlayerRepo):
        self.event_repo = event_repo
        self.game_repo = game_repo
        self.player_repo = player_repo

    def start_game(self, server_id: str, event_strs: List[str]) -> None:
        game = self.game_repo.read_active_game(server_id)
        if game is not None:
            raise DisplayableError('A game is already running.')

        game = self.game_repo.create_game(server_id)
        self.event_repo.create_events(game.game_id, event_strs)

    def finish_game(self, server_id: str) -> None:
        game = self.game_repo.read_active_game(server_id)
        if game is None:
            raise DisplayableError('No game is currently running.')

        game.time_finished = datetime.now()
        self.game_repo.update_game(game)

    def set_entry(self, server_id: str, player_id: str,
                  combo_set_indices: List[List[int]]) -> None:
        game = self.game_repo.read_active_game(server_id)
        events = self.event_repo.read_all_events(game.game_id)
        for event in events:
            if event.is_hit:
                raise DisplayableError(
                    'Cannot add/change entry as events have already been hit')

        self.player_repo.delete_entry(game.game_id, player_id)

        combos = []
        for combo_index, event_indices in enumerate(combo_set_indices):
            try:
                combos.append(Combo([events[i] for i in event_indices]))
            except IndexError:
                raise DisplayableError('Invalid event index.')
        combo_set = ComboSet(player_id, combos)

        self.player_repo.create_entry(game.game_id, combo_set)

    def _search_event(self, game_id, *, index: Optional[int],
                      desc: Optional[str]) -> Event:
        if index is not None:
            hit_event = self.event_repo.read_event_by_index(
                game_id, index)
            if hit_event is None:
                raise DisplayableError('Invalid event index.')
        elif desc is not None:
            hit_events = self.event_repo.read_events_by_desc(
                game_id, desc)
            if len(hit_events) == 0:
                raise DisplayableError(
                    'No event description matches search string.')
            elif len(hit_events) > 1:
                error_str = (
                    'More than one event description matches search string.\n'
                    'Matches include:\n'
                    f'{hit_events[0].desc}\n'
                    f'{hit_events[1].desc}'
                )
                if len(hit_events) > 2:
                    error_str += '\n...'
                raise DisplayableError(error_str)
            else:
                hit_event = hit_events[0]
        else:
            raise ValueError('No event has been specified.')
        return hit_event

    def hit(self, server_id: str, *, index: int = None, desc: str = None) \
            -> None:
        game = self.game_repo.read_active_game(server_id)
        hit_event = self._search_event(game.game_id, index=index, desc=desc)
        if hit_event.is_hit:
            raise DisplayableError((f'Event "{hit_event.desc}" ',
                                    'has already been hit.'))
        hit_event.is_hit = True
        self.event_repo.update_event(game.game_id, hit_event)

    def unhit(self, server_id: str, *, index: int = None, desc: str = None) \
            -> None:
        game = self.game_repo.read_active_game(server_id)
        unhit_event = self._search_event(game.game_id, index=index, desc=desc)
        if not unhit_event.is_hit:
            raise DisplayableError((f'Event "{unhit_event.desc}" ',
                                    'is already unhit.'))
        unhit_event.is_hit = False
        self.event_repo.update_event(game.game_id, unhit_event)

        # some players may have lost their win consequently
        combo_sets = self.player_repo.read_all_combo_sets(game.game_id)
        for combo_set in combo_sets:
            # TODO: optimise this
            entry = self.player_repo.read_entry(game.game_id,
                                                combo_set.player_id)
            if entry.time_won is not None and not combo_set.has_won():
                entry.time_won = None
                self.player_repo.update_entry(entry)

    def bingo(self, server_id: str, player_id: str) -> None:
        game = self.game_repo.read_active_game(server_id)
        entry = self.player_repo.read_entry(game.game_id, player_id)
        if entry.time_won is not None:
            raise DisplayableError('Entry has already won.')

        combo_set = self.player_repo.read_combo_set(game.game_id, player_id)
        if combo_set.has_won():
            entry.time_won = datetime.now()
            self.player_repo.update_entry(entry)
        else:
            raise DisplayableError('Entry has not yet won.')

    def view_events(self, server_id: str) -> None:
        pass

    def view_progress(self, server_id: str) -> None:
        pass
