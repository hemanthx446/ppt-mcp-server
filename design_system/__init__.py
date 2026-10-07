"""
Presentation Design System for Enterprise Architecture & Consulting Decks.

Separates:
  CONTENT -> SEMANTIC STRUCTURE -> VISUAL INTENT -> LAYOUT SELECTION -> VISUAL PRIMITIVES -> PPTX RENDERER
"""

from .typography import TypographyToken, TypographySystem, FONT_FAMILY
from .spacing import SpacingSystem, CanvasBounds, Margins, SpacingScale, GridCalculator
from .color import ColorSystem, Theme, ExecutiveNavyTheme, ConsultingSlateTheme, RGB
from .semantic import (
    VisualIntent,
    SemanticSlide,
    ContentBlock,
    KeyMetric,
    TableData,
    ProcessStep,
    ArchitectureTier,
    RoadmapPhase
)
from .primitives import (
    HeaderPrimitive,
    FooterPrimitive,
    SurfacePrimitive,
    TextPrimitive,
    MetricPrimitive,
    TablePrimitive,
    ConnectorPrimitive,
    CalloutBannerPrimitive,
)
from .renderer import PPTXRenderer
from .intelligence import (
    AudienceType,
    InformationRelationship,
    VisualRepresentation,
    SlideContext,
    CompositeSlot,
    CompositeSlideSpec,
    VisualIntelligenceEngine
)

__all__ = [
    "FONT_FAMILY",
    "TypographyToken",
    "TypographySystem",
    "SpacingSystem",
    "CanvasBounds",
    "Margins",
    "SpacingScale",
    "GridCalculator",
    "ColorSystem",
    "Theme",
    "ExecutiveNavyTheme",
    "ConsultingSlateTheme",
    "RGB",
    "VisualIntent",
    "SemanticSlide",
    "ContentBlock",
    "KeyMetric",
    "TableData",
    "ProcessStep",
    "ArchitectureTier",
    "RoadmapPhase",
    "HeaderPrimitive",
    "FooterPrimitive",
    "SurfacePrimitive",
    "TextPrimitive",
    "MetricPrimitive",
    "TablePrimitive",
    "ConnectorPrimitive",
    "CalloutBannerPrimitive",
    "PPTXRenderer",
    "AudienceType",
    "InformationRelationship",
    "VisualRepresentation",
    "SlideContext",
    "CompositeSlot",
    "CompositeSlideSpec",
    "VisualIntelligenceEngine",
    # Composition Engine
    "NarrativeSection",
    "SectionArchetype",
    "SECTION_ARCHETYPES",
    "VisualRhythmController",
    "ArchitectureDeckSpec",
    "EnterpriseArchitectureCompositionEngine",
    # Executive Dashboard Engine
    "DashboardArchetype",
    "DashboardQuestionClassifier",
    "ExecutiveCockpitSpec",
    "ExecutiveDashboardComposer",
    # Manufacturing Vocabulary
    "EntityCategory",
    "SemanticPatternType",
    "RecognizedEntity",
    "SemanticPatternMatch",
    "MANUFACTURING_VOCABULARY",
    "ManufacturingSemanticAnalyzer",
    # Enterprise Architecture Engine
    "ArchElementType",
    "FlowDirection",
    "ArchElement",
    "ArchFlow",
    "ArchLayer",
    "ArchAnnotation",
    "ArchitectureDiagramSpec",
    "ArchitectureElementRenderer",
    "EnterpriseArchitectureComposer",
    "ArchitectureBlueprintFactory",
    # Enterprise Table Engine
    "TableArchetype",
    "TableRowItem",
    "EnterpriseTableSpec",
    "TableDataClassifier",
    "EnterpriseTableComposer",
    "EnterpriseTableFactory",
    # Visual Density & Whitespace Intelligence
    "VisualDensity",
    "VisualDensityClassifier",
    "DensityEvaluation",
    "WhitespaceIntelligenceEngine",
    "LowDensitySlideRenderer",
    # Narrative Intelligence
    "NarrativeFramework",
    "AudienceCognitiveObjective",
    "NarrativeSlideIntent",
    "NarrativeIntelligenceEngine",
    # Architecture Review Engine
    "ArchitecturalLens",
    "InquiryReviewResult",
    "ArchitectureReviewScorecard",
    "ArchitectureReviewEngine",
    # Presentation Quality Gate
    "QualityStatus",
    "QualityDimensionAudit",
    "QualityGateReport",
    "PresentationQualityGate",
    # Scenario Engine
    "VisualFormDescriptor",
    "SemanticVisualFormResolver",
    "DomainPayloadSynthesizer",
    "ScenarioDeckResult",
    "ScenarioPresentationEngine",
]

from .composition import (
    NarrativeSection,
    SectionArchetype,
    SECTION_ARCHETYPES,
    VisualRhythmController,
    ArchitectureDeckSpec,
    EnterpriseArchitectureCompositionEngine,
)

from .dashboard import (
    DashboardArchetype,
    DashboardQuestionClassifier,
    ExecutiveCockpitSpec,
    ExecutiveDashboardComposer,
)

from .manufacturing_vocabulary import (
    EntityCategory,
    SemanticPatternType,
    RecognizedEntity,
    SemanticPatternMatch,
    MANUFACTURING_VOCABULARY,
    ManufacturingSemanticAnalyzer,
)

from .architecture_engine import (
    ArchElementType,
    FlowDirection,
    ArchElement,
    ArchFlow,
    ArchLayer,
    ArchAnnotation,
    ArchitectureDiagramSpec,
    ArchitectureElementRenderer,
    EnterpriseArchitectureComposer,
    ArchitectureBlueprintFactory,
)

from .table_engine import (
    TableArchetype,
    TableRowItem,
    EnterpriseTableSpec,
    TableDataClassifier,
    EnterpriseTableComposer,
    EnterpriseTableFactory,
)

from .density_intelligence import (
    VisualDensity,
    VisualDensityClassifier,
    DensityEvaluation,
    WhitespaceIntelligenceEngine,
    LowDensitySlideRenderer,
)

from .narrative_intelligence import (
    NarrativeFramework,
    AudienceCognitiveObjective,
    NarrativeSlideIntent,
    NarrativeIntelligenceEngine,
)

from .architecture_review import (
    ArchitecturalLens,
    InquiryReviewResult,
    ArchitectureReviewScorecard,
    ArchitectureReviewEngine,
)

from .quality_gate import (
    QualityStatus,
    QualityDimensionAudit,
    QualityGateReport,
    PresentationQualityGate,
)

from .scenario_engine import (
    VisualFormDescriptor,
    SemanticVisualFormResolver,
    DomainPayloadSynthesizer,
    ScenarioDeckResult,
    ScenarioPresentationEngine,
)
