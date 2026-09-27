"""Regenerate curation/node_review_open.csv: one row per backbone node in backbone.py, with its age, whether it is
cited or still approximate, the families PLACEMENTS_OPEN anchors on it, and how many listed species those families hold.
Reviewers fill the last two columns.

    python3 scripts/node_review.py scripts/backbone.py curation/curation.py data/edible_eukaryotes_candidates.csv curation/node_review_open.csv
"""
import csv, re, sys, collections, importlib.util
bb, cur, cands, out = sys.argv[1:5]
src = open(bb, encoding="utf-8").read()
spec = importlib.util.spec_from_file_location("curation_tables", cur); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
fam_n = collections.Counter(r["family"] for r in csv.DictReader(open(cands, encoding="utf-8")))
anch = collections.defaultdict(list)
for fam, (targets, age) in getattr(C, "PLACEMENTS_OPEN", {}).items():
    for t in targets:
        if t.startswith("@"): anch[t[1:]].append(fam); break
rows = []
for m in re.finditer(r'N\("([^"]+)",\s*([\d.]+),\s*(.+?)(?:,\s*\n|\),?\s*\n|,\s*N\()', src):
    name, age, expr = m.group(1), m.group(2), m.group(3).strip()
    approx = "APPROX" in expr
    fams = anch.get(name, [])
    rows.append([name, age, "mine, approximate" if approx else "cited: see backbone.py", expr[:160], ", ".join(fams), sum(fam_n[f] for f in fams), "", ""])
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["node", "age_Ma", "basis", "source_expr", "families_anchored_here", "n_species", "reviewer_suggested_age", "reviewer_notes"]); w.writerows(rows)
print(len(rows), "nodes,", sum(1 for r in rows if r[2].startswith("mine")), "approximate")
