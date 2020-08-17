## datacatalog-templates

This repository contains sample Tag Templates in yaml-format and a [`create_template.py`](create_template.py) script that takes as input the yaml-formatted template and creates an actual Tag Template in Google Cloud's Data Catalog service. 


## Dependencies

Before running create_template.py, please install the pyyaml and google-cloud-datacatalog modules as follows:

```
pip install pyyaml
pip install google-cloud-datacatalog
```

## Running the Script

```
export GOOGLE_APPLICATION_CREDENTIALS='my_keyfile.json'
export PROJECT='my-project-id'
export REGION='us'
export TEMPLATE='dg_template.yaml'

python create_template.py $GOOGLE_APPLICATION_CREDENTIALS $PROJECT $REGION $TEMPLATE
```

## Contributing

See the contributing [instructions](/CONTRIBUTING.md) to get started
contributing.


## License

All solutions within this repository are provided under the
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) license. Please see
the [LICENSE](/LICENSE) file for more detailed terms and conditions.


## Disclaimer

This repository and its contents are not an official Google Product.