#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vintage Story - Creation of modlist from the mod folder (modlist.json)
"""
__author__ = "Laerinok"
__date__ = "2025-03-19"
__version__ = "1.0.0"

import time
from pathlib import Path
import zipfile
import json
import pathlib
import requests
import re
import urllib.parse
import configparser
import sys


def get_mod_path(config_file="config.ini"):
    config_path = Path(config_file)
    if not config_path.exists():
        print(f"Error: The file '{config_path}' is not found.")
        time.sleep(2)
        sys.exit(1)  # Stop the script with an error code

    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")

    if "ModPath" not in config or "path" not in config["ModPath"]:
        print(f"Error: The section [ModPath] or the key 'path' is missing in '{config_path}'.")
        time.sleep(2)
        sys.exit(1)

    return Path(config["ModPath"]["path"]).resolve()


def fix_json(json_data):
    # Fix 1: Remove final commas
    json_data = re.sub(r",\s*([}\]])", r"\1", json_data)
    return json_data


def is_zip_valid(zip_path):
    """Checks if a zip file is valid and not corrupted."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.testzip()  # Tests the integrity of the zip file
        return True
    except (zipfile.BadZipFile, zipfile.LargeZipFile):
        return False


def get_modinfo_from_zip(zip_path):
    """Gets modid, name, and version information from modinfo.json in a zip file."""
    mod_api = f'https://mods.vintagestory.at/api/mod/'
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Opens modinfo.json inside the zip file
            with zip_ref.open('modinfo.json') as modinfo_file:
                raw_json = modinfo_file.read().decode('utf-8')
                fixed_json = fix_json(raw_json)
                modinfo = json.loads(fixed_json)
                # Convert all keys to lowercase to ignore case
                modinfo_lower = {k.lower(): v for k, v in modinfo.items()}
                mod_url_api = f'{mod_api}{modinfo_lower.get("modid")}'
                return modinfo_lower.get('modid'), modinfo_lower.get('name'), modinfo_lower.get('version'), mod_url_api, modinfo_lower.get('description')
    except Exception as e:
        print(f"Error extracting modinfo.json from {zip_path}: {e}")
        return None, None, None, None


def get_cs_info(cs_path):
    """Gets Version, Side, namespace information from a .cs file."""
    mod_api = f'https://mods.vintagestory.at/api/mod/'
    with open(cs_path, 'r', encoding='utf-8') as cs_file:
        content = cs_file.read()

        # Using regex to extract the values
        version_match = re.search(r'Version\s*=\s*"([^"]+)"', content)
        side_match = re.search(r'Side\s*=\s*"([^"]+)"', content)
        namespace_match = re.search(r'namespace\s+([A-Za-z0-9_]+)', content)
        description_match = re.search(r'Description\s*=\s*"([^"]+)"', content)
        # If the information is found, return it
        version = version_match.group(1) if version_match else None
        side = side_match.group(1) if side_match else None
        description = description_match.group(1) if description_match else None
        namespace = namespace_match.group(1) if namespace_match else None
        modid = namespace.lower().replace(" ", "") if namespace else None
        mod_url_api = f'{mod_api}{modid}'
        return version, side, namespace, modid, mod_url_api, description


def get_mainfile_for_version(mod_version, api_response):
    """
    Retrieves the 'mainfile' link for the given version in modinfo and compares it with the versions in the API file.

    mod_version: the mod version extracted from modinfo.json or a .cs file.
    api_response: the API response containing the version information and 'mainfile'.

    Returns the link for the corresponding 'mainfile'.
    """

    for release in api_response:
        modversion = release.get('modversion', [])
        # Check if the modinfo version is in the tags
        if mod_version == modversion:
            return release.get('mainfile')

    # If no match is found
    print(f"No link found for version {mod_version}.")
    return None


def make_dl_link(mod_file_onlinepath_raw):
    # Common domain
    base_domain = "https://moddbcdn.vintagestory.at/"
    # URL parsing
    parsed_url = urllib.parse.urlparse(mod_file_onlinepath_raw)
    # Extracting the "path" (after the domain)
    file_path = parsed_url.path
    # Extracting parameters (query string)
    params = parsed_url.query
    # Encoding parameters to ensure they are valid in a URL
    encoded_params = urllib.parse.quote(params, safe="=&")
    # Reconstructing the final URL
    mod_file_onlinepath = f"{base_domain}{file_path}?{encoded_params}"
    return mod_file_onlinepath


def get_api_info(modid):
    """Gets, via the API, the assetid and download link for the file corresponding to the mod version."""
    url_api = "https://mods.vintagestory.at/api/mod/"
    url_api_mod = f"{url_api}{modid}"
    try:
        response = requests.get(url_api_mod)
        response.raise_for_status()
        data = response.json()
        mod_asset_id = data['mod']['assetid']
        releases = data['mod']['releases']
        side = data['mod']['side']
        return mod_asset_id, side, releases
    except requests.RequestException:
        print(f"Error fetching API info for {modid}")
        return "", ""


def list_mods(mods_folder):
    """Lists the mods in the specified folder and creates a modlist.json file."""
    url_moddb = f'https://mods.vintagestory.at/show/mod/'
    mods_data = {"Mods": []}
    mods_folder = pathlib.Path(mods_folder)
    invalid_files = []  # List to store invalid or corrupted files

    for file in mods_folder.iterdir():
        if file.suffix == '.zip':
            if is_zip_valid(file):
                modid, name, version, mod_url_dl, description = get_modinfo_from_zip(file)
                if modid and name and version:
                    # Get API info to retrieve version and download link
                    assetid, side, releases = get_api_info(modid)
                    mod_file_onlinepath = get_mainfile_for_version(version, releases)
                    if mod_file_onlinepath:
                        url_mod = f'{url_moddb}{assetid}'
                        mods_data["Mods"].append({
                            "Name": name,
                            "Version": version,
                            "ModId": modid,
                            "Side": side,
                            "Description": description,
                            "url_mod": url_mod,
                            "url_download": mod_file_onlinepath
                        })
                    else:
                        invalid_files.append(file.name)  # If no link found, add to invalid files
                else:
                    invalid_files.append(file.name)  # Add file name to invalid files list
            else:
                invalid_files.append(file.name)  # Add corrupted file name to invalid files list
        elif file.suffix == '.cs':
            version, side, namespace, modid, mod_url_dl, description = get_cs_info(file)
            if version and side and namespace and modid and mod_url_dl:
                assetid, side, releases = get_api_info(modid)
                mod_file_onlinepath = get_mainfile_for_version(version, releases)
                if mod_file_onlinepath:
                    url_mod = f'{url_moddb}{assetid}'
                    mods_data["Mods"].append({
                        "Name": namespace,
                        "Version": version,
                        "ModId": modid,
                        "Side": side,
                        "Description": description,
                        "url_mod": url_mod,
                        "url_download": mod_file_onlinepath
                    })
                else:
                    invalid_files.append(
                        file.name)  # If no link found, add to invalid files list
            else:
                invalid_files.append(file.name)  # Add invalid .cs file name

    # Sort mods alphabetically by "Name"
    mods_data["Mods"].sort(key=lambda mod: mod["ModId"].lower())

    # Save data to modlist.json
    with open('modlist.json', 'w', encoding='utf-8') as json_file:
        json.dump(mods_data, json_file, indent=4, ensure_ascii=False)

    # Display invalid or corrupted files
    if invalid_files:
        print("Invalid or corrupted files:")
        for invalid_file in invalid_files:
            print(f"- {invalid_file}")
    else:
        print("No invalid or corrupted files.")


# Get the path from config.ini
mod_path = get_mod_path()

# Run the function with the retrieved path
list_mods(mod_path)
