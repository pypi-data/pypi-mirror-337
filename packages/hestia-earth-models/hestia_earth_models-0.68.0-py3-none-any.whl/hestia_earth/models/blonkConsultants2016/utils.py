from hestia_earth.utils.model import find_primary_product
from hestia_earth.utils.lookup import extract_grouped_data
from hestia_earth.utils.tools import safe_parse_float

from hestia_earth.models.log import logger
from hestia_earth.models.utils.crop import FAOSTAT_AREA_LOOKUP_COLUMN, get_crop_grouping_faostat_area
from hestia_earth.models.utils.lookup import get_region_lookup_value
from . import MODEL


def get_emission_factor(term_id: str, cycle: dict, factor: str):
    site = cycle.get('site', {})
    country_id = site.get('country', {}).get('@id')
    product = find_primary_product(cycle) or {}
    product_id = product.get('term', {}).get('@id')
    crop_grouping = get_crop_grouping_faostat_area(MODEL, term_id, product.get('term', {}))

    logger.debug('model=%s, country=%s, product=%s, crop_grouping=%s',
                 MODEL, country_id, product_id, f"'{crop_grouping}'")

    lookup_name = f"region-crop-{FAOSTAT_AREA_LOOKUP_COLUMN}-{factor}.csv"
    value = get_region_lookup_value(
        lookup_name, country_id, crop_grouping, model=MODEL, term=term_id
    ) if crop_grouping else get_region_lookup_value(
        lookup_name, country_id, 'NONE', model=MODEL, term=term_id
    )

    data = safe_parse_float(value, None)
    # fallback to site.siteType data if possible
    return data if data is not None else safe_parse_float(extract_grouped_data(value, site.get('siteType')), None)
