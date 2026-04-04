import functools, random
from typing import Callable, NoReturn, Tuple
from abc import ABC, abstractmethod

### Errors ###
class WrongNumberOfRoles(Exception):
    pass

class UnknownRole(KeyError):
    pass

class WrongNumberOfConvicts(Exception):
    pass

class PlayerError(Exception):
    def __str__(self) -> str:
        return super().__str__()

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

    role
        A role of this player.
        Since this is an abstract property, please set the string value
        in each class.
        Also, when you create custom roles, do not forget
        to create setters as needed.
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.killer = None
        self.add_data(self.team)

    @property
    @abstractmethod
    def role(self):
        pass

    @property
    @abstractmethod
    def team(self):
        pass
    
    # game settings
    convict_number_per_time = 1

    # game data
    survivors: dict[str, list[str]] = {
        'list': []
    }

    victims: dict[str, list[str]] = {
        'list': []
    }

    teams: list[str] = []

    def add_data(self, team: str) -> None:
        if Player.survivors.get(team) == None:
            Player.survivors[team] = [self.name]
            Player.teams.append(team) # if文分けた方がいい?
        else:
            Player.survivors[team].append(self.name)

    def die(self, reason: str):
        """Wipe the target who is a surviving player from the world."""
        if self.name in self.survivors['list']:
            match reason:
                case 'vote':
                    self.killer = 'vote'
            self.survivors['list'].remove(self.name)
            self.victims['list'].append(self.name) # ここをどうにかしたい
            if self.team in self.victims:
                self.victims[self.team].append(self.name)
            else:
                self.victims[self.team] = [self.name]
        else: # error handling
            if self.name in self.victims['list']:
                errmsg = "player already dead"
            else:
                errmsg = "unknown player given"
            raise PlayerError(errmsg)

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

""" This is a list of default roles. There are some aliases """
DEFSULT_ROLES_LIST = {
    'villager': Villager, 'vil': Villager,
    'werewolf': Wolf, 'wolf': Wolf
}

### Utilities ###
def instantiate_role(role: str, roles_list: dict) -> type | NoReturn:
    if role in roles_list:
        return roles_list[role]
    else:
        raise UnknownRole("Unknown role specified")

# 終了確認関数のラッパー
def isOver(f: Callable[[], str | None]) -> Tuple[bool, str | None]:
    @functools.wraps(f)
    def _wrapper(*args, **keywords):
        result = False
        termination = f(*args, **keywords)
        # タスク：ここで処理を
        if termination != None:
            result = True
        return result, termination
    return _wrapper

### For default ###
# デフォルトで使用される終了確認関数
@isOver
def determ() -> str | None:
    termination = None
    if len(Player.survivors['innocent']) <= len(Player.survivors['wolf']):
        termination = 'wolf'
    return termination

### Main ###
# assignは役職クラスのリスト
def assign(players: list[str], assign: list[str], classes: dict = DEFSULT_ROLES_LIST) -> dict | NoReturn:
    if len(players) != len(assign):
        raise WrongNumberOfRoles("The number of assigned roles does not match the number of players")
    asgmt = {}
    random.shuffle(assign)
    for i, role in enumerate(assign):
        instance: Player = instantiate_role(role, classes)(players[i])
        asgmt[players[i]] = instance
        instance.survivors['list'].append(players[i])
    return asgmt

def day_act(convict: Player | list, determfunc: Callable[[], str | None] = determ) -> bool | NoReturn:
    if issubclass(type(convict), Player):
        if convict.convict_number_per_time == 1:
            convict.die('vote')
        else:
            raise WrongNumberOfConvicts("The number of convict people is different from the game setting")
    elif type(convict) == list:
        if Player.convict_number_per_time == len(convict):
            for player in convict:
                player.die('vote')
        else:
            raise WrongNumberOfConvicts("The number of convict people is different from the game setting")
    else:
        raise TypeError("convict must be list or instance of Player subclass only")
    return determfunc()
