import json
import jsonschema
import yaml
import requests
# import ipdb

from wstore.asset_manager.resource_plugins.plugin import Plugin
from django.conf import settings


class MastermindPlugin(Plugin):

    _yaml_validator = json.load(open("mastermind-schema.json"))
    _headers = {'content-type': 'application/json'}

    def _validate(self, yml, validator):
        errors = sorted(jsonschema.Draft4Validator(validator).iter_errors(yaml.load(yml)), key=lambda e: e.path)
        return [str(x.message) for x in errors]

    def _send_request(self, asset, mm_url, headers):

        if not mm_url:
            raise ValueError("URL must be specified")
        try:
            mm_req = requests.post(mm_url, json=asset.meta_info, headers=headers)

        except requests.ConnectionError:
            raise ValueError("URL not found: " + mm_url)

        if mm_req.status_code != 201:
            raise ValueError("URL did not accept the request: " + mm_url)

        if not mm_url.endswith("/"):
            mm_url += "/"

        asset.download_link = mm_url + str(mm_req.json().get('id'))

    def on_post_product_spec_validation(self, provider, asset):

        mastermind = asset.meta_info['configuration_template']
        err_list = self._validate(mastermind, self._yaml_validator)

        if len(err_list):
            raise ValueError("Found errors in mastermind.yml: "' '.join(err_list))

        self._send_request(asset, asset.get_url(), self._headers)

    def on_pre_product_spec_attachment(self, asset, asset_t, product_spec):
        url = settings.CATALOG

        if not url.endswith("/"):
            url += "/"
        url += "api/catalogManagement/v2/productSpecification/{}".format(product_spec["id"])

        asset.save()
        product_spec['productSpecCharacteristic'][2]['productSpecCharacteristicValue'][0]['value'] = asset.download_link
        requests.put(url, json=product_spec, headers=self._headers)
