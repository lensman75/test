# -*- coding: utf-8 -*-
import os
import sys

from flask import request


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'fc7253fa85e5a4faa285b0bc41c2bbdbd18c293f'
    MONGODB_SETTINGS = {'db': 'lod', 'alias': 'default'}

    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = False
    SECURITY_POST_LOGIN_VIEW = '/'
    SECURITY_POST_LOGOUT_VIEW = '/login'
    SECURITY_SEND_REGISTER_EMAIL = False

    UPLOAD_FOLDER = '/tmp/'  # in ~/

    SECURITY_TRACKABLE = False

    LANGUAGES = {
        'uk': 'uk_UA',
    }

    # EDBO_HOST = 'http://194.146.142.183'
    EDBO_HOST = 'http://192.168.0.78'
    EDBO_TEST_PORT = '9090'
    EDBO_ROOT_PORT = '80'
    EDBO_SUFFIX = '/data/EDEBOWebApi'
    EDBO_UNIVER_KEY = 'SEF2YzJpMVRrOFc2MEc1RmNRbjhSN1hwZlA0dnk1eDJYMVhQYUdQVndZalVEZjA0dTJwcnMycExPZzducEZ1cUw0aTlVckVHYkNOMlljVmFaOWFHUWZLNU5tYTRKQkcxRDNqSzYxamR5VHEwcXdYTHY3eXBFWUxFdW94SHFLN0s='


class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_PANELS = (
        'flask.ext.debugtoolbar.panels.versions.VersionDebugPanel',
        'flask.ext.debugtoolbar.panels.timer.TimerDebugPanel',
        'flask.ext.debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask.ext.debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask.ext.debugtoolbar.panels.template.TemplateDebugPanel',
        'flask.ext.debugtoolbar.panels.logger.LoggingPanel',
        'flask.ext.mongoengine.panels.MongoDebugPanel'
    )
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    CELERY_RESULT_BACKEND = 'amqp'
    # CELERY_RESULT_BACKEND = 'cache'
    CELERY_CACHE_BACKEND = 'amqp'
    CELERY_BACKEND = 'amqp'
    CELERY_BROKER = 'amqp://'
    # CELERY_BROKER = 'amqp://guest:**@127.0.0.1:5672//'
    # CELERY_ALWAYS_EAGER = True  # must be commented to celery working on server / on local uncomment


class TestingConfig(Config):
    TESTING = True


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
VENS_ROOT = os.path.dirname(sys.executable)
if not os.path.exists(VENS_ROOT + '/wkhtmltopdf'):
    VENS_ROOT = '/srv/apps/venvs/lod/bin'
if not os.path.exists(VENS_ROOT + '/wkhtmltopdf'):
    VENS_ROOT = '/usr/bin/'
STATIC_FOLDER_PATH = os.path.join(APP_ROOT, 'modules/static/')
SABBATICAL_PATH = os.path.join(APP_ROOT, 'modules/static/Sabbatical')
LOG_PATH = os.path.join(APP_ROOT, 'modules/static/logs/')
QW_PROTECTIONS_PATH = os.path.join(APP_ROOT, 'modules/static/QW_PROTECTIONS/')
DIPLOMA_SUPPLEMENT_PATH = os.path.join(APP_ROOT, 'modules/static/DiplomaSupplement')
MAGAZINES_PATH = os.path.join(APP_ROOT, 'modules/static/Magazines')
EXPORT_MARK_PATH = os.path.join(APP_ROOT, 'modules/static/ExportMark/')
FILES_FOR_DECREE = os.path.join(APP_ROOT, 'modules/static/FilesForDecree/')
ACCOUNTING = os.path.join(APP_ROOT, 'modules/static/Accounting/')
SUBJECTS_OF_GROUP = os.path.join(APP_ROOT, 'modules/static/SubjectsOfGroup/')
TRIZUB = os.path.join(APP_ROOT, 'modules/static/trizub.png')
EMBLEM = os.path.join(APP_ROOT, 'modules/static/emblem.jpg')
WATERMARK = os.path.join(APP_ROOT, 'modules/static/watermark.pdf')
BACHELORS = os.path.join(APP_ROOT, 'modules/static/bachelors.json')
RATINGXLS = os.path.join(APP_ROOT, 'modules/static/copy_rating.xls')
METHODIC = os.path.join(APP_ROOT, 'modules/static/methodic_for_magister.doc')
SPECIALISTS = os.path.join(APP_ROOT, 'modules/static/specialists.json')
LOD = os.path.join(APP_ROOT, 'modules/static/LOD.png')
DIAGRAM_FOR_DS_V4 = os.path.join(APP_ROOT, 'modules/static/Diag.png')
DIAGRAM_ENG_FOR_DS_V4 = os.path.join(APP_ROOT, 'modules/static/Diag_eng.png')
ADD_SCORES_PATH = os.path.join(APP_ROOT, 'modules/static/additional_scores/')
NUMBER_TO_WORD = {
    0: "Нуль",
    100: "Сто",
    101: "Сто один",
    102: "Сто два",
    103: "Сто три",
    104: "Сто чотири",
    105: "Сто п'ять",
    106: "Сто шість",
    107: "Сто сім",
    108: "Сто вісім",
    109: "Сто дев'ять",
    110: "Сто десять",
    111: "Сто одинадцять",
    112: "Сто дванадцять",
    113: "Сто тринадцять",
    114: "Сто чотирнадцять",
    115: "Сто п'ятнадцять",
    116: "Сто шістнадцять",
    117: "Сто сімнадцять",
    118: "Сто вісімнадцять",
    119: "Сто дев'ятнадцять",
    120: "Сто двадцять",
    121: "Сто двадцять один",
    122: "Сто двадцять два",
    123: "Сто двадцять три",
    124: "Сто двадцять чотири",
    125: "Сто двадцять п'ять",
    126: "Сто двадцять шість",
    127: "Сто двадцять сім",
    128: "Сто двадцять вісім",
    129: "Сто двадцять дев'ять",
    130: "Сто тридцять",
    131: "Сто тридцять один",
    132: "Сто тридцять два",
    133: "Сто тридцять три",
    134: "Сто тридцять чотири",
    135: "Сто тридцять п'ять",
    136: "Сто тридцять шість",
    137: "Сто тридцять сім",
    138: "Сто тридцять вісім",
    139: "Сто тридцять дев'ять",
    140: "Сто сорок",
    141: "Сто сорок один",
    142: "Сто сорок два",
    143: "Сто сорок три",
    144: "Сто сорок чотири",
    145: "Сто сорок п'ять",
    146: "Сто сорок шість",
    147: "Сто сорок сім",
    148: "Сто сорок вісім",
    149: "Сто сорок дев'ять",
    150: "Сто п'ятдесят",
    151: "Сто п'ятдесят один",
    152: "Сто п'ятдесят два",
    153: "Сто п'ятдесят три",
    154: "Сто п'ятдесят чотири",
    155: "Сто п'ятдесят п'ять",
    156: "Сто п'ятдесят шість",
    157: "Сто п'ятдесят сім",
    158: "Сто п'ятдесят вісім",
    159: "Сто п'ятдесят дев'ять",
    160: "Сто шістдесят",
    161: "Сто шістдесят один",
    162: "Сто шістдесят два",
    163: "Сто шістдесят три",
    164: "Сто шістдесят чотири",
    165: "Сто шістдесят п'ять",
    166: "Сто шістдесят шість",
    167: "Сто шістдесят сім",
    168: "Сто шістдесят вісім",
    169: "Сто шістдесят дев'ять",
    170: "Сто сімдесят",
    171: "Сто сімдесят один",
    172: "Сто сімдесят два",
    173: "Сто сімдесят три",
    174: "Сто сімдесят чотири",
    175: "Сто сімдесят п'ять",
    176: "Сто сімдесят шість",
    177: "Сто сімдесят сім",
    178: "Сто сімдесят вісім",
    179: "Сто сімдесят дев'ять",
    180: "Сто вісімдесят",
    181: "Сто вісімдесят один",
    182: "Сто вісімдесят два",
    183: "Сто вісімдесят три",
    184: "Сто вісімдесят чотири",
    185: "Сто вісімдесят п'ять",
    186: "Сто вісімдесят шість",
    187: "Сто вісімдесят сім",
    188: "Сто вісімдесят вісім",
    189: "Сто вісімдесят дев'ять",
    190: "Сто дев'яносто",
    191: "Сто дев'яносто один",
    192: "Сто дев'яносто два",
    193: "Сто дев'яносто три",
    194: "Сто дев'яносто чотири",
    195: "Сто дев'яносто п'ять",
    196: "Сто дев'яносто шість",
    197: "Сто дев'яносто сім",
    198: "Сто дев'яносто вісім",
    199: "Сто дев'яносто дев'ять",
    200: "Двісті"
}

estimate_division = [
    (60, 62),
    (63, 65),
    (66, 68),
    (69, 71),
    (72, 74),
    (75, 77),
    (78, 80),
    (81, 83),
    (84, 86),
    (87, 89),
    (90, 92),
    (93, 95),
    (96, 98),
    (99, 100)
]