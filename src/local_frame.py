"""Shared Catastro-aligned frame: EPSG:25830 minus the original UTM anchor.
The approximate lat/lon plane in legacy renderers is NOT this frame.
"""
from pyproj import Transformer
from parse_bu import E0, N0
_TRANSFORM = Transformer.from_crs('EPSG:4326', 'EPSG:25830', always_xy=True)
def to_local(lat, lon):
    east, north = _TRANSFORM.transform(lon, lat)
    return east-E0, north-N0
