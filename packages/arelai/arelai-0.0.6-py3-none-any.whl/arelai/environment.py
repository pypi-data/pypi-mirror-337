from abc import ABC
from copy import deepcopy

from uuid import UUID


class State(ABC):
    """
    Represents the state of the game, which holds the actor IDs.

    The State class should never directly store Player objects. Instead, it stores the UUIDs of the players involved,
    ensuring that the game logic is decoupled from the Player objects.

    Attributes:
        actor_ids (list[UUID]): A list of UUIDs representing the actors (players) in the current state.
    """

    def __init__(self, actor_ids: list[UUID]):
        """
        Initializes the state with a list of actor IDs (UUIDs).

        Args:
            actor_ids (list[UUID]): A list of UUIDs representing the actors (players) in the game.
        """
        self.actor_ids = actor_ids

    def clone(self) -> "State":
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
        observer_id (UUID): The UUID of the player who made the observation.
    """

    def __init__(self, observer_id: UUID):
        """
        Initializes the observation with the ID of the observing player.

        Args:
            observer_id (UUID): The UUID of the player who is observing the state of the game.
        """
        self.observer_id = observer_id

    def clone(self) -> "Observation":
        """
        Creates and returns a deep copy of the current observation.

        Returns:
            Observation: A deep copy of the observation to ensure no unintended modifications
                         are made to the original object.
        """
        return deepcopy(self)
