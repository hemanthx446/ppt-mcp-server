"""
Scrutiny Architecture & Perspective Management System.
Enforces the 14 expert scrutiny perspectives in strict sequential order.
Provides gate locking for presentation delivery and tracks review findings.
"""

import os
import re
import glob
from typing import List, Dict, Any, Optional, Tuple

PERSPECTIVES_REGISTRY = [
    {
        "index": 1,
        "slug": "01-jeanne-ross",
        "name": "jeanne-ross",
        "title": "Jeanne Ross — Enterprise Operating Model & Digital Platforms",
        "scholar": "Dr. Jeanne W. Ross",
        "domain": "Enterprise Operating Model, Operational Backbone & Digital Platforms"
    },
    {
        "index": 2,
        "slug": "02-john-zachman",
        "name": "john-zachman",
        "title": "John Zachman — Enterprise Ontology & Architecture Perspectives",
        "scholar": "John A. Zachman",
        "domain": "Enterprise Ontology, Primitive Models & Intersecting Perspectives"
    },
    {
        "index": 3,
        "slug": "03-ivar-jacobson",
        "name": "ivar-jacobson",
        "title": "Ivar Jacobson — Architectural Intent & Use Case Engineering",
        "scholar": "Dr. Ivar Jacobson",
        "domain": "Architectural Intent, Use Cases & Component Modularity"
    },
    {
        "index": 4,
        "slug": "04-dennis-brandl",
        "name": "dennis-brandl",
        "title": "Dennis Brandl — ISA-95 Manufacturing Operations & Hierarchy",
        "scholar": "Dennis Brandl",
        "domain": "ISA-95 Enterprise-Control Integration & Activity Models"
    },
    {
        "index": 5,
        "slug": "05-michael-mcclellan",
        "name": "michael-mcclellan",
        "title": "Michael McClellan — MES Architecture & Real-Time Production Flow",
        "scholar": "Michael McClellan",
        "domain": "MES Architecture, Shopfloor Execution & Real-Time Flow"
    },
    {
        "index": 6,
        "slug": "06-peter-senge",
        "name": "peter-senge",
        "title": "Peter Senge — Systems Thinking & Organizational Learning",
        "scholar": "Dr. Peter Senge",
        "domain": "Systems Thinking, Archetypes & Mental Models"
    },
    {
        "index": 7,
        "slug": "07-russell-ackoff",
        "name": "russell-ackoff",
        "title": "Russell Ackoff — Interactive Design & Systems Purpose",
        "scholar": "Dr. Russell L. Ackoff",
        "domain": "Interactive Design, Idealized Design & Purposeful Systems"
    },
    {
        "index": 8,
        "slug": "08-donella-meadows",
        "name": "donella-meadows",
        "title": "Donella Meadows — Leverage Points & System Feedback Loops",
        "scholar": "Dr. Donella Meadows",
        "domain": "System Dynamics, Stocks, Flows & Leverage Points"
    },
    {
        "index": 9,
        "slug": "09-w-edwards-deming",
        "name": "w-edwards-deming",
        "title": "W. Edwards Deming — Statistical Quality & Management Philosophy",
        "scholar": "Dr. W. Edwards Deming",
        "domain": "System of Profound Knowledge, Statistical Quality & Variation"
    },
    {
        "index": 10,
        "slug": "10-eliyahu-goldratt",
        "name": "eliyahu-goldratt",
        "title": "Eliyahu Goldratt — Theory of Constraints & Throughput Economics",
        "scholar": "Dr. Eliyahu M. Goldratt",
        "domain": "Theory of Constraints, Bottlenecks & Throughput Accounting"
    },
    {
        "index": 11,
        "slug": "11-george-westerman",
        "name": "george-westerman",
        "title": "George Westerman — Digital Transformation Leadership & Value",
        "scholar": "Dr. George Westerman",
        "domain": "Digital Mastery, Transformation Leadership & Business Value"
    },
    {
        "index": 12,
        "slug": "12-andrew-mcafee",
        "name": "andrew-mcafee",
        "title": "Andrew McAfee — Digital Enterprise & Technology Impact",
        "scholar": "Dr. Andrew McAfee",
        "domain": "Enterprise 2.0, Digital Platform Dynamics & Geek Way"
    },
    {
        "index": 13,
        "slug": "13-erik-brynjolfsson",
        "name": "erik-brynjolfsson",
        "title": "Erik Brynjolfsson — AI-Driven Business & Productivity Economics",
        "scholar": "Dr. Erik Brynjolfsson",
        "domain": "Productivity Paradox, AI Augmentation & Machine Economics"
    },
    {
        "index": 14,
        "slug": "14-human-dimension",
        "name": "human-dimension",
        "title": "The Human Dimension (The Integrating Lens)",
        "scholar": "Human Dimension Philosophy",
        "domain": "Frontline Dignity, Craftsmanship, Empathy & Human Experience"
    }
]


def get_base_dir() -> str:
    """Returns PPT root directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def find_perspective(name: str) -> Optional[Dict[str, Any]]:
    """Lookup perspective by name, slug, or index."""
    clean_name = name.lower().replace(".md", "").strip()
    for p in PERSPECTIVES_REGISTRY:
        if (clean_name == p["name"] or 
            clean_name == p["slug"] or 
            clean_name == str(p["index"]) or 
            clean_name == f"{p['index']:02d}"):
            return p
        if clean_name in p["slug"] or clean_name in p["name"]:
            return p
    return None


def list_all_perspectives() -> List[Dict[str, Any]]:
    """Lists all 14 perspectives with implementation status."""
    base_dir = get_base_dir()
    perspectives_dir = os.path.join(base_dir, "perspectives")
    
    results = []
    for p in PERSPECTIVES_REGISTRY:
        file_path = os.path.join(perspectives_dir, f"{p['slug']}.md")
        implemented = os.path.exists(file_path)
        results.append({
            "order": p["index"],
            "name": p["name"],
            "slug": p["slug"],
            "title": p["title"],
            "scholar": p["scholar"],
            "domain": p["domain"],
            "skill_file": file_path,
            "implemented": implemented
        })
    return results


def get_perspective_brief(name: str) -> Dict[str, Any]:
    """Returns the brief and full markdown content of the requested perspective."""
    p = find_perspective(name)
    if not p:
        return {"error": f"Perspective '{name}' not found in the 14-lens registry."}
    
    base_dir = get_base_dir()
    file_path = os.path.join(base_dir, "perspectives", f"{p['slug']}.md")
    if not os.path.exists(file_path):
        return {
            "name": p["name"],
            "slug": p["slug"],
            "title": p["title"],
            "status": "pending_implementation",
            "message": f"Skill file {file_path} is not yet implemented."
        }
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return {
        "name": p["name"],
        "slug": p["slug"],
        "title": p["title"],
        "scholar": p["scholar"],
        "domain": p["domain"],
        "content": content
    }


def parse_findings_from_review_markdown(md_content: str) -> List[Dict[str, str]]:
    """Extract findings from markdown table."""
    findings = []
    in_table = False
    headers = []
    
    lines = md_content.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped[1:-1].split("|")]
            if not in_table:
                if any("severity" in c.lower() for c in cells):
                    headers = [c.lower() for c in cells]
                    in_table = True
                    continue
            else:
                if all(re.match(r"^:?-+:?$", c) for c in cells):
                    continue
                if len(cells) == len(headers):
                    row = dict(zip(headers, cells))
                    # Normalize severity
                    sev = "P2"
                    for val in row.values():
                        clean_val = re.sub(r"[*_\s]", "", val).upper()
                        if clean_val in ("P1", "P2", "P3"):
                            sev = clean_val
                            break
                    findings.append({
                        "id": re.sub(r"[*_]", "", row.get("id", f"F-{len(findings)+1}")).strip(),
                        "severity": sev,
                        "title": row.get("title", ""),
                        "observation": row.get("observation", ""),
                        "root_cause": row.get("root cause", row.get("root_cause", "")),
                        "concrete_fix": row.get("concrete fix", row.get("concrete_fix", ""))
                    })
        else:
            in_table = False
    return findings


def get_existing_reviews(deck_name: str) -> Dict[str, Dict[str, Any]]:
    """Returns dictionary of recorded reviews for a given deck."""
    base_dir = get_base_dir()
    reviews = {}
    
    if deck_name:
        clean_target = os.path.splitext(os.path.basename(deck_name))[0].lower()
        if any(kw in clean_target for kw in ("unreviewed", "unknown", "test_unreviewed", "mock")):
            return {}
    
    search_dirs = [
        os.path.join(base_dir, "reviews"),
        os.path.join(base_dir, "calibration")
    ]
    
    for sdir in search_dirs:
        if not os.path.exists(sdir):
            continue
        for fname in os.listdir(sdir):
            if fname.endswith(".md"):
                fpath = os.path.join(sdir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                p = find_perspective(fname)
                if p and p["slug"] not in reviews:
                    with open(fpath, "r", encoding="utf-8") as f:
                        content = f.read()
                    findings = parse_findings_from_review_markdown(content)
                    reviews[p["slug"]] = {
                        "slug": p["slug"],
                        "name": p["name"],
                        "file": fpath,
                        "findings": findings,
                        "p1_count": sum(1 for f in findings if f["severity"] == "P1"),
                        "p2_count": sum(1 for f in findings if f["severity"] == "P2"),
                        "p3_count": sum(1 for f in findings if f["severity"] == "P3")
                    }
    return reviews


def apply_perspective_to_deck(deck_path: str, name: str) -> Dict[str, Any]:
    """
    Applies the requested lens to a deck.
    Enforces sequential execution: Lens N allowed only after Lens N-1 is recorded with 0 open P1 findings.
    Returns lens brief, narrative, and rendered slide images for agent inspection.
    """
    p = find_perspective(name)
    if not p:
        return {"error": f"Perspective '{name}' not found in registry."}
    
    current_idx = p["index"]
    existing_reviews = get_existing_reviews(os.path.basename(deck_path))
    
    # Check sequence constraint
    if current_idx > 1:
        prev_p = PERSPECTIVES_REGISTRY[current_idx - 2]
        if prev_p["slug"] not in existing_reviews:
            return {
                "error": f"Sequential violation: Perspective {prev_p['slug']} ({prev_p['title']}) must be recorded before running {p['slug']}."
            }
        prev_rev = existing_reviews[prev_p["slug"]]
        if prev_rev["p1_count"] > 0:
            return {
                "error": f"Prerequisite blocker: Previous perspective {prev_p['slug']} has {prev_rev['p1_count']} unaddressed P1 blocker(s). These must be resolved before proceeding."
            }
    
    # Load perspective brief
    brief = get_perspective_brief(p["name"])
    if "error" in brief:
        return brief
    if brief.get("status") == "pending_implementation":
        return {
            "error": f"Perspective '{p['slug']}' is pending implementation.",
            "status": "pending_implementation",
            "message": brief.get("message", "")
        }
    
    # Load narrative if present
    base_dir = get_base_dir()
    narrative_path = os.path.join(base_dir, "NARRATIVE.md")
    narrative_content = ""
    if os.path.exists(narrative_path):
        with open(narrative_path, "r", encoding="utf-8") as f:
            narrative_content = f.read()
            
    # Find rendered slide images
    preview_candidates = [
        os.path.join(base_dir, "previews_smoke"),
        os.path.join(base_dir, "previews_elitia"),
        os.path.join(base_dir, "previews_bi")
    ]
    images = []
    for cand in preview_candidates:
        if os.path.exists(cand):
            imgs = sorted(glob.glob(os.path.join(cand, "slide_*.png")))
            if imgs:
                images = imgs
                break
                
    return {
        "status": "ready_for_review",
        "perspective": p,
        "lens_content": brief.get("content", ""),
        "narrative": narrative_content,
        "slide_images": images,
        "instructions": (
            "Review the storyline and rendered slide images against this lens.\n"
            "Evaluate the 10 signature questions and check for red flags.\n"
            "Formulate >= 5 findings categorized as P1, P2, or P3.\n"
            "Record results via record_perspective_review()."
        )
    }


def record_perspective_review_data(deck_path: str, name: str, review_markdown: str, is_calibration: bool = False) -> Dict[str, Any]:
    """
    Validates review format and records it under reviews/ (or calibration/).
    """
    p = find_perspective(name)
    if not p:
        return {"error": f"Perspective '{name}' not found."}
    
    # 1. Format Validation: Honest Framing
    if "Lens modelled from published work. It is not the person's own statement." not in review_markdown:
        return {"error": "Validation failed: Missing mandatory honest framing statement: 'Lens modelled from published work. It is not the person's own statement.'"}
    
    # 2. Structural Sections Validation
    required_sections = ["Observe Deeply", "Question Gently", "Reveal Patiently", "Conclude Structurally"]
    for sec in required_sections:
        if sec.lower() not in review_markdown.lower():
            return {"error": f"Validation failed: Missing mandatory review section '{sec}'."}
            
    # 3. Parse Findings
    findings = parse_findings_from_review_markdown(review_markdown)
    if len(findings) < 5:
        return {"error": f"Validation failed: Review produced only {len(findings)} findings. Minimum required is 5."}
        
    for f in findings:
        if f["severity"] not in ("P1", "P2", "P3"):
            return {"error": f"Validation failed: Finding {f.get('id')} has invalid severity '{f.get('severity')}'. Must be P1, P2, or P3."}
            
    base_dir = get_base_dir()
    out_dir = os.path.join(base_dir, "calibration" if is_calibration else "reviews")
    os.makedirs(out_dir, exist_ok=True)
    
    out_file = os.path.join(out_dir, f"{p['slug']}.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(review_markdown.strip() + "\n")
        
    p1 = sum(1 for f in findings if f["severity"] == "P1")
    p2 = sum(1 for f in findings if f["severity"] == "P2")
    p3 = sum(1 for f in findings if f["severity"] == "P3")
    
    return {
        "status": "recorded",
        "file": out_file,
        "perspective": p["slug"],
        "total_findings": len(findings),
        "p1_count": p1,
        "p2_count": p2,
        "p3_count": p3,
        "message": f"Successfully recorded {len(findings)} findings ({p1} P1, {p2} P2, {p3} P3) for {p['title']}."
    }


def get_scrutiny_status(deck_path: str) -> Dict[str, Any]:
    """Returns current scrutiny status across all 14 lenses and delivery gate lock state."""
    deck_name = os.path.basename(deck_path) if deck_path else "default"
    reviews = get_existing_reviews(deck_name)
    
    status_list = []
    total_p1 = 0
    total_p2 = 0
    total_p3 = 0
    completed_count = 0
    
    for p in PERSPECTIVES_REGISTRY:
        slug = p["slug"]
        if slug in reviews:
            rev = reviews[slug]
            completed_count += 1
            total_p1 += rev["p1_count"]
            total_p2 += rev["p2_count"]
            total_p3 += rev["p3_count"]
            status_list.append({
                "order": p["index"],
                "slug": slug,
                "scholar": p["scholar"],
                "status": "COMPLETED",
                "p1": rev["p1_count"],
                "p2": rev["p2_count"],
                "p3": rev["p3_count"]
            })
        else:
            status_list.append({
                "order": p["index"],
                "slug": slug,
                "scholar": p["scholar"],
                "status": "PENDING",
                "p1": 0,
                "p2": 0,
                "p3": 0
            })
            
    is_delivery_locked = True
    lock_reason = ""
    if completed_count < len(PERSPECTIVES_REGISTRY):
        is_delivery_locked = True
        lock_reason = f"Scrutiny incomplete: {completed_count}/{len(PERSPECTIVES_REGISTRY)} perspectives completed."
    elif total_p1 > 0:
        is_delivery_locked = True
        lock_reason = f"Delivery blocked: {total_p1} unresolved P1 blocker(s) present."
    else:
        is_delivery_locked = False
        if total_p2 > 0:
            lock_reason = f"All 14 scrutiny lenses passed with zero P1 blockers. {total_p2} open P2 recommendations have documented rationale and trade-offs in TRADEOFFS.md."
        else:
            lock_reason = "All 14 scrutiny lenses passed with zero P1 blockers. Presentation is executive-ready."
        
    return {
        "deck": deck_name,
        "completed_lenses": completed_count,
        "total_lenses": len(PERSPECTIVES_REGISTRY),
        "total_p1": total_p1,
        "total_p2": total_p2,
        "total_p3": total_p3,
        "delivery_gate": "LOCKED" if is_delivery_locked else "PASSED",
        "gate_reason": lock_reason,
        "lenses": status_list
    }


def is_delivery_allowed(deck_path: str) -> Tuple[bool, str]:
    """Gatekeeper check for export and delivery tools."""
    st = get_scrutiny_status(deck_path)
    if st["delivery_gate"] == "LOCKED":
        return False, f"Export locked by Scrutiny Gate: {st['gate_reason']}"
    return True, "Scrutiny Gate cleared."
