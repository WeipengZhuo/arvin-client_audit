#!/usr/bin/env python3
"""
Client Conduct Auditor - Main CLI Interface

Batch process client activity PDFs and generate termination recommendations.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from pdf_extractor import extract_from_folder
from behavior_classifier import BehaviorClassifier
from spreadsheet_generator import generate_spreadsheet


def print_banner():
    """Print tool banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         CLIENT CONDUCT AUDITOR v1.0                          ║
║         Saenz-Garcia Law SOP Compliance Tool                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def validate_inputs(pdf_folder: str, sop_path: str) -> tuple[bool, Optional[str]]:
    """
    Validate input paths.

    Returns:
        (is_valid, error_message)
    """
    # Check PDF folder
    pdf_path = Path(pdf_folder)
    if not pdf_path.exists():
        return False, f"PDF folder not found: {pdf_folder}"

    if not pdf_path.is_dir():
        return False, f"Path is not a directory: {pdf_folder}"

    # Check for PDF files
    pdf_files = list(pdf_path.glob("*.pdf"))
    if not pdf_files:
        return False, f"No PDF files found in: {pdf_folder}"

    # Check SOP file
    sop_file = Path(sop_path)
    if not sop_file.exists():
        return False, f"SOP file not found: {sop_path}"

    return True, None


def progress_indicator(current: int, total: int):
    """Simple progress indicator."""
    percentage = (current / total) * 100
    bar_length = 40
    filled = int(bar_length * current / total)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"\rProgress: [{bar}] {percentage:.1f}% ({current}/{total})", end="", flush=True)


def main():
    """Main execution flow."""
    parser = argparse.ArgumentParser(
        description="Batch process client activity PDFs and generate assessment spreadsheet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process PDFs in Downloads folder
  python auditor.py ~/Downloads/client_pdfs

  # Specify custom output location
  python auditor.py ~/Downloads/client_pdfs -o ~/Desktop/client_assessment.xlsx

  # Use custom SOP file
  python auditor.py ~/Downloads/client_pdfs --sop /path/to/custom_sop.md

  # Set API key via environment
  export ANTHROPIC_API_KEY="sk-ant-..."
  python auditor.py ~/Downloads/client_pdfs
        """
    )

    parser.add_argument(
        "pdf_folder",
        help="Path to folder containing client activity PDFs"
    )

    parser.add_argument(
        "-o", "--output",
        default="./client_assessment.xlsx",
        help="Output path for assessment spreadsheet (default: ./client_assessment.xlsx)"
    )

    parser.add_argument(
        "--sop",
        default="/Users/weipengzhuo/Downloads/special delinquent sop.md",
        help="Path to SOP markdown file (default: ~/Downloads/special delinquent sop.md)"
    )

    parser.add_argument(
        "--api-key",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    # Print banner
    print_banner()

    # Validate inputs
    is_valid, error = validate_inputs(args.pdf_folder, args.sop)
    if not is_valid:
        print(f"❌ Error: {error}\n")
        sys.exit(1)

    # Count PDFs
    pdf_files = list(Path(args.pdf_folder).glob("*.pdf"))
    print(f"📁 PDF folder: {args.pdf_folder}")
    print(f"📄 Found {len(pdf_files)} PDF files\n")

    try:
        # Step 1: Extract data from PDFs
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("STEP 1: Extracting data from PDFs")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        extracted_data = extract_from_folder(args.pdf_folder)

        print(f"\n✅ Successfully extracted data from {len(extracted_data)} PDFs\n")

        # Step 2: Analyze client behavior
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("STEP 2: Analyzing client behavior using Claude API")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        print("⚙️  Initializing behavior classifier...")
        classifier = BehaviorClassifier(api_key=args.api_key)

        print("🤖 Starting batch analysis...\n")

        analysis_results = classifier.batch_analyze(
            extracted_data,
            progress_callback=progress_indicator if not args.verbose else None
        )

        print(f"\n\n✅ Completed analysis of {len(analysis_results)} cases\n")

        # Step 3: Generate spreadsheet
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("STEP 3: Generating assessment spreadsheet")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        generate_spreadsheet(analysis_results, args.output)

        # Summary
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("SUMMARY")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        # Count recommendations
        recommendations = {}
        for result in analysis_results:
            rec = result.get("recommendation", "Unknown")
            recommendations[rec] = recommendations.get(rec, 0) + 1

        print("Recommendations:")
        for rec, count in sorted(recommendations.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {rec}: {count} cases")

        print(f"\n📊 Output saved to: {args.output}")
        print("\n✅ Audit complete!\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user\n")
        sys.exit(1)

    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}\n")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
