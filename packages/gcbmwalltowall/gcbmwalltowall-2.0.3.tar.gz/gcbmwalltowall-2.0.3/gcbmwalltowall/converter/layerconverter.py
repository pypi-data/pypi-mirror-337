from __future__ import annotations
import logging
from pathlib import Path
from tempfile import TemporaryDirectory
from arrow_space.input.attribute_table_reader import InMemoryAttributeTableReader
from pandas import DataFrame
from arrow_space.input.raster_input_layer import RasterInputLayer
from arrow_space.input.raster_input_layer import RasterInputSource
from mojadata.config import GDAL_CREATION_OPTIONS
from mojadata.util import gdal
from mojadata.util.gdal_calc import Calc

class LayerConverter:
    
    def __init__(self, *args, temp_dir: Path | str = None, **kwargs):
        if temp_dir:
            self._temp_dir = Path(temp_dir)
        else:
            self._temp_dir_ref = TemporaryDirectory()
            self._temp_dir = Path(self._temp_dir_ref.name)
    
    def handles(self, layer: PreparedLayer) -> bool:
        raise NotImplementedError()

    def convert(self, layers: list[PreparedLayer]) -> list[RasterInputLayer]:
        return self.convert_internal([l for l in layers if self.handles(l)])

    def convert_internal(self, layers: list[PreparedLayer]) -> list[RasterInputLayer]:
        raise NotImplementedError()


class DelegatingLayerConverter(LayerConverter):
    
    def __init__(self, converters: list[LayerConverter], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._converters = converters
    
    def handles(self, layer: PreparedLayer) -> bool:
        return any((c.handles(layer) for c in self._converters))
    
    def convert_internal(self, layers: list[PreparedLayer]) -> list[RasterInputLayer]:
        results = []
        for subconverter in self._converters:
            results.extend(subconverter.convert(layers))

        return results


class DefaultLayerConverter(LayerConverter):
    
    def __init__(self, name_remappings: dict[str, str] = None, include_disturbances: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name_remappings = name_remappings or {}
        self._include_disturbances = include_disturbances
    
    def handles(self, layer: PreparedLayer) -> bool:
        _handles = layer.name not in {"initial_current_land_class"}
        if not self._include_disturbances:
            _handles = _handles and "disturbance" not in layer.study_area_metadata.get("tags", [])

        return _handles

    def convert_internal(self, layers: list[PreparedLayer]) -> list[RasterInputLayer]:
        if not layers:
            return []
        
        logging.info(f"Converting layers: {', '.join((l.name for l in layers))}")

        return [
            RasterInputLayer(
                self._name_remappings.get(layer.name, layer.name),
                [RasterInputSource(path=str(layer.path))],
                self._build_attribute_table(layer),
                layer.study_area_metadata.get("tags")
            ) for layer in layers
        ]

    def _build_attribute_table(self, layer: PreparedLayer) -> DataFrame:
        gcbm_attribute_table = layer.tiler_metadata.get("attributes")
        if not gcbm_attribute_table:
            return None
        
        rows = []
        for att_id, att_value in gcbm_attribute_table.items():
            row = {"id": int(att_id)}
            if isinstance(att_value, dict):
                row.update({k: v for k, v in att_value.items() if k != "conditions"})
            else:
                row.update({"value": att_value})
            
            rows.append(row)

        return InMemoryAttributeTableReader(DataFrame(rows))


class LandClassLayerConverter(LayerConverter):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def handles(self, layer: PreparedLayer) -> bool:
        return layer.name == "initial_current_land_class"

    def convert_internal(self, layers: list[PreparedLayer]) -> list[RasterInputLayer]:
        layer = next(iter(layers), None)
        if not layer:
            return []
        
        logging.info(f"Converting layer: {layer.name}")
        
        gcbm_cbm4_landclass_lookup = {
            "FL": 0,
            "CL": 1,
            "GL": 2,
            "WL": 3,
            "SL": 4,
            "OL": 5,
            "UFL": 16,
        }
        
        original_ndv = layer.tiler_metadata["nodata"]
        new_ndv = 32767

        px_calcs = (
            f"((A == {original_px}) * {gcbm_cbm4_landclass_lookup.get(gcbm_landclass, new_ndv)})"
            for original_px, gcbm_landclass in layer.tiler_metadata["attributes"].items()
        )

        calc = "+".join((
            f"((A == {original_ndv}) * {new_ndv})",
            *px_calcs
        ))

        output_path = Path(self._temp_dir.name).joinpath(f"{layer.name}.tif")
        Calc(calc, str(output_path), new_ndv, quiet=True, creation_options=GDAL_CREATION_OPTIONS,
             overwrite=True, hideNoData=False, type=gdal.GDT_Int16, A=layer.path)
        
        return [
            RasterInputLayer(
                "land_class",
                [RasterInputSource(path=str(output_path))],
                tags=layer.study_area_metadata.get("tags")
            )
        ]
