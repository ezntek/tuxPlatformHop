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
#    limitations under the License

from . import Entity
from ..colors import Colors
from .. import rlapi as rl

class Player(Entity):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, 60, 80)
        self._hitbox_color = Colors.maroon

    def _handle_key(self, current_key: rl.KeyboardKey) -> None:
        match current_key:
            case rl.KEY_LEFT:
                self.hitbox.x -= 10
            case rl.KEY_RIGHT:
                self.hitbox.x += 10

    def collision(self, sprite: Entity) -> None:
        pass

    def render(self) -> None:
        rl.draw_rectangle_rec(self.hitbox, self._hitbox_color)
    
    def refresh(self, sprite: Entity, input_buffer: list[rl.KeyboardKey]) -> None:
        self._kb_input(input_buffer)
        self.collision(sprite)