# Copyright 2019 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# [START generate_dag]

from jinja2 import Environment, FileSystemLoader
import os
import json
import argparse
from colorama import Fore, Back, Style, init
init(autoreset=True)

config_json = ''
template_name = ''
def main():
    parser = argparse.ArgumentParser(description= \
        '''This application downloads CCDA files from GCS, 
        parses them using bluebutton.js library
        and uploads the parsed content to BigQuery.''')

    parser.add_argument('-config_json', 
                    required=True,
                    help='''Provide DAG configuration json file location
                    e.g. ./config.json''')
    parser.add_argument('-template_name', 
                        required=True,
                        help='''Provide template name to use
                                e.q. simple_dag.template''')
    options = parser.parse_args()
    global config_json, template_name

    config_json = options.config_json
    template_name = options.template_name
def process():

    f = open(config_json)
    config_data = json.load(f)

    file_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(file_dir))

    template = env.get_template(template_name)

    values = {}

    filename = os.path.join(file_dir, config_data['generated_file_name'])
    print(len(config_data['tasks']))
    print(config_data['tasks'][0]['task_type'])
    with open(filename, 'w') as fh:
        fh.write(template.render(
            config_data=config_data,
            **values
        ))

if __name__ == '__main__':
    main()
    process()

 # [END generate_dag]

