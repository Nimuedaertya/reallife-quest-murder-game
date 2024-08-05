# imports
import yaml
import logging as log

# specific imports
from os import listdir
from os.path import isfile, join
from schematics.exceptions import DataError, ValidationError
from static_variables import PATH_YAML_PLAYERS, PATH_YAML_ROLES, PATH_YAML_TASK_DIR, PATH_TEMPLATE_TASKS_DEFAULT
from schematics.models import Model
from schematics.types import StringType, BooleanType, ListType, IntType

###
# functions
###


def load_players(path=None):
    """Load player yaml file from static path"""

    if path is None:
        players = load_yaml(PATH_YAML_PLAYERS)
    else:
        players = load_yaml(path)

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


def load_roles(path=None):
    """Load roles yaml file from static path"""

    if path is None:
        roles = load_yaml(PATH_YAML_ROLES)
    else:
        roles = load_yaml(path)

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


def load_tasks(path=None):
    """Load task yaml files from static directory"""

    if path is None:
        all_files = [f for f in listdir(PATH_YAML_TASK_DIR) if isfile(join(PATH_YAML_TASK_DIR, f))]
        tmp = {}
        for file in all_files:

            # check if file has yaml suffix
            filename_splitted = file.split(".")
            if len(filename_splitted) < 2 or not ("yml" in filename_splitted[-1]):
                log.warning("Invalid task file name (has to end with .yml): {}".format(file))
                continue

            # load yaml file
            file_path = join(PATH_YAML_TASK_DIR, file)
            file_tasks = load_yaml(file_path)
            log.debug("Loading task file: {}".format(file_path))

            # update task dictionary with tasks
            tmp = tmp | file_tasks
    else:
        tmp = load_yaml(path)

    # validation for each task
    for identifier, task in list(tmp.items()):
        task['id'] = identifier
        try:
            validator_obj = TaskModel(task)
            validator_obj.validate()
            tmp[identifier] = validator_obj.serialize()
        except (DataError, ValidationError) as e:
            log.error("Task validation failed at task '{}': {}".format(id, e))
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
    can_kill = BooleanType(default=False)
    parent_role = StringType()
    amount = IntType(required=True)
    chance = IntType(default=100)

    def validate_parent_role(self, data, value):
        if data['parent_role'] is None:
            data.pop('parent_role')


class TaskModel(Model):
    id = StringType(required=True)
    name = StringType(required=True)
    description = StringType(required=True)
    max_existence = IntType(required=True)
    task_done = BooleanType(default=False, choices=[False, True])
    path_to_template = StringType(default=PATH_TEMPLATE_TASKS_DEFAULT)
