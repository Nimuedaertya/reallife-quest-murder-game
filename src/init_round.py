# imports
import copy
import static_variables as const
import logging as log

# specific imports
from random import randint, shuffle

###
# functions
###

def distribute_roles(players, roles):
    role_pool = []
    visible_to_data = {}

    for role in roles:
        
        # some roles have only a chance to be there
        existence_chance = abs(roles[role]['chance'])
        if existence_chance > 100:
            existence_chance = existence_chance % 100
            log.debug("Role with higher existence trimmed to <= 100")
 
        # show person to other roles
        if len(roles[role]['visible_to']) > 0:
            visible_to = roles[role]['visible_to']
            visible_to_data[role] = {'show_to': visible_to, 'entities': []}

        for _ in range(roles[role]['amount']):
            
            role_pool.append(roles[role])

    if not len(role_pool) >= len(players.keys()):
        log.error("Not enough roles")
        log.debug("Roles: {}".format([role['name'] for role in role_pool]))
        log.debug("Player count: {}".format(len(players.keys())))
        exit(-1)

    shuffle(role_pool)
    log.debug("Shuffled roles")

    allocated_roles_index = []
    for player_ind in range(len(players.keys())):
        player = list(players.keys())[player_ind]
        if players[player]['force_role'] is not None:
            for role_ind in range(len(role_pool)):
                if role_pool[role_ind]['name'] == players[player]['force_role']:
                    tmp = copy.deepcopy(role_pool[role_ind])
                    role_pool[role_ind] = role_pool[player_ind]
                    role_pool[player_ind] = tmp
                    break
            else:
                log.error("Forced role '{}' of player '{}' was not in role_pool".format(players[player]['force_role'], player))
                exit()
    
    # give each player a role
    for index in range(len(players.keys())):
        player = players[list(players.keys())[index]]
        player['kTimeStamp'] = False
        player['dead'] = False
        
        # player has no forced role
        if 'role' not in player:
            
            if 'parent_role' in role_pool[index]:
                if existence_chance > randint(0,100):
                    player['role'] = role_pool[index]
                else:
                    log.debug("Role discarded: {}".format(roles[role]['name']))
                    player['role'] = roles[role_pool[index]['parent_role']]
            else:
                player['role'] = role_pool[index]
        log.debug("Role selected: {} ({})".format(roles[role]['name'], player['name']))

        # populate visibility of roles
        got_role = player['role']['name']
        if got_role in list(visible_to_data.keys()):
            visible_to_data[got_role]['entities'].append(player['name'])

    for role in list(visible_to_data):
        if len(visible_to_data[role]['entities']) == 0:
            visible_to_data.pop(role)

    # add visibility of roles to player_data
    for index in range(len(players.keys())):
        player = players[list(players.keys())[index]]
        got_role = player['role']['name']
        for role, role_data in visible_to_data.items():
            if got_role in role_data['show_to']:
                if 'other_role_info' in player.keys():
                    player['other_role_info'].update({role: role_data})
                else:
                    player['other_role_info'] = {role: copy.deepcopy(role_data)}

    # remove self name and empty groups
    for player in players:
        if 'other_role_info' in players[player]:
            print(players[player]['other_role_info'])

            # iterate through role visibility until own name found
            for role in players[player]['other_role_info']:
                for tmp in players[player]['other_role_info'][role]['entities']:
                    if tmp == players[player]['name']:
                        players[player]['other_role_info'][role]['entities'].remove(players[player]['name'])
                        break
                else:
                    continue
                break

    log.info("Distributed roles")
    return players, visible_to_data


def distribute_tasks(players, tasks):
    
    tmp_list = list(players.items())
    shuffle(tmp_list)
    players = dict(tmp_list)
    for player in players:

        counter = const.TASKS_PER_PLAYER
        if const.TASKS_SlIGHT_RANDOMNESS:
            if randint(0,10) > 8:
                counter -= 1

        players[player]['tasks'] = []

        to_be_deleted = []
        task_items = list(tasks.items())
        shuffle(task_items)
        for task_id, task in task_items:

            tmp_task = {}
            players[player]['tasks'].append(copy.deepcopy(task))
            
            if players[player]['role']['has_tasks']:
                tasks[task_id]['max_existence'] -= 1

                if tasks[task_id]['max_existence'] == 0:
                    to_be_deleted.append(task_id)

            counter -= 1
            if counter == 0:
                break
        
        for task_id in to_be_deleted:
            tasks.pop(task_id)
    return players
