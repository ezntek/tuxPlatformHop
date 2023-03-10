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

import typing

from . import ControllableEntity, Entity, Sprite
from ..colors import Colors
from .. import rlapi as rl

class Player(ControllableEntity):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, 60, 80)
        self._hitbox_color = Colors.maroon
        self._keys: dict[rl.KeyboardKey, typing.Callable[[], None]] = {
            rl.KEY_LEFT: (lambda *_: self.move_to(self.hitbox.x - 10, self.hitbox.y)),
            rl.KEY_RIGHT: (lambda *_: self.move_to(self.hitbox.x + 10, self.hitbox.y)),
            rl.KEY_SPACE: (lambda *_: self.jump()),
        }

        # physics related variables
        self.ticker = 0
        self.jump_ticker = 0
        self.stop_ticking_jump = False
        self.velocity = rl.Vector2(0, 0)
        self.floor_height = 900

    def jump(self) -> None:
        if self.hitbox.y > self.floor_height - self.hitbox.height or self.jump_ticker > 0:
            return
        
        if self.ticker % 6 == 0 and not self.stop_ticking_jump:
            self.jump_ticker += 1

        if self.jump_ticker <= 3:
            self.velocity.y -= 2
        elif self.jump_ticker > 4 and self.hitbox.y - self.hitbox.height > self.floor_height:
            self.velocity.y = 3
            self.stop_ticking_jump = True
        
        if rl.is_key_released(rl.KEY_SPACE):
            self.velocity.y = 0
            self.jump_ticker = 0
            self.stop_ticking_jump = False

    def collision(self, item: Entity | Sprite | None) -> None:
        pass

    def render(self, ticker: int) -> None:
        rl.draw_rectangle_rec(self.hitbox, self._hitbox_color)
    
    def refresh(self, collision_item: Entity | Sprite | None, ticker: int) -> None:
        self.ticker = ticker
        self._kb_input()
        self.collision(collision_item)

        if self.hitbox.y < self.floor_height - self.hitbox.height:
            self.velocity.y += 2

        if self.hitbox.y >= self.floor_height - self.hitbox.height:
            self.hitbox.y = self.floor_height - self.hitbox.height
            self.velocity.y = 0
        
        self.hitbox.x += self.velocity.x
        self.hitbox.y += self.velocity.y

        self._screen_wrap()