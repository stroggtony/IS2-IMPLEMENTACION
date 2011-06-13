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
   
    new_form_type = UserRegistrationForm





from repoze.what import predicates
from repoze.what.predicates import not_anonymous

"""configuraciones del modelo Proyecto"""
"""proyecto_form_validator =  Schema(chained_validators=(FieldsMatch('password',
                                                         'verify_password',
                                                         messages={'invalidNoMatch':
                                                         'Passwords do not match'}),))"""
class ProyectoRegistrationForm(AddRecordForm):
    __model__ = Proyecto
    __require_fields__ = ['cod_proyecto', 'nombre']
    __omit_fields__ = ['id_proyecto', 'estado','fecha_creacion' ,'fecha_inicio', 
                      'fecha_finalizacion_anulacion', 'fases','user']
    cod_proyecto           = TextField
    nombre                 = TextField
    usuario_creador = HiddenField
    __dropdown_field_names__ = {'tipo_items':'nombre'}
     

class ProyectoCrudConfig(CrudRestControllerConfig):
    class table_type(TableBase):
        __entity__ = Proyecto
        __limit_fields__ = ['cod_proyecto', 'nombre','estado', 'fecha_creacion','fecha_inicio', 
                            'fecha_finalizacion_anulacion','usuario_creador']
        #__omit_fields__ = ['__actions__'] 
          
        
        
        __url__ = '../proyecto.json' #this just tidies up the URL a bit

    class table_filler_type(TableFiller):
        __entity__ = Proyecto
        __limit_fields__ = ['id_proyecto','cod_proyecto', 'nombre','estado', 'fecha_creacion', 
                            'fecha_inicio', 'fecha_finalizacion_anulacion','usuario_creador']
                            
        """def user_id(self, obj, **kw):
            user = DBSession.query(User).filter_by(user_id=obj.user_id).one()
            return user.user_name"""
        
        
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
            '<a class="fases_link" href="../fases/?pid='+pklist+'">Fases</a>'\
            '</div></div>'
            
            return value
        
        
    
    class defaultCrudRestController(CrudRestController):
        @with_trailing_slash
        @expose('proyectosaptg.templates.get_all')
        @expose('json')
        @paginate('value_list', items_per_page=7)
        def get_all(self, *args, **kw):
            return CrudRestController.get_all(self, *args, **kw)
      
    
        @without_trailing_slash
        @expose('proyectosaptg.templates.new')
        def new(self, *args, **kw):
            """Display a page to show a new record."""
            
            #obtenemos el nombre del usuario creador del proyecto
            user = request.identity['repoze.who.userid'] 
           
            print "new de proyecto, esto es user:\n"
            print user
            
            kw["usuario_creador"]= user
            
            tmpl_context.widget = self.new_form
            
            retorno = dict(value=kw, model=self.model.__name__)
            
            return retorno
    
    #proyecto_table_filler = CamposTableFiller(DBSession)                        
    new_form_type = ProyectoRegistrationForm

      
    
    
    
  
      
    
    


"""configuraciones del modelo TipoItem"""
"""tipo_item_form_validator =  Schema(chained_validators=(FieldsMatch('password',
                                                         'verify_password',
                                                         messages={'invalidNoMatch':
                                                         'Passwords do not match'}),))"""


"""from sprox.widgets import PropertyMultipleSelectField
class MyPropertyMultipleSelectField(PropertyMultipleSelectField):
    def _my_update_params(self, d, nullable=False):
        
        print "MyPropertyMultipleSelectField,d:\n:"
        print d
        
        atributos = DBSession.query(Atributo).filter_by(id_atributo=d["filtrar_id"]).all()
        options = [(atributo.id_atributo, atributo.nombre)
                            for atributo in atributos]
        d['options']= options
        return d"""
    



class TipoItemRegistrationForm(AddRecordForm):
    __model__ = TipoItem
    __require_fields__ = ['cod_tipo_item','nombre' ,'descripcion']
    __omit_fields__ = ['id_tipo_item']
    #__field_order__        = ['user_name', 'email_address', 'display_name', 'password', 'verify_password']
    #__base_validator__     = user_form_validator
    nombre           = TextField
    cod_tipo_item           = TextField
    #descripcion                 = TextArea
    __dropdown_field_names__ = {'atributos':'nombre'}
    
    #atributos_options = [1,2]
   #atributos =  MyPropertyMultipleSelectField
    

class TipoItemCrudConfig(CrudRestControllerConfig):
    class table_type(TableBase):
        __entity__ =  TipoItem
        __limit_fields__ = ['cod_tipo_item', 'nombre','descripcion','atributos']
        
        
        __url__ = '../tipoitem.json' #this just tidies up the URL a bit
       


    class table_filler_type(TableFiller):
        __entity__ = TipoItem
        __limit_fields__ = ['id_tipo_item','cod_tipo_item', 'nombre','descripcion','atributos']
        
        def atributos(self, obj, **kw):
            nombres_atributos = ""
            
            for a in obj.atributos:
                        nombres_atributos = nombres_atributos + ", " + a.nombre
            
            return nombres_atributos[1:]
    
    new_form_type = TipoItemRegistrationForm



"""configuraciones del modelo Atributo"""
"""atributo_form_validator =  Schema(chained_validators=(FieldsMatch('password',
                                                         'verify_password',
                                                         messages={'invalidNoMatch':
                                                         'Passwords do not match'}),))"""


from sprox.widgets import PropertySingleSelectField
class AtributoRegistrationForm(AddRecordForm):
    __model__ = Atributo
    __require_fields__ = ['cod_atributo', 'nombre','tipo_dato']
    __omit_fields__ = ['id_atributo']
    cod_atributo           = TextField
    nombre = TextField
    tipodatochoices = (("Cadena"),("Numerico"))
    
    
    tipo_dato = SingleSelectField
    #descripcion                 = TextArea
    
    


class AtributoCrudConfig(CrudRestControllerConfig):
    class table_type(TableBase):
        __entity__ =  Atributo
        __limit_fields__ = ['cod_atributo', 'nombre','descripcion', 'tipo_dato']
        __url__ = '../atributo.json' #this just tidies up the URL a bit

    class table_filler_type(TableFiller):
        __entity__ = Atributo
        __limit_fields__ = ['id_atributo','cod_atributo', 'nombre','descripcion', 'tipo_dato']
        
    
    
    class defaultCrudRestController(CrudRestController):
        
        
            
        @without_trailing_slash
        @expose('proyectosaptg.templates.new_atributo')
        def new(self, *args, **kw):
            """Display a page to show a new record."""
            
            
            tipos = ["Cadena","Numerico","Fecha"]
            
            tmpl_context.widget = self.new_form
            
            retorno = dict(value=kw, model=self.model.__name__, tipo_dato_options = tipos)
            
            return retorno
    
    
    
    
    
    new_form_type = AtributoRegistrationForm



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
            
                       
            value =  '<div><div><a class="edit_link" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
            '</div><div>'\
            '<form method="POST" action="'+pklist+'" class="button-to">'\
            '<input type="hidden" name="_method" value="DELETE" />'\
            '<input class="delete-button" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" '\
            'style="background-color: transparent; float:left; border:0; color: #286571; display: inline; margin: 0; padding: 0;"/>'\
            '</form>'\
            '<a class="itmes_link" href="../items/?fid='+pklist+'">Items</a> '\
            '<a class="lineas_link" href="../lineabases/?fid='+pklist+'">Linea Base</a> '\
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



"""configuraciones del modelo Item"""
class ItemRegistrationForm(AddRecordForm):
    __model__ = Item
    __require_fields__ = ['cod_item', 'nombre','id_fase_fk']
    __omit_fields__ = ['id_item','version','total_peso', 'estado', 'relaciones','id_linea_base_fk', 
                    'relacion','linea_base']
    #__field_order__        = ['user_name', 'email_address', 'display_name', 'password', 'verify_password']
    #__base_validator__     = user_form_validator
    cod_item           = TextField
    nombre = TextField
    __dropdown_field_names__ = {'tipo_item':'nombre'}
    
    tipo_item = SingleSelectField
    
    
class ItemCrudConfig(CrudRestControllerConfig):
    class table_type(TableBase):
        __entity__ =  Item
        __limit_fields__ = ['cod_item', 'nombre','estado', 'version','peso','id_tipo_item_fk','id_linea_base_fk','relaciones']
        __url__ = '../item.json' #this just tidies up the URL a bit

    class table_filler_type(TableFiller):
        __entity__ = Item
        __limit_fields__ = ['cod_item', 'nombre','estado', 'version','peso','id_tipo_item_fk','id_linea_base_fk','relaciones']
    
     
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
            '<a class="valores_link" href="../valoress/?iid='+pklist+'">Atributos</a> '\
            '<a class="relacion_link" href="../relacions/?iid='+pklist+'">Relaciones</a>'\
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
        
    new_form_type = ItemRegistrationForm
    
    
    class defaultCrudRestController(CrudRestController):
        
        
        @with_trailing_slash
        @expose('proyectosaptg.templates.get_all_item')
        @expose('json')
        @paginate('value_list', items_per_page=7)
        def get_all(self, *args, **kw):
            
            #print "fase get_all"
            
            val = kw["fid"]
            
            
            #print kw
            #print args
            
            retorno =  CrudRestController.get_all(self, *args, **kw)
           
            retorno["fid"] = val 
            
            #print retorno
            
            return retorno
            
        @without_trailing_slash
        @expose('proyectosaptg.templates.new_item')
        def new(self, *args, **kw):
            """Display a page to show a new record."""
            print "new itme\n"
            
            """filtramos solo los Tipos de Items asociados al Proyecto"""
            id_fase = args[0]
            #traemos la fase de la BD
            fase = DBSession.query(Fase).filter_by(id_fase = id_fase).one()
            #obtenemos el id del Proyecto, traemos el Proyecto y sus Tipos de Items
            id_proyecto = fase.proyecto_id
            proyecto = DBSession.query(Proyecto).filter_by(id_proyecto = id_proyecto).one()
            tipo_items = proyecto.tipo_items
            #obtenemos lo id y los nombres de los tipos de items del Proyecto para enviarlos como las opciones 
            #disponibles
            id_tipo_items = []
            for tipo_item in tipo_items:
                id_tipo_items.append((tipo_item.id_tipo_item,tipo_item.nombre))
                
            print id_tipo_items    
            
            
            
            
            if len(args) > 0:
                print "entre en el if\n"
                kw['id_fase_fk'] = args[0]
                print kw
                print args
    
                
            
            tmpl_context.widget = self.new_form
            
            retorno = dict(value=kw, model=self.model.__name__)
            
            retorno["id_tipo_items"] = id_tipo_items
            
            return retorno
            
        
        
        @expose()
        @registered_validate(error_handler=new)
        def post(self, *args, **kw):
            
            print "post item:"
            print kw
            print args
            
            
            fid = kw["id_fase_fk"]
            #print kw["proyecto_id"]
            
            
            #kw['tipo_item']
            
            new_item = self.provider.create(self.model, params=kw)
            
            #generamos los campos para los valores de los atributos...
            atributos_new_item = new_item.tipo_item.atributos
            fk_item = new_item.id_item 
            for atributo in atributos_new_item:
                fk_atributo = atributo.id_atributo
                el_valor = {}
                el_valor['fk_atributo'] = fk_atributo
                el_valor['fk_item'] = fk_item
                el_valor['valor'] = "vacio"
                
                print el_valor
                self.provider.create(Valores, params=el_valor)
             
            path = '../?fid='+ str(fid)
            
            print path
            
            raise redirect(path)


        @expose()
        def post_delete(self, *args, **kw):
            """This is the code that actually deletes the record"""
            
            #obtenemos el id de la fase para hacer el filtrado despues de la redireccion
            item_to_del = DBSession.query(Item).filter_by(id_item=args[0]).one()
            fid = item_to_del.id_fase_fk
            
            
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
    
    
        
        


    




"""configuraciones del modelo Valores"""
class ValoresRegistrationForm(AddRecordForm):
    __model__ = Valores
    __require_fields__ = ['fk_atributo', 'fk_item','valor']
    __omit_fields__ = ['id_valor']
   
    #__field_order__        = ['user_name', 'email_address', 'display_name', 'password', 'verify_password']
    #__base_validator__     = user_form_validator
    #cod_item           = TextField
    #nombre = TextField
    #__dropdown_field_names__ = {'tipo_item':'nombre'}


class ValoresCrudConfig(CrudRestControllerConfig):
    class table_type(TableBase):
        __entity__ =  Valores
        __limit_fields__ = ['fk_atributo', 'fk_item','valor']
        __url__ = '../valores.json' #this just tidies up the URL a bit
       


    class table_filler_type(TableFiller):
        __entity__ = Valores
        __limit_fields__ = ['fk_atributo', 'fk_item','valor']
            
        def fk_atributo(self, obj, **kw):
            atributo = DBSession.query(Atributo).filter_by(id_atributo=obj.fk_atributo).one()
            return atributo.nombre

        def fk_item(self, obj, **kw):
            item = DBSession.query(Item).filter_by(id_item=obj.fk_item).one()
            return item.nombre
    
    class edit_form_type(EditableForm):
        __entity__ = Valores
        __require_fields__     = ['valor']
        __omit_fields__        = ['id_valor']
               
        
        def _do_get_disabled_fields(self):
            fields = self.__disable_fields__[:]
            fields.append(self.__provider__.get_primary_field(self.__entity__))
            print fields
            fields.append("fk_atributo")
            fields.append("fk_item")
            return fields
        
        
    class edit_filler_type(EditFormFiller):
        __entity__ = Valores
        
        def fk_atributo(self, obj,**kw):    
            atributo_nombre = DBSession.query(Atributo.nombre).filter_by(id_atributo = obj.fk_atributo).one()
            print atributo_nombre
            return str(atributo_nombre[0])
        
        def fk_item(self, obj,**kw):  
            item_nombre = DBSession.query(Item.nombre).filter_by(id_item = obj.fk_item).one()
           
            return str(item_nombre[0])
        
    
    
    
    new_form_type = ValoresRegistrationForm





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
            #print kw["proyecto_id"]
            
            
            #kw['tipo_item']
            
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




"""configuraciones del modelo Relacion"""
class RelacionRegistrationForm(AddRecordForm):
    __model__ = Relacion
    __require_fields__ = ['cod_relacion', 'descripcion']
    __omit_fields__ = ['id_relacion', 'estado']
    cod_relacion           = TextField
    descripcion            = TextArea
    
class RelacionCrudConfig(CrudRestControllerConfig):
    class table_type(TableBase):
        __entity__ = Relacion
        __limit_fields__ = ['cod_relacion', 'descripcion','estado',]
        __url__ = '../relacion.json' #this just tidies up the URL a bit

    class table_filler_type(TableFiller):
        __entity__ = Relacion
        __limit_fields__ = ['id_relacion','cod_relacion', 'descripcion','estado']
        
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
            '<a class="fases_link" href="../relaciones/?pid='+pklist+'">Relacion</a>'\
            '</div></div>'
            
            return value
            
            
	def _do_get_provider_count_and_objs(self, **kw):
            
            limit = kw.get('limit', None)
            offset = kw.get('offset', None)
            order_by = kw.get('order_by', None)
            desc = kw.get('desc', False)
            if len(kw) > 0:
                objs = DBSession.query(self.__entity__).filter_by(item_origen_fk=kw['iid']).all()
            else:
                objs = DBSession.query(self.__entity__).all()
                
            count = len(objs)
            self.__count__ = count
            return count, objs    
            

    class defaultCrudRestController(CrudRestController):
        @with_trailing_slash
        @expose('proyectosaptg.templates.get_all')
        @expose('json')
        @paginate('value_list', items_per_page=7)
        def get_all(self, *args, **kw):
            return CrudRestController.get_all(self, *args, **kw)
      
    new_form_type = RelacionRegistrationForm


    
    

#instancimos todas nuestras configuraciones
class MyAdminConfig(AdminConfig):
      
    #DefaultControllerConfig    = MyCrudRestControllerConfig  
    
    user = UserCrudConfig
    proyecto = ProyectoCrudConfig
    tipoitem = TipoItemCrudConfig
    atributo = AtributoCrudConfig
    fase = FaseCrudConfig
    item = ItemCrudConfig
    valores = ValoresCrudConfig
    lineabase = LineaBaseCrudConfig
    relacion = RelacionCrudConfig
   
    
   