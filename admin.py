# -*- coding: utf-8 -*-
import os
import random
import string
import re
import datetime
from pprint import pprint


from flask import Flask, Response, make_response, render_template, json, abort, jsonify
from flask.json import JSONEncoder
from flask import request, url_for
from flask_login import current_user

from config import APP_ROOT

from modules.jiq_connection.token import Token


app = Flask(__name__)

# ---------------------

import traceback
from time import sleep, strptime, mktime

from collections import defaultdict

import sys
import xlrd

from flask.ext.admin.base import MenuLink, Admin
from flask.ext.babelex import Babel
from flask.ext.celeryext import FlaskCeleryExt
from flask.ext.security import Security, MongoEngineUserDatastore
from mongoengine import connect, ValidationError, MultipleObjectsReturned, DoesNotExist, Q
from mongoengine.base.common import get_document
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename

from config import APP_ROOT
from modules import app
from modules.address.models import AddressCombinations, District, Region, Settlement
from modules.address.updater import update_address
from modules.address.view import AddressView, DistrictView, RegionView, SettlementView
from modules.setting import CATEGORY_ADD_SCORES, TYPE_WORK_CHOICES, ECTS_CHOICES, EDUCATION_FORM
from modules.utils.date import StudyYear

ext = FlaskCeleryExt(app)

from modules.profession import QualificationLevel, ProffOptions, ProffOptionsView, ProfesionView, \
    QualificationLevelView, EducationalProgramMain, SpecialisationView, Qualification, QualificationView, \
    KnowledgeField, \
    KnowledgeFieldView, LevelOfQualification, LevelOfQualificationView, OfficialDurationOfProgramme, \
    OfficialDurationOfProgrammeView, AcquiredCompetences, AcquiredCompetencesView, AcademicRights, AcademicRightsView, \
    AccessRequirements, AccessRequirementsView
from modules.fields import DateField
from modules.document import DocumentType, DocumentTypeView, Order, OrderView

from modules.student import Student, AdditionalScores
from modules.unit.models import AcademicGroup
from modules.unit.views import AcademicGroupView, DepartamentView, InstituteView, UniversityView, PHView, \
    GroupMagAdditionView, GroupBacAdditionView, ArchiveAcademicGroupView, GraduateView, AlienCenterView

from modules.subject.view import SubjectView, TeacherView
from modules.subject.models import Subject, Teacher
from modules.views import *
from modules.estimates import Mark, Sheet, Slider

from modules.user.form import CustomLoginForm

user_datastore = MongoEngineUserDatastore(db, User, None)
security = Security(app, user_datastore, login_form=CustomLoginForm)
babel = Babel(app, default_locale='uk', )

celery = ext.celery
from modules.estimates.views import RatingStipendView, StipendOrderView, RatingFixerView
db = connect('lod_3test', alias='default')


def create_role():
    check_role=Role.objects(name=str(sys.argv[3]))
    if check_role:
        print 'DB has same role!'
    else:
        role = Role(name=str(sys.argv[3]))
        role.save()
        print 'Role was successful created!'


def create_user():
    check_user=User.objects(login=str(sys.argv[3]), password=str(sys.argv[4]))
    if check_user:
        print 'DB has same user!'
    else:
        user = User(login=str(sys.argv[3]), password=str(sys.argv[4]))
        user.save()
        print 'User was successful created!'


command = str(sys.argv[1])
print command

if command == "create":
    if str(sys.argv[2]) == "role":
        if len(sys.argv) != 4:
            print "Invalid count arguments"
        else:
            create_role()
    if str(sys.argv[2]) == "user":
        if len(sys.argv) != 5:
            print "Invalid count arguments"
        else:
            create_user()
    if str(sys.argv[2]) != "user" and str(sys.argv[2]) != "role":
        print "unrecognised parameter!"
else:
    print 'unrecognised command!'
    exit()

