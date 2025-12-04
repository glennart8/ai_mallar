"""
Generera test-PDF:er för bidragsansökningar.
Skapar både korrekta och felaktiga formulär för testning.
"""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

# Skapa data-mappen om den inte finns
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def create_grant_application(
    filename: str,
    name: str = "",
    organization: str = "",
    org_number: str = "",
    email: str = "",
    phone: str = "",
    project_name: str = "",
    project_description: str = "",
    budget: str = "",
    requested_amount: str = ""
):
    """Skapar en PDF med bidragsansökan."""
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Titel
    c.setFont("Helvetica-Bold", 18)
    c.drawString(2*cm, height - 2*cm, "Bidragsansokan")

    # Formulärfält
    c.setFont("Helvetica", 12)
    y_position = height - 4*cm
    line_height = 1.2*cm

    fields = [
        ("Namn:", name),
        ("Organisation:", organization),
        ("Organisationsnummer:", org_number),
        ("E-post:", email),
        ("Telefon:", phone),
        ("Projektnamn:", project_name),
        ("Budget (kr):", budget),
        ("Sokt belopp (kr):", requested_amount),
    ]

    for label, value in fields:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(2*cm, y_position, label)
        c.setFont("Helvetica", 10)
        c.drawString(6*cm, y_position, value)
        y_position -= line_height

    # Projektbeskrivning (längre text)
    y_position -= 0.5*cm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2*cm, y_position, "Projektbeskrivning:")
    y_position -= 0.6*cm

    c.setFont("Helvetica", 10)
    # Dela upp lång text i rader
    if project_description:
        words = project_description.split()
        line = ""
        for word in words:
            test_line = line + " " + word if line else word
            if c.stringWidth(test_line, "Helvetica", 10) < width - 4*cm:
                line = test_line
            else:
                c.drawString(2*cm, y_position, line)
                y_position -= 0.5*cm
                line = word
        if line:
            c.drawString(2*cm, y_position, line)

    c.save()
    print(f"PDF skapad: {filename}")


def create_valid_application():
    """Skapar en korrekt ifylld ansökan."""
    create_grant_application(
        filename=str(DATA_DIR / "valid_application.pdf"),
        name="Anna Svensson",
        organization="Kulturforeningen Norden",
        org_number="802456-7890",
        email="anna.svensson@kulturforeningen.se",
        phone="070-123 45 67",
        project_name="Musikfestival for Ungdomar 2025",
        project_description="Vi planerar att arrangera en musikfestival for ungdomar i aldern 15-25 ar. "
                          "Festivalen kommer att innehalla workshoppar i musikproduktion, sangskrivning "
                          "och scenframtradande. Malet ar att ge unga musiker en plattform att visa upp "
                          "sin talang och knyta kontakter inom musikbranschen. Vi raknar med cirka 500 deltagare.",
        budget="150000",
        requested_amount="75000"
    )


def create_invalid_application():
    """Skapar en ansökan med flera fel."""
    create_grant_application(
        filename=str(DATA_DIR / "invalid_application.pdf"),
        name="Erik",  # Saknar efternamn
        organization="",  # Saknas helt
        org_number="12345",  # Fel format
        email="erik@",  # Ogiltig e-post
        phone="",  # Saknas (men optional)
        project_name="Projekt X",
        project_description="Vi vill gora nagonting bra.",  # For kort
        budget="mycket pengar",  # Inte ett tal
        requested_amount=""  # Saknas
    )


def create_partial_application():
    """Skapar en ansökan med några fel."""
    create_grant_application(
        filename=str(DATA_DIR / "partial_application.pdf"),
        name="Maria Johansson",
        organization="Idrottsklubben IK",
        org_number="802123-4567",
        email="maria@ik-klubben.se",
        phone="",
        project_name="",  # Saknas
        project_description="Vi vill starta en ny ungdomsverksamhet for att fa fler barn att rora pa sig.",  # Lite kort
        budget="50000",
        requested_amount="50000"
    )


def create_over_budget_application():
    """Skapar en ansökan där sökt belopp överstiger budget."""
    create_grant_application(
        filename=str(DATA_DIR / "over_budget_application.pdf"),
        name="Test Testsson",
        organization="Testforeningen",
        org_number="802456-1234",
        email="test@test.se",
        phone="070-123 45 67",
        project_name="Testprojekt",
        project_description="Detta ar en lang projektbeskrivning som uppfyller kravet pa minst 100 tecken for att testet ska fungera korrekt och valideringen ska ga igenom.",
        budget="50000",
        requested_amount="75000"  # Överstiger budget!
    )


if __name__ == "__main__":
    print("Skapar test-PDF:er...\n")

    create_valid_application()
    create_invalid_application()
    create_partial_application()
    create_over_budget_application()

    print("\nKlart! Du kan nu validera dessa med main.py")
