#!/usr/bin/python
#
# Copyright 2020 Google LLC
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
from google.cloud.datacatalog import DataCatalogClient, enums, types

"""
Args:
    key_file: The json key file to use
    project_id: The Google Cloud project id to use 
    region: The Google Cloud region in which to create the Tag Template
    yaml_file: path to the yaml file containing the template specification
Returns:
    None; the response from the API is printed to the terminal.
"""

def create_template(key_file, project_id, region, yaml_file):
    
    datacatalog_client = DataCatalogClient.from_service_account_file(key_file)
    location = DataCatalogClient.location_path(project_id, region)
    template_instance = types.TagTemplate()
    
    with open(yaml_file) as file:
        file_contents = yaml.full_load(file)
        template_contents = file_contents.get("template")[0]

        for k, v in template_contents.items():
            print(k + "->" + str(v))
    
            if k == 'name': 
                template_id = v
            if k == 'display_name':
                template_instance.display_name = v
            if k == 'fields':
                fields = v
                
                for field in fields:
                    
                    field_name = None
                    datatype = None
                    enum_values = None
                    display_name = None
                    required = False
                    
                    for fname, fval in field.items():
                        print(fname + "->" + str(fval))
                    
                        if fname == "field":
                            field = fval
                        if fname == "type":
                            datatype = fval
                        if fname == "values":
                            enum_values = fval
                        if fname == "display":
                            display = fval
                        if fname == "required":
                            required = fval
                            
                    
                    if datatype.lower() == "enum":
                        
                        enum_list = enum_values.split("|")
                        
                        for enum_value in enum_list:
                            template_instance.fields[field].type.enum_type.allowed_values.add().display_name = enum_value
                            template_instance.fields[field].display_name = display
                            template_instance.fields[field].is_required = required
                    
                    elif datatype.lower() == "bool":
                        
                        template_instance.fields[field].type.primitive_type = enums.FieldType.PrimitiveType.BOOL
                        template_instance.fields[field].display_name = display
                        template_instance.fields[field].is_required = required
                    
                    elif datatype.lower() == "string":
                        
                        template_instance.fields[field].type.primitive_type = enums.FieldType.PrimitiveType.STRING
                        template_instance.fields[field].display_name = display
                        template_instance.fields[field].is_required = required
                    
                    elif datatype.lower() == "double":
                        
                        template_instance.fields[field].type.primitive_type = enums.FieldType.PrimitiveType.DOUBLE
                        template_instance.fields[field].display_name = display
                        template_instance.fields[field].is_required = required
                    
                    elif datatype.lower() == "timestamp":
                        
                        template_instance.fields[field].type.primitive_type = enums.FieldType.PrimitiveType.TIMESTAMP
                        template_instance.fields[field].display_name = display
                        template_instance.fields[field].is_required = required
                    
        datacatalog_client.create_tag_template(parent=location, tag_template_id=template_id, tag_template=template_instance)
                        
                        
                        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="creates a Data Catalog Tag Template based on a yaml file specification.")
    parser.add_argument('key_file', help='Path to your .json credential file.')
    parser.add_argument('project_id', help='Your Google Cloud Project ID.')
    parser.add_argument('region', help='The Google Cloud region in which to create the Tag Template.')
    parser.add_argument('yaml_file', help='Path to your yaml file containing the template specification.')
    args = parser.parse_args()
    create_template(args.key_file, args.project_id, args.region, args.yaml_file)
   