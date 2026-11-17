import unittest

from core.pipe_database import (
    PipeDatabaseError,
    calculate_internal_diameter,
    get_pipe_dimensions,
    get_pipe_geometry,
    list_available_pipes,
)


class TestPipeDatabase(unittest.TestCase):
    def test_database_contains_initial_sdr11_records(self):
        records = list_available_pipes(material_grade="PE100", sdr=11)
        self.assertEqual(len(records), 22)
        self.assertEqual(records[0]["dn_od_mm"], 32)
        self.assertEqual(records[-1]["dn_od_mm"], 630)

    def test_exact_lookup(self):
        pipe = get_pipe_dimensions(110, 11, "PE100")
        self.assertEqual(pipe["nominal_wall_thickness_mm"], 10.0)
        self.assertEqual(pipe["status"], "catalogue_transcribed")

    def test_nominal_internal_diameter(self):
        pipe = get_pipe_geometry(110, 11, "PE100")
        self.assertAlmostEqual(pipe["nominal_internal_diameter_mm"], 90.0)

    def test_unknown_size_is_not_inferred(self):
        with self.assertRaises(PipeDatabaseError):
            get_pipe_dimensions(100, 11, "PE100")

    def test_invalid_geometry(self):
        with self.assertRaises(PipeDatabaseError):
            calculate_internal_diameter(100, 50)

    def test_filter_by_grade_and_sdr(self):
        records = list_available_pipes(material_grade="PE100", sdr=11)
        self.assertTrue(all(p["material_grade"] == "PE100" for p in records))
        self.assertTrue(all(p["sdr"] == 11 for p in records))


if __name__ == "__main__":
    unittest.main()
