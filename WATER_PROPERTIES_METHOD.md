# Water Properties Module — Method and Engineering Notes

## 1. Purpose

The module supplies density and viscosity to the later hydraulic calculations. It separates freshwater, natural seawater and inland brine because conductivity does not have the same interpretation for all three.

## 2. Public API

```python
calculate_water_properties(
    temperature_C,
    water_type,
    pressure_MPa_abs=0.101325,
    EC_value=None,
    EC_unit=None,
    conductivity_temperature_mode="in_situ",
    latitude_deg=None,
    longitude_deg=None,
)
```

Pressure is **absolute pressure in MPa**. Gauge pressure must be converted before calling the function.

Supported EC units:

- `uS/cm`, `µS/cm`, `μS/cm`
- `mS/cm`
- `S/m`

Conversions:

- 1 mS/cm = 1,000 µS/cm
- 1 S/m = 10 mS/cm
- 35,000 µS/cm = 35 mS/cm = 3.5 S/m

## 3. Freshwater

The Python `iapws` implementation of IAPWS-IF97 is used for density and dynamic viscosity at the supplied temperature and absolute pressure.

The saturated-liquid state is used to obtain saturation pressure when temperature is within the subcritical range.

Electrical conductivity is retained as contextual water-quality information only. It does not alter the IAPWS freshwater property calculation.

## 4. Natural seawater

### 4.1 Conductivity and Practical Salinity

PSS-78 is applied through:

```python
SP = gsw.SP_from_C(C, t, p)
```

where:

- `C` is conductivity in mS/cm,
- `t` is in-situ temperature in °C (ITS-90 convention),
- `p` is sea pressure in dbar.

Absolute pressure is converted to sea pressure using:

[
p_{sea,dbar}=(p_{abs,MPa}-0.101325)\times100
]

This conversion assumes standard atmospheric reference pressure. If the actual atmospheric pressure is material to the application, the reference should be made configurable in a later revision.

### 4.2 Absolute Salinity

With coordinates, TEOS-10 is called:

```python
SA = gsw.SA_from_SP(SP, p_sea_dbar, longitude, latitude)
```

Without coordinates, the code uses Reference Salinity:

[
S_R=\frac{35.16504}{35}SP
]

and explicitly warns that the local Absolute Salinity anomaly is omitted.

### 4.3 Density

The code converts in-situ temperature to Conservative Temperature and then evaluates TEOS-10 density:

```python
CT = gsw.CT_from_t(SA, t, p_sea_dbar)
rho = gsw.rho(SA, CT, p_sea_dbar)
```

### 4.4 Dynamic viscosity

Sharqawy et al. (2010), Eqs. 22–23:

[
\mu_{sw}=\mu_w(1+A S+B S^2)
]

[
A=1.541+1.998\times10^{-2}t-9.52\times10^{-5}t^2
]

[
B=7.974-7.561\times10^{-2}t+4.724\times10^{-4}t^2
]

[
\mu_w=4.2844\times10^{-5}+
\left[0.157(t+64.993)^2-91.296\right]^{-1}
]

Here `t` is °C and `S` is salinity mass fraction in kg/kg. The API accepts salinity in g/kg and converts it internally by dividing by 1000.

The documented correlation range is 0 < t < 180 °C and 0 < S < 0.15. This is the correlation's range, not a blanket guarantee that every seawater state is valid in TEOS-10 at every such temperature.

## 5. Inland brines and RO reject

EC-to-salinity conversion is composition-dependent. A sodium-chloride brine, sulfate-rich groundwater and mixed RO reject can have different relationships between conductivity, mass fraction, density and viscosity.

Therefore, `water_type="inland_brine"` raises `NotImplementedError` in this version. A future implementation should require either:

- a complete ionic analysis and an appropriate thermodynamic model, or
- a site-specific EC-to-composition/property calibration with documented range and uncertainty.

Do not route arbitrary brine through PSS-78.

## 6. Temperature-compensated conductivity

PSS-78 requires conductivity measured at the in-situ temperature. A meter's EC value normalized to 25 °C cannot be treated as raw conductivity unless its compensation algorithm is known and reversed.

This version rejects any `conductivity_temperature_mode` other than `"in_situ"` for seawater.

## 7. Output fields

The result dictionary includes:

- model and method description,
- Practical Salinity and Absolute Salinity where applicable,
- density (kg/m³),
- dynamic viscosity (Pa·s),
- kinematic viscosity (m²/s),
- vapor pressure where implemented,
- warnings, assumptions and validity notes.

Seawater vapor pressure is left as `None` in this release. The module does not substitute a freshwater vapor-pressure value for seawater.

## 8. Validation plan

Current tests cover:

- EC unit conversions,
- rejection of unsupported units,
- rejection of inland-brine inference from EC alone,
- rejection of compensated EC in the PSS-78 path,
- positivity and consistency of calculated properties,
- the Sharqawy 15 °C / 35.16504 g/kg regression point.

Next validation task: transcribe the ITTC 2024 freshwater and seawater reference tables into CSV files, with page/table provenance, then add tolerance-based regression tests. Reference values must not be guessed or fabricated.

## 9. References

1. IAPWS, IF97: https://iapws.org/relguide/IF97-Rev.html
2. IAPWS, viscosity release: https://iapws.org/relguide/visc.pdf
3. GSW-Python: https://teos-10.github.io/GSW-Python/
4. Sharqawy, Lienhard & Zubair (2010): https://web.mit.edu/lienhard/www/papers/journal/Thermophysical_properties_of_seawater-DWT-16-354-2010.pdf
5. ITTC 2024, 7.5-02-01-03 Rev 03: https://ittc.info/media/11764/75-02-01-03.pdf
