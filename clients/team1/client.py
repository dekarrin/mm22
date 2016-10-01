    #!/usr/bin/python2
import socket
import json
import os
import random
import sys
from socket import error as SocketError
import errno
sys.path.append("../..")
import src.game.game_constants as game_consts
from src.game.character import *
from src.game.gamemap import *

# Game map that you can use to query 
gameMap = GameMap()

# --------------------------- SET THIS IS UP -------------------------
teamName = "WizardCats"
# ---------------------------------------------------------------------

# Set initial connection data
def initialResponse():
# ------------------------- CHANGE THESE VALUES -----------------------
    return {'TeamName': teamName,
            'Characters': [
                {"CharacterName": "Rebecca",
                 "ClassId": "Paladin"},
                {"CharacterName": "Eric",
                 "ClassId": "Assassin"},
                {"CharacterName": "Amanda",
                 "ClassId": "Assassin"},
            ]}
# ---------------------------------------------------------------------

# Determine actions to take on a given turn, given the server response
def processTurn(serverResponse):
# --------------------------- CHANGE THIS SECTION -------------------------
    # Setup helper variables
    actions = []
    myteam = []
    enemyteam = []
    # Find each team and serialize the objects
    for team in serverResponse["Teams"]:
        if team["Id"] == serverResponse["PlayerInfo"]["TeamId"]:
            for characterJson in team["Characters"]:
                character = Character()
                character.serialize(characterJson)
                myteam.append(character)
        else:
            for characterJson in team["Characters"]:
                character = Character()
                character.serialize(characterJson)
                enemyteam.append(character)
# ------------------ You shouldn't change above but you can ---------------

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
        for character in enemyteam:
            if character.classId == priority:
                if not character.is_dead():
                    target_order.append(character)

    target = target_order[0]

    # If we found a target
    if target:
        for character in myteam:

            # druid ai
            if character.classId == 'Druid':
                done = False

                # break CC if druid is stunned or silenced if it's off cooldown
                if character.attributes.stunned < 0 or character.attributes.silenced < 0:
                    cooldown = character.abilities['0']
                    if cooldown == 0:
                        actions.append({
                            "Action": "Cast",
                            "CharacterId": character.id,
                            # Am I buffing or debuffing? If buffing, target myself
                            "TargetId": character.id,
                            "AbilityId": 0
                        })
                        done = True

                # See if we are busy casting a spell
                if not done:
                    if character.casting:
                        print "casting"
                        done = True

                # See if we need to heal our ally
                if not done:
                    cooldown = character.abilities['3']
                    if cooldown == 0:
                        for ally in myteam:
                            healthLost = ally.attributes.maxHealth - ally.attributes.health
                            if ally.attributes.health > 0 and healthLost >= 250:
                                actions.append({
                                    "Action": "Cast",
                                    "CharacterId": character.id,
                                    # Am I buffing or debuffing? If buffing, target myself
                                    "TargetId": ally.id,
                                    "AbilityId": 3
                                })
                                print "healing: " + str(ally.id)
                                done = True

                # If I am in range, either move towards target
                if character.in_range_of(target, gameMap) and not done:
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
                            actions.append({
                                "Action": "Attack",
                                "CharacterId": character.id,
                                "TargetId": target.id,
                            })
                else: # Not in range, move towards
                    actions.append({
                        "Action": "Move",
                        "CharacterId": character.id,
                        "TargetId": target.id,
                    })

            # warrior ai
            if character.classId == 'Warrior':
                # If I am in range, either move towards target
                if character.in_range_of(target, gameMap):
                    # Am I already trying to cast something?
                    if character.casting is None:
                        cast = False
                        for abilityId, cooldown in character.abilities.items():
                            # Do I have an ability not on cooldown
                            if cooldown == 0:
                                # If I can, then cast it
                                ability = game_consts.abilitiesList[int(abilityId)]
                                # Get ability
                                actions.append({
                                    "Action": "Cast",
                                    "CharacterId": character.id,
                                    # Am I buffing or debuffing? If buffing, target myself
                                    "TargetId": target.id if ability["StatChanges"][0]["Change"] < 0 else character.id,
                                    "AbilityId": int(abilityId)
                                })
                                cast = True
                                break
                        # Was I able to cast something? otherwise attack
                        if not cast:
                            actions.append({
                                "Action": "Attack",
                                "CharacterId": character.id,
                                "TargetId": target.id,
                            })
                else: # Not in range, move towards
                    actions.append({
                        "Action": "Move",
                        "CharacterId": character.id,
                        "TargetId": target.id,
                    })

            # archer

            # assassin ai
            if character.classId == 'Assassin':
                # If I am in range, either move towards target
                if character.in_range_of(target, gameMap):
                    # Am I already trying to cast something?
                    if character.casting is None:
                        cast = False
                        for abilityId, cooldown in character.abilities.items():
                            # Do I have an ability not on cooldown
                            if cooldown == 0:
                                # If I can, then cast it
                                ability = game_consts.abilitiesList[int(abilityId)]
                                # Get ability
                                actions.append({
                                    "Action": "Cast",
                                    "CharacterId": character.id,
                                    # Am I buffing or debuffing? If buffing, target myself
                                    "TargetId": target.id if ability["StatChanges"][0]["Change"] < 0 else character.id,
                                    "AbilityId": int(abilityId)
                                })
                                cast = True
                                break
                        # Was I able to cast something? otherwise attack
                        if not cast:
                            actions.append({
                                "Action": "Attack",
                                "CharacterId": character.id,
                                "TargetId": target.id,
                            })
                else: # Not in range, move towards
                    actions.append({
                        "Action": "Move",
                        "CharacterId": character.id,
                        "TargetId": target.id,
                    })

            # enchanter

            # paladin
            if character.classId == 'Paladin':
                done = False

                # break CC if druid is stunned or silenced if it's off cooldown
                if character.attributes.stunned < 0 or character.attributes.silenced < 0:
                    cooldown = character.abilities['0']
                    if cooldown == 0:
                        actions.append({
                            "Action": "Cast",
                            "CharacterId": character.id,
                            # Am I buffing or debuffing? If buffing, target myself
                            "TargetId": character.id,
                            "AbilityId": 0
                        })
                        done = True

                # See if we are busy casting a spell
                if not done:
                    if character.casting:
                        print "casting"
                        done = True

                # See if we need to heal our ally
                if not done:
                    cooldown = character.abilities['3']
                    if cooldown == 0:
                        for ally in myteam:
                            healthLost = ally.attributes.maxHealth - ally.attributes.health
                            if ally.attributes.health > 0 and healthLost >= 250:
                                actions.append({
                                    "Action": "Cast",
                                    "CharacterId": character.id,
                                    # Am I buffing or debuffing? If buffing, target myself
                                    "TargetId": ally.id,
                                    "AbilityId": 3
                                })
                                print "healing: " + str(ally.id)
                                done = True

                # stun something if they are casting, if they have a caster
                if not done:
                    enemy_has_caster = False
                    for enemy in enemyteam:
                        if enemy.attributes.health > 0 and enemy in :

                    cooldown = character.abilities['14'] #stun
                    if cooldown == 0:
                        for enemy in enemyteam:
                            if enemy.

                # If I am in range, either move towards target
                if character.in_range_of(target, gameMap) and not done:
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
                            actions.append({
                                "Action": "Attack",
                                "CharacterId": character.id,
                                "TargetId": target.id,
                            })
                else: # Not in range, move towards
                    actions.append({
                        "Action": "Move",
                        "CharacterId": character.id,
                        "TargetId": target.id,
                    })
            # sorcerer

            # wizard
            if character.classId == 'Wizard':
                # If I am in range, either move towards target
                if character.in_range_of(target, gameMap):
                    # Am I already trying to cast something?
                    if character.casting is None:
                        cast = False
                        for abilityId, cooldown in character.abilities.items():
                            # Do I have an ability not on cooldown
                            if cooldown == 0:
                                # If I can, then cast it
                                ability = game_consts.abilitiesList[int(abilityId)]
                                # Get ability
                                actions.append({
                                    "Action": "Cast",
                                    "CharacterId": character.id,
                                    # Am I buffing or debuffing? If buffing, target myself
                                    "TargetId": target.id if ability["StatChanges"][0][
                                                                 "Change"] < 0 else character.id,
                                    "AbilityId": int(abilityId)
                                })
                                cast = True
                                break
                        # Was I able to cast something? otherwise attack
                        if not cast:
                            actions.append({
                                "Action": "Attack",
                                "CharacterId": character.id,
                                "TargetId": target.id,
                            })
                else:  # Not in range, move towards
                    actions.append({
                        "Action": "Move",
                        "CharacterId": character.id,
                        "TargetId": target.id,
                    })

        # for character in myteam:
        #     # If I am in range, either move towards target
        #     if character.in_range_of(target, gameMap):
        #         # Am I already trying to cast something?
        #         if character.casting is None:
        #             cast = False
        #             for abilityId, cooldown in character.abilities.items():
        #                 # Do I have an ability not on cooldown
        #                 if cooldown == 0:
        #                     # If I can, then cast it
        #                     ability = game_consts.abilitiesList[int(abilityId)]
        #                     # Get ability
        #                     actions.append({
        #                         "Action": "Cast",
        #                         "CharacterId": character.id,
        #                         # Am I buffing or debuffing? If buffing, target myself
        #                         "TargetId": target.id if ability["StatChanges"][0]["Change"] < 0 else character.id,
        #                         "AbilityId": int(abilityId)
        #                     })
        #                     cast = True
        #                     break
        #             # Was I able to cast something? Either wise attack
        #            if not cast:
        #                 actions.append({
        #                     "Action": "Attack",
        #                     "CharacterId": character.id,
        #                     "TargetId": target.id,
        #                 })
        #     else: # Not in range, move towards
        #         actions.append({
        #             "Action": "Move",
        #             "CharacterId": character.id,
        #             "TargetId": target.id,
        #         })

    # Send actions to the server
    return {
        'TeamName': teamName,
        'Actions': actions
    }
# ---------------------------------------------------------------------

# Main method
# @competitors DO NOT MODIFY
if __name__ == "__main__":
    # Config
    conn = ('localhost', 1337)
    if len(sys.argv) > 2:
        conn = (sys.argv[1], int(sys.argv[2]))

    # Handshake
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(conn)

    # Initial connection
    s.sendall(json.dumps(initialResponse()) + '\n')

    # Initialize test client
    game_running = True
    members = None

    # Run game
    try:
        data = s.recv(1024)
        while len(data) > 0 and game_running:
            value = None
            if "\n" in data:
                data = data.split('\n')
                if len(data) > 1 and data[1] != "":
                    data = data[1]
                    data += s.recv(1024)
                else:
                    value = json.loads(data[0])

                    # Check game status
                    if 'winner' in value:
                        game_running = False

                    # Send next turn (if appropriate)
                    else:
                        msg = processTurn(value) if "PlayerInfo" in value else initialResponse()
                        s.sendall(json.dumps(msg) + '\n')
                        data = s.recv(1024)
            else:
                data += s.recv(1024)
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise  # Not error we are looking for
        pass  # Handle error here.
    s.close()
