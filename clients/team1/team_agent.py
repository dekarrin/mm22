class GameState(object):
	def __init__(self, ourTeam, enemyTeam, map):
		self.teams = {'allies': ourTeam, 'enemies': enemyTeam}
		self.map = map

class Agent(object):
	# charInfo is the Character obj created by server,
	# gameState is a gameState object
	def __init__(self, name, classId, ai_func):
		self.classId = classId
		self.ai_func = ai_func
		self.charInfo = None
		self.name = name
		self.target = None
		
	def getAction(self, gameState):
		self.target = 
		self.charInfo = [x for x in gameState.ourTeam if x.name == self.name][0]
		if self.target:
			action = self.ai_func(self, gameState)
		return action
		
	def selectTarget(self, gameState):
		# Caster list aka things we can interrupt
		casters = [
			'Druid',
			'Enchanter',
			'Sorcerer',
			'Paladin',
			'Wizard'
		]

		# Choose a target
		priority_list = [
			'Druid',
			'Enchanter',
			'Sorcerer',
			'Wizard',
			'Assassin',
			'Archer',
			'Paladin',
			'Warrior'
		]
		
		target = None
		target_order = []

		for priority in priority_list:
			for character in gameState.teams['enemies']:
				if character.classId == priority:
					if not character.is_dead():
						target_order.append(character)

		if len(target_order) > 0:
			target = target_order[0]
		return target