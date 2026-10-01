#!/usr/bin/env python3
"""Validate topic-local standards evidence registers without external dependencies."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from schema_validation import validate as validate_schema

ROOT=Path(__file__).resolve().parents[2]
TOPICS=ROOT/"knowledge"/"topics"
TOPIC_RE=re.compile(r"^(TOPIC-\d{2}-\d{3})")
STATUSES={"SOURCE_VERIFIED","PRIMARY_CORROBORATED","SECONDARY_CORROBORATED","MODEL_DERIVED_AUDIT_REQUIRED","CONFLICTED","NOT_RESEARCHED"}
FRAMEWORKS={"IFRS","US_GAAP","UK_GAAP","AASB","SEC","REGULATORY","OTHER"}
SOURCE_KINDS={"CURRENT_STANDARD","OFFICIAL_AMENDMENT","REGULATOR","OFFICIAL_TAXONOMY","PROFESSIONAL_LITERATURE","MODEL_KNOWLEDGE","OTHER"}

errors=[]; warnings=[]; seen={}
schema=json.loads((ROOT/"knowledge/standards-evidence/claim.schema.json").read_text())
topic_dirs=[p for p in TOPICS.iterdir() if p.is_dir() and TOPIC_RE.match(p.name)]
registers=list(TOPICS.glob("TOPIC-*/standards-claims.json"))

for path in registers:
    folder_id=TOPIC_RE.match(path.parent.name).group(1)
    try: doc=json.loads(path.read_text())
    except Exception as e:
        errors.append(f"{path}: invalid JSON: {e}"); continue
    errors.extend(f"{path}: {error}" for error in validate_schema(doc,schema))
    if doc.get("topic_id") != folder_id:
        errors.append(f"{path}: topic_id {doc.get('topic_id')!r} != {folder_id}")
    if not isinstance(doc.get("claims"),list):
        errors.append(f"{path}: claims must be an array"); continue
    for i,c in enumerate(doc["claims"]):
        loc=f"{path}:claims[{i}]"
        cid=c.get("claim_id")
        if not cid: errors.append(f"{loc}: missing claim_id")
        elif cid in seen: errors.append(f"{loc}: duplicate claim_id also in {seen[cid]}")
        else: seen[cid]=loc
        if c.get("framework") not in FRAMEWORKS: errors.append(f"{loc}: invalid framework")
        if not c.get("proposition"): errors.append(f"{loc}: empty proposition")
        status=c.get("evidence_status")
        if status not in STATUSES: errors.append(f"{loc}: invalid evidence_status")
        sources=c.get("sources")
        if not isinstance(sources,list): errors.append(f"{loc}: sources must be array"); sources=[]
        for j,src in enumerate(sources):
            sl=f"{loc}:sources[{j}]"
            if src.get("source_kind") not in SOURCE_KINDS: errors.append(f"{sl}: invalid source_kind")
            if not src.get("title"): errors.append(f"{sl}: missing title")
        audit=c.get("audit_required")
        if not isinstance(audit,bool): errors.append(f"{loc}: audit_required must be boolean")
        if status=="SOURCE_VERIFIED":
            inspected=[x for x in sources if x.get("inspected") is True and x.get("source_kind") in {"CURRENT_STANDARD","REGULATOR"}]
            if not inspected: errors.append(f"{loc}: SOURCE_VERIFIED lacks inspected current standard/regulator source")
            if c.get("reference_confidence")!="VERIFIED": errors.append(f"{loc}: SOURCE_VERIFIED requires VERIFIED reference_confidence")
            if audit: warnings.append(f"{loc}: SOURCE_VERIFIED still audit_required=true")
        elif audit is False:
            errors.append(f"{loc}: non-SOURCE_VERIFIED claim cannot set audit_required=false")
        if status=="MODEL_DERIVED_AUDIT_REQUIRED" and not any(x.get("source_kind")=="MODEL_KNOWLEDGE" for x in sources):
            warnings.append(f"{loc}: model-derived status has no MODEL_KNOWLEDGE source record")
        if status=="CONFLICTED" and not c.get("limitations"):
            warnings.append(f"{loc}: CONFLICTED claim should describe conflict in limitations")

missing=sorted(p.name for p in topic_dirs if not (p/"standards-claims.json").exists())
print(json.dumps({
    "topic_directories":len(topic_dirs),
    "registers":len(registers),
    "topics_missing_register":len(missing),
    "claims":len(seen),
    "errors":len(errors),
    "warnings":len(warnings),
    "missing_registers":missing,
    "error_details":errors,
    "warning_details":warnings
},indent=2))
sys.exit(1 if errors else 0)
