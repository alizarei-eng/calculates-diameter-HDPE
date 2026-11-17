"""Select a documented PE pipe size using flow rate and target velocity.

This is a preliminary velocity-based size screening tool. It does not calculate
pressure loss, pressure class suitability, water hammer, or lifecycle cost.
"""
from __future__ import annotations

import math
from typing import Any

from core.pipe_database import PipeDatabaseError, list_available_pipes


def recommend_pipe_diameter(
    *,
    flow_rate_m3_h: float,
    target_velocity_m_s: float,
    material_grade: str = "PE100",
    sdr: float = 11,
    database: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Rank catalogue pipes by closeness of actual velocity to target velocity.

    The selected option is the documented catalogue size whose calculated
    velocity is closest to the requested target. Actual velocity is calculated
    from nominal geometric ID (OD minus twice nominal wall thickness).
    """
    if flow_rate_m3_h <= 0:
        raise PipeDatabaseError("Flow rate must be greater than zero.")
    if target_velocity_m_s <= 0:
        raise PipeDatabaseError("Target velocity must be greater than zero.")

    flow_m3_s = float(flow_rate_m3_h) / 3600.0
    records = list_available_pipes(
        material_grade=material_grade, sdr=sdr, database=database
    )
    candidates: list[dict[str, Any]] = []

    for record in records:
        wall = record.get("nominal_wall_thickness_mm")
        if wall is None:
            continue
        od_mm = float(record["dn_od_mm"])
        id_mm = od_mm - 2.0 * float(wall)
        if id_mm <= 0:
            continue
        area_m2 = math.pi * (id_mm / 1000.0) ** 2 / 4.0
        velocity = flow_m3_s / area_m2
        candidates.append({
            "material_grade": record["material_grade"],
            "dn_od_mm": od_mm,
            "sdr": float(record["sdr"]),
            "nominal_wall_thickness_mm": float(wall),
            "nominal_internal_diameter_mm": id_mm,
            "velocity_m_s": velocity,
            "velocity_difference_m_s": velocity - float(target_velocity_m_s),
            "absolute_velocity_difference_m_s": abs(
                velocity - float(target_velocity_m_s)
            ),
            "source_id": record.get("source_id"),
            "status": record.get("status"),
        })

    if not candidates:
        raise PipeDatabaseError(
            f"No usable catalogue dimensions found for grade={material_grade}, SDR={sdr}."
        )

    candidates.sort(key=lambda item: (
        item["absolute_velocity_difference_m_s"],
        item["dn_od_mm"],
    ))
    return {
        "input": {
            "flow_rate_m3_h": float(flow_rate_m3_h),
            "target_velocity_m_s": float(target_velocity_m_s),
            "material_grade": material_grade.strip().upper(),
            "sdr": float(sdr),
        },
        "recommended_pipe": candidates[0],
        "ranked_alternatives": candidates,
        "selection_method": (
            "Closest calculated velocity to the user target among documented "
            "catalogue sizes. This is a velocity-only preliminary selection."
        ),
        "limitations": [
            "Internal diameter uses nominal OD and nominal wall thickness; actual bore depends on tolerances.",
            "The current catalogue is a limited PE100 SDR11 dataset, not a complete current ISO 4427 catalogue.",
            "Pressure rating, pressure loss, surge, temperature derating, and manufacturer availability are not checked.",
        ],
    }
