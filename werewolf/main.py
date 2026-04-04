import functools, random
from typing import Optional
from abc import ABC, abstractmethod
from __future__ import annotations

### Errors ###
    
### Utilities ###

### Role classes ###
class Player(ABC):
    """An abstract class which is the parent of all player classes.

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
        self.game: Optional[Game] = None

    def __bool__(self) -> bool:
        """Returns True if the player is alive, False if the player is dead."""
        return self.killer is None

    def __str__(self):
        return f"{self.name} ({self.role})"

    @property
    @abstractmethod
    def role(self):
        """Abstract property for role. Please set the string value in each class."""
        pass

    @property
    @abstractmethod
    def team(self):
        """Abstract property for team. Please set the string value in each class."""
        pass

    @property
    def game(self) -> Optional[Game]:
        return self.game
    
    @game.setter
    def game(self, game: Game):
        """A setter for game property. This is used to register the game instance to the player."""
        if self.game is None: self.game = game

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

### Game class ###
class Game():
    """A class which manages the game.
    
    Please start a game by creating an instance of this class."""
    def __init__(self, asgmt: dict[str, Player]) -> None:
        # Initialize game data
        self.players: dict[str, Player] = asgmt
        self.day: int = 0
        self.isNight: bool = False

        # Survivors and corpses data
        self.survivors: list[str] = list(self.players.keys())
        self.corpses: list[str] = []

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
    def assign(members: list[str], roles: list[Player]) -> Player:
        """A static method to assign random roles to players and create a game instance."""
        asgmt = {m: r for m, r in zip(members, random.sample(roles, len(roles)))}
        return Game(asgmt)

    def dawn(self):
        self.day += 1
        self.isNight = False

    def dusk(self):
        self.isNight = True

    def dayAct(self, act: function):
        act()

    def nightAct(self, act: function):
        act()