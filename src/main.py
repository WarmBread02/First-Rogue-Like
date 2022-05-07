import copy

import tcod

import color
from engine import Engine
import entity_factories

from procgen import generate_dungeon

def main() -> None:
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 43
    
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    
    max_monsters_per_room = 2

    #telling tcod what font to use
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    #use it to receive events and process them.
    player = copy.deepcopy(entity_factories.player)
    
    #this sets the player coords and an npc coord
    engine = Engine(player=player)
    
    
    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        engine=engine,
    )
    
    engine.update_fov()
    
    engine.message_log.add_message(
        "The First Dungeon", color.welcome_text
    )

    #creating the actual screen
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="My first Roguelike game",
        vsync=True,
    ) as context:
        #creates the console, which is what is being drawn to
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            #printing to the console
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)
            

            #this updates the screen and handles events
            engine.event_handler.handle_events(context)
            


if __name__ == "__main__":
    main()