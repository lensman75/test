#coding: utf-8
from mongoengine import connect, Q

db = connect('lod_3test', alias='default')
from modules.estimates import Mark, Slider, Sabbatical
from modules.student import Student

marks = Mark.objects((Q(rating=u"Не з'явився") or Q(rating=u'Недопущений') or Q(rating=u'Незараховано'))).distinct('student')
print (marks)


def debtor_student_update(arg):
    print (u'SYSTEM: Debtor Student Update')
    for mark in Mark.objects(rating=u'-'):
        mark.rating = u"Не з'явився"
        mark.save()
    bad_students = Mark.objects((Q(rating=u"Не з'явився") or Q(rating=u'Недопущений') or Q(rating=u'Незараховано'))).distinct('student')
    for stud in bad_students:
        # marks = Mark.objects(student=stud, rating=u'-')
        marks = Mark.objects((Q(rating=u"Не з'явився") or Q(rating=u'Недопущений') or Q(rating=u'Незараховано')), Q(student=stud))
        marks = marks.filter(student=stud)
        marks_count = marks.count()
        status = True
        for m in marks:
            status = False
            #if isinstance(m.source, Sheet):
            tmp_marks = Mark.objects(student=stud, type=m.type, subject=m.subject, credit=m.credit, model=m.model, semester=m.semester)
            for tmp_m in tmp_marks:
                if isinstance(tmp_m.source, Slider) or isinstance(tmp_m.source, Sabbatical):
                    status = True
                    marks_count -= 1

        if marks_count < 1:
            stud.is_debtor = False
        else:
            if not stud.human.major:
                stud.is_debtor = True

        stud.save()


debtor_student_update(0)