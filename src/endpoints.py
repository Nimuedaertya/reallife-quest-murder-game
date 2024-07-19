# imports
import argparse
import logging as log
import static_variables as const

# specific impors
from flask import Flask, render_template, request, redirect, jsonify
from flask_classful import FlaskView, route
from flask_socketio import SocketIO, emit
from flask_assets import Bundle, Environment
from loading import load_roles, load_tasks, load_players
from init_round import distribute_roles, distribute_tasks

###
# statics
###

ENDPOINT_USERS = '/user'
ENDPOINT_ADMIN = '/admin'
ENDPOINT_ADMIN_JSON = '/adminjson'

###
# globals
###

app = Flask(__name__)
assets = Environment(app)
css = Bundle(const.PATH_CSS_INPUT, output=const.PATH_CSS_OUTPUT)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = const.FLASK_SECRET_KEY
https_enabled = False

###
# Websocket
# documentation: https://flask-socketio.readthedocs.io/en/latest/getting_started.html#initialization
###


# The report Message which is send to all users on the Website on this time
@socketio.on('report')
def reporting(message):
    emit('report', message['data'], broadcast=True)
    print('received message: ' + str(message))


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


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
            return render_template(const.PATH_TEMPLATE_INDEX)

        if request.method == 'POST':
            user = request.form['User']
            return redirect(ENDPOINT_USERS + '/' + user)

    @route(ENDPOINT_ADMIN, methods=['GET'])
    def admin(self):
        return render_template(const.PATH_TEMPLATE_ADMIN, data=self.data)

    @route(ENDPOINT_ADMIN_JSON, methods=['GET'])
    def adminjson(self):
        return self.data

    @route('/players', methods=['GET'])
    def players(self):

        all_players = len(self.data.keys())
        alive = 0
        for player in self.data:
            if self.data[player]['dead'] is False:
                alive += 1

        return render_template(const.PATH_TEMPLATE_PLAYERS, number_all=all_players, number_alive=alive)

    @route(ENDPOINT_USERS + '/<username>', methods=['GET', 'POST'])
    def user(self, username):

        if request.method == 'GET':
            if username not in self.data:
                return redirect('/')

            user_data = self.data[username]

            return render_template(const.PATH_TEMPLATE_PLAYER_INFO, username=username, data=user_data)

        if request.method == 'POST':
            dead_bool = request.form['dead_button']
            self.data[username]['dead'] = dead_bool
            return "TOP"

    @route('/tasks/<task>', methods=['POST', 'GET'])
    def data_tasks(self, task):
        if request.method == 'GET':
            return render_template(self.tasks[task]['path_to_template'], task=self.tasks[task])

        if request.method == 'POST':

            name = request.form['Name']

            if name in self.data and task in [x['id'] for x in self.data[name]['tasks']]:
                for i in self.data[name]['tasks']:
                    if i['id'] == task:
                        i['task_done'] = True
                        break
                return render_template(const.PATH_TEMPLATE_SUCCESSFUL_TASK, name=name)

            # Default return
            return render_template(const.PATH_TEMPLATE_FAILED_TASK)

    @route('/tasks', methods=['GET'])
    def task_overview(self,):

        overall = 0
        completed = 0

        for player in self.data:
            if self.data[player]['role']['has_tasks']:
                overall += len(self.data[player]['tasks'])
                for task in self.data[player]['tasks']:
                    if task['task_done']:
                        completed += 1

        return render_template('tasks_overview.html', amount_tasks=overall, completed_tasks=completed)

    @route('/getTimer/', methods=['POST'])
    def getTimer(self):
        return jsonify({'kTimer': const.KTIMER})

    @route('/killTime/<user>', methods=['POST'])
    def killT(self, user):
        timeStamp = request.form.get('timeStamp')
        if timeStamp:
            self.data[user]['kTimeStamp'] = int(timeStamp)
        else:
            self.data[user]['kTimeStamp'] = False
        return str(const.KTIMER)

    @route('/kill/<user>', methods=['POST'])
    def kill_post(self, user):
        if self.data[user]['kTimeStamp']:
            return jsonify({'going': True, 'timeStamp': self.data[user]['kTimeStamp']})
        else:
            return jsonify({'going': False, 'timeStamp': None})

    @route('/alive/<user>', methods=['GET'])
    def kill_get(self, user):
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
    # needed for notifications and qr_scanner
    parser.add_argument('-s', '--secure',
                        action='store_true')
    parser.add_argument('-p', '--public',
                        action='store_true')
    parser.add_argument('--port')

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
    Round.register(app, route_base='/')
    game = Round()

    # set pport
    port = const.DEFAULT_PORT
    if args.port:
        port = args.port

    # need --public flag to be available in network
    if args.secure:
        if args.public:
            log.info("Public https server will be started")
            socketio.run(app, host="0.0.0.0", port=port, ssl_context=(const.PATH_SSL_CERT, const.PATH_SSL_KEY))

        else:
            log.info("Local https server will be started")
            socketio.run(app,
                         port=port,
                         allow_unsafe_werkzeug=True,
                         debug=True,
                         ssl_context=(const.PATH_SSL_CERT, const.PATH_SSL_KEY)
                         )

    else:
        if args.public:
            log.info("Public http server will be started")
            app.run(host="0.0.0.0", port=port)

        else:
            log.info("Local http server will be started")
            app.run(port=port, debug=True)
