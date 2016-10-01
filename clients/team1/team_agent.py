class GameState(object):
    def __init__(self, ourTeam, enemyTeam, map):
        self.teams = {'allies': ourTeam, 'enemies': enemyTeam}
        self.map = map
        
STATE_DEFAULT = 0
STATE_RUNNING = 1
STATE_RAN = 2

class Agent(object):
    # charInfo is the Character obj created by server,
    # gameState is a gameState object
    def __init__(self, name, classId, ai_func):
        self.classId = classId
        self.ai_func = ai_func
        self.charInfo = None
        self.name = name
        self.target = None
        self.state = STATE_DEFAULT
        self.turnsmoving = 0
        
    def getAction(self, gameState):
        self.target = self.selectTarget(gameState)
        self.charInfo = [x for x in gameState.teams['allies'] if x.name == self.name][0]
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
        
    def get_best_location(self):
        character = self.charInfo
        print "me" + str(character.position)
        # for enemy in enemyteam:
            # print "enemy" + str(enemy.position)
        if character.position == (2, 1):
            # top, go up
            destination = (2,0)

        elif character.position == (1, 2):
            # left, go left
            destination = (0,2)

        elif character.position == (2, 3):
            # bottom, go down
            destination = (2,4)

        elif character.position == (3, 2):
            # right, move right
            destination = (4,2)

        elif character.position == (2, 2):
            # middle, go left
            destination = (1,2)
        else:
            # we are in the perimeter, peruse around it
            x = character.position[0]
            y = character.position[1]
            if x == 0:
                if y == 0:
                    # top left, go right
                    destination = (x+1, y)
                else:
                    # we are on the left, go up
                    destination = (x, y-1)
            elif y == 0:
                if x == 4:
                    # top right, go down
                    destination = (x, y+1)
                #we are on the top, go left
                else:
                    destination = (x+1, y)
            elif x == 4:
                if y == 4:
                    # bottom right, go left
                    destination = (x-1, y)
                else:
                    #we are on the right, go down
                    destination = (x, y+1)
            elif y == 4:
                if x == 0:
                    # bottom left, go up
                    destination = (x, y-1)
                else:
                    # we are on the bottom, go left
                    destination = (x-1, y)
        return destination