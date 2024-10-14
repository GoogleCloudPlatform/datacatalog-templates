#!/usr/bin/python
#
# Copyright 2024 Google LLC
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
from google.cloud import dataplex
from google.cloud.dataplex import CatalogServiceClient

"""
Args:
    project_id: The Google Cloud project ID to use 
    region: The Google Cloud region in which to create the aspect type
    yaml_file: path to the yaml file containing the aspect type specification
Returns:
    None; the response from the API is printed to the terminal.
"""

def main(project_id, region, yaml_file):
    
    dp_client = CatalogServiceClient()
    aspect_type = dataplex.AspectType()
    
    parent = f"projects/{project_id}/locations/{region}"
    record_fields = []
    
    with open(yaml_file) as file:
        file_contents = yaml.full_load(file)
        aspect_type_contents = file_contents.get("aspect_type")[0]

        for k, v in aspect_type_contents.items():
            #print(k + "->" + str(v))
            if k == 'name': 
                aspect_type_id = v
            if k == 'display_name':
                aspect_type.display_name = v
            if k == 'fields':
                fields = v
                
                for field in fields:
                    field_id = None
                    datatype = None
                    enum_values = None
                    display_name = None
                    description = None
                    required = False
                    
                    for fname, fval in field.items():
                        if fname == "values":
                            fval = fval.replace(' ', '_')
                            
                        #print(fname + "->" + str(fval))
                        if fname == "field":
                            field_id = fval
                        if fname == "type":
                            datatype = fval
                        if fname == "values":
                            enum_values = fval
                        if fname == "display":
                            display = fval
                        if fname == "description":
                            description = fval
                        if fname == "required":
                            required = fval
                        if fname == "order":
                            order = fval
                   
                    aspect_field = {"name": field_id, "type_": datatype.lower()}
                    
                    if order:
                        aspect_field["index"] = order
                    
                    if required:
                        aspect_field["constraints"] = {"required": True}
                        
                    if display:
                        annotations_dict = {"display_name": display}
                        
                        if description:
                            annotations_dict["description"] = description
                        
                        if order:
                            annotations_dict["display_order"] = order
                        
                        aspect_field["annotations"] = annotations_dict
                    
                    if datatype.lower() == "enum":
                        enum_list = enum_values.split("|")
                        enum_values = []
                        
                        for index, value in enumerate(enum_list):
                            index += 1
                            enum_value = {"name": value, "index": index}
                            enum_values.append(enum_value)
                        
                        aspect_field['enum_values'] = enum_values

                    record_fields.append(aspect_field)
                                                        
        #print('record_fields:', record_fields)
        
        aspect_type.metadata_template.name = aspect_type_id
        aspect_type.metadata_template.type_ = "record"
        aspect_type.metadata_template.record_fields = record_fields

        print('aspect_type:', aspect_type)
        
        request = dataplex.CreateAspectTypeRequest(
            parent=parent,
            aspect_type_id=aspect_type_id,
            aspect_type=aspect_type
        )

        try:
            operation = dp_client.create_aspect_type(request=request)
            response = operation.result()
            print('response:', response)
            
        except Exception as e:
            print("Error occurred while creating your aspect type:", e) 
                    
                                              
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Creates a Dataplex aspect type based on a yaml file specification.")
    parser.add_argument('project_id', help='The Google Cloud Project ID in which to create the tag template.')
    parser.add_argument('region', help='The Google Cloud region in which to create the tag template.')
    parser.add_argument('yaml_file', help='Path to your yaml file containing the template specification.')
    args = parser.parse_args()
    main(args.project_id, args.region, args.yaml_file)
    
