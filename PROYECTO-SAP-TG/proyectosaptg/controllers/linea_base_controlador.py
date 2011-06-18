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


"""configuraciones del modelo LineaBase"""
class LineaBaseRegistrationForm(AddRecordForm):
    __model__ = LineaBase
    __require_fields__ = ['cod_linea_base', 'descripcion', 'items']
    __omit_fields__ = ['id_linea_base', 'version', 'estado','peso_acumulado', 'fecha_creacion']
    cod_linea_base           = TextField
    descripcion              = TextArea

class LineaBaseCrudConfig(CrudRestControllerConfig):
    class table_type(TableBase):
        __entity__ =  LineaBase
        __limit_fields__ = ['cod_linea_base', 'descripcion', 'items']
        __url__ = '../linea_base.json' #this just tidies up the URL a bit

    class table_filler_type(TableFiller):
        __entity__ = LineaBase
        __limit_fields__ = ['id_linea_base','cod_linea_base','descripcion', 'items']
    
        def __actions__(self, obj):
            """Override this function to define how action links should be displayed for the given record."""
            primary_fields = self.__provider__.get_primary_fields(self.__entity__)
            pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))

            value =  '<div><div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
            '</div><div>'\
            '<form method="POST" action="'+pklist+'" class="button-to">'\
            '<input type="hidden" name="_method" value="DELETE" />'\
            '<input class="delete-button" onclick="return confirm(\'Esta seguro que desea eliminar?\');" value="delete" type="submit" '\
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
                objs = DBSession.query(self.__entity__).filter_by(id_fase_fk=kw['fid']).all()
            else:
                objs = DBSession.query(self.__entity__).all()
                
            count = len(objs)
            self.__count__ = count
            return count, objs



    class defaultCrudRestController(CrudRestController):
        @with_trailing_slash
        @expose('proyectosaptg.templates.get_all_lineabase')
        @expose('json')
        @paginate('value_list', items_per_page=7)
        def get_all(self, *args, **kw):
                    
            print args
            print kw
            
            fid = kw['fid']
            
                    
            retorno = CrudRestController.get_all(self, *args, **kw)

            retorno['fid'] = fid
                    
            return retorno

        @without_trailing_slash
        @expose('proyectosaptg.templates.new_fase')
        def new(self, *args, **kw):
            """Display a page to show a new record."""
            print "new de linea base\n"
            
            
            print kw
            print args
            
                                
            
            
            
            if len(args) > 0:
                print "entre en el if\n"
                 
                
                #kw['fase'] = args[0]
                kw['id_fase_fk'] =  args[0] 
                
                print kw
                print args
    
            
            
            
            
            tmpl_context.widget = self.new_form
            
            retorno = dict(value=kw, model=self.model.__name__)
            
            print "retorno:\n"
            print retorno
            
            return retorno

        @expose()
        @registered_validate(error_handler=new)
        def post(self, *args, **kw):
            
            print "post item:"
            print kw
            print args
            
            
            fid = kw['id_fase_fk']
            
            
            new_item = self.provider.create(self.model, params=kw)
            
                        
            path = '../?fid='+ str(fid)
            
            print path
            
            raise redirect(path)
                
        @expose()
        def post_delete(self, *args, **kw):
            """This is the code that actually deletes the record"""
            
            #obtenemos el id de la linea base para hacer el filtrado despues de la redireccion
            lb_to_del = DBSession.query(LineaBase).filter_by(id_linea_base=args[0]).one()
            fid = lb_to_del.id_fase_fk
            
            
            pks = self.provider.get_primary_fields(self.model)
            d = {}
            for i, arg in enumerate(args):
                d[pks[i]] = arg
            self.provider.delete(self.model, d)
            
            path = './' + '../' * (len(pks) - 1) + '?fid=' + str(fid)
            
            redirect(path)
                

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
            
            
            fid = kw['id_fase_fk']
            path = '../' * len(pks) + "?fid=" + str(fid)
            
            self.provider.update(self.model, params=kw)
            redirect(path)



    new_form_type = LineaBaseRegistrationForm



