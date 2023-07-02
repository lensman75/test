# -*- coding: utf-8 -*-
import traceback
from time import sleep

import os

from collections import defaultdict
from flask import render_template, jsonify
from flask.ext.admin.base import MenuLink, Admin
from flask.ext.babelex import Babel
from flask.ext.celeryext import FlaskCeleryExt
from flask.ext.security import Security, MongoEngineUserDatastore
from mongoengine import connect, ValidationError, MultipleObjectsReturned, DoesNotExist
from mongoengine.base.common import get_document

from modules import app
from modules.address.models import AddressCombinations, District, Region, Settlement
from modules.address.updater import update_address
from modules.address.view import AddressView, DistrictView, RegionView, SettlementView
from modules.setting import CATEGORY_ADD_SCORES

ext = FlaskCeleryExt(app)

from modules.document import DocumentType, DocumentTypeView, Order, OrderView
from modules.human import Human
from modules.student import Student, AdditionalScores
from modules.unit.models import AcademicGroup
from modules.unit.views import AcademicGroupView, DepartamentView, InstituteView, UniversityView, PHView, \
    GroupMagAdditionView, GroupBacAdditionView, ArchiveAcademicGroupView, GraduateView, AlienCenterView
from modules.profession import Profession, QualificationLevel, ProffOptions, ProffOptionsView, ProfesionView, \
    QualificationLevelView, EducationalProgramMain, EducationalProgramMainView, Qualification, QualificationView, KnowledgeField, \
    KnowledgeFieldView, LevelOfQualification, LevelOfQualificationView, OfficialDurationOfProgramme, \
    OfficialDurationOfProgrammeView, AcquiredCompetences, AcquiredCompetencesView, AcademicRights, AcademicRightsView, \
    AccessRequirements, AccessRequirementsView
from modules.subject.view import SubjectView, TeacherView
from modules.subject.models import Subject, Teacher
from modules.views import *

from modules.estimates import Mark, Sheet, SliderView, Slider, SheetView, MarkView, Sabbatical, DiplomaSupplement, \
    SabbaticalView, DiplomaSupplementView, DiplomaProtection, DiplomaProtectionView
from modules.history import HistoryView, History
from modules.models import Basis
from modules.human import HumanView
from modules.student.view import StudentView, StudentDiplomaView, StudentHistoryView, GradebookView, DebtorView, \
    PrepareForExpelledStudentsView, LearningView, LearningHistoryView, PrepareForExpelledLearningView, \
    StudentAcademView, LearningAcademView, AdditionalScoresView

from modules.import_xls import ImportXLSView, AfterImportView, ExportDataForOrder

from modules.user.form import CustomLoginForm
from modules.user import Role, User, UserView

from modules.permissions.views import RoleView
from modules.tickets.views import TicketView
from modules.tickets.models import Ticket
from modules.forms import TableSizeForm
from modules.generate_mark_file.views import ImportStudentsXml, GenerateMarkFileView, ImportSubjectsView
from modules.type_qualification_works.view import TypesQualificationWorksView
from modules.type_qualification_works.model import TypesQualificationWorks
from modules.global_variables.models import MagazineVariables, Country, GlobalVariables, JuristicPeople, Universities
from modules.global_variables.view import MagazineVariablesView, CountryView, GlobalVariablesView, JuristicPeopleView, \
    UniversitiesView
from modules.estimates import RatingStipend
from modules.stipendium import AdditionalStipendiumView
from modules.stipendium import MainStipendiumView
from modules.document.view import RatingPDFView, AccountingView, AppendixToOrderOfGraduation
from modules.document import Accounting
from modules.generate_documents.accounting import get_accounting_file

user_datastore = MongoEngineUserDatastore(db, User, None)
security = Security(app, user_datastore, login_form=CustomLoginForm)
babel = Babel(app, default_locale='uk', )

celery = ext.celery
from modules.estimates.views import RatingStipendView, StipendOrderView, RatingFixerView

bed_marks = [u"Не з'явився", u'Недопущений', u'Незараховано']
try:
    import uwsgidecorators

    bed_marks = [u"Не з'явився", u'Недопущений', u'Незараховано']


    @app.errorhandler(Exception)
    def default_handler(e):
        print (traceback.format_exc())
        from config import LOG_PATH
        current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        try:
            user = unicode(current_user)
        except:
            user = 'undefined'

        try:
            referrer = request.referrer
            url = request.path
            get_params = unicode(dict(request.args))
            post_params = unicode(dict(request.form))
            files = unicode(request.files) if request.files else 'No files in query'
            ip = request.remote_addr
        except:
            referrer = 'undefined'
            url = 'undefined'
            get_params = 'undefined'
            post_params = 'undefined'
            files = 'undefined'
            ip = 'undefined'

        with open(os.path.join(LOG_PATH, current_time + '.txt'), 'w') as log:
            log.write(u'Time: {time}\n'.format(time=current_time))
            log.write(u'User: {login}\tIP: {ip}\n'.format(login=user, ip=ip))
            log.write(u'Referrer: {ref}\n'.format(ref=referrer))
            log.write(u'Page: {url}\n'.format(url=url))
            log.write(u'GET: {params}\n'.format(params=get_params))
            log.write(u'POST: {params}\n'.format(params=post_params))
            log.write(u'Files: {params}\n'.format(params=files))
            log.write(traceback.format_exc())
        return render_template('admin/exception_handler.html')


    @uwsgidecorators.cron(-5, -3, -1, -1, -1)
    def crutch_which_fixes_a_bug_elusive(arg):
        for group in AcademicGroup.objects():
            if group.list_students:
                l = set(group.list_students)
                if len(group.list_students) != len(l):
                    group.list_students = list(l)
                    group.save()

                    # @uwsgidecorators.cron(-5, -1, -1, -1, -1)
                    # def update_debtors_with_prof_layer(arg):
                    #     academ_students = Student.objects(Q(prof_layer__ne=None) | Q(individual_prof_layer__ne=None))
                    #     for student in academ_students:
                    #         academ_subjects = {}
                    #         individ_subjects = {}
                    #         if student.prof_layer.subjects:
                    #             academ_subjects = student.prof_layer.subjects
                    #         if student.individual_prof_layer.subjects:
                    #             individ_subjects = student.individual_prof_layer.subjectsz
                    #         subjects = dict(academ_subjects.items() + individ_subjects.items())
                    #         for subject in subjects:
                    #             s = subject.split('@')
                    #             subj = s[0]
                    #             semester = s[1]
                    #             mark = Mark.objects(student=student, subject=subj, credit=subjects[subject]['credit'],
                    #                                 semester=int(semester),
                    #                                 is_credit=subjects[subject]['is_credit'],
                    #                                 rating__in=[u"A", u'B', u'C', u'D', u'E', u'Зараховано'])
                    #             if len(mark) == 0:
                    #                 student.is_debtor = True
                    #             student.save()
                    #             if student.is_debtor:
                    #                 continue


    # every first day of month in 01:00 am
    @uwsgidecorators.cron(1, 0, 1, -1, -1)
    def gen_accounting_every_month(arg):
        model = Accounting()
        model.date = datetime.date.today()
        model.formed_by = u'Автоматично'
        model.formed_date = datetime.date.today()
        f = get_accounting_file()
        files = open(f.name, 'rb')
        model.file.new_file()
        model.file.replace(files)
        model.save()
except Exception, e:
    print (e)


@app.context_processor
def inject_global_template_context():
    try:
        messages = Ticket.objects(to=current_user.id, user_read_list__ne=str(current_user.id),
                                  user_delete_list__ne=current_user.id).count()
    except:
        messages = 0
    try:
        current_user.last_activity = datetime.datetime.now()
        current_user.save()
    except:
        pass
    size_form = TableSizeForm()
    if current_user.has_role('Admin') or current_user.has_role('Operator') or current_user.has_role('Moderator') \
            or current_user.has_role('cpo'):
        return dict(new_messages=messages, size_form=size_form, user=1, is_operator=current_user.has_role('Operator'))
    else:
        return dict(new_messages=messages, size_form=size_form, user=0, is_operator=current_user.has_role('Operator'))


admin = Admin(app, u'LoD', translations_path=os.path.dirname(__file__) + '/translations', static_url_path='/static',
              index_view=IndexView(url='/admin'), base_template='admin/base.html')
admin.add_link(MenuLink(u'Вийти', url='/logout'))

# студенти
admin.add_view(StudentView(Student, endpoint='student', name=u'Студенти, що навчаються',
                           category=u'Контингент студентів'))
admin.add_view(StudentAcademView(Student, endpoint='student_academ', name=u'Студенти в академ. відпустці',
                                 academ=True, category=u'Контингент студентів'))
admin.add_view(StudentHistoryView(Student, endpoint='history_student', name=u'Архів студентів',
                                  category=u'Контингент студентів'))
admin.add_view(PrepareForExpelledStudentsView(Student, endpoint='prepare_of_expelled', name=u'Студенти на відрахування',
                                              category=u'Контингент студентів'))

admin.add_view(LearningView(Student, endpoint='learning', name=u'Слухачі, що навчаються',
                            category=u'Контингент слухачів'))
admin.add_view(LearningAcademView(Student, endpoint='learning_academ', name=u'Слухачі в академ. відпустці',
                                  academ=True, category=u'Контингент слухачів'))
admin.add_view(LearningHistoryView(Student, endpoint='history_learning', name=u'Архів слухачів',
                                   category=u'Контингент слухачів'))
admin.add_view(PrepareForExpelledLearningView(Student, endpoint='prepare_of_expelled_learning',
                                              name=u'Слухачі на відрахування',
                                              category=u'Контингент слухачів'))

# групи

admin.add_view(AcademicGroupView(endpoint='group', name=u'Групи', category=u'Групи'))
admin.add_view(ArchiveAcademicGroupView(endpoint='archive_group', name=u'Архів груп', category=u'Групи'))

# успішність
admin.add_view(SabbaticalView(Sabbatical, endpoint='sabbatical', name=u'Академічні довідки', category=u'Успішність'))
admin.add_view(DiplomaSupplementView(DiplomaSupplement, endpoint='diploma_supplement', name=u'Додатки до диплому',
                                     category=u'Успішність'))
admin.add_view(SliderView(Slider, endpoint='slider', name=u'Аркуші успішності студента', category=u'Успішність'))
admin.add_view(SheetView(Sheet, endpoint='sheet', name=u'Відомості', category=u'Успішність'))
admin.add_view(DiplomaProtectionView(DiplomaProtection, endpoint='diploma_protection',
                                     name=u'Захист кваліфікаційних робіт', category=u'Успішність'))
admin.add_view(DebtorView(model=Student, endpoint='debtors', name=u'Боржники', category=u'Успішність'))
admin.add_view(RatingStipendView(RatingStipend, endpoint='rating_stipend', name=u'Рейтинг', category=u'Успішність'))
admin.add_view(RatingPDFView(endpoint='rating_pdf', name=u'Рейтинги в PDF',
                             category=u'Успішність'))

# Дипломи
# admin.add_view(StudentDiplomaView(Student, endpoint='diploma', name=u'Дипломи'))
# admin.add_view(GradebookView(Student, endpoint='gradebook', name=u'Студентські'))

# структурні підрозділи
admin.add_view(DepartamentView(endpoint='departament', name=u'Факультети', category=u'Структурні підрозділи'))
admin.add_view(InstituteView(endpoint='institute', name=u'Інститути', category=u'Структурні підрозділи'))
admin.add_view(
    GraduateView(endpoint='graduate', name=u'Центр післядипломної освіти', category=u'Структурні підрозділи'))
admin.add_view(
    AlienCenterView(endpoint='alien_center', name=u'Центр міжнародних зв’язків', category=u'Структурні підрозділи'))
admin.add_view(UniversityView(endpoint='university', name=u'Університет', category=u'Структурні підрозділи'))

# навчальний процес
admin.add_view(SubjectView(Subject, endpoint='subject', name=u'Дисципліни', category=u'Навчальний процес'))
admin.add_view(
    ProfesionView(Profession, endpoint='profession', name=u'Спеціальності', category=u'Навчальний процес'))
admin.add_view(
    EducationalProgramMainView(EducationalProgramMain, endpoint='educational_program', name=u'Спеціалізації', category=u'Навчальний процес'))
admin.add_view(QualificationLevelView(QualificationLevel, endpoint='qualification_level', name=u'Кваліфікаційні рівні',
                                      category=u'Навчальний процес'))
admin.add_view(
    QualificationView(Qualification, endpoint='qualification', name=u'Кваліфікації', category=u'Навчальний процес'))
admin.add_view(
    KnowledgeFieldView(KnowledgeField, endpoint='knowledge_field', name=u'Галузі знань', category=u'Навчальний процес'))
admin.add_view(
    LevelOfQualificationView(LevelOfQualification, endpoint='level_of_qualification', name=u'Рівень кваліфікації',
                             category=u'Навчальний процес'))
admin.add_view(OfficialDurationOfProgrammeView(OfficialDurationOfProgramme, endpoint='official_duration_of_programme',
                                               name=u'Тривалість навчання', category=u'Навчальний процес'))
admin.add_view(
    AcquiredCompetencesView(AcquiredCompetences, endpoint='acquired_competences', name=u'Набуті компетентності',
                            category=u'Навчальний процес'))
admin.add_view(AcademicRightsView(AcademicRights, endpoint='academic_rights', name=u'Академічні права',
                                  category=u'Навчальний процес'))
admin.add_view(AccessRequirementsView(AccessRequirements, endpoint='access_requirements', name=u'Вимоги до вступу',
                                      category=u'Навчальний процес'))
admin.add_view(TeacherView(Teacher, endpoint='teachers', name=u'Викладачі', category=u'Навчальний процес'))
admin.add_view(AppendixToOrderOfGraduation(endpoint='appendix', name=u'Додаток до наказу про закінчення навчання',
                                           category=u'Навчальний процес'))

# накази
admin.add_view(OrderView(Order, endpoint='orders', name=u'Накази'))
admin.add_view(StipendOrderView(u'Наказ (стипендії)', endpoint='stipend_order'))

# звітність по контингенту на факультет
admin.add_view(AccountingView(Accounting, endpoint='accounting', name=u'Звітність'))

# Service
admin.add_view(ImportXLSView(name=u'Імпорт XLS', endpoint='import', category=u'Сервіс'))
admin.add_view(AfterImportView(name=u'Післяімпортна обробка', endpoint='next_import', category=u'Сервіс'))
admin.add_view(GenerateMarkFileView(name=u'Експорт даних по оцінкам', endpoint='gen_mark_file', category=u'Сервіс'))
admin.add_view(ImportSubjectsView(name=u'Імпорт дисциплін', endpoint='import_subjects', category=u'Сервіс'))
admin.add_view(ImportStudentsXml(name=u'Імпорт даних з xml', endpoint='import_student_info', category=u'Сервіс'))
admin.add_view(ExportDataForOrder(name=u'Експорт даних для наказу', endpoint='export_order_data', category=u'Сервіс'))
# admin.add_view(MagazineWorkProfessionView(name=u'Журнал робітничої професії',
#                                           endpoint='magazine_work_profession', category=u'Сервіс'))

# Загальні дані
admin.add_view(DocumentTypeView(DocumentType, endpoint='doc_type', name=u'Типи документів', category=u'Загальні дані'))
admin.add_view(ReasonView(Reason, endpoint='reason', name=u'Причини відрахування', category=u'Загальні дані'))
admin.add_view(AcademReasonView(AcademReason, endpoint='academreason', name=u'Причини академ. відпустки',
                                category=u'Загальні дані'))
admin.add_view(BasisView(Basis, endpoint='basis', name=u'Підстави відрахування', category=u'Загальні дані'))
admin.add_view(AcademBasisView(AcademBasis, endpoint='academ_basis', name=u'Підстави академ. відпустки',
                               category=u'Загальні дані'))
admin.add_view(GlobalVariablesView(GlobalVariables, name=u'Глобальні дані', endpoint='global_variables',
                                   category=u'Загальні дані'))
admin.add_view(CountryView(Country, name=u'Країни', endpoint='countries', category=u'Загальні дані'))
admin.add_view(TypesQualificationWorksView(model=TypesQualificationWorks, name=u'Типи кваліфікаційних робіт',
                                           endpoint='qualification_works', category=u'Загальні дані'))
admin.add_view(AdditionalScoresView(AdditionalScores, name=u'Додаткові бали', endpoint='additional_scores',
                                    category=u'Загальні дані'))
admin.add_view(
    JuristicPeopleView(JuristicPeople, name=u'Юридичний відділ', endpoint='juristic', category=u'Загальні дані'))
admin.add_view(
    UniversitiesView(Universities, name=u'Вищі навчальні заклади', endpoint='universities', category=u'Загальні дані'))
admin.add_view(AddressView(model=AddressCombinations, endpoint='postal', name=u'Поштові коди', category=u'Загальні дані'))
admin.add_view(DistrictView(model=District, endpoint='district', name=u'Області', category=u'Загальні дані'))
admin.add_view(RegionView(model=Region, endpoint='region', name=u'Райони', category=u'Загальні дані'))
admin.add_view(SettlementView(model=Settlement, endpoint='settlement', name=u'Нас. пункти', category=u'Загальні дані'))

# Адміністрування
admin.add_view(HumanView(Human, endpoint='human', name=u'Особові картки студентів', category=u'Адміністрування'))
admin.add_view(NewsView(model=News, name=u'Новини', endpoint='news', category=u'Адміністрування'))
admin.add_view(UserView(User, name=u'Користувачі', endpoint='user', category=u'Адміністрування'))
admin.add_view(HistoryView(History, name=u'Історія', endpoint='history', category=u'Адміністрування'))
admin.add_view(PHView(name=u'П.Х.', endpoint='abstract', category=u'Адміністрування'))
admin.add_view(MagazineVariablesView(MagazineVariables, name=u'Дані на журнал', endpoint='magazine_variables',
                                     category=u'Адміністрування'))
admin.add_view(RoleView(model=Role, endpoint='role', name=u'Ролі', category=u'Адміністрування', views=admin._views))
admin.add_view(ErrorView(u'Логи помилок', category=u'Адміністрування'))
admin.add_view(ProffOptionsView(ProffOptions, endpoint='p_option', name=u'Проф. опції', category=u'Адміністрування'))
admin.add_view(GroupBacAdditionView(endpoint='gb_option', name=u'Академ. Груп.Бак. опції', category=u'Адміністрування'))
admin.add_view(GroupMagAdditionView(endpoint='gm_option', name=u'Академ. Груп.Маг.опції', category=u'Адміністрування'))
admin.add_view(RatingFixerView(endpoint='rating_fixer', name=u'Виправлення рейтингу', category=u'Адміністрування'))


# стипендія
admin.add_view(MainStipendiumView(endpoint='main_stipendium', name=u'Осн. стипендія', category=u'Стипендії'))
admin.add_view(
    AdditionalStipendiumView(endpoint='additional_stipendium', name=u'Дод. стипендія', category=u'Стипендії'))

admin.add_view(TicketView(name=u'Пошта', endpoint='ticket'))

admin.add_view(MarkView(Mark, endpoint='mark'))

app.jinja_env.globals['isinstance'] = isinstance
app.jinja_env.globals['enumerate'] = enumerate
app.jinja_env.globals['unicode'] = unicode
app.jinja_env.globals['len'] = len
app.jinja_env.globals['reversed'] = reversed
app.jinja_env.globals['datetime'] = datetime
app.jinja_env.globals['Sheet'] = Sheet
app.jinja_env.globals['Slider'] = Slider
app.jinja_env.globals['Sabbatical'] = Sabbatical


@app.route('/rep', methods=['GET'])
def rep():
    my_row = request.args.get('q')
    if my_row == '':
        return 'eror'
    print my_row
    txt = {'key1': ('city1', 'city2'),
           'key2': ['wave1', 'wave2'],
           'musor': ('game', 'over')}

    return jsonify(txt)


@app.route('/init_rating_date')
def init_rating_date():
    if not current_user.has_role('Admin'):
        return 'not allowed'

    courses = Student.objects.distinct('course')
    print courses
    not_expelled = Student.objects(is_expelled=False)

    for course in courses:
        print course
        filtered = not_expelled.filter(course=course)
        RatingStipend.objects(student__in=filtered, course=course).update(set__date=datetime.datetime(2017, 12, 12))
        RatingStipend.objects(student__in=filtered, course__lt=course).update(set__date=datetime.datetime(2016, 12, 12))

    RatingStipend.objects(student__in=Student.objects(is_expelled=True)).update(set__date=datetime.datetime(2016, 12, 12))
    return 'good'


@app.route('/fix_rating_for_course/<int:course>')
def fix_rating(course):
    if not current_user.has_role('Admin'):
        return 'not allowed'

    d = defaultdict(set)
    for st in Student.objects(is_expelled=False, in_academic=False, course=course):
        rat = RatingStipend.objects(student=st).order_by('-semester').first()
        if not rat:
            continue
        semester = rat.semester
        # print '\n\n{} -- {}:'.format(st, st.group)

        scores_credit = 0
        credits = 0
        for mark in Mark.objects(student=st, semester=semester, for_rating=True):
            scores_credit += mark.scores * mark.credit
            credits += mark.credit

        # print 'scores_credit : {}'.format(scores_credit)
        # print 'credits : {}'.format(credits)

        if not scores_credit or not credits:
            print '\n\n{} -- {}\nscores_credit: {}'.format(st, st.group, scores_credit)
            continue

        marks_rating = scores_credit / credits
        # print 'marks_rating : {}'.format(marks_rating)

        add_scores = st.get_add_score(semester=semester)
        sport = add_scores.get(CATEGORY_ADD_SCORES[0][0], 0)
        science = add_scores.get(CATEGORY_ADD_SCORES[1][0], 0)
        social = add_scores.get(CATEGORY_ADD_SCORES[2][0], 0)

        additional_rating = (sport + science + social) * 0.1
        if additional_rating > 10:
            additional_rating = 10

        # print 'additional_rating : {}'.format(additional_rating)

        rating = marks_rating * 0.9 + additional_rating
        if rating > 100:
            rating = 100
        # print 'rating : {}'.format(rating)

        rating_stipend = RatingStipend.objects(student=st, semester=semester).first()
        # print rating_stipend

        if rating != rating_stipend.rating:
            # print '\n\n{} -- {}:'.format(st, st.group)
            # print 'scores_credit : {}'.format(scores_credit)
            # print 'credits : {}'.format(credits)
            # print 'marks_rating : {}'.format(marks_rating)
            # print 'additional_rating : {}'.format(additional_rating)
            # print 'rating : {}'.format(rating)
            # print rating_stipend
            d[st.group.id].add(semester)
    print d, '\n\n'

    from modules.estimates.update_mark_info import update_destiny_by_document
    for group_id in d:
        for semester in d[group_id]:
            print '\n\ngroup: {}, semester: {}'.format(AcademicGroup.objects(id=group_id).first(), semester)
            students = Student.objects(group=group_id, is_expelled=False).distinct('id')
            ratings = RatingStipend.objects(student__in=students, semester=semester)
            print ratings
            ratings.delete()
            print 'ratings deleted'

            Mark.objects(source__in=Sheet.objects(group=group_id, semester=semester, all_done=True))\
                .update(set__for_rating=False, set__old_scores=0)
            Mark.objects(source__in=Slider.objects(semester=semester, all_done=True, student__in=students))\
                .update(set__for_rating=False, set__old_scores=0)
            print 'marks done'

            for sheet in Sheet.objects(group=group_id, semester=semester, all_done=True):
                update_destiny_by_document(sheet)
            print 'sheets done'

            for slider in Slider.objects(semester=semester, all_done=True,
                                         student__in=students):
                update_destiny_by_document(slider)
            print 'sliders done'
    return unicode(d)


@app.route('/check_rating_for_course/<int:course>')
def check_rating(course):
    if not current_user.has_role('Admin'):
        return 'not allowed'

    if not course:
        return 'no data'

    for st in Student.objects(is_expelled=False, in_academic=False, course=course):
        rat = RatingStipend.objects(student=st).order_by('-semester').first()
        if not rat:
            continue
        semester = rat.semester
        # print '\n\n{} -- {}:'.format(st, st.group)

        scores_credit = 0
        credits = 0
        for mark in Mark.objects(student=st, semester=semester, for_rating=True):
            scores_credit += mark.scores * mark.credit
            credits += mark.credit

        # print 'scores_credit : {}'.format(scores_credit)
        # print 'credits : {}'.format(credits)

        if not scores_credit or not credits:
            print '\n\n{} -- {}\nscores_credit: {}'.format(st, st.group, scores_credit)
            continue

        marks_rating = scores_credit / credits
        # print 'marks_rating : {}'.format(marks_rating)

        add_scores = st.get_add_score(semester=semester)
        sport = add_scores.get(CATEGORY_ADD_SCORES[0][0], 0)
        science = add_scores.get(CATEGORY_ADD_SCORES[1][0], 0)
        social = add_scores.get(CATEGORY_ADD_SCORES[2][0], 0)

        additional_rating = (sport + science + social) * 0.1
        if additional_rating > 10:
            additional_rating = 10

        # print 'additional_rating : {}'.format(additional_rating)

        rating = marks_rating * 0.9 + additional_rating
        if rating > 100:
            rating = 100
        # print 'rating : {}'.format(rating)

        rating_stipend = RatingStipend.objects(student=st, semester=semester).first()
        # print rating_stipend

        if rating != rating_stipend.rating:
            print '\n\n{} -- {}:'.format(st, st.group)
            print 'scores_credit : {}'.format(scores_credit)
            print 'credits : {}'.format(credits)
            print 'marks_rating : {}'.format(marks_rating)
            print 'additional_rating : {}'.format(additional_rating)
            print 'rating : {}'.format(rating)
            print rating_stipend
    return 'checked'


@app.route('/fix_group_rating/<string:group_id>/<int:semester>')
def fix_group_rating(group_id, semester):
    if not current_user.has_role('Admin'):
        return 'not allowed'

    if not group_id or not semester:
        return 'no data'

    from modules.estimates.update_mark_info import update_destiny_by_document

    print 'group: {}, semester: {}'.format(AcademicGroup.objects(id=group_id).first(), semester)
    students = Student.objects(group=group_id, is_expelled=False).distinct('id')
    RatingStipend.objects(student__in=students, semester=semester).delete()
    print 'ratings deleted'

    Mark.objects(source__in=Sheet.objects(group=group_id, semester=semester, all_done=True)) \
        .update(set__for_rating=False, set__old_scores=0)
    Mark.objects(source__in=Slider.objects(semester=semester, all_done=True, student__in=students)) \
        .update(set__for_rating=False, set__old_scores=0)
    print 'marks done'

    for sheet in Sheet.objects(group=group_id, semester=semester, all_done=True):
        update_destiny_by_document(sheet)
    print 'sheets done'

    for slider in Slider.objects(semester=semester, all_done=True,
                                 student__in=students):
        update_destiny_by_document(slider)
    print 'sliders done'

    return 'success'


if __name__ == '__main__':
    # RatingStipend.objects().update(set__date=datetime.datetime(2017, 9, 1))
    # for r in RatingStipend.objects(date__gte=datetime.datetime(2017, 9, 1),
    #                                date__lt=datetime.datetime(2017, 9, 2)).limit(10):
    #     print r.date
    # a = input("enter 1: ")
    # if a == 1:
    #     update_address()


    # a = input("enter 1")
    # if a == 1:
    #     Student.objects().update(set__not_transfered=False)
    #     from modules.setting.choices import NAKAZ_CHOICES
    #     for student in Student.objects(is_delete__ne=True, is_expelled__ne=True, in_academic__ne=True):
    #         flag = True
    #         for expelled_info in student.expelled_info:
    #             if expelled_info.category == NAKAZ_CHOICES[1][0] and expelled_info.date.year == 2017:
    #                 flag = False
    #                 break
    #         if flag:
    #             student.not_transfered = True
    #             student.save()
    # print Student.objects(not_transfered__ne=False).count()
    # a = input("enter 1")
    # if a == 1:
    #     group_ids = ['543e6eac027cbc0d789bce63']
    #     from modules.estimates.update_mark_info import update_destiny_by_document
    #     for group_id in group_ids:
    #         semester = 9
    #         RatingStipend.objects(student__in=Student.objects(group=AcademicGroup.objects.get(id=group_id)), semester=semester).delete()
    #         Mark.objects(source__in=Sheet.objects(group=AcademicGroup.objects.get(id=group_id), date__gte=datetime.date(2017, 4, 1), all_done=True)).update(set__for_rating=False, set__old_scores=0)
    #         Mark.objects(source__in=Slider.objects(end_date__gte=datetime.date(2017, 4, 1), all_done=True,
    #                                                student__in=Student.objects(group=AcademicGroup.objects.get(id=group_id)))).update(set__for_rating=False, set__old_scores=0)
    #         for sheet in Sheet.objects(group=AcademicGroup.objects.get(id=group_id), date__gte=datetime.date(2017, 4, 1), all_done=True, marks__in=Mark.objects(semester=semester)):
    #             update_destiny_by_document(sheet)
    #         print 'sheets done'
    #         for slider in Slider.objects(end_date__gte=datetime.date(2017, 4, 1), all_done=True,
    #                                                student__in=Student.objects(group=AcademicGroup.objects.get(id=group_id)), mark__in=Mark.objects(semester=semester)):
    #             update_destiny_by_document(slider)
    #         print 'sliders done'




    # from bson import DBRef
    # for sheet in Sheet.objects(group=AcademicGroup.objects.get(id='543f8135027cbc0efd8f21a9')):
    #     for i, mark in enumerate(sheet.marks):
    #         if isinstance(mark, DBRef):
    #             del sheet.marks[i]
    #     sheet.save()

    # app.run(debug=True, port=9998)
    app.run(host='0.0.0.0', debug=True, port=5000)
