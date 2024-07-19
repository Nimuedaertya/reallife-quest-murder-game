DEFAULT_PORT = 5000

###
# paths
###
PATH_YAML_PLAYERS = "config/players.yml"
PATH_YAML_ROLES = "config/roles.yml"
PATH_YAML_TASK_DIR = "config/tasks/"
PATH_TEMPLATE_TASKS_DEFAULT = "task_basic.html"
PATH_TEMPLATE_INDEX = 'index.html'
PATH_TEMPLATE_PLAYER_INFO = 'player_info.html'
PATH_TEMPLATE_PLAYERS = 'players.html'
PATH_TEMPLATE_SUCCESSFUL_TASK = 'successful_task.html'
PATH_TEMPLATE_FAILED_TASK = 'try_again_task.html'
PATH_CSS_INPUT = 'src/input.css'
PATH_CSS_OUTPUT = 'src/styles/output.css'
PATH_SSL_CERT = 'config/certs/cert.pem'
PATH_SSL_KEY = 'config/certs/key.pem'
KTIMER = 20  # XXX

###
# tasks
###
TASKS_PER_PLAYER = 7
TASKS_SlIGHT_RANDOMNESS = True

###
# secrets
###
# this secret is only important for publicly used instances of this application (not recommended case)
FLASK_SECRET_KEY = 'keep_me_secret!'

###
# qr code
###
QR_CODE_BASE_ADDRESS = "http://192.168.0.1:5000/tasks/{}"
QR_CODE_PDF_FILE = 'qr_codes/qr_codes{}.pdf'
QR_CODE_PATH_INFO = 'qr_codes/info'
QR_CODE_FONT = 'Helvetica'
QR_CODE_FONT_SIZE = 21
QR_CODE_PATH_IMG = "qr_codes/"
