from __future__ import annotations
from typing import Optional

from abc import ABC, abstractmethod

from .environment import State, Observation
from .player import Action, Player


class Game(ABC):
    """
    Represents a game where multiple players interact within a dynamic environment.

    Attributes:
        players (list[Player]): A list of players involved in the game, where the keys are player IDs.
        current_player (Player): The player whose turn it is currently.
        current_state (State): The current state of the game.
        round (int): The current round of the game.
        action_profile (dict[UUID, Action]): A dictionary that holds the actions chosen by players in the current round.
        old_state (State): The state of the game from the previous round.
    """

    def __init__(self, players: list[Player], initial_state: State):
        """
        Initializes the game with players and the initial state.

        Args:
            players (list[Player]): The list of players involved in the game.
            initial_state (State): The initial state of the game, representing the starting conditions.
        """
        self.round = 0
        self.players = players

        self.old_state = None 
        self.state = initial_state

    def play(self):
        """
        Runs the game loop, where players take actions and interact with the environment.

        The game continues until a terminal state is reached, and actions are applied to the state at each step.

        Returns:
            tuple: A tuple containing two lists:
                - state_sequence (list[State]): A list of all states traversed in the game.
                - action_sequence (list): A list of all actions taken in the game.
        """
        while not self.terminal(self.state):
            # output something.
            self.output()

            self.round += 1

            actor = self.state.actor

            legal_actions = self.all_actions(actor, self.state)
            observation = self.observe(actor, self.state)
            action = actor.select_action(legal_actions, observation, self.simulate_action)

            # save the current state as old_state for reward calculation
            self.old_state = self.state.clone()

            # apply the action to the state and get the new state
            self.state = self.apply_action(
                self.state.clone(), action.clone()
            )

            # reward all players for the action
            for player in self.players:
                has_acted = player == self.old_state.actor

                # calculate rewards based on the old and current states
                old_observation = self.observe(player, self.old_state)
                current_observation = self.observe(player, self.state)

                environment_reward = self.calculate_reward(
                    player.clone(),
                    self.old_state.clone(),
                    self.state.clone(),
                )

                # Update the player's reward based on their actions
                player.calculate_reward(
                    old_observation.clone(),
                    current_observation.clone(),
                    has_acted,
                    environment_reward,
                )

        # Final output at the end of the game
        self.output()

    @abstractmethod
    def output(self) -> str:
        """
        Specifies what to output after each turn.

        This method should be implemented in subclasses to define the game-specific output.

        Returns:
            str: The output to be displayed after each round.
        """
        pass

    @abstractmethod
    def terminal(self, state: State) -> bool:
        """
        Determines whether the game should terminate or not.

        Args:
            state (State): The current state of the game.

        Returns:
            bool: True if the game has reached a terminal state, otherwise False.
        """
        pass

    @abstractmethod
    def observe(self, observer: Player, state: State) -> Observation:
        """
        Allows a player to observe the current state of the game.

        Args:
            observer (Player): The player who is observing the state.
            state (State): The current state of the game.

        Returns:
            Observation: The observation made by the player.
        """
        pass

    @abstractmethod
    def all_actions(self, actor: Player, state: State) -> list[Action]:
        """
        Returns all possible actions that a given actor can take in the current state.

        Args:
            actor (Player): The player whose actions are being determined.
            state (State): The current state of the game.

        Returns:
            list[Action]: A list of all possible actions the actor can take.
        """
        pass
        
    @abstractmethod
    def apply_action(self, state: State, action: Action) -> State:
        """
        Applies the action to the current state.

        Args:
            state (State): The current state of the game. Modifying this variable
            will not actually affect the state.
            action (Action): The action being applied to get to the next state.

        Returns:
            State: The new state of the game after actions have been applied.
        """
        pass

    
    def simulate_action(self, action: Action) -> Observation:
        """
        Applies the action to the current state and then returns an observation.

        Args:
            state (State): The current state of the game. Modifying this variable
            will not actually affect the state.
            action (Action): The action being applied to get to the next state.

        Returns:
            State: The new state of the game after actions have been applied.
        """
                
        current_state = self.state
        new_state = self.apply_action(current_state, action)
        observation = self.observe(self.players[action.actor], new_state)
        return observation


    @abstractmethod
    def calculate_reward(
        self,
        player: Player,
        old_state: State,
        new_state: State,
    ) -> Optional[float]:
        """
        Calculates the reward for a player based on the state transition.

        Args:
            player (Player): The player whose reward is being calculated.
            old_state (State): The previous state before the action.
            new_state (State): The new state after the actions have been applied.

        Returns:
            float: The calculated reward for the player.
        """
        pass
