# coding: utf-8
from mongoengine import *

from modules.setting import TYPE_WORK_CHOICES

db = connect('lod_3test', alias='default')


class BaseSubject(Document):
    name = StringField(required=True, unique=True)
    # professions = ListField(ReferenceField('Profession'))

    meta = {'allow_inheritance': True}

    def __unicode__(self):
        return self.name


class Subject(BaseSubject):
    in_file = BooleanField(default=False)


class EstimateInfo(Document):
    number = StringField(unique=False)
    course = IntField()
    semester = IntField()
    meta = {'allow_inheritance': True}
    subject = ReferenceField(Subject, reverse_delete_rule=NULLIFY)
    type = IntField(choices=((1, u'Робітнича професія'), (2, u'Бакалаврат'), (3, u'Спец.Маг')))
    model = IntField(choices=TYPE_WORK_CHOICES)  # (choices=((1, u'Іспит'), (2, u'Залік'), (3, u'Курсова робота')))
    credit = FloatField()
    is_credit = BooleanField(default=True)


class _Student(Document):
    edbo_pk = IntField()
    # group = ReferenceField(document_type='AcademicGroup')
    # expelled_group = ReferenceField(document_type='AcademicGroup')
    individual_plans = StringField()  # ListField(ReferenceField(document_type='HumanDocument'))  # індивідуальний план
    # gradebook = ListField(EmbeddedDocumentField(Gradebook))  # StringField()#required=True)  # студентське
    record_book = StringField()
    date_entry = DateTimeField()  # дата вступу
    course = IntField(default=1)  # курс
    marks = ListField(ReferenceField(document_type='Mark'))
    # qualification_level = ReferenceField(document_type=QualificationLevel, reverse_delete_rule=NULLIFY)
    qualification_full_name = StringField()
    qualification_full_name_eng = StringField()
    # training_dir = ReferenceField(document_type='Profession', reverse_delete_rule=NULLIFY)  # напрям підготовки
    # educational_program = ReferenceField(document_type='Specialisation')  # спеціалізація
    # specialty = ReferenceField(document_type='Profession', reverse_delete_rule=NULLIFY)  # напрям підготовки
    # proff_options = ReferenceField('ProffOptions')
    # reason = ReferenceField(document_type='Reason')
    previous_paper_on_education = StringField()
    order_of_enrollment_transfer = StringField()
    # prof_layer = ReferenceField(document_type='AbstractProfLayer')
    # individual_prof_layer = ReferenceField(document_type='AbstractProfLayer')
    transfer_nakaz = StringField()
    transfer_date = DateTimeField()
    prepare_of_expelled = BooleanField(default=False)
    quota = StringField()
    po = BooleanField(default=False)
    student_type = StringField(default=u'студент', choices=[
        (u'студент', u'студент'), (u'слухач', u'слухач'), (u'здобувач', u'здобувач'), (u'аспірант', u'аспірант')
    ])

    debts = ListField(ReferenceField(document_type='Mark'))

    # master_diploma = ListField(EmbeddedDocumentField(Diploma))
    # bachelor_diploma = ListField(EmbeddedDocumentField(Diploma))
    # expert_diploma = ListField(EmbeddedDocumentField(Diploma))
    # profession_diploma = ListField(EmbeddedDocumentField(Diploma))
    # academs = ListField(EmbeddedDocumentField(SabbaticalPeriod))
    in_academic = BooleanField(default=False)
    is_expelled = BooleanField(default=False)
    expelled_date = DateTimeField()
    expelled_nakaz = StringField()
    # expelled_info = ListField(EmbeddedDocumentField(ExpelledNakaz))
    is_updated = BooleanField(default=False)
    is_second_edu = BooleanField(default=False)
    is_academic_vac = BooleanField(default=False)
    is_re_certif = BooleanField(default=False)
    is_alien = BooleanField(default=False)
    is_re_learning = BooleanField(default=False)
    is_debtor = BooleanField(default=False)
    is_completed = BooleanField(default=False)
    is_delete = BooleanField(default=False)
    not_transfered = BooleanField(default=False)


class Mark(Document):
    rating_scale = {u'A': u'Відмінно', u'B': u'Добре', u'C': u'Добре', u'D': u'Задовільно', u'E': u'Задовільно'}
    source = ReferenceField(document_type=EstimateInfo, reverse_delete_rule=CASCADE)
    subject = ReferenceField(Subject, reverse_delete_rule=NULLIFY)
    student = ReferenceField(required=True, document_type=_Student, reverse_delete_rule=NULLIFY)

    type = IntField(choices=((1, u'Оцінки Робітнича професія'), (2, u'Оцінки Бакалаврат'), (3, u'Оцінки Спец.Маг')))
    model = IntField(choices=TYPE_WORK_CHOICES)  # ((1, u'Іспит'), (2, u'Залік'), (3, u'Курсова робота')))
    rating = StringField(choices=(u'A', u'B', u'C', u'D', u'E',
                                  u'Зараховано', u"Не з'явився", u'Недопущений', u'Незараховано', u'Не вивчає',
                                  u'Індивідуальний план'))

    scores = IntField()
    semester = IntField()
    credit = FloatField()
    is_credit = BooleanField(default=True)
    improved = BooleanField(default=False)
    retake = BooleanField(default=False)  # перездача


# Бігунок
class Slider(EstimateInfo):
    student = ReferenceField(required=True, document_type=_Student, reverse_delete_rule=NULLIFY)
    mark = ReferenceField('Mark')
    improving = BooleanField(default=False)

    start_date = DateTimeField()
    end_date = DateTimeField()

    def __unicode__(self):
        return u'Аркуш успішності студента №{0}'.format(self.number)


# Академ відомість
class Sabbatical(EstimateInfo):
    date_entry = DateTimeField()
    date = DateTimeField()
    type = IntField(choices=((1, u'Оцінки Робітнича професія'), (2, u'Оцінки Бакалаврат'), (3, u'Оцінки Спец.Маг')))
    reg_number = StringField(required=True)
    nakaz = StringField()
    expelled_date = DateTimeField()
    # reason = ReferenceField(document_type='Reason')
    student = ReferenceField(required=True, document_type=_Student, reverse_delete_rule=NULLIFY)
    marks = ListField(ReferenceField(Mark))
    all_done = BooleanField()
    printed = BooleanField()

    # group = ReferenceField(document_type='AcademicGroup', reverse_delete_rule=NULLIFY)

    def __unicode__(self):
        return u'Академічна довідка №{0}'.format(self.number)


class Sheet(EstimateInfo):
    # group = ReferenceField(document_type='AcademicGroup')
    marks = ListField(ReferenceField(Mark))
    # teacher = ReferenceField(document_type='Teacher', reverse_delete_rule=NULLIFY)

    date = DateTimeField()
    all_done = BooleanField(default=False)

    def __unicode__(self):
        return u'Відомість №{0}'.format(self.number)


# Академічна різниця
class AcademicDifference(EstimateInfo):
    def __unicode__(self):
        return u'Академічна різниця/Перезарахування'


bed_marks = [u"Не з'явився", u'Недопущений', u'Незараховано', u'Індивідуальний план']


def update_debtors_state():  # оцінки не задовільно
    bed_marks_docs = Mark.objects(rating__in=bed_marks, retake__ne=True,
                                  # студент не відрахований та не в академці
                                  student__in=_Student.objects(is_expelled=False, in_academic=False))
    bed_students = bed_marks_docs.distinct('student')  # потенційні боржники
    all_bed_students = _Student.objects(is_expelled=False, in_academic=False, is_debtor=True)
    print len(all_bed_students)
    for st in all_bed_students:
        if st in bed_students:
            continue
        else:
            st.is_debtor = False
            st.save()
    print len(bed_students)
    for student in bed_students:
        st_bed_marks = bed_marks_docs.filter(student=student)  # погані оцінки студента
        bed_marks_count = st_bed_marks.count()  # кількість поганих оцінок у студента

        if bed_marks_count <= 0 and student.is_debtor:  # Якщо не має поганих оцінок та не боржник
            student.is_debtor = False  # -- обновити студента(він не боржник4)
            student.save()
        # if bed_marks_count:
        else:
            for m in st_bed_marks:  # кожна погана оцінка студента
                # student -- студент,
                # type (1, u'Оцінки Робітнича професія'), (2, u'Оцінки Бакалаврат'), (3, u'Оцінки Спец.Маг')
                # subject предмет
                # credit - кредит
                # model - # ((1, u'Іспит'), (2, u'Залік'), (3, u'Курсова робота')))
                # semester - семестр

                tmp_marks = Mark.objects(student=student, type=m.type, subject=m.subject,
                                         credit=m.credit, model=m.model, semester=m.semester)  # оцінки для перевірки
                for tmp_m in tmp_marks:
                    if (isinstance(tmp_m.source, Slider) or isinstance(tmp_m.source,
                                                                       Sabbatical)) and tmp_m.rating not in bed_marks:
                        m.retake = True
                        m.save()
                        bed_marks_count -= 1
            is_debtor = bed_marks_count >= 1  # and not student.human.major
            if is_debtor != student.is_debtor:
                student.is_debtor = is_debtor
                student.save()
    print(u'finish 1')


update_debtors_state()
