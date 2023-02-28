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

import abc
import typing
import dataclasses

from .. import rlapi as rl
from ..colors import Colors

# Class Definitions
class Sprite(abc.ABC):
    "The base class for all Sprites."

    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.hitbox: rl.Rectangle = rl.Rectangle(x, y, width, height)
        self.should_delete: bool = False
        
        # private vars
        self._repr_text: str = ""
        self._hitbox_color: rl.Color = Colors.nothing

    def __repr__(self) -> str:
        return self._repr_text

    # Function Definitions
    @abc.abstractmethod
    def _kb_input(self) -> None:
        pass
    
    @abc.abstractmethod
    def collision(self, sprite: typing.Any | None) -> None:
        return
    
    @abc.abstractmethod
    def refresh(self, collision_sprite: typing.Any | None, input_buffer: list[rl.KeyboardKey]) -> None:
        pass

    @abc.abstractmethod
    def render(self) -> None:
        pass

class Entity(Sprite):
    "The base class for an entity."

    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        super().__init__(x, y, width, height)

    def _handle_key(self, current_key: rl.KeyboardKey):
        pass

    def _kb_input(self, input_buffer: list[rl.KeyboardKey]) -> None:
        while len(input_buffer) > 0:
            self._handle_key(input_buffer.pop(-1))
    
    def collision(self, sprite: Sprite | None) -> None:
        pass

    def move_to(self, pos_x: float, pos_y: float) -> None:
        self.hitbox.xy = pos_x, pos_y

    def move_to_v(self, position: rl.Vector2) -> None:
        self.hitbox.xy = position.xy

    def render(self) -> None:
        return super().render()
    
    def refresh(self, collision_sprite: Sprite | None, input_buffer: list[rl.KeyboardKey]) -> None:
        return super().refresh(collision_sprite, input_buffer)

@dataclasses.dataclass
class SpriteSlot():
    "A slot for a Sprite that holds additional metadata and utility functions for cleaner code."

    content: Sprite
    index: int = 0

    def set_index(self, index: int) -> None:
        self.index = index
    
    def set_content(self, sprite: Sprite) -> None:
        self.sprite = sprite

    def __repr__(self) -> str:
        return f"{self.content.__repr__()} at index {self.index}"

class SpriteGroup():
    "Just an iterable group of sprites (with utility functions of course)" 

    def __init__(self, *sprites: Sprite | Entity) -> None:
        self.sprites: list[SpriteSlot] = [SpriteSlot(sprite, index=count) for count, sprite in enumerate(sprites)]
        self._current_index = 0 # for the iterator

        self._recently_deleted_sprites: list[int] = []
        

    def squeeze(self) -> None:
        try:
            if self.sprites[-1].content == None:
                self.sprites.pop(-1)
                try:
                    self.squeeze()
                except IndexError:
                    return 
        except IndexError:
            return

    def register_sprite(self, new_sprite: Sprite | Entity):
        if len(self._recently_deleted_sprites) != 0:
            self.sprites[self._recently_deleted_sprites[-1]].set_content(new_sprite)
            self._recently_deleted_sprites.pop(-1)
        self.sprites.append(SpriteSlot(new_sprite, index=len(self.sprites)))

    def delete_sprite(self, at_index: int) -> None:
        self.sprites[at_index].set_content(None) # type: ignore
        self._recently_deleted_sprites.append(at_index)

    def __iter__(self) -> typing.Self:
        return self
    
    def __next__(self) -> SpriteSlot:
        if self._current_index >= len(self.sprites):
            self._current_index = 0
            raise StopIteration
        retval: SpriteSlot = self.sprites[self._current_index]
        self._current_index += 1
        return retval
    
    def __getitem__(self, index: int) -> SpriteSlot:
        return self.sprites[index]

    def render(self) -> None:
        for slot in self:
            try:
                slot.content.render()
            except ValueError: # because can be None
                pass

    def refresh(self, collision_sprite: Sprite | Entity | None, input_buffer: list[rl.KeyboardKey]) -> None:
        for slot in self:
            slot.content.refresh(collision_sprite, input_buffer)