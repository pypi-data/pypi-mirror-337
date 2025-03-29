"""
Pre Checks Country

Load the complete country data from HESTIA to be able to use `subClassOf` for example.
"""
from hestia_earth.utils.api import download_hestia


def run(site: dict): return site | {'country': download_hestia(site.get('country', {}).get('@id'))}
