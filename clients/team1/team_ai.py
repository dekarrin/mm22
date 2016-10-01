import src.game.game_constants as game_consts

def paladin(agent, gameState):
	character = agent.charInfo
	
	# break CC if druid is stunned or silenced if it's off cooldown
	if character.attributes.stunned < 0 or character.attributes.silenced < 0 or character.attributes.rooted < 0:
		cooldown = character.abilities[0]
		if cooldown == 0:
			return {
				"Action": "Cast",
				"CharacterId": character.id,
				# Am I buffing or debuffing? If buffing, target myself
				"TargetId": character.id,
				"AbilityId": 0
			}

	# See if we are busy casting a spell
	if character.casting:
		print "casting"
		return

	# See if we need to heal our ally
	cooldown = character.abilities[3]
	if cooldown == 0:
		for ally in gameState.teams['allies']:
			healthLost = ally.attributes.maxHealth - ally.attributes.health
			if ally.attributes.health > 0 and healthLost >= 250:
				print "healing: " + str(ally.id)
				return {
					"Action": "Cast",
					"CharacterId": character.id,
					# Am I buffing or debuffing? If buffing, target myself
					"TargetId": ally.id,
					"AbilityId": 3
				}

	# stun something if they are casting, if they have a caster, otherwise just stun something
	cooldown = character.abilities[14]  # stun
	if cooldown == 0:
		enemy_has_caster = False
		for enemy in gameState.teams['enemies']:
			if enemy.attributes.health > 0 and enemy.classId in casters:
				enemy_has_caster = True

		if enemy_has_caster:
			for enemy in enemyteam:
				if enemy.casting:
					return {
						"Action": "Cast",
						"CharacterId": character.id,
						"TargetId": enemy.id,
						"AbilityId": 14
					}

		else: #just stun the target if in range
			if character.in_range_of(agent.target, gameState.map):
				return {
					"Action": "Cast",
					"CharacterId": character.id,
					# Am I buffing or debuffing? If buffing, target myself
					"TargetId": agent.target.id,
					"AbilityId": 14
				}
			
	# If I am in range, either move towards target
	if character.in_range_of(agent.target, gameState.map):
		return {
			"Action": "Attack",
			"CharacterId": character.id,
			"TargetId": agent.target.id,
		}
	else:  # Not in range, move towards
		return {
			"Action": "Move",
			"CharacterId": character.id,
			"TargetId": agent.target.id,
		}

def assassin(agent, gameState):
	done = False

	# break CC if druid is stunned or silenced if it's off cooldown
	if character.attributes.stunned < 0 or character.attributes.rooted < 0:
		cooldown = character.abilities[0]
		if cooldown == 0:
			return {
				"Action": "Cast",
				"CharacterId": character.id,
				"TargetId": character.id,
				"AbilityId": 0
			}
			
	if character.in_range_of(agent.target, gameState.map):
		cooldown = character.abilities[11]
		if cooldown == 0:
			return {
				"Action": "Cast",
				"CharacterId": character.id,
				"TargetId": agent.target.id,
				"AbilityId": 11
			}

	# If i'm dying, run away
	# if not done:
	#     if character.attributes.health < 500:
	#         print "we are hurt"
	#         actions.append({
	#             "Action": "Move",
	#             "CharacterId": character.id,
	#             "Location": (1, 4),
	#         })
	#         done = True

	# If I am in range, either move towards target
	if character.in_range_of(agent.target, gameState.map):
		return {
			"Action": "Attack",
			"CharacterId": character.id,
			"TargetId": agent.target.id,
		}
	else: # Not in range, move towards, might as well sprint if we can
		cooldown = character.abilities[12]
		if cooldown == 0:
			return {
				"Action": "Cast",
				"CharacterId": character.id,
				"TargetId": character.id,
				"AbilityId": 12
			}
		else:
			return {
				"Action": "Move",
				"CharacterId": character.id,
				"TargetId": agent.target.id,
			}

def default(agent, gameState):
	character = agent.charInfo
	# If I am in range, either move towards target
	if character.in_range_of(agent.target, gameState.map):
		# Am I already trying to cast something?
		if character.casting is None:
			cast = False
			for abilityId, cooldown in character.abilities.items():
				# Do I have an ability not on cooldown
				if cooldown == 0:
					# If I can, then cast it
					ability = game_consts.abilitiesList[int(abilityId)]
					# Get ability
					return {
						"Action": "Cast",
						"CharacterId": character.id,
						# Am I buffing or debuffing? If buffing, target myself
						"TargetId": agent.target.id if ability["StatChanges"][0]["Change"] < 0 else character.id,
						"AbilityId": int(abilityId)
					}
			# Was I able to cast something? otherwise attack
			if not cast:
				return {
					"Action": "Attack",
					"CharacterId": character.id,
					"TargetId": target.id,
				}
	else: # Not in range, move towards
		return {
			"Action": "Move",
			"CharacterId": character.id,
			"TargetId": target.id,
		}

def druid(agent, gameState):
	defaultAction = {
		"Action": "Move",
		"CharacterId": character.id,
		"TargetId": target.id,
	}
	character = agent.charInfo
	
	# break CC if druid is stunned or silenced if it's off cooldown
	if character.attributes.stunned < 0 or character.attributes.silenced < 0:
		cooldown = character.abilities[0]
		if cooldown == 0:
			return {
				"Action": "Cast",
				"CharacterId": character.id,
				# Am I buffing or debuffing? If buffing, target myself
				"TargetId": character.id,
				"AbilityId": 0
			}

	# See if we are busy casting a spell
	if character.casting:
		print "casting"
		return defaultAction

	# See if we need to heal our ally
	cooldown = character.abilities[3]
	if cooldown == 0:
		for ally in gameState.teams['allies']:
			healthLost = ally.attributes.maxHealth - ally.attributes.health
			if ally.attributes.health > 0 and healthLost >= 250:
				print "healing: " + str(ally.id)
				return {
					"Action": "Cast",
					"CharacterId": character.id,
					# Am I buffing or debuffing? If buffing, target myself
					"TargetId": ally.id,
					"AbilityId": 3
				}
				
	# If I am in range, either move towards target
	if character.in_range_of(agent.target, gameState.map):
		# Am I already trying to cast something?
		if character.casting is None:
			cast = False
			for abilityId, cooldown in character.abilities.items():
				# Do I have an ability not on cooldown
				if cooldown == 0:
					pass
					# print abilityId, cooldown
					# If I can, then cast it
					# ability = game_consts.abilitiesList[int(abilityId)]
					# # Get ability
					# actions.append({
					#     "Action": "Cast",
					#     "CharacterId": character.id,
					#     # Am I buffing or debuffing? If buffing, target myself
					#     "TargetId": target.id if ability["StatChanges"][0]["Change"] < 0 else character.id,
					#     "AbilityId": int(abilityId)
					# })
					# cast = True
					# break
			# Was I able to cast something? otherwise attack
			if not cast:
				return {
					"Action": "Attack",
					"CharacterId": character.id,
					"TargetId": target.id,
				}