# Project Handover — HDPE Pipe Diameter Engineering Library

## Project objective

Develop a traceable Python engineering library that selects and compares standard PE/HDPE pipe sizes using fluid properties, hydraulic constraints and life-cycle cost.

## Engineering decisions

- Initial pipe material family: PE/HDPE.
- Target outside diameter range: 20–1200 mm, subject to verified standard/product data.
- Only documented market-standard OD, wall thickness and SDR combinations may be treated as standard.
- Internal diameter must be derived from the selected documented wall thickness; OD/SDR is not used as a substitute for nominal thickness.
- Water types remain distinct: freshwater, natural seawater and inland brine.
- EC alone must not be used to infer arbitrary inland-brine composition.
- Pressure inputs to the water-property module are absolute MPa.
- PE grade changes pressure-design capacity, not automatically hydraulic roughness.
- PE100-RC is a crack-resistance designation; it is not assumed to have a different hydraulic roughness from PE100.

## Repository implementation status

### Implemented

- Stage 3 water-property API: IAPWS-IF97 freshwater, GSW/TEOS-10 natural seawater and Sharqawy seawater viscosity.
- EC unit conversion, input validation, warnings and assumptions.
- Explicit unsupported status for generic inland-brine inference from EC alone.
- Initial pipe dimensional database: 22 PE100 SDR11 records, nominal OD 32–630 mm.
- Pipe database API for loading, filtering, exact lookup and nominal ID calculation.
- Initial PE material reference database for PE80, PE100 and PE100-RC, with MRS/design coefficient fields and a material-level MRS/C helper.
- PE100-RC is not assigned an MRS or pressure-rating uplift over PE100.
- Unit tests and method/source documentation for both implemented modules.

### Pipe database limitations

- Initial values are transcribed from BSI Kitemark Licence KM 546725 referring to ISO 4427-2:2007.
- This is a limited historical catalogue transcription, not a complete/current controlled ISO dataset.
- Only SDR11 and PE100 are included.
- OD tolerances, wall-thickness minimum/maximum tolerances, ovality and manufacturer-specific availability are not included.
- Verify against the current controlled ISO 4427-2 edition and actual manufacturer documentation before procurement or formal engineering design.

### Not yet implemented

- Expanded pipe dimensions for other SDR series and full tolerances.
- Complete PE material pressure-design database, including verified temperature derating and manufacturer-specific approvals.
- Hydraulic module (velocity, Reynolds, friction factor, Darcy-Weisbach headloss).
- Standard-size screening/diameter optimization.
- Pump energy and total-cost-of-ownership optimization.
- GUI and engineering report generator.
- ITTC numerical reference CSV datasets and regression tests against those tables.

## Next recommended task

Extend the initial PE material database with verified temperature derating curves and manufacturer-specific compound approvals. Then implement the hydraulic core. Keep pressure-design calculations separate from hydraulic roughness and diameter calculations.

## Main references

- ISO 4427-2:2019 catalogue overview: https://www.standards.iteh.ai/catalog/standards/iso/b2350076-a85e-4eaf-a158-5720ee090324/iso-4427-2-2019
- BSI Kitemark Licence KM 546725, ISO 4427-2:2007, page 2: https://tsscgroup.com/wp-content/uploads/2017/09/KM-ISO-4427.pdf
- IAPWS IF97: https://iapws.org/relguide/IF97-Rev.html
- GSW-Python / TEOS-10: https://teos-10.github.io/GSW-Python/
- Sharqawy et al. (2010): https://web.mit.edu/lienhard/www/papers/journal/Thermophysical_properties_of_seawater-DWT-16-354-2010.pdf
- ITTC 2024: https://ittc.info/media/11764/75-02-01-03.pdf
- ISO 4427-1:2007 material classification table (PE80 / PE100 MRS and design stress): https://studylib.net/doc/27075244/iso-4427-1-2007-hdpe
- PE100+ material designation guidance: https://www.pe100plus.com/PE-Pipes/Technical-guidance/model/Materials/mrs/What-is-the-meaning-of-the-designations-PE80-PE100-PE100-RC-i254.html
- AGRU PE100 / PE100-RC handbook: https://cdn.myvink.be/0a/d1/7971/ps_doc_technical_handbook_pe100_rc_agru_agruline_2015_en_de.pdf
- PE100+ technical guidance: https://www.pe100plus.com/PE-Pipes/Technical-guidance/model/Design/PE-pressure-pipe/PE-pipe-design-i244.html
- PPI Handbook of PE Pipe: https://plasticpipe.org/
