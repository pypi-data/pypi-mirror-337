from requests.exceptions import RequestsDependencyWarning
import warnings
import json
import requests
from OpenSSL.crypto import (
    dump_certificate_request,
    dump_privatekey,
    PKey,
    TYPE_RSA,
    X509Req
)
from OpenSSL.SSL import FILETYPE_PEM
import os
import logging
import shutil
from requests.auth import HTTPBasicAuth
import urllib3
import ssl
import socket
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


warnings.filterwarnings("ignore", category=RequestsDependencyWarning)

# Basic logger configuration

log_path = 'logs/sdk_logs.log'

log_dir = os.path.dirname(log_path)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.NOTSET,  # Minimum severity level to log
    # Log message format
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path),  # Logs to a file
        logging.StreamHandler()  # Also outputs to the console
    ]
)


class capif_provider_connector:
    """
    Τhis class is responsible for onboarding an exposer (eg. NEF emulator) to CAPIF
    """

    def __init__(self, config_file: str):
        """
        Initializes the CAPIFProvider connector with the parameters specified in the configuration file.
        """
        # Load configuration from file if necessary
        config_file = os.path.abspath(config_file)
        self.config_path = os.path.dirname(config_file)+"/"
        config = self.__load_config_file(config_file)
        debug_mode = os.getenv('DEBUG_MODE', config.get('debug_mode', 'False')).strip().lower()
        if debug_mode == "false":
            debug_mode = False
        else:
            debug_mode = True

        # Initialize logger for this class
        self.logger = logging.getLogger(self.__class__.__name__)
        if debug_mode:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.WARNING)

        # Set logging level for urllib based on debug_mode
        urllib_logger = logging.getLogger("urllib3")
        if not debug_mode:
            urllib_logger.setLevel(logging.WARNING)
        else:
            urllib_logger.setLevel(logging.DEBUG)

        try:
            # Retrieve provider configuration from JSON or environment variables
            provider_config = config.get('provider', {})
            provider_general_folder = os.path.abspath(
                os.getenv('PROVIDER_FOLDER', provider_config.get('provider_folder', '')).strip())

            capif_host = os.getenv('CAPIF_HOST', config.get('capif_host', '')).strip()
            capif_register_host = os.getenv('REGISTER_HOST', config.get('register_host', '')).strip()
            capif_https_port = str(os.getenv('CAPIF_HTTPS_PORT', config.get('capif_https_port', '')).strip())
            capif_register_port = str(os.getenv('CAPIF_REGISTER_PORT', config.get('capif_register_port', '')).strip())
            capif_provider_username = os.getenv('CAPIF_USERNAME', config.get('capif_username', '')).strip()
            capif_provider_password = os.getenv('CAPIF_PASSWORD', config.get('capif_password', '')).strip()

            # Get CSR (Certificate Signing Request) details from config or environment variables
            cert_generation = provider_config.get('cert_generation', {})
            csr_common_name = os.getenv('PROVIDER_CSR_COMMON_NAME', cert_generation.get('csr_common_name', '')).strip()
            csr_organizational_unit = os.getenv('PROVIDER_CSR_ORGANIZATIONAL_UNIT', cert_generation.get('csr_organizational_unit', '')).strip()
            csr_organization = os.getenv('PROVIDER_CSR_ORGANIZATION', cert_generation.get('csr_organization', '')).strip()
            csr_locality = os.getenv('PROVIDER_CSR_LOCALITY', cert_generation.get('csr_locality', '')).strip()
            csr_state_or_province_name = os.getenv('PROVIDER_CSR_STATE_OR_PROVINCE_NAME', cert_generation.get('csr_state_or_province_name', '')).strip()
            csr_country_name = os.getenv('PROVIDER_CSR_COUNTRY_NAME', cert_generation.get('csr_country_name', '')).strip()
            csr_email_address = os.getenv('PROVIDER_CSR_EMAIL_ADDRESS', cert_generation.get('csr_email_address', '')).strip()

            # Retrieve provider specific values (APFs, AEFs)
            supported_features = os.getenv('PROVIDER_SUPPORTED_FEATURES', provider_config.get('supported_features', '')).strip()
            if not supported_features:
                supported_features = "0"

            apfs = os.getenv('PROVIDER_APFS', provider_config.get('apfs', '')).strip()
            aefs = os.getenv('PROVIDER_AEFS', provider_config.get('aefs', '')).strip()
            api_description_path = os.path.abspath(os.getenv('PROVIDER_API_DESCRIPTION_PATH', provider_config.get('api_description_path', '')).strip())

            # Check required fields and log warnings/errors
            if not capif_host:
                self.logger.warning("CAPIF_HOST is not provided; defaulting to an empty string")
            if not capif_provider_username:
                self.logger.error("CAPIF_PROVIDER_USERNAME is required but not provided")
                raise ValueError("CAPIF_PROVIDER_USERNAME is required")

            # Setup the folder to store provider files (e.g., certificates)
            self.provider_folder = os.path.join(provider_general_folder, capif_provider_username)
            os.makedirs(self.provider_folder, exist_ok=True)

            # Set attributes for provider credentials and configuration
            self.capif_host = capif_host.strip()
            self.capif_provider_username = capif_provider_username
            self.capif_provider_password = capif_provider_password
            self.capif_register_host = capif_register_host
            self.capif_register_port = capif_register_port
            self.csr_common_name = csr_common_name
            self.csr_organizational_unit = csr_organizational_unit
            self.csr_organization = csr_organization
            self.csr_locality = csr_locality
            self.csr_state_or_province_name = csr_state_or_province_name
            self.csr_country_name = csr_country_name
            self.csr_email_address = csr_email_address
            self.supported_features = supported_features
            self.aefs = int(aefs)
            self.apfs = int(apfs)

            # Get publish request details from config or environment variables
            publish_req_config = provider_config.get('publish_req', {})
            self.publish_req = {
                "service_api_id": os.getenv('PUBLISH_REQ_SERVICE_API_ID', publish_req_config.get('service_api_id', '')).strip(),
                "publisher_apf_id": os.getenv('PUBLISH_REQ_PUBLISHER_APF_ID', publish_req_config.get('publisher_apf_id', '')).strip(),
                "publisher_aefs_ids": os.getenv('PUBLISH_REQ_PUBLISHER_AEFS_IDS', publish_req_config.get('publisher_aefs_ids', ''))
            }

            # Set the path for the API description file
            self.api_description_path = api_description_path

            # Set the CAPIF HTTPS port and construct CAPIF URLs
            self.capif_https_port = str(capif_https_port)

            self.provider_capif_ids = {}

            path_prov_funcs = os.path.join(self.provider_folder, "provider_capif_ids.json")
            if os.path.exists(path_prov_funcs):
                self.provider_capif_ids = self._load_provider_api_details()

            path_published = os.path.join(self.provider_folder, "provider_service_ids.json")
            if os.path.exists(path_published):
                self.provider_service_ids = self.__load_config_file(path_published)

            # Construct the CAPIF HTTPS URL
            if len(self.capif_https_port) == 0 or int(self.capif_https_port) == 443:
                self.capif_https_url = f"https://{capif_host.strip()}/"
            else:
                self.capif_https_url = f"https://{capif_host.strip()}:{self.capif_https_port.strip()}/"

            # Construct the CAPIF register URL
            if len(capif_register_port) == 0:
                self.capif_register_url = f"https://{capif_register_host.strip()}:8084/"
            else:
                self.capif_register_url = f"https://{capif_register_host.strip()}:{capif_register_port.strip()}/"

            events_config = provider_config.get('events', {})
            self.events_description = os.getenv('PROVIDER_EVENTS_DESCRIPTION', events_config.get('description', ''))
            self.events_filter = os.getenv('PROVIDER_EVENTS_FILTERS', events_config.get('eventFilters', ''))
            self.notification_destination = os.getenv('PROVIDER_EVENTS_FILTERS', events_config.get('notificationDestination', ''))
            self.websock_notif_config = os.getenv('PROVIDER_EVENTS_FILTERS', events_config.get('websockNotifConfig', ''))
            # Log initialization success message
            self.logger.info("capif_provider_connector initialized with the capif_sdk_config.json parameters")

        except Exception as e:
            # Catch and log any exceptions that occur during initialization
            self.logger.error(f"Error during initialization: {e}")
            raise

    def __store_certificate(self) -> None:
        self.logger.info("Retrieving capif_cert_server.pem...")

        try:
            # Crear un contexto SSL que no valide certificados
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            with socket.create_connection((self.capif_host, self.capif_https_port)) as sock:
                with context.wrap_socket(sock, server_hostname=self.capif_host) as ssock:
                    cert = ssock.getpeercert(binary_form=True)
                    cert_file = os.path.join(self.provider_folder, "capif_cert_server.pem")
                    with open(cert_file, "wb") as f:
                        f.write(ssl.DER_cert_to_PEM_cert(cert).encode())
            self.logger.info("cert_server.pem successfully generated!")
        except Exception as e:
            self.logger.error(f"Error occurred while retrieving certificate: {e}")
            raise

    def __load_config_file(self, config_file: str):
        """Carga el archivo de configuración."""
        try:
            with open(config_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            self.logger.warning(
                f"Configuration file {config_file} not found. Using defaults or environment variables.")
            return {}

    def __create_private_and_public_keys(self, api_prov_func_role) -> bytes:
        """
        Creates private and public keys in the certificates folder.
        :return: The contents of the public key
        """
        private_key_path = os.path.join(
            self.provider_folder, f"{api_prov_func_role}_private_key.key")
        csr_file_path = os.path.join(
            self.provider_folder, f"{api_prov_func_role}_public.csr")

        # Create key pair
        key = PKey()
        key.generate_key(TYPE_RSA, 2048)

        # Create CSR
        req = X509Req()
        subject = req.get_subject()
        subject.CN = api_prov_func_role.lower()
        subject.O = self.csr_organization
        subject.OU = self.csr_organizational_unit
        subject.L = self.csr_locality
        subject.ST = self.csr_state_or_province_name
        subject.C = self.csr_country_name
        subject.emailAddress = self.csr_email_address

        req.set_pubkey(key)
        req.sign(key, "sha256")

        # Write CSR and private key to files
        with open(csr_file_path, "wb") as csr_file:
            public_key = dump_certificate_request(FILETYPE_PEM, req)
            csr_file.write(public_key)

        with open(private_key_path, "wb") as private_key_file:
            private_key_file.write(dump_privatekey(FILETYPE_PEM, key))

        return public_key

    def __onboard_exposer_to_capif(self, access_token, capif_onboarding_url):
        self.logger.info(
            "Onboarding Provider to CAPIF and waiting signed certificate by giving our public keys to CAPIF")

        url = f"{self.capif_https_url}{capif_onboarding_url}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # Create the list of roles without indexing
        roles = ["AMF"]
        for n in range(1, self.aefs + 1):
            roles.append("AEF")

        for n in range(1, self.apfs + 1):
            roles.append("APF")

        # Build the payload with the non-indexed roles
        payload = {
            "apiProvFuncs": [
                {"regInfo": {"apiProvPubKey": ""}, "apiProvFuncRole": role,
                    "apiProvFuncInfo": f"{role.lower()}"}
                for role in roles
            ],
            "apiProvDomInfo": "This is provider",
            "suppFeat": self.supported_features,
            "failReason": "string",
            "regSec": access_token,
        }

        # Generate the indexed roles for certificate creation
        indexedroles = ["AMF"]
        for n in range(1, self.aefs + 1):
            indexedroles.append(f"AEF-{n}")

        for n in range(1, self.apfs + 1):
            indexedroles.append(f"APF-{n}")

        # Save the public keys and generate certificates with indexed roles
        for i, api_func in enumerate(payload["apiProvFuncs"]):
            # Generate public keys with the indexed role, but do not update the payload with the indexed role
            public_key = self.__create_private_and_public_keys(indexedroles[i])

            # Assign the public key to the payload
            api_func["regInfo"]["apiProvPubKey"] = public_key.decode("utf-8")
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(payload),
                verify=os.path.join(self.provider_folder, "ca.crt"),
            )
            response.raise_for_status()
            self.logger.info(
                "Provider onboarded and signed certificate obtained successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(
                f"Onboarding failed: {e} - Response: {response.text}")
            raise

    def __write_to_file(self, onboarding_response, capif_registration_id, publish_url):
        self.logger.info("Saving the most relevant onboarding data")

        # Generate the indexed roles for correspondence
        indexedroles = ["AMF"]
        for n in range(1, self.aefs + 1):
            indexedroles.append(f"AEF-{n}")

        for n in range(1, self.apfs + 1):
            indexedroles.append(f"APF-{n}")

        # Save the certificates with the indexed names
        for i, func_profile in enumerate(onboarding_response["apiProvFuncs"]):
            role = indexedroles[i].lower()
            cert_path = os.path.join(self.provider_folder, f"{role}.crt")
            with open(cert_path, "wb") as cert_file:
                cert_file.write(
                    func_profile["regInfo"]["apiProvCert"].encode("utf-8"))

        # Save the provider details
        provider_details_path = os.path.join(
            self.provider_folder, "provider_capif_ids.json")
        with open(provider_details_path, "w") as outfile:
            data = {
                "capif_registration_id": capif_registration_id,
                "publish_url": publish_url,
                **{f"{indexedroles[i]}": api_prov_func["apiProvFuncId"]
                   for i, api_prov_func in enumerate(onboarding_response["apiProvFuncs"])}
            }
            for i, api_prov_func in enumerate(onboarding_response["apiProvFuncs"]):
                self.provider_capif_ids[indexedroles[i]] = api_prov_func["apiProvFuncId"]

            json.dump(data, outfile, indent=4)
        self.logger.info("Data saved")

    def __save_capif_ca_root_file_and_get_auth_token(self):
        url = f"{self.capif_register_url}getauth"
        self.logger.info(
            "Saving CAPIF CA root file and getting auth token with user and password given by the CAPIF administrator")

        try:
            response = requests.get(
                url,
                headers={"Content-Type": "application/json"},
                auth=HTTPBasicAuth(self.capif_provider_username,
                                   self.capif_provider_password),
                verify=False
            )
            response.raise_for_status()

            self.logger.info("Authorization acquired successfully")

            response_payload = response.json()
            ca_root_file_path = os.path.join(self.provider_folder, "ca.crt")

            with open(ca_root_file_path, "wb") as ca_root_file:
                ca_root_file.write(response_payload["ca_root"].encode("utf-8"))

            self.logger.info(
                "CAPIF CA root file saved and auth token obtained successfully")
            return response_payload

        except requests.exceptions.RequestException as e:
            self.logger.error(
                f"Error acquiring authorization: {e} - Response: {response.text}")
            raise

    def onboard_provider(self) -> None:
        """
        Retrieves and stores the certificate from CAPIF, acquires authorization, and registers the provider.
        """
        # Store the certificate
        self.__store_certificate()

        # Retrieve CA root file and get authorization token
        capif_postauth_info = self.__save_capif_ca_root_file_and_get_auth_token()

        # Extract necessary information
        capif_onboarding_url = capif_postauth_info["ccf_api_onboarding_url"]
        access_token = capif_postauth_info["access_token"]
        ccf_publish_url = capif_postauth_info["ccf_publish_url"]

        # Onboard provider to CAPIF
        onboarding_response = self.__onboard_exposer_to_capif(
            access_token, capif_onboarding_url
        )

        # Save onboarding details to file
        capif_registration_id = onboarding_response["apiProvDomId"]
        self.__write_to_file(
            onboarding_response, capif_registration_id, ccf_publish_url
        )

    def publish_services(self) -> dict:
        """
        Publishes services to CAPIF and returns the published services dictionary.

        :param service_api_description_json_full_path: The full path of the service_api_description.json containing
        the endpoints to be published.
        :return: The published services dictionary that was saved in CAPIF.
        """
        self.logger.info("Starting the service publication process")

        # Load provider details
        provider_details_path = os.path.join(
            self.provider_folder, "provider_capif_ids.json")
        self.logger.info(
            f"Loading provider details from {provider_details_path}")

        provider_details = self._load_provider_api_details()

        publish_url = provider_details["publish_url"]

        chosenAPFsandAEFs = self.publish_req

        APF_api_prov_func_id = chosenAPFsandAEFs["publisher_apf_id"]
        AEFs_list = chosenAPFsandAEFs["publisher_aefs_ids"]

        apf_number = None
        for key, value in provider_details.items():
            if value == APF_api_prov_func_id and key.startswith("APF-"):
                apf_inter = key.split("-")[1]
                # Obtain the APF number
                apf_number = apf_inter.split("_")[0]
                break

        if apf_number is None:
            self.logger.error(
                f"No matching APF found for publisher_apf_id: {APF_api_prov_func_id}")
            raise ValueError("Invalid publisher_apf_id")
        service_api_description_json_full_path = self.api_description_path
        # Read and modify the API description
        self.logger.info(
            f"Reading and modifying service API description from {service_api_description_json_full_path}")

        try:
            with open(service_api_description_json_full_path, "r") as service_file:
                data = json.load(service_file)

                # Verifying that the number of AEFs is equal to the aefProfiles
                if len(AEFs_list) != len(data.get("aefProfiles", [])):
                    self.logger.error(
                        "The number of AEFs in publisher_aefs_ids does not match the number of profiles in aefProfiles")
                    raise ValueError(
                        "Mismatch between number of AEFs and profiles")

                # Assigning each AEF

                for profile, aef_id in zip(data.get("aefProfiles", []), AEFs_list):
                    if not isinstance(profile, dict):  # Verificar que profile sea un diccionario
                        raise TypeError(f"Expected profile to be a dict, got {type(profile).__name__}")

                    profile["aefId"] = aef_id  # Asignar el ID de AEF

                    versions = profile.get("versions")  # Obtener versions

                    i = 1
                    for version in versions:  # Iterar sobre cada versión
                        if not isinstance(version, dict):  # Verificar que cada versión sea un diccionario
                            raise TypeError(f"Expected each version to be a dict, got {type(version).__name__}")

                        # Obtener nombres existentes de operaciones personalizadas
                        existing_operations = {
                            op["custOpName"].strip()
                            for op in version.get("custOperations", []) if isinstance(op, dict)
                        }

                        # Verificar y agregar `check-authentication` si no existe
                        if "check-authentication" not in existing_operations and i == 1:
                            version.setdefault("custOperations", []).append({
                                "commType": "REQUEST_RESPONSE",
                                "custOpName": "check-authentication",
                                "operations": ["POST"],
                                "description": "Check authentication request."
                            })

                        # Verificar y agregar `revoke-authentication` si no existe
                        if "revoke-authentication" not in existing_operations and i == 1:
                            version.setdefault("custOperations", []).append({
                                "commType": "REQUEST_RESPONSE",
                                "custOpName": "revoke-authentication",
                                "operations": ["POST"],
                                "description": "Revoke authorization for service APIs."
                            })
                        i -= 1

                self.logger.info(
                    "Service API description modified successfully")

                # Saving changes into the file
                with open(service_api_description_json_full_path, "w") as service_file:
                    json.dump(data, service_file, indent=4)

        except FileNotFoundError:
            self.logger.error(
                f"Service API description file not found: {service_api_description_json_full_path}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(
                f"Error decoding JSON from file {service_api_description_json_full_path}: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Error with the input data: {e}")
            raise

        # Publish services
        url = f"{self.capif_https_url}{publish_url.replace('<apfId>', APF_api_prov_func_id)}"
        cert = (
            os.path.join(self.provider_folder, f"apf-{apf_number}.crt"),
            os.path.join(self.provider_folder,
                         f"APF-{apf_number}_private_key.key"),
        )

        self.logger.info(f"Publishing services to URL: {url}")
        try:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
                cert=cert,
                verify=os.path.join(self.provider_folder, "ca.crt"),
            )
            response.raise_for_status()
            self.logger.info("Services published successfully")

            # Save response to file
            capif_response_text = response.text

            capif_response_json = json.loads(capif_response_text)

            # Default name if apiName is missing
            file_name = capif_response_json.get("apiName", "default_name")
            id = capif_response_json.get("apiId", "default_id")
            output_path = os.path.join(
                self.provider_folder, f"capif_{file_name}_{id}_api.json")

            with open(output_path, "w") as outfile:
                outfile.write(capif_response_text)
            self.logger.info(f"CAPIF response saved to {output_path}")
            output_path = os.path.join(

                self.provider_folder, "provider_service_ids.json")

            # Read the existing file of published APIs
            provider_service_ids = {}
            if os.path.exists(output_path):
                with open(output_path, "r") as outfile:
                    provider_service_ids = json.load(outfile)

            # Add the newly published API

            provider_service_ids[file_name] = id

            self.provider_service_ids = provider_service_ids
            # Write the updated file of published APIs
            with open(output_path, "w") as outfile:
                json.dump(provider_service_ids, outfile, indent=4)
            self.logger.info(
                f"API '{file_name}' with ID '{id}' added to Published Apis.")
            return json.loads(capif_response_text)

        except requests.RequestException as e:
            self.logger.error(
                f"Request to CAPIF failed: {e} - Response: {response.text}")
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error during service publication: {e} - Response: {response.text}")
            raise

    def unpublish_service(self) -> dict:
        """
        Publishes services to CAPIF and returns the published services dictionary.

        :param service_api_description_json_full_path: The full path of the service_api_description.json containing
        the endpoints to be published.
        :return: The published services dictionary that was saved in CAPIF.
        """
        self.logger.info("Starting the service unpublication process")
        provider_details_path = os.path.join(
            self.provider_folder, "provider_capif_ids.json")
        self.logger.info(
            f"Loading provider details from {provider_details_path}")

        provider_details = self._load_provider_api_details()
        publish_url = provider_details["publish_url"]

        # Load provider details
        publish = self.publish_req
        api_id = "/" + publish["service_api_id"]
        APF_api_prov_func_id = publish["publisher_apf_id"]
        apf_number = None
        for key, value in provider_details.items():
            if value == APF_api_prov_func_id and key.startswith("APF-"):
                apf_inter = key.split("-")[1]
                # Get the number of APFs
                apf_number = apf_inter.split("_")[0]
                break

        if apf_number is None:
            self.logger.error(
                f"No matching APF found for publisher_apf_id: {APF_api_prov_func_id}")
            raise ValueError("Invalid publisher_apf_id")

        self.logger.info(
            f"Loading provider details from {provider_details_path}")

        url = f"{self.capif_https_url}{publish_url.replace('<apfId>', APF_api_prov_func_id)}{api_id}"

        cert = (
            os.path.join(self.provider_folder, f"apf-{apf_number}.crt"),
            os.path.join(self.provider_folder, f"APF-{apf_number}_private_key.key"),
        )

        self.logger.info(f"Unpublishing service to URL: {url}")

        try:
            response = requests.delete(
                url,
                headers={"Content-Type": "application/json"},
                cert=cert,
                verify=os.path.join(self.provider_folder, "ca.crt"),
            )

            response.raise_for_status()

            directory = self.provider_folder

            # Iterar sobre todos los archivos en el directorio
            for filename in os.listdir(directory):
                path = os.path.join(directory, filename)

                # Check if the file starts with 'CAPIF-'

                if filename.startswith("CAPIF-") and publish["service_api_id"] in filename:

                    # Exit the loop if the file is deleted
                    os.remove(path)
                    break

            output_path = os.path.join(

                self.provider_folder, "provider_service_ids.json")

            # Read the existing file of published APIs
            provider_service_ids = {}
            if os.path.exists(output_path):
                with open(output_path, "r") as outfile:
                    provider_service_ids = json.load(outfile)

            # API ID you want to delete
            # Replace with the specific ID
            api_id_to_delete = publish["service_api_id"]

            # Search and delete the API by its ID
            api_name_to_delete = None
            for name, id in provider_service_ids.items():
                if id == api_id_to_delete:
                    api_name_to_delete = name
                    break

            if api_name_to_delete:
                del provider_service_ids[api_name_to_delete]
                self.logger.info(
                    f"API with ID '{api_id_to_delete}' removed from Published Apis.")
            else:
                self.logger.warning(
                    f"API with ID '{api_id_to_delete}' not found in Published Apis.")

            # Write the updated file of published APIs
            with open(output_path, "w") as outfile:

                json.dump(provider_service_ids, outfile, indent=4)
            self.provider_service_ids = provider_service_ids
            self.logger.info("Services unpublished successfully")

        except requests.RequestException as e:
            self.logger.error(
                f"Request to CAPIF failed: {e} - Response: {response.text}")
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error during service unpublication: {e} - Response: {response.text}")
            raise

    def get_service(self) -> dict:
        """
        Publishes services to CAPIF and returns the published services dictionary.

        :param service_api_description_json_full_path: The full path of the service_api_description.json containing
        the endpoints to be published.
        :return: The published services dictionary that was saved in CAPIF.
        """
        self.logger.info("Starting the service unpublication process")

        provider_details_path = os.path.join(
            self.provider_folder, "provider_capif_ids.json")
        self.logger.info(
            f"Loading provider details from {provider_details_path}")

        provider_details = self._load_provider_api_details()
        publish_url = provider_details["publish_url"]

        chosenAPFsandAEFs = self.publish_req

        APF_api_prov_func_id = chosenAPFsandAEFs["publisher_apf_id"]

        api_id = "/" + chosenAPFsandAEFs["service_api_id"]

        apf_number = None
        for key, value in provider_details.items():
            if value == APF_api_prov_func_id and key.startswith("APF-"):
                apf_inter = key.split("-")[1]
                # Get the number of apfs
                apf_number = apf_inter.split("_")[0]
                break

        if apf_number is None:
            self.logger.error(
                f"No matching APF found for publisher_apf_id: {APF_api_prov_func_id}")
            raise ValueError("Invalid publisher_apf_id")

        url = f"{self.capif_https_url}{publish_url.replace('<apfId>', APF_api_prov_func_id)}{api_id}"

        cert = (
            os.path.join(self.provider_folder, f"apf-{apf_number}.crt"),
            os.path.join(self.provider_folder,
                         f"APF-{apf_number}_private_key.key"),
        )

        self.logger.info(f"Getting service to URL: {url}")

        try:
            response = requests.get(
                url,
                headers={"Content-Type": "application/json"},
                cert=cert,
                verify=os.path.join(self.provider_folder, "ca.crt"),
            )

            response.raise_for_status()

            self.logger.info("Service received successfully")
            path = os.path.join(self.provider_folder, "service_received.json")
            with open(path, 'w') as f:
                json_data = json.loads(response.text)
                json.dump(json_data, f, indent=4)
            self.logger.info(f"Service saved in {path}")

        except requests.RequestException as e:
            self.logger.error(
                f"Request to CAPIF failed: {e} - Response: {response.text}")
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error during service getter: {e} - Response: {response.text}")
            raise

    def get_all_services(self) -> dict:
        """
        Publishes services to CAPIF and returns the published services dictionary.

        :param service_api_description_json_full_path: The full path of the service_api_description.json containing
        the endpoints to be published.
        :return: The published services dictionary that was saved in CAPIF.
        """
        self.logger.info("Starting the service publication process")

        # Load provider details
        provider_details_path = os.path.join(
            self.provider_folder, "provider_capif_ids.json")
        self.logger.info(
            f"Loading provider details from {provider_details_path}")

        provider_details = self._load_provider_api_details()
        publish_url = provider_details["publish_url"]

        chosenAPFsandAEFs = self.publish_req

        APF_api_prov_func_id = chosenAPFsandAEFs["publisher_apf_id"]

        apf_number = None
        for key, value in provider_details.items():
            if value == APF_api_prov_func_id and key.startswith("APF-"):
                apf_inter = key.split("-")[1]
                # Get the number of APFs
                apf_number = apf_inter.split("_")[0]
                break

        if apf_number is None:
            self.logger.error(
                f"No matching APF found for publisher_apf_id: {APF_api_prov_func_id}")
            raise ValueError("Invalid publisher_apf_id")

        # Read and modify the description of the API services

        # Publish services
        url = f"{self.capif_https_url}{publish_url.replace('<apfId>', APF_api_prov_func_id)}"
        cert = (
            os.path.join(self.provider_folder, f"apf-{apf_number}.crt"),
            os.path.join(self.provider_folder,
                         f"APF-{apf_number}_private_key.key"),
        )

        self.logger.info(f"Getting services to URL: {url}")

        try:
            response = requests.get(
                url,
                headers={"Content-Type": "application/json"},
                cert=cert,
                verify=os.path.join(self.provider_folder, "ca.crt"),
            )
            response.raise_for_status()
            self.logger.info("Services received successfully")

            path = os.path.join(self.provider_folder, "service_received.json")
            with open(path, 'w') as f:
                json_data = json.loads(response.text)
                json.dump(json_data, f, indent=4)
            self.logger.info(f"Services saved in {path}")

            # Save response to file

        except requests.RequestException as e:
            self.logger.error(
                f"Request to CAPIF failed: {e} - Response: {response.text}")
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error during services reception: {e} - Response: {response.text}")
            raise

    def update_service(self) -> dict:
        """
        Publishes services to CAPIF and returns the published services dictionary.

        :param service_api_description_json_full_path: The full path of the service_api_description.json containing
        the endpoints to be published.
        :return: The published services dictionary that was saved in CAPIF.
        """
        self.logger.info("Starting the service publication process")

        # Load provider details
        # Load provider details
        provider_details_path = os.path.join(
            self.provider_folder, "provider_capif_ids.json")
        self.logger.info(
            f"Loading provider details from {provider_details_path}")

        provider_details = self._load_provider_api_details()
        publish_url = provider_details["publish_url"]

        chosenAPFsandAEFs = self.publish_req

        APF_api_prov_func_id = chosenAPFsandAEFs["publisher_apf_id"]
        AEFs_list = chosenAPFsandAEFs["publisher_aefs_ids"]

        apf_number = None
        for key, value in provider_details.items():
            if value == APF_api_prov_func_id and key.startswith("APF-"):
                apf_inter = key.split("-")[1]
                # Get the number of APFs
                apf_number = apf_inter.split("_")[0]
                break

        if apf_number is None:
            self.logger.error(
                f"No matching APF found for publisher_apf_id: {APF_api_prov_func_id}")
            raise ValueError("Invalid publisher_apf_id")

        service_api_description_json_full_path = self.api_description_path
        # Read and modify the description of the API services
        self.logger.info(
            f"Reading and modifying service API description from {service_api_description_json_full_path}")

        try:
            with open(service_api_description_json_full_path, "r") as service_file:
                data = json.load(service_file)

                # verify the aefs number corresponds to the aefProfiles
                if len(AEFs_list) != len(data.get("aefProfiles", [])):
                    self.logger.error(
                        "The number of AEFs in publisher_aefs_ids does not match the number of profiles in aefProfiles")
                    raise ValueError(
                        "Mismatch between number of AEFs and profiles")

                # Asing the chosen AEFs
                for profile, aef_id in zip(data.get("aefProfiles", []), AEFs_list):
                    if not isinstance(profile, dict):  # Verificar que profile sea un diccionario
                        raise TypeError(f"Expected profile to be a dict, got {type(profile).__name__}")

                    profile["aefId"] = aef_id  # Asignar el ID de AEF

                    versions = profile.get("versions")  # Obtener versions
                    i = 1
                    for version in versions:  # Iterar sobre cada versión
                        if not isinstance(version, dict):  # Verificar que cada versión sea un diccionario
                            raise TypeError(f"Expected each version to be a dict, got {type(version).__name__}")

                        # Obtener nombres existentes de operaciones personalizadas
                        existing_operations = {
                            op["custOpName"].strip()
                            for op in version.get("custOperations", []) if isinstance(op, dict)
                        }

                        # Verificar y agregar `check-authentication` si no existe
                        if "check-authentication" not in existing_operations and i == 1:
                            version.setdefault("custOperations", []).append({
                                "commType": "REQUEST_RESPONSE",
                                "custOpName": "check-authentication",
                                "operations": ["POST"],
                                "description": "Check authentication request."
                            })

                        # Verificar y agregar `revoke-authentication` si no existe
                        if "revoke-authentication" not in existing_operations and i == 1:
                            version.setdefault("custOperations", []).append({
                                "commType": "REQUEST_RESPONSE",
                                "custOpName": "revoke-authentication",
                                "operations": ["POST"],
                                "description": "Revoke authorization for service APIs."
                            })
                        i -= 1

                self.logger.info(
                    "Service API description modified successfully")

                # Save changes
                with open(service_api_description_json_full_path, "w") as service_file:
                    json.dump(data, service_file, indent=4)

        except FileNotFoundError:
            self.logger.error(
                f"Service API description file not found: {service_api_description_json_full_path}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(
                f"Error decoding JSON from file {service_api_description_json_full_path}: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Error with the input data: {e}")
            raise
        api_id = "/" + chosenAPFsandAEFs["service_api_id"]
        # Publish services
        url = f"{self.capif_https_url}{publish_url.replace('<apfId>', APF_api_prov_func_id)}{api_id}"
        cert = (
            os.path.join(self.provider_folder, f"apf-{apf_number}.crt"),
            os.path.join(self.provider_folder,
                         f"APF-{apf_number}_private_key.key"),
        )

        self.logger.info(f"Publishing services to URL: {url}")

        try:
            response = requests.put(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
                cert=cert,
                verify=os.path.join(self.provider_folder, "ca.crt"),
            )
            response.raise_for_status()
            self.logger.info("Services updated successfully")

            # Save response to file
            capif_response_text = response.text

            capif_response_json = json.loads(capif_response_text)

            # Default name if apiName is missing
            file_name = capif_response_json.get("apiName", "default_name")
            id = capif_response_json.get("apiId", "default_id")
            directory = self.provider_folder

            # Iterate over all files in the directory
            for filename in os.listdir(directory):
                path = os.path.join(directory, filename)

                # Check if the file starts with 'CAPIF-'

                if filename.startswith("CAPIF-") and id in filename:

                    # Exit the loop if the file is deleted
                    os.remove(path)
                    break

            output_path = os.path.join(
                self.provider_folder, f"capif_{file_name}_{id}_api.json")

            with open(output_path, "w") as outfile:
                outfile.write(capif_response_text)
            self.logger.info(f"CAPIF response saved to {output_path}")
            output_path = os.path.join(

                self.provider_folder, "provider_service_ids.json")

            # Read the existing file of published APIs
            provider_service_ids = {}
            if os.path.exists(output_path):
                with open(output_path, "r") as outfile:
                    provider_service_ids = json.load(outfile)

            keys_to_remove = [key for key,
                              value in provider_service_ids.items() if value == id]
            for key in keys_to_remove:
                del provider_service_ids[key]
            # Add the new id of the published API

            provider_service_ids[file_name] = id
            self.provider_service_ids = provider_service_ids

            # Update the file with the published APIs
            with open(output_path, "w") as outfile:
                json.dump(provider_service_ids, outfile, indent=4)
            self.logger.info(
                f"API '{file_name}' with ID '{id}' added to Published Apis.")
            return json.loads(capif_response_text)
        except requests.RequestException as e:
            self.logger.error(
                f"Request to CAPIF failed: {e} - Response: {response.text}")
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error during service publication: {e} - Response: {response.text}")
            raise

    def offboard_provider(self) -> None:
        """
        Offboards and deregisters the NEF (Network Exposure Function).
        """
        try:
            self.offboard_nef()
            self.__remove_files()
            self.logger.info(
                "Provider offboarded and deregistered successfully.")
        except Exception as e:
            self.logger.error(
                f"Failed to offboard and deregister Provider: {e}")
            raise

    def offboard_nef(self) -> None:
        """
        Offboards the NEF (Network Exposure Function) from CAPIF.
        """
        try:
            self.logger.info("Offboarding the provider")

            # Load CAPIF API details
            capif_api_details = self._load_provider_api_details()
            url = f"{self.capif_https_url}api-provider-management/v1/registrations/{capif_api_details['capif_registration_id']}"

            # Define certificate paths
            cert_paths = (
                os.path.join(self.provider_folder, "amf.crt"),
                os.path.join(self.provider_folder, "AMF_private_key.key")
            )

            # Send DELETE request to offboard the provider
            response = requests.delete(
                url,
                cert=cert_paths,
                verify=os.path.join(self.provider_folder, "ca.crt")
            )

            response.raise_for_status()
            self.logger.info("Offboarding performed successfully")

        except requests.exceptions.RequestException as e:
            self.logger.error(
                f"Error offboarding Provider: {e} - Response: {response.text}")
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error: {e} - Response: {response.text}")
            raise

    def __remove_files(self):
        self.logger.info("Removing files generated")
        try:
            folder_path = self.provider_folder

            if os.path.exists(folder_path):
                # Deletes all content within the folder, including files and subfolders
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        os.remove(os.path.join(root, file))
                    for dir in dirs:
                        shutil.rmtree(os.path.join(root, dir))
                os.rmdir(folder_path)
                self.logger.info(
                    f"All contents in {folder_path} removed successfully.")
            else:
                self.logger.warning(f"Folder {folder_path} does not exist.")
        except Exception as e:
            self.logger.error(f"Error during removing folder contents: {e}")
            raise

    def _load_provider_api_details(self) -> dict:
        """
        Loads NEF API details from the CAPIF provider details JSON file.

        :return: A dictionary containing NEF API details.
        :raises FileNotFoundError: If the CAPIF provider details file is not found.
        :raises json.JSONDecodeError: If there is an error decoding the JSON file.
        """
        file_path = os.path.join(self.provider_folder,
                                 "provider_capif_ids.json")

        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(
                f"Error decoding JSON from file {file_path}: {e}")
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error while loading NEF API details: {e}")
            raise

    def update_provider(self):
        self.certs_modifications()

        capif_postauth_info = self.__save_capif_ca_root_file_and_get_auth_token()
        capif_onboarding_url = capif_postauth_info["ccf_api_onboarding_url"]
        access_token = capif_postauth_info["access_token"]
        ccf_publish_url = capif_postauth_info["ccf_publish_url"]
        onboarding_response = self.update_onboard(
            capif_onboarding_url, access_token)

        capif_registration_id = onboarding_response["apiProvDomId"]
        self.__write_to_file(
            onboarding_response, capif_registration_id, ccf_publish_url
        )

    def certs_modifications(self):
        self.logger.info("Starting certificate removal process...")

        # List of possible certificate patterns to remove
        cert_patterns = ["APF-", "apf-", "AEF-", "aef-"]
        cert_extensions = ["_private_key.key", "_public.csr", ".crt"]

        # Iterate over the directory and remove matching files
        for file_name in os.listdir(self.provider_folder):
            if any(file_name.startswith(pattern) for pattern in cert_patterns) and any(file_name.endswith(ext) for ext in cert_extensions):
                file_path = os.path.join(self.provider_folder, file_name)
                try:
                    os.remove(file_path)
                    self.logger.info(f"Removed certificate file: {file_name}")
                except Exception as e:
                    self.logger.error(f"Error removing {file_name}: {e}")

        self.logger.info("Certificate removal process completed.")

    def update_onboard(self, capif_onboarding_url, access_token):
        self.logger.info(
            "Onboarding Provider to CAPIF and waiting signed certificate by giving our public keys to CAPIF")
        api_details = self._load_provider_api_details()
        capif_id = "/" + api_details["capif_registration_id"]

        url = f"{self.capif_https_url}{capif_onboarding_url}{capif_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # Create the list of unindexed roles
        roles = ["AMF"]
        for n in range(1, self.aefs + 1):
            roles.append("AEF")

        for n in range(1, self.apfs + 1):
            roles.append("APF")

        # Build the payload with unindexed roles
        payload = {
            "apiProvFuncs": [
                {"regInfo": {"apiProvPubKey": ""}, "apiProvFuncRole": role,
                    "apiProvFuncInfo": f"{role.lower()}"}
                for role in roles
            ],
            "apiProvDomInfo": "This is provider",
            "suppFeat": self.supported_features,
            "failReason": "string",
            "regSec": access_token,
        }

        # Generate the indexed roles for certificate creation
        indexed_roles = ["AMF"] + [f"AEF-{n}" for n in range(1, self.aefs + 1)] + [
            f"APF-{n}" for n in range(1, self.apfs + 1)]

        # Iterate over each API provider function
        for i, api_func in enumerate(payload["apiProvFuncs"]):
            # Folder path for providers
            folder_path = self.provider_folder

            # Check if the folder exists
            if os.path.exists(folder_path):
                found_key = False  # Variable to control if a public key has already been found

                # Iterate over the files in the folder
                for root, dirs, files in os.walk(folder_path):
                    for file_name in files:
                        if file_name.endswith(".csr"):
                            # Check if the file starts with the expected role
                            role_prefix = indexed_roles[i]
                            if any(file_name.startswith(prefix) and role_prefix == prefix for prefix in [f"APF-{i+1}", f"AEF-{i+1}", "AMF"]):
                                file_path = os.path.join(root, file_name)

                                # Read the public key from the file
                                with open(file_path, "r") as csr_file:
                                    api_func["regInfo"]["apiProvPubKey"] = csr_file.read(
                                    )

                                found_key = True
                                break

                    if found_key:
                        break

                # If a file with the public key is not found, generate a new key
                if not found_key:

                    public_key = self.__create_private_and_public_keys(
                        indexed_roles[i])
                    api_func["regInfo"]["apiProvPubKey"] = public_key.decode(
                        "utf-8")

        cert = (
            os.path.join(self.provider_folder, "amf.crt"),
            os.path.join(self.provider_folder, "AMF_private_key.key"),
        )

        try:
            response = requests.put(
                url,
                headers=headers,
                data=json.dumps(payload),
                cert=cert,
                verify=os.path.join(self.provider_folder, "ca.crt"),
            )

            response.raise_for_status()
            self.logger.info(
                "Provider onboarded and signed certificate obtained successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(
                f"Onboarding failed: {e} - Response: {response.text}")
            raise

    def _create_or_update_file(self, file_name, file_type, content, mode="w"):
        """
        Create or update a file with the specified content.

        :param file_name: Name of the file (without extension).
        :param file_type: File type or extension (e.g., "txt", "json", "html").
        :param content: Content to write into the file. Can be a string, dictionary, or list.
        :param mode: Write mode ('w' to overwrite, 'a' to append). Default is 'w'.
        """
        # Validate the mode
        if mode not in ["w", "a"]:
            raise ValueError("Mode must be 'w' (overwrite) or 'a' (append).")

        # Construct the full file name
        full_file_name = f"{file_name}.{file_type}"
        full_path = os.path.join(self.provider_folder, full_file_name)

        # Ensure the content is properly formatted
        if isinstance(content, (dict, list)):
            if file_type == "json":
                try:
                    # Serialize content to JSON
                    content = json.dumps(content, indent=4)
                except TypeError as e:
                    raise ValueError(f"Failed to serialize content to JSON: {e}")
            else:
                raise TypeError("Content must be a string when the file type is not JSON.")
        elif not isinstance(content, str):
            raise TypeError("Content must be a string, dictionary, or list.")

        try:
            # Open the file in the specified mode
            with open(full_path, mode, encoding="utf-8") as file:
                file.write(content)

            # Log success based on the mode
            if mode == "w":
                self.logger.info(f"File '{full_file_name}' created or overwritten successfully.")
            elif mode == "a":
                self.logger.info(f"Content appended to file '{full_file_name}' successfully.")
        except Exception as e:
            self.logger.error(f"Error handling the file '{full_file_name}': {e}")
            raise

    def _find_key_by_value(self, data, target_value):
        """
        Given a dictionary and a value, return the key corresponding to that value.

        :param data: Dictionary to search.
        :param target_value: Value to find the corresponding key for.
        :return: Key corresponding to the target value, or None if not found.
        """
        for key, value in data.items():
            if value == target_value:
                return key
        return None

    def _load_config_file(self, config_file: str):
        """Loads the configuration file."""
        try:
            with open(config_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            self.logger.warning(
                f"Configuration file {config_file} not found. Using defaults or environment variables.")
            return {}
    
    def check_invoker_authentication(self, invoker_id, aef_id, api_id, supportedfeatures_rx, cert_rx):
        service_security = self._get_trusted_invokers(invoker_id, aef_id)
        
        # Check if _get_trusted_invokers returned an error and propagate it
        if isinstance(service_security, dict) and "status" in service_security:
            return service_security  

        result = self._check_service_security(service_security, aef_id, api_id, supportedfeatures_rx, cert_rx)

        return result

    def _get_trusted_invokers(self, invoker_id, aef_id):
        if not aef_id:
            return self._problem_details(
                status=500,
                title="Internal Server Error",
                detail="AEF ID is missing.",
                instance=f"/capif-security/v1/trustedInvokers/{invoker_id}",
                cause="MissingAEFId"
            )
        if not invoker_id:
            return self._problem_details(
                status=500,
                title="Internal Server Error",
                detail="Invoker ID is missing.",
                instance=f"/capif-security/v1/trustedInvokers/{invoker_id}",
                cause="MissingAEFId"
            )

        url = f"{self.capif_https_url}/capif-security/v1/trustedInvokers/{invoker_id}?authenticationInfo={True}&authorizationInfo={True}"
        
        provider_details = self._load_provider_api_details()
        key = self._find_key_by_value(data=provider_details, target_value=aef_id)

        if not key:
            return self._problem_details(
                status=500,
                title="Internal Server Error",
                detail=f"No key found for AEF ID: {aef_id}.",
                instance=url,
                cause="KeyNotFound"
            )

        keylow = key.lower()
        cert = (
            os.path.join(self.provider_folder, f"{keylow}.crt"),
            os.path.join(self.provider_folder, f"{key}_private_key.key")
        )

        try:
            response = requests.get(
                url,
                headers={"Content-Type": "application/json"},
                cert=cert,
                verify=os.path.join(self.provider_folder, "ca.crt")
            )
            response.raise_for_status()
            return response.json()  

        except requests.RequestException as e:
            return self._problem_details(
                status=502,
                title="Bad Gateway",
                detail=f"Failed to retrieve trusted invokers: {str(e)}",
                instance=url,
                cause="RequestFailure"
            )

    def _check_service_security(self, service_security, aef_id, api_id, supportedfeatures_rx, cert_rx):
        service_security_selected = self._find_security_info(service_security, aef_id, api_id)

        # If _find_security_info returns an error, propagate it
        if isinstance(service_security_selected, dict) and "status" in service_security_selected:
            return service_security_selected
        
        if service_security_selected["selSecurityMethod"] == "PKI":
            # TOBEDONE
            print("To be done")

        return {"status": 200, "message": {"supportedFeatures": supportedfeatures_rx}}

    def _find_security_info(self, service_security, aef_id, api_id):
        if not service_security or "securityInfo" not in service_security:
            return self._problem_details(
                status=500,
                title="Internal Server Error",
                detail="Service security information is missing or malformed.",
                instance="/capif-security/v1/securityInfo",
                cause="MalformedServiceSecurity"
            )

        for entry in service_security["securityInfo"]:
            if entry["aefId"] == aef_id and entry["apiId"] == api_id:
                return entry

        return self._problem_details(
            status=404,
            title="Security Information Not Found",
            detail=f"No security information found for AEF ID: {aef_id}, API ID: {api_id}.",
            instance=f"/capif-security/v1/securityInfo/{aef_id}/{api_id}",
            cause="SecurityInfoNotFound"
        )

    def _problem_details(self, status, title, detail, instance, cause, invalidParams=None, supportedFeatures=None):
        """Generates the error message structure according to the ProblemDetails standard"""
        problem = {
            "type": "https://example.com/probs/security-error",
            "title": title,
            "status": status,
            "detail": detail,
            "instance": instance,
            "cause": cause
        }
        if invalidParams:
            problem["invalidParams"] = invalidParams
        if supportedFeatures:
            problem["supportedFeatures"] = supportedFeatures
        return problem
