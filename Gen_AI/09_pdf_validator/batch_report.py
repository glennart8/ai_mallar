"""
Batch-validering av PDF:er med CSV-rapport.
"""

import csv
import shutil
import time
from pathlib import Path
from main import validate_pdf


def move_to_result_folder(pdf_file: Path, folder: Path, valid: bool):
    """Flyttar PDF till godkanda/ eller underkanda/ baserat på resultat."""
    target_dir = folder / ("godkanda" if valid else "underkanda")
    target_dir.mkdir(exist_ok=True)
    shutil.move(str(pdf_file), str(target_dir / pdf_file.name))


def generate_report(folder: str = "data"):
    """Validerar alla PDF:er i en mapp och sparar rapport som CSV i logs/."""
    # Skapa logs-mappen
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    output = logs_dir / "rapport.csv"

    pdf_files = list(Path(folder).glob("*.pdf"))
    results = []

    for i, pdf_file in enumerate(pdf_files):
        print(f"Validerar: {pdf_file.name}")
        result = validate_pdf(str(pdf_file))

        results.append({
            "fil": pdf_file.name,
            "status": "GODKÄND" if result["valid"] else "UNDERKÄND",
            "antal_fel": len(result["errors"]),
            "fel": "; ".join([f"{e['field']}: {e['error']}" for e in result["errors"]])
        })

        # Flytta till godkanda/ eller underkanda/ efter validering
        move_to_result_folder(pdf_file, Path(folder), result["valid"])

        if i < len(pdf_files) - 1:
            time.sleep(2)

    # Skriv CSV
    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["fil", "status", "antal_fel", "fel"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nRapport sparad: {output}")
    return results


if __name__ == "__main__":
    generate_report()
