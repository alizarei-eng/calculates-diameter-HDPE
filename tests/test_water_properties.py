import math
import unittest

from core.water_properties import (
    calculate_water_properties,
    conductivity_to_ms_cm,
    sharqawy_seawater_viscosity_Pa_s,
)


class TestConductivityConversions(unittest.TestCase):
    def test_micro_siemens_to_millisiemens(self):
        self.assertAlmostEqual(conductivity_to_ms_cm(35000, "uS/cm"), 35.0)

    def test_micro_symbol_variant(self):
        self.assertAlmostEqual(conductivity_to_ms_cm(35000, "µS/cm"), 35.0)

    def test_siemens_per_metre(self):
        self.assertAlmostEqual(conductivity_to_ms_cm(3.5, "S/m"), 35.0)

    def test_unknown_unit_rejected(self):
        with self.assertRaises(ValueError):
            conductivity_to_ms_cm(10, "ppm")

    def test_negative_ec_rejected(self):
        with self.assertRaises(ValueError):
            conductivity_to_ms_cm(-1, "mS/cm")


class TestSharqawyViscosity(unittest.TestCase):
    def test_published_regression_point(self):
        # Sharqawy et al. correlation at 15 °C and 35.16504 g/kg.
        mu = sharqawy_seawater_viscosity_Pa_s(15.0, 35.16504)
        self.assertAlmostEqual(mu, 0.0012203003, delta=2.0e-7)

    def test_invalid_temperature_rejected(self):
        with self.assertRaises(ValueError):
            sharqawy_seawater_viscosity_Pa_s(0.0, 35.0)

    def test_invalid_salinity_rejected(self):
        with self.assertRaises(ValueError):
            sharqawy_seawater_viscosity_Pa_s(20.0, 0.0)


class TestInputValidation(unittest.TestCase):
    def test_inland_brine_rejected_without_model(self):
        with self.assertRaises(NotImplementedError):
            calculate_water_properties(
                temperature_C=25,
                water_type="inland_brine",
                EC_value=20,
                EC_unit="mS/cm",
            )

    def test_compensated_ec_rejected_for_seawater(self):
        with self.assertRaises(ValueError):
            calculate_water_properties(
                temperature_C=25,
                water_type="seawater",
                EC_value=50,
                EC_unit="mS/cm",
                conductivity_temperature_mode="compensated_to_25C",
            )

    def test_unknown_water_type_rejected(self):
        with self.assertRaises(ValueError):
            calculate_water_properties(temperature_C=20, water_type="brackish")

    def test_zero_absolute_pressure_rejected(self):
        with self.assertRaises(ValueError):
            calculate_water_properties(
                temperature_C=20,
                water_type="freshwater",
                pressure_MPa_abs=0,
            )


class TestFreshwaterProperties(unittest.TestCase):
    def test_properties_are_positive_and_consistent(self):
        try:
            result = calculate_water_properties(
                temperature_C=20,
                water_type="freshwater",
                pressure_MPa_abs=0.101325,
            )
        except ImportError:
            self.skipTest("iapws dependency is not installed")

        self.assertGreater(result["density_kg_m3"], 0)
        self.assertGreater(result["dynamic_viscosity_Pa_s"], 0)
        self.assertGreater(result["kinematic_viscosity_m2_s"], 0)
        self.assertTrue(math.isclose(
            result["kinematic_viscosity_m2_s"],
            result["dynamic_viscosity_Pa_s"] / result["density_kg_m3"],
            rel_tol=1e-12,
        ))
        self.assertIsNotNone(result["vapor_pressure_MPa"])


class TestSeawaterProperties(unittest.TestCase):
    def test_seawater_outputs_are_positive(self):
        try:
            result = calculate_water_properties(
                temperature_C=15,
                water_type="seawater",
                pressure_MPa_abs=0.101325,
                EC_value=42.914,
                EC_unit="mS/cm",
                latitude_deg=27.0,
                longitude_deg=56.0,
            )
        except ImportError:
            self.skipTest("gsw dependency is not installed")

        self.assertGreater(result["practical_salinity"], 0)
        self.assertGreater(result["absolute_salinity_g_kg"], 0)
        self.assertGreater(result["density_kg_m3"], 0)
        self.assertGreater(result["dynamic_viscosity_Pa_s"], 0)
        self.assertIsNone(result["vapor_pressure_MPa"])
        self.assertTrue(math.isclose(
            result["kinematic_viscosity_m2_s"],
            result["dynamic_viscosity_Pa_s"] / result["density_kg_m3"],
            rel_tol=1e-12,
        ))


if __name__ == "__main__":
    unittest.main()
