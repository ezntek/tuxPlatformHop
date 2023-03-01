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
    def refresh(self, ticker: int) -> None:
        pass

    @abc.abstractmethod
    def render(self, ticker: int) -> None:
        pass

class Entity(Sprite):
    "The base class for an entity."

    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        super().__init__(x, y, width, height)

    def _screen_wrap(self): 
        if self.hitbox.x > 600 - (self.hitbox.width/2):
            self.hitbox.x = 0 - (self.hitbox.width/2)
        
        if self.hitbox.x < 0 - (self.hitbox.width/2):
            self.hitbox.x = 600 - (self.hitbox.width/2)

    def collision(self, item: 'Entity | Sprite | None') -> None:
        pass

    def move_to(self, pos_x: float, pos_y: float) -> None:
        self.hitbox.xy = pos_x, pos_y

    def move_to_v(self, position: rl.Vector2) -> None:
        self.hitbox.xy = position.xy

    def render(self, ticker: int) -> None:
        return super().render(ticker)
    
    def refresh(self, collision_item: 'Sprite | Entity | None', ticker: int) -> None:
        self.collision(collision_item)
        self._screen_wrap()

class ControllableEntity(Entity):
    "A user-controllable Entity."

    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        super().__init__(x, y, width, height)
        self._keys: dict[rl.KeyboardKey, typing.Callable[[], None]]

    def _kb_input(self) -> None:
        for key, fn in self._keys.items():
            fn() if rl.is_key_down(key) else None

    def collision(self, item: 'Entity | Sprite | None') -> None:
        pass

    def move_to(self, pos_x: float, pos_y: float) -> None:
        self.hitbox.xy = pos_x, pos_y

    def move_to_v(self, position: rl.Vector2) -> None:
        self.hitbox.xy = position.xy

    def render(self, ticker: int) -> None:
        return super().render(ticker)
    
    def refresh(self, collision_item: 'Entity | Sprite | None', ticker: int) -> None:
        return super().refresh(collision_item, ticker)

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

@dataclasses.dataclass
class EntitySlot(SpriteSlot):
    "A slot for an Entity that holds additional metadata and a few utility functions for cleaner code."

    content: Entity

    def set_content(self, entity: Entity) -> None:
        self.content = entity

class SpriteGroup():
    "Just an iterable group of sprites (with utility functions of course)" 

    def __init__(self, *sprites: Sprite) -> None:
        self.items: list[SpriteSlot] = [SpriteSlot(sprite, index=count) for count, sprite in enumerate(sprites)]
        self._current_index = 0 # for the iterator

        self._recently_deleted_items: list[int] = []
        
    def squeeze(self) -> None:
        try:
            if self.items[-1].content == None:
                self.items.pop(-1)
                try:
                    self.squeeze()
                except IndexError:
                    return 
        except IndexError:
            return

    def register_item(self, new_item: Sprite):
        if len(self._recently_deleted_items) != 0:
            self.items[self._recently_deleted_items.pop(-1)].set_content(new_item)
            return
        self.items.append(SpriteSlot(new_item, index=len(self.items)))

    def delete_item(self, at_index: int) -> None:
        self.items[at_index].set_content(None) # type: ignore
        self._recently_deleted_items.append(at_index)

    def __iter__(self) -> 'SpriteGroup':
        return self
    
    def __next__(self) -> SpriteSlot:
        if self._current_index >= len(self.items):
            self._current_index = 0
            raise StopIteration
        retval: SpriteSlot = self.items[self._current_index]
        self._current_index += 1
        return retval
    
    def __getitem__(self, index: int) -> SpriteSlot:
        return self.items[index]

    def render(self, ticker: int) -> None:
        for slot in self.items:
            try:
                slot.content.render(ticker)
            except ValueError: # because can be None
                pass

    def refresh(self, ticker: int) -> None:
        for slot in self.items:
            slot.content.refresh(ticker)

class EntityGroup(SpriteGroup):
    def __init__(self, *entities: Entity) -> None:
        self.items: list[EntitySlot] = [EntitySlot(entity, count) for count, entity in enumerate(entities)]
        self._recently_deleted_items: list[int] = []

    def register_item(self, new_item: Entity) -> None:
        if len(self._recently_deleted_items) != 0:
            self.items[self._recently_deleted_items.pop(-1)].set_content(new_item)
            return
        self.items.append(EntitySlot(new_item, index=len(self.items)))

    def __next__(self) -> EntitySlot:
        if self._current_index >= len(self.items):
            self._current_index = 0
            raise StopIteration
        retval: EntitySlot = self.items[self._current_index]
        self._current_index += 1
        return retval

    def __getitem__(self, index: int) -> EntitySlot:
        return self.items[index]
 
    def render(self, ticker: int) -> None:
        for slot in self.items:
            try:
                slot.content.render(ticker)
            except ValueError: # because can be None
                pass

    def refresh(self, ticker: int, collision_item: Entity | Sprite | None) -> None:
        for slot in self.items:
            slot.content.refresh(collision_item, ticker)