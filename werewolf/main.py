import functools, random
from typing import Optional, Type
from abc import ABC, abstractmethod
from __future__ import annotations

### Errors ###

### Utilities ###

### Role classes ###
class Player(ABC):
    """
    An abstract class which is the parent of all player classes.

    When you create custom role, create it by inheriting from this class.
    Also, don't forget to create some abstract methods.

    Attributes
    ----------
    name: :class:`str`
        The name of the player. Non-standard alphabets and other characters
        are also possible.

    Parameters
    ----------
    name: :class:`str`
        The name of the player.
    
    killer: Optional[:class:`str`]
        When the player died, the cause of death is in this variable.
        This will contain one of the following:
        - ``vote``: The player died by daylight vote
        - Player name: The player died by action of the player with this name

    game: Optional[:class:`Game`]
        The game instance which this player belongs to.
        This is set when the game starts, so you don't have to set it by yourself.
        
    role: Optional[:class:`str`]
        A role of this player.
        Since this is an abstract property, please set the string value
        in each class.

    team: Optional[:class:`str`]
        The team which this player belongs to.
        Since this is an abstract property, please set the string value
        in each class.
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.killer: Optional[str] = None
        self.__game: Optional[Game] = None

    def __bool__(self) -> bool:
        """
        Returns True if the player is alive, False if the player is dead.
        """
        return self.killer is None

    def __str__(self):
        return f"{self.name} ({self.role})"

    @property
    @abstractmethod
    def role(self):
        """
        Abstract property for role. Please set the string value in each class.
        """
        pass

    @property
    @abstractmethod
    def team(self):
        """
        Abstract property for team. Please set the string value in each class.
        """
        pass

    def dayAct(self):
        """
        A method for daytime action.
        """
        self.__game.dayAct(self.name, lambda _: None)

    def nightAct(self):
        """
        A method for nighttime action.
        """
        self.__game.nightAct(self.name, lambda _: None)

    @property
    def game(self):
        return self.__game

    @game.setter
    def game(self, game: Game):
        """
        A setter for game property. This is used to register the game instance to the player.
        """
        if self.__game is None: self.__game = game

class Villager(Player):
    def __init__(self, name) -> None:
        super().__init__(name)

    @property
    def role(self):
        return 'villager'

    @property
    def team(self):
        return 'innocent'

class Wolf(Player):
    def __init__(self, name) -> None:
        super().__init__(name)

    @property
    def role(self):
        return 'werewolf'
    
    @property
    def team(self):
        return 'wolf'

    def nightAct(self, name: str | list[str]) -> bool:
        return self.game.nightAct(self.name, lambda game: game.kill(name, self.name))

### Game class ###
class Game():
    """
    A class which manages the game.
    
    Please start a game by creating an instance of this class.
    """
    def __init__(self, asgmt: dict[str, Player]) -> None:
        # Initialize game data
        self.players: dict[str, Player] = asgmt
        self.day: int = 0
        self.isNight: bool = False

        # Survivors and corpses data
        self.survivors: list[str] = list(self.players.keys())
        self.corpses: list[str] = []
        self.acted: list[str] = []

        # Team information
        self.teams: dict[str] = {}
        for player in self.players.values():
            if player.team not in self.teams:
                self.teams[player.team] = [player]
            else:
                self.teams[player.team].append(player)

        # Register game to players
        for player in self.players.values():
            player.game = self

    def __len__(self) -> int:
        return len(self.survivors)

    def __getitem__(self, name: str) -> Player:
        return self.players[name]

    def __bool__(self) -> bool:
        return self.isNight

    def __str__(self) -> str:
        return f"Game ({len(self.survivors)} players survived)"

    @staticmethod
    def assign(members: list[str], roles: list[Type[Player]]) -> Game:
        """A static method to assign random roles to players and create a game instance."""
        asgmt = {m: r(m) for m, r in zip(members, random.sample(roles, len(roles)))}
        return Game(asgmt)

    def dawn(self):
        """
        Proceed to the next day.
        """
        self.day += 1
        self.isNight = False
        self.acted = []

    def dusk(self):
        """
        Proceed to the next night.
        """
        self.isNight = True
        self.acted = []

    def dayAct(self, name: str, act: function = lambda _: None):
        """
        A method for daytime action. This is called when a player performs an action during the day.
        """
        act(self)
        self.acted.append(name)
        if self.survivors == self.acted:
            self.dusk()
            return True
        return False

    def nightAct(self, name: str, act: function = lambda _: None):
        """
        A method for nighttime action. This is called when a player performs an action during the night.
        """
        act(self)
        self.acted.append(name)
        if self.survivors == self.acted:
            self.dusk()
            return True
        return False
    
    def kill(self, name: str, killer: Optional[str] = None):
        """
        A method to kill a player. This can be called by a player's action or
        by other things such as a daytime vote.
        """
        self.players[name].killer = killer
        self.survivors.remove(name)
        self.corpses.append(name)