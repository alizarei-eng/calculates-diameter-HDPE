# PE Material Database — Method and Limitations

## 1. Purpose

This stage stores traceable reference classifications for PE80, PE100 and PE100-RC. It is separate from the pipe dimensional database and hydraulic calculations.

## 2. MRS and design stress

MRS is the Minimum Required Strength classification derived from long-term hydrostatic-strength regression and classified under ISO 12162. The reference condition is 20 °C and 50 years.

| Grade | MRS (MPa) | Minimum design coefficient for water | Reference design stress (MPa) |
|---|---:|---:|---:|
| PE80 | 8.0 | 1.25 | 6.3 |
| PE100 | 10.0 | 1.25 | 8.0 |
| PE100-RC | 10.0 | 1.25 | 8.0 |

The material-level calculation is:

\[
\sigma_s = \frac{MRS}{C}
\]

The reference_design_stress_MPa field records the tabulated ISO 4427 reference value. The API calculates MRS/C for a selected coefficient; small differences can occur because tabulated stress values are rounded/classified in the product standard.

## 3. PE100-RC interpretation

PE100-RC has the PE100 MRS classification (10 MPa). The RC designation identifies enhanced resistance to slow crack growth; it must not be interpreted as a higher MRS or automatically higher pressure class. Compound qualification and product compliance must be verified from the actual manufacturer and applicable product standard.

## 4. Scope restrictions

This database does not yet include temperature derating factors or material-specific pressure-temperature curves, manufacturer-specific compound grades or approvals, chemical compatibility, surge/water-hammer or installation factors, or complete PN/MOP tables.

Consequently, the API intentionally does not calculate a pipe pressure rating. A later pressure-design module must combine a verified material classification, actual pipe dimensions/SDR, application-specific design coefficient, temperature/lifetime basis, product standard and transient design cases.

The default coefficient 1.25 is a reference minimum for water applications in the cited PE guidance. It is not a universal project coefficient. More demanding applications may require a higher coefficient under the governing code and engineering assessment.

## 5. Sources

1. ISO 4427-1:2007 material classification table: PE100 MRS 10 MPa / design stress 8 MPa; PE80 MRS 8 MPa / design stress 6.3 MPa.
2. PE100+ Association, PE80/PE100/PE100-RC material designations: https://www.pe100plus.com/PE-Pipes/Technical-guidance/model/Materials/mrs/What-is-the-meaning-of-the-designations-PE80-PE100-PE100-RC-i254.html
3. PE100+ Association, pressure design and design coefficient guidance: https://www.pe100plus.com/PE-Pipes/Technical-guidance/model/Design/PE-pressure-pipe/PE-pipe-design-i244.html
4. ISO 4427-1:2019 terminology preview: https://gso-sims-preview-doc-aws.s3-eu-west-1.amazonaws.com/iso-4427-1-2019-en.html
5. AGRU PE100 / PE100-RC handbook: https://cdn.myvink.be/0a/d1/7971/ps_doc_technical_handbook_pe100_rc_agru_agruline_2015_en_de.pdf

Online guidance and standard previews are explanatory references, not substitutes for controlled copies of current applicable standards or the selected manufacturer's technical file.
