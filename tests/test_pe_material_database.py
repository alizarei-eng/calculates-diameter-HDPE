import unittest
from core.pe_material_database import (
    PEMaterialDatabaseError, calculate_design_stress, get_pe_material,
    list_pe_materials, load_pe_material_database,
)


class TestPEMaterialDatabase(unittest.TestCase):
    def test_database_contains_three_initial_grades(self):
        records = list_pe_materials()
        self.assertEqual(len(records), 3)
        self.assertEqual({item["material_grade"] for item in records}, {"PE80", "PE100", "PE100-RC"})

    def test_pe80_mrs(self):
        self.assertEqual(get_pe_material("PE80")["mrs_MPa"], 8.0)

    def test_pe100_mrs(self):
        self.assertEqual(get_pe_material("PE100")["mrs_MPa"], 10.0)

    def test_pe100_rc_has_same_mrs_as_pe100(self):
        pe100, rc = get_pe_material("PE100"), get_pe_material("PE100-RC")
        self.assertEqual(rc["mrs_MPa"], pe100["mrs_MPa"])
        self.assertEqual(rc["slow_crack_growth_class"], "enhanced_resistance")

    def test_grade_lookup_is_case_insensitive(self):
        self.assertEqual(get_pe_material("pe100")["material_grade"], "PE100")

    def test_unknown_grade_raises(self):
        with self.assertRaises(PEMaterialDatabaseError):
            get_pe_material("PE125")

    def test_default_pe100_design_stress(self):
        result = calculate_design_stress("PE100")
        self.assertAlmostEqual(result["design_stress_MPa"], 8.0)
        self.assertEqual(result["design_coefficient"], 1.25)

    def test_custom_design_coefficient(self):
        result = calculate_design_stress("PE100", design_coefficient=1.6)
        self.assertAlmostEqual(result["design_stress_MPa"], 6.25)

    def test_coefficient_below_water_minimum_raises(self):
        with self.assertRaises(PEMaterialDatabaseError):
            calculate_design_stress("PE100", design_coefficient=1.0)

    def test_loaded_database_has_scope_warning(self):
        self.assertIn("not a manufacturer approval list", load_pe_material_database()["scope"])


if __name__ == "__main__":
    unittest.main()
