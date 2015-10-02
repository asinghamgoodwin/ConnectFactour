--drop table if exists Ingredient, Category, Salad;

create table Game (
    game_id  integer primary key autoincrement not null,
    game_state        text,
    game_url            text
);
