# Reference data policy

This directory is reserved for numerical reference datasets used in regression tests.

No ITTC reference table has been copied into this initial commit. This is intentional: reference values must be transcribed from the controlled source PDF, retain units and page/table provenance, and be independently checked before they become test fixtures.

Planned datasets:

- `ittc_2024_freshwater_10_40C.csv`
- `ittc_2024_seawater_15C_SA_10_40.csv`

Until those files are added, the test suite uses physical consistency checks and a published Sharqawy viscosity regression point. Do not create synthetic values and label them as ITTC data.
