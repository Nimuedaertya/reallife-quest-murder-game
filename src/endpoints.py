# imports
import argparse
import logging as log
import copy

# specific impors
from flask import url_for, Flask, render_template, request, redirect, jsonify
from flask_classful import FlaskView, route
from flask_assets import Bundle, Environment
from loading import load_roles, load_tasks, load_players
from init_round import distribute_roles, distribute_tasks
from random import sample

###
# statics
###

ENDPOINT_USERS = '/user'
ENDPOINT_ADMIN = '/admin'
PATH_TEMPLATE_INDEX = 'index.html'
PATH_TEMPLATE_PLAYER_INFO = 'player_info.html'
PATH_TEMPLATE_PLAYERS = 'players.html'
PATH_TEMPLATE_SUCCESSFUL_TASK = 'successful_task.html'
PATH_TEMPLATE_FAILED_TASK = 'try_again_task.html'
PATH_CSS_INPUT = 'src/input.css'
PATH_CSS_OUTPUT = 'src/styles/output.css'
KTIMER = 20 # XXX
TASKS_07_DRAW_LIST = ["Hund", "Heuballen", "Haus", "Ziege", "Frosch", "Pferd", "Vase", "Blumen", "Rosenstrauch", "Bücherregal", "Schachbrett", "Bett", "Essen", "Palme"]

###
# globals
###

app = Flask(__name__)
assets = Environment(app)
css = Bundle(PATH_CSS_INPUT, output=PATH_CSS_OUTPUT)

###
# classes
###

class Round(FlaskView):
    
    roles = load_roles()
    tasks = load_tasks()
    players = load_players()
    players, visible_to_data = distribute_roles(players, roles)
    players = distribute_tasks(players, tasks)
    data = players
    
    @route('/', methods=['GET', 'POST'])
    def index(self):
        if request.method == 'GET':
            return render_template(PATH_TEMPLATE_INDEX)

        if request.method == 'POST':
            user = request.form['User']
            return redirect(ENDPOINT_USERS + '/' + user)


    @route(ENDPOINT_ADMIN, methods=['GET'])
    def admin(self):
        return self.data


    @route('/players', methods=['GET'])
    def players(self):

        all_players = len(self.data.keys())
        alive = 0
        for player in self.data:
            if self.data[player]['dead'] == False:
                alive += 1

        return render_template(PATH_TEMPLATE_PLAYERS, number_all=all_players, number_alive=alive)



    @route(ENDPOINT_USERS + '/<username>', methods=['GET', 'POST'])
    def user(self, username):

        if request.method == 'GET':
            if username not in self.data:
                return redirect('/')

            user_data = self.data[username]

            return render_template(PATH_TEMPLATE_PLAYER_INFO, username=username, data=user_data)

        if request.method == 'POST':
            dead_bool = request.form['dead_button']
            self.data[username]['dead'] = dead_bool
            return "TOP"


    @route('/tasks/<task>', methods = ['POST', 'GET'])
    def data_tasks(self, task):
        if request.method == 'GET':
            print(self.tasks.keys())
            print(self.tasks[task].keys())
            return render_template(self.tasks[task]['path_to_template'], task=self.tasks[task])

        if request.method == 'POST':

            name = request.form['Name']
            
            if name in self.data and task in [x['id'] for x in self.data[name]['tasks']]:
                for i in self.data[name]['tasks']:
                    if i['id'] == task:
                        i['task_done'] = True
                        break
                return render_template(PATH_TEMPLATE_SUCCESSFUL_TASK, name = name)

            # Default return
            return render_template(PATH_TEMPLATE_FAILED_TASK)


    @route('/tasks', methods = ['GET'])
    def task_overview(self,):
        
        overall = 0
        completed = 0

        for player in self.data:
            if self.data[player]['role']['has_tasks']:
                overall += len(self.data[player]['tasks'])
                for task in self.data[player]['tasks']:
                    if task['task_done']:
                        completed += 1
           
        return render_template('tasks_overview.html', amount_tasks = overall, completed_tasks = completed)


    @route('/getTimer/', methods=['POST'])
    def getTimer(self):
        return jsonify({'kTimer': KTIMER})


    @route('/killTime/<user>', methods=['POST'])
    def killT(self, user):
        timeStamp = request.form.get('timeStamp')
        if timeStamp:
            self.data[user]['kTimeStamp'] = int(timeStamp)
        else:
            self.data[user]['kTimeStamp'] = False
        return str(KTIMER)


    @route('/kill/<user>',methods=['POST'])
    def kill(self, user):
        if self.data[user]['kTimeStamp']:
            return jsonify({'going': True, 'timeStamp': self.data[user]['kTimeStamp']})
        else:
            return jsonify({'going': False, 'timeStamp': None})


    @route('/alive/<user>', methods=['GET'])
    def kill(self, user):
        return jsonify({'dead': self.data[user]['dead']})


if __name__ == '__main__':
    
    # read passed arguments
    parser = argparse.ArgumentParser(
            prog="Space Mafia IRL",
            description='Space Mafia with QR-Codes and Real Life Application',
            )
    parser.add_argument('-v', '--verbose',
                        action='store_true')
    parser.add_argument('-vv', '--extended_verbose',
                        action='store_true')
    parser.add_argument('-p', '--public',
                        action='store_true')

    args = parser.parse_args()
    
    # configure logger
    if args.verbose:
        log.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%I:%M:%S %p', level=log.INFO)
        log.info("Verbose output.")
    elif args.extended_verbose:
        log.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%I:%M:%S %p', level=log.DEBUG)
        log.info("Verbose output.")
    else:
        log.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%I:%M:%S %p')
    
    # css
    assets.register("css", css)
    css.build()

    # create round object
    Round.register(app, route_base = '/')
    game = Round()

    # need --public flag to be available in network
    if args.public:
        log.info("Public server will be started")
        app.run(debug = True, host="0.0.0.0")
    # start server normally on localhost
    else:
        log.info("Local server will be started")
        app.run(debug = True)
