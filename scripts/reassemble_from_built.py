"""Turn the built food_tree.newick (tips = Phylodiet ids) back into a species-labelled tree that assemble_tree.py accepts,
so new candidate species can be gap-filled into the built tree when the source chronograms are not at hand.

    python3 scripts/reassemble_from_built.py . species_tree.nwk
    python3 scripts/assemble_tree.py species_tree.nwk data/edible_eukaryotes_candidates.csv outdir

Every species already in the tree is matched as is (ages and topology unchanged); candidates that are new are placed
by the gap-fill rules. Keep the earlier tree/assembly_report.txt: the one written to outdir counts every old tip as matched."""
import csv, sys, os
sys.setrecursionlimit(1_000_000)
repo, out = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(repo, "scripts")); os.chdir(repo)
from assemble_tree import parse_newick, write_newick
ids = {r["id"]: r["species"] for r in csv.DictReader(open("tree/taxa.csv", encoding="utf-8"))}
root = parse_newick(open("tree/food_tree.newick", encoding="utf-8").read())
n = 0
for t in root.tips():
    t.label = ids[t.label].replace(" ", "_"); n += 1
open(out, "w", encoding="utf-8").write(write_newick(root) + "\n"); print("tips relabelled", n)
