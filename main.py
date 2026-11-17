"""Interactive command-line entry point for the HDPE engineering library.

Run from the repository root:
    python main.py

This interface orchestrates existing core modules; engineering calculations
remain inside the independently testable modules under core/.
"""
from __future__ import annotations

import json
from typing import Any

from core.pipe_database import (
    PipeDatabaseError,
    get_pipe_geometry,
    list_available_pipes,
)
from core.pipe_sizing import recommend_pipe_diameter
from core.pe_material_database import (
    PEMaterialDatabaseError,
    calculate_design_stress,
    get_pe_material,
    list_pe_materials,
)
from core.water_properties import calculate_water_properties


def read_float(prompt: str, default: float | None = None) -> float:
    """Read a numeric value, optionally accepting a displayed default."""
    while True:
        suffix = f" [{default}]" if default is not None else ""
        raw = input(f"{prompt}{suffix}: ").strip()
        if not raw and default is not None:
            return default
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")


def print_json(data: Any) -> None:
    """Print dictionaries/lists in a readable format."""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def show_pipe_menu() -> None:
    print("\n--- Pipe dimensional database ---")
    print("1. List available pipes")
    print("2. Look up one pipe and calculate nominal ID")
    print("3. Recommend a pipe diameter from flow and target velocity")
    choice = input("Select: ").strip()

    try:
        if choice == "1":
            grade = input("Material grade [PE100]: ").strip() or "PE100"
            sdr_text = input("SDR (leave blank for all): ").strip()
            records = list_available_pipes(
                material_grade=grade,
                sdr=float(sdr_text) if sdr_text else None,
            )
            print(f"\nFound {len(records)} documented record(s):")
            print_json(records)
        elif choice == "2":
            grade = input("Material grade [PE100]: ").strip() or "PE100"
            od = read_float("Nominal outside diameter (mm)")
            sdr = read_float("SDR")
            print_json(get_pipe_geometry(od, sdr, grade))
        elif choice == "3":
            flow = read_float("Required flow rate (m3/h)")
            target_velocity = read_float("Target flow velocity (m/s)")
            grade = input("Material grade [PE100]: ").strip() or "PE100"
            sdr_text = input("SDR [11]: ").strip()
            sdr = float(sdr_text) if sdr_text else 11.0
            result = recommend_pipe_diameter(
                flow_rate_m3_h=flow,
                target_velocity_m_s=target_velocity,
                material_grade=grade,
                sdr=sdr,
            )
            print("\nRecommended catalogue size and alternatives:")
            print_json(result)
        else:
            print("Unknown selection.")
    except (PipeDatabaseError, ValueError) as exc:
        print(f"Pipe database error: {exc}")


def show_material_menu() -> None:
    print("\n--- PE material reference database ---")
    print("1. List material grades")
    print("2. Show one grade and calculate reference design stress")
    choice = input("Select: ").strip()

    try:
        if choice == "1":
            print_json(list_pe_materials())
        elif choice == "2":
            grade = input("Material grade (PE80 / PE100 / PE100-RC): ").strip()
            print("\nMaterial record:")
            print_json(get_pe_material(grade))
            coefficient_text = input(
                "Design coefficient [database minimum]: "
            ).strip()
            coefficient = float(coefficient_text) if coefficient_text else None
            print("\nReference design-stress calculation:")
            print_json(calculate_design_stress(grade, coefficient))
            print(
                "\nWARNING: this is a material-level reference value, "
                "not a pipe PN/MOP or complete pressure design."
            )
        else:
            print("Unknown selection.")
    except (PEMaterialDatabaseError, ValueError) as exc:
        print(f"PE material database error: {exc}")


def show_water_menu() -> None:
    print("\n--- Water properties ---")
    print("1. Freshwater")
    print("2. Natural seawater")
    print("Note: inland brine is not supported using EC alone.")
    choice = input("Select water type: ").strip()

    try:
        temperature = read_float("Temperature (°C)")
        pressure = read_float("Absolute pressure (MPa)", 0.101325)

        if choice == "1":
            result = calculate_water_properties(
                temperature_C=temperature,
                water_type="freshwater",
                pressure_MPa_abs=pressure,
            )
        elif choice == "2":
            ec = read_float("In-situ electrical conductivity")
            unit = input("EC unit (mS/cm, uS/cm, µS/cm, S/m): ").strip()
            lat_text = input("Latitude in degrees (optional): ").strip()
            lon_text = input("Longitude in degrees (optional): ").strip()
            if bool(lat_text) != bool(lon_text):
                raise ValueError("Enter both latitude and longitude, or leave both blank.")
            kwargs: dict[str, Any] = {}
            if lat_text:
                kwargs["latitude_deg"] = float(lat_text)
                kwargs["longitude_deg"] = float(lon_text)
            result = calculate_water_properties(
                temperature_C=temperature,
                water_type="seawater",
                pressure_MPa_abs=pressure,
                EC_value=ec,
                EC_unit=unit,
                conductivity_temperature_mode="in_situ",
                **kwargs,
            )
        else:
            print("Unknown selection.")
            return

        print_json(result)
    except (ValueError, ImportError, NotImplementedError, ArithmeticError) as exc:
        print(f"Water-property calculation error: {exc}")


def main() -> None:
    """Display the main menu and dispatch to the selected library module."""
    while True:
        print("\n==============================================")
        print("       HDPE Pipe Engineering Library")
        print("==============================================")
        print("1. Pipe dimensions")
        print("2. PE material properties")
        print("3. Water properties")
        print("0. Exit")
        choice = input("Select a section: ").strip()

        if choice == "1":
            show_pipe_menu()
        elif choice == "2":
            show_material_menu()
        elif choice == "3":
            show_water_menu()
        elif choice == "0":
            print("Program closed.")
            break
        else:
            print("Invalid selection. Choose 0, 1, 2 or 3.")


if __name__ == "__main__":
    main()
