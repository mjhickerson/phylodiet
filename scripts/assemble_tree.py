#!/usr/bin/env python3
"""Assemble the Phylodiet tree from a dated Newick and the candidate species CSV.

    python3 assemble_tree.py dated.nwk edible_eukaryotes_candidates.csv outdir/ [extra_aliases.csv ...]
    (with no alias file given, every data/aliases*.csv next to the candidates list is used: aliases.csv holds the
     hand-curated English food words such as egg, bacon, bread, flour; aliases_es.csv the Spanish ones; without them
     the app only knows common and Latin names)

Inputs
  dated.nwk   ultrametric tree with branch lengths in Myr; tip labels are species
              names (TimeTree style "Genus_species", asterisks and quotes tolerated)
  candidates  CSV with columns species, common_name, genus, family, clade, group

Outputs (in outdir)
  food_tree.newick   tips relabelled to Phylodiet ids, gap-filled taxa added
  taxa.csv           id, common_name, species, lineage, clade, aliases (Phylodiet format)
  assembly_report.txt  what was matched, substituted, gap-filled, and left out

Gap-fill rule for a species absent from the tree:
  1. two or more congeners present  -> add as a child of the genus MRCA (polytomy)
  2. exactly one congener            -> add as sister to it, splitting at half its terminal branch (max 5 Myr)
  3. otherwise, two or more family members present -> child of the family MRCA
  4. exactly one family member       -> sister to it at half its terminal branch (max 20 Myr)
  5. otherwise                        -> not placed; listed in the report

Pure Python, no dependencies. Polytomies are fine throughout.
"""
import csv, re, sys, os, unicodedata
from collections import defaultdict
if os.getcwd() not in sys.path: sys.path.insert(1, os.getcwd())   # curation.py from the working directory
try:
    import curation
    if not hasattr(curation, "SYNONYMS"):   # a 'curation/' folder (as in the repository) shadows the module: load the file inside it
        import importlib.util
        for _c in (os.path.join(os.getcwd(), "curation", "curation.py"), os.path.join(os.getcwd(), "curation.py")):
            if os.path.exists(_c):
                _spec = importlib.util.spec_from_file_location("curation_tables", _c); curation = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(curation); break
        else: raise ImportError
    SYNONYMS, PLACEMENTS, CLADE_NAMES = curation.SYNONYMS, curation.PLACEMENTS, curation.CLADE_NAMES
    PLACEMENTS_OPEN = getattr(curation, "PLACEMENTS_OPEN", {})
    ALIAS_ADD, ALIAS_REMOVE = getattr(curation, "ALIAS_ADD", {}), getattr(curation, "ALIAS_REMOVE", {})
    GENUS_CROWN = getattr(curation, "GENUS_CROWN", {})
    FAMILY_CROWN = getattr(curation, "FAMILY_CROWN", {})
    TREE_VERSION, CHANGELOG = getattr(curation, "TREE_VERSION", "unversioned"), getattr(curation, "CHANGELOG", [])
except ImportError:
    SYNONYMS, PLACEMENTS, CLADE_NAMES, TREE_VERSION, CHANGELOG, PLACEMENTS_OPEN, ALIAS_ADD, ALIAS_REMOVE, GENUS_CROWN, FAMILY_CROWN = {}, {}, {}, "unversioned", [], {}, {}, {}, {}, {}

# ---------------- Newick ----------------
class Node:
    __slots__ = ("label", "bl", "children", "parent", "height")
    def __init__(self, label="", bl=0.0):
        self.label, self.bl, self.children, self.parent, self.height = label, bl, [], None, 0.0
    def is_tip(self): return not self.children
    def add(self, c): c.parent = self; self.children.append(c); return c
    def tips(self):
        out = []
        stack = [self]
        while stack:
            n = stack.pop()
            if n.is_tip(): out.append(n)
            else: stack.extend(n.children)
        return out

def parse_newick(s):
    s = s.strip()
    if s.endswith(";"): s = s[:-1]
    i = 0
    def read_label():
        nonlocal i
        if i < len(s) and s[i] == "'":
            j = s.index("'", i + 1)
            while j + 1 < len(s) and s[j + 1] == "'":
                j = s.index("'", j + 2)
            lab = s[i + 1:j].replace("''", "'"); i = j + 1; return lab
        j = i
        while j < len(s) and s[j] not in ":,()[]": j += 1
        lab = s[i:j]; i = j; return lab
    def skip_comment():
        nonlocal i
        if i < len(s) and s[i] == "[":
            i = s.index("]", i) + 1
    def node():
        nonlocal i
        n = Node()
        if s[i] == "(":
            i += 1
            n.add(node())
            while s[i] == ",":
                i += 1; n.add(node())
            assert s[i] == ")", f"expected ) at {i}"
            i += 1
        n.label = read_label().strip()
        skip_comment()
        if i < len(s) and s[i] == ":":
            i += 1
            j = i
            while j < len(s) and s[j] not in ",()[];": j += 1
            n.bl = float(s[i:j] or 0); i = j
            skip_comment()
        return n
    root = node()
    return root

def write_newick(n):
    def rec(x):
        inner = "(" + ",".join(rec(c) for c in x.children) + ")" if x.children else ""
        lab = x.label
        if lab and re.search(r"[\s,:;()\[\]']", lab):
            lab = "'" + lab.replace("'", "''") + "'"
        bl = f":{x.bl:.6g}" if x.parent is not None else ""
        return f"{inner}{lab}{bl}"
    return rec(n) + ";"

def set_heights(root):
    """height = max distance to a descendant tip (== age for an ultrametric tree)."""
    def rec(n):
        if n.is_tip(): n.height = 0.0; return 0.0
        n.height = max(rec(c) + c.bl for c in n.children); return n.height
    rec(root)

def mrca(nodes):
    paths = []
    for n in nodes:
        p = []
        while n is not None: p.append(n); n = n.parent
        paths.append(set(p))
    common = set.intersection(*paths)
    # deepest common = the one with smallest height
    return min(common, key=lambda x: x.height)

# ---------------- names ----------------
def clean_label(lab):
    lab = lab.strip().strip("'\"").replace("_", " ")
    lab = lab.replace("*", "").strip()
    lab = re.sub(r"\s+", " ", lab)
    return lab

def norm_species(name):
    name = clean_label(name)
    name = name.replace("×", "").replace(" x ", " ").replace(" kl. ", " ")
    name = re.sub(r"\s+", " ", name).strip().lower()
    return name

def genus_of(species):
    parts = norm_species(species).split()
    return parts[0] if parts else ""

def slugify(text, taken):
    base = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().replace("'", "")
    parts = [p.strip() for p in re.sub(r"\(.*?\)", "", base).split("/") if p.strip()]
    base = parts[0].lower()
    if len(parts) > 1 and len(base.split()) == 1:
        last = parts[-1].lower().split()
        if len(last) >= 2 and last[-1] not in base: base += " " + last[-1]
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-") or "taxon"
    slug, k = base, 2
    while slug in taken:
        slug = f"{base}-{k}"; k += 1
    taken.add(slug)
    return slug

PART_WORDS = set('''seed seeds petals petal greens leaves leaf root roots tuber tubers flowers flower fruit fruits
shoots shoot sap oil oils processed historical historically egg eggs nut nuts honey caviar roe tea tips bark pods pod
buds bud cooked stems stem pith bulb bulbs corm corms larva larvae pupa pupae brood alate fry fermented foaming agent
fat butter colourant rennet jelly starch gum needles receptacle fleshy inner grain nectar young pulp heart hearts
in the of and a an or white red black green yellow blue brown purple pink orange golden silver giant small large common
wild domestic dwarf greater lesser european american asian african chinese japanese indian pacific atlantic mediterranean
northern southern eastern western sweet sour bitter edible true false farmed cultivated historical marxianus
berries berry acorn acorns hips rhizome rhizomes manna flavouring flavoring samaras seedling
gulf africa west east north south central europe asia america americas chile peru mexico brazil argentina india china japan
korea thailand nz australia tasmania hawaii sahel cape sonoran nsw florida yunnan mauritius indochina caribbean andes
patagonia amazon texas california alaska'''.split())
def _is_part(piece):
    words = [w for w in re.split(r"[^a-z]+", piece.lower()) if w]
    return bool(words) and all(w in PART_WORDS for w in words)
def final_aliases(r, extra_aliases):
    """all alias sources merged, then curation.ALIAS_ADD / ALIAS_REMOVE applied (matched case-insensitively)"""
    merged = [a for a in (aliases_for(r["common_name"], r["species"]) + ";" + extra_aliases.get(norm_species(r["species"]), "")).split(";") if a]
    merged += ALIAS_ADD.get(r["species"], [])
    drop = {x.lower() for x in ALIAS_REMOVE.get(r["species"], [])}
    return ";".join(dict.fromkeys(a for a in merged if a.lower() not in drop))

def aliases_for(common, species):
    parts = [p.strip() for p in common.split("/")]
    extra = re.findall(r"\((.*?)\)", common)
    out = []
    p0 = re.sub(r"\(.*?\)", "", parts[0]).strip().lower()
    for p in parts:
        p2 = re.sub(r"\(.*?\)", "", p).strip()
        if p2 and p2.lower() != p0 and not _is_part(p2): out.append(p2)
    latin = {w.lower() for w in re.split(r"[\s×]+", species) if w}
    for e in extra:
        for piece in e.split(","):
            piece = piece.strip()
            if piece and len(piece) > 2 and not _is_part(piece) and piece.lower() not in latin: out.append(piece)   # "(acuminata)" is not an alias
    return ";".join(dict.fromkeys(out))

# ---------------- main ----------------
EXTRA_ALIAS_FILES = []
def main(nwk_path, csv_path, outdir):
    os.makedirs(outdir, exist_ok=True)
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
    report = defaultdict(list)
    root = parse_newick(open(nwk_path, encoding="utf-8").read())
    set_heights(root)
    syn = {norm_species(k): v for k, v in SYNONYMS.items()}
    for n in _all_nodes(root):
        if n.is_tip():
            key = norm_species(n.label)
            if key in syn:
                report["synonym applied (tree label -> candidate)"].append(f"{clean_label(n.label)} -> {syn[key]}")
                n.label = syn[key]
        elif re.fullmatch(r"'?\d+'?", n.label or ""):
            n.label = ""

    # index tree tips by normalised species and by genus
    tip_by_species = {}
    for t in root.tips():
        key = norm_species(t.label)
        tip_by_species.setdefault(key, t)
    # 1. match candidates to tips
    matched = {}   # species row -> tip node
    unmatched = []
    for r in rows:
        key = norm_species(r["species"])
        t = tip_by_species.get(key)
        if t is None:
            # TimeTree may return "Genus_sp." or a substituted congener; try genus-level unique match later
            unmatched.append(r)
        else:
            matched[r["species"]] = t
            report["matched"].append(r["species"])

    # tips the tree returned under a different name (TimeTree substitutes): claim by genus when unambiguous
    claimed = set(id(t) for t in matched.values())
    unmatched_by_genus = defaultdict(list)
    for r in unmatched: unmatched_by_genus[genus_of(r["species"])].append(r)
    matched_genera = {genus_of(sp) for sp in matched}
    still_unmatched = []
    helper_tips = defaultdict(list)   # non-food congeners kept by graft_tree as anchors for genus placement
    for t in root.tips():
        if id(t) in claimed or t.label.startswith("__placeholder__"): continue
        if t.label.startswith("__helper__"):
            helper_tips[genus_of(t.label[len("__helper__"):])].append(t); continue
        g = genus_of(t.label)
        cands = unmatched_by_genus.get(g, [])
        if len(cands) == 1 and g not in matched_genera:
            r = cands[0]
            report["assumed substitute (tree label -> candidate)"].append(f'{clean_label(t.label)} -> {r["species"]}')
            t.label = r["species"]; matched[r["species"]] = t; claimed.add(id(t)); unmatched_by_genus[g] = []
        else:
            report["tree tips not in candidate list (dropped)"].append(clean_label(t.label))
    unmatched = [r for r in unmatched if r["species"] not in matched]

    # 2. gap-fill the unmatched
    def members(pred):
        return [t for sp, t in matched.items() if pred(sp)]
    genus_index = defaultdict(list); family_index = defaultdict(list)
    fam_of = {r["species"]: r["family"] for r in rows}
    clade_of = {r["species"]: r.get("clade", "") for r in rows}
    def congeners(g, r):   # same genus AND same clade; helper tips (no row) are trusted
        return [t for t in genus_index.get(g, []) if t.label.startswith("__helper__") or clade_of.get(t.label, r.get("clade", "")) == r.get("clade", "")]
    for sp, t in matched.items():
        genus_index[genus_of(sp)].append(t); family_index[fam_of[sp]].append(t)
    for g, ts in helper_tips.items():
        if not genus_index.get(g): genus_index[g].extend(ts)

    def attach_on_stem(node, r, age):
        """insert the new tip on the branch above `node` at `age` (or at node's parent if age is older)."""
        while node.parent is not None and age >= node.parent.height: node = node.parent   # climb until the branch above `node` spans `age`
        par = node.parent
        if par is None:
            n = Node(r["species"], node.height); node.add(n); return f"child of node at {node.height:.0f} Myr"
        if age <= node.height:
            n = Node(r["species"], node.height); node.add(n); return f"child of MRCA at {node.height:.0f} Myr"
        par.children.remove(node)
        inner = Node("", par.height - age); inner.height = age; par.add(inner)
        node.bl = age - node.height; inner.add(node)
        n = Node(r["species"], age); inner.add(n)
        return f"sister to anchor clade at {age:.0f} Myr"
    def attach_family(fm, r, f):
        """family rule: polytomy at the family MRCA, or sister to a lone member (max 20 Myr); FAMILY_CROWN lifts the join to a known crown age"""
        node = mrca(fm) if len(fm) >= 2 else fm[0]
        fc = FAMILY_CROWN.get(f)
        if fc and fc > node.height: return attach_on_stem(node, r, fc)
        return attach_polytomy(node, r) if len(fm) >= 2 else attach_sister(node, r, 20.0)
    def attach_polytomy(parent, r):
        n = Node(r["species"], parent.height)
        parent.add(n); return "child of MRCA"
    def attach_sister(sib, r, cap):
        split = min(cap, sib.bl / 2.0)
        if split <= 0: split = min(cap, 1.0)
        old_parent = sib.parent
        old_parent.children.remove(sib)
        inner = Node("", sib.bl - split); inner.height = split
        old_parent.add(inner)
        sib.bl = split; inner.add(sib)
        n = Node(r["species"], split); inner.add(n)
        return f"sister to {clean_label(sib.label)} at {split:.2f} Myr"

    placed_rows = []; leftovers = []
    source_tips = set(id(t) for t in matched.values())   # species dated by a source tree, before any gap-filling
    for r in unmatched:
        g, f = genus_of(r["species"]), r["family"]
        gm, fm = congeners(g, r), family_index.get(f, [])
        how = None
        if len(gm) >= 2:
            how = attach_polytomy(mrca(gm), r); level = "genus"
        elif len(gm) == 1:
            how = attach_sister(gm[0], r, 5.0); level = "genus"
        elif fm:
            how = attach_family(fm, r, f); level = "family"
        if how:
            report[f"gap-filled at {level}"].append(f'{r["species"]}: {how}')
            placed_rows.append(r)
            new_tip = next(t for t in root.tips() if t.label == r["species"])
            matched[r["species"]] = new_tip
            genus_index[g].append(new_tip); family_index[f].append(new_tip)
            set_heights(root)
        else:
            leftovers.append(r)

    # 2b. order-level anchors for families with no member in the tree; deepest ages first so nesting works
    node_by_label = {}
    for n in _all_nodes(root):
        if not n.is_tip() and n.label: node_by_label.setdefault(n.label, n)
    def anchor_node(fams):
        """anchors are family names (MRCA of their tips) or '@Node label' (a named backbone node); the first
        resolvable option wins, so a list can hold a family for one build and a backbone node for another."""
        missing = []
        for fa in fams:
            if fa.startswith("@"):
                n = node_by_label.get(fa[1:])
                if n is not None: return n, missing
                missing.append(fa)
            elif family_index.get(fa):
                pass
            else:
                missing.append(fa)
        tips_ = [t for fa in fams if not fa.startswith("@") for t in family_index.get(fa, [])]
        return (mrca(tips_) if len(tips_) >= 2 else (tips_[0] if tips_ else None)), missing
    def placement_for(f):
        """the open-tree table wins when its anchor resolves in this tree; otherwise the general table"""
        for table in (PLACEMENTS_OPEN, PLACEMENTS):
            if f in table:
                node, missing = anchor_node(table[f][0])
                if node is not None: return table[f]
        return None
    order_key = lambda r: -((placement_for(r["family"]) or ([], None))[1] or 0)
    for r in sorted(leftovers, key=order_key):
        f = r["family"]
        # a congener or family member may have been placed by an earlier anchor: reuse the genus/family rule
        gm, fm = congeners(genus_of(r["species"]), r), family_index.get(f, [])
        skel = placement_for(f) if f in PLACEMENTS_OPEN and PLACEMENTS_OPEN[f][0][0].startswith("@") else None
        if gm:
            node = mrca(gm) if len(gm) >= 2 else gm[0]
            gc = GENUS_CROWN.get(genus_of(r["species"]).capitalize())
            if len(gm) >= 2 and gc: how = attach_on_stem(node, r, gc) if gc > node.height else attach_polytomy(node, r)
            elif len(gm) >= 2: how = attach_polytomy(node, r)
            else: how = attach_sister(node, r, gc if gc else 5.0)
            level = "genus"
        elif skel is not None and not any(id(t) in source_tips for t in fm):   # family on a skeleton node, no source-dated relative
            fams, age = skel
            node, missing = anchor_node(fams)
            how = attach_on_stem(node, r, age) if age else attach_polytomy(node, r)
            level = "order (anchor)"
        elif fm:
            how = attach_family(fm, r, f)
            level = "family"
        elif placement_for(f) is not None:
            fams, age = placement_for(f)
            node, missing = anchor_node(fams)
            if node is None:
                report["not placed"].append(f'{r["species"]} ({f}): anchors absent {fams}'); continue
            if missing: report["anchor families missing (placement still made)"].append(f'{f}: {missing}')
            how = attach_on_stem(node, r, age) if age else attach_polytomy(node, r)
            level = "order (anchor)"
        else:
            report["not placed"].append(f'{r["species"]} ({f})'); continue
        report[f"gap-filled at {level}"].append(f'{r["species"]}: {how}')
        new_tip = next(t for t in root.tips() if t.label == r["species"])
        matched[r["species"]] = new_tip
        genus_index[genus_of(r["species"])].append(new_tip); family_index[f].append(new_tip)
        set_heights(root)

    # rebuild tip index after edits, then prune tree to candidate tips only (placeholder tips fall out here)
    set_heights(root)
    keep = {norm_species(r["species"]) for r in rows}
    def prune(n):
        if n.is_tip():
            return n if norm_species(n.label) in keep else None
        n.children = [c for c in (prune(c) for c in n.children) if c is not None]
        for c in n.children: c.parent = n
        if not n.children: return None
        if len(n.children) == 1 and n.parent is not None:
            c = n.children[0]; c.bl += n.bl; c.parent = n.parent; return c
        return n
    root = prune(root)
    while root and len(root.children) == 1:
        root = root.children[0]; root.parent = None; root.bl = 0.0
    set_heights(root)

    # 3. name internal nodes: genus and family MRCAs when monophyletic, then higher clades from CLADE_NAMES
    by_species = {norm_species(r["species"]): r for r in rows}
    tip_rows = {t: by_species[norm_species(t.label)] for t in root.tips()}
    # supplemental aliases (e.g. the hand-written prototype table), merged by species
    extra_aliases = {}
    for path in EXTRA_ALIAS_FILES:
        for r in csv.DictReader(open(path, encoding="utf-8")):
            key = norm_species(r.get("species", "")); al = r.get("aliases", "")
            # the other table's plain common name(s) become aliases too ("basil" for a species now called "sweet basil")
            names = [re.sub(r"\(.*?\)", "", p).strip() for p in r.get("common_name", "").split("/")]
            al = ";".join([a for a in names if a] + ([al] if al else []))
            if key and al: extra_aliases[key] = ";".join([extra_aliases[key], al]) if key in extra_aliases else al
    def name_mrca(groups, label_of, need_monophyly=True):
        for key, tips_ in groups.items():
            if len(tips_) < 2: continue
            m = mrca(tips_)
            if need_monophyly and any(tip_rows[t] not in [tip_rows[x] for x in tips_] for t in m.tips()): continue
            if not m.label: m.label = label_of(key)
    gen = defaultdict(list); fam = defaultdict(list)
    for t, r in tip_rows.items(): gen[genus_of(r["species"])].append(t); fam[r["family"]].append(t)
    name_mrca(gen, lambda g: g.capitalize())
    name_mrca(fam, lambda f: f)
    for name, fams in CLADE_NAMES.items():
        tips_ = [t for t in root.tips() if tip_rows[t]["family"] in fams]
        if len(tips_) >= 2:
            m = mrca(tips_); m.label = name   # clade names override family/genus labels on the same node
    for n in _all_nodes(root):
        if not n.is_tip() and n.label and re.fullmatch(r"'?\d+'?", n.label): n.label = ""
    # relabel tips to ids and write outputs
    taken = set(); out_rows = []
    for t in root.tips():
        r = by_species[norm_species(t.label)]
        slug = slugify(r["common_name"], taken)
        t.label = slug
        out_rows.append({
            "id": slug, "common_name": r["common_name"], "species": r["species"],
            "lineage": r["family"], "clade": r["clade"] if r["clade"] in {"animal","fungus","plant","green","red","brown","other"} else "plant",
            "aliases": final_aliases(r, extra_aliases),
        })
    # name internal nodes that TimeTree labelled (keep), leave others blank
    with open(os.path.join(outdir, "food_tree.newick"), "w", encoding="utf-8") as f:
        f.write(write_newick(root) + "\n")
    with open(os.path.join(outdir, "tree_version.txt"), "w", encoding="utf-8") as f: f.write(TREE_VERSION + "\n")
    with open(os.path.join(outdir, "taxa.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id","common_name","species","lineage","clade","aliases"], lineterminator="\n")
        w.writeheader(); w.writerows(out_rows)
    total = sum(n.bl for n in _all_nodes(root) if n.parent is not None)
    with open(os.path.join(outdir, "assembly_report.txt"), "w", encoding="utf-8") as f:
        f.write(f"tree version: {TREE_VERSION}\ntips in output: {len(out_rows)}   root age: {root.height:.0f} Myr   total branch length: {total:.0f} Myr\n\n")
        f.write("== changelog\n")
        for d, who, what, src in CHANGELOG: f.write(f"   {d}  {who}: {what}  [{src}]\n")
        f.write("\n")
        for k in ["matched", "synonym applied (tree label -> candidate)", "assumed substitute (tree label -> candidate)", "gap-filled at genus", "gap-filled at family", "gap-filled at order (anchor)", "anchor families missing (placement still made)", "not placed", "tree tips not in candidate list (dropped)"]:
            v = report.get(k, [])
            f.write(f"== {k}: {len(v)}\n")
            if k != "matched":
                for line in v: f.write("   " + line + "\n")
            f.write("\n")
    print(f"tips: {len(out_rows)}  root: {root.height:.0f} Myr  total: {total:.0f} Myr  "
          f"matched {len(report['matched'])}, genus-filled {len(report['gap-filled at genus'])}, "
          f"family-filled {len(report['gap-filled at family'])}, anchor-filled {len(report['gap-filled at order (anchor)'])}, not placed {len(report['not placed'])}")

def _all_nodes(root):
    stack = [root]
    while stack:
        n = stack.pop(); yield n; stack.extend(n.children)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__); sys.exit(1)
    EXTRA_ALIAS_FILES = sys.argv[4:]
    import glob
    _default_aliases = sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(sys.argv[2])), "aliases*.csv")))   # data/aliases*.csv beside the candidates list
    if not EXTRA_ALIAS_FILES and _default_aliases: EXTRA_ALIAS_FILES = _default_aliases
    print("alias files:", EXTRA_ALIAS_FILES or "none (common names only)", file=sys.stderr)
    main(*sys.argv[1:4])
