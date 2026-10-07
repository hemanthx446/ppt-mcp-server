"""
Manufacturing Enterprise Architecture Semantic Vocabulary.

Formal ontology and relationship recognition engine for:
1. ENTERPRISE (Business Unit, Plant, Site, Customer, Supplier)
2. SAP / ERP (S/4HANA, Orders, Material, BOM, Routing, Batch, Serial, Inventory, Movements)
3. MANUFACTURING (MES, MOM, Work Order, Operation, WIP, Work Center, Machine, Operator, Shift)
4. QUALITY (Characteristic, Specification, Tolerance, Defect, NCR, CAPA, Calibration)
5. TRACEABILITY (Serial, Batch, Component, Genealogy, As-Built, Parent, Child, Consumption)
6. INTEGRATION (API, OData, IDoc, Event, Message, Middleware, BTP, Edge, OPC UA, MQTT, Power BI)

Detects semantic patterns such as:
- SAP -> MES                          => Integration Architecture
- Production Order -> Operation -> WIP => Manufacturing Process Flow
- Serial -> Components -> Parameters  => Genealogy / As-Built Tree
- Plant -> Work Center -> Machine     => Operational Hierarchy
- KPI -> Business Decision -> Action  => Decision Loop / Outcome Chain
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Set, Tuple, Optional, Any
import re


# =============================================================================
# 1. Semantic Domains & Entity Categories
# =============================================================================

class EntityCategory(Enum):
    ENTERPRISE = auto()
    SAP_ERP = auto()
    MANUFACTURING = auto()
    QUALITY = auto()
    TRACEABILITY = auto()
    INTEGRATION = auto()


class SemanticPatternType(Enum):
    INTEGRATION_FLOW = auto()         # SAP -> MES, Cloud -> Edge
    MANUFACTURING_FLOW = auto()       # Order -> Operation -> Material -> WIP
    GENEALOGY_TRACEABILITY = auto()   # Serial -> Component -> Parameters -> Quality
    OPERATIONAL_HIERARCHY = auto()    # Plant -> Work Center -> Machine -> Operator -> Shift
    DECISION_LOOP = auto()            # KPI -> Business Decision -> Action
    QUALITY_EXCEPTION = auto()        # Tolerance -> Defect -> NCR -> CAPA -> Rework


# =============================================================================
# 2. Vocabulary Registry
# =============================================================================

MANUFACTURING_VOCABULARY: Dict[EntityCategory, List[str]] = {
    EntityCategory.ENTERPRISE: [
        "business unit", "plant", "site", "customer", "supplier",
        "enterprise", "facility", "subsidiary", "vendor"
    ],
    EntityCategory.SAP_ERP: [
        "s/4hana", "s4hana", "sap", "ecc", "sales order", "purchase order",
        "production order", "process order", "material", "material master",
        "bom", "bill of materials", "routing", "work center", "batch",
        "batch master", "serial number", "inventory", "inspection lot",
        "delivery", "outbound delivery", "inbound delivery", "goods movement",
        "movement 101", "movement 261", "confirmation", "co11n", "cost",
        "acdoca", "universal ledger", "bapi", "idoc", "prt"
    ],
    EntityCategory.MANUFACTURING: [
        "mes", "mom", "manufacturing execution system", "work order",
        "operation", "operation sequence", "wip", "work in process",
        "work center", "machine", "cnc", "plc", "tool", "tooling",
        "operator", "shift", "process parameter", "production event",
        "non-conformance", "rework", "scrap", "downtime", "cycle time",
        "spindle", "andon", "setup time", "changeover", "oee"
    ],
    EntityCategory.QUALITY: [
        "inspection characteristic", "specification", "tolerance",
        "defect", "ncr", "non-conformance report", "capa",
        "corrective action", "preventive action", "calibration",
        "inspection result", "first pass yield", "fpy", "spc",
        "statistical process control", "optical inspection", "cpc", "cpk"
    ],
    EntityCategory.TRACEABILITY: [
        "serial", "serial number", "batch", "batch genealogy", "component",
        "genealogy", "as-built", "as built", "parent", "child",
        "consumption", "process history", "lot genealogy", "e-traveler",
        "digital traveler", "barcode", "qr code", "traceability"
    ],
    EntityCategory.INTEGRATION: [
        "api", "rest api", "odata", "idoc", "event", "event mesh",
        "message", "message broker", "middleware", "btp", "sap btp",
        "edge", "edge collector", "edge broker", "opc ua", "opc-ua",
        "mqtt", "database", "sql", "power bi", "sac", "kafka",
        "rfc", "webhook", "dmz", "data diode"
    ]
}


@dataclass
class RecognizedEntity:
    """An identified entity instance within the text."""
    term: str
    canonical_name: str
    category: EntityCategory
    position: int


@dataclass
class SemanticPatternMatch:
    """Recognized relational pattern connecting entities."""
    pattern_type: SemanticPatternType
    matched_sequence: List[str]
    confidence: float
    recommended_primitive: str
    explanation: str


# =============================================================================
# 3. Manufacturing Semantic Analyzer
# =============================================================================

class ManufacturingSemanticAnalyzer:
    """
    Parses textual content, identifying domain entities and multi-entity
    relational patterns without inventing unstated technical components.
    """

    @classmethod
    def extract_entities(cls, text: str) -> List[RecognizedEntity]:
        """Finds all occurrences of manufacturing enterprise entities in text."""
        lowered = text.lower()
        recognized: List[RecognizedEntity] = []

        # Sort terms by length descending to match multi-word phrases first
        all_terms: List[Tuple[str, EntityCategory]] = []
        for cat, terms in MANUFACTURING_VOCABULARY.items():
            for t in terms:
                all_terms.append((t, cat))
        all_terms.sort(key=lambda x: len(x[0]), reverse=True)

        found_spans: List[Tuple[int, int]] = []

        for term, cat in all_terms:
            # Word boundary regex matching
            escaped = re.escape(term)
            pattern = re.compile(rf"\b{escaped}\b", re.IGNORECASE)
            for m in pattern.finditer(lowered):
                span = (m.start(), m.end())
                # Check for overlap with already found longer terms
                if not any(s[0] <= span[0] and span[1] <= s[1] for s in found_spans):
                    found_spans.append(span)
                    recognized.append(RecognizedEntity(
                        term=m.group(0),
                        canonical_name=term.upper(),
                        category=cat,
                        position=m.start()
                    ))

        # Sort by position in text
        recognized.sort(key=lambda x: x.position)
        return recognized

    @classmethod
    def detect_relational_patterns(cls, text: str) -> List[SemanticPatternMatch]:
        """
        Detects specific entity-to-entity flows and relational structures.
        Faithfully reflects user inputs.
        """
        lowered = text.lower()
        matches: List[SemanticPatternMatch] = []

        # 1. SAP -> MES / ERP -> Plant Edge Integration Pattern
        erp_terms = ["sap", "s/4hana", "s4hana", "ecc", "erp"]
        mes_terms = ["mes", "mom", "shop floor", "plant edge", "edge", "scada"]
        has_erp = any(re.search(rf"\b{re.escape(t)}\b", lowered) for t in erp_terms)
        has_mes = any(re.search(rf"\b{re.escape(t)}\b", lowered) for t in mes_terms)

        if has_erp and has_mes:
            # Check for integration direction indicators (->, to, exchange, sync, interface)
            has_connector = any(c in lowered for c in ["->", "-->", "to", "sync", "interface", "integration", "push", "pull", "stream", "bridge"])
            matches.append(SemanticPatternMatch(
                pattern_type=SemanticPatternType.INTEGRATION_FLOW,
                matched_sequence=["ERP (SAP)", "Middleware / Event Mesh", "MES / Shop Floor"],
                confidence=0.95 if has_connector else 0.85,
                recommended_primitive="integration_architecture",
                explanation="SAP and MES co-occur with integration intent; should be represented as a directional integration architecture, not isolated cards."
            ))

        # 2. Production Order -> Operation -> Material -> WIP Manufacturing Flow
        flow_keywords = ["production order", "work order", "operation", "material", "wip", "routing", "shift", "confirmation"]
        present_flow_terms = [k for k in flow_keywords if re.search(rf"\b{re.escape(k)}\b", lowered)]
        if len(present_flow_terms) >= 3 or ("production order" in lowered and "operation" in lowered):
            matches.append(SemanticPatternMatch(
                pattern_type=SemanticPatternType.MANUFACTURING_FLOW,
                matched_sequence=present_flow_terms,
                confidence=0.92,
                recommended_primitive="horizontal_process_flow",
                explanation="Order release cascading into workstation operations and WIP movements; representable as a manufacturing process flow."
            ))

        # 3. Serial Number -> Components -> Parameters -> Quality (Genealogy / As-Built)
        genealogy_keywords = ["serial", "serial number", "component", "genealogy", "as-built", "process parameter", "parent", "child", "lot", "batch"]
        present_gen_terms = [k for k in genealogy_keywords if re.search(rf"\b{re.escape(k)}\b", lowered)]
        if ("genealogy" in lowered or "as-built" in lowered) or len(present_gen_terms) >= 3:
            matches.append(SemanticPatternMatch(
                pattern_type=SemanticPatternType.GENEALOGY_TRACEABILITY,
                matched_sequence=present_gen_terms,
                confidence=0.94,
                recommended_primitive="genealogy_tree",
                explanation="Serial number traced through parent-child component lots, process parameters, and inspection results; representable as a genealogy tree."
            ))

        # 4. Plant -> Work Center -> Machine -> Operator -> Shift (Operational Hierarchy)
        hier_keywords = ["plant", "work center", "machine", "operator", "shift", "site", "cell"]
        present_hier_terms = [k for k in hier_keywords if re.search(rf"\b{re.escape(k)}\b", lowered)]
        if len(present_hier_terms) >= 3 or ("plant" in lowered and "work center" in lowered and "machine" in lowered):
            matches.append(SemanticPatternMatch(
                pattern_type=SemanticPatternType.OPERATIONAL_HIERARCHY,
                matched_sequence=present_hier_terms,
                confidence=0.90,
                recommended_primitive="enterprise_to_shopfloor",
                explanation="ISA-95 operational decomposition from Plant down to Work Center, Machine, Operator, and Shift; representable as an operational hierarchy."
            ))

        # 5. KPI -> Business Decision -> Action (Decision Loop / Outcome Chain)
        decision_keywords = ["kpi", "decision", "action", "outcome", "lever", "closed-loop", "trigger", "steer"]
        present_dec_terms = [k for k in decision_keywords if re.search(rf"\b{re.escape(k)}\b", lowered)]
        if ("kpi" in lowered and ("decision" in lowered or "action" in lowered)) or len(present_dec_terms) >= 3:
            matches.append(SemanticPatternMatch(
                pattern_type=SemanticPatternType.DECISION_LOOP,
                matched_sequence=present_dec_terms,
                confidence=0.88,
                recommended_primitive="decision_flow",
                explanation="Telemetry and KPIs driving operational decisions and immediate corrective action; representable as a closed-loop decision flow."
            ))

        # 6. Quality Exception: Tolerance -> Defect -> NCR -> CAPA -> Rework
        quality_keywords = ["defect", "ncr", "capa", "rework", "non-conformance", "tolerance", "scrap", "quarantine"]
        present_qual_terms = [k for k in quality_keywords if re.search(rf"\b{re.escape(k)}\b", lowered)]
        if len(present_qual_terms) >= 2 and any(t in ["ncr", "capa", "rework", "defect"] for t in present_qual_terms):
            matches.append(SemanticPatternMatch(
                pattern_type=SemanticPatternType.QUALITY_EXCEPTION,
                matched_sequence=present_qual_terms,
                confidence=0.91,
                recommended_primitive="exception_rework_flow",
                explanation="Quality non-conformance logging with NCR, CAPA, and rework loopback; representable as an exception rework flow."
            ))

        # Sort matches by confidence descending
        matches.sort(key=lambda x: x.confidence, reverse=True)
        return matches

    @classmethod
    def recommend_visualization(cls, title: str, narrative_subtitle: str = "", body_text: str = "") -> Optional[str]:
        """
        Evaluates input text and recommends the optimal visual primitive
        based on the detected manufacturing enterprise semantics.
        """
        combined = f"{title} {narrative_subtitle} {body_text}"
        matches = cls.detect_relational_patterns(combined)
        if matches:
            return matches[0].recommended_primitive
        return None
