from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from abc import ABC
from copy import deepcopy

if TYPE_CHECKING:
    from .player import Player, Action

class State(ABC):
    """
    Represents the state of the game, which holds the actor IDs.

    Attributes:
        actor (Player): The actor in this state.
        action: (Action): The action that resulted in this state.
    """

    def __init__(self, actor: Player, action: Optional[Action] = None):
        """
        Initializes the state with the actor's ID.

        Args:
            actor_id (UUID): A list of UUIDs representing the actor for the current state.
        """
        self.actor = actor
        self.action = action

    def clone(self) -> State:
        """
        Creates and returns a deep copy of the current state.

        Returns:
            State: A deep copy of the current state, ensuring that any modifications to the clone
                   do not affect the original state.
        """
        return deepcopy(self)


class Observation(ABC):
    """
    Represents an observation made by a player in the game.

    This class allows players to observe the current state of the game without directly modifying the game state.

    Attributes:
        observer: The player who is making the observation.
    """

    def __init__(self, observer: Player):
        """
        Initializes the observation with the ID of the observing player.

        Args:
            observer (Player): The player who is making the observation.
        """
        self.observer = observer

    def clone(self) -> Observation:
        """
        Creates and returns a deep copy of the current observation.

        Returns:
            Observation: A deep copy of the observation to ensure no unintended modifications
                         are made to the original object.
        """
        return deepcopy(self)
