create schema bingo_bot_test;
set search_path to bingo_bot_test;

create table Game (
	game_id SERIAL not null,
	server_id VARCHAR(255) not null,
	time_started TIMESTAMP not null,
	time_finished TIMESTAMP null,
	primary key (game_id)
);

create table GameEvent (
	event_id SERIAL not null,
	game_id SERIAL not null references Game(game_id),
	event_desc VARCHAR(255) not null,
	index_in_game INT not null,
	is_hit BOOLEAN not null,
	primary key (event_id),
	unique (game_id, index_in_game)
);

create table GameEntry (
	entry_id SERIAL not null,
	game_id SERIAL not null references Game(game_id),
	player_id VARCHAR(255) not null,
	time_won TIMESTAMP null,
	primary key (entry_id),
	unique (game_id, player_id)
);

create table Combo (
	combo_id SERIAL not null,
	entry_id SERIAL not null references GameEntry(entry_id) on delete cascade,
	index_in_entry INT not null,
	primary key (combo_id),
	unique (entry_id, index_in_entry)
);

create table EventInCombo (
	combo_id SERIAL not null references Combo(combo_id) on delete cascade,
	event_id SERIAL not null references GameEvent(event_id),
	index_in_combo INT not null,
	primary key (combo_id, event_id),
	unique (combo_id, event_id, index_in_combo)
);

