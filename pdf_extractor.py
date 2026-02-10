"""
PDF extraction module for MyCase client activity documents.
Extracts text, timeline events, and structured data from client PDFs.
"""

import pdfplumber
from pathlib import Path
from typing import Dict, List, Optional
import re
from datetime import datetime


class PDFExtractor:
    """Extract structured data from MyCase PDF exports."""

    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        self.raw_text = ""
        self.case_name = ""
        self.timeline_events = []
        self.metadata = {}

    def extract_all(self) -> Dict:
        """
        Extract all relevant data from PDF.

        Returns:
            Dict with keys: case_name, timeline_events, metadata, raw_text
        """
        with pdfplumber.open(self.pdf_path) as pdf:
            # Extract all text
            self.raw_text = "\n".join([page.extract_text() or "" for page in pdf.pages])

        # Parse structured data
        self._extract_case_name()
        self._extract_timeline_events()
        self._extract_metadata()

        return {
            "case_name": self.case_name,
            "timeline_events": self.timeline_events,
            "metadata": self.metadata,
            "raw_text": self.raw_text,
            "pdf_filename": self.pdf_path.name
        }

    def _extract_case_name(self):
        """Extract case name from PDF header or Items/Info section."""
        # Common patterns in MyCase PDFs
        patterns = [
            r"Case:\s*(.+?)(?:\n|$)",
            r"Client Name:\s*(.+?)(?:\n|$)",
            r"Matter:\s*(.+?)(?:\n|$)",
            r"^(.+?)\s*-\s*Activities",  # "John Doe - Activities & Timeline"
        ]

        for pattern in patterns:
            match = re.search(pattern, self.raw_text, re.MULTILINE | re.IGNORECASE)
            if match:
                self.case_name = match.group(1).strip()
                return

        # Fallback: use filename
        self.case_name = self.pdf_path.stem.replace("_", " ")

    def _extract_timeline_events(self):
        """
        Extract timeline events with dates, actors, and content.
        Looks for patterns like:
        - Date | User | Activity Type | Description
        - MM/DD/YYYY - Note by John Doe: "Client called demanding..."
        """
        events = []

        # Pattern for date-based entries
        date_patterns = [
            r"(\d{1,2}/\d{1,2}/\d{2,4})\s*[-|]\s*(.+?)(?=\n\d{1,2}/\d{1,2}/\d{2,4}|\Z)",
            r"(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}[AP]M)?\s*(.+?)(?=\n\d{4}-\d{2}-\d{2}|\Z)",
        ]

        for pattern in date_patterns:
            matches = re.finditer(pattern, self.raw_text, re.DOTALL | re.MULTILINE)
            for match in matches:
                try:
                    date_str = match.group(1)
                    content = match.group(2).strip() if len(match.groups()) == 2 else match.group(3).strip()

                    # Try to parse date
                    try:
                        event_date = self._parse_date(date_str)
                    except:
                        event_date = date_str

                    events.append({
                        "date": event_date,
                        "content": content[:500],  # Limit content length
                        "raw_text": content
                    })
                except Exception as e:
                    continue

        # Sort by date if possible
        self.timeline_events = sorted(
            events,
            key=lambda x: x["date"] if isinstance(x["date"], datetime) else datetime.min
        )

    def _parse_date(self, date_str: str) -> datetime:
        """Parse various date formats."""
        formats = [
            "%m/%d/%Y",
            "%m/%d/%y",
            "%Y-%m-%d",
            "%d-%m-%Y",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except:
                continue

        raise ValueError(f"Cannot parse date: {date_str}")

    def _extract_metadata(self):
        """Extract case metadata like case number, attorney, payment status."""
        metadata = {}

        # Look for common metadata fields
        patterns = {
            "case_number": r"Case\s*#?\s*:?\s*(\d+)",
            "attorney": r"Attorney:\s*(.+?)(?:\n|$)",
            "paralegal": r"Paralegal:\s*(.+?)(?:\n|$)",
            "case_type": r"Case Type:\s*(.+?)(?:\n|$)",
            "opened_date": r"Opened:\s*(\d{1,2}/\d{1,2}/\d{2,4})",
            "status": r"Status:\s*(.+?)(?:\n|$)",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, self.raw_text, re.IGNORECASE)
            if match:
                metadata[key] = match.group(1).strip()

        self.metadata = metadata

    def get_communication_snippets(self, limit: int = 10) -> List[str]:
        """
        Extract the most relevant communication snippets for behavior analysis.
        Prioritizes entries with emotional language, complaints, or threats.
        """
        if not self.timeline_events:
            return []

        # Keywords indicating problematic behavior
        priority_keywords = [
            "yell", "scream", "profanity", "threat", "lawsuit", "state bar",
            "fraud", "incompetent", "complaint", "demand", "angry", "upset",
            "dissatisfied", "frustrated", "fire", "terminate", "refund",
            "review", "google", "yelp", "hang up", "refused to speak"
        ]

        scored_events = []
        for event in self.timeline_events:
            content = event["raw_text"].lower()
            score = sum(1 for keyword in priority_keywords if keyword in content)
            scored_events.append((score, event))

        # Sort by score descending, take top N
        scored_events.sort(key=lambda x: x[0], reverse=True)
        top_events = [event for score, event in scored_events[:limit] if score > 0]

        # If no high-priority events, just take most recent
        if not top_events:
            top_events = self.timeline_events[-limit:]

        return [event["raw_text"] for event in top_events]


def extract_from_folder(folder_path: str) -> List[Dict]:
    """
    Extract data from all PDFs in a folder.

    Args:
        folder_path: Path to folder containing client PDFs

    Returns:
        List of extracted data dictionaries
    """
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    pdf_files = list(folder.glob("*.pdf"))
    if not pdf_files:
        raise ValueError(f"No PDF files found in {folder_path}")

    results = []
    for pdf_file in pdf_files:
        try:
            print(f"Extracting: {pdf_file.name}")
            extractor = PDFExtractor(str(pdf_file))
            data = extractor.extract_all()
            results.append(data)
        except Exception as e:
            print(f"Error extracting {pdf_file.name}: {str(e)}")
            # Continue with other files
            continue

    return results
