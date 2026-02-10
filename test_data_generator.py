#!/usr/bin/env python3
"""
Test Data Generator - Create sample PDFs for testing the auditor.

Generates realistic MyCase-style PDFs with various client behavior patterns.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime, timedelta
import random
from pathlib import Path


class TestCaseGenerator:
    """Generate sample client case PDFs for testing."""

    def __init__(self, output_dir: str = "./test_pdfs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.styles = getSampleStyleSheet()

    def generate_test_suite(self):
        """Generate a full suite of test cases covering all classifications."""

        test_cases = [
            # Normal clients
            {
                "name": "Sarah Johnson - I-485 Adjustment",
                "classification": "normal",
                "events": self._normal_client_events(),
            },

            # Special clients (difficult but respectful)
            {
                "name": "Michael Chen - Asylum Application",
                "classification": "special",
                "events": self._special_client_events(),
            },
            {
                "name": "Anna Rodriguez - Family Petition",
                "classification": "special_justified",
                "events": self._special_justified_events(),
            },

            # E-Special clients (abusive)
            {
                "name": "Robert Williams - Deportation Defense",
                "classification": "e_special",
                "events": self._e_special_events(),
            },
            {
                "name": "Jennifer Davis - Citizenship Application",
                "classification": "e_special_threats",
                "events": self._e_special_threats_events(),
            },

            # Delinquent
            {
                "name": "Carlos Martinez - Work Permit",
                "classification": "delinquent",
                "events": self._delinquent_events(),
            },

            # Delinquent + Special
            {
                "name": "Lisa Thompson - Green Card Renewal",
                "classification": "delinquent_special",
                "events": self._delinquent_special_events(),
            },
        ]

        print("Generating test PDFs...\n")

        for i, case in enumerate(test_cases, 1):
            filename = f"test_case_{i:02d}_{case['name'].replace(' ', '_').replace('-', '').lower()}.pdf"
            filepath = self.output_dir / filename

            self._generate_pdf(case["name"], case["events"], filepath)
            print(f"✅ Generated: {filename}")

        print(f"\n✅ Generated {len(test_cases)} test PDFs in: {self.output_dir}")
        print(f"\nTo test the auditor:")
        print(f"  python3 auditor.py {self.output_dir}")

    def _generate_pdf(self, case_name: str, events: list, filepath: Path):
        """Generate a single PDF file."""

        doc = SimpleDocTemplate(str(filepath), pagesize=letter)
        story = []

        # Title
        title_style = ParagraphStyle(
            'Title',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1F4E78'),
            spaceAfter=12
        )
        story.append(Paragraph(f"Activities & Timeline: {case_name}", title_style))
        story.append(Spacer(1, 0.2*inch))

        # Case metadata
        metadata = [
            ["Case:", case_name],
            ["Case #:", f"20240{random.randint(100, 999)}"],
            ["Attorney:", random.choice(["John Smith", "Maria Garcia", "David Lee"])],
            ["Paralegal:", random.choice(["Sarah Johnson", "Michael Chen", "Lisa Davis"])],
            ["Status:", random.choice(["Active", "Pending", "Under Review"])],
            ["Opened:", (datetime.now() - timedelta(days=random.randint(180, 720))).strftime("%m/%d/%Y")],
        ]

        table = Table(metadata, colWidths=[1.5*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))

        story.append(table)
        story.append(Spacer(1, 0.3*inch))

        # Timeline events
        story.append(Paragraph("Timeline & Activities", self.styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))

        for event in events:
            date_str = event['date'].strftime("%m/%d/%Y")
            text = f"<b>{date_str}</b> - {event['content']}"
            story.append(Paragraph(text, self.styles['Normal']))
            story.append(Spacer(1, 0.1*inch))

        doc.build(story)

    def _normal_client_events(self) -> list:
        """Events for a normal, professional client."""
        base_date = datetime.now() - timedelta(days=180)

        return [
            {"date": base_date, "content": "Initial consultation completed. Client expressed interest in adjustment of status. Fees discussed and contract signed."},
            {"date": base_date + timedelta(days=7), "content": "Retainer payment received in full. Case file created."},
            {"date": base_date + timedelta(days=14), "content": "Email from client providing requested documents (birth certificate, passport copies). All documents received as requested."},
            {"date": base_date + timedelta(days=30), "content": "Phone call with client to review I-485 draft. Client had minor questions about employment history section. Questions answered satisfactorily."},
            {"date": base_date + timedelta(days=45), "content": "I-485 package filed with USCIS. Client notified via email. Receipt notice expected within 2-3 weeks."},
            {"date": base_date + timedelta(days=60), "content": "Email from client asking about status. Explained typical processing timelines. Client understanding and patient."},
            {"date": base_date + timedelta(days=90), "content": "USCIS issued biometrics appointment notice. Forwarded to client immediately. Client confirmed receipt."},
        ]

    def _special_client_events(self) -> list:
        """Events for a special (difficult but respectful) client."""
        base_date = datetime.now() - timedelta(days=120)

        return [
            {"date": base_date, "content": "Initial consultation. Client very anxious about timeline and kept asking if case would be approved."},
            {"date": base_date + timedelta(days=3), "content": "Phone call from client. Client calling to ask if we've started working on the case yet. Reassured client that work begins after retainer received."},
            {"date": base_date + timedelta(days=5), "content": "Client called again asking about timeline. Explained typical 6-8 month processing time. Client expressed concern about urgency."},
            {"date": base_date + timedelta(days=7), "content": "Retainer received. Client immediately called asking for update even though payment just processed."},
            {"date": base_date + timedelta(days=10), "content": "Client sent email: 'I haven't heard anything. Is anyone working on my case? I thought this would be faster.'"},
            {"date": base_date + timedelta(days=12), "content": "Phone call with client. Client expressed dissatisfaction with communication frequency. Explained our standard update schedule. Client requested more frequent updates."},
            {"date": base_date + timedelta(days=15), "content": "Client called requesting to speak with attorney directly, stating paralegal explanations are insufficient. Attorney spoke with client for 30 minutes providing reassurance."},
            {"date": base_date + timedelta(days=20), "content": "Client emailed asking if we can expedite the case and requesting services outside original contract scope. Explained additional fees would apply."},
            {"date": base_date + timedelta(days=25), "content": "Client calling daily for updates despite being told processing time is 6-8 months. Client remains polite but clearly anxious."},
        ]

    def _special_justified_events(self) -> list:
        """Special client whose behavior is justified by firm error."""
        base_date = datetime.now() - timedelta(days=90)

        return [
            {"date": base_date, "content": "Initial consultation completed. Client signed contract for asylum application."},
            {"date": base_date + timedelta(days=30), "content": "Client submitted all requested documents on time. Professional and cooperative."},
            {"date": base_date + timedelta(days=60), "content": "FIRM ERROR: Paralegal missed RFE deadline. RFE was not responded to in time. Case may be at risk."},
            {"date": base_date + timedelta(days=61), "content": "Client called after receiving USCIS notice of intent to deny. Client understandably upset and asked why RFE was not submitted. Client remained respectful despite serious firm error."},
            {"date": base_date + timedelta(days=62), "content": "Managing attorney spoke with client. Firm took responsibility for error. Offered to file motion to reopen at no cost to client."},
            {"date": base_date + timedelta(days=65), "content": "Client sent email expressing frustration: 'I trusted you with my case and this mistake could cost me everything. I need assurance this won't happen again.'"},
            {"date": base_date + timedelta(days=70), "content": "Client calling frequently for updates on motion to reopen. Client's anxiety is justified given firm's mistake. Client has not yelled or threatened but is clearly stressed."},
        ]

    def _e_special_events(self) -> list:
        """E-Special client with abusive behavior."""
        base_date = datetime.now() - timedelta(days=60)

        return [
            {"date": base_date, "content": "Initial consultation. Client seemed impatient but signed contract."},
            {"date": base_date + timedelta(days=10), "content": "Client called demanding immediate updates. When paralegal explained case just started, client raised voice and said 'This is ridiculous. I paid you money and nothing is happening.'"},
            {"date": base_date + timedelta(days=15), "content": "Client sent aggressive email with subject 'UNACCEPTABLE SERVICE' stating we are incompetent and demanding refund."},
            {"date": base_date + timedelta(days=20), "content": "Phone call with client. Client became hostile during call. QUOTE: 'You people are worthless. I want to speak to Arvin NOW. Don't transfer me to another useless paralegal.' Client hung up on paralegal."},
            {"date": base_date + timedelta(days=22), "content": "Client showed up at office unannounced and demanded to see attorney immediately. When informed attorney was in court, client became aggressive and pounded on reception desk. Security escort requested."},
            {"date": base_date + timedelta(days=25), "content": "Client sent email with profanity: 'This is bullshit. You're all a bunch of incompetent idiots. Get your act together or I'm filing a complaint.'"},
            {"date": base_date + timedelta(days=28), "content": "Managing attorney attempted to speak with client. Client yelled at attorney and stated: 'I'm calling the State Bar. This is fraud. You took my money and did nothing.'"},
        ]

    def _e_special_threats_events(self) -> list:
        """E-Special client with explicit threats."""
        base_date = datetime.now() - timedelta(days=45)

        return [
            {"date": base_date, "content": "Case opened for naturalization application."},
            {"date": base_date + timedelta(days=10), "content": "Client dissatisfied with processing timeline. Started demanding faster service."},
            {"date": base_date + timedelta(days=20), "content": "Client sent threatening email: 'If my case is not filed by next week I will sue your firm for malpractice and post terrible reviews on every website I can find.'"},
            {"date": base_date + timedelta(days=22), "content": "Phone call escalated quickly. Client stated: 'I will destroy your reputation. I will report you to the State Bar. I will make sure nobody ever uses your services again.'"},
            {"date": base_date + timedelta(days=25), "content": "Client posted negative Google review containing false accusations of fraud and theft. Screenshot saved to case file."},
            {"date": base_date + timedelta(days=28), "content": "Client sent email: 'Give me what I want or I'm filing a Bar complaint tomorrow. I have documentation of your incompetence.' This constitutes review blackmail per firm SOP."},
            {"date": base_date + timedelta(days=30), "content": "QA team reviewing case for potential termination. Client behavior shocks the conscience and includes multiple threats (lawsuit, State Bar, defamation). Staff protection is paramount."},
        ]

    def _delinquent_events(self) -> list:
        """Delinquent client (payment issue only, no behavioral problems)."""
        base_date = datetime.now() - timedelta(days=90)

        return [
            {"date": base_date, "content": "Initial consultation completed. Payment plan approved for work permit renewal."},
            {"date": base_date + timedelta(days=7), "content": "First payment received. Case work initiated."},
            {"date": base_date + timedelta(days=30), "content": "Second payment due. Payment not received by due date. Client contacted via email reminder."},
            {"date": base_date + timedelta(days=35), "content": "Client responded apologetically. Stated experiencing financial difficulties. Requested extension."},
            {"date": base_date + timedelta(days=40), "content": "Finance team granted 1-week extension. Client acknowledged and thanked firm for understanding."},
            {"date": base_date + timedelta(days=47), "content": "Extension deadline passed. Payment still not received. Account now $800 past due."},
            {"date": base_date + timedelta(days=50), "content": "Finance team called client. Client did not answer. Voicemail left requesting payment or contact to discuss options."},
            {"date": base_date + timedelta(days=55), "content": "No response from client. MyCase shows outstanding balance of $800. Case marked as delinquent pending Finance review per firm SOP."},
        ]

    def _delinquent_special_events(self) -> list:
        """Client who is both delinquent and exhibiting special behavior."""
        base_date = datetime.now() - timedelta(days=75)

        return [
            {"date": base_date, "content": "Green card renewal case opened. Payment plan established."},
            {"date": base_date + timedelta(days=10), "content": "First payment late by 5 days. Client called expressing frustration with payment system."},
            {"date": base_date + timedelta(days=20), "content": "Client called asking why case is not progressing faster despite being behind on payments. Explained payment plan must be current for work to continue."},
            {"date": base_date + timedelta(days=25), "content": "Second payment missed entirely. Client called demanding updates even though account is past due. Client becoming increasingly difficult."},
            {"date": base_date + timedelta(days=30), "content": "Finance contacted client about past due balance ($1,200). Client responded with long email complaining about service quality rather than addressing payment issue."},
            {"date": base_date + timedelta(days=35), "content": "Client calling daily demanding case updates. Paralegal explained case is on hold due to non-payment. Client expressed dissatisfaction: 'I already paid you so much money. Why isn't anything happening?'"},
            {"date": base_date + timedelta(days=40), "content": "Client emailed requesting to speak with manager about 'lack of progress' - does not acknowledge outstanding payment balance. Client becoming more demanding despite delinquent status."},
            {"date": base_date + timedelta(days=45), "content": "Dual assessment required: Finance needs to determine payment viability, Paulina Rodriguez needs to assess if relationship is salvageable given both payment and behavioral issues."},
        ]


def main():
    """Generate test suite."""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║         TEST DATA GENERATOR                                  ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    try:
        # Check if reportlab is installed
        import reportlab
    except ImportError:
        print("❌ Error: reportlab is required to generate test PDFs")
        print("\nInstall with:")
        print("  pip install reportlab")
        print()
        return

    generator = TestCaseGenerator()
    generator.generate_test_suite()


if __name__ == "__main__":
    main()
