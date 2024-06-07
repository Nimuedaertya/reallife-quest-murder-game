import loading


PATH_PLAYERS = "tests/test_loading_config_files/players.yml"
PATH_ROLES = "tests/test_loading_config_files/roles.yml"
PATH_TASKS = "tests/test_loading_config_files/tasks.yml"


def test_loading_players():
    tmp = loading.load_players(PATH_PLAYERS)
    validator = loading.PlayerModel()
    for player in tmp:
        validator.validate(player)


def test_loading_players_default():
    loading.load_players()


def test_loading_roles():
    tmp = loading.load_roles(PATH_ROLES)
    validator = loading.RoleModel()
    for role in tmp:
        validator.validate(role)


def test_loading_roles_default():
    loading.load_roles()


def test_loading_tasks():
    tmp = loading.load_tasks(PATH_TASKS)
    validator = loading.TaskModel()
    for task in tmp:
        validator.validate(task)


def test_loading_tasks_default():
    loading.load_tasks()
