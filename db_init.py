# -*- coding: utf-8 -*-
from mongoengine import connect
from modules.student import Student
from modules.user import User, Role


def init():
    db = connect('lod_3test', alias='default')

    role_admin = Role(name='Admin')
    role_admin.permissions = {u'class-modules-subject-view-SubjectView': {u'read_only': [], u'form_edit_columns': [u'name', u'professions'], u'column_list': [u'name', u'professions'], u'form_create_columns': [u'name', u'professions'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-unit-views-InstituteView': {u'read_only': [], u'form_edit_columns': [u'abbreviated', u'marshall', u'date_creation', u'date_liquidation', u'units', u'full_name', u'owner'], u'column_list': [u'abbreviated', u'marshall', u'date_creation'], u'form_create_columns': [u'abbreviated', u'marshall', u'date_creation', u'date_liquidation', u'units', u'full_name', u'owner'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-unit-views-UniversityView': {u'read_only': [], u'form_edit_columns': [u'abbreviated', u'marshall', u'date_creation', u'date_liquidation', u'full_name', u'units'], u'column_list': [u'abbreviated', u'marshall', u'date_creation'], u'form_create_columns': [u'abbreviated', u'marshall', u'date_creation', u'date_liquidation', u'full_name', u'units'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-profession-view-QualificationLevelView': {u'read_only': [], u'form_edit_columns': [u'name'], u'column_list': [u'name'], u'form_create_columns': [u'name'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-profession-view-ProffOptionsView': {u'read_only': [], u'form_edit_columns': [u'date_into_mag', u'type_bachelor_work', u'date_into_bach', u'topic_mag_work', u'topic_bachelor_work', u'tech_trans', u'cond_mag', u'prev_doc_bach', u'prev_doc_mag', u'mark_mag_work', u'mark_bachelor_work', u'foreign_lang', u'cond_bachelor'], u'column_list': [], u'form_create_columns': [u'date_into_mag', u'type_bachelor_work', u'date_into_bach', u'topic_mag_work', u'topic_bachelor_work', u'tech_trans', u'cond_mag', u'prev_doc_bach', u'prev_doc_mag', u'mark_mag_work', u'mark_bachelor_work', u'foreign_lang', u'cond_bachelor'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-profession-view-ProfesionView': {u'read_only': [], u'form_edit_columns': [u'code', u'name', u'end_date', u'start_date', u'qualification'], u'column_list': [u'code', u'name', u'end_date', u'start_date', u'qualification'], u'form_create_columns': [u'code', u'name', u'end_date', u'start_date', u'qualification'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-unit-views-DepartamentView': {u'read_only': [], u'form_edit_columns': [u'abbreviated', u'marshall', u'date_creation', u'date_liquidation', u'units', u'full_name', u'owner'], u'column_list': [u'abbreviated', u'marshall', u'date_creation'], u'form_create_columns': [u'abbreviated', u'marshall', u'date_creation', u'date_liquidation', u'units', u'full_name', u'owner'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-estimates-views-SabbaticalView': {u'read_only': [u'student'], u'form_edit_columns': [u'number', u'student', u'reg_number', u'date', u'type'], u'column_list': [u'number', u'student', u'reg_number'], u'form_create_columns': [u'number', u'student', u'reg_number', u'date', u'type'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-unit-views-GroupBacAdditionView': {u'read_only': [], u'form_edit_columns': [u'load', u'data_entry', u'term_training', u'demands_study', u'edu_qual_gen_case', u'periods_practice', u'date_issue_diploma'], u'column_list': [], u'form_create_columns': [u'load', u'data_entry', u'term_training', u'demands_study', u'edu_qual_gen_case', u'periods_practice', u'date_issue_diploma'], u'actions': {u'can_edit': False, u'can_delete': False, u'can_create': False}}, u'class-modules-student-view-GradebookView': {u'read_only': [], u'form_edit_columns': [], u'column_list': [u'qualification_level', u'course', u'human', u'group', u'training_dir'], u'form_create_columns': [], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-unit-views-GraduateView': {u'read_only': [], u'form_edit_columns': [u'abbreviated', u'marshall', u'date_liquidation', u'full_name', u'date_creation'], u'column_list': [u'abbreviated', u'marshall', u'date_liquidation', u'full_name', u'date_creation'], u'form_create_columns': [u'abbreviated', u'marshall', u'date_liquidation', u'full_name', u'date_creation'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-history-view-HistoryView': {u'read_only': [u'date_change', u'user', u'procedure'], u'form_edit_columns': [u'date_change', u'user', u'procedure'], u'column_list': [u'date_change', u'user', u'procedure'], u'form_create_columns': [u'date_change', u'user', u'procedure'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-human-view-HumanView': {u'read_only': [], u'form_edit_columns': [u'phone_number', u'human_documents', u'dative_name', u'name', u'privileges', u'actual_address', u'sex', u'patronymic', u'registration_address', u'parents', u'birth_date', u'nationality', u'surname', u'hostel'], u'column_list': [u'phone_number', u'human_documents', u'dative_name', u'name', u'privileges', u'actual_address', u'sex', u'patronymic', u'registration_address', u'parents', u'birth_date', u'nationality', u'surname', u'hostel'], u'form_create_columns': [u'phone_number', u'human_documents', u'dative_name', u'name', u'privileges', u'actual_address', u'sex', u'patronymic', u'registration_address', u'parents', u'birth_date', u'nationality', u'surname', u'hostel'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-estimates-views-SliderView': {u'read_only': [], u'form_edit_columns': [u'end_date', u'number', u'student', u'type', u'start_date', u'semester', u'model'], u'column_list': [u'end_date', u'number', u'student', u'type', u'subject'], u'form_create_columns': [u'end_date', u'number', u'student', u'type', u'subject', u'start_date', u'semester', u'model'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-student-view-StudentDiplomaView': {u'read_only': [], u'form_edit_columns': [], u'column_list': [u'qualification_level', u'course', u'human', u'group', u'training_dir'], u'form_create_columns': [], u'actions': {u'can_edit': False, u'can_delete': False, u'can_create': False}}, u'class-modules-unit-views-GroupMagAdditionView': {u'read_only': [], u'form_edit_columns': [u'load', u'data_entry', u'term_training', u'demands_study', u'edu_qual_gen_case', u'periods_practice', u'date_issue_diploma'], u'column_list': [], u'form_create_columns': [u'load', u'data_entry', u'term_training', u'demands_study', u'edu_qual_gen_case', u'periods_practice', u'date_issue_diploma'], u'actions': {u'can_edit': False, u'can_delete': False, u'can_create': False}}, u'class-modules-student-view-StudentView': {u'read_only': [u'group'], u'form_edit_columns': [u'finance', u'training_dir', u'qualification_level', u'course', u'date_entry', u'gradebook', u'group'], u'column_list': [u'finance', u'training_dir', u'qualification_level', u'course', u'human', u'group'], u'form_create_columns': [], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-student-view-StudentHistoryView': {u'read_only': [u'qualification_level', u'course', u'group', u'date_entry', u'finance', u'training_dir', u'gradebook'], u'form_edit_columns': [u'course', u'group', u'finance', u'training_dir', u'reason', u'qualification_level', u'date_entry', u'is_expelled', u'gradebook'], u'column_list': [u'course', u'human', u'group', u'finance', u'training_dir', u'reason'], u'form_create_columns': [], u'actions': {u'can_edit': True, u'can_delete': False, u'can_create': False}}, u'class-modules-unit-views-AcademicGroupView': {u'read_only': [], u'form_edit_columns': [u'abbreviated', u'training_dir', u'qualification_level', u'course', u'academic_law', u'education_form', u'date_liquidation', u'full_name', u'is_archive', u'year_study', u'list_students', u'date_creation', u'unit_layer'], u'column_list': [u'abbreviated', u'training_dir', u'qualification_level', u'course'], u'form_create_columns': [u'abbreviated', u'training_dir', u'qualification_level', u'course', u'academic_law', u'education_form', u'date_liquidation', u'full_name', u'is_archive', u'year_study', u'date_creation', u'unit_layer'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-estimates-views-SheetView': {u'read_only': [u'group', u'number', u'course', u'semester', u'date', u'model', u'type', u'subject'], u'form_edit_columns': [u'group', u'number', u'semester', u'date', u'subject', u'course', u'model', u'type'], u'column_list': [u'group', u'number', u'semester', u'date', u'subject'], u'form_create_columns': [u'group', u'number', u'semester', u'date', u'subject', u'model', u'type'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-unit-views-PHView': {u'read_only': [], u'form_edit_columns': [u'departament', u'end_date', u'institute', u'switch', u'start_date', u'professions'], u'column_list': [u'departament', u'end_date', u'institute', u'switch', u'start_date'], u'form_create_columns': [u'departament', u'end_date', u'institute', u'switch', u'start_date', u'professions'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-estimates-views-MarkView': {u'read_only': [], u'form_edit_columns': [], u'column_list': [], u'form_create_columns': [], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-user-view-UserView': {u'read_only': [], u'form_edit_columns': [u'active', u'login', u'password', u'roles', u'unit_layer'], u'column_list': [u'active', u'login', u'password', u'roles'], u'form_create_columns': [u'active', u'login', u'password', u'roles', u'unit_layer'], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}}
    role_admin.save()
    #role_admin = Role.objects.get(name='Admin')
    user_admin = User(password='123456', login='admin', active=True)
    user_admin.roles = [role_admin]
    user_admin.save()

    role_operator = Role(name='Operator')
    role_operator.permissions = {u'class-modules-subject-view-SubjectView': {u'read_only': [], u'form_edit_columns': [u'name', u'professions'], u'column_list': [u'name', u'professions'], u'form_create_columns': [u'name', u'professions'], u'actions': {u'can_edit': True, u'can_delete': False, u'can_create': True}}, u'class-modules-unit-views-InstituteView': {u'read_only': [], u'form_edit_columns': [u'abbreviated', u'marshall', u'date_creation', u'date_liquidation', u'units', u'full_name', u'owner'], u'column_list': [u'abbreviated', u'marshall', u'date_creation'], u'form_create_columns': [u'abbreviated', u'marshall', u'date_creation', u'date_liquidation', u'units', u'full_name', u'owner'], u'actions': {u'can_edit': False, u'can_delete': False, u'can_create': False}}, u'class-modules-unit-views-UniversityView': {u'read_only': [], u'form_edit_columns': [u'abbreviated', u'marshall', u'date_creation', u'date_liquidation', u'full_name', u'units'], u'column_list': [u'abbreviated', u'marshall', u'date_creation'], u'form_create_columns': [u'abbreviated', u'marshall', u'date_creation', u'date_liquidation', u'full_name', u'units'], u'actions': {u'can_edit': False, u'can_delete': False, u'can_create': False}}, u'class-modules-profession-view-QualificationLevelView': {u'read_only': [], u'form_edit_columns': [u'name'], u'column_list': [u'name'], u'form_create_columns': [u'name'], u'actions': {u'can_edit': True, u'can_delete': False, u'can_create': True}}, u'class-modules-profession-view-ProffOptionsView': {u'read_only': [], u'form_edit_columns': [u'date_into_mag', u'type_bachelor_work', u'date_into_bach', u'topic_mag_work', u'topic_bachelor_work', u'tech_trans', u'cond_mag', u'prev_doc_bach', u'prev_doc_mag', u'mark_mag_work', u'mark_bachelor_work', u'foreign_lang', u'cond_bachelor'], u'column_list': [], u'form_create_columns': [u'date_into_mag', u'type_bachelor_work', u'date_into_bach', u'topic_mag_work', u'topic_bachelor_work', u'tech_trans', u'cond_mag', u'prev_doc_bach', u'prev_doc_mag', u'mark_mag_work', u'mark_bachelor_work', u'foreign_lang', u'cond_bachelor'], u'actions': {u'can_edit': True, u'can_delete': False, u'can_create': True}}, u'class-modules-profession-view-ProfesionView': {u'read_only': [], u'form_edit_columns': [u'code', u'name', u'end_date', u'start_date', u'qualification'], u'column_list': [u'code', u'name', u'end_date', u'start_date', u'qualification'], u'form_create_columns': [u'code', u'name', u'end_date', u'start_date', u'qualification'], u'actions': {u'can_edit': True, u'can_delete': False, u'can_create': True}}, u'class-modules-unit-views-DepartamentView': {u'read_only': [], u'form_edit_columns': [u'abbreviated', u'marshall', u'date_creation', u'date_liquidation', u'units', u'full_name', u'owner'], u'column_list': [u'abbreviated', u'marshall', u'date_creation'], u'form_create_columns': [u'abbreviated', u'marshall', u'date_creation', u'date_liquidation', u'units', u'full_name', u'owner'], u'actions': {u'can_edit': False, u'can_delete': False, u'can_create': False}}, u'class-modules-estimates-views-SabbaticalView': {u'read_only': [u'student'], u'form_edit_columns': [u'number', u'student', u'type', u'reg_number', u'date'], u'column_list': [u'number', u'student', u'type', u'reg_number', u'date'], u'form_create_columns': [u'number', u'student', u'type', u'reg_number', u'date'], u'actions': {u'can_edit': True, u'can_delete': False, u'can_create': True}}, u'class-modules-unit-views-GroupBacAdditionView': {u'read_only': [], u'form_edit_columns': [u'load', u'data_entry', u'term_training', u'demands_study', u'edu_qual_gen_case', u'periods_practice', u'date_issue_diploma'], u'column_list': [], u'form_create_columns': [u'load', u'data_entry', u'term_training', u'demands_study', u'edu_qual_gen_case', u'periods_practice', u'date_issue_diploma'], u'actions': {u'can_edit': True, u'can_delete': False, u'can_create': True}}, u'class-modules-student-view-GradebookView': {u'read_only': [], u'form_edit_columns': [], u'column_list': [u'qualification_level', u'course', u'human', u'group', u'training_dir'], u'form_create_columns': [], u'actions': {u'can_edit': False, u'can_delete': False, u'can_create': False}}, u'class-modules-unit-views-GraduateView': {u'read_only': [], u'form_edit_columns': [u'abbreviated', u'marshall', u'date_liquidation', u'full_name', u'date_creation'], u'column_list': [u'abbreviated', u'marshall', u'date_creation'], u'form_create_columns': [u'abbreviated', u'marshall', u'date_liquidation', u'full_name', u'date_creation'], u'actions': {u'can_edit': False, u'can_delete': False, u'can_create': False}}, u'class-modules-history-view-HistoryView': {u'read_only': [], u'form_edit_columns': [u'date_change', u'user', u'procedure'], u'column_list': [u'date_change', u'user', u'procedure'], u'form_create_columns': [u'date_change', u'user', u'procedure'], u'actions': {u'can_edit': False, u'can_delete': False, u'can_create': False}}, u'class-modules-human-view-HumanView': {u'read_only': [], u'form_edit_columns': [u'phone_number', u'human_documents', u'dative_name', u'name', u'privileges', u'actual_address', u'sex', u'patronymic', u'registration_address', u'parents', u'birth_date', u'nationality', u'surname', u'hostel'], u'column_list': [u'phone_number', u'human_documents', u'dative_name', u'name', u'privileges', u'actual_address', u'sex', u'patronymic', u'registration_address', u'parents', u'birth_date', u'nationality', u'surname', u'hostel'], u'form_create_columns': [u'phone_number', u'human_documents', u'dative_name', u'name', u'privileges', u'actual_address', u'sex', u'patronymic', u'registration_address', u'parents', u'birth_date', u'nationality', u'surname', u'hostel'], u'actions': {u'can_edit': True, u'can_delete': False, u'can_create': True}}, u'class-modules-estimates-views-SliderView': {u'read_only': [], u'form_edit_columns': [u'end_date', u'number', u'student', u'type', u'subject', u'course', u'start_date', u'semester', u'model'], u'column_list': [u'end_date', u'number', u'student', u'type', u'subject'], u'form_create_columns': [u'end_date', u'number', u'student', u'type', u'subject', u'start_date', u'semester', u'model'], u'actions': {u'can_edit': True, u'can_delete': False, u'can_create': True}}, u'class-modules-student-view-StudentDiplomaView': {u'read_only': [], u'form_edit_columns': [], u'column_list': [u'qualification_level', u'course', u'human', u'group', u'training_dir'], u'form_create_columns': [], u'actions': {u'can_edit': False, u'can_delete': False, u'can_create': False}}, u'class-modules-unit-views-GroupMagAdditionView': {u'read_only': [], u'form_edit_columns': [u'load', u'data_entry', u'term_training', u'demands_study', u'edu_qual_gen_case', u'periods_practice', u'date_issue_diploma'], u'column_list': [], u'form_create_columns': [u'load', u'data_entry', u'term_training', u'demands_study', u'edu_qual_gen_case', u'periods_practice', u'date_issue_diploma'], u'actions': {u'can_edit': True, u'can_delete': False, u'can_create': True}}, u'class-modules-student-view-StudentView': {u'read_only': [u'group'], u'form_edit_columns': [u'finance', u'training_dir', u'qualification_level', u'course', u'group', u'is_debtor', u'individual_plans', u'date_entry', u'gradebook'], u'column_list': [u'finance', u'training_dir', u'qualification_level', u'course', u'human', u'group'], u'form_create_columns': [u'finance', u'training_dir', u'qualification_level', u'course', u'group', u'individual_plans', u'date_entry', u'gradebook'], u'actions': {u'can_edit': True, u'can_delete': False, u'can_create': True}}, u'class-modules-student-view-StudentHistoryView': {u'read_only': [u'course', u'human', u'group', u'finance', u'training_dir'], u'form_edit_columns': [u'qualification_level', u'course', u'group', u'date_entry', u'finance', u'training_dir', u'reason', u'is_expelled', u'gradebook'], u'column_list': [u'course', u'human', u'group', u'finance', u'training_dir', u'reason'], u'form_create_columns': [], u'actions': {u'can_edit': True, u'can_delete': False, u'can_create': False}}, u'class-modules-unit-views-AcademicGroupView': {u'read_only': [u'unit_layer'], u'form_edit_columns': [u'abbreviated', u'training_dir', u'qualification_level', u'course', u'is_archive', u'academic_law', u'education_form', u'date_liquidation', u'full_name', u'year_study', u'list_students', u'date_creation', u'unit_layer'], u'column_list': [u'abbreviated', u'training_dir', u'qualification_level', u'course', u'is_archive'], u'form_create_columns': [u'abbreviated', u'training_dir', u'qualification_level', u'course', u'is_archive', u'academic_law', u'education_form', u'full_name', u'year_study', u'date_creation', u'unit_layer'], u'actions': {u'can_edit': True, u'can_delete': False, u'can_create': True}}, u'class-modules-estimates-views-SheetView': {u'read_only': [u'group', u'number', u'course', u'semester', u'date', u'subject'], u'form_edit_columns': [u'group', u'number', u'semester', u'date', u'subject', u'model', u'type'], u'column_list': [u'group', u'number', u'semester', u'date', u'subject'], u'form_create_columns': [u'group', u'number', u'semester', u'date', u'subject', u'model', u'type'], u'actions': {u'can_edit': True, u'can_delete': False, u'can_create': True}}, u'class-modules-unit-views-PHView': {u'read_only': [], u'form_edit_columns': [u'departament', u'end_date', u'institute', u'switch', u'start_date', u'professions'], u'column_list': [u'departament', u'end_date', u'institute', u'switch', u'start_date'], u'form_create_columns': [u'departament', u'end_date', u'institute', u'switch', u'start_date', u'professions'], u'actions': {u'can_edit': False, u'can_delete': False, u'can_create': False}}, u'class-modules-estimates-views-MarkView': {u'read_only': [], u'form_edit_columns': [], u'column_list': [], u'form_create_columns': [], u'actions': {u'can_edit': True, u'can_delete': True, u'can_create': True}}, u'class-modules-user-view-UserView': {u'read_only': [], u'form_edit_columns': [u'active', u'login', u'password', u'roles', u'unit_layer'], u'column_list': [u'active', u'login', u'password', u'roles'], u'form_create_columns': [u'active', u'login', u'password', u'roles', u'unit_layer'], u'actions': {u'can_edit': False, u'can_delete': False, u'can_create': False}}}
    role_operator.save()

    user_operator1 = User(password='123456', login='dekanat', active=True)
    user_operator1.roles = [role_operator]
    user_operator1.save()

if __name__ == '__main__':
    init()