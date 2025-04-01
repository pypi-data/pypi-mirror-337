import argparse
import base64
import datetime
import json
import os
import sys
import requests


def get_license_data_from_api(license_key):
    api_url = (
        "https://api.keygen.sh/v1/accounts/bluelightai/licenses/actions/validate-key"
    )
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
    }
    payload = {"meta": {"key": license_key}}
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=20)
    except Exception:
        print(
            "Could not connect to license server.\n"
            "Please check that you are connected to the internet and that your firewall allows HTTPS connections to "
            "api.keygen.sh.\nContact support@bluelightai.com with any questions."
        )
        sys.exit()

    if 500 <= response.status_code < 600:
        print(
            "Could not connect to license server. "
            "Please check that you are connected to the internet and that your firewall allows HTTPS connections to "
            "api.keygen.sh. Contact support@bluelightai.com with any questions."
        )
        sys.exit()
    response = response.json()
    if "errors" in response or not response.get("data"):
        print(
            "Could not retrieve license key information from server. Please check the key."
        )
        sys.exit()

    return response


def decrypt_license(enc, license_key):
    from cryptography.exceptions import InvalidKey, InvalidTag
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    try:
        ciphertext, iv, tag = map(base64.b64decode, enc.split("."))
        digest = hashes.Hash(algorithm=hashes.SHA256(), backend=default_backend())
        digest.update(data=license_key.encode())
        key = digest.finalize()

        aes = Cipher(
            algorithm=algorithms.AES(key=key),
            mode=modes.GCM(initialization_vector=iv, tag=tag),
            backend=default_backend(),
        )

        dec = aes.decryptor()
        plaintext = dec.update(ciphertext) + dec.finalize()
        return json.loads(plaintext.decode())
    except (InvalidKey, InvalidTag):
        raise ValueError("Decryption failed: Invalid license key") from None


def get_license_file_payload(license_file_path: str, license_key: str) -> dict:
    try:
        with open(license_file_path, "r", encoding="utf-8") as f:
            license_file_contents = f.read()
    except FileNotFoundError as e:
        raise e

    payload = license_file_contents.replace(
        "-----BEGIN LICENSE FILE-----\n", ""
    ).replace("-----END LICENSE FILE-----\n", "")
    payload_dict = json.loads(base64.b64decode(payload))

    license_data = decrypt_license(payload_dict["enc"], license_key)
    return license_data


def print_license_data(license_file_path: str, license_key: str):
    use_license_file = False
    if license_file_path:
        try:
            license_data = get_license_file_payload(license_file_path, license_key)
            use_license_file = True
        except FileNotFoundError:
            print(f"License file does not exist at path: {license_file_path}")
            print("Attempting to retrieve license data from server.")
            license_data = get_license_data_from_api(license_key)
        except Exception:
            print(
                "Could not read license file. Attempting to retrieve license data from server."
            )
            license_data = get_license_data_from_api(license_key)
    else:
        try:
            license_data = get_license_data_from_api(license_key)
        except Exception:
            sys.exit()

    data = license_data.get("data")
    if not data or "attributes" not in data:
        print(
            "License information not found. Please double check the key and/or license file."
        )
        sys.exit()

    attributes = data.get("attributes")
    if not attributes:
        print(
            "License information not found. Please double check the key and/or license file."
        )
        sys.exit()

    metadata = attributes.get("metadata", {})

    try:
        product_id = data["relationships"]["product"]["data"]["id"]
    except KeyError:
        product_id = None
    product_name = (
        "Cobalt" if product_id == "a9dbb072-eb38-4bd0-a32a-1327138cabbd" else None
    )
    product_code = (
        "8358-0" if product_id == "a9dbb072-eb38-4bd0-a32a-1327138cabbd" else None
    )

    start_date_str = metadata.get("licenseStart")
    if not start_date_str:
        start_date_str = attributes.get("created")
    end_date_str = attributes.get("expiry")

    if start_date_str:
        start_date = datetime.datetime.fromisoformat(start_date_str).astimezone()
    else:
        start_date = None
    if end_date_str:
        end_date = datetime.datetime.fromisoformat(end_date_str).astimezone()
    else:
        end_date = None

    product_description = metadata.get("productDescription") or product_name
    license_description = metadata.get("licenseDescription")
    product_code = metadata.get("productCode") or product_code
    user = metadata.get("name")
    email = metadata.get("email")
    company = metadata.get("company")

    site_name = metadata.get("siteName") or company
    site_id = metadata.get("siteId")
    site_contact_name = metadata.get("siteContactName") or user
    site_contact_email = metadata.get("siteContactEmail") or email
    is_noncommercial = metadata.get("licenseType") == "noncommercial"

    print()
    print("BluelightAI License Information")
    print("===============================")
    if use_license_file:
        print(f"License file: {license_file_path}")
    print(f"License key: {license_key}")
    print()
    if product_description:
        print(f"Product: {product_description}")
    if product_code:
        print(f"Product code: {product_code}")
    if license_description:
        print(license_description)

    print()
    if start_date:
        print(f"License start date: {start_date.strftime('%Y-%m-%d %H:%M')}")
    if end_date:
        print(f"License end date: {end_date.strftime('%Y-%m-%d %H:%M')}")

    print()
    if site_name:
        print(f"Site Name: {site_name}")
    if site_id:
        print(f"Site ID: {site_id}")
    if site_contact_name:
        print(f"Site Contact: {site_contact_name}")
    if site_contact_email:
        print(f"Site Contact Email: {site_contact_email}")

    if is_noncommercial:
        print()
        print("This license is for noncommercial use only.")
        print(
            "Please contact hello@bluelightai.com for information about upgrading to a commercial license."
        )


def main():
    parser = argparse.ArgumentParser(
        description="Show details for a BluelightAI license."
    )
    parser.add_argument(
        "--license-key",
        type=str,
        help="The license key to process. If not provided, will check for a key in the COBALT_LICENSE_KEY environment variable or in the ~/.config/cobalt/cobalt.json config file.",
    )
    parser.add_argument(
        "--license-file",
        type=str,
        help="Path to the license file. If not provided, will check for a file at ~/.config/cobalt/license.lic.",
    )

    args = parser.parse_args()

    config_dir = os.path.join(os.path.expanduser("~"), ".config", "cobalt")

    if args.license_key:
        license_key = args.license_key
    else:
        print("No license key provided. Checking for license in environment variable.")
        license_key = os.getenv("COBALT_LICENSE_KEY")
        if not license_key:
            print(
                "License key not found in environment variable. Checking Cobalt config file."
            )
            try:
                with open(
                    os.path.join(config_dir, "cobalt.json"), encoding="utf-8"
                ) as config_file:
                    config_data = json.load(config_file)
                license_key = config_data.get("license_key")
                if not license_key:
                    print(
                        "No license key found. Please provide a license key with flag --license-key."
                    )
                    sys.exit()
            except FileNotFoundError:
                print(
                    "No config file found. Please provide a license key with flag --license-key."
                )
                sys.exit()

    if args.license_file:
        if os.path.exists(args.license_file):
            license_file_path = args.license_file
        else:
            print(f"License file does not exist at provided path: {args.license_file}")
            sys.exit()
    else:
        print(
            "No license file path provided. Checking for license file in Cobalt config."
        )
        license_file_path = os.path.join(config_dir, "license.lic")
    print_license_data(license_file_path, license_key)


if __name__ == "__main__":
    main()
