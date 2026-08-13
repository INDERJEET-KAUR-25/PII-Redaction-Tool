from pathlib import Path

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_DOC = PROJECT_ROOT / "input" / "Red_Herring_Prospectus.docx"

OUTPUT_DOC = PROJECT_ROOT / "output" / "Redacted.docx"

SPACY_MODEL = "en_core_web_sm"