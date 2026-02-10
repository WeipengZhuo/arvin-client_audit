"""
Client behavior classification engine based on Saenz-Garcia Law SOP.
Uses Claude API to analyze client conduct and provide recommendations.
"""

import os
from typing import Dict, List, Optional
from anthropic import Anthropic


class BehaviorClassifier:
    """Classify client behavior using SOP rules and Claude API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found. Set environment variable or pass to constructor.")

        self.client = Anthropic(api_key=self.api_key)

        # Load SOP document
        self.sop_path = "/Users/weipengzhuo/Downloads/special delinquent sop.md"
        with open(self.sop_path, 'r') as f:
            self.sop_content = f.read()

    def analyze_client(self, case_data: Dict) -> Dict:
        """
        Analyze a single client case and return classification.

        Args:
            case_data: Dictionary with case_name, timeline_events, metadata, raw_text

        Returns:
            Dict with classification, recommendation, notice_type, firm_fault, reasoning
        """
        # Build analysis prompt
        prompt = self._build_analysis_prompt(case_data)

        # Call Claude API
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            temperature=0.3,  # Lower temperature for more consistent analysis
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Parse response
        result = self._parse_analysis_response(response.content[0].text, case_data)

        return result

    def _build_analysis_prompt(self, case_data: Dict) -> str:
        """Build the analysis prompt for Claude."""

        timeline_summary = "\n\n".join([
            f"Date: {event['date']}\n{event['raw_text'][:300]}"
            for event in case_data.get("timeline_events", [])[:15]  # Limit to 15 most relevant
        ])

        prompt = f"""You are analyzing client behavior for a law firm to determine if continued representation is appropriate.

## REFERENCE DOCUMENT
Below is the firm's SOP that defines client classifications:

{self.sop_content[:15000]}  # Limit SOP to avoid token limits

## CLIENT CASE DATA

**Case Name:** {case_data.get('case_name', 'Unknown')}
**PDF File:** {case_data.get('pdf_filename', 'Unknown')}

**Metadata:**
{self._format_metadata(case_data.get('metadata', {}))}

**Timeline & Activities (Key Events):**
{timeline_summary if timeline_summary else "No timeline events extracted"}

---

## YOUR TASK

Analyze this case and provide a structured assessment following the SOP definitions.

**Classification Criteria:**
- **Normal Client:** Pays on time, communicates respectfully, stays within scope
- **Special Client:** Difficult but respectful - excessive contact, dissatisfaction, scope expansion attempts, BUT NO abuse
- **Excessively Special (E-Special):** Shocks the conscience - yelling, profanity, threats (lawsuit, State Bar, physical), accusations of fraud, hostile conduct, review blackmail
- **Delinquent:** Any past-due balance

**Key Rule:** E-Special behavior is NEVER excused by payment status or firm error. Staff protection is paramount.

## OUTPUT FORMAT (JSON-like structure)

Provide your analysis in this exact format:

```
CLASSIFICATION: [Normal / Special / E-Special / Delinquent / Delinquent + Special]

NOTICE SENT: [Notice to Cure / Notice of Termination / None sent / Cannot determine from records]

FIRM FAULT: [Yes / No / Unclear from records]

FIRM FAULT EXPLANATION: [If Yes: brief explanation of what firm did wrong. If No: "No firm fault identified." If Unclear: explain what info is missing]

CURRENT STATUS: [Active / Pending Cure / Terminated / Recommended for Termination / Cannot determine]

RECOMMENDATION: [Continue representation / Send Notice to Cure / Proceed with Termination / Executive Review Required]

REASONING: [2-3 sentences explaining your classification and recommendation based on specific evidence from the timeline]

KEY EVIDENCE: [Quote 1-3 specific timeline entries that support your classification]
```

**Important Guidelines:**
1. Be conservative - only classify as E-Special if behavior truly "shocks the conscience" per SOP definition
2. Special clients are SALVAGEABLE - recommend cure unless abuse is present
3. If payment status is unclear, note it but focus on behavior
4. Look for patterns, not isolated incidents
5. If records are incomplete, say "Cannot determine from provided records" rather than speculating

Analyze now:"""

        return prompt

    def _format_metadata(self, metadata: Dict) -> str:
        """Format metadata dictionary for display."""
        if not metadata:
            return "No metadata extracted"

        return "\n".join([f"  - {key}: {value}" for key, value in metadata.items()])

    def _parse_analysis_response(self, response_text: str, case_data: Dict) -> Dict:
        """Parse Claude's response into structured format."""

        # Extract fields using regex
        import re

        def extract_field(field_name: str) -> str:
            pattern = rf"{field_name}:\s*(.+?)(?=\n[A-Z\s]+:|$)"
            match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
            return match.group(1).strip() if match else "Not specified"

        result = {
            "case_name": case_data.get("case_name", "Unknown"),
            "pdf_filename": case_data.get("pdf_filename", "Unknown"),
            "classification": extract_field("CLASSIFICATION"),
            "notice_sent": extract_field("NOTICE SENT"),
            "firm_fault": extract_field("FIRM FAULT"),
            "firm_fault_explanation": extract_field("FIRM FAULT EXPLANATION"),
            "current_status": extract_field("CURRENT STATUS"),
            "recommendation": extract_field("RECOMMENDATION"),
            "reasoning": extract_field("REASONING"),
            "key_evidence": extract_field("KEY EVIDENCE"),
            "full_analysis": response_text
        }

        return result

    def batch_analyze(self, cases: List[Dict], progress_callback=None) -> List[Dict]:
        """
        Analyze multiple cases in batch.

        Args:
            cases: List of case data dictionaries
            progress_callback: Optional function(current, total) to track progress

        Returns:
            List of analysis results
        """
        results = []
        total = len(cases)

        for i, case_data in enumerate(cases, 1):
            if progress_callback:
                progress_callback(i, total)

            try:
                print(f"\nAnalyzing {i}/{total}: {case_data.get('case_name', 'Unknown')}")
                result = self.analyze_client(case_data)
                results.append(result)
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                # Add error result
                results.append({
                    "case_name": case_data.get("case_name", "Unknown"),
                    "pdf_filename": case_data.get("pdf_filename", "Unknown"),
                    "classification": "Error during analysis",
                    "notice_sent": "N/A",
                    "firm_fault": "N/A",
                    "firm_fault_explanation": f"Error: {str(e)}",
                    "current_status": "Error",
                    "recommendation": "Manual review required",
                    "reasoning": "Automated analysis failed",
                    "key_evidence": "N/A",
                    "full_analysis": f"Error: {str(e)}"
                })

        return results


class SOPRuleEngine:
    """
    Lightweight rule engine for basic pattern matching.
    Used as a fallback or supplement to Claude API analysis.
    """

    @staticmethod
    def has_e_special_indicators(text: str) -> tuple[bool, List[str]]:
        """
        Check for E-Special behavior indicators using regex patterns.

        Returns:
            (has_indicators, list_of_matched_patterns)
        """
        indicators = {
            "yelling": r"\b(yell|scream|shout|raised voice)\b",
            "profanity": r"\b(fuck|shit|damn|bitch|asshole|profanity|cursing|vulgar)\b",
            "threats_lawsuit": r"\b(lawsuit|sue|legal action|taking you to court)\b",
            "threats_bar": r"\b(state bar|bar complaint|report you|file complaint)\b",
            "threats_physical": r"\b(physical|harm|hurt|violence|beat)\b",
            "threats_review": r"\b(bad review|yelp|google review|destroy your reputation)\b",
            "accusations": r"\b(fraud|theft|steal|criminal|scam|con artist)\b",
            "hostile_conduct": r"\b(pound|slam|aggressive|intimidating|hostile)\b",
            "extreme_escalation": r"\b(only speak to|only talk to|refuse to speak|hanging up|hung up on)\b",
        }

        matched = []
        text_lower = text.lower()

        for category, pattern in indicators.items():
            if re.search(pattern, text_lower):
                matched.append(category)

        return (len(matched) > 0, matched)

    @staticmethod
    def has_special_indicators(text: str) -> tuple[bool, List[str]]:
        """
        Check for Special (but not E-Special) behavior indicators.

        Returns:
            (has_indicators, list_of_matched_patterns)
        """
        indicators = {
            "excessive_contact": r"\b(call(ed)? (again|multiple times|daily|constantly)|excessive contact)\b",
            "dissatisfaction": r"\b(dissatisfied|unhappy|frustrated|concerned|worried|not satisfied)\b",
            "reassurance_seeking": r"\b(anything happening|any update|what's going on|when will)\b",
            "complaints": r"\b(complaint|complain|not happy with|issue with service)\b",
            "scope_expansion": r"\b(also need|in addition|can you also|outside of contract)\b",
            "management_escalation": r"\b(speak with manager|talk to attorney|escalate|someone in charge)\b",
        }

        matched = []
        text_lower = text.lower()

        for category, pattern in indicators.items():
            if re.search(pattern, text_lower):
                matched.append(category)

        return (len(matched) > 0, matched)
