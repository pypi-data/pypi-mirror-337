from abc import ABC, abstractmethod
from copy import deepcopy

from typing import Optional

import random
import uuid
from uuid import UUID


from .environment import Observation


class Action(ABC):
    """
    Represents an action taken by a player in the game.

    The Action class provides a base for defining specific actions a player can take.

    Attributes:
        actor_id (UUID): The ID of the player who performs the action.
    """

    def __init__(self, actor_id: UUID):
        """
        Initializes the action with the actor's ID.

        Args:
            actor_id (UUID): The UUID of the player who will perform the action.
        """
        self.actor_id = actor_id

    def clone(self) -> "Action":
        """
        Creates and returns a deep copy of the current action.

        Returns:
            Action: A deep copy of the action to ensure no unintended modifications
                    are made to the original object.
        """
        return deepcopy(self)

    @abstractmethod
    def all_actions(self, observation: Observation) -> list['Action']:
        """
        Returns a list of all possible actions based on the current observation.

        Args:
            observation (Observation): The observation that may influence the possible actions.

        Returns:
            list[Action]: A list of all possible actions the player can take.
        """
        return []


class NoAction(Action):
    """
    Represents a 'no action' or a placeholder action where the player does nothing.

    Inherits from the Action class, representing the concept of a player choosing to do nothing.
    """
    pass


class Player(ABC):
    """
    Represents a player in the game.

    The Player class defines the general behavior of a player, such as selecting actions
    and calculating rewards. Specific player behavior is implemented in subclasses.

    Attributes:
        _rng (random.Random): A random number generator for the player, seeded with a provided value.
        _name (str): The name of the player.
        _id (UUID): A unique identifier for the player.
    """

    def __init__(self, seed: int, name: str):
        """
        Initializes the player with a name and a random seed.

        Args:
            seed (int): A seed for the random number generator.
            name (str): The name of the player.
        """
        self._rng = random.Random(seed)
        self._name = name
        self._id = uuid.uuid4()

    @property
    def id(self) -> UUID:
        """
        Returns the player's unique identifier.

        Returns:
            UUID: The unique ID of the player.
        """
        return self._id
    
    @property
    def rng(self) -> random.Random:
        """
        Returns the player's random number generator.

        Returns:
            random.Random: The random number generator for the player.
        """
        return self._rng

    @property
    def name(self) -> str:
        """
        Returns the player's name.

        Returns:
            str: The name of the player.
        """
        return self._name

    @abstractmethod
    def select_action(self, actions: list[Action], observation: Observation) -> Action:
        """
        Selects an action for the player based on the provided legal actions and observation.

        Args:
            actions (list[Action]): A list of possible actions the player can take.
            observation (Observation): The current observation of the game state.

        Returns:
            Action: The action selected by the player.
        """
        pass

    @abstractmethod
    def calculate_reward(self,
                         old_observation: Observation,
                         new_observation: Observation,
                         has_acted: bool,
                         environment_reward: Optional[float] = None):
        """
        Calculates the player's reward after taking an action.

        Args:
            old_observation (Observation): The player's previous observation of the game state.
            new_observation (Observation): The player's new observation of the game state.
            has_acted (bool): Whether the player has acted in this transition.
            environment_reward (Optional[float]): The environment's reward (if any) for the player.

        Returns:
            None
        """
        pass

    def clone(self) -> "Player":
        """
        Creates and returns a deep copy of the current player.

        Returns:
            Player: A deep copy of the player, ensuring the original player remains unaffected.
        """
        return deepcopy(self)