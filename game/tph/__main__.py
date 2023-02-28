#    Copyright 2023 Eason Qin (ezntek, ezntek@xflymusic.com)
#   
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    
#      http://www.apache.org/licenses/LICENSE-2.0
#    
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from . import sprites
from .sprites import player
from . import screens
from . import rlapi as rl
from . import __version__

def main() -> None:
    rl.init_window(600, 900, "test")
    rl.set_target_fps(60)
    
    # set up the screens
    active_screen: screens.Screen = screens.MainScreen(f"tuxPlatformHop {__version__}")
    rl.set_window_title(active_screen.title)

    # sprites
    main_sprite_group = sprites.SpriteGroup()
    main_sprite_group.register_sprite(player.Player(50, 50))

    while not rl.window_should_close():
        with rl.drawing(): active_screen.render([main_sprite_group])
        active_screen.refresh([main_sprite_group])
             
    rl.close_window()