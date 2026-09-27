# Curation tables for assemble_tree.py. Edit freely; the script imports this file if present.

# Bump TREE_VERSION whenever anything below (or the species list, or the TimeTree export) changes,
# and add a CHANGELOG line: (date, who, what changed, source). Both are written into the report and shown in the app.
TREE_VERSION = "open-0.17 (2026-09-27)"
CHANGELOG = [
    ("2026-09-19", "MH", "First TimeTree 5 build: 2,607 dated species; 49 synonyms; 63 families anchored by hand", "TimeTree 5 export of the 3,279-name list"),
    ("2026-09-19", "MH", "Red algae anchors revised: Gigartinales families to the Gigartinales crown; Gelidiales, Bonnemaisoniales, Ceramiales, Nemaliales to subclass stems", "Yang et al. 2016 Sci Rep 6:21361"),
    ("2026-09-19", "MH", "Suillaceae to 130 Ma; Naematelia to 100 Ma; jellyfish to 650 Ma; Mucoromycota kept at 900 Ma", "Varga et al. 2019 Nat Ecol Evol 3:668; Park et al. 2012 Mol Phylogenet Evol; fungal timetree Nat Ecol Evol 2025"),
    ("2026-09-20", "MH", "Open tree v0.1: Strassert 2021 backbone; Smith & Brown 2018, Nitta 2022, Rabosky 2018, Upham 2019, Varga 2019 grafted", "see backbone.py"),
    ("2026-09-20", "Bruce Taylor", "Eukaryote rooting confirmed as Opimoda/Diphoda (= Strassert Amorphea-rooted analysis); Euglena stays with Diaphoretickes", "Williamson et al. 2025 Nature; Derelle et al. 2015 PNAS"),
    ("2026-09-20", "MH", "Open tree v0.2: Jetz 2012 birds grafted; class/order skeleton (~60 nodes, mostly approximate) for molluscs, arthropods, algae, ascomycetes, small phyla, herps, sharks; every listed species placed", "backbone.py; PLACEMENTS_OPEN in curation.py"),
    ("2026-09-20", "MH", "Open tree v0.3: VertLife subsets grafted for sharks (Stein 2018), amphibians (Jetz & Pyron 2018), squamates (Tonini 2016); their skeleton nodes retired", "backbone.py"),
    ("2026-09-20", "MH", "Open tree v0.4: decapod skeleton nodes set from Wolfe et al. 2019 chronograms (UGAM model throughout; CIR values recorded); Palinuridae and crayfish nodes added; Malacostraca/Eucarida raised to fit", "Wolfe et al. 2019 Proc R Soc B, Dryad doi:10.5061/dryad.k7505mn"),
    ("2026-09-20", "MH", "Open tree v0.5: bivalve skeleton dated from Li et al. 2025 (Bivalvia 485, Pteriomorphia 446, Ostreida/Mytilida 421, core Imparidentia 362, Myida+Venerida 301, Adapedonta+Cardiida 300); gastropod topology cited to Uribe et al. 2022, ages still approximate", "Li et al. 2025 Syst Biol 74:16; Uribe et al. 2022 Syst Biol"),
    ("2026-09-20", "John Wares", "Keyword matcher: 'tuna' matched prickly pear (Spanish name) and 'cheese' matched Mucor; ALIAS_ADD/ALIAS_REMOVE tables added; 'tuna' now maps to yellowfin tuna", "user report"),
    ("2026-09-24", "Rachel Swenie", "Varga et al. 2019 kept as the mushroom source: she finds it runs young for deep nodes (her Cantharellales estimate 314 vs Varga 372, cf. Sanchez-Garcia et al. 2020 PNAS), Tim James finds it runs old; the two bracket it", "R. Swenie pers. comm."),
    ("2026-09-24", "Rachel Swenie", "Cantharellales divergence estimated at 314 Ma in her own work (Varga 372, Tim James 225-263); Varga may run young for deep nodes, so with Tim's view that it runs old the chronogram is bracketed and kept as is; Sanchez-Garcia et al. 2020 PNAS noted as fossil-calibrated cross-check", "R. Swenie pers. comm.; Sanchez-Garcia et al. 2020 PNAS"),
    ("2026-09-24", "Tim James", "Varga et al. 2019 judged to run old but with wide variation; keep as is. Natto raised: bacteria are deliberately outside the tree; page and README now say so", "T. James pers. comm."),
    ("2026-09-26", "MH", "Open tree v0.16: 17 animals had been grafted inside the plants because a genus name is shared across kingdoms (Magallana oyster / Magallana plant, Donax clam / Donax herb, Paphia, Callista, Calamus porgy / rattan, Ruspolia, Oryctes): the graft step took a non-food congener from the plant tree and the oysters, venus clams, wedge clams, a porgy, a bush cricket and two scarab grubs followed it. Congener lookup is now clade-aware in graft_tree.py and assemble_tree.py; the 17 re-placed in their own families or order nodes. Meals with Pacific or flat oysters, butter or littleneck clams were over-scored before this", "found when the meal tree root read 'Bivalves'"),
    ("2026-09-26", "MH", "Open tree v0.16.1: full regraft from the source chronograms with the clade-aware graft step (v0.16 had been patched from the built tree). Identical except the oysters: Magallana, Ostrea and Saccostrea now join Crassostrea as a polytomy at the Ostreida node (421) rather than as 20 Myr sisters, pending an Ostreidae crown age", "regraft; seam_report.txt regenerated"),
    ("2026-09-27", "Rhema Uche-Dike, Kate Montana, Julia Amoroso (Ware lab, AMNH)", "Open tree v0.17: insect skeleton dated from their review sheet. Neoptera 383 and Eumetabola 373 (Wang et al. 2016 Sci Rep); Ensifera 268 and Acrididae+Pyrgomorphidae 140 (Song et al. 2015); Cicadidae 199 and Nepomorpha 243 (Wang et al. 2017/2019 Cladistics); Pentatomoidea 100.5 (Wang et al. 2016 Cladistics); Vespidae 110 (Blaimer et al. 2023); Coleoptera 300 now cited, Cucujiformia 200, Tenebrionidae 122, Scarabaeidae 120 (Zhang et al. 2018), Polyphaga 260 approx; Cossidae 120, Bombycoidea 88, Saturniidae 70 (Wahlberg et al. 2013); Insecta 441 upgraded to Misof 2014. Not adopted: Insecta 301 (Cen et al. 2025) and Collembola-Archaeognatha 344, which sit below Pterygota 406; Pterygota 385 (Thomas et al. 2013) kept at Misof's 406 for consistency; Apidae-Formicidae split 110, which is younger than the ant crown; single-species family crowns (Dytiscidae 170, Curculionidae 120, Stratiomyidae 129, Chaoboridae 118, Hesperiidae 85, Termitidae 54) recorded in backbone.py notes", "insect_review_Rhema_Kate.csv, 2026-09-25"),
    ("2026-09-27", "Jessica Ware", "Forthcoming 1KITE Nature ms moves the deep insect nodes older: Hexapoda ~523, Insecta ~523, Pterygota ~470s, Neoptera ~475, Polyneoptera 425+, Hymenoptera ~298. Recorded beside each node in backbone.py; to be adopted when the paper is out (Hexapoda 523 would also need the Pancrustacea node above it revisited)", "J. Ware, email 2026-09-27"),
    ("2026-09-23", "Christine Maggs", "Gracilariaceae node added at ~300 Ma and Gracilaria crown set to ~230 Ma from the Kim et al. 2026 preprint (Ahnfeltia genomes) she pointed to; GENUS_CROWN table introduced so old genera are not collapsed to 5 Myr", "Kim et al. 2026 preprint, researchgate 405471651"),
    ("2026-09-23", "MH", "Open tree v0.14: red algal crowns from Yang et al. 2016 text (Nemaliophycidae 331, Rhodymeniophycidae 412); finer order splits remain approximate, unresolved in that study", "Yang et al. 2016 Sci Rep"),
    ("2026-09-22", "Tim James", "Mucoromycota split confirmed at ~700 Ma; Discinaceae moved to sister of Morchellaceae; Pyronemataceae and Sarcoscyphaceae on the stem above truffles+morels at ~250. His ballparks for splits now taken from source trees, recorded for the record: Cantharellales 225-263 (Varga 372), morels vs truffles 200 (Shen 173), Suillus vs Boletus 150 (Varga 115), Naematelia vs Tremella 125 (Varga 53)", "T. James pers. comm."),
    ("2026-09-21", "TimeTree team / MH", "TimeTree granted use of the pruned tree in the app (email, 2026-09-21). Skeleton audited against TimeTree 5: 25 of 30 comparable nodes within ~25%; five adopted from TimeTree with attribution (Cirripedia 193, Neogastropoda 239, Echinoidea 113, Ulvales 609, Trebouxiophyceae 827)", "Kumar et al. 2022 Mol Biol Evol"),
    ("2026-09-21", "MH", "Open tree v0.11: cephalopod nodes from Tanner et al. 2017 Suppl. Table 2 (Coleoidea 289, Octobrachia 239, Incirrata 98, Decabrachia 173, Myopsida 100, Oegopsida 104); gastropod subclass nodes from Tanner Fig. S4 CI midpoints (Vetigastropoda 370, Apogastropoda 394, Caenogastropoda 225)", "Tanner et al. 2017 Proc R Soc B"),
    ("2026-09-21", "MH", "Open tree v0.10: deepest two gastropod nodes cited to a 2022 mitogenomic timetree (532, 493); cephalopod nodes annotated with Tanner et al. 2017 qualitative ages pending the table", "Frontiers Ecol Evol 2022 10.3389/fevo.2022.973485; Tanner et al. 2017 Proc R Soc B"),
    ("2026-09-21", "MH", "Open tree v0.9: Shen et al. 2020 1,107-genome Ascomycota timetree grafted (20 species direct, 11 by congener); ascomycete skeleton retired", "Shen et al. 2020 Sci Adv; Figshare doi:10.6084/m9.figshare.12196149"),
    ("2026-09-21", "MH", "Open tree v0.8: ascomycete skeleton dated from Shen et al. 2020 (Ascomycota 563, Saccharomycotina 438, Pezizomycotina 408, Pezizomycetes 248)", "Shen et al. 2020 Sci Adv"),
    ("2026-09-20", "MH", "Open tree v0.7: brown algal skeleton dated from Choi et al. 2024 (Phaeophyceae 371, BACR 167, Fucales 66, Laminariales 83, Ectocarpales 54); red algal skeleton restructured to use Yang et al. 2016's 661 Ma Nemaliophycidae split; green seaweed topology per Del Cortona 2020 / Hou 2022 (Bryopsidales with Chlorophyceae), UTC crown raised to 800 and flagged against Strassert's 583", "Choi et al. 2024 Curr Biol; Yang et al. 2016 Sci Rep; Del Cortona et al. 2020 PNAS; Hou et al. 2022 Nat Commun"),
    ("2026-09-20", "MH", "Open tree v0.6: insect nodes cited: Hexapoda 479, Pterygota 406 (new node), Holometabola 345 (Misof 2014); Hymenoptera 281 (Peters 2017); Lepidoptera 300 (Kawahara 2019); Ditrysia node (210, approx) added so Cossidae no longer sits at the Lepidoptera crown", "Misof et al. 2014 Science; Peters et al. 2017 Curr Biol; Kawahara et al. 2019 PNAS"),
]

# Names as TimeTree returned them -> names in the candidate CSV.
SYNONYMS = {
    "Neopyropia yezoensis": "Pyropia yezoensis",
    "Neoporphyra haitanensis": "Pyropia haitanensis",
    "Urochloa deflexa": "Brachiaria deflexa",
    "Stipa hymenoides": "Eriocoma hymenoides",
    "Inga feuillei": "Inga feuilleei",
    "Chaenomeles sinensis": "Pseudocydonia sinensis",
    "Rhaphiolepis bibas": "Eriobotrya japonica",
    "Cormus domestica": "Sorbus domestica",
    "Juglans ailanthifolia": "Juglans ailantifolia",
    "Morella esculenta": "Myrica esculenta",
    "Morella rubra": "Myrica rubra",
    "Sicyos edulis": "Sechium edule",
    "Benincasa fistulosa": "Praecitrullus fistulosus",
    "Cucumis metulifer": "Cucumis metuliferus",
    "Chamaenerion angustifolium": "Chamerion angustifolium",
    "Zanthoxylum asiaticum": "Toddalia asiatica",
    "Vasconcellea cundinamarcensis": "Vasconcellea pubescens",
    "Corynandra viscosa": "Cleome viscosa",
    "Gynandropsis gynandra": "Cleome gynandra",
    "Lucuma campechiana": "Pouteria campechiana",
    "Wollastonia biflora": "Melanthera biflora",
    "Pseudopodospermum hispanicum": "Scorzonera hispanica",
    "Cicerbita muralis": "Mycelis muralis",
    "Ixeridium dentatum": "Ixeris dentata",
    "Anethum ridolfia": "Ridolfia segetum",
    "Anethum foeniculum": "Foeniculum vulgare",
    "Azorella polaris": "Stilbocarpa polaris",
    "Alkekengi officinarum": "Physalis alkekengi",
    "Mesosphaerum suaveolens": "Hyptis suaveolens",
    "Erythranthe guttata": "Mimulus guttatus",
    "Nopalea cochenillifera": "Opuntia cochenillifera",
    "Ceodes grandis": "Pisonia grandis",
    "Cinnamomum burmanni": "Cinnamomum burmannii",
    "Cinnamomum aromaticum": "Cinnamomum cassia",
    "Rochia nilotica": "Tectus niloticus",
    "Grimothea gregaria": "Munida gregaria",
    "Tragelaphus oryx": "Taurotragus oryx",
    "Phoca groenlandica": "Pagophilus groenlandicus",
    "Pelophylax lessonae": "Pelophylax kl. esculentus",
    "Megaleporinus obtusidens": "Leporinus obtusidens",
    "Myzopsetta ferruginea": "Limanda ferruginea",
    "Pentaceros wheeleri": "Pseudopentaceros wheeleri",
    "Pagrus auratus": "Chrysophrys auratus",
    "Lepista saeva": "Lepista personata",
    "Melothria sphaerocarpa": "Melothria scabra",
    "Galactites tomentosa": "Galactites tomentosus",
    "Planiliza haematocheilus": "Planiliza haematocheila",
    "Helostoma temminkii": "Helostoma temminckii",
    "Pseudotolithus senegallus": "Pseudotolithus senegalensis",
}

# Families with no dated member in TimeTree. Each entry: anchor families already in the tree, and
# an optional age (Myr). Without an age the family attaches as a child of the anchors' MRCA (crown).
# With an age it attaches on the stem above that MRCA at that age (i.e. as its sister clade).
PLACEMENTS = {
    # brown algae
    "Chordariaceae":      (["Laminariaceae", "Fucaceae"], None),
    "Scytosiphonaceae":   (["Laminariaceae", "Fucaceae"], None),
    # red algae
    # Gigartinales families: crown of Gigartinales = MRCA(Gigartinaceae, Cystocloniaceae), 209 Ma in TimeTree
    "Phyllophoraceae":    (["Gigartinaceae", "Cystocloniaceae"], None),
    "Solieriaceae":       (["Gigartinaceae", "Cystocloniaceae"], None),
    "Kallymeniaceae":     (["Gigartinaceae", "Cystocloniaceae"], None),
    "Caulacanthaceae":    (["Gigartinaceae", "Cystocloniaceae"], None),
    "Dumontiaceae":       (["Gigartinaceae", "Cystocloniaceae"], None),
    # early-diverging Rhodymeniophycidae orders (Gelidiales, Bonnemaisoniales): on the stem above the core
    # Rhodymeniophycidae node (349 Ma), below the Ahnfeltiophycidae split (508 Ma, Yang et al. 2016; 427 in TimeTree)
    "Gelidiaceae":        (["Gigartinaceae", "Halymeniaceae"], 400),
    "Pterocladiaceae":    (["Gigartinaceae", "Halymeniaceae"], 400),
    "Bonnemaisoniaceae":  (["Gigartinaceae", "Halymeniaceae"], 400),
    # Ceramiales: crown 335 Ma (284-395) per Yang et al. 2016; its split from the rest a little older
    "Rhodomelaceae":      (["Gigartinaceae", "Halymeniaceae"], 380),
    # Nemaliales sits in Nemaliophycidae with Palmariales; subclass split 661 Ma (Yang 2016), crown age not reported
    "Liagoraceae":        (["Palmariaceae"], 500),
    # green algae
    "Monostromataceae":   (["Ulvaceae", "Caulerpaceae"], None),
    "Prasiolaceae":       (["Ulvaceae", "Chlorellaceae"], None),
    # fungi
    "Rhizopodaceae":      (["Saccharomycetaceae", "Agaricaceae"], 900),   # Mucoromycota, sister to Dikarya
    "Mucoraceae":         (["Saccharomycetaceae", "Agaricaceae"], 900),
    "Morchellaceae":      (["Tuberaceae", "Pyronemataceae"], None),        # Pezizales crown
    "Naemateliaceae":     (["Tremellaceae"], 100),                        # Tremellales; N. aurantialba was Tremella aurantialba
    "Suillaceae":         (["Boletaceae", "Gyroporaceae"], 130),           # Boletales crown 142 (133-153) Ma, Varga et al. 2019
    "Cantharellaceae":    (["Agaricaceae", "Gomphaceae", "Hericiaceae"], None),  # Agaricomycetes crown
    "Hydnaceae":          (["Agaricaceae", "Gomphaceae", "Hericiaceae"], None),
    # invertebrates
    "Rhizostomatidae":    (["Actiniidae"], 650),   # Anthozoa/Medusozoa split; Park et al. 2012 741 (686-819) Ma, capped below TimeTree's Cnidaria/Bilateria node at 716
    "Stomolophidae":      (["Actiniidae"], 650),
    "Echinidae":          (["Parechinidae", "Strongylocentrotidae"], None),
    "Eunicidae":          (["Urechidae", "Sipunculidae"], None),
    "Pharidae":           (["Solenidae", "Hiatellidae"], None),
    "Pinnidae":           (["Ostreidae", "Pectinidae"], None),
    "Pholadidae":         (["Myidae", "Hiatellidae"], None),
    "Teredinidae":        (["Myidae", "Hiatellidae"], None),
    "Achatinidae":        (["Helicidae"], 120),
    "Potamididae":        (["Littorinidae", "Buccinidae"], None),
    "Busyconidae":        (["Buccinidae", "Muricidae"], None),
    "Tegulidae":          (["Turbinidae", "Trochidae"], None),
    "Viviparidae":        (["Ampullariidae", "Littorinidae"], None),
    "Aplysiidae":         (["Helicidae"], 300),
    "Eledonidae":         (["Octopodidae", "Enteroctopodidae"], None),
    "Enoploteuthidae":    (["Loliginidae", "Ommastrephidae"], None),
    "Pandalidae":         (["Palaemonidae", "Crangonidae"], None),
    "Solenoceridae":      (["Penaeidae", "Aristeidae"], None),
    "Sergestidae":        (["Penaeidae", "Aristeidae"], None),
    "Mysidae":            (["Penaeidae", "Euphausiidae"], 420),           # Peracarida vs Eucarida, Malacostraca crown (approx.)
    "Munididae":          (["Lithodidae", "Portunidae"], None),
    "Carcinidae":         (["Portunidae", "Cancridae"], None),
    "Ucididae":           (["Gecarcinidae", "Portunidae"], None),
    "Cheiragonidae":      (["Cancridae", "Portunidae"], None),
    "Chaoboridae":        (["Stratiomyidae"], 230),                       # Culicomorpha vs Brachycera, near the Diptera crown (approx.)
    "Vespidae":           (["Apidae", "Formicidae"], None),
    "Belostomatidae":     (["Cicadidae"], 300),
    "Corixidae":          (["Cicadidae"], 300),
    "Tessaratomidae":     (["Cicadidae"], 300),
    "Pentatomidae":       (["Cicadidae"], 300),
    "Cossidae":           (["Bombycidae", "Saturniidae"], 190),           # basal ditrysian moth (approx.)
    "Hesperiidae":        (["Bombycidae", "Saturniidae"], 130),           # Papilionoidea vs Bombycoidea (approx.)
    "Theraphosidae":      (["Scorpionidae"], 450),
    # fishes
    "Lamnidae":           (["Scyliorhinidae"], 190),
    "Triakidae":          (["Scyliorhinidae"], 150),
    "Carcharhinidae":     (["Scyliorhinidae"], 150),
    "Leiognathidae":      (["Carangidae", "Sparidae"], None),
    "Gobiesocidae":       (["Gobiidae", "Carangidae"], None),
    # plants
    "Pontederiaceae":     (["Commelinaceae"], 100),
    "Humiriaceae":        (["Euphorbiaceae", "Passifloraceae"], None),
    "Caryocaraceae":      (["Euphorbiaceae", "Passifloraceae"], None),
    "Dipterocarpaceae":   (["Malvaceae", "Cistaceae"], None),
    "Icacinaceae":        (["Rubiaceae", "Boraginaceae", "Solanaceae"], None),
    "Pittosporaceae":     (["Apiaceae", "Araliaceae"], None),
}

# Higher-level node names for the tree display, defined by anchor families (MRCA of their tips).
CLADE_NAMES = {
    "Eukaryotes": ["Bovidae", "Poaceae", "Euglenaceae"],
    "Amorphea (animals + fungi)": ["Bovidae", "Agaricaceae"],
    "Diaphoretickes (plants + algae)": ["Poaceae", "Laminariaceae"],
    "Archaeplastida": ["Poaceae", "Bangiaceae"],
    "Viridiplantae": ["Poaceae", "Ulvaceae"],
    "Land plants": ["Poaceae", "Onocleaceae"],
    "Seed plants": ["Poaceae", "Pinaceae"],
    "Angiosperms": ["Poaceae", "Nymphaeaceae"],
    "Monocots": ["Poaceae", "Araceae"],
    "Eudicots": ["Fabaceae", "Papaveraceae"],
    "Rosids": ["Fabaceae", "Brassicaceae"],
    "Asterids": ["Asteraceae", "Ericaceae"],
    "Brown algae": ["Laminariaceae", "Fucaceae"],
    "Red algae": ["Bangiaceae", "Palmariaceae"],
    "Green algae": ["Ulvaceae", "Chlorellaceae"],
    "Fungi": ["Agaricaceae", "Rhizopodaceae"],
    "Dikarya": ["Agaricaceae", "Saccharomycetaceae"],
    "Basidiomycota": ["Agaricaceae", "Ustilaginaceae"],
    "Agaricomycotina": ["Agaricaceae", "Tremellaceae"],
    "Ascomycota": ["Saccharomycetaceae", "Tuberaceae"],
    "Animals": ["Bovidae", "Actiniidae"],
    "Bilateria": ["Bovidae", "Penaeidae"],
    "Vertebrates": ["Bovidae", "Petromyzontidae"],
    "Bony fishes + tetrapods": ["Bovidae", "Salmonidae"],
    "Teleost fishes": ["Salmonidae", "Anguillidae"],
    "Tetrapods": ["Bovidae", "Ranidae"],
    "Mammals": ["Bovidae", "Tachyglossidae"],
    "Therian mammals": ["Bovidae", "Macropodidae"],
    "Birds": ["Phasianidae", "Struthionidae"],
    "Molluscs": ["Ostreidae", "Octopodidae"],
    "Arthropods": ["Penaeidae", "Limulidae"],
    "Pancrustacea": ["Penaeidae", "Gryllidae"],
    "Crustaceans (decapods)": ["Penaeidae", "Portunidae"],
    "Monocots + eudicots": ["Poaceae", "Fabaceae"],
    "Lamiids": ["Solanaceae", "Lamiaceae"],
    "Campanulids": ["Asteraceae", "Apiaceae"],
    "Fabids": ["Fabaceae", "Rosaceae"],
    "Malvids": ["Brassicaceae", "Malvaceae"],
    "Commelinids": ["Poaceae", "Zingiberaceae"],
    "Ruminants": ["Bovidae", "Cervidae"],
    "Even-toed ungulates": ["Bovidae", "Camelidae"],
    "Rodents": ["Caviidae", "Sciuridae"],
    "Percomorph fishes": ["Carangidae", "Sparidae"],
    "Cartilaginous fishes": ["Squalidae", "Chimaeridae"],
    "Bivalves": ["Ostreidae", "Veneridae"],
    "Gastropods": ["Helicidae", "Haliotidae"],
    "Cephalopods": ["Octopodidae", "Loliginidae"],
    "Bees, wasps and ants": ["Apidae", "Formicidae"],
    "Beetles": ["Tenebrionidae", "Dytiscidae"],
    "Moths and butterflies": ["Cossidae", "Saturniidae"],
    "Agaricales (gilled mushrooms)": ["Agaricaceae", "Omphalotaceae"],
    "Cnidarians": ["Actiniidae", "Rhizostomatidae"],
    "Echinoderms": ["Strongylocentrotidae", "Stichopodidae"],
}

# Placements for the open tree: family -> (["@backbone node" or family anchors], age or None).
# None = attach at the node's crown (family joins at the node's age). Used ahead of PLACEMENTS when the anchor resolves.
_O = lambda node, age=None: (["@" + node], age)
PLACEMENTS_OPEN = {
    # fungi
    "Rhizopodaceae": _O("Mucoromycota + Dikarya"), "Mucoraceae": _O("Mucoromycota + Dikarya"),
    # ascomycetes now come from the Shen et al. 2020 timetree; families it lacks anchor to families it has
    "Discinaceae": (["Morchellaceae"], 120),          # sister to the morels (T. James, pers. comm.); age approximate
    "Pyronemataceae": (["Morchellaceae", "Tuberaceae"], 250), "Sarcoscyphaceae": (["Morchellaceae", "Tuberaceae"], 250),   # stem above truffles+morels, ~250 (T. James)
    "Hypocreaceae": (["Nectriaceae", "Cordycipitaceae"], None),
    "Cyttariaceae": (["Sordariaceae", "Aspergillaceae"], None),
    "Ustilaginaceae": _O("Basidiomycota"), "Phallaceae": (["Gomphaceae", "Agaricaceae"], None),
    # cnidarians, echinoderms, tunicates, worms, brachiopod, lancelet
    "Actiniidae": _O("Cnidaria"), "Rhizostomatidae": _O("Cnidaria"), "Stomolophidae": _O("Cnidaria"),
    "Strongylocentrotidae": _O("Echinoidea"), "Echinometridae": _O("Echinoidea"), "Parechinidae": _O("Echinoidea"),
    "Toxopneustidae": _O("Echinoidea"), "Echinidae": _O("Echinoidea"),
    "Stichopodidae": _O("Holothuroidea"), "Holothuriidae": _O("Holothuroidea"), "Cucumariidae": _O("Holothuroidea"),
    "Pyuridae": _O("Tunicata"), "Styelidae": _O("Tunicata"), "Branchiostomatidae": _O("Chordates"),
    "Eunicidae": _O("Annelida"), "Sipunculidae": _O("Annelida"), "Urechidae": _O("Annelida"), "Lingulidae": _O("Lophotrochozoa"),
    # molluscs
    "Chitonidae": _O("Mollusca"),
    "Pectinidae": _O("Pteriomorphia"),
    "Arcidae": _O("Ostreida + Arcida + Mytilida"), "Glycymerididae": _O("Ostreida + Arcida + Mytilida"), "Mytilidae": _O("Ostreida + Arcida + Mytilida"),
    "Ostreidae": _O("Ostreida + Arcida + Mytilida"), "Pinnidae": _O("Ostreida + Arcida + Mytilida"), "Margaritidae": _O("Ostreida + Arcida + Mytilida"),
    "Veneridae": _O("Myida + Venerida"), "Mactridae": _O("Myida + Venerida"), "Cyrenidae": _O("Myida + Venerida"), "Arcticidae": _O("Myida + Venerida"),
    "Myidae": _O("Myida + Venerida"), "Pholadidae": _O("Myida + Venerida"), "Teredinidae": _O("Myida + Venerida"),
    "Cardiidae": _O("Adapedonta + Cardiida"), "Donacidae": _O("Adapedonta + Cardiida"),
    "Solenidae": _O("Adapedonta + Cardiida"), "Pharidae": _O("Adapedonta + Cardiida"), "Hiatellidae": _O("Adapedonta + Cardiida"),
    "Patellidae": _O("Gastropoda"), "Nacellidae": _O("Gastropoda"), "Neritidae": _O("Orthogastropoda"),
    "Haliotidae": _O("Vetigastropoda"), "Fissurellidae": _O("Vetigastropoda"), "Trochidae": _O("Vetigastropoda"),
    "Tegulidae": _O("Vetigastropoda"), "Turbinidae": _O("Vetigastropoda"),
    "Ampullariidae": _O("Caenogastropoda"), "Viviparidae": _O("Caenogastropoda"), "Littorinidae": _O("Caenogastropoda"),
    "Strombidae": _O("Caenogastropoda"), "Potamididae": _O("Caenogastropoda"), "Thiaridae": _O("Caenogastropoda"),
    "Semisulcospiridae": _O("Caenogastropoda"),
    "Buccinidae": _O("Neogastropoda"), "Busyconidae": _O("Neogastropoda"), "Babyloniidae": _O("Neogastropoda"), "Muricidae": _O("Neogastropoda"),
    "Aplysiidae": _O("Heterobranchia"), "Helicidae": _O("Stylommatophora"), "Achatinidae": _O("Stylommatophora"),
    "Octopodidae": _O("Incirrata"), "Enteroctopodidae": _O("Incirrata"), "Eledonidae": _O("Incirrata"),
    "Sepiidae": _O("Decabrachia"), "Sepiolidae": _O("Decabrachia"), "Loliginidae": _O("Myopsida"),
    "Ommastrephidae": _O("Oegopsida"), "Enoploteuthidae": _O("Oegopsida"),
    # crustaceans, chelicerates, myriapods
    "Limulidae": _O("Chelicerata"), "Theraphosidae": _O("Arachnida"), "Scorpionidae": _O("Arachnida"), "Scolopendridae": _O("Mandibulata"),
    "Balanidae": _O("Cirripedia"), "Pollicipedidae": _O("Cirripedia"), "Lepadidae": _O("Cirripedia"),
    "Squillidae": _O("Malacostraca"), "Mysidae": _O("Eumalacostraca"), "Euphausiidae": _O("Eucarida"),
    "Penaeidae": _O("Dendrobranchiata"), "Aristeidae": _O("Dendrobranchiata"), "Solenoceridae": _O("Dendrobranchiata"), "Sergestidae": _O("Dendrobranchiata"),
    "Palaemonidae": _O("Caridea"), "Pandalidae": _O("Caridea"), "Crangonidae": _O("Caridea"),
    "Palinuridae": _O("Palinuridae"), "Scyllaridae": _O("Achelata"),
    "Nephropidae": _O("Astacidea"), "Astacidae": _O("Crayfish (Astacoidea + Parastacoidea)"), "Cambaridae": _O("Crayfish (Astacoidea + Parastacoidea)"), "Parastacidae": _O("Crayfish (Astacoidea + Parastacoidea)"),
    "Lithodidae": _O("Anomura"), "Munididae": _O("Anomura"), "Raninidae": _O("Brachyura"),
    "Portunidae": _O("Eubrachyura"), "Cancridae": _O("Eubrachyura"), "Carcinidae": _O("Eubrachyura"), "Polybiidae": _O("Eubrachyura"),
    "Ovalipidae": _O("Eubrachyura"), "Cheiragonidae": _O("Eubrachyura"), "Majidae": _O("Eubrachyura"), "Menippidae": _O("Eubrachyura"),
    "Geryonidae": _O("Eubrachyura"), "Oregoniidae": _O("Eubrachyura"), "Varunidae": _O("Eubrachyura"), "Gecarcinidae": _O("Eubrachyura"),
    "Ucididae": _O("Eubrachyura"),
    # insects
    "Gryllidae": _O("Ensifera"), "Tettigoniidae": _O("Ensifera"), "Acrididae": _O("Acrididae + Pyrgomorphidae"), "Pyrgomorphidae": _O("Acrididae + Pyrgomorphidae"),
    "Termitidae": _O("Polyneoptera"), "Cicadidae": _O("Cicadidae"),
    "Belostomatidae": _O("Nepomorpha"), "Corixidae": _O("Nepomorpha"), "Pentatomidae": _O("Pentatomoidea"), "Tessaratomidae": _O("Pentatomoidea"),
    "Vespidae": _O("Vespidae"), "Apidae": _O("Apoidea + Formicoidea"), "Formicidae": _O("Apoidea + Formicoidea"),
    "Tenebrionidae": _O("Tenebrionidae"), "Curculionidae": _O("Cucujiformia"), "Scarabaeidae": _O("Scarabaeidae"), "Dytiscidae": (["@Coleoptera", "@Beetles"], None),   # the Coleoptera node is relabelled Beetles by CLADE_NAMES in the built tree
    "Stratiomyidae": _O("Diptera"), "Chaoboridae": _O("Diptera"),
    "Cossidae": _O("Cossidae"), "Hesperiidae": _O("Obtectomera"), "Bombycidae": _O("Bombycoidea"), "Saturniidae": _O("Saturniidae"),
    # jawless and cartilaginous fishes, herps
    "Petromyzontidae": _O("Cyclostomata"), "Geotriidae": _O("Cyclostomata"), "Myxinidae": _O("Cyclostomata"),
    "Callorhinchidae": _O("Chondrichthyes"), "Chimaeridae": _O("Chondrichthyes"),
    "Squalidae": _O("Selachii"), "Lamnidae": _O("Galeomorphii"),
    "Scyliorhinidae": _O("Carcharhiniformes"), "Triakidae": _O("Carcharhiniformes"), "Carcharhinidae": _O("Carcharhiniformes"),
    "Rajidae": _O("Batoidea"), "Dasyatidae": _O("Batoidea"),
    "Ranidae": _O("Anura"), "Dicroglossidae": _O("Anura"), "Pyxicephalidae": _O("Anura"), "Leptodactylidae": _O("Anura"),
    "Iguanidae": _O("Squamata"), "Pythonidae": _O("Squamata"), "Colubridae": _O("Squamata"), "Elapidae": _O("Squamata"),
    "Viperidae": _O("Squamata"), "Varanidae": _O("Squamata"), "Teiidae": _O("Squamata"),
    "Chelydridae": _O("Testudines"), "Emydidae": _O("Testudines"), "Trionychidae": _O("Testudines"),
    "Alligatoridae": _O("Crocodylia"), "Crocodylidae": _O("Crocodylia"),
    # fishes missing from Rabosky under my names: hang on their nearest family in his tree
    "Caesionidae": (["Lutjanidae"], 60), "Cynoglossidae": (["Soleidae"], 60), "Helostomatidae": (["Osphronemidae"], 60),
    "Rhombosoleidae": (["Pleuronectidae"], 60), "Uranoscopidae": (["Trachinidae"], 80), "Mochokidae": (["Claroteidae", "Bagridae"], 80),
    # plants missing from ALLMB
    "Cynomoriaceae": (["Grossulariaceae", "Crassulaceae"], None), "Zygophyllaceae": (["Fabaceae", "Rosaceae", "Euphorbiaceae"], 105),
    "Lennoaceae": (["Boraginaceae"], 60), "Hypoxidaceae": (["Asparagaceae", "Orchidaceae"], None),
    # brown algae
    "Ralfsiaceae": _O("BACR II-V"), "Chordaceae": _O("Laminariales"),
    "Chordariaceae": _O("Ectocarpales"), "Scytosiphonaceae": _O("Ectocarpales"),
    "Laminariaceae": _O("Laminariales"), "Alariaceae": _O("Laminariales"), "Lessoniaceae": _O("Laminariales"),
    "Fucaceae": _O("Fucales"), "Sargassaceae": _O("Fucales"), "Himanthaliaceae": _O("Fucales"), "Durvillaeaceae": _O("Fucales"),
    # red algae
    "Bangiaceae": _O("Bangiales"), "Palmariaceae": _O("Nemaliophycidae"), "Liagoraceae": _O("Nemaliophycidae"),
    "Ahnfeltiaceae": _O("Ahnfeltiophycidae + Rhodymeniophycidae"),
    "Gelidiaceae": _O("Rhodymeniophycidae"), "Pterocladiaceae": _O("Rhodymeniophycidae"), "Bonnemaisoniaceae": _O("Rhodymeniophycidae"),
    "Rhodomelaceae": _O("Ceramiales"),
    "Gracilariaceae": _O("Gracilariaceae"), "Halymeniaceae": _O("Gigartinales + Gracilariales + Halymeniales"),
    "Endocladiaceae": _O("Gigartinales + Gracilariales + Halymeniales"), "Sarcodiaceae": _O("Gigartinales + Gracilariales + Halymeniales"),
    "Gigartinaceae": _O("Gigartinales"), "Cystocloniaceae": _O("Gigartinales"), "Phyllophoraceae": _O("Gigartinales"),
    "Solieriaceae": _O("Gigartinales"), "Kallymeniaceae": _O("Gigartinales"), "Dumontiaceae": _O("Gigartinales"), "Caulacanthaceae": _O("Gigartinales"),
    # green algae
    "Ulvaceae": _O("Ulvales"), "Monostromataceae": _O("Ulvales"), "Caulerpaceae": _O("Bryopsidales"), "Codiaceae": _O("Bryopsidales"),
    "Chlorellaceae": _O("Trebouxiophyceae"), "Prasiolaceae": _O("Trebouxiophyceae"),
    "Haematococcaceae": _O("Chlorophyceae"), "Dunaliellaceae": _O("Chlorophyceae"),
}


# Alias corrections for the keyword matcher (species -> words). Applied after all other alias sources.
ALIAS_ADD = {
    "Thunnus albacares": ["tuna", "canned tuna", "tuna steak", "ahi"],
    "Thunnus thynnus": ["bluefin"],
    "Katsuwonus pelamis": ["bonito flakes", "katsuobushi"],
    "Penaeus vannamei": ["shrimp", "prawns", "prawn", "shrimps"],
    "Strongylocentrotus purpuratus": ["sea urchin", "uni", "sea urchin roe"],
    "Scomber scombrus": ["mackerel"],
    "Gadus morhua": ["cod"],
    "Salmo salar": ["salmon"],
    "Crassostrea virginica": ["oysters", "oyster"],
    "Mytilus edulis": ["mussels", "mussel"],
    "Homarus americanus": ["lobster"],
    "Octopus vulgaris": ["octopus"],
    "Doryteuthis pealeii": ["squid", "calamari"],
}
ALIAS_REMOVE = {
    "Opuntia ficus-indica": ["tuna"],            # Spanish for the fruit; collides with the fish
    "Mucor racemosus": ["cheese"], "Mucor circinelloides": ["cheese"], "Mucor mucedo": ["cheese"],
}


# Crown ages for genera whose species split far deeper than the default 5 Myr congener rule (Ma).
GENUS_CROWN = {
    "Gracilaria": 230,   # early Mesozoic; Kim et al. 2026 preprint via C. Maggs
}
