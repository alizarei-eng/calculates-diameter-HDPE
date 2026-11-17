# PE Pipe Dimensional Database — Method and Limitations

## Purpose

This module provides traceable lookup of documented PE pipe dimensions and a small geometry helper. It is the first implementation of Roadmap Stage 1.

## Current dataset

The initial dataset contains 22 PE100 SDR11 nominal OD / nominal wall-thickness pairs from 32 mm through 630 mm. Values are transcribed from the PE100 dimensions table on page 2 of BSI Kitemark Licence KM 546725, which cites ISO 4427-2:2007.

This is a deliberately limited starter dataset. It is not a complete copy of ISO 4427, and the cited licence is historical. Before procurement, pressure design, or issue of a certified engineering calculation, check the current controlled edition of ISO 4427-2 and the actual manufacturer's datasheet.

## API

- `load_pipe_database()`: load the JSON database.
- `list_available_pipes(material_grade=None, sdr=None)`: list documented records.
- `get_pipe_dimensions(dn_od_mm, sdr, material_grade="PE100")`: exact lookup; missing combinations raise `PipeDatabaseError`.
- `calculate_internal_diameter(dn_od_mm, wall_thickness_mm)`: calculate geometric ID from an explicitly supplied thickness.
- `get_pipe_geometry(...)`: lookup plus nominal ID calculation.

## Geometry

Nominal geometric internal diameter is calculated as:

`ID = OD - 2e`

where OD is nominal outside diameter and e is the documented nominal wall thickness.

This is a nominal geometric value, not a guaranteed minimum flow bore. Actual internal diameter depends on outside-diameter tolerance, wall-thickness tolerance, ovality, manufacturing and installation conditions. Those tolerance fields are not yet included in the initial dataset.

## Data policy

- No missing OD/SDR combination is generated from a formula.
- OD/SDR is not used to overwrite a published nominal wall thickness.
- Material grade, dimensional standard and source are stored with each record.
- Data with incomplete verification must remain clearly labelled as an initial catalogue transcription.
- SDR11 is the only included SDR in this first dataset. Additional SDR series will be added after source tables are selected and checked.

## Source

BSI Kitemark Licence No. KM 546725, ISO 4427-2:2007, page 2:
https://tsscgroup.com/wp-content/uploads/2017/09/KM-ISO-4427.pdf

A current ISO 4427-2:2019 catalogue overview is available at:
https://www.standards.iteh.ai/catalog/standards/iso/b2350076-a85e-4eaf-a158-5720ee090324/iso-4427-2-2019

The online catalogue is a discovery aid; use the controlled standard for formal engineering work.
