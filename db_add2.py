# -*- coding: utf-8 -*-
from mongoengine import connect
db = connect('lod_3test', alias='default')
# from modules.student import Student
from modules.user import User, Role


def init():

    rector = Role.objects.get(name='Rector')
    vice_rector = Role.objects.get(name='Vice_Rector')
    director = Role.objects.get(name='Diector')
    educational_department = Role.objects.get(name='Educational_Department')
    labor_protection_department = Role.objects.get(name='Labor_Protection_Department')
    archive = Role.objects.get(name='Archive')
    HR_department = Role.objects.get(name='HR_department')
    Planning_and_Finance_Department = Role.objects.get(name='Planning_and_Finance_Department')
    operator = Role.objects.get(name='Operator')

    vice_rector.permissions = director.permissions = educational_department.permissions = rector.permissions = operator.permissions
    labor_protection_department.permissions = archive.permissions = HR_department.permissions = Planning_and_Finance_Department.permissions = rector.permissions

    rector.save()
    vice_rector.save()
    director.save()
    educational_department.save()
    labor_protection_department.save()
    archive.save()
    HR_department.save()
    Planning_and_Finance_Department.save()


if __name__ == '__main__':
    init()