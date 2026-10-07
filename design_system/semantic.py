"""
Semantic Slide Model & Visual Intent Definitions.

Separates raw content and narrative from visual primitives and presentation rendering.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Tuple, Any, Dict


class VisualIntent(Enum):
    """The communicative purpose of a slide, driving layout and primitive selection."""
    EXECUTIVE_OPENING = auto()     # Strategic positioning, hero narrative, 3 pillars
    PROBLEM_FRICTION = auto()      # Operational friction, tension, Current vs. Target
    SYSTEM_ARCHITECTURE = auto()   # Multi-tier technical stack, data pipelines, boundaries
    PROCESS_JOURNEY = auto()       # Sequential physical/digital workflow, Poka-Yoke steps
    OPERATIONAL_COCKPIT = auto()   # Multi-metric operational cockpit, decision towers
    GOVERNANCE_MATRIX = auto()     # Deep tabular alignment (5 W's, persona, tables, P&L)
    PHASED_ROADMAP = auto()        # Sequential delivery timeline, phases, gates
    VALUE_REALIZATION = auto()     # Quantified operational and financial ROI scorecard
    GENERIC_COMPARISON = auto()    # Clean side-by-side comparative analysis


@dataclass
class ContentBlock:
    """Structured text block with lead-in and descriptive body."""
    title: str
    subtitle: Optional[str] = None
    bullets: List[Tuple[str, str]] = field(default_factory=list)  # [(bold_lead_in, description)]
    annotation: Optional[str] = None


@dataclass
class KeyMetric:
    """Quantitative performance indicator or ROI metric."""
    value: str                     # e.g., "-65%", "$14.2M", "14-Month"
    label: str                     # e.g., "WIP Inventory Latency Reduction"
    context: Optional[str] = None  # e.g., "Across 3 target manufacturing plants"
    delta: Optional[str] = None    # e.g., "+14 pts YoY"
    is_positive: bool = True


@dataclass
class ArchitectureTier:
    """A distinct layer or tier in an enterprise solution architecture."""
    tier_number: int               # e.g., 1, 2, 3
    tier_name: str                 # e.g., "TIER 1: SAP S/4HANA ENTERPRISE CORE"
    subtitle: str                  # e.g., "System of Record (Single Source of Financial Truth)"
    components: List[str]          # Bullet points or subsystems
    guarantee_badge: Optional[str] = None # e.g., "[ 100% READ-ONLY | ZERO WRITE CALLS ]"
    protocol_to_next: Optional[str] = None # e.g., "OData GET / TLS 1.3"


@dataclass
class ProcessStep:
    """A discrete station, step, or phase in an operational workflow."""
    step_num: int
    station_name: str              # e.g., "1. Receiving Dock Verification"
    action: str                    # e.g., "Supplier Barcode & ASN Match"
    poka_yoke_rule: Optional[str] = None # Hardware halt or digital interlock rule
    approval_gate: Optional[str] = None  # Supervisor / QC sign-off


@dataclass
class TableData:
    """Tabular dataset with column weighting and cell content."""
    headers: List[str]
    rows: List[List[str]]
    column_weights: Optional[List[float]] = None  # Relative width proportions


@dataclass
class RoadmapPhase:
    """A scheduled phase in an agile / enterprise rollout."""
    phase_id: str                  # e.g., "PHASE 1"
    duration: str                  # e.g., "Weeks 1–3" (or "Days 1–15")
    title: str                     # e.g., "Architecture Blueprint & Edge Setup"
    workstreams: List[str]         # Deliverables / activities
    gate_criteria: Optional[str] = None # Quantitative pass gate


@dataclass
class SemanticSlide:
    """
    Pure semantic representation of a slide.
    Completely decoupled from shape math, pixel coordinates, or python-pptx objects.
    """
    title: str
    category_tag: str
    visual_intent: VisualIntent
    narrative_subtitle: Optional[str] = None
    elements: List[Any] = field(default_factory=list)
    callout_banner: Optional[str] = None
    is_dark: bool = False
    footer_metadata: str = "Confidential Enterprise Advisory Proposal"
    slide_number: int = 1
    total_slides: int = 1
