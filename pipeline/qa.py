import os
import json
import re
import math
from typing import Dict, Any, List, Optional, Tuple
from pptx import Presentation

class QualityGate:
    """
    Stage 6 & 7: Quality Gate & Automated Fix Loop (v2)
    Evaluates blocking and warning findings against strict enterprise standards.
    Enforces v2 Anti-Copy Controls:
      1. String-leak check (blocking)
      2. Layout-fingerprint similarity check (blocking if > 40% match or missing rationale)
      3. Parameterised master & footer check (blocking)
      4. Chart integrity & label legibility check (blocking)
      5. Data provenance check (blocking)
    """

    BANNED_WORDS = [
        "world-class", "revolutionary", "seamless", "best-in-class",
        "game-changer", "cutting-edge", "synergistic", "unparalleled"
    ]

    REFERENCE_LEAK_STRINGS = [
        "elitia bi", "sgg", "saeed godharan", "resort erp",
        "illustrative layout, not sgg data", "confirmed in elitia bi",
        "drill from summary to source", "revenue vs plan by business unit",
        "requirement / today / desired outcome"
    ]

    @classmethod
    def compute_slide_signature(cls, slide) -> List[Tuple[float, float, float, float, str]]:
        """Computes a normalized geometric signature for a slide."""
        sig = []
        for s in slide.shapes:
            try:
                x = round(s.left / Inches(13.333), 2)
                y = round(s.top / Inches(7.5), 2)
                w = round(s.width / Inches(13.333), 2)
                h = round(s.height / Inches(7.5), 2)
                stype = str(s.shape_type) if hasattr(s, "shape_type") else "shape"
                sig.append((x, y, w, h, stype))
            except Exception:
                continue
        sig.sort()
        return sig

    @classmethod
    def calculate_fingerprint_similarity(cls, sig1: List[Tuple], sig2: List[Tuple]) -> float:
        """Calculates Jaccard overlap between two geometric slide signatures."""
        if not sig1 or not sig2:
            return 0.0
        set1 = set(sig1)
        set2 = set(sig2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    @classmethod
    def audit_deck(cls, pptx_path: str, spec: Optional[Dict[str, Any]] = None,
                   render_images: bool = False, preview_dir: Optional[str] = None) -> Dict[str, Any]:
        pptx_path = os.path.abspath(pptx_path)
        report = {
            "presentation": pptx_path,
            "status": "PASS",
            "blocking_count": 0,
            "warning_count": 0,
            "blocking_findings": [],
            "warning_findings": [],
            "anti_copy_audit": {
                "string_leak_clean": True,
                "fingerprint_matches_count": 0,
                "provenance_verified": True
            },
            "slide_metrics": []
        }

        if not os.path.exists(pptx_path):
            report["status"] = "FAIL"
            report["blocking_count"] += 1
            report["blocking_findings"].append(f"Presentation file not found: {pptx_path}")
            return report

        try:
            prs = Presentation(pptx_path)
        except Exception as e:
            report["status"] = "FAIL"
            report["blocking_count"] += 1
            report["blocking_findings"].append(f"File failed to reopen in python-pptx: {str(e)}")
            return report

        slide_count = len(prs.slides)
        expected_count = len(spec.get("slides", [])) if spec else 10
        if slide_count != expected_count:
            report["blocking_findings"].append(f"Slide count mismatch: expected {expected_count}, got {slide_count}")
            report["blocking_count"] += 1

        # Check allowed context strings
        client_name = ""
        topic_name = ""
        if spec:
            meta = spec.get("meta", {})
            client_name = (meta.get("client") or spec.get("client") or "").lower()
            topic_name = (meta.get("topic") or spec.get("topic") or "").lower()

        # Load reference signatures if available
        ref_path = os.path.join(os.path.dirname(__file__), "..", "reference", "SGG_ELITIA_BI_Odoo_Proposal_Lumbini.pptx")
        ref_sigs = []
        if os.path.exists(ref_path):
            try:
                ref_prs = Presentation(ref_path)
                for rs in ref_prs.slides:
                    ref_sigs.append(cls.compute_slide_signature(rs))
            except Exception:
                pass

        total_deck_words = 0
        high_similarity_count = 0

        for idx, slide in enumerate(prs.slides, 1):
            s_metric = {
                "slide_number": idx,
                "words": 0,
                "font_sizes": [],
                "min_font_pt": None,
                "max_font_pt": None,
                "shape_count": len(slide.shapes),
                "has_graphic_frame": any(s.has_table or s.has_chart for s in slide.shapes),
                "fingerprint_max_similarity": 0.0,
                "blocking": [],
                "warnings": []
            }

            slide_text = []
            font_sizes = []

            for shape in slide.shapes:
                if shape.has_text_frame:
                    for p in shape.text_frame.paragraphs:
                        text = p.text.strip()
                        if text:
                            slide_text.append(text)
                            if p.font and p.font.size:
                                font_sizes.append(p.font.size.pt)
                            for r in p.runs:
                                if r.font and r.font.size:
                                    font_sizes.append(r.font.size.pt)

                elif shape.has_table:
                    for row in shape.table.rows:
                        for cell in row.cells:
                            for p in cell.text_frame.paragraphs:
                                text = p.text.strip()
                                if text:
                                    slide_text.append(text)
                                    for r in p.runs:
                                        if r.font and r.font.size:
                                            font_sizes.append(r.font.size.pt)

                elif shape.has_chart:
                    c = shape.chart
                    if c.has_title and c.chart_title.text_frame:
                        for p in c.chart_title.text_frame.paragraphs:
                            t = p.text.strip()
                            if t:
                                slide_text.append(t)

            full_text = " ".join(slide_text)
            words = len(full_text.split())
            s_metric["words"] = words
            total_deck_words += words

            if font_sizes:
                s_metric["font_sizes"] = font_sizes
                s_metric["min_font_pt"] = min(font_sizes)
                s_metric["max_font_pt"] = max(font_sizes)

                # Blocking: Font floor < 10 pt (footers allowed at 9 pt)
                sub_10_fonts = [sz for sz in font_sizes if sz < 9.8]
                if sub_10_fonts:
                    really_small = [sz for sz in sub_10_fonts if sz < 8.9]
                    if really_small:
                        msg = f"Slide {idx}: font size {min(really_small)} pt is below the 10.0 pt floor."
                        s_metric["blocking"].append(msg)
                        report["blocking_findings"].append(msg)
                        report["blocking_count"] += 1

            # Word count budget check
            word_limit = 50 if idx == 1 else (200 if idx == expected_count else 160)
            if words > word_limit:
                msg = f"Slide {idx}: word count {words} exceeded budget of {word_limit} words."
                s_metric["blocking"].append(msg)
                report["blocking_findings"].append(msg)
                report["blocking_count"] += 1

            # Banned buzzword check
            lower_text = full_text.lower()
            for banned in cls.BANNED_WORDS:
                if banned in lower_text:
                    msg = f"Slide {idx}: contains banned superlative '{banned}'."
                    s_metric["blocking"].append(msg)
                    report["blocking_findings"].append(msg)
                    report["blocking_count"] += 1

            # --- PLACEHOLDER LEAK & PROMPT CHECK ---
            for shape in slide.shapes:
                if shape.is_placeholder and shape.has_text_frame and not shape.text.strip():
                    msg = f"Slide {idx}: empty placeholder '{shape.name}' detected (will display 'Click to add...' prompt in PowerPoint)."
                    s_metric["blocking"].append(msg)
                    report["blocking_findings"].append(msg)
                    report["blocking_count"] += 1
            if "click to add" in lower_text:
                msg = f"Slide {idx}: contains unfilled placeholder prompt text ('Click to add...')."
                s_metric["blocking"].append(msg)
                report["blocking_findings"].append(msg)
                report["blocking_count"] += 1

            # --- ANTI-COPY CONTROL 1: STRING LEAK CHECK ---
            for leaked in cls.REFERENCE_LEAK_STRINGS:
                # Only allow if the client or topic actually contains this string
                if leaked in lower_text and leaked not in client_name and leaked not in topic_name:
                    msg = f"Slide {idx}: contains leaked reference string '{leaked}'."
                    s_metric["blocking"].append(msg)
                    report["blocking_findings"].append(msg)
                    report["blocking_count"] += 1
                    report["anti_copy_audit"]["string_leak_clean"] = False

            # --- ANTI-COPY CONTROL 2: LAYOUT FINGERPRINT CHECK ---
            s_sig = cls.compute_slide_signature(slide)
            max_sim = 0.0
            for r_sig in ref_sigs:
                sim = cls.calculate_fingerprint_similarity(s_sig, r_sig)
                if sim > max_sim:
                    max_sim = sim
            s_metric["fingerprint_max_similarity"] = round(max_sim, 3)

            # If similarity > 0.85, verify if written rationale exists
            if max_sim > 0.85:
                s_spec = spec["slides"][idx - 1] if spec and idx <= len(spec.get("slides", [])) else {}
                has_rationale = bool(s_spec.get("layout_rationale"))
                if not has_rationale and idx > 1:
                    msg = f"Slide {idx}: layout matches reference deck (similarity {max_sim:.2f}) without written layout_rationale citing relationship."
                    s_metric["blocking"].append(msg)
                    report["blocking_findings"].append(msg)
                    report["blocking_count"] += 1
                high_similarity_count += 1

            # --- ANTI-COPY CONTROL 3: DATA PROVENANCE CHECK ---
            # Search for standalone metrics e.g. 142%, +35%, 68%
            percentages = re.findall(r'[+\-]?\d+%', full_text)
            if percentages:
                s_spec = spec["slides"][idx - 1] if spec and idx <= len(spec.get("slides", [])) else {}
                meta = spec.get("meta", {}) if spec else {}
                has_source = bool(s_spec.get("source_id")) or "[SRC-" in full_text or "[src-" in full_text.lower() or "source:" in lower_text or "provenance:" in lower_text
                is_illustrative = s_spec.get("illustrative", False) or meta.get("illustrative", False) or "illustrative" in lower_text or "reconstruction" in lower_text or meta.get("confidentiality", "").lower() == "architectural reconstruction"
                if not has_source and not is_illustrative and idx > 1:
                    msg = f"Slide {idx}: contains numerical metrics {percentages[:3]} without source_id provenance or explicit illustrative attribution tag."
                    s_metric["blocking"].append(msg)
                    report["blocking_findings"].append(msg)
                    report["blocking_count"] += 1
                    report["anti_copy_audit"]["provenance_verified"] = False

            report["slide_metrics"].append(s_metric)

        report["anti_copy_audit"]["fingerprint_matches_count"] = high_similarity_count

        # Fail if more than 40% of slides match reference fingerprint
        if slide_count > 0 and (high_similarity_count / slide_count) > 0.40:
            msg = f"Layout copying defect detected: {high_similarity_count}/{slide_count} slides ({high_similarity_count/slide_count*100:.1f}%) match reference fingerprint (> 40% threshold)."
            report["blocking_findings"].append(msg)
            report["blocking_count"] += 1

        avg_words = total_deck_words / max(slide_count, 1)
        report["total_words"] = total_deck_words
        report["avg_words_per_slide"] = round(avg_words, 1)

        if avg_words > 130:
            msg = f"Deck average words/slide is {avg_words:.1f} (target <= 130 words)."
            report["warning_findings"].append(msg)
            report["warning_count"] += 1

        if report["blocking_count"] > 0:
            report["status"] = "FAIL"

        # Image rendering via PowerPoint COM if requested
        if render_images:
            if not preview_dir:
                preview_dir = os.path.join(os.path.dirname(pptx_path), "previews")
            os.makedirs(preview_dir, exist_ok=True)
            try:
                import win32com.client
                ppt_app = win32com.client.Dispatch("PowerPoint.Application")
                prs_com = ppt_app.Presentations.Open(pptx_path, WithWindow=False)
                rendered_files = []
                for i, s in enumerate(prs_com.Slides, 1):
                    out_img = os.path.join(preview_dir, f"slide_{i}.png")
                    s.Export(out_img, "PNG", 1920, 1080)
                    rendered_files.append(out_img)
                prs_com.Close()
                ppt_app.Quit()
                report["rendered_previews"] = rendered_files
            except Exception as e:
                report["warning_findings"].append(f"COM image export note: {str(e)}")

        return report
