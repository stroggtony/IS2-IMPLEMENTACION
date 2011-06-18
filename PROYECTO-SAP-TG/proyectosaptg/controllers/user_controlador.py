# -*- coding: utf-8 -*-

from tgext.admin.config import AdminConfig, CrudRestControllerConfig
from sprox.formbase import AddRecordForm, EditableForm
from formencode import Schema
from formencode.validators import FieldsMatch
from tw.forms import *


from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sprox.fillerbase import EditFormFiller



from proyectosaptg.model import *

from tg import expose, flash, require, url, request, redirect
from tg.decorators import without_trailing_slash, with_trailing_slash
from tg.decorators import paginate
from tgext.crud.decorators import registered_validate, register_validators, catch_errors



from tg import tmpl_context

from tgext.crud.controller import CrudRestController


from sprox.widgets import PropertyMultipleSelectField


"""configuraciones del modelo User"""
user_form_validator =  Schema(chained_validators=(FieldsMatch('password',
                                                         'verify_password',
                                                         messages={'invalidNoMatch':
                                                         'Passwords do not match'}),))
class UserRegistrationForm(AddRecordForm):
    __model__ = User
    __require_fields__     = ['password', 'user_name', 'email_address']
    __omit_fields__        = ['_password', 'created', 'user_id', 'town_id','proyectos','display_name']
    __field_order__        = ['user_name', 'email_address', 'display_name', 'password', 'verify_password']
    __base_validator__     = user_form_validator
    email_address          = TextField
    nombres_apellidos      = TextField
    verify_password        = PasswordField('verify_password')

  


class UserCrudConfig(CrudRestControllerConfig):
    class table_type(TableBase):
        __entity__ = User
        __limit_fields__ = ['user_name','nombres_apellidos', 'email_address','created','groups']
        __url__ = '../user.json' #this just tidies up the URL a bit

    class table_filler_type(TableFiller):
        __entity__ = User
        __limit_fields__ = ['user_id', 'user_name','nombres_apellidos', 'email_address','created','groups']
        
        def __actions__(self, obj):
            """Override this function to define how action links should be displayed for the given record."""
            primary_fields = self.__provider__.get_primary_fields(self.__entity__)
            pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
            
            value =  '<div><div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
            '</div><div>'\
            '<form method="POST" action="'+pklist+'" class="button-to">'\
            '<input type="hidden" name="_method" value="DELETE" />'\
            '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
            'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
            '</form>'\
            '</div></div>'

            return value

        def _do_get_provider_count_and_objs(self, **kw):
            limit = kw.get('limit', None)
            offset = kw.get('offset', None)
            order_by = kw.get('order_by', None)
            desc = kw.get('desc', False)
            if len(kw) > 0:
                #se obtienen la lista de id's de roles que estan permitidos en la fase
                id_rol = DBSession.query("group_id").from_statement("SELECT group_id FROM tg_fase_group WHERE fase_id=:idfase").params(idfase = int(kw['fid'])).all()
                #for i in id_rol:
                    #usuario_rol = DBSession.query("user_id").from_statement("SELECT user_id FROM tg_user_group WHERE group_id=:groupid").params(groupid = id_rol)
                objs = DBSession.query(self.__entity__).all()
            else:
                objs = DBSession.query(self.__entity__).all()
                
            #count = len(objs)
            #self.__count__ = count
            return len(objs), objs
   
    new_form_type = UserRegistrationForm
