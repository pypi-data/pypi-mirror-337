from hestia_earth.schema import EmissionMethodTier

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.constant import Units, get_atomic_conversion
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.input import total_excreta, total_excreta_tan
from hestia_earth.models.utils.practice import is_model_enabled
from hestia_earth.models.utils.aquacultureManagement import valid_site_type
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "inputs": [{
            "@type": "Input",
            "value": "",
            "term.termType": "excreta",
            "term.units": "kg N",
            "properties": [
                {"@type": "Property", "value": "", "term.@id": "nitrogenContent"},
                {"@type": "Property", "value": "", "term.@id": "totalAmmoniacalNitrogenContentAsN"}
            ]
        }],
        "practices": [{"@type": "Practice", "value": "", "term.termType": "excretaManagement"}]
    }
}
RETURNS = {
    "Emission": [{
        "value": "",
        "methodTier": "tier 1"
    }]
}
TERM_ID = 'n2OToAirAquacultureSystemsDirect'
TIER = EmissionMethodTier.TIER_1.value
EF_Aqua = {'NH3N_N2ON': 0.018, 'OtherN_N2ON': 0.005}


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    return emission


def _run(excr_tan: float, excr_n: float):
    value = EF_Aqua['NH3N_N2ON'] * excr_tan + (EF_Aqua['OtherN_N2ON'] * (excr_n - excr_tan) if excr_n else 0)
    value = value * get_atomic_conversion(Units.KG_N2O, Units.TO_N)
    return [_emission(value)]


def _should_run(cycle: dict):
    inputs = cycle.get('inputs', [])
    excr_n = total_excreta(inputs)
    excr_tan = total_excreta_tan(inputs)
    model_enabled = is_model_enabled(MODEL, TERM_ID, cycle.get('practices', [None])[0])

    set_to_zero = not valid_site_type(cycle)  # if site is not water, set value to 0

    logRequirements(cycle, model=MODEL, term=TERM_ID,
                    model_enabled=model_enabled,
                    excr_n=excr_n,
                    excr_tan=excr_tan,
                    set_to_zero=set_to_zero)

    should_run = all([(model_enabled and (excr_n or excr_tan)) or set_to_zero])
    logShouldRun(cycle, MODEL, TERM_ID, should_run, methodTier=TIER)
    return should_run, excr_tan, excr_n, set_to_zero


def run(cycle: dict):
    should_run, excr_tan, excr_n, set_to_zero = _should_run(cycle)
    return [_emission(0)] if set_to_zero else _run(excr_tan, excr_n) if should_run else []
