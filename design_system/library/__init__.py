"""
Enterprise Visual Primitive Library.

Provides 60 first-class, reusable, theme-aware, data-driven visual primitives
rendered using native editable PowerPoint shapes, tables, and charts.

Categories:
  1. ARCHITECTURE (Primitives 1–9)
  2. PROCESS (Primitives 10–16)
  3. DATA (Primitives 17–21)
  4. ANALYTICS (Primitives 22–34)
  5. BUSINESS (Primitives 35–41)
  6. DELIVERY (Primitives 42–46)
  7. GOVERNANCE (Primitives 47–50)
  8. STRUCTURED INFORMATION (Primitives 51–56)
  9. NARRATIVE (Primitives 57–60)
"""

from .architecture import (
    SystemArchitecturePrimitive,
    LayeredArchitecturePrimitive,
    EnterpriseToShopfloorPrimitive,
    ApplicationLandscapePrimitive,
    IntegrationArchitecturePrimitive,
    DataFlowArchitecturePrimitive,
    SecurityBoundaryPrimitive,
    DeploymentArchitecturePrimitive,
    CloudEdgeArchitecturePrimitive,
)

from .process import (
    HorizontalProcessFlowPrimitive,
    VerticalProcessFlowPrimitive,
    ValueStreamPrimitive,
    OperationalWorkflowPrimitive,
    SwimlaneProcessPrimitive,
    DecisionFlowPrimitive,
    ExceptionReworkFlowPrimitive,
)

from .data import (
    DataLineagePrimitive,
    EntityRelationshipPrimitive,
    GenealogyTreePrimitive,
    ParentChildRelationshipPrimitive,
    DataLifecyclePrimitive,
)

from .analytics import (
    KPIStripPrimitive,
    ExecutiveDashboardPrimitive,
    TrendChartPrimitive,
    BarChartPrimitive,
    StackedBarPrimitive,
    LineChartPrimitive,
    WaterfallPrimitive,
    ParetoPrimitive,
    HeatmapPrimitive,
    VarianceViewPrimitive,
    CapacityVsDemandPrimitive,
    AgingAnalysisPrimitive,
    RiskMatrixPrimitive,
)

from .business import (
    CapabilityMapPrimitive,
    OperatingModelPrimitive,
    OutcomeChainPrimitive,
    ValueDriverTreePrimitive,
    DecisionMatrixPrimitive,
    MaturityModelPrimitive,
    CurrentVsFutureStatePrimitive,
)

from .delivery import (
    TransformationRoadmapPrimitive,
    TimelinePrimitive,
    MilestoneGatesPrimitive,
    ReleasePlanPrimitive,
    WorkstreamViewPrimitive,
)

from .governance import (
    ApprovalGatesPrimitive,
    RACIResponsibilityPrimitive,
    ControlFrameworkPrimitive,
    GovernanceModelPrimitive,
)

from .structured_info import (
    ProfessionalTablePrimitive,
    ComparisonMatrixPrimitive,
    CommercialTablePrimitive,
    KPITablePrimitive,
    ActionRegisterPrimitive,
    RiskRegisterPrimitive,
)

from .narrative import (
    ExecutiveStatementPrimitive,
    InsightAndEvidencePrimitive,
    KeyTakeawayPrimitive,
    SectionDividerPrimitive,
)

from .registry import (
    PRIMITIVE_CATALOG,
    list_primitives_catalog,
    get_primitive_metadata,
    normalize_primitive_key,
)

__all__ = [
    # Architecture
    "SystemArchitecturePrimitive",
    "LayeredArchitecturePrimitive",
    "EnterpriseToShopfloorPrimitive",
    "ApplicationLandscapePrimitive",
    "IntegrationArchitecturePrimitive",
    "DataFlowArchitecturePrimitive",
    "SecurityBoundaryPrimitive",
    "DeploymentArchitecturePrimitive",
    "CloudEdgeArchitecturePrimitive",
    # Process
    "HorizontalProcessFlowPrimitive",
    "VerticalProcessFlowPrimitive",
    "ValueStreamPrimitive",
    "OperationalWorkflowPrimitive",
    "SwimlaneProcessPrimitive",
    "DecisionFlowPrimitive",
    "ExceptionReworkFlowPrimitive",
    # Data
    "DataLineagePrimitive",
    "EntityRelationshipPrimitive",
    "GenealogyTreePrimitive",
    "ParentChildRelationshipPrimitive",
    "DataLifecyclePrimitive",
    # Analytics
    "KPIStripPrimitive",
    "ExecutiveDashboardPrimitive",
    "TrendChartPrimitive",
    "BarChartPrimitive",
    "StackedBarPrimitive",
    "LineChartPrimitive",
    "WaterfallPrimitive",
    "ParetoPrimitive",
    "HeatmapPrimitive",
    "VarianceViewPrimitive",
    "CapacityVsDemandPrimitive",
    "AgingAnalysisPrimitive",
    "RiskMatrixPrimitive",
    # Business
    "CapabilityMapPrimitive",
    "OperatingModelPrimitive",
    "OutcomeChainPrimitive",
    "ValueDriverTreePrimitive",
    "DecisionMatrixPrimitive",
    "MaturityModelPrimitive",
    "CurrentVsFutureStatePrimitive",
    # Delivery
    "TransformationRoadmapPrimitive",
    "TimelinePrimitive",
    "MilestoneGatesPrimitive",
    "ReleasePlanPrimitive",
    "WorkstreamViewPrimitive",
    # Governance
    "ApprovalGatesPrimitive",
    "RACIResponsibilityPrimitive",
    "ControlFrameworkPrimitive",
    "GovernanceModelPrimitive",
    # Structured Information
    "ProfessionalTablePrimitive",
    "ComparisonMatrixPrimitive",
    "CommercialTablePrimitive",
    "KPITablePrimitive",
    "ActionRegisterPrimitive",
    "RiskRegisterPrimitive",
    # Narrative
    "ExecutiveStatementPrimitive",
    "InsightAndEvidencePrimitive",
    "KeyTakeawayPrimitive",
    "SectionDividerPrimitive",
    # Registry
    "PRIMITIVE_CATALOG",
    "list_primitives_catalog",
    "get_primitive_metadata",
    "normalize_primitive_key",
]
