import init_round as init


class TestDistributeRoles:

    players = {
                    'dummy1': {'name': 'dummy', 'force_role': None},
                    'dummy2': {'name': 'dummy2', 'force_role': None},
                    'dummy3': {'name': 'dummy3', 'force_role': None}
                    }

    vamps = 0
    crews = 2
    impos = 1
    jacks = 0
    roles = {
            'Crewmate':
                {
                      'name': 'Crewmate',
                      'description':
                      'Complete all tasks or vote all Imposters out!',
                      'visible_to': [],
                      'has_tasks': True,
                      'amount': crews,
                      'chance': 100
                },
            'Imposter':
                {
                    'name': 'Imposter',
                    'description': 'Kill all Crewmates',
                    'visible_to': ['Imposter', 'Lawyer', 'Vampire'],
                    'has_tasks': False,
                    'amount': impos,
                    'chance': 100
                },
            'Vampire':
                {
                    'name': 'Vampire',
                    'description': '',
                    'visible_to': ['Imposter', 'Lawyer', 'Vampir'],
                    'has_tasks': False,
                    'parent_role': 'Imposter',
                    'amount': vamps,
                    'chance': 100},
            'Jackal':
                {
                    'name': 'Jackal',
                    'description': '',
                    'visible_to': [],
                    'has_tasks': False,
                    'amount': jacks,
                    'chance': 100}
            }

    def test_distribute_roles_visible_to(self):
        players, visible_to = init.distribute_roles(self.players, self.roles)

        assert len(visible_to) == 1
        assert 'Imposter' in visible_to
        assert 'entities' in visible_to['Imposter']
        assert visible_to['Imposter']['entities'][0] in [x['name'] for x in self.players.values()]

    def test_distribute_roles_players(self):
        players, visible_to = init.distribute_roles(self.players, self.roles)
        
        assert len(players) == len(self.players)
