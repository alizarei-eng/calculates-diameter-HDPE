# Project Handover — HDPE Pipe Diameter Engineering Library

## Project objective

Develop a traceable Python engineering library that selects and compares standard PE/HDPE pipe sizes using fluid properties, hydraulic constraints and, later, life-cycle cost.

## Engineering decisions

- Initial pipe material family: PE/HDPE.
- Target outside diameter range: 20–1200 mm, subject to verified standard/product data.
- Only documented market-standard OD, wall thickness and SDR combinations may be treated as standard.
- Internal diameter must be derived from the selected standard wall thickness; OD/SDR is only a preliminary approximation.
- Water types must remain distinct: freshwater, natural seawater and inland brine.
- EC alone must not be used to infer arbitrary inland-brine composition.
- Pressure inputs to the water-property module are absolute MPa.
- PE grade changes pressure-design capacity, not automatically hydraulic roughness.
- PE100-RC is a crack-resistance designation; it is not assumed to have a different hydraulic roughness from PE100.

## Repository implementation status

### Implemented in this commit

- Stage 3 water-property API.
- Freshwater IAPWS-IF97 path.
- Natural seawater GSW/TEOS-10 salinity and density path.
- Sharqawy seawater viscosity correlation.
- EC unit conversion and input validation.
- Explicit unsupported status for generic inland-brine inference.
- Unit tests and method/source documentation.

### Not yet implemented

- Pipe standard dimensions database.
- PE material pressure-design database.
- Hydraulic module (velocity, Reynolds, friction factor, headloss).
- Diameter screening/optimization.
- Pump energy and total-cost-of-ownership optimization.
- GUI and engineering report generator.
- ITTC numerical reference CSV datasets and regression tests against those tables.

## Next recommended task

Validate the Stage 3 module in a clean Python environment, run the unit tests, compare the Sharqawy regression value against the cited paper and transcribe the ITTC 2024 tables with exact page/table provenance. Then implement Stage 1 pipe-standard data using a verified dimensional standard/catalogue.

## Main references

- IAPWS IF97: https://iapws.org/relguide/IF97-Rev.html
- GSW-Python / TEOS-10: https://teos-10.github.io/GSW-Python/
- Sharqawy et al. (2010): https://web.mit.edu/lienhard/www/papers/journal/Thermophysical_properties_of_seawater-DWT-16-354-2010.pdf
- ITTC 2024: https://ittc.info/media/11764/75-02-01-03.pdf
- PE100+ technical guidance: https://www.pe100plus.com/PE-Pipes/Technical-guidance/model/Design/PE-pressure-pipe/PE-pipe-design-i244.html
- PPI Handbook of PE Pipe: https://plasticpipe.org/
