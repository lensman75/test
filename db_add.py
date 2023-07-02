# -*- coding: utf-8 -*-
from mongoengine import connect, register_connection
from modules.student import Student
from modules.user import User, Role


def init():
    db = connect('lod_3test', alias='default')
    # register_connection(alias='human_2000', name='human')

    role_admin = Role.objects.get(name='Admin')


    # role_operator = Role.objects.get(name='Operator')

    moder = Role(name='Moderator')
    moder.permissions = role_admin.permissions
    # vice_rector = Role(name='Vice_Rector')
    # director = Role(name='Diector')
    # educational_department = Role(name='Educational_Department')
    # labor_protection_department = Role(name='Labor_Protection_Department')
    # archive = Role(name='Archive')
    # HR_department = Role(name='HR_department')
    # Planning_and_Finance_Department = Role(name='Planning_and_Finance_Department')
    #
    # rector.permissions = role_operator.permissions
    # vice_rector.permissions = director.permissions = educational_department.permissions = rector.permissions
    # labor_protection_department.permissions = archive.permissions = HR_department.permissions = Planning_and_Finance_Department.permissions = rector.permissions
    moder.save()
    # rector.save()
    # vice_rector.save()
    # director.save()
    # educational_department.save()
    # labor_protection_department.save()
    # archive.save()
    # HR_department.save()
    # Planning_and_Finance_Department.save()
if __name__ == '__main__':
    init()