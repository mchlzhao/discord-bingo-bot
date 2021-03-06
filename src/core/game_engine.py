from datetime import datetime
from typing import List, Optional

from src.core.game_engine_response import GameEngineResponse
from src.entities.combo import Combo
from src.entities.combo_set import ComboSet
from src.repos.abstract.ievent_repo import IEventRepo
from src.repos.abstract.igame_repo import IGameRepo
from src.repos.abstract.iplayer_repo import IPlayerRepo


class GameEngine:
    def __init__(self, event_repo: IEventRepo, game_repo: IGameRepo,
                 player_repo: IPlayerRepo):
        self.event_repo = event_repo
        self.game_repo = game_repo
        self.player_repo = player_repo

    def start_game(self, server_id: str, event_strs: List[str]) \
            -> GameEngineResponse:
        game = self.game_repo.read_active_game(server_id)
        if game is not None:
            return GameEngineResponse(
                display_error='A game is already running.')

        game = self.game_repo.create_game(server_id)
        events = self.event_repo.create_events(game.game_id, event_strs)
        return GameEngineResponse({'events': events})

    def finish_game(self, server_id: str) -> GameEngineResponse:
        game = self.game_repo.read_active_game(server_id)
        if game is None:
            return GameEngineResponse(
                display_error='No game is currently running.')

        game.time_finished = datetime.now()
        self.game_repo.update_game(game)

        entries = self.player_repo.read_all_entries(game.game_id)
        entries = list(filter(lambda e: e.time_won is not None, entries))
        entries.sort(key=lambda e: e.time_won)
        events = self.event_repo.read_all_events(game.game_id)
        return GameEngineResponse(
            {'winning_entries': entries, 'events': events})

    def set_entry(self, server_id: str, player_id: str,
                  combo_set_indices: List[List[int]]) -> GameEngineResponse:
        game = self.game_repo.read_active_game(server_id)
        if game is None:
            return GameEngineResponse(
                display_error='No game is currently running.')

        events = self.event_repo.read_all_events(game.game_id)
        if any([event.is_hit for event in events]):
            return GameEngineResponse(display_error=(
                'Cannot add/change entry as events have already been hit.'))

        combos = []
        for combo_index, event_indices in enumerate(combo_set_indices):
            try:
                combos.append(Combo(None, [events[i] for i in event_indices],
                                    combo_index))
            except IndexError:
                return GameEngineResponse(display_error=(
                    f'Combo {combo_index + 1} contains invalid event index.'))

        self.player_repo.delete_entry(game.game_id, player_id)
        combo_set = ComboSet(player_id, combos)
        self.player_repo.create_entry(game.game_id, combo_set)

        return GameEngineResponse()

    def _search_event(self, game_id, *, index: Optional[int],
                      desc: Optional[str]) -> GameEngineResponse:
        events = self.event_repo.read_all_events(game_id)
        if index is not None:
            events.sort(key=lambda event: event.index)
            try:
                hit_event = events[index]
            except IndexError:
                return GameEngineResponse(display_error='Invalid event index.')
            return GameEngineResponse({'event': hit_event})
        if desc is not None:
            matches = list(filter(
                lambda event: desc.lower() in event.desc.lower(), events))
            if len(matches) == 0:
                return GameEngineResponse(display_error=(
                    'No event description matches search string.'))
            elif len(matches) > 1:
                error_str = (
                    f'More than one event description matches "{desc}".\n'
                    f'Matches include: {matches[0].desc}\n{matches[1].desc}')
                if len(matches) > 2:
                    error_str += '\n...'
                return GameEngineResponse(display_error=error_str)
            else:
                return GameEngineResponse({'event': matches[0]})
        raise ValueError('No search method has been specified.')

    def change_hit(self, server_id: str, is_hit: bool, *, index: int = None,
                   desc: str = None) -> GameEngineResponse:
        game = self.game_repo.read_active_game(server_id)
        if game is None:
            return GameEngineResponse(
                display_error='No game is currently running.')

        response = self._search_event(game.game_id, index=index, desc=desc)
        if response.display_error is not None:
            return response
        event = response.response['event']
        if is_hit and event.is_hit:
            return GameEngineResponse(
                display_error=f'Event "{event.desc}" has already been hit.')
        elif not is_hit and not event.is_hit:
            return GameEngineResponse(
                display_error=f'Event "{event.desc}" is already unhit.')
        event.is_hit = is_hit
        self.event_repo.update_event(game.game_id, event)

        if not is_hit:
            # some players may have lost their win consequently
            combo_sets = self.player_repo.read_all_combo_sets(game.game_id)
            entries = self.player_repo.read_all_entries(game.game_id)
            entry_by_player_id = {entry.player_id: entry for entry in entries}
            for combo_set in combo_sets:
                entry = entry_by_player_id[combo_set.player_id]
                if entry.time_won is not None and not combo_set.has_won():
                    entry.time_won = None
                    self.player_repo.update_entry(entry)

        return GameEngineResponse({'event': event})

    def bingo(self, server_id: str, player_id: str) -> GameEngineResponse:
        game = self.game_repo.read_active_game(server_id)
        if game is None:
            return GameEngineResponse(
                display_error='No game is currently running.')

        entry = self.player_repo.read_entry(game.game_id, player_id)
        if entry is None:
            return GameEngineResponse(display_error='You are not in the game.')
        if entry.time_won is not None:
            return GameEngineResponse(
                display_error='Your entry has already won.')

        combo_set = self.player_repo.read_combo_set(game.game_id, player_id)
        if combo_set.has_won():
            entry.time_won = datetime.now()
            self.player_repo.update_entry(entry)
        else:
            return GameEngineResponse(
                display_error='Your entry has not yet won.')
        return GameEngineResponse()

    def view_events(self, server_id: str) -> GameEngineResponse:
        game = self.game_repo.read_active_game(server_id)
        if game is None:
            return GameEngineResponse(
                display_error='No game is currently running.')

        events = self.event_repo.read_all_events(game.game_id)
        events.sort(key=lambda event: event.index)
        return GameEngineResponse({'events': events})

    def view_progress(self, server_id: str) -> GameEngineResponse:
        game = self.game_repo.read_active_game(server_id)
        if game is None:
            return GameEngineResponse(
                display_error='No game is currently running.')

        combo_sets = self.player_repo.read_all_combo_sets(game.game_id)
        events = self.event_repo.read_all_events(game.game_id)
        has_started = any([event.is_hit for event in events])
        return GameEngineResponse({'combo_sets': combo_sets,
                                   'game_has_started': has_started})

    def view_winners(self, server_id: str) -> GameEngineResponse:
        game = self.game_repo.read_active_game(server_id)
        if game is None:
            return GameEngineResponse(
                display_error='No game is currently running.')

        entries = self.player_repo.read_all_entries(game.game_id)
        entries = list(filter(lambda e: e.time_won is not None, entries))
        entries.sort(key=lambda e: e.time_won)
        return GameEngineResponse({'winning_entries': entries})
