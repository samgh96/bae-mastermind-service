import jsonschema
import yaml
import requests

from wstore.asset_manager.resource_plugins.plugin import Plugin
from mastermindschema import MastermindSchema
from keystone_client import KeystoneClient

from django.conf import settings


class MastermindPlugin(Plugin):

    _yaml_validator = MastermindSchema._schema
    _headers = {'content-type': 'application/json'}

    def _validate(self, yml, validator):
        errors = sorted(jsonschema.Draft4Validator(validator).iter_errors(yaml.load(yml)), key=lambda e: e.path)
        return [str(x.message) for x in errors]

    def _create_service_mm(self, asset, mm_url, headers):
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

        return mm_url + str(mm_req.json().get('id'))

    def on_post_product_spec_validation(self, provider, asset):
        kc = KeystoneClient(asset.get_url(), is_url=True)
        kc.check_ownership(provider.name)
        mastermind = asset.meta_info['configuration_template']
        err_list = self._validate(mastermind, self._yaml_validator)

        if len(err_list):
            raise ValueError("Found errors in mastermind.yml: "' '.join(err_list))

        asset.meta_info.update({'api_url': kc.get_api_url(), 'app_id': kc.get_app_id()})

        asset.save()

    def on_pre_product_spec_attachment(self, asset, asset_t, product_spec):
        url = settings.CATALOG
        if not url.endswith("/"):
            url += "/"
        url += "api/catalogManagement/v2/productSpecification/{}".format(product_spec["id"])

        asset.download_link = self._create_service_mm(asset, asset.meta_info['api_url'], self._headers)

        for i in product_spec['productSpecCharacteristic']:
            if i['name'] == 'Location':
                i['productSpecCharacteristicValue'][0]['value'] = asset.download_link

        spec_req = requests.put(url, json=product_spec, headers=self._headers)
        spec_req.raise_for_status()
        asset.save()

    def on_product_acquisition(self, asset, contract, order):
        kc = KeystoneClient(asset.meta_info['app_id'])
        kc.grant_permission(order.customer, 'owner')

    def on_product_suspension(self, asset, contract, order):
        kc = KeystoneClient(asset.meta_info['app_id'])
        kc.revoke_permission(order.customer, 'owner')
