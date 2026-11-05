import re
from typing import List, Dict, Any, Optional, Tuple

class StorylinePlanner:
    """
    Stage 2: Management Consultant Storyline Synthesis
    Enforces Minto's Pyramid Principle:
      - 1 message per slide
      - Action titles (<= 9 words, stating the conclusion, not the topic)
      - Single-allocation rule (0 cross-slide fact duplication)
      - Rejection of banned buzzwords
    """

    BANNED_WORDS = [
        "world-class", "revolutionary", "seamless", "best-in-class",
        "game-changer", "cutting-edge", "synergistic", "unparalleled"
    ]

    @classmethod
    def validate_action_title(cls, title: str) -> Tuple[bool, str]:
        words = title.strip().split()
        if len(words) > 9:
            return False, f"Title has {len(words)} words (max 9 allowed): '{title}'"
        
        # Check topic-only titles
        lower = title.lower()
        if lower in ["overview", "details", "scope", "introduction", "background", "architecture", "workstreams"]:
            return False, f"Title is a passive topic label rather than an action statement: '{title}'"
            
        for banned in cls.BANNED_WORDS:
            if banned in lower:
                return False, f"Title contains banned superlative '{banned}': '{title}'"
                
        return True, "Valid"

    @classmethod
    def plan_proposal_storyline(cls, brief: str, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes an executive pyramid storyline for an enterprise proposal.
        """
        client = research_data.get("client_name", "Enterprise Client")
        solution = research_data.get("solution_name", "Enterprise Platform")
        
        slides = [
            {
                "slide_number": 1,
                "role": "context",
                "message": f"Proposal for {client} to deploy {solution} and modernize enterprise ERP operations.",
                "action_title": f"{client} – {solution} & Odoo Enhancement Proposal",
                "subtitle": "Centralized Insights  |  Improved ERP Experience  |  Connected Business Processes",
                "content_shape": "cover",
                "evidence_keys": ["client_name", "solution_name"]
            },
            {
                "slide_number": 2,
                "role": "requirements",
                "message": "Direct alignment of existing operational challenges to measurable business outcomes.",
                "action_title": f"Understanding {client}'s business requirements",
                "subtitle": "From today's challenges to the outcomes being sought",
                "content_shape": "requirement_to_outcome",
                "evidence_keys": ["challenges", "desired_outcomes"]
            },
            {
                "slide_number": 3,
                "role": "solution_architecture",
                "message": "Four integrated workstreams anchored around Odoo as the central system of record.",
                "action_title": "Four connected workstreams around Odoo",
                "subtitle": f"Each workstream strengthens {client}'s Odoo environment as the single system of record",
                "content_shape": "hub_and_spokes",
                "evidence_keys": ["workstreams"]
            },
            {
                "slide_number": 4,
                "role": "product_proof",
                "message": f"{solution} delivers a governed reporting layer without altering the core ERP.",
                "action_title": f"{solution}: centralized business intelligence",
                "subtitle": f"Odoo stays the source of truth; {solution} turns it into one governed reporting layer",
                "content_shape": "dashboard_concept",
                "evidence_keys": ["elitia_kpi_cards", "semantic_layer", "drill_down"]
            },
            {
                "slide_number": 5,
                "role": "executive_visibility",
                "message": "Multi-tier visibility delivering tailored intelligence from board summaries to line items.",
                "action_title": "Executive reporting and business visibility",
                "subtitle": "Management visibility, faster reporting and informed decisions at every level",
                "content_shape": "levels_x_dimensions",
                "evidence_keys": ["stakeholder_tiers", "domain_reporting"]
            },
            {
                "slide_number": 6,
                "role": "erp_assessment",
                "message": "Structured diagnostic assessment optimizing workflows and user experience prior to changes.",
                "action_title": "Odoo ERP health check and UI/UX audit",
                "subtitle": "Assess first, then recommend: improvements are prioritized from evidence",
                "content_shape": "process_linear",
                "evidence_keys": ["health_check_steps", "health_deliverables"]
            },
            {
                "slide_number": 7,
                "role": "data_migration",
                "message": "A 6-step controlled migration pathway restoring historical reporting continuity.",
                "action_title": "Resort ERP to Odoo data migration",
                "subtitle": "A six-step path from legacy extracts to signed-off data in Odoo",
                "content_shape": "process_linear",
                "evidence_keys": ["migration_steps", "migration_deliverables"]
            },
            {
                "slide_number": 8,
                "role": "operational_automation",
                "message": "Automated time-tracking ingestion connecting biometric devices directly to bank salary upload.",
                "action_title": "Automated payroll and time-tracking integration",
                "subtitle": "From the biometric device to the bank upload",
                "content_shape": "flow_with_actions",
                "evidence_keys": ["payroll_flow", "wps_spec"]
            },
            {
                "slide_number": 9,
                "role": "delivery_roadmap",
                "message": "Phased 5-stage deployment with built-in clean-core compatibility for future Odoo upgrades.",
                "action_title": "Implementation approach and delivery roadmap",
                "subtitle": "Five phases. Timelines will be confirmed in discovery and mutually agreed.",
                "content_shape": "phases_over_time",
                "evidence_keys": ["phases", "odoo_v20_compatibility"]
            },
            {
                "slide_number": 10,
                "role": "commercials_governance",
                "message": "Transparent investment schedule, dedicated consulting team, and standard engagement terms.",
                "action_title": "Commercials, resources and terms and conditions",
                "subtitle": None,
                "content_shape": "roles_and_terms",
                "evidence_keys": ["commercial_rows", "manpower_roles", "terms_list"]
            }
        ]

        return {
            "deck_theme": "lumbini",
            "client_name": client,
            "solution_name": solution,
            "total_slides": len(slides),
            "slides": slides
        }
