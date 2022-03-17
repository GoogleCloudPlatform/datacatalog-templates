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
from google.cloud.datacatalog import DataCatalogClient

"""
Args:
    project_id: The Google Cloud project id to use 
    region: The Google Cloud region in which to create the Tag Template
    yaml_file: path to the yaml file containing the template specification
Returns:
    None; the response from the API is printed to the terminal.
"""

def create_template(project_id, region, yaml_file):
    
    dc_client = DataCatalogClient()
    tag_template = datacatalog.TagTemplate()
    
    with open(yaml_file) as file:
        file_contents = yaml.full_load(file)
        template_contents = file_contents.get("template")[0]

        for k, v in template_contents.items():
            print(k + "->" + str(v))
    
            if k == 'name': 
                tag_template_id = v
            if k == 'display_name':
                tag_template.display_name = v
            if k == 'fields':
                fields = v
                
                for field in fields:
                    
                    field_id = None
                    datatype = None
                    enum_values = None
                    display_name = None
                    required = False
                    
                    for fname, fval in field.items():
                        print(fname + "->" + str(fval))
                    
                        if fname == "field":
                            field_id = fval
                        if fname == "type":
                            datatype = fval
                        if fname == "values":
                            enum_values = fval
                        if fname == "display":
                            display = fval
                        if fname == "required":
                            required = fval
                        if fname == "order":
                            order = fval
                   
                    if datatype.lower() == "enum":
                        
                        field = datacatalog.TagTemplateField()
                        enum_list = enum_values.split("|")
                        
                        for value in enum_list:
                            enum_value = datacatalog.FieldType.EnumType.EnumValue()
                            enum_value.display_name = value
                            field.type_.enum_type.allowed_values.append(enum_value)
                            
                            field.display_name = display
                            field.is_required = required
                            field.order = order
                            tag_template.fields[field_id] = field
                            
                    elif datatype.lower() == "bool":
                        
                        field = datacatalog.TagTemplateField()
                        field.type_.primitive_type = datacatalog.FieldType.PrimitiveType.BOOL
                        field.display_name = display
                        field.is_required = required
                        field.order = order
                        tag_template.fields[field_id] = field
                    
                    elif datatype.lower() == "string":
                        
                        field = datacatalog.TagTemplateField()
                        field.type_.primitive_type = datacatalog.FieldType.PrimitiveType.STRING
                        field.display_name = display
                        field.is_required = required
                        field.order = order
                        tag_template.fields[field_id] = field
                    
                    elif datatype.lower() == "double":
                        
                        field = datacatalog.TagTemplateField()
                        field.type_.primitive_type = datacatalog.FieldType.PrimitiveType.DOUBLE
                        field.display_name = display
                        field.is_required = required
                        field.order = order
                        tag_template.fields[field_id] = field
                    
                    elif datatype.lower() in ("timestamp", "datetime"):
                        
                        field = datacatalog.TagTemplateField()
                        field.type_.primitive_type = datacatalog.FieldType.PrimitiveType.TIMESTAMP
                        field.display_name = display
                        field.is_required = required
                        field.order = order
                        tag_template.fields[field_id] = field
                    
        created_tag_template = dc_client.create_tag_template(parent=f'projects/{project_id}/locations/{region}', tag_template_id=tag_template_id, tag_template=tag_template)               
                        
        return created_tag_template
                        
                        
                        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="creates a Data Catalog Tag Template based on a yaml file specification.")
    parser.add_argument('project_id', help='Your Google Cloud Project ID.')
    parser.add_argument('region', help='The Google Cloud region in which to create the Tag Template.')
    parser.add_argument('yaml_file', help='Path to your yaml file containing the template specification.')
    args = parser.parse_args()
    create_template(args.project_id, args.region, args.yaml_file)
   
