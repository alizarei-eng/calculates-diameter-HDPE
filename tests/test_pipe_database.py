import unittest

from core.pipe_sizing import recommend_pipe_diameter

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

    def test_recommend_pipe_from_flow_and_target_velocity(self):
        result = recommend_pipe_diameter(
            flow_rate_m3_h=50,
            target_velocity_m_s=1.5,
            material_grade="PE100",
            sdr=11,
        )
        selected = result["recommended_pipe"]
        self.assertEqual(selected["dn_od_mm"], 110)
        self.assertAlmostEqual(selected["velocity_m_s"], 1.455, places=2)
        self.assertTrue(result["ranked_alternatives"])

    def test_reject_nonpositive_flow_or_velocity(self):
        with self.assertRaises(PipeDatabaseError):
            recommend_pipe_diameter(flow_rate_m3_h=0, target_velocity_m_s=1.5)
        with self.assertRaises(PipeDatabaseError):
            recommend_pipe_diameter(flow_rate_m3_h=50, target_velocity_m_s=0)

    def test_filter_by_grade_and_sdr(self):
        records = list_available_pipes(material_grade="PE100", sdr=11)
        self.assertTrue(all(p["material_grade"] == "PE100" for p in records))
        self.assertTrue(all(p["sdr"] == 11 for p in records))


if __name__ == "__main__":
    unittest.main()
