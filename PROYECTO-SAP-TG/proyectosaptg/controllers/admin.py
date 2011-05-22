from tgext.admin.config import AdminConfig, CrudRestControllerConfig
from sprox.formbase import AddRecordForm
from formencode import Schema
from formencode.validators import FieldsMatch
from tw.forms import PasswordField, TextField


from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller


from proyectosaptg.model import *




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
    
    #class NewForm():
     #   pass
       # ___fields__ = ['_password', 'groups', 'created', 'user_id', 'town_id','proyectos']
        
    
    
    new_form_type = UserRegistrationForm






"""configuraciones del modelo Proyecto"""
"""proyecto_form_validator =  Schema(chained_validators=(FieldsMatch('password',
                                                         'verify_password',
                                                         messages={'invalidNoMatch':
                                                         'Passwords do not match'}),))"""
class ProyectoRegistrationForm(AddRecordForm):
    __model__ = Proyecto
    __require_fields__ = ['cod_proyecto', 'nombre']
    __omit_fields__ = ['id_proyecto', 'estado','fecha_creacion' ,'fecha_inicio', 'fecha_finalizacion_anulacion']
    #__field_order__        = ['user_name', 'email_address', 'display_name', 'password', 'verify_password']
    #__base_validator__     = user_form_validator
    cod_proyecto           = TextField
    nombre                 = TextField
    
    

class ProyectoCrudConfig(CrudRestControllerConfig):
    class table_type(TableBase):
        __entity__ = Proyecto
        __limit_fields__ = ['cod_proyecto', 'nombre','estado', 'fecha_creacion','fecha_inicio', 'fecha_finalizacion_anulacion']
        __url__ = '../proyecto.json' #this just tidies up the URL a bit

    class table_filler_type(TableFiller):
        __entity__ = Proyecto
        __limit_fields__ = ['id_proyecto','cod_proyecto', 'nombre','estado',    'fecha_creacion', 'fecha_inicio', 'fecha_finalizacion_anulacion']
    new_form_type = ProyectoRegistrationForm





"""configuraciones del modelo TipoItem"""
"""tipo_item_form_validator =  Schema(chained_validators=(FieldsMatch('password',
                                                         'verify_password',
                                                         messages={'invalidNoMatch':
                                                         'Passwords do not match'}),))"""
class TipoItemRegistrationForm(AddRecordForm):
    __model__ = TipoItem
    __require_fields__ = ['cod_tipo_item', 'descripcion']
    __omit_fields__ = ['id_tipo_item']
    #__field_order__        = ['user_name', 'email_address', 'display_name', 'password', 'verify_password']
    #__base_validator__     = user_form_validator
    cod_tipo_item           = TextField
    #descripcion                 = TextArea
    
    

class TipoItemCrudConfig(CrudRestControllerConfig):
    class table_type(TableBase):
        __entity__ =  TipoItem
        __limit_fields__ = ['cod_tipo_item', 'descripcion','atributos']
        __url__ = '../tipoitem.json' #this just tidies up the URL a bit

    class table_filler_type(TableFiller):
        __entity__ = TipoItem
        __limit_fields__ = ['id_tipo_item','cod_tipo_item', 'descripcion','atributos']
    new_form_type = TipoItemRegistrationForm



"""configuraciones del modelo Atributo"""
"""atributo_form_validator =  Schema(chained_validators=(FieldsMatch('password',
                                                         'verify_password',
                                                         messages={'invalidNoMatch':
                                                         'Passwords do not match'}),))"""
class AtributoRegistrationForm(AddRecordForm):
    __model__ = Atributo
    __require_fields__ = ['cod_atributo', 'nombre','tipo_dato']
    __omit_fields__ = ['id_atributo',]
    #__field_order__        = ['user_name', 'email_address', 'display_name', 'password', 'verify_password']
    #__base_validator__     = user_form_validator
    cod_atributo           = TextField
    nombre = TextField
    tipo_dato = TextField
    #descripcion                 = TextArea
    
    


class AtributoCrudConfig(CrudRestControllerConfig):
    class table_type(TableBase):
        __entity__ =  Atributo
        __limit_fields__ = ['cod_atributo', 'nombre','descripcion', 'tipo_dato']
        __url__ = '../atributo.json' #this just tidies up the URL a bit

    class table_filler_type(TableFiller):
        __entity__ = Atributo
        __limit_fields__ = ['id_atributo','cod_atributo', 'nombre','descripcion', 'tipo_dato']
    new_form_type = AtributoRegistrationForm



"""configuraciones del modelo Fase"""
class FaseRegistrationForm(AddRecordForm):
    __model__ = Fase
    __require_fields__ = ['cod_fase', 'nombre']
    __omit_fields__ = ['id_fase','estado','lineas_bases']
    #__field_order__        = ['user_name', 'email_address', 'display_name', 'password', 'verify_password']
    #__base_validator__     = user_form_validator
    cod_fase           = TextField
    nombre = TextField
    #descripcion                 = TextArea
    
    


class FaseCrudConfig(CrudRestControllerConfig):
    class table_type(TableBase):
        __entity__ =  Fase
        __limit_fields__ = ['cod_fase', 'nombre','estado', 'items','lineas_bases']
        __url__ = '../fase.json' #this just tidies up the URL a bit

    class table_filler_type(TableFiller):
        __entity__ = Fase
        __limit_fields__ = ['id_fase','cod_fase', 'nombre','estado', 'items','lineas_bases']
    new_form_type = FaseRegistrationForm




#instancimos todas nuestras configuraciones
class MyAdminConfig(AdminConfig):
    user = UserCrudConfig
    proyecto = ProyectoCrudConfig
    tipoitem = TipoItemCrudConfig
    atributo = AtributoCrudConfig
    fase = FaseCrudConfig