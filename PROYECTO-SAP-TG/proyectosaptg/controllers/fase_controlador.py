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



"""configuraciones del modelo Fase"""
class FaseRegistrationForm(AddRecordForm):
  
    __model__ = Fase
    __require_fields__ = ['cod_fase', 'nombre']
    __omit_fields__ = ['id_fase','estado','lineas_bases','items']
    #__field_order__        = ['user_name', 'email_address', 'display_name', 'password', 'verify_password']
    #__base_validator__     = user_form_validator
    #__hidden_fields__      = ['proyecto_id']
    cod_fase           = TextField
    nombre = TextField
    #descripcion                 = TextArea
    #proyecto_id = HiddenField
    


class FaseCrudConfig(CrudRestControllerConfig):
  
    
    class table_type(TableBase):
        __entity__ =  Fase
        __limit_fields__ = ['cod_fase', 'nombre','estado', 'proyecto_id']
        __url__ = '../fases.json' #this just tidies up the URL a bit"""

    class table_filler_type(TableFiller):
        __entity__ = Fase
        __limit_fields__ = ['cod_fase', 'nombre','estado', 'proyecto_id']
        
        
        def __actions__(self, obj):
            """Override this function to define how action links should be displayed for the given record."""
            primary_fields = self.__provider__.get_primary_fields(self.__entity__)
            pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
            
            print "obj:"
            print obj
            
                       
            value =  '<div><div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
            '</div><div>'\
            '<form method="POST" action="'+pklist+'" class="button-to">'\
            '<input type="hidden" name="_method" value="DELETE" />'\
            '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
            'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
            '</form>'\
            '<a class="itmes_link" href="../items/?fid='+pklist+'">Items</a> '\
            '<br/>'\
            '<a class="lineas_link" href="../lineabases/?fid='+pklist+'">Linea Base</a> '\
            '<br/>'\
            '<a class="user_link" href="../users/?fid='+pklist+'">Usuarios_Asignados</a> '\
            '<br/>'\
            '</div></div>'
            
            return value
        
        
        
        
        def proyecto_id(self, obj,**kw):
            #print obj.proyecto_id
            proyecto = DBSession.query(Proyecto).filter_by(id_proyecto=obj.proyecto_id).one()
            return proyecto.nombre
        
        def _do_get_provider_count_and_objs(self, **kw):
            
            limit = kw.get('limit', None)
            offset = kw.get('offset', None)
            order_by = kw.get('order_by', None)
            desc = kw.get('desc', False)
            if len(kw) > 0:
                objs = DBSession.query(self.__entity__).filter_by(proyecto_id=kw['pid']).all()
            else:
                objs = DBSession.query(self.__entity__).all()
                
            count = len(objs)
            self.__count__ = count
            return count, objs
        
        
    class defaultCrudRestController(CrudRestController):
        
        
        @with_trailing_slash
        @expose('proyectosaptg.templates.get_all_fase')
        @expose('json')
        @paginate('value_list', items_per_page=7)
        def get_all(self, *args, **kw):
            
            #print "fase get_all"
            
            val = kw["pid"]
            
            #print kw
            #print args
            
            retorno =  CrudRestController.get_all(self, *args, **kw)
           
            retorno["pid"] = val 
            
            #print retorno
            
            return retorno
            
      
        @without_trailing_slash
        @expose('proyectosaptg.templates.new_fase')
        def new(self, *args, **kw):
            """Display a page to show a new record."""
            
          
            """print "new de fase:"
            print kw
            print args"""
            
            if len(args) > 0:
                #print "entre en el if\n"
                kw['proyecto_id'] = args[0]
                #print kw
                #print args
    
                
            
            tmpl_context.widget = self.new_form
            
            retorno = dict(value=kw, model=self.model.__name__)
            #print retorno
            return retorno
            
        
        
        @expose()
        @registered_validate(error_handler=new)
        def post(self, *args, **kw):
            
            """print "post:\n"
            print kw
            print args"""
            
            pid = kw["proyecto_id"]
            #print kw["proyecto_id"]
            
            self.provider.create(self.model, params=kw)
            
            path = '../?pid='+ str(pid)
            
            #print path
            
            raise redirect(path)
        
        @expose()
        def post_delete(self, *args, **kw):
            """This is the code that actually deletes the record"""
            
            
            fase_to_del = DBSession.query(Fase).filter_by(id_fase=args[0]).one()
            pid = fase_to_del.proyecto_id
            
            #print "fase a borrar:pid\n"
            #print fase_to_del.proyecto_id
            
            pks = self.provider.get_primary_fields(self.model)
            d = {}
            for i, arg in enumerate(args):
                d[pks[i]] = arg
            self.provider.delete(self.model, d)
            
            #print "post_delete:\n"
            
            #print kw
            #print args
            
            
            path = './' + '../' * (len(pks) - 1) + '?pid=' + str(pid)
            #print './' + '../' * (len(pks) - 1) + '?pid=' + str(pid)
            
            #redirect('./' + '../' * (len(pks) - 1))
            redirect(path)
        
        @expose('proyectosaptg.templates.get_delete_fase')
        def get_delete(self, *args, **kw):
            """This is the code that creates a confirm_delete page"""    
            return dict(args=args)    
        
        @expose('tgext.crud.templates.edit')
        def edit(self, *args, **kw):
            """Display a page to edit the record."""
            tmpl_context.widget = self.edit_form
            pks = self.provider.get_primary_fields(self.model)
            kw = {}
            for i, pk in  enumerate(pks):
                kw[pk] = args[i]
            value = self.edit_filler.get_value(kw)
            value['_method'] = 'PUT'
            
            return dict(value=value, model=self.model.__name__, pk_count=len(pks))
        
        
        @expose()
        @registered_validate(error_handler=edit)
        def put(self, *args, **kw):
            """update"""
            pks = self.provider.get_primary_fields(self.model)
            for i, pk in enumerate(pks):
                if pk not in kw and i < len(args):
                    kw[pk] = args[i]
            #print "update:\n"
            #print kw
            #print args
            
            pid = kw['proyecto_id']
            
            path = '../' * len(pks) + "?pid=" + str(pid)
            
            self.provider.update(self.model, params=kw)
            #redirect('../' * len(pks))
            redirect(path)    
        
    new_form_type = FaseRegistrationForm
