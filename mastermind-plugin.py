import json
import jsonschema
import yaml
import requests

from wstore.asset_manager.resource_plugins.plugin import Plugin


class MastermindPlugin(Plugin):

    _yaml_validator = json.load(open("mastermind-schema.json"))

    def _validate(self, yml, validator):
        errors = sorted(jsonschema.Draft4Validator(validator).iter_errors(yaml.load(yml)), key=lambda e: e.path)
        return [x.message for x in errors]

    def on_post_product_offering_validation(self, provider, asset):
        mastermind = asset.meta_info['configuration_template']
        err_list = self._validate(mastermind, self._yaml_validator)

        if len(err_list):
            raise ValueError(' '.join(err_list))

    def on_post_product_spec_attachment(self, asset, asset_t, product_spec):
        url = asset.meta_info.get('url')
        headers = {'content-type': 'application/json'}
        if not url:
            raise ValueError("URL must be specified")

        requests.put(url, json=product_spec, headers=headers)
