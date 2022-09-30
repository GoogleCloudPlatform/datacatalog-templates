#!/usr/bin/python
#
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import yaml
from google.cloud import datacatalog
from google.cloud import datacatalog_v1
from google.cloud.datacatalog import DataCatalogClient

dc_client = DataCatalogClient()

# status codes
OK = 0
ERROR = -1

def update_enum_field(project_id, region, tag_template_id, field_id, display_name, description, enum_values, is_required, order):
    
    tag_template_field = datacatalog.TagTemplateField()
    
    for value in enum_values:
        enum_value = datacatalog.FieldType.EnumType.EnumValue()
        enum_value.display_name = value
        tag_template_field.type_.enum_type.allowed_values.append(enum_value)
    
    if display_name:
        tag_template_field.display_name = display_name
    
    if is_required:
        tag_template_field.is_required = is_required
    
    if order:
        tag_template_field.order = order
       
    if description:
        tag_template_field.description = description
           
    request = datacatalog.UpdateTagTemplateFieldRequest(
        name='projects/{0}/locations/{1}/tagTemplates/{2}/fields/{3}'.format(project_id, region, tag_template_id, field_id),
        tag_template_field=tag_template_field
    )

    try:
        response = dc_client.update_tag_template_field(request=request)
        print('Done.')
    except Exception as e:
        print('Error: Cannot update enum ' + field_id + '. Error message: ' + str(e))
        return OK
        
    return ERROR
    

def add_enum_field(project_id, region, tag_template_id, field_id, display_name, description, enum_values, is_required, order):
    
    tag_template_field = datacatalog.TagTemplateField()

    for value in enum_values:
        enum_value = datacatalog.FieldType.EnumType.EnumValue()
        enum_value.display_name = value
        tag_template_field.type_.enum_type.allowed_values.append(enum_value)
        
    if display_name:
        tag_template_field.display_name = display_name
    
    if is_required:
        tag_template_field.is_required = is_required
    
    if order:
        tag_template_field.order = order
       
    if description:
        tag_template_field.description = description
           
    request = datacatalog.CreateTagTemplateFieldRequest(
        parent='projects/{0}/locations/{1}/tagTemplates/{2}'.format(project_id, region, tag_template_id),
        tag_template_field_id=field_id,
        tag_template_field=tag_template_field
    )

    try:
        response = dc_client.create_tag_template_field(request=request)
        print('Done.')
    except Exception as e:
        print('Error: Cannot create field ' + field_id + '. Error message: ' + str(e))
        return ERROR
    
    #print('response: ', response)
    
    return OK


def update_primitive_field(project_id, region, tag_template_id, field_id, field_type, display_name, description, is_required, order):
    
    tag_template_field = datacatalog.TagTemplateField()
    tag_template_field.type_.primitive_type = field_type
    
    if display_name:
        tag_template_field.display_name = display_name
    
    if is_required:
        tag_template_field.is_required = is_required
    
    if order:
        tag_template_field.order = order
       
    if description:
        tag_template_field.description = description
            
    request = datacatalog.UpdateTagTemplateFieldRequest(
        name='projects/{0}/locations/{1}/tagTemplates/{2}/fields/{3}'.format(project_id, region, tag_template_id, field_id),
        tag_template_field=tag_template_field
    )
    
    try:
        response = dc_client.update_tag_template_field(request=request)
        print('Done.')
    except Exception as e:
        print('Error: Cannot update field ' + field_id + '. Error message: ' + str(e))
        return ERROR
        
    return OK


def add_primitive_field(project_id, region, tag_template_id, field_id, field_type, display_name, description, is_required, order):
    
    tag_template_field = datacatalog.TagTemplateField()
    tag_template_field.type_.primitive_type = field_type
    
    if display_name:
        tag_template_field.display_name = display_name
    
    if is_required:
        tag_template_field.is_required = is_required
    
    if order:
        tag_template_field.order = order
       
    if description:
        tag_template_field.description = description
            
    request = datacatalog.CreateTagTemplateFieldRequest(
        parent='projects/{0}/locations/{1}/tagTemplates/{2}'.format(project_id, region, tag_template_id),
        tag_template_field_id=field_id,
        tag_template_field=tag_template_field
    )

    try:
        response = dc_client.create_tag_template_field(request=request)
        print('Done.')
    except Exception as e:
        print('Error: Cannot create field ' + field_id + '. Error message: ' + str(e))
        return ERROR
    
    #print('response: ', response)
    
    return OK


def rename_field(project_id, region, tag_template_id, cur_field, new_field):
    
    tag_template_field = datacatalog.TagTemplateField()
            
    request = datacatalog.RenameTagTemplateFieldRequest(
        name='projects/{0}/locations/{1}/tagTemplates/{2}/fields/{3}'.format(project_id, region, tag_template_id, cur_field),
        new_tag_template_field_id=new_field
    )

    try:
        response = dc_client.rename_tag_template_field(request=request)
        print('Done.')
    except Exception as e:
        print('Error: Cannot rename field ' + cur_field + 'to ' + new_field + '. Error message: ' + str(e))
        return ERROR
    
    #print('response: ', response)
    
    return OK

def remove_field(project_id, region, tag_template_id, field_id):
    
    
    request = datacatalog_v1.DeleteTagTemplateFieldRequest(
        name='projects/{0}/locations/{1}/tagTemplates/{2}/fields/{3}'.format(project_id, region, tag_template_id, field_id),
        force=True
    )

    try:
        response = dc_client.delete_tag_template_field(request=request)
        print('Done.')
    except Exception as e:
        print('Error: Cannot delete field ' + field_id + '. Error message: ' + str(e))
        return ERROR
            
    return OK
    
        
def equivalent_enum_fields(dc_field, dc_enum_values, yaml_enum_values, yaml_display_name, yaml_description, yaml_is_required, yaml_order):
                              
    dc_field_type, dc_display_name, dc_is_required, dc_description, dc_order = dc_field
    
    #print('dc_enum_values: ', dc_enum_values)
    
    if dc_enum_values.sort() != yaml_enum_values.sort():
        return False
    
    if dc_display_name != yaml_display_name:
        return False
    
    if dc_description != yaml_description:
        return False
    
    if dc_is_required != yaml_is_required:
        return False
    
    if dc_order != yaml_order:
        return False
    
    return True
        

def equivalent_primitive_fields(dc_field, yaml_display_name, yaml_description, yaml_is_required, yaml_order):
    
    dc_field_type, dc_display_name, dc_is_required, dc_description, dc_order = dc_field
    
    if dc_display_name != yaml_display_name:
        return False
    
    if dc_description != yaml_description:
        return False
    
    if dc_is_required != yaml_is_required:
        return False
    
    if dc_order != yaml_order:
        return False
    
    return True
    

"""
Args:
    project_id: The Google Cloud project id to use 
    region: The Google Cloud region in which to create the Tag Template
    yaml_file: path to the yaml file containing the template specification
Returns:
    None; the response from the API is printed to the terminal.
"""
def evolve_template(mode, project_id, region, yaml_file):
    
    with open(yaml_file) as file:
        file_contents = yaml.full_load(file)
        template_contents = file_contents.get("template")[0]

        for k, v in template_contents.items():
            #print(k + "->" + str(v))
    
            if k == 'name': 
                tag_template_id = v
                template_path = DataCatalogClient.tag_template_path(project_id, region, tag_template_id)
                request = datacatalog.GetTagTemplateRequest(name=template_path)
                
                try:
                    tag_template = dc_client.get_tag_template(request)
                except Exception as e:
                    print('Error: Tag template ' + tag_template_id + ' does not exist in project ' + project_id + ' and region ' + region + '.')
                    print('Hint: To create a new tag template, run create_template.py.')
                    return -1
                
                dc_fields = {}
                dc_enum_values = {}
                
                for field_id, field_value in tag_template.fields.items():
                    
                    #print('field_id:', field_id)
                    #print('field_value', field_value)
                    
                    display_name = field_value.display_name
                    is_required = field_value.is_required
                    description = field_value.description
                    order = field_value.order
                        
                    if field_value.type_.primitive_type == datacatalog_v1.types.FieldType.PrimitiveType.PRIMITIVE_TYPE_UNSPECIFIED:
                        
                        field_type = 'enum'
                        allowed_values = field_value.type_.enum_type.allowed_values
                        
                        enum_value_list = []
                        
                        for allowed_value in allowed_values:
                            enum_value_list.append(allowed_value.display_name)
                        
                        dc_enum_values[field_id] = enum_value_list
                        
                    elif field_value.type_.primitive_type == datacatalog_v1.types.FieldType.PrimitiveType.STRING:
                        field_type = 'string'
                    elif field_value.type_.primitive_type == datacatalog_v1.types.FieldType.PrimitiveType.BOOL:
                        field_type = 'bool'
                    elif field_value.type_.primitive_type == datacatalog_v1.types.FieldType.PrimitiveType.DOUBLE:
                        field_type = 'double' 
                    elif field_value.type_.primitive_type == datacatalog_v1.types.FieldType.PrimitiveType.TIMESTAMP:
                        field_type = 'timestamp'
                    elif field_value.type_.primitive_type == datacatalog_v1.types.FieldType.PrimitiveType.RICHTEXT:
                        field_type = 'richtext'  
                    
                    field_attributes = (field_type, display_name, is_required, description, order)
                    dc_fields[field_id] = field_attributes
                
                #print('dc_fields: ', dc_fields)
                   
            if k == 'display_name':
                tag_template.display_name = v
            if k == 'public':
                tag_template.is_publicly_readable = v
            if k == 'fields':
                fields = v
                
                for field in fields:
                    
                    field_id = None
                    datatype = None
                    enum_values = None
                    display_name = None
                    description = None
                    is_required = False
                    order = None
                    
                    for fname, fval in field.items():
                        
                        if fname == "values":
                            fval = fval.replace(' ', '_')
                            
                        #print(fname + "->" + str(fval))
                    
                        if fname == "field":
                            field_id = fval
                        if fname == "type":
                            datatype = fval
                        if fname == "values":
                            enum_values = fval.split("|")
                        if fname == "display":
                            display_name = fval
                        if fname == "description":
                            description = fval
                        if fname == "required":
                            is_required = fval
                        if fname == "order":
                            order = fval
                   
                    if datatype.lower() == "enum":
                        
                        #print('dc_fields:', dc_fields)
                        #print('dc_enum_values:', dc_enum_values)
                        
                        # enum has not changed
                        if field_id in dc_fields and equivalent_enum_fields(dc_fields[field_id], dc_enum_values[field_id], \
                                                                            enum_values, display_name, description, is_required, order):
                        
                            # previous and new fields are equivalent
                            # remove entry from dictionary to signal that it has been processed
                            print('Field ' + field_id + ' (enum) has not changed.')
                            del dc_fields[field_id]
                        
                        # enum has changed
                        elif field_id in dc_fields and equivalent_enum_fields(dc_fields[field_id], dc_enum_values[field_id], enum_values, \
                                                                              display_name, description, is_required, order) == False:
                        
                            # yaml field is different from the current Data Catalog field
                            print('Update field ' + field_id + ' (enum) because it has changed.')
                    
                            if mode == 'apply':
                                update_enum_field(project_id, region, tag_template_id, field_id, display_name, description, enum_values, \
                                                  is_required, order) 
                                del dc_fields[field_id]
                        
                        # we either have a new enum or a renamed enum    
                        elif field_id not in dc_fields:
                            
                            if len(field_id.split(':')) > 1:
                                is_rename = True
                                cur_field = field_id.split(':')[0]
                                new_field = field_id.split(':')[1]
                                print('Rename ' + cur_field + ' (enum) to ' + new_field + '.')
                                
                                if mode == 'apply':
                                    rename_field(project_id, region, tag_template_id, cur_field, new_field)
                                    
                                if equivalent_enum_fields(dc_fields[cur_field], dc_enum_values[cur_field], enum_values, \
                                                          display_name, description, is_required, order) == False:    
                                 
                                    print('Update field ' + new_field + ' (enum) because it has changed.')
                                    
                                    # update enum
                                    if mode == 'apply':
                                        update_enum_field(project_id, region, tag_template_id, new_field, display_name, description, enum_values, \
                                                          is_required, order)
                                
                                del dc_fields[cur_field]
                                    
                            else:
                                # adding enum field
                                print('Add field ' + field_id + ' (enum) to the tag template.')
                            
                                if mode == 'apply':
                                    add_enum_field(project_id, region, tag_template_id, field_id, display_name, \
                                                    description, enum_values, is_required, order)
                                                   
                                        
                    elif datatype.lower() == "bool":
                        
                        # field is the same
                        if field_id in dc_fields and equivalent_primitive_fields(dc_fields[field_id], display_name, description, \
                                                                                    is_required, order):
                            # remove entry from dictionary to signal that it has been processed
                            print('Field ' + field_id + ' (bool) has not changed.')
                            del dc_fields[field_id]
                        
                        # field has changed
                        elif field_id in dc_fields and equivalent_primitive_fields(dc_fields[field_id], display_name, description, \
                                                                                    is_required, order) == False:
                            # yaml field is different from the current Data Catalog field
                            print('Update field ' + field_id + ' (bool) because it has changed.')
                            
                            if mode == 'apply':
                                update_primitive_field(project_id, region, tag_template_id, field_id, \
                                                        datacatalog_v1.types.FieldType.PrimitiveType.BOOL, \
                                                        display_name, description, is_required, order)
                            del dc_fields[field_id]
                        
                        # field is either new or renamed
                        elif field_id not in dc_fields:
                            
                            # field has been renamed
                            if len(field_id.split(':')) > 1:
                                is_rename = True
                                cur_field = field_id.split(':')[0]
                                new_field = field_id.split(':')[1]
                                print('Rename ' + cur_field + ' (bool) to ' + new_field + '.')
                                
                                if mode == 'apply':
                                    rename_field(project_id, region, tag_template_id, cur_field, new_field)
                                    
                                # field has additional changes
                                if equivalent_primitive_fields(dc_fields[cur_field], display_name, description, \
                                                                is_required, order) == False:
                                    
                                    print('Update field ' + new_field + ' (bool) because it has changed.')
                            
                                    if mode == 'apply':
                                        update_primitive_field(project_id, region, tag_template_id, new_field, \
                                                                datacatalog_v1.types.FieldType.PrimitiveType.BOOL, \
                                                                display_name, description, is_required, order)
                                    
                                del dc_fields[cur_field]
                            
                            # we have a new bool
                            else:
                                print('Add field ' + field_id + ' (bool) to the tag template.')
                                if mode == 'apply':
                                    add_primitive_field(project_id, region, tag_template_id, field_id, \
                                                         datacatalog.FieldType.PrimitiveType.BOOL, \
                                                         display_name, description, is_required, order)
                        
                        
  
                    elif datatype.lower() == "string":
                        
                        # field is the same
                        if field_id in dc_fields and equivalent_primitive_fields(dc_fields[field_id], display_name, description, \
                                                                                 is_required, order):
                            # remove entry from dictionary to signal that it has been processed
                            print('Field ' + field_id + ' (string) has not changed.')
                            del dc_fields[field_id]
                        
                        # field has changed
                        elif field_id in dc_fields and equivalent_primitive_fields(dc_fields[field_id], display_name, description, \
                                                                                    is_required, order) == False:
                            # yaml field is different from the current Data Catalog field
                            print('Update field ' + field_id + ' (string) because it has changed.')
                            
                            if mode == 'apply':
                                update_primitive_field(project_id, region, tag_template_id, field_id, \
                                                        datacatalog_v1.types.FieldType.PrimitiveType.STRING, \
                                                        display_name, description, is_required, order)
                            del dc_fields[field_id]
                        
                        # field is either new or renamed
                        elif field_id not in dc_fields:
                            
                            # field has been renamed
                            if len(field_id.split(':')) > 1:
                                is_rename = True
                                cur_field = field_id.split(':')[0]
                                new_field = field_id.split(':')[1]
                                print('Rename ' + cur_field + ' (string) to ' + new_field + '.')
                                
                                if mode == 'apply':
                                    rename_field(project_id, region, tag_template_id, cur_field, new_field)
                                    
                                # field has additional changes
                                if equivalent_primitive_fields(dc_fields[cur_field], display_name, description, \
                                                                is_required, order) == False:
                                    
                                    print('Update field ' + new_field + ' (string) because it has changed.')
                            
                                    if mode == 'apply':
                                        update_primitive_field(project_id, region, tag_template_id, new_field, \
                                                                datacatalog_v1.types.FieldType.PrimitiveType.STRING, \
                                                                display_name, description, is_required, order)
                                    
                                del dc_fields[cur_field]
                            
                            # we have a new string
                            else:
                                print('Add field ' + field_id + ' (string) to the tag template.')
                                if mode == 'apply':
                                    add_primitive_field(project_id, region, tag_template_id, field_id, \
                                                         datacatalog.FieldType.PrimitiveType.STRING, \
                                                         display_name, description, is_required, order)
                        
                    
                    elif datatype.lower() == "double":
                        
                        # field is the same
                        if field_id in dc_fields and equivalent_primitive_fields(dc_fields[field_id], display_name, description, \
                                                                                    is_required, order):
                            # remove entry from dictionary to signal that it has been processed
                            print('Field ' + field_id + ' (double) has not changed.')
                            del dc_fields[field_id]
                        
                        # field has changed
                        elif field_id in dc_fields and equivalent_primitive_fields(dc_fields[field_id], display_name, description, \
                                                                                    is_required, order) == False:
                            # yaml field is different from the current Data Catalog field
                            print('Update field ' + field_id + ' (double) because it has changed.')
                            
                            if mode == 'apply':
                                update_primitive_field(project_id, region, tag_template_id, field_id, \
                                                        datacatalog_v1.types.FieldType.PrimitiveType.DOUBLE, \
                                                        display_name, description, is_required, order)
                            del dc_fields[field_id]
                        
                        # field is either new or renamed
                        elif field_id not in dc_fields:
                            
                            # field has been renamed
                            if len(field_id.split(':')) > 1:
                                is_rename = True
                                cur_field = field_id.split(':')[0]
                                new_field = field_id.split(':')[1]
                                print('Rename ' + cur_field + ' (double) to ' + new_field + '.')
                                
                                if mode == 'apply':
                                    rename_field(project_id, region, tag_template_id, cur_field, new_field)
                                    
                                # field has additional changes
                                if equivalent_primitive_fields(dc_fields[cur_field], display_name, description, \
                                                                is_required, order) == False:
                                    
                                    print('Update field ' + new_field + ' (double) because it has changed.')
                            
                                    if mode == 'apply':
                                        update_primitive_field(project_id, region, tag_template_id, new_field, \
                                                                datacatalog_v1.types.FieldType.PrimitiveType.DOUBLE, \
                                                                display_name, description, is_required, order)
                                    
                                del dc_fields[cur_field]
                            
                            # we have a new double
                            else:
                                print('Add field ' + field_id + ' (double) to the tag template.')
                                if mode == 'apply':
                                    add_primitive_field(project_id, region, tag_template_id, field_id, \
                                                         datacatalog.FieldType.PrimitiveType.DOUBLE, \
                                                         display_name, description, is_required, order)
                        

                    
                    elif datatype.lower() in ("timestamp", "datetime"):
                        
                        # field is the same
                        if field_id in dc_fields and equivalent_primitive_fields(dc_fields[field_id], display_name, description, \
                                                                                    is_required, order):
                            # remove entry from dictionary to signal that it has been processed
                            print('Field ' + field_id + ' (timestamp) has not changed.')
                            del dc_fields[field_id]
                        
                        # field has changed
                        elif field_id in dc_fields and equivalent_primitive_fields(dc_fields[field_id], display_name, description, \
                                                                                    is_required, order) == False:
                            # yaml field is different from the current Data Catalog field
                            print('Update field ' + field_id + ' (timestamp) because it has changed.')
                            
                            if mode == 'apply':
                                update_primitive_field(project_id, region, tag_template_id, field_id, \
                                                        datacatalog_v1.types.FieldType.PrimitiveType.TIMESTAMP, \
                                                        display_name, description, is_required, order)
                            del dc_fields[field_id]
                        
                        # field is either new or renamed
                        elif field_id not in dc_fields:
                            
                            # field has been renamed
                            if len(field_id.split(':')) > 1:
                                is_rename = True
                                cur_field = field_id.split(':')[0]
                                new_field = field_id.split(':')[1]
                                print('Rename ' + cur_field + ' (timestamp) to ' + new_field + '.')
                                
                                if mode == 'apply':
                                    rename_field(project_id, region, tag_template_id, cur_field, new_field)
                                    
                                # field has additional changes
                                if equivalent_primitive_fields(dc_fields[cur_field], display_name, description, \
                                                                is_required, order) == False:
                                    
                                    print('Update field ' + new_field + ' (timestamp) because it has changed.')
                            
                                    if mode == 'apply':
                                        update_primitive_field(project_id, region, tag_template_id, new_field, \
                                                                datacatalog_v1.types.FieldType.PrimitiveType.TIMESTAMP, \
                                                                display_name, description, is_required, order)
                                    
                                del dc_fields[cur_field]
                            
                            # we have a new timestamp
                            else:
                                print('Add field ' + field_id + ' (bool) to the tag template.')
                                if mode == 'apply':
                                    add_primitive_field(project_id, region, tag_template_id, field_id, \
                                                         datacatalog.FieldType.PrimitiveType.TIMESTAMP, \
                                                         display_name, description, is_required, order)
                        
                    
                    elif datatype.lower() == "richtext":
                        
                        # field is the same
                        if field_id in dc_fields and equivalent_primitive_fields(dc_fields[field_id], display_name, description, \
                                                                                 is_required, order):
                            # remove entry from dictionary to signal that it has been processed
                            print('Field ' + field_id + ' (richtext) has not changed.')
                            del dc_fields[field_id]
                        
                        # field has changed
                        elif field_id in dc_fields and equivalent_primitive_fields(dc_fields[field_id], display_name, description, \
                                                                                    is_required, order) == False:
                            # yaml field is different from the current Data Catalog field
                            print('Update field ' + field_id + ' (richtext) because it has changed.')
                            
                            if mode == 'apply':
                                update_primitive_field(project_id, region, tag_template_id, field_id, \
                                                        datacatalog_v1.types.FieldType.PrimitiveType.RICHTEXT, \
                                                        display_name, description, is_required, order)
                            del dc_fields[field_id]
                        
                        # field is either new or renamed
                        elif field_id not in dc_fields:
                            
                            # field has been renamed
                            if len(field_id.split(':')) > 1:
                                is_rename = True
                                cur_field = field_id.split(':')[0]
                                new_field = field_id.split(':')[1]
                                print('Rename ' + cur_field + ' (richtext) to ' + new_field + '.')
                                
                                if mode == 'apply':
                                    rename_field(project_id, region, tag_template_id, cur_field, new_field)
                                    
                                # field has additional changes
                                if equivalent_primitive_fields(dc_fields[cur_field], display_name, description, \
                                                                is_required, order) == False:
                                    
                                    print('Update field ' + new_field + ' (richtext) because it has changed.')
                            
                                    if mode == 'apply':
                                        update_primitive_field(project_id, region, tag_template_id, new_field, \
                                                                datacatalog_v1.types.FieldType.PrimitiveType.RICHTEXT, \
                                                                display_name, description, is_required, order)
                                    
                                del dc_fields[cur_field]
                            
                            # we have a new richtext
                            else:
                                print('Add field ' + field_id + ' (richtext) to the tag template.')
                                if mode == 'apply':
                                    add_primitive_field(project_id, region, tag_template_id, field_id, \
                                                         datacatalog.FieldType.PrimitiveType.RICHTEXT, \
                                                         display_name, description, is_required, order)
                        

                    
        # finished processing the yaml
        # remove any fields remaining in dc_fields from the tag template
        for field_id, field_attributes in dc_fields.items():
            print('Remove field ' + field_id + ' (' + field_attributes[0] + ') from the tag template.')
            
            if mode == 'apply':
                remove_field(project_id, region, tag_template_id, field_id)
            
                            
                       
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Evolves a Data Catalog tag template based on a yaml file specification.')
    parser.add_argument('mode', help='Runs the script in either "validate" or "apply" mode.')
    parser.add_argument('project_id', help='The Google Cloud Project ID in which your tag template resides.')
    parser.add_argument('region', help='The Google Cloud region in which your tag template resides.')
    parser.add_argument('yaml_file', help='The path to your yaml file containing the tag template specification.')
    args = parser.parse_args()
    
    if args.mode != 'validate' and args.mode != 'apply':
        print('Input error: mode must be either "validate" or "apply"')
    else:
        print('Info: you are running in ' + args.mode + ' mode.')
        evolve_template(args.mode, args.project_id, args.region, args.yaml_file)
   
