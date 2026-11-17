# HDPE Pipe Diameter Engineering Library

A modular Python engineering library for PE/HDPE pipe dimensional lookup, water-property calculations, hydraulic sizing and optimization.

## Implemented scope

### Water properties

- Freshwater density, dynamic viscosity and saturation pressure using IAPWS-IF97.
- Natural seawater practical salinity using PSS-78 through GSW (TEOS-10), followed by Absolute Salinity and density.
- Seawater dynamic viscosity using the Sharqawy et al. (2010) correlation.
- Explicit rejection of inland brines when only EC is supplied; EC alone is not a universal salinity measurement.
- Input validation, assumptions and warnings returned with every result.

### Pipe dimensional database — initial release

- JSON database for 22 PE100 SDR11 nominal OD / wall-thickness pairs from 32 mm through 630 mm.
- Exact lookup by material grade, nominal OD and SDR.
- Nominal internal-diameter calculation from the documented nominal wall thickness.
- Missing OD/SDR combinations are rejected; no dimensions are fabricated or inferred.
- Source provenance and limitations are stored with the dataset.

The initial pipe dataset is transcribed from a published BSI Kitemark product licence referring to ISO 4427-2:2007. It is a starter dataset, not a complete or current controlled copy of ISO 4427. Verify dimensions against the current standard edition and the selected manufacturer's datasheet before procurement or engineering release.

## Installation

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

python -m pip install -r requirements.txt
```

## Quick examples

### Water properties

```python
from core.water_properties import calculate_water_properties

result = calculate_water_properties(
    temperature_C=25.0,
    water_type="freshwater",
    pressure_MPa_abs=0.101325,
)
print(result["density_kg_m3"])
print(result["dynamic_viscosity_Pa_s"])
```

### Pipe dimensions

```python
from core.pipe_database import get_pipe_geometry

pipe = get_pipe_geometry(
    dn_od_mm=110,
    sdr=11,
    material_grade="PE100",
)
print(pipe["nominal_wall_thickness_mm"])       # 10.0 mm
print(pipe["nominal_internal_diameter_mm"])    # 90.0 mm
```

The internal diameter above is nominal geometry (OD - 2 × nominal wall thickness), not a guaranteed minimum flow bore. Actual bore depends on dimensional tolerances and product data.

### PE material reference database — initial release

- Reference records for PE80, PE100 and PE100-RC.
- MRS classification, minimum water design-coefficient reference and reference design stress.
- Lookup and material-level design-stress calculation API.
- PE100-RC is recorded with the same MRS as PE100 and enhanced slow-crack-growth resistance; no pressure-rating uplift is assumed.
- Temperature derating, manufacturer-specific approvals and pressure ratings are intentionally not yet implemented.

See [PE_MATERIAL_DATABASE_METHOD.md](PE_MATERIAL_DATABASE_METHOD.md).

## Important engineering limitations

1. The seawater path is intended for natural seawater compatible with PSS-78. Do not use it for industrial brines, produced water or concentrated RO reject without a validated chemistry-specific model.
2. Conductivity compensated to 25 °C must not be passed as in-situ conductivity. The compensation algorithm would need to be known and reversed first.
3. When latitude and longitude are omitted, Absolute Salinity is approximated from Reference Salinity and a warning is returned.
4. The Sharqawy viscosity correlation is documented for 0 < temperature < 180 °C and 0 < salinity mass fraction < 0.15. The validity range of the underlying seawater state model may be narrower; review warnings.
5. Seawater vapor pressure is not estimated in this release.
6. The pipe database currently contains PE100 SDR11 only, OD 32–630 mm. It does not yet contain OD tolerances, wall-thickness tolerance limits, ovality, manufacturer availability or additional SDR series.
7. The pipe dimensional source refers to ISO 4427-2:2007. Verify against the current controlled standard and the actual supplier before formal design/procurement.
8. No complete PE pipe pressure rating is calculated. The material module only returns MRS/C at the 20 °C, 50-year reference basis. Pressure design additionally requires verified dimensions, temperature/lifetime derating, applicable standards, transient loads and manufacturer data.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Project layout

```text
core/
  water_properties.py
  pipe_database.py
  pe_material_database.py
data/
  DATA_README.md
databases/
  water_properties.json
  pipe_standards.json
  pe_materials.json
sources/
  source_register.json
tests/
  test_water_properties.py
  test_pipe_database.py
  test_pe_material_database.py
WATER_PROPERTIES_METHOD.md
PIPE_DATABASE_METHOD.md and PE_MATERIAL_DATABASE_METHOD.md
```

## Roadmap

1. ~~Initial pipe-standard database~~ — limited PE100 SDR11 subset implemented; extend with verified SDR series, tolerances and product sources.
2. ~~PE material reference database~~ — initial PE80/PE100/PE100-RC classification subset implemented; add verified temperature derating and manufacturer data.
3. Hydraulic core (velocity, Reynolds number, friction factor and Darcy-Weisbach loss).
4. Standard-size screening and hydraulic diameter selection.
5. Economic optimization using total cost of ownership (pipe, installation and pumping energy).
6. Engineering report and graphical interface.

See [WATER_PROPERTIES_METHOD.md](WATER_PROPERTIES_METHOD.md) and [PIPE_DATABASE_METHOD.md](PIPE_DATABASE_METHOD.md) for methods, assumptions and references.
