"""PDK."""

import gdsfactory as gf
from cachetools.func import ttl_cache
from gdsfactory.get_factories import get_cells

from hhi import cells, cells2
from hhi.models import models
from hhi.tech import (
    LAYER,
    LAYER_STACK,
    LAYER_VIEWS,
    MATERIALS_INDEX,
    constants,
    cross_sections,
)

cells_dict = get_cells([cells, cells2])


class LicenseError(ValueError):
    """License error."""

    pass


@ttl_cache(ttl=600)
def check_license() -> bool:
    """Check if the user of the library has a license to use the pdk."""
    from gdsfactoryplus.core.shared import validate_access

    pdk_name = "hhi"
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwZGsiOiJkYTIzYmRjOC05ZDMwLTQ1ZTEtYjY4ZS04MzYxODYzODI0ZjgiLCJhdWQiOiJHRFNGYWN0b3J5OnBka3MifQ.EwpDlsUEXqjlgu8ZyeKwA4GaVYFAwJrX_ynS_kJac5Q"

    try:
        validate_access(pdk_name, pdk_key=access_token, check_pdk_access=True)
    except ValueError as e:
        raise LicenseError(
            "Invalid GFP_API_KEY.\nPlease contact contact@gdsfactory.com."
        ) from e
    return True


check_license()


layer_transitions = {
    (LAYER.M1, LAYER.M2): "taper_dc",
    (LAYER.M2, LAYER.M1): "taper_dc",
}

PDK = gf.Pdk(
    name="HHI",
    cells=cells_dict,
    cross_sections=cross_sections,
    layers=LAYER,
    layer_stack=LAYER_STACK,
    layer_views=LAYER_VIEWS,
    layer_transitions=layer_transitions,
    materials_index=MATERIALS_INDEX,
    constants=constants,
    models=models,
)
PDK.activate()

__all__ = [
    "PDK",
]
