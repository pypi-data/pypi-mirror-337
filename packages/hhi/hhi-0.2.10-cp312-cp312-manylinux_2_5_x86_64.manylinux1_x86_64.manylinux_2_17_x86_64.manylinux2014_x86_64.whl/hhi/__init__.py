"""hhi - HHI photonics PDK"""

from hhi import cells, cells2, config
from hhi.pdk import PDK
from hhi.tech import (
    LAYER,
    LAYER_STACK,
    LAYER_VIEWS,
    constants,
    cross_sections,
)

layer_transitions = {
    (LAYER.M1, LAYER.M2): "taper_dc",
    (LAYER.M2, LAYER.M1): "taper_dc",
}


__all__ = (
    "cells",
    "cells2",
    "config",
    "PDK",
    "LAYER",
    "LAYER_VIEWS",
    "LAYER_STACK",
    "cross_sections",
    "constants",
)
__version__ = "0.2.10"
