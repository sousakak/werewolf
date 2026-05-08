import werewolf

players = ['a', 'b', 'c']
roles = [werewolf.Villager] * 2 + [werewolf.Wolf]
game = werewolf.Game.assign(players, roles)
print("You are" + game['a'].role + "in the team" + game['a'].team)
