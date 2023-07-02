# -*- coding: utf-8 -*-
import os
import random
import string
import re
import datetime
import uuid
from pprint import pprint
from modules.history.utility import registration_actions_jiq

from flask import Flask, Response, make_response, render_template, json, abort, jsonify
from flask.json import JSONEncoder
from flask import request, url_for
from flask_login import current_user

from config import APP_ROOT

from modules.jiq_connection.token import Token

# app = Flask(__name__)

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
from modules.human import Human
from modules.student import Student, AdditionalScores
from modules.unit.models import AcademicGroup, AbstractUnitLayer, Departament, Institute
from modules.unit.views import AcademicGroupView, DepartamentView, InstituteView, UniversityView, PHView, \
    GroupMagAdditionView, GroupBacAdditionView, ArchiveAcademicGroupView, GraduateView, AlienCenterView

from modules.subject.view import SubjectView, TeacherView
from modules.subject.models import Subject, Teacher
from modules.views import *
from modules.estimates import Mark, Sheet, Slider

# ----------------------
import bson

abreviatures = {
    u'feeem': u'ФЕЕЕМ',
    u'fbtgp': u'ФБТЕГП',
    u'fitki': u'ФІТКІ',
    u'fksa': u'ФКСА',
    u'firen': u'ФІРЕН',
    u'fmt': u'ФМТ',
    u'fmib': u'ФМІБ',
    u'fiita': u'ФІІТА',
    u'fbtsei': u'ФБЦЕІ',
    u'fies': u'ФІЕС',
    u'inebmd': u'ІнЕБМД'
}

@app.route('/admin', methods=['POST', 'GET'])
def first_page():
    registration_actions_jiq(u'Звернення до LOD')
    req = request.json
    return 'Hello jiq!'


# echo return data
# for jiq main key is data
@app.route('/jiq', methods=['POST', 'GET'])
def send_request():
    registration_actions_jiq(u'Звернення до LOD')
    req = None
    try:
        req = request.json
    except:
        return Response(json.dumps({'status': 'fail', 'message': 'request not has json'}), status=406,
                        mimetype='application/json')
    if not req:
        return Response(json.dumps({'status': 'fail', 'message': 'request is empty'}), status=406,
                        mimetype='application/json')
    if 'data' not in req:
        return Response(json.dumps({'status': 'fail', 'message': 'request json not has data'}), status=406,
                        mimetype='application/json')

    return Response(json.dumps(req['data']), status=200, mimetype='application/json')


# validate sheet
# for jiq main key is data
@app.route('/jiq/sheet', methods=['POST', 'GET'])
def sheet():
    req = None
    try:
        req = request.json
    except:
        return Response(json.dumps({'status': 'fail', 'message': 'request not has json'}), status=406,
                        mimetype='application/json')

    if not req:
        return Response(json.dumps({'status': 'fail', 'message': 'request is empty'}), status=406,
                        mimetype='application/json')
    if 'data' not in req:
        return Response(json.dumps({'status': 'fail', 'message': 'request json not has data'}), status=406,
                        mimetype='application/json')

    result = jiq_sheet_validation(req['data'])
    status = json.loads(result).get("status")

    return Response(result, status=(200 if status == "success" else 400), mimetype='application/json')


# validate sheet and try create
# for jiq main key is data
@app.route('/jiq/sheet/create/<tok>', methods=['GET', 'POST'])
def token(tok):
    req = None
    try:
        req = request.json
    except:
        return Response(json.dumps({'status': 'fail', 'message': 'request not has json'}), status=406,
                        mimetype='application/json')

    # token len must be 24 chars
    if len(tok) != 24:
        return Response(json.dumps({'status': 'fail', 'message': u'Ключ не дійсний'}), status=403,
                        mimetype='application/json')

    # check if request empty
    if not req:
        return Response(json.dumps({'status': 'fail', 'message': 'request is empty'}), status=406,
                        mimetype='application/json')

    # check if request not has data
    if not 'data' in req:
        return Response(json.dumps({'status': 'fail', 'message': 'request json not has data'}), status=406,
                        mimetype='application/json')

    # try get token from DB
    try:
        token_obj = Token.objects(pk=tok)
    except ValueError:
        return Response(json.dumps({'status': 'fail', 'message': u'Ключ не дійсний ValueError'}), status=403,
                        mimetype='application/json')

    # check if token not empty
    if token_obj:
        registration_actions_jiq(
            u'Створення відомості (Користувач :  {0})'.format(token_obj[0].owner))
        for token in token_obj:

            # check if token not activated
            if token.actived is False:
                token.actived = True
                token.save()

                # check current date more date born
                if datetime.datetime.now() > token.date_born:

                    # check current date less date death
                    if datetime.datetime.now() < token.date_death:

                        if token.action == 'sheet.create':
                            result = jiq_sheet_validation(req['data'])

                            status = json.loads(result).get('status')  # parse json

                            if status == 'success':
                                result = jiq_sheet_create(req)
                                status = json.loads(result).get('status')
                                print status
                                return Response(result, status=(200 if status == "success" else 400),
                                                mimetype='application/json')

                            return Response(result, status=(200 if status == "success" else 400),
                                            mimetype='application/json')

                        return Response(json.dumps({'status': 'fail', 'message': u'Ключ не має доступу'}),
                                        status=400, mimetype='application/json')

                    return Response(json.dumps({'status': 'fail', 'message': u'Вийшов час сесії ключа'}), status=400,
                                    mimetype='application/json')

                return Response(json.dumps({'status': 'fail', 'message': u'Ключ не дійсний'}), status=400,
                                mimetype='application/json')

            return Response(json.dumps({'status': 'fail', 'message': u'Ключ був активований'}), status=400,
                            mimetype='application/json')

    return Response(json.dumps({'status': 'fail', 'message': u'Ключ не дійсний'}), status=400,
                    mimetype='application/json')


# validate slider
# for jiq main key is data
@app.route('/jiq/slider', methods=['POST', 'GET'])
def slider():
    req = None
    try:
        req = request.json
    except:
        return Response(json.dumps({'status': 'fail', 'message': 'request not has json'}), status=406,
                        mimetype='application/json')

    if not req:
        return Response(json.dumps({'status': 'fail', 'message': 'request is empty'}), status=406,
                        mimetype='application/json')
    if 'data' not in req:
        return Response(json.dumps({'status': 'fail', 'message': 'request json not has data'}), status=406,
                        mimetype='application/json')

    result = jiq_slider_validation(req['data'])
    status = json.loads(result).get("status")

    return Response(result, status=(200 if status == "success" else 400), mimetype='application/json')


# validate sheet and try create
# for jiq main key is data
@app.route('/jiq/slider/create/<tok>', methods=['GET', 'POST'])
def slider_token(tok):
    req = None
    try:
        req = request.json
    except:
        return Response(json.dumps({'status': 'fail', 'message': 'request not has json'}), status=406,
                        mimetype='application/json')

    # token len must be 24 chars
    if len(tok) != 24:
        return Response(json.dumps({'status': 'fail', 'message': u'Ключ не дійсний'}), status=403,
                        mimetype='application/json')

    # check if request empty
    if not req:
        return Response(json.dumps({'status': 'fail', 'message': 'request is empty'}), status=406,
                        mimetype='application/json')

    # check if request not has data
    if not 'data' in req:
        return Response(json.dumps({'status': 'fail', 'message': 'request json not has data'}), status=406,
                        mimetype='application/json')

    # try get token from DB
    try:
        token_obj = Token.objects(pk=tok)
    except ValueError:
        return Response(json.dumps({'status': 'fail', 'message': u'Ключ не дійсний ValueError'}), status=403,
                        mimetype='application/json')

    # check if token not empty
    if token_obj:
        registration_actions_jiq(
            u'Створення аркуша успішності (Користувач :  {0})'.format(token_obj[0].owner))

        for token in token_obj:

            # check if token not activated
            if token.actived is False:
                token.actived = True
                token.save()

                # check current date more date born
                if datetime.datetime.now() > token.date_born:

                    # check current date less date death
                    if datetime.datetime.now() < token.date_death:

                        if token.action == 'slider.create':
                            result = jiq_slider_validation(req['data'])

                            status = json.loads(result).get('status')  # parse json

                            if status == 'success':
                                result = jiq_slider_create(req['data'])
                                status = json.loads(result).get('status')
                                return Response(result, status=(200 if status == "success" else 400),
                                                mimetype='application/json')

                            return Response(result, status=(200 if status == "success" else 400),
                                            mimetype='application/json')

                        return Response(json.dumps({'status': 'fail', 'message': u'Ключ не має доступу'}),
                                        status=400, mimetype='application/json')

                    return Response(json.dumps({'status': 'fail', 'message': u'Вийшов час сесії ключа'}), status=400,
                                    mimetype='application/json')

                return Response(json.dumps({'status': 'fail', 'message': u'Ключ не дійсний'}), status=400,
                                mimetype='application/json')

            return Response(json.dumps({'status': 'fail', 'message': u'Ключ був активований'}), status=400,
                            mimetype='application/json')

    return Response(json.dumps({'status': 'fail', 'message': u'Ключ не дійсний'}), status=400,
                    mimetype='application/json')


@app.route('/back_up', methods=["GET"])
def back_up_fksa():
    originalAbr = u'ФМІБ'

    answer = {}

    departament = [
        # u'ФЕЕЕМ',
        #  u'ФБТЕГП',
        # u'ФІТКІ',
        u'ФКСА',
        # u'ФІРЕН',
        # u'ФМТ',
        # u'ФМІБ',
        # u
    ]

    for abr in departament:
        unitLayer = AbstractUnitLayer.objects(for_vstup_kompany=True)
        i = 0
        for gr in AcademicGroup.objects(is_archive=False, unit_layer__nin=unitLayer):
            if gr:
                if gr.unit_layer:
                    if gr.unit_layer.departament or gr.unit_layer.institute:
                        if (gr.unit_layer.departament and unicode(gr.unit_layer.departament.abbreviated) == abr) or \
                                (gr.unit_layer.institute and unicode(gr.unit_layer.institute.abbreviated) == abr):
                            answer[i] = {}
                            answer[i]['group'] = json.loads(gr.to_json())
                            answer[i]['students'] = []
                            for itr, st in enumerate(Student.objects(group=gr)):
                                if st.human:
                                    answer[i]['students'].append({itr: json.loads(st.to_json())})
                            i = i + 1

    return Response(json.dumps(answer),
                    status=200, mimetype='application/json', content_type='application/json')


@app.route("/get/subjects", methods=["GET"])
def fksa_subjects_for_jiq():
    answer = {}
    subjects = set()
    for gr in AcademicGroup.objects(is_archive=False):
        if gr:
            if gr.unit_layer:
                if gr.unit_layer.departament or gr.unit_layer.institute:
                    # if unicode(gr.unit_layer.departament.abbreviated) == u'ФКСА':
                    if gr.prof_layer:
                        if gr.prof_layer.subjects:
                            for key in gr.prof_layer.subjects:
                                part_of_key = key.split("@")[0]
                                subj = Subject.objects(id=part_of_key).first()
                                if subj.in_file:
                                    subjects.add(subj)
    list = []
    for el in subjects:
        list.append(({'name': el.name, 'uuid': el.uuid}))
    answer["subjects"] = list
    registration_actions_jiq(u'Перегляд предметів')
    return jsonify(answer)


@app.route("/get/semesters_subjects/<virtual>/<abr>/<period>", methods=["POST", "GET"])
def semester_subjects_for_jiq(virtual, abr, period):
    if virtual == u'0':
        virtual = [False, None]
    else:
        virtual = [True]
    if abr not in abreviatures:
        return Response(json.dumps({'status': 'fail', 'message': u'Структури не існує'}), status=400,
                        mimetype='application/json')
    answer = {}
    group_subjects = {}
    originalAbr = getInistituteAbr(abr)
    ab = None
    depart = Departament.objects(abbreviated=originalAbr, date_liquidation=None).first()
    if depart:
        ab = AbstractUnitLayer.objects(end_date=None, switch=0, for_vstup_kompany__ne=True, departament=depart).first()
    else:
        inst = Institute.objects(abbreviated=originalAbr, date_liquidation=None).first()
        if inst:
            ab = AbstractUnitLayer.objects(end_date=None, switch=1, for_vstup_kompany__ne=True,
                                           institute=inst).first()
    if ab:
        for gr in AcademicGroup.objects(is_archive=False, unit_layer=ab, is_virtual__in=virtual):
            subjects = {}
            if gr.prof_layer:
                if gr.prof_layer.subjects:
                    # max_semster = max(int(gr.prof_layer.subjects[kz]["semester"]) for kz in gr.prof_layer.subjects)
                    for key in gr.prof_layer.subjects:
                        part_of_key = key.split("@")[0]
                        subj = Subject.objects(id=part_of_key).first()
                        if subj.in_file and subj.uuid:
                            if gr.prof_layer.subjects[key]["period"] == period or period == "all":
                                model = gr.prof_layer.subjects[key].get('model') if gr.prof_layer.subjects[key].get('model') else "0"
                                subjects[u"{}_{}_{}".format(subj.uuid, model, gr.prof_layer.subjects[key]["semester"])] = gr.prof_layer.subjects[key]

            if subjects:
                for key in subjects.keys():
                    subjects[key].pop("is_diploma_mark")
            group_subjects[u"{}_{}".format(gr.abbreviated, gr.education_form)] = subjects

        answer[abr] = group_subjects
    result = {"subjects": answer}
    registration_actions_jiq(u'Перегляд семестровок груп підрозділу {}'.format(originalAbr))
    return jsonify(result)


# Функция для получения JSON со студентами факультета АКСА
@app.route('/get/students/<virtual>/<abr>', methods=["POST", "GET"])
def get_students_for_jiq(virtual, abr):
    if abr not in abreviatures:
        return Response(json.dumps({'status': 'fail', 'message': u'Структури не існує'}), status=400,
                        mimetype='application/json')
    originalAbr = getInistituteAbr(abr)
    if virtual == u"0":
        virtual = [False, None]
    else:
        virtual = [True]
    ab = None
    depart = Departament.objects(abbreviated=originalAbr, date_liquidation=None).first()
    if depart:
        ab = AbstractUnitLayer.objects(end_date=None, switch=0, for_vstup_kompany__ne=True, departament=depart).first()
    else:
        inst = Institute.objects(abbreviated=originalAbr, date_liquidation=None).first()
        if inst:
            ab = AbstractUnitLayer.objects(end_date=None, switch=1, for_vstup_kompany__ne=True,
                                           institute=inst).first()
    answer = {}
    groups = AcademicGroup.objects(is_archive=False, unit_layer=ab, is_virtual__in=virtual)
    for gr in groups:
        if gr.is_virtual == True:
            gr_key = unicode(gr.abbreviated) + u'_' + revertEducForm(gr.education_form) + u'_' + Subject.objects(id=gr.virtual_subject.id).first().uuid
        else:
            gr_key = gr.abbreviated + '_' + revertEducForm(gr.education_form)
        answer[gr_key] = {}
        if gr.uuid:
            answer[gr_key]["uuid_gr"] = gr.uuid
        if gr.specialisation:
            answer[gr_key]["specialisation"] = {}
            answer[gr_key]["specialisation"][
                "name"] = gr.specialisation.name
            if not gr.specialisation.uuid:
                gr.specialisation.uuid = str(uuid.uuid4())
                gr.specialisation.save()
            answer[gr_key]["specialisation"][
                "uuid"] = gr.specialisation.uuid
            if gr.specialisation.code:
                answer[gr_key]["specialisation"][
                    "code"] = gr.specialisation.code
        if gr.educational_program:
            try:
                answer[gr_key]["educational_program"] = {}
                answer[gr_key]["educational_program"][
                    "name"] = gr.educational_program.name
            except Exception:
                print gr
            if not gr.educational_program.uuid:
                gr.educational_program.uuid = str(uuid.uuid4())
                gr.educational_program.save()
            answer[gr_key]["educational_program"][
                "uuid"] = gr.educational_program.uuid
        if gr.training_dir:
            answer[gr_key]["training_dir"] = {}
            answer[gr_key]["training_dir"][
                "name"] = gr.training_dir.name
            if not gr.training_dir.uuid:
                gr.training_dir.uuid = str(uuid.uuid4())
                gr.training_dir.save()
            answer[gr_key]["training_dir"][
                "uuid"] = gr.training_dir.uuid
            if gr.training_dir.code:
                answer[gr_key]["training_dir"][
                    "code"] = gr.training_dir.code
            if gr.training_dir.start_date:
                answer[gr_key]["training_dir"][
                    "start_date"] = gr.training_dir.start_date
        for itr, st in enumerate(gr.list_students):
            answer[gr_key][itr] = {}
            if st.human:
                if st.human.name:
                    answer[gr_key][itr][
                        'name'] = st.human.name
                if st.human.surname:
                    answer[gr_key][itr][
                        'surname'] = st.human.surname
                if st.human.patronymic:
                    answer[gr_key][itr][
                        'patronymic'] = st.human.patronymic
            if st.record_book:
                answer[gr_key][itr][
                    'record_book'] = st.record_book
            if st.uuid:
                answer[gr_key][itr]['uuid'] = st.uuid

    registration_actions_jiq(u'Перегляд студентів {}'.format(originalAbr))
    return jsonify(answer)


# validator for shwwt from jiq
# @param data mast be lest
def jiq_sheet_validation(data):
    # check data as list
    if isinstance(data, list):
        return json.dumps({"status": "fail", "message": u"Відсутні дані"})

    # check number of sheet
    if not data.get('number'):
        return json.dumps({"status": "fail", "message": u"Відсутній номер відомості"})

    registration_actions_jiq(u'Валідація відомості: № {0}'.format(data.get('number')))

    # check course of sheet
    if not data.get("course"):
        return json.dumps({"status": "fail", "message": u"Відсутній курс"})

    # course must be int
    try:
        data["course"] = int(data["course"])
    except:
        return json.dumps({"status": "fail", "message": u"Не вірно вказаний курс"})

    # course not 1 to 10
    if data["course"] < 1 or data["course"] > 10:
        return json.dumps({"status": "fail", "message": u"Не вірно вказаний курс"})

    # check semester of sheet
    if not data.get("semester"):
        return json.dumps({"status": "fail", "message": u"Відсутній     семестр"})

    # semester must be int
    try:
        data["semester"] = int(data["semester"])
    except:
        return json.dumps({"status": "fail", "message": u"Не вірно вказаний семестр"})

    # semester not 1 to 50
    if data["semester"] < 1 or data["semester"] > 50:
        return json.dumps({"status": "fail", "message": u"Не вірно вказаний семестр"})

    if not data.get("uuid_gr"):
        return json.dumps({"status": "fail", "message": u"у групи відсутній uuid"})

    if not data.get("subj_uuid"):
        # subject
        if not data.get("subjectName"):
            return json.dumps({"status": "fail", "message": u"Відсутній предмет"})

        try:
            subject = Subject.objects(name=unicode(data["subjectName"])).first()

            if not subject:
                return json.dumps({"status": "fail", "message": u"Такого предмету не існує"})  # ----------------------
        except:
            return json.dumps({"status": "fail", "message": u"Предмет введено не вірно"})
    else:
        try:
            subject = Subject.objects(uuid=data["subj_uuid"]).first()

            if not subject:
                if not data.get("subjectName"):
                    return json.dumps({"status": "fail", "message": u"Відсутній предмет"})

                try:
                    subject = Subject.objects(name=unicode(data["subjectName"])).first()

                    if not subject:
                        return json.dumps(
                            {"status": "fail", "message": u"Такого предмету не існує"})  # ----------------------
                except:
                    return json.dumps({"status": "fail", "message": u"Предмет введено не вірно"})
        except:
            return json.dumps({"status": "fail", "message": u"uuid предмету введено не вірно"})
    print subject
    # check form education in choices
    # module/setting/choices.py
    # @EDUCATION_FORM
    if not data.get("formEducation"):
        return json.dumps({"status": "fail", "message": u"Відсутня форма навчання"})
    formEducation = educationForm(data["formEducation"])

    if formEducation == -1:
        return json.dumps({"status": "fail", "message": u"Форма навчання введено невірно"})

    # type of work checking
    # module/setting/choices.py
    # @TYPE_WORK_CHOICES
    if not data.get("testType"):
        return json.dumps({"status": "fail", "message": u"Відсутній тип роботи"})
    testTypeNumber = phv2(data["testType"])

    if testTypeNumber == -1:
        return json.dumps({"status": "fail", "message": u"Тип роботи введено невірно"})

    # check credit
    if not data.get("credit"):
        return json.dumps({"status": "fail", "message": u"Відсутні кредити"})

    # credit must by float
    try:
        data["credit"] = float(data["credit"])
    except:
        return json.dumps({"status": "fail", "message": u"Не вірно вказані кредити"})

    # check qualification
    if not data.get("qualification"):
        return json.dumps({"status": "fail", "message": u"Відсутня кваліфікація"})

    # check qualification in DB
    try:
        if not QualificationLevel.objects(name__iexact=unicode(data["qualification"])).first():
            return json.dumps({"status": "fail", "message": u"Не знайдено кваліфікацію"})  # --------------
    except:
        return json.dumps({"status": "fail", "message": u"Кваліфікація введена невірно"})  # --------------

    # check teacher
    if not data.get("teacher"):
        return json.dumps({"status": "fail", "message": u"Відсутні дані про викладача"})

    # check teacher as FIO
    if not (data["teacher"].get('name') and data["teacher"].get('surname') and data["teacher"].get('patronymic')):
        return json.dumps({"status": "fail", "message": u"Відсутні ПІБ дані викладача"})

    # check teacher in DB
    try:
        if not advansed_search(unicode(data["teacher"]["surname"]),
                               unicode(data["teacher"]["name"]),
                               unicode(data["teacher"]["patronymic"])):
            return json.dumps({"status": "fail", "message": u"Такого викладача не існує"})  # ----------------
    except:
        return json.dumps({"status": "fail", "message": u"Викладача введено невірно"})  # ----------------

    # check degree teacher
    if not data["teacher"].get("degree"):
        return json.dumps({"status": "fail", "message": u"Відсутні дані про посаду викладача"})

    # check assistant
    if not data.get("assistant"):
        return json.dumps({"status": "fail", "message": u"Відсутні дані про асистента"})

    # check assistant as FIO
    if not (data["assistant"].get('name') and data["assistant"].get('surname') and data["assistant"].get('patronymic')):
        return json.dumps({"status": "fail", "message": u"Відсутні ПІБ дані асистента"})

    # check assistant in DB
    # maybe In DB assistant has problem FIO
    try:
        if not advansed_search(unicode(data["assistant"]["surname"]),
                               unicode(data["assistant"]["name"]),
                               unicode(data["assistant"]["patronymic"])):
            return json.dumps({"status": "fail", "message": u"Такого асистента не існує"})
    except:
        return json.dumps({"status": "fail", "message": u"Відсутній асистент"})

    # check degree teacher
    if not data["assistant"].get("degree"):
        return json.dumps({"status": "fail", "message": u"Відсутні дані про посаду контролюючого викладача"})

    # date проверка на ввода даты в обе сторону (год - месяц - день и наоборот)
    if not data.get("date"):
        return json.dumps({"status": "fail", "message": u"Відсутні дані про дату"})
    try:
        date = strptime(data["date"], '%Y-%m-%d')
    except:
        try:
            date = strptime(data["date"], '%d-%m-%Y')
        except:
            return json.dumps({"status": "fail", "message": u"Дата введено невірно"})

    if date.tm_year > datetime.datetime.now().year + 1 or date.tm_year < datetime.datetime.now().year - 1:
        return json.dumps({"status": "fail", "message": u"Рік введено невірно"})

    # check students data
    if not (data.get("students") and isinstance(data["students"], list)):
        return json.dumps({"status": "fail", "message": u"Відсутні Студенти"})

    student_list = []
    errors = []

    for _student in data["students"]:

        if not _student.get("uuid"):
            errors.append(u"Невідомий студент")
            return json.dumps({"status": "fail", "message": errors})

        # check human
        else:
            st = None
            try:
                st = Student.objects(uuid=_student['uuid'],
                                     # record_book=_student["bookRegistration"],
                                     is_expelled=False,
                                     in_academic=False,
                                     is_delete=False).first()
            except:
                if _student["human"].get('name') and _student["human"].get('surname') and "patronymic" in _student[
                    "human"]:
                    errors.append(u"Відсутній студент {0} {1} {2}".format(_student["human"].get('surname'),
                                                                          _student["human"].get('name'),
                                                                          _student["human"].get('patronymic')))
                else:
                    errors.append(u"Відсутній студент з таким uuid: " + _student["uuid"])
                return json.dumps({"status": "fail", "message": errors})

            if not st:
                if _student["human"].get('name') and _student["human"].get('surname') and "patronymic" in _student[
                    "human"]:
                    errors.append(u"Відсутній студент {0} {1} {2}".format(_student["human"].get('surname'),
                                                                          _student["human"].get('name'),
                                                                          _student["human"].get('patronymic')))
                else:
                    errors.append(u"Відсутній студент з таким uuid: " + _student["uuid"])
                return json.dumps({"status": "fail", "message": errors})
            else:

                if not _student.get("mark") and (_student.get("overcharging") or _student.get("pass")):
                    pass
                else:
                    # check mark
                    if not _student.get("mark"):
                        errors.append(
                            u"У студента відсутня оцінка: " + st.human.surname + ' ' + st.human.name + ' ' + st.human.patronymic)

                    # check scope
                    if not _student["mark"].get("scope") and testTypeNumber == 2:
                        pass
                    else:
                        # check scope if testType not 'Залік'
                        if not _student["mark"].get("scope"):
                            errors.append(
                                u"У студента відсутня оцінка за 100 шкалою: " + ' ' + st.human.surname + ' ' + st.human.name + ' ' + st.human.patronymic)

                    # check mark as ECTS
                    if not _student["mark"].get("ects"):
                        errors.append(
                            u"У студента відсутня оцінка за ECTS шкалою: " + ' ' + st.human.surname + ' ' + st.human.name + ' ' + st.human.patronymic)

                    # type of ECTS checking
                    # module/setting/choices.py
                    # @ECTS_CHOICES
                    if ects2(_student["mark"].get("ects")) == -1:
                        errors.append(
                            u"У студента помилка за ECTS шкалою: " + ' ' + st.human.surname + ' ' + st.human.name + ' ' + st.human.patronymic)

                student_list.append(st)

    # якщо є студенти у списку
    if student_list:
        group = None
        #  дістаєм групи по знайденим студентам і курсу
        try:
            group = AcademicGroup.objects.get(uuid=data.get("uuid_gr"))
        except:
            errors.append(u"Не знайдено жодної групи")
        if group and not len(group.list_students) == len(student_list):
            errors.append(u"Кількість студентів у групі не співпадає з наданими")
            group = None
        elif group:
            subjects = []
            try:
                for key in group.prof_layer.subjects:
                    part_of_key = key.split("@")[0]
                    if unicode(part_of_key) == unicode(subject.id):
                        subjects.append(group.prof_layer.subjects[key])
                if not subjects:
                    errors.append(u'Дисципліна "{0}"відсутня у групі'.format(subject))
                else:

                    passed = False
                    errors_subject = []
                    for s in subjects:
                        if unicode(s['model']) == unicode(testTypeNumber):
                            passed = True
                            if unicode(s['semester']) == unicode(data["semester"]):
                                if unicode(s['credit']) == unicode(data["credit"]):
                                    errors_subject = []
                                    break
                                    pass
                                else:
                                    errors_subject.append(
                                        u"У дисципліни {0} не правильно введені кредити".format(subject))
                            else:
                                errors_subject.append(
                                    u"У групи відсутня дисципліна {0} в {1} семестрі".format(subject,
                                                                                             data["semester"]))
                    if not passed:
                        errors.append(
                            u"Для дисципліни {0} не правильно введений тип роботи".format(subject))
                    errors = errors + errors_subject
            except Exception:
                errors.append(u'Дисципліна "{0}"відсутня у групі'.format(subject))
    else:
        errors.append(u"Наданих студентів не знайдено")
    if errors:
        return json.dumps({"status": "fail", "message": errors})

    return json.dumps({"status": "success", "message": u"Перевірено"})


def jiq_slider_validation(data):
    # not has data as list
    if isinstance(data, list):
        return json.dumps({"status": "fail", "message": u"Відсутні дані"})  # -----------------------

    # not has number of slider
    if not data.get('number'):
        return json.dumps({"status": "fail", "message": u"Відсутній номер аркуша успішності"})

    registration_actions_jiq(u'Валідація аркуша успішності: № {0}'.format(data.get('number')))

    # not has semester of sheet
    if not data.get("semester"):
        return json.dumps({"status": "fail", "message": u"Відсутній семестр"})

    # semester must be int
    try:
        data["semester"] = int(data["semester"])
    except:
        return json.dumps({"status": "fail", "message": u"Не вірно вказаний семестр"})

    # semester not 1 to 50
    if data["semester"] < 1 or data["semester"] > 50:
        return json.dumps({"status": "fail", "message": u"Не вірно вказаний семестр"})
    if not data.get("subj_uuid"):
        # subject
        if not data.get("subjectName"):
            return json.dumps({"status": "fail", "message": u"Відсутній предмет"})

        try:
            subject = Subject.objects(name=unicode(data["subjectName"])).first()

            if not subject:
                return json.dumps({"status": "fail", "message": u"Такого предмету не існує"})  # ----------------------
        except:
            return json.dumps({"status": "fail", "message": u"Предмет введено не вірно"})
    else:
        try:
            subject = Subject.objects(uuid=data["subj_uuid"]).first()

            if not subject:
                if not data.get("subjectName"):
                    return json.dumps({"status": "fail", "message": u"Відсутній предмет"})

                try:
                    subject = Subject.objects(name=unicode(data["subjectName"])).first()

                    if not subject:
                        return json.dumps(
                            {"status": "fail", "message": u"Такого предмету не існує"})  # ----------------------
                except:
                    return json.dumps({"status": "fail", "message": u"Предмет введено не вірно"})
        except:
            return json.dumps({"status": "fail", "message": u"uuid предмету введено не вірно"})

    # Type of work with checking by phv2
    if not data.get("testType"):
        return json.dumps({"status": "fail", "message": u"Відсутній тип роботи"})
    testTypeNumber = phv2(data["testType"])

    if testTypeNumber == -1:
        return json.dumps({"status": "fail", "message": u"Тип роботи введено невірно"})  # ------------------

    # not has credit
    if not data.get("credit"):
        return json.dumps({"status": "fail", "message": u"Відсутні кредити"})

    try:
        float(data["credit"])
    except:
        return json.dumps({"status": "fail", "message": u"Не вірно вказані кредити"})

    # not has qualification
    if not data.get("qualification"):
        return json.dumps({"status": "fail", "message": u"Відсутня кваліфікація"})

    # check has qualification in DB
    try:
        if not QualificationLevel.objects(name__iexact=unicode(data["qualification"])).first():
            return json.dumps({"status": "fail", "message": u"Не знайдено кваліфікацію"})  # --------------
    except:
        return json.dumps({"status": "fail", "message": u"Кваліфікація введена невірно"})  # --------------

    # date(from) проверка на ввода даты в обе сторону (год - месяц - день и наоборот)
    if not data.get("date-from"):
        return json.dumps({"status": "fail", "message": u"Дійсний від: Відсутні дані про дату "})
    try:
        date_from = strptime(data["date-from"], '%Y-%m-%d')
    except:
        try:
            date_from = strptime(data["date-from"], '%d-%m-%Y')
        except:
            return json.dumps({"status": "fail", "message": u"Дійсний від: Дата введено невірно"})

    if date_from.tm_year > datetime.datetime.now().year + 1 or date_from.tm_year < datetime.datetime.now().year - 1:
        return json.dumps({"status": "fail", "message": u"Дійсний від: Рік введено невірно"})

    # date(to) проверка на ввода даты в обе сторону (год - месяц - день и наоборот)
    if not data.get("date-to"):
        return json.dumps({"status": "fail", "message": u"Дійсний по: Відсутні дані про дату"})
    try:
        date_to = strptime(data["date-to"], '%Y-%m-%d')
    except:
        try:
            date_to = strptime(data["date-to"], '%d-%m-%Y')
        except:
            return json.dumps({"status": "fail", "message": u"Дійсний по: Дата введено невірно"})

    if date_to.tm_year > datetime.datetime.now().year + 1 or date_to.tm_year < datetime.datetime.now().year - 1:
        return json.dumps({"status": "fail", "message": u"Дійсний по: Рік введено невірно"})

    # check students data
    if not (data.get("student")):
        return json.dumps({"status": "fail", "message": u"Відсутній студент в аркуші"})

    errors = []

    try:
        student = Student.objects(uuid=data['student']['uuid']).first()
        print student
        student = Student.objects(uuid=data['student']['uuid'], is_debtor=True).first()
        if not student:
            return json.dumps({"status": "fail", "message": u"Студент не є боржником"})
    except:
        return json.dumps({"status": "fail", "message": u"Відсутній студент"})

    #
    if not data['student'].get("mark"):
        errors.append(u"У студента відсутня оцінка: " + student.human.surname + u" " +
                      student.human.name + u" " + student.human.patronymic)

    #
    if not data['student']["mark"].get("scope") and testTypeNumber == 2:
        pass
    else:
        if not data['student']["mark"].get("scope"):
            errors.append(
                u"У студента відсутня оцінка за 100 шкалою: " + student.human.surname + u" " +
                student.human.name + u" " + student.human.patronymic)

    #
    if not data['student']["mark"].get("ects"):
        errors.append(
            u"У студента відсутня оцінка за ECTS шкалою: " + student.human.surname + u" " +
            student.human.name + u" " + student.human.patronymic)

    #
    if ects2(data['student']["mark"].get("ects")) == -1:
        errors.append(
            u"У студента помилка за ECTS шкалою: " + student.human.surname + u" " +
            student.human.name + u" " + student.human.patronymic)

    try:
        # заміняємо точку на слеш у кредитах (для пошуку предмету по семестру)
        credit = unicode(data["credit"])
        if '.' in credit:
            credit = credit.replace('.', '/')
        # формуємо ключ
        if testTypeNumber == 3 or testTypeNumber == 5:
            key = u'{0}@{1}@{2}@{3}'.format(subject.id, data["semester"], testTypeNumber, credit)

        else:
            key = u'{0}@{1}@{2}'.format(subject.id, data["semester"], credit)
        # дістаєм предмет по ключу і звіряємо тип роботи у них, якщо все зівпало - йдемо далі,

    except Exception:
        errors.append(u'Дисципліна "{0}"відсутня у групі'.format(subject))

    if errors:
        return json.dumps({"status": "fail", "message": errors})

    return json.dumps({"status": "success", "message": u"Аркуш успішності Перевірено"})


# Create sheet from jiq
# @param req must be lest
def jiq_sheet_create(req):
    from modules.estimates.update_mark_info import update_group_destiny, update_add_scores_semester
    # get all value from JSON
    prepare_number_sheet = req['data']['number']
    prepare_semester = int(req['data']['semester'])
    prepare_course = int(req['data']['course'])
    uuid = req['data']['uuid_gr']

    # parse date of sheet
    try:
        prepare_date = datetime.datetime.fromtimestamp(mktime(strptime(req['data']['date'], '%Y-%m-%d')))
    except:
        prepare_date = datetime.datetime.fromtimestamp(mktime(strptime(req['data']['date'], '%d-%m-%Y')))
    prepare_subject = Subject.objects(uuid=req["data"]["subj_uuid"]).first()
    if not prepare_subject:
        prepare_subject = Subject.objects(name=unicode(req["data"]["subjectName"])).first()
    prepare_number = phv2(req['data']['testType'])
    prepare_qualification = QualificationLevel.objects(name__iexact=unicode(req['data']['qualification'])).first()

    if prepare_qualification.name.startswith(u"Бакалавр"):
        prepare_mark_type = 2
    else:
        prepare_mark_type = 3

    # get teacher
    prepare_teacher = advansed_search(unicode(req["data"]["teacher"]["surname"]),
                                      unicode(req["data"]["teacher"]["name"]),
                                      unicode(req["data"]["teacher"]["patronymic"]))

    # get assistant
    prepare_assistant = advansed_search(unicode(req["data"]["assistant"]["surname"]),
                                        unicode(req["data"]["assistant"]["name"]),
                                        unicode(req["data"]["assistant"]["patronymic"]))

    prepare_credit = float(req["data"]["credit"])

    prepare_group = AcademicGroup.objects.get(uuid=uuid)

    prepare_sheet = Sheet.objects(group=prepare_group,
                                  teacher_mark=prepare_teacher,
                                  teacher_control=prepare_assistant,
                                  date=prepare_date,
                                  number=prepare_number_sheet,
                                  course=prepare_course,
                                  semester=prepare_semester,
                                  subject=prepare_subject,
                                  type=prepare_mark_type,
                                  model=prepare_number,
                                  credit=prepare_credit).first()

    if prepare_sheet:
        return json.dumps({"status": "fail", "message": u"Така відомість була збережена раніше"})

    prepare_sheet = Sheet(group=prepare_group,
                          teacher_mark=prepare_teacher,
                          teacher_control=prepare_assistant,
                          date=prepare_date,
                          number=prepare_number_sheet,
                          course=prepare_course,
                          semester=prepare_semester,
                          subject=prepare_subject,
                          type=prepare_mark_type,
                          model=prepare_number,
                          credit=prepare_credit).save()

    registration_actions_jiq(u'Створення: відомість № {0}'.format(prepare_number_sheet))

    # get every student
    for student in req['data']['students']:
        # prepare_marks.append(i["mark"]["scope"])

        temp_student = Student.objects(uuid=student['uuid'],
                                       # record_book=student["bookRegistration"],
                                       is_expelled=False,
                                       in_academic=False,
                                       is_delete=False).first()

        if not student.get("mark") and (student.get("overcharging") or student.get("pass")):
            pass
        else:
            # make every mark in student
            z_mark = Mark(student=temp_student,
                          type=prepare_mark_type,
                          subject=prepare_subject,
                          credit=prepare_credit,
                          model=prepare_number,
                          semester=prepare_semester,
                          source=prepare_sheet)

            if student["mark"]["ects"] == 'nz':
                z_mark.scores = 0
            else:
                z_mark.scores = student['mark']["scope"]

            z_mark.rating = ects2(student["mark"]["ects"])

            z_mark.save()
            prepare_sheet.marks.append(z_mark)
    prepare_sheet.all_done = True
    prepare_sheet.save()
    update_add_scores_semester.delay(str(prepare_sheet.id))
    update_group_destiny.delay(str(prepare_sheet.id), None)
    registration_actions_jiq(u'Редагування оцінок: відомість № {0}'.format(prepare_number_sheet))
    # status 200 all done

    return json.dumps({"status": "success", "message": u"Відомість вдало збережена"})


def jiq_slider_create(req):
    # get all value from JSON
    prepare_number_slider = req['number']
    prepare_semester = req['semester']

    # parse date of slider
    try:
        prepare_date_from = datetime.datetime.fromtimestamp(mktime(strptime(req['date-from'], '%Y-%m-%d')))
    except:
        prepare_date_from = datetime.datetime.fromtimestamp(mktime(strptime(req['date-from'], '%d-%m-%Y')))

    try:
        prepare_date_to = datetime.datetime.fromtimestamp(mktime(strptime(req['date-to'], '%Y-%m-%d')))
    except:
        prepare_date_to = datetime.datetime.fromtimestamp(mktime(strptime(req['date-to'], '%d-%m-%Y')))

    prepare_subject = Subject.objects(uuid=req["subj_uuid"]).first()
    if not prepare_subject:
        prepare_subject = Subject.objects(name=unicode(req["subjectName"])).first()
    prepare_number = phv2(req['testType'])
    prepare_qualification = QualificationLevel.objects(name__iexact=unicode(req['qualification'])).first()

    if prepare_qualification.name.startswith(u"Бакалавр"):
        prepare_mark_type = 2
    else:
        prepare_mark_type = 3

    prepare_credit = req["credit"]
    prepare_student = Student.objects(uuid=req["student"]["uuid"]).first()

    # prepare_slider = Slider.objects(number=prepare_number_slider,
    #                                 student=prepare_student,
    #                                 subject=prepare_subject,
    #                                 start_date=prepare_date_from,
    #                                 end_date=prepare_date_to,
    #                                 semester=prepare_semester,
    #                                 type=prepare_mark_type,
    #                                 model=prepare_number,
    #                                 credit=prepare_credit).first()
    #
    # if prepare_slider:
    #     return json.dumps({"status": "fail", "message": u"Такий аркуш успішності був збережений раніше"})

    prepare_slider = Slider(number=prepare_number_slider,
                            student=prepare_student,
                            subject=prepare_subject,
                            start_date=prepare_date_from,
                            end_date=prepare_date_to,
                            semester=prepare_semester,
                            type=prepare_mark_type,
                            model=prepare_number,
                            credit=prepare_credit).save()
    registration_actions_jiq(u'Створення: аркуш успішності студента № {0}'.format(prepare_number_slider))
    # make mark in student
    temp_student = Student.objects(uuid=req["student"]["uuid"]).first()

    z_mark = Mark(student=temp_student,
                  type=prepare_mark_type,
                  subject=prepare_subject,
                  credit=prepare_credit,
                  model=prepare_number,
                  semester=prepare_semester,
                  source=prepare_slider,
                  scores=req["student"]["mark"]["scope"])
    z_mark.rating = z_mark.get_rating(z_mark.scores, z_mark.model)
    z_mark.save()
    prepare_slider.mark = z_mark

    prepare_slider.save()

    registration_actions_jiq(u'Редагування оцінок: аркуш успішності студента № {0}'.format(prepare_number_slider))
    return json.dumps({"status": "success", "message": u"Аркуш успішності вдало збережений"})


def advansed_search(search_surname, search_name, search_patron):
    search_surname = re.sub("`", "'", search_surname)
    search_surname = re.sub("ʼ", "'", search_surname)

    search_name = re.sub("`", "'", search_name)
    search_name = re.sub("ʼ", "'", search_name)

    search_patron = re.sub("`", "'", search_patron)
    search_patron = re.sub("ʼ", "'", search_patron)

    short_name = search_name[0] + '.'
    short_patron = search_patron[0] + '.'

    teacher = Teacher.objects(name=unicode(search_surname + " " + search_name + " " + search_patron)).first()

    if teacher:
        return teacher

    teacher = Teacher.objects(name=unicode(search_surname + " " + short_name + short_patron)).first()
    if teacher:
        return teacher

    search_surname = re.sub("'", "`", search_surname)
    search_surname = re.sub("ʼ", "`", search_surname)

    search_name = re.sub("'", "`", search_name)
    search_name = re.sub("ʼ", "`", search_name)

    search_patron = re.sub("'", "`", search_patron)
    search_patron = re.sub("ʼ", "`", search_patron)

    teacher = Teacher.objects(name=unicode(search_surname + " " + search_name + " " + search_patron)).first()

    if teacher:
        return teacher

    teacher = Teacher.objects(name=unicode(search_surname + " " + short_name + short_patron)).first()
    if teacher:
        return teacher

    search_surname = re.sub("'", "ʼ", search_surname)
    search_surname = re.sub("`", "ʼ", search_surname)

    search_name = re.sub("'", "ʼ", search_name)
    search_name = re.sub("`", "ʼ", search_name)

    search_patron = re.sub("'", "ʼ", search_patron)
    search_patron = re.sub("`", "ʼ", search_patron)

    teacher = Teacher.objects(name=unicode(search_surname + " " + search_name + " " + search_patron)).first()

    if teacher:
        return teacher

    teacher = Teacher.objects(name=unicode(search_surname + " " + short_name + short_patron)).first()
    if teacher:
        return teacher

    return None


@app.route('/test', methods=['POST'])
def test():
    return jiq_slider_validation(request.json['data'])


def phv2(found_choice):
    for choice in TYPE_WORK_CHOICES:
        if choice[1] == found_choice:
            return choice[0]
    return -1


#
def ects2(found_choice):
    for choice in ECTS_CHOICES:
        if choice[1] == found_choice:
            return choice[0]
    return -1


#
def educationForm(found_choice):
    for choice in EDUCATION_FORM:
        if choice[1] == found_choice:
            return choice[0]
    return -1


def revertEducForm(found_choice):
    for choice in EDUCATION_FORM:
        if choice[0] == found_choice:
            return choice[1]
    return -1


#
def search_humans_by_full_name(name):
    return Human.objects(Q(full_name__contains=name['name']) & Q(full_name__contains=name['surname'])
                         & Q(full_name__contains=name['patronymic'])).first()


def getInistituteAbr(x):
    return abreviatures[x]


if __name__ == '__main__':
    host = os.environ.get('LOD_JIQ_HOST', '0.0.0.0')
    port = int(os.environ.get('LOD_JIQ_PORT', '5001'))
    app.run(host=host, debug=True, port=port)
