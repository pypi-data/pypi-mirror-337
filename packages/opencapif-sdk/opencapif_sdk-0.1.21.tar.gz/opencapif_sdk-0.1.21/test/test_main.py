import subprocess
import pytest
import urllib3
# Desactivar solo el warning de solicitudes HTTPS no verificadas
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
# flake8: noqa

from opencapif_sdk import capif_invoker_connector, capif_provider_connector, service_discoverer, capif_logging_feature, capif_invoker_event_feature, capif_provider_event_feature,api_schema_translator


capif_sdk_config_path = "./capif_sdk_config_sample_test.json"

# Fixture para configurar el proveedor
@pytest.fixture
def provider_setup():
    provider = capif_provider_connector(capif_sdk_config_path)
    provider.onboard_provider()
    yield provider
    provider.offboard_provider()

# Fixture para configurar el proveedor
@pytest.fixture
def invoker_setup():
    invoker = capif_invoker_connector(capif_sdk_config_path)
    invoker.onboard_invoker()
    yield invoker
    invoker.offboard_invoker()

@pytest.fixture
def test_provider_update(provider_setup):
    provider = capif_provider_connector(capif_sdk_config_path)
    provider.aefs=1
    provider.apfs=1
    provider.update_provider()

@pytest.fixture
def test_provider_publish(test_provider_update):
    provider = capif_provider_connector(capif_sdk_config_path) 
    APF1 = provider.provider_capif_ids['APF-1']
    AEF1 = provider.provider_capif_ids['AEF-1']
    
    translator = api_schema_translator("./test1.yaml")
    translator.build(url="https://192.168.1.10:8080/test1/v1",supported_features= "0",api_supp_features= "0")
    provider.api_description_path="./test1.json"
    # Update configuration file
    provider.publish_req['publisher_apf_id'] = APF1
    provider.publish_req['publisher_aefs_ids'] = [AEF1]
    
    provider.publish_services()

@pytest.fixture
def test_events(test_provider_publish):
    provider=capif_provider_connector(capif_sdk_config_path)
    event_provider = capif_provider_event_feature(config_file=capif_sdk_config_path)

    APF1 = provider.provider_capif_ids['APF-1']
    AEF1 = provider.provider_capif_ids['AEF-1']

    event_provider.create_subscription(name="Ejemplo1",id=AEF1)

    event_provider.create_subscription(name="Ejemplo2",id=APF1)

    event_provider.delete_subscription(name="Ejemplo1",id=AEF1)

    event_provider.delete_subscription(name="Ejemplo2",id=APF1)
@pytest.fixture
def tokens(invoker_setup):
    discoverer = service_discoverer(config_file=capif_sdk_config_path)
    discoverer.discover()
    discoverer.get_tokens()


def test_logs(test_provider_publish,tokens):
    provider=capif_provider_connector(capif_sdk_config_path)
    discoverer = service_discoverer(config_file=capif_sdk_config_path)
    AEF1 = provider.provider_capif_ids['AEF-1']
    token = discoverer.token
    capif_log = capif_logging_feature(capif_sdk_config_path)
    
    capif_log.create_logs(aefId=AEF1,jwt=token)

""" def test_check_invoker(test_provider_publish,tokens):
    provider=capif_provider_connector(capif_sdk_config_path)
    discoverer = service_discoverer(config_file=capif_sdk_config_path)
    AEF1 = provider.provider_capif_ids['AEF-1']
    api_invoker_id = discoverer.invoker_capif_details['api_invoker_id']
    provider.get_trusted_invokers(api_invoker_id,AEF1)
     """

def test_invoker_discover(invoker_setup,test_provider_publish):
    discoverer = service_discoverer(config_file=capif_sdk_config_path)
    discoverer.discover()
    discoverer.get_tokens()

def test_provider_unpublish_1(test_events):
    provider=capif_provider_connector(capif_sdk_config_path)
    APF1 = provider.provider_capif_ids['APF-1']
    provider.publish_req['publisher_apf_id'] = APF1
    service_api_id = provider.provider_service_ids["test1"]
    provider.publish_req['service_api_id'] = service_api_id
    provider.unpublish_service()

def test_provider_update_service(test_provider_publish):
    provider=capif_provider_connector(capif_sdk_config_path)
    APF1 = provider.provider_capif_ids['APF-1']
    AEF1 = provider.provider_capif_ids['AEF-1']
    provider.publish_req['publisher_apf_id'] = APF1
    provider.publish_req['publisher_aefs_ids'] = [AEF1]
    service_api_id = provider.provider_service_ids["test1"]
    provider.publish_req['service_api_id'] = service_api_id
    provider.api_description_path="test1.json"
    
    provider.update_service()
    

def preparation_for_update(APFs, AEFs,capif_provider_connector):
    
    capif_provider_connector.apfs = APFs
    capif_provider_connector.aefs = AEFs
    
    return capif_provider_connector


    
