"""Reference database access for PE pressure-pipe material classifications."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

DEFAULT_DATABASE_PATH = Path(__file__).resolve().parents[1] / "databases" / "pe_materials.json"


class PEMaterialDatabaseError(ValueError):
    """Raised when PE material data cannot be loaded or found."""


def load_pe_material_database(path: str | Path | None = None) -> dict[str, Any]:
    """Load and validate the PE material reference database."""
    database_path = Path(path) if path is not None else DEFAULT_DATABASE_PATH
    try:
        with database_path.open("r", encoding="utf-8") as file:
            database = json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        raise PEMaterialDatabaseError(f"Could not load PE material database: {database_path}") from exc
    if not isinstance(database.get("materials"), list):
        raise PEMaterialDatabaseError("Database must contain a materials list.")
    required = {"material_grade", "mrs_MPa", "design_coefficient_min_water",
                "reference_design_stress_MPa", "source_ids", "status"}
    for record in database["materials"]:
        missing = required.difference(record)
        if missing:
            raise PEMaterialDatabaseError(f"Material record is missing fields: {sorted(missing)}")
        if record["mrs_MPa"] <= 0:
            raise PEMaterialDatabaseError("MRS must be positive.")
        if record["design_coefficient_min_water"] <= 1:
            raise PEMaterialDatabaseError("Design coefficient must be greater than 1.")
    return database


def list_pe_materials(database: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Return all material records."""
    data = database if database is not None else load_pe_material_database()
    return list(data["materials"])


def get_pe_material(material_grade: str, database: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return an exact material-grade record (case-insensitive)."""
    data = database if database is not None else load_pe_material_database()
    requested = material_grade.strip().upper()
    for record in data["materials"]:
        if record["material_grade"].upper() == requested:
            return dict(record)
    available = ", ".join(record["material_grade"] for record in data["materials"])
    raise PEMaterialDatabaseError(f"Unknown PE material grade: {material_grade!r}. Available grades: {available}")


def calculate_design_stress(material_grade: str, design_coefficient: float | None = None,
                            database: dict[str, Any] | None = None) -> dict[str, float | str]:
    """Calculate reference design stress as MRS/C, at the 20 C, 50-year MRS basis.

    This is not a temperature-adjusted allowable stress or a product pressure rating.
    """
    record = get_pe_material(material_grade, database)
    coefficient = float(record["design_coefficient_min_water"]) if design_coefficient is None else float(design_coefficient)
    minimum = float(record["design_coefficient_min_water"])
    if coefficient < minimum:
        raise PEMaterialDatabaseError(
            f"Design coefficient {coefficient} is below the database minimum for water applications ({minimum})."
        )
    if coefficient <= 1:
        raise PEMaterialDatabaseError("Design coefficient must be greater than 1.")
    return {
        "material_grade": record["material_grade"],
        "mrs_MPa": float(record["mrs_MPa"]),
        "design_coefficient": coefficient,
        "design_stress_MPa": float(record["mrs_MPa"]) / coefficient,
        "reference_temperature_C": 20.0,
        "reference_lifetime_years": 50.0,
        "status": "material_level_reference_only",
    }
