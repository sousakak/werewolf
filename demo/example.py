import werewolf

players = ['a', 'b', 'c']
roles = ['vil', 'vil', 'wolf']
asgmt = werewolf.assign(players, roles) # {'a': Villager, ...}
print("You are" + asgmt['a'].role + "in the team" + asgmt['a'].team) # display to player a
werewolf.day_act('a') # a was executed
