# imports
import copy
import yaml
import logging as log

# specific imports
from schematics.exceptions import DataError, ValidationError
from static_variables import PATH_YAML_PLAYERS, PATH_YAML_ROLES, PATH_YAML_TASKS_NO_PREP, PATH_YAML_TASKS_ONCE_PREP, PATH_YAML_TASKS_ALWAYS_PREP, PATH_TEMPLATE_TASKS_DEFAULT
from schematics.models import Model
from schematics.types import StringType, BooleanType, ListType, IntType, DictType, ModelType, BaseType

###
# functions
###

def load_players():
    """Load player yaml file from static path"""

    players = load_yaml(PATH_YAML_PLAYERS)
    
    error = False
    for tmp, player in players.items():
        try:
            validator_obj = PlayerModel(player)
            validator_obj.validate()
            players[tmp] = validator_obj.serialize()
        except (DataError, ValidationError) as e:
            log.error("Task validation failed at player '{}' with error: {}".format(tmp, e))
            error = True
    
    if error:
        exit(-1)
    log.info("Players validated successfully")

    return players


def load_roles():
    """Load roles yaml file from static path"""

    roles = load_yaml(PATH_YAML_ROLES)
    
    error = False
    for tmp, role in roles.items():
        try:
            validator_obj = RoleModel(role)
            validator_obj.validate()
            roles[tmp] = validator_obj.serialize()
        except (DataError, ValidationError) as e:
            log.error("Task validation failed at role '{}' with error: {}".format(tmp, e))
            error = True
    
    if error:
        exit(-1)
    log.info("Roles validated successfully")

    return roles


def load_tasks():
    """Load task yaml file from static path"""

    tasks_no_prep = load_yaml(PATH_YAML_TASKS_NO_PREP)
    tasks_once_prep = load_yaml(PATH_YAML_TASKS_ONCE_PREP)
    tasks_always_prep = load_yaml(PATH_YAML_TASKS_ALWAYS_PREP)

    tmp = tasks_no_prep | tasks_once_prep | tasks_always_prep
    error = False
    for identifier, task in list(tmp.items()):
        task['id'] = identifier
        try:
            validator_obj = TaskModel(task)
            validator_obj.validate()
            tmp[identifier] = validator_obj.serialize()
        except (DataError, ValidationError) as e:
            log.error("Task validation failed at task '{}' with error: {}".format(id, e))
            error = True
    
    if error:
        exit(-1)
    log.info("Tasks validated successfully")

    return tmp

def load_yaml(path):
    """Load yaml file from path"""

    with open(path, 'r') as file:
        data = yaml.safe_load(file)
    log.debug("Fetched content from yaml file: {}".format(data))

    return data

###
# classes
###
"""Schematics classes for yaml input validation """

class PlayerModel(Model):
    name = StringType(required=True)
    force_role = StringType(default=None)

class RoleModel(Model):
    name = StringType(required=True, max_length=60)
    description = StringType(required=True)
    visible_to = ListType(StringType, default=[])
    has_tasks = BooleanType(default=True)
    parent_role = StringType()
    amount = IntType(required=True)
    chance = IntType(default=100) # in percent

class TaskModel(Model):
    id = StringType(required=True)
    name = StringType(required=True)
    description = StringType(required=True)
    max_existence = IntType(required=True)
    task_done = BooleanType(default=False, choices=[False, True])
    path_to_template = StringType(default=PATH_TEMPLATE_TASKS_DEFAULT)
