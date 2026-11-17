# HDPE Pipe Diameter Engineering Library

A modular Python engineering library for water-property calculations that will support hydraulic pipe sizing and optimization for PE/HDPE pipelines.

## Current scope

This initial repository release implements **Stage 3: water properties**:

- Freshwater density, dynamic viscosity and saturation pressure using IAPWS-IF97.
- Natural seawater practical salinity using PSS-78 through GSW (TEOS-10), followed by Absolute Salinity and density.
- Seawater dynamic viscosity using the Sharqawy et al. (2010) correlation.
- Explicit rejection of inland brines when only EC is supplied; EC alone is not a universal salinity measurement.
- Input validation, assumptions and warnings returned with every result.

Hydraulic calculations, standard pipe dimensions and the diameter optimizer are planned subsequent stages and are not represented as implemented in this release.

## Installation

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

python -m pip install -r requirements.txt
```

## Quick example

```python
from core.water_properties import calculate_water_properties

result = calculate_water_properties(
    temperature_C=25.0,
    water_type="freshwater",
    pressure_MPa_abs=0.101325,
)

print(result["density_kg_m3"])
print(result["dynamic_viscosity_Pa_s"])
print(result["warnings"])
```

For natural seawater, provide **raw, in-situ conductivity** and its measured temperature:

```python
result = calculate_water_properties(
    temperature_C=15.0,
    water_type="seawater",
    EC_value=42.914,       # Example only: mS/cm; replace with measured raw EC
    EC_unit="mS/cm",
    conductivity_temperature_mode="in_situ",
    pressure_MPa_abs=0.101325,
    latitude_deg=27.0,
    longitude_deg=56.0,
)
```

The example EC value is illustrative and is not a site measurement.

## Important engineering limitations

1. The seawater path is intended for natural seawater compatible with PSS-78. Do not use it for industrial brines, produced water or concentrated RO reject without a validated chemistry-specific model.
2. Conductivity compensated to 25 °C must not be passed as in-situ conductivity. The compensation algorithm would need to be known and reversed first.
3. When latitude and longitude are omitted, Absolute Salinity is approximated from Reference Salinity and a warning is returned.
4. The Sharqawy viscosity correlation is documented for 0 < temperature < 180 °C and 0 < salinity mass fraction < 0.15. The validity range of the underlying seawater state model may be narrower; use engineering judgement and review warnings.
5. The current seawater vapor-pressure field is intentionally not estimated from an unrelated freshwater equation.
6. No pressure design rating is calculated here. PE pressure design requires grade, SDR, temperature derating, design coefficient and applicable standards.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Project layout

```text
core/
  water_properties.py
data/
  DATA_README.md
databases/
  water_properties.json
sources/
  source_register.json
tests/
  test_water_properties.py
WATER_PROPERTIES_METHOD.md
```

## Roadmap

1. Pipe-standard database (OD, wall thickness, SDR and dimensional tolerances).
2. PE material database (MRS, design coefficient and pressure-design references).
3. Hydraulic core (velocity, Reynolds number, friction factor and Darcy-Weisbach loss).
4. Standard-size screening and hydraulic diameter selection.
5. Economic optimization using total cost of ownership (pipe, installation and pumping energy).
6. Engineering report and graphical interface.

See [WATER_PROPERTIES_METHOD.md](WATER_PROPERTIES_METHOD.md) for equations, assumptions and references.
