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

import typing
from .. import sprites
from .. import rlapi as rl

# Class Definitions
class Screen():
    def __init__(self, title: str = "Screen Base Class") -> None:
        self.title: str = title
        self.ticker: int = 0
        self.current_color: rl.Color = rl.BLACK

    def _toggle_color(self):
        self.current_color = rl.BLACK if self.current_color == rl.BLACK else rl.GRAY

    def render(self):
        rl.draw_text(self.title, 20, 20, 20, self.current_color)

    def refresh(self):
        self.ticker += 1

        self._toggle_color() if self.ticker % 20 == 0 else None
        
    def __repr__(self) -> str:
        return f"Screen Base Class ({self.title})"

class MainScreen(Screen):
    def __init__(self: typing.Self, title: str = "Main Window") -> None:
        # variables
        self.ticker: int = 0
        self.title = title

    def refresh(self, sprite_groups: list[sprites.SpriteGroup], entity_groups: list[sprites.EntityGroup]) -> None:
        for group in sprite_groups:
            group.refresh(self.ticker)
        
        for entity_group in entity_groups:
            entity_group.refresh(self.ticker, None)

    def render(self, sprite_groups: list[sprites.SpriteGroup]) -> None:
        rl.clear_background(rl.RAYWHITE)
        rl.draw_fps(20, 20)

        for group in sprite_groups:
            group.render(self.ticker)