"""Stage 11 clustering rule set: cluster definitions, ordered rules, brand/noise overrides. Local, auditable; no API calls."""
# Stage 11 clustering rule set (auditable). Patterns run against a normalized keyword:
# lowercase, hyphens/slashes -> space, apostrophes removed, whitespace collapsed.
# First matching cluster (by PRIO order) wins. strength: 'S' = specific topical rule, 'L' = topic-only/lexical.

LG = r"(lab grown|lab created|lab made|laboratory grown|lab diamond|grown lab|lgd)"

A_LGD = "8. Lab-Grown Diamonds"
A_NAT = "9. Natural Diamonds"
A_SHAPE = "10. Diamond Shapes"
A_CUT = "11. Diamond Cuts"
A_4C = "12. Diamond Quality / 4Cs"
A_CERT = "13. Diamond Certification"
A_EDU = "14. Diamond Buying / Education"
A_MET = "15. Jewellery Materials / Metals"
A_GEM = "16. Gemstones"
A_ER = "1. Engagement Rings"
A_EAR = "3. Earrings"
A_UNK = "UNCLASSIFIED_OR_UNKNOWN"

I, CR, T, N, M, U = "INFORMATIONAL", "COMMERCIAL_RESEARCH", "TRANSACTIONAL", "NAVIGATIONAL", "MIXED", "UNCLEAR"

# ---------------------------------------------------------------- hard overrides
# Explicit brand terms (third-party retailers / producers / brand names). Only applied to INCLUDE/AMBIGUOUS keywords
# that Stage 5/7 did not already mark COMPETITOR_BRAND. Recorded as a Stage 11 override.
BRAND_REGEX = [
    (r"\bblue nile\b", "Blue Nile"), (r"\bbrilliant earth\b", "Brilliant Earth"), (r"\bhelzberg\b", "Helzberg"),
    (r"\btiffany\b", "Tiffany & Co."), (r"\bkay (lab|jewelers)\b|\bkay lab\b|\blab grown diamonds? kay\b|^kay\b", "Kay Jewelers"),
    (r"\bzales\b", "Zales"), (r"\bjtv\b", "JTV"), (r"\bhsn\b", "HSN"), (r"\bqvc\b", "QVC"), (r"\bmacys\b", "Macy's"),
    (r"\bcartier\b", "Cartier"), (r"\bvrai\b", "VRAI"), (r"\bluvansh\b", "Luvansh"), (r"\bmiadonna\b", "MiaDonna"),
    (r"\britani\b", "Ritani"), (r"\bdoes diamonds direct\b", "Diamonds Direct"), (r"\bdiamond nexus\b", "Diamond Nexus"),
    (r"\baffinity diamonds?\b", "Affinity Diamonds"), (r"\beterneva\b", "Eterneva"), (r"\btacori\b", "Tacori"),
    (r"\blvmh\b", "LVMH"), (r"\bidc\b", "IDC"), (r"\bbhanderi\b", "Bhanderi"), (r"\bgoenka\b", "Goenka"),
    (r"\badamante\b", "Adamante"), (r"\bcalavera\b", "Calavera"), (r"\bkira lab\b", "Kira"), (r"\bevolv\b", "Evolv"),
    (r"\bprazana\b", "Prazana"), (r"\bchamet\b", "Chamet"), (r"\ben ?route\b", "En Route Jewelry"),
    (r"\bethan and lara\b", "Ethan & Lara"), (r"\bmatilda and milo\b", "Matilda & Milo"), (r"\bslide jewelry\b", "Slide Jewelry"),
    (r"\baurate\b", "Aurate"), (r"\bpandora\b", "Pandora"), (r"\bdiesel\b", "Diesel"), (r"\bluvansh\b", "Luvansh"),
    (r"\bdew moissanite\b", "Dew Moissanite"), (r"\bdiamonluxe\b", "Diamonluxe"), (r"\bagape\b", "Agape"),
    (r"\bsimplex diamonds\b", "Simplex Diamonds"), (r"\bnivoda\b", "Nivoda"), (r"\brapaport\b", "Rapaport"),
    (r"\bnatural diamond council\b", "Natural Diamond Council"), (r"\btriton (tungsten )?rings\b", "Triton"),
    (r"\bvibranium lab\b", "Vibranium (unverified brand-style query)"), (r"\bneptune diamonds\b", "Neptune Diamonds"),
    (r"\bmethra\b", "Methra"), (r"\bkaiser diamond bar\b", "Kaiser Diamond Bar"), (r"\bquest lab diamond bar\b", "Quest Lab Diamond Bar"),
    (r"\bgemesis\b", "Gemesis"), (r"\btanishq\b", "Tanishq"), (r"\bstuller\b", "Stuller"), (r"\bcanos\b", "Canos"),
    (r"\bshaftel\b", "Shaftel Diamonds"), (r"\bshapiro diamonds\b", "Shapiro Diamonds"), (r"\bstrauss diamond\b", "Strauss Diamond"),
    (r"\btidewater diamond\b", "Tidewater Diamond"), (r"\bprovidence diamond\b", "Providence Diamond"),
    (r"\bcontinental diamond\b", "Continental Diamond"), (r"\borigin diamonds\b", "Origin Diamonds"),
    (r"\buniversal diamonds\b", "Universal Diamonds"), (r"\bpure grown diamonds\b", "Pure Grown Diamonds"),
    (r"\beliantte\b", "Eliantte"), (r"\bdanger incorporated\b", "Danger Incorporated Diamonds"),
    (r"\bmiadonna\b", "MiaDonna"), (r"\bhearts on fire\b", "Hearts On Fire"), (r"\bjared\b", "Jared"), (r"\bloose grown diamonds?\b", "Loose Grown Diamond"), (r"\bcaydia\b", "Caydia"),
]

# Name patterns that look like company names but whose brand identity is NOT independently verified in project data.
# These are routed to UNCLUSTERED_REVIEW (not COMPETITOR_BRAND) to avoid asserting a brand identity.
WEAK_BRAND_REGEX = r"\b(canos|chamet|continental diamond|origin diamonds|universal diamonds|providence diamond|strauss diamond|tidewater diamond|shaftel|shapiro diamonds|neptune diamonds|simplex diamonds|eliantte|danger incorporated|pure grown diamonds|vibranium|kaiser diamond bar|quest lab diamond bar|methra)\b"

# Off-topic patterns (gaming, cannabis, industrial, sports/people, local business names, craft kits, unrelated 'ring' products).
# Applied only to INCLUDE/AMBIGUOUS keywords; tag records the basis.
NOISE_REGEX = [
    (r"\b(thc|thca|live resin|liquid diamonds?|liquid live|diamonds? dabs?|diamond dabber|diamond concentrates|diamonds strain|diamond vape|rosin|cartridge|jeeter|stiiizy|hypervenom|muha)\b|^melted diamonds?( vs live resin| muha)?$|^live resin", "CANNABIS_PRODUCT (Stage 8: thc/thca SERPs are cannabis)"),
    (r"\b(minecraft|elytra|armor|pickaxe|smelt|tnt|prot [13] iron|y level|y11|y 11|rlcraft|fivem|matcap|blender|azerothian|capacitive primal|doppler|kryptonite|cotw|mine diamonds with gold|diverging diamond|ugk diamonds)\b|^what level is best for diamonds$|^double diamond fabrication$", "GAMING_REFERENCE"),
    (r"\b(oura|simplisafe|og anunoby|tales of wedding rings|saint tree bellvine)\b|^adt vs ring$", "UNRELATED_CONSUMER_PRODUCT_OR_GAME"),
    (r"\b(diamond dotz|dotz|dust diamonds)\b|^dotz diamond kits$", "CRAFT_KIT (Stage 8: dust diamonds SERP = diamond painting)"),
    (r"^(diamond (bits?|burr|coring bit|core|paste|powder|polishing paste|stropping compound|whetstone|wire|wafers|sand|mills|grid|anvil cell|coating|emulsions|peel)|white diamond (powder|polishing compound)|polycrystalline diamond|industrial diamond|wera diamond bits|lenox diamond bit|ftb diamond drill|ls diamond pistons|diamond custom pistons|diamond z grinders|atoma diamond (plate|sharpening stones|stone)|whetstone vs diamond|diamond stropping compound|pna diamond dowels)$", "INDUSTRIAL_ABRASIVE_OR_TOOL"),
    (r"^(diamond (deshields|construction|detailing|recycling|equipment|disposal|waste|storage|brass|grille|brite|bolts? e|bolt e|kinetics|spaulding|contracting|prox|environment|devices|sa|d3|type frame)|reed diamond|marcite vs diamond brite)$", "NAMED_PERSON_OR_LOCAL_BUSINESS_OR_HARDWARE (Stage 8 SERP evidence where validated)"),
    (r"^(solder rings|lead ring|pyrrole ring|six carbon ring|3 carbon ring|ring of elements|methra ring making|sparx rings|rsc rings|embr rings|triodent rings|rolled ring forgings|ring moulds|powder coated (d )?rings|pure steel rings|tungsten copper ring|cast vs moly rings|tymo ring or ionic|ring vs simplisafe)$", "UNRELATED_RING_PRODUCT_OR_CHEMISTRY"),
    (r"^(diamond (crystal salt|naturals|water))$", "CONSUMER_PRODUCT_BRAND_UNRELATED (salt/pet food/beverage)"),
    (r"^(skewb diamond|diamond tessellation|epp diamond patterns|diamond tufting|diamond lit|diamond texture|diamond texture fivem|ripstop diamond|diamond mosaic|mosaic diamond|diamond overlay)$", "NON_JEWELLERY_MEANING (geometry/pattern/craft/sign language)"),
    (r"^(transmute diamond|diamond alchemy|unscramble diamond|diamond shreddies|diamond stl|hardest diamonds cotw|diamond glaze|diamond grooming|diamond detailing|diamond development|diamond construct|diamond works|diamond energy|diamond process|diamond cluster|diamond concepts?|diamond presentation|diamond problems?|diamond problem solver|diamond problems examples|diamond sweat|diamond cell|diamond intent|diamond heat|diamond fusion su|diamonds fusion|diamond veneer|diamond ore|diamond ore texture|hazard diamond|hazmat diamond|diamond kits?)$", "GENERIC_NON_JEWELLERY_MEANING (business/idiom/tech/game/hardware)"),
]

# ---------------------------------------------------------------- cluster definitions
# fields: id, name, parent, area, primary_intent, secondary_intents, definition, patterns [(regex, strength)], exact [kw], notes
CLUSTERS = []


def cl(id, name, parent, area, pi, si, definition, patterns=(), exact=(), notes="", prio=50, ambiguous_ok=False):
    def _lk(p):
        if p.startswith(LG + ".*"):
            rest = p[len(LG) + 2:]
            return "(?=.*" + LG + ")(?=.*" + rest + ")"
        return p
    pats = [(p if isinstance(p, tuple) else (p, "S")) for p in patterns]
    pats = [(_lk(p), st) for p, st in pats]
    CLUSTERS.append(dict(id=id, name=name, parent=parent, area=area, primary_intent=pi, secondary_intents=si,
                         definition=definition, patterns=pats,
                         exact=set(exact), notes=notes, prio=prio, ambiguous_ok=ambiguous_ok))


P_LGD = "Lab-Grown Diamonds"
P_CERT = "Diamond Certification"
P_4C = "Diamond Quality & 4Cs"
P_SHAPE = "Diamond Shapes & Types"
P_NAT = "Natural Diamonds"
P_SCI = "Diamond Science & Education"
P_ALT = "Moissanite & Diamond Alternatives"
P_GEM = "Gemstones"
P_MET = "Jewellery Metals & Materials"
P_RING = "Rings, Settings & Earrings"

# ---- Lab-grown ----
cl("CL-001", "Lab-Grown Diamonds: General & Head Terms", P_LGD, A_LGD, M, [T, N, CR, I],
   "Broad head-term demand for lab-grown/lab-created diamonds where Stage 8 shows retailer/category SERPs (brand- and category-dominant) rather than a single informational intent.",
   exact=["lab grown diamonds", "lab diamonds", "lab created diamonds", "diamond growing lab", "laboratory grown diamonds", "grown lab diamond",
          "grown lab diamonds", "online lab grown diamonds", "lab grown diamond online", "loose diamonds lab", "lab stone diamond", "lab diamond search",
          "lab grown diamond search", "lab grown diamond lab", "lab grown diamonds lab", "unique lab grown diamond", "lab diamond companies",
          "lab cut diamond", "lab grown diamonds direct", "lab diamonds direct", "what is the best lab grown diamond"],
   patterns=[(r"^high quality lab (grown )?diamonds$", "S"), (r"^lab grown diamonds? (lab|search)$", "S"), (r"^grown diamonds$", "L")],
   notes="Validated head terms (lab grown diamonds / lab diamonds / diamond growing lab) share 4-7 top-10 URLs each other in Stage 8.", ambiguous_ok=True, prio=1)
cl("CL-002", "What Are Lab-Grown Diamonds? Definition & Basics", P_LGD, A_LGD, I, [],
   "Definitional/encyclopedic queries about what lab-grown diamonds are.",
   patterns=[r"^lab grown diamonds? (definition|wiki|wikipedia|information|article|forum|wsj)$", r"^man made diamonds wiki$"])
cl("CL-003", "Lab-Grown Diamond Names & Terminology", P_LGD, A_LGD, I, [CR],
   "What lab-grown diamonds are called (lab-created, synthetic, man-made, cultured) and how the terms differ.",
   patterns=[r"^lab grown diamonds? (name|called|name list)$", r"^(name of|lab created diamonds? name|lab grown vs lab created)", r"^lab grown diamonds? called$",
             r"^synthetic diamonds$", r"^lab created diamonds? name$", r"^ftc "])
cl("CL-004", "Types of Lab-Grown Diamonds", P_LGD, A_LGD, I, [CR],
   "Searchers asking what kinds/categories of lab-grown diamond exist.",
   patterns=[r"^(different )?types of lab grown diamonds?$", r"^lab grown diamond types$"])
cl("CL-005", "Lab-Grown Diamonds by Location (local and country modifiers)", P_LGD, A_LGD, M, [T, N, CR, I],
   "Lab-grown diamond queries with a city, state or country modifier (local/regional purchase intent). Includes non-US modifiers present in the Stage 4/6 data.",
   patterns=[rf"{LG}.*\b(uk|usa|us|europe|ireland|switzerland|uae|vietnam|hk|lebanon|belgium|toronto|vancouver|ontario|edmonton|dfw|philadelphia|phoenix|portland|utah|nj|dc)\b$",
             r"^(us|usa) lab grown diamonds$"],
   notes="Modifier list is taken from keywords actually present in the master database; not an exhaustive geo taxonomy.", prio=20)
cl("CL-006", "Lab-Grown Diamonds by Carat Weight", P_LGD, A_LGD, T, [CR, I],
   "Carat-size-specific lab-grown diamond queries (shopping/size browsing).",
   patterns=[r"^\d+ ?ct lab created diamond$", r"^lab grown diamonds? ct$", r"^ct diamond$", r"^calibrated lab grown diamonds$"],
   notes="'ct diamond' and 'calibrated lab grown diamonds' are low-evidence peripheral members.", ambiguous_ok=True)
cl("CL-007", "Lab-Grown Diamond Wholesale & Suppliers (Trade)", P_LGD, A_LGD, T, [N, CR],
   "B2B/trade purchasing queries: wholesale, suppliers and melee for lab-grown diamonds and gemstones.",
   patterns=[rf"{LG}.*\b(wholesale|supplier|melee)\b", r"^lab grown gemstones wholesale$"],
   notes="Stage 8 validated 'wholesale lab grown diamonds' (Stuller, B2B suppliers). Stage 9 competitors for this SERP differ from consumer retailers.")
cl("CL-008", "Lab-Grown Diamond Pricing & Affordability", P_LGD, A_LGD, I, [CR, T],
   "Cost and price questions: are lab-grown diamonds cheaper, price per carat, clearance/affordable options.",
   patterns=[rf"{LG}.*\b(cheaper|cheap|less expensive|per carat|clearance|get cheaper)\b", r"^affordable lab created diamonds$", r"^will lab grown diamonds get cheaper$"])
cl("CL-009", "Lab-Grown Diamond Value, Resale & Investment", P_LGD, A_LGD, I, [CR],
   "Whether lab-grown diamonds hold value, can be resold, or are an investment.",
   patterns=[rf"{LG}.*\b(hold (their )?value|resale value|good investment|increase in value|have value|worthless|worth less|worth anything)\b",
             r"^does lab diamond have resale value$", r"^do natural diamonds hold value better than lab grown$", r"^will lab grown diamonds hold value$",
             r"^do lab grown diamonds hold value$"], prio=41)
cl("CL-010", "Are Lab-Grown Diamonds Real? (Authenticity)", P_LGD, A_LGD, I, [CR],
   "Is a lab-grown diamond a real/genuine diamond or fake. Stage 8: COMPARISON/editorial SERP (reddit, retailer guides).",
   patterns=[rf"{LG}.*\b(real|fake|genuine)\b", rf"^(is|are) .*{LG}.* (real diamonds?|a real diamond)$", r"^lab created diamond real$", r"^lab created diamonds real$"],
   notes="Excludes moissanite/cubic-zirconia/tester/brand phrasing, which are routed earlier.")
cl("CL-011", "Lab-Grown vs Natural Diamonds", P_LGD, A_LGD, CR, [I],
   "Head-to-head comparison of lab-grown and natural diamonds (differences, which is better, natural vs synthetic). Stage 8: four validated variants share 3-7 top-10 URLs.",
   patterns=[r"\b(vs|versus|or|and) (natural|mined|real)\b.*", r"\bnatural (vs|versus|or) ", r"difference between (lab|natural)", r"^is there a difference between lab grown and natural",
             rf"^(which|what).*(better|best).*{LG}.*natural", r"^lab (or|vs) natural", r"^natural (or|vs) lab", r"^natural versus lab", r"^diamonds lab vs natural$",
             r"^lab diamonds vs diamonds$", r"^lab made vs natural", r"^natural and lab grown diamonds$", r"^natural vs synthetic diamonds$", r"^difference between lab grown diamonds$",
             r"^lab grown diamonds? difference$", r"^natural diamonds? (vs|versus) lab", r"^what s better lab grown or natural", r"^which diamond is better lab grown or natural"],
   notes="'Real' comparisons ('are lab grown diamonds real') are a separate authenticity cluster; SERP overlap between the two is 0-2 URLs.", prio=40)
cl("CL-012", "Are Lab-Grown Diamonds Worth It? (Pros, Cons & Buying Decision)", P_LGD, A_LGD, I, [CR, T],
   "Evaluation queries: are they good/worth it, pros and cons, disadvantages, should I buy, tacky/popular.",
   patterns=[rf"{LG}.*\b(worth it|waste of money|good|okay|ok|tacky|popular|cons|pros and cons|disadvantages|better|replace the real thing|should i buy|worth the money)\b",
             r"^should i buy (a )?lab grown diamonds?", r"^cons of lab grown diamonds$", r"^disadvantages of lab grown diamonds$", r"^are lab grown diamonds worth it$"],
   notes="Ambiguous 'better' phrasing without a natural comparator lands here (LOW).", prio=42)
cl("CL-013", "Ethical & Sustainable Lab-Grown Diamonds", P_LGD, A_LGD, I, [CR],
   "Ethical, environmental and sustainability questions about lab-grown diamonds.",
   patterns=[rf"{LG}.*\b(ethical|sustainable|sustainability|environment|environmentally friendly|carbon neutral|eco)\b", r"^(eco grown diamond|ethical lab grown diamonds|sustainable lab grown diamonds|carbon neutral lab grown diamonds)$"], prio=39)
cl("CL-014", "Lab-Grown Diamond History & Market Trends", P_LGD, A_LGD, I, [],
   "History, origins, market direction and popularity of lab-grown diamonds.",
   patterns=[rf"{LG}.*\b(history|first|trends|future)\b", r"^are more people buying lab grown diamonds$", r"^largest synthetic diamond$", r"^general electric man made diamond$",
             r"^first lab grown diamond$", r"^future of lab grown diamonds$"])
cl("CL-015", "How Lab-Grown Diamonds Are Made (Process)", P_LGD, A_LGD, I, [],
   "How lab-grown/synthetic diamonds are manufactured, in general terms (not the CVD-vs-HPHT comparison).",
   patterns=[rf"{LG}.*\b(process|made|making|methods|manufacturing|how|time lapse)\b", r"^how are synthetic diamonds made$", r"^synthetic diamonds process$", r"^can we make artificial diamonds$",
             r"^can you make diamonds$", r"^how lab grown diamonds$", r"^lab grown diamond process$", r"^lab grown diamond methods$"])
cl("CL-016", "CVD vs HPHT Lab-Grown Diamonds", P_LGD, A_LGD, I, [CR],
   "Comparison of the two lab-grown growth methods (CVD vs HPHT), including 'which is better'. Stage 8: nine validated variants share 4-7 top-10 URLs pairwise (tightest SERP group in the dataset). HOD holds Stage 3 rankings for this family.",
   patterns=[r"^(?!.*tester)(?=.*\bcvd\b)(?=.*\bhpht\b)", r"^(what is )?cvd diamond vs lab grown$"], prio=10,
   notes="Stage 8 override of wording: 'cvd diamond vs lab grown' and 'what is cvd diamond vs lab grown' share 4-5 top-10 URLs with the CVD-vs-HPHT SERPs, so Google serves them the same intent.")
cl("CL-017", "HPHT Lab-Grown Diamonds", P_LGD, A_LGD, I, [T, CR],
   "Single-method HPHT queries (what HPHT lab diamonds are). Stage 8: five validated variants share 6-8 top-10 URLs pairwise but only 0-3 URLs with the CVD-vs-HPHT SERPs.",
   patterns=[r"\bhpht\b"], prio=30)
cl("CL-018", "CVD Lab-Grown Diamonds", P_LGD, A_LGD, I, [CR],
   "Single-method CVD queries (what CVD diamonds are, are CVD diamonds real, CVD vs generic lab-grown). Stage 8 SERPs for these share 2-5 URLs with the CVD-vs-HPHT SERPs.",
   patterns=[r"\bcvd\b"], prio=31, ambiguous_ok=True)
cl("CL-019", "Lab-Grown Diamond Fluorescence & Appearance", P_LGD, A_LGD, I, [],
   "Physical/optical behaviour of lab-grown diamonds: fluorescence, glow, cloudiness, fading, rainbow sparkle, looking real.",
   patterns=[rf"{LG}.*\b(fluoresce|fluorescence|glow|cloudy|fade|tarnish|sparkle|look real|uv light)\b", rf"^do {LG}.*(fluoresce|glow|cloudy|fade|tarnish|sparkle|look real)"], prio=30,
   notes="Hardness/durability of lab-grown diamonds is routed to the generic hardness cluster.")
cl("CL-020", "Telling Lab-Grown from Natural Diamonds (Identification & Detection)", P_LGD, A_LGD, I, [CR],
   "How to identify or detect a lab-grown diamond: jeweler detection, microscope, serial numbers, X-ray.",
   patterns=[rf"{LG}.*\b(detected|jeweler tell|microscope|serial numbers?|x ray|tell)\b", r"^can a jeweler tell", r"^real diamond under microscope$", r"^do lab grown diamonds have serial numbers$"], prio=36)
cl("CL-021", "Do Lab-Grown Diamonds Pass a Diamond Tester?", P_LGD, A_LGD, I, [CR],
   "Will a standard diamond tester read a lab-grown diamond as real. No Stage 8 validation for this exact phrasing.",
   patterns=[rf"{LG}.*\b(pass|test as|test real|pass the diamond test)\b", r"^do si diamonds pass diamond tester$", r"^will si diamonds pass a diamond tester$"], prio=25)
cl("CL-022", "Diamond Testers & Testing Methods", P_LGD, A_LGD, T, [CR, I],
   "Diamond tester devices and how to test a diamond (thermal/electrical testers, CVD/HPHT testers, where to get a diamond tested). Stage 8 SERPs inside this cluster share 0 top-10 URLs, so the sub-needs are heterogeneous.",
   patterns=[r"\btesters?\b", r"^where can i get a diamond tested$", r"^light test diamond$", r"^diamond sparkle test$", r"^raw diamond testing$", r"^diamond vs cubic zirconia test$", r"^does a diamond tester work on gold$"], prio=26,
   notes="Business area follows Stage 5/6 (lab-grown/education) but tester-device SERPs are CATEGORY/EDITORIAL mixed.")
cl("CL-023", "Lab-Grown Diamond Quality Grades & Charts", P_LGD, A_LGD, I, [CR],
   "Clarity/quality/grade charts and ratings specifically framed around lab-grown diamonds.",
   patterns=[rf"{LG}.*\b(clarity|quality|grades|chart|ratings|scale|vvs|flawless)\b", r"^clarity lab grown", r"^vvs lab", r"^quality of lab grown", r"^best clarity for lab grown diamond$", r"^lab diamonds clarity chart$",
             r"^do lab grown diamonds have clarity ratings$"], prio=45)
cl("CL-024", "Choosing a Lab-Grown Diamond (Buying Guidance)", P_LGD, A_EDU, CR, [I, T],
   "Buying-guide style queries for choosing a lab-grown diamond or ring. HOD holds a Stage 3 ranking for 'how to choose a lab grown diamond'.",
   patterns=[r"^how to choose a lab grown diamond$", r"^should i buy a lab grown diamond engagement ring$"], prio=15)

# ---- Certification ----
cl("CL-026", "Lab-Grown Diamond Industry, Manufacturing & Business", P_LGD, A_LGD, I, [CR],
   "Industry-side queries: factories, manufacturing technology, equipment, production, expos and starting/running a lab-grown diamond business.",
   patterns=[rf"{LG}.*\b(factory|equipment|expo|business|industry|technology|production)\b"],
   notes="Trade/industry information; distinct from wholesale purchasing (CL-007) and from how-it-is-made curiosity (CL-015), with which it may share searchers.")
cl("CL-030", "Diamond Certification Lab Comparisons (GIA vs IGI vs Others)", P_CERT, A_CERT, CR, [I],
   "Comparisons and choice among grading labs (GIA vs IGI vs AGS/EGL/GSI). Stage 8: 'gia vs igi lab diamond' is EDITORIAL; shares 0 URLs with the general certification SERP.",
   patterns=[r"\b(gia|igi|ags|egl|gsi)\b.*\b(vs|versus|or)\b", r"^which diamond certificate is the best$", r"^different diamond certifications$", r"^is egl a good diamond certificate$", r"^igi certified diamonds vs gia$"], prio=12)
cl("CL-031", "GIA Lab-Grown & Natural Diamond Reports", P_CERT, A_CERT, I, [CR, N],
   "GIA-specific queries: does GIA certify lab-grown diamonds, GIA reports/grading, GIA lab-grown or natural.",
   patterns=[r"\bgia\b"], prio=32)
cl("CL-032", "IGI Lab-Grown Diamond Certification & Reports", P_CERT, A_CERT, I, [CR],
   "IGI-specific queries: IGI lab-grown certification, IGI reports, grading chart, is IGI good.",
   patterns=[r"\bigi\b"], prio=33, notes="HOD has an IGI blog article (Stage 10); topic string-match links the cluster to it.")
cl("CL-033", "Lab-Grown Diamond Certification & Grading (Overview)", P_CERT, A_CERT, I, [CR],
   "General certification/grading/report questions for lab-grown diamonds not tied to one lab.",
   patterns=[rf"{LG}.*\b(certif|certified|certificate|graded|grading|report|appraisal)\b", r"^are lab grown diamonds graded$", r"^do lab grown diamonds come with a certificate$", r"^grading lab grown diamonds$",
             r"^certified lab diamonds$", r"^lab grown diamond certification$", r"^lab grown diamond report check$", r"^lab diamond grading$"], prio=44)
cl("CL-034", "Other Grading Labs, Report Lookup & Generic Diamond Reports", P_CERT, A_CERT, N, [I, CR],
   "AGS, GCAL, EGL, GSL/GEL lookups and generic grading-lab/report queries. Stage 8: 'ags diamond grading' is BRAND/navigational.",
   patterns=[r"\b(ags|gcal|egl|gsl|gel)\b", r"^diamond grading (lab|report|kit)$", r"^national diamond lab$", r"^diamond lab report$", r"^certified natural diamonds$", r"^can you sell diamond without certificate$",
             r"^lab grown diamond report$"], prio=34, ambiguous_ok=True)

# ---- 4Cs ----
cl("CL-040", "Diamond Grading Scales & 4Cs Charts (General)", P_4C, A_4C, I, [CR],
   "General grading-scale/chart/classification queries (color, clarity, cut together) not specific to one grade. Stage 8: 'diamond clarity grading scale' SERP is UNCLEAR/OTHER.",
   patterns=[r"^diamond (clarity grading scale|clarity types|clarity comparison|grading chart|grading scale|classification chart|quality scale|quality measurement|grading and clarity|characteristics)$",
             r"^grading system for diamonds$", r"^4cs of diamond grading$", r"^diamond categories$", r"^diamond clarity chart$"], prio=46)
cl("CL-041", "SI Clarity Diamonds (SI1, SI2, SI3)", P_4C, A_4C, I, [CR],
   "Single-grade explainers and quality questions for SI clarity. Stage 8: 'si2 diamond' and 'si2 diamond clarity' share 7 URLs.",
   patterns=[r"\bsi[123]?\b.*(diamond|clarity|quality)", r"^is si (diamond )?good$"], prio=42, ambiguous_ok=True)
cl("CL-042", "VS Clarity Diamonds (VS1, VS2)", P_4C, A_4C, I, [CR],
   "Single-grade explainers and quality questions for VS clarity.",
   patterns=[r"^vs (clarity )?diamond( clarity| quality| chart)?$", r"^is vs1 good for a diamond$", r"^are vs2 diamonds eye clean$", r"^vs1? or vs2$"], prio=43)
cl("CL-043", "VVS, IF & Flawless Clarity Diamonds", P_4C, A_4C, I, [CR],
   "VVS/IF/FL clarity explainers. Stage 8: 'v v s diamond' (18,100) is informational/editorial (HIGH).",
   patterns=[r"^v v s diamond$", r"\bvvs\b.*(diamond|lab)", r"^are vvs diamonds lab grown$", r"^flawless diamonds vs vvs$"], prio=47, ambiguous_ok=True)
cl("CL-044", "Clarity Grade Comparisons (VS vs SI, VVS vs VS, IF vs FL)", P_4C, A_4C, CR, [I],
   "Comparing adjacent clarity grades to decide between them.",
   patterns=[r"\b(vs|vvs|si|if|fl|flawless)\b.*\b(vs|or|versus)\b.*\b(vs|vvs|si|if|fl|flawless)\b", r"^diamond clarity vs$", r"^difference between (si|vs|vvs)", r"^which diamond is better vs", r"^diamond clarity vvs vs$", r"^diamond vs si$"], prio=41)
cl("CL-045", "Best Diamond Clarity to Buy", P_4C, A_4C, CR, [I],
   "How much clarity matters and which clarity grade to choose.",
   patterns=[r"^what is the best clarity for a diamond$", r"^which is the best diamond clarity$", r"^what clarity diamond should i get$", r"^does diamond clarity really matter$",
             r"^how much does diamond clarity matter$", r"^best clarity for lab grown diamond$"], prio=35)
cl("CL-046", "Diamond Inclusions & Eye-Clean Clarity", P_4C, A_4C, I, [],
   "What inclusions/imperfections are and what is eye-clean.",
   patterns=[r"^diamond (inclusions|inclusion examples|internal graining)$", r"^imperfection in a diamond$", r"^lab grown diamond inclusions$"], prio=36)
cl("CL-047", "Diamond Color Grades: Comparisons & Quality", P_4C, A_4C, CR, [I],
   "Color-grade comparisons (D vs E, G vs H, near-colorless) and whether a color grade is good. Stage 8: 'are g h diamonds good quality' is editorial (HIGH).",
   patterns=[r"^[d-k]( |$)(vs|or)?", r"^[d-k]{2} (vs|quality)", r"^(f|g|h|i|j) ?(g|h|i|j)? vs diamond$", r"^are (g h|gh) diamonds? good quality$", r"^is (f|g h|gh) diamond good$",
             r"^color grade diamond$", r"^what letter diamond is the best$", r"^colorless diamond$", r"^ef quality diamond$", r"^d f diamond$", (r"^d diamond$", "L"), (r"^diamond (j|k)$", "L"), (r"^k diamonds?$", "L")], prio=48, ambiguous_ok=True)
cl("CL-048", "Color & Clarity Grade Combinations (e.g. G/VS, F-VS2)", P_4C, A_4C, CR, [I],
   "Queries pairing a color grade with a clarity grade.",
   patterns=[r"^is (f|gh|g h) (vs2|si|si2)", r"^is f (vs2|si2) a good diamond$", r"^g vs diamond quality$", r"^vs g h diamond quality$", r"^vvs (vs|ef)", r"^diamond e vs$", r"^ef vs g h diamond$", r"^g h vs (si|i j)",
             r"^ij si vs gh si diamond$", r"^g h vs i j diamond$", r"^vvs ef diamond rate$", r"^vs and vvs diamond$"], prio=38, ambiguous_ok=True)
cl("CL-049", "Diamond Carat Size Suitability (Is It Big Enough?)", P_4C, A_4C, I, [CR],
   "Whether a given carat weight is a good size / too small / too big, including carat abbreviations.",
   patterns=[r"^is (a )?(\d|half|one|1).*(carat|ct)", r"^is a? ?half carat", r"^is (a )?\d.*(too small|too big|good size)", r"^diamond ct vs ctw$", r"^is (\d+ \d+|\d/\d+) ?(ct|carat)"], prio=37)
cl("CL-050", "Diamond Cut Quality & Grades", P_4C, A_CUT, I, [CR],
   "What cut grade means and which cut quality gives the best sparkle. Stage 8: 'diamond cut grade' is editorial (HIGH).",
   patterns=[r"cut grade", r"^what is a good cut for a diamond$", r"^does the cut of a diamond matter$", r"^is (ideal|very good|brilliant) cut", r"^what is super ideal cut diamond$",
             r"^what is the best cut", r"^standard cut diamond$", r"^ideal cut", r"^does .*cut of a diamond"], prio=39)
cl("CL-051", "Fancy-Colored Diamonds (Black, Red, Pink, Green, Purple & Others)", P_4C, A_4C, I, [CR, T],
   "Coloured/fancy diamonds, natural and lab-grown: are they real, lab-grown colours, natural fancy colours.",
   patterns=[r"^(?!.*opal)(?!.*natural white).*\b(black|red|pink|green|purple|orange|brown|blue|salt and pepper) diamonds?\b(?!.*(dust|powder|company))", r"^is there red diamonds$", r"^natural (red|orange|brown) diamond$", r"^lab grown (red|green|purple|black)"], prio=22,
   notes="Natural and lab-grown fancy colours share the same searcher subject; origin is a secondary axis.")

# ---- Shapes ----
cl("CL-060", "Diamond Shapes Overview", P_SHAPE, A_SHAPE, I, [CR],
   "Broad 'diamond shape' demand (60,500). Stage 8: informational/editorial SERP (HIGH).",
   patterns=[r"^diamond shape$"], prio=50)
cl("CL-061", "Asscher Cut Diamonds", P_SHAPE, A_SHAPE, M, [T, CR, N],
   "Asscher shape queries incl. asscher vs emerald/radiant and asscher moissanite/lab. Stage 8: 'asscher cut diamond' UNCLEAR/OTHER (retailers), 'asscher diamond' BRAND-dominant.",
   patterns=[r"\basscher\b"], prio=18)
cl("CL-062", "Radiant Cut Diamonds", P_SHAPE, A_SHAPE, M, [T, I],
   "Radiant shape queries incl. length-to-width ratio and radiant lab-grown.",
   patterns=[r"\bradiant\b"], prio=19)
cl("CL-063", "Marquise-Oval & Moval Diamonds (Elongated Cuts)", P_SHAPE, A_SHAPE, T, [I, CR],
   "Moval/marquise-oval hybrid shape queries. Stage 8: 'marquise oval diamond' is a PRODUCT SERP; HOD ranks for it with a PDP (Stage 3/10).",
   patterns=[r"\bmoval\b", r"^marquise oval diamond$"], prio=17, ambiguous_ok=True)
cl("CL-064", "Choosing a Diamond Shape (Emerald, Princess & Other Cuts)", P_SHAPE, A_SHAPE, CR, [I],
   "Shape-selection and shape-quality questions (does an emerald cut sparkle, is princess good, which shape to get).",
   patterns=[r"^does an emerald cut diamond sparkle$", r"^is an emerald cut diamond more expensive$", r"^is princess cut diamond good$", r"^what shape diamond should i get$"], prio=51)
cl("CL-065", "Types of Diamonds (General Overview)", P_SHAPE, A_EDU, M, [I, CR],
   "Broad 'types of diamonds / diamond types / diamond names' queries whose intended sense (shapes, natural vs lab, type Ia/IIa, colours) is not resolved by available SERP evidence.",
   patterns=[r"^(diamond types|types of diamonds|different types of diamonds|diamond types vs|different diamond names|list of diamond names|diamond materials)$"], prio=52)

# ---- Natural ----
cl("CL-070", "Natural Diamonds: General & Head Terms", P_NAT, A_NAT, M, [N, CR, T, I],
   "Head-term demand for natural/mined diamonds, including natural wholesale. Stage 8: 'natural diamonds' and 'natural mined diamonds' are BRAND/navigational-dominant and 'natural diamond wholesale' shares 5 top-10 URLs with 'natural diamonds'.",
   patterns=[r"^natural (mined |grown |white |untreated )?diamonds?( stone)?$", r"^natural untreated diamonds?$", r"^natural mined diamonds$", r"^gia natural diamonds$", r"^natural diamond stone$", r"^natural diamond wholesale$", (r"^are white diamonds real$", "L")], prio=53)
cl("CL-071", "Rough & Raw Diamonds", P_NAT, A_NAT, T, [I],
   "Uncut/rough/raw diamond queries, natural and lab-grown. Stage 8: 'raw diamond' and 'rough natural diamond' are CATEGORY SERPs (rough-diamond dealers).",
   patterns=[r"^(?!.*(impact|star))(?=.*\b(rough|raw|unpolished|unrefined)\b)(?=.*(diamond|lab grown))", r"^(rough|raw) diamond$", r"^how raw diamond look like$", r"^lab grown rough diamonds$", r"^raw red diamond$"], prio=21, ambiguous_ok=True)
cl("CL-073", "Blood Diamonds & Conflict-Free Sourcing", P_NAT, A_NAT, I, [CR],
   "Blood/conflict diamond questions, Kimberley Process and conflict-free sourcing. Stage 8: 'conflict free diamonds' SERP mixes retailers, Gem Society and Reddit (intent UNCLEAR).",
   patterns=[r"\bblood diamonds?\b", r"^conflict free diamonds$", r"^kimberley process", r"^diamond industry slavery$", r"^solutions for blood diamonds$"], prio=23)
cl("CL-074", "Diamond Mining, Extraction & Processing", P_NAT, A_NAT, I, [],
   "How natural diamonds are mined, extracted and processed.",
   patterns=[r"^(how diamonds are (extracted|processed)|how is diamond extracted|diamond extraction process|stages of diamond processing|diamond mining information|diamond pipes?|diamond source)$"], prio=55)
cl("CL-075", "How Diamonds Form (Natural Formation)", P_NAT, A_NAT, I, [],
   "How diamonds are created/formed in nature (and by extension made). Ambiguous between natural and lab origin for 'how are diamonds made'.",
   patterns=[r"^what makes diamonds$", r"^how (are |do |does |is )?(a )?diamonds? (created|formed|form|made)", r"^how diamond (created|made)$", r"^diamond formation$", r"^natural diamond formation$", r"^diamonds made under pressure$", r"^diamonds pressure$",
             r"^controlled metamorphosis diamond$"], prio=56, ambiguous_ok=True)
cl("CL-076", "Diamond Industry, Supply & Rarity", P_NAT, A_NAT, I, [],
   "Market/industry, supply and rarity questions about diamonds in general.",
   patterns=[r"^(diamond industry|future of diamond industry|diamond industry collapse|diamond supply|rarity of diamonds|is diamond actually rare|blood diamond industry)$"], prio=57, ambiguous_ok=True)

# ---- Diamond science / education ----
cl("CL-080", "Diamond Composition & Crystal Structure", P_SCI, A_EDU, I, [CR],
   "What diamonds are made of: carbon, crystal lattice, mineral/element status, polymorphs (lonsdaleite, type IIa).",
   patterns=[r"^(what are diamonds made of|what element are diamonds made of|is a diamond an element|is diamond an element|is diamond a (mineral|crystal)|are diamonds minerals|diamond (mineral|atomic|molecule|element|carbon|lattice|crystalline structure|cube))$",
             r"^(diamond crystalline structure|crystalline structure of diamonds|carbon diamond|chemical diamond|hexagonal diamonds?|lonsdaleite diamond|type iia diamond|diamond vs graphite|diamond on periodic table)$"], prio=58, ambiguous_ok=True)
cl("CL-081", "Diamond Melting Point & Heat Resistance", P_SCI, A_EDU, I, [],
   "Melting/boiling point and burning/heat behaviour of diamonds.",
   patterns=[r"melting point", r"^can diamonds melt$", r"^is it possible to melt a diamond$", r"^can you burn diamond$", r"^diamond (boiling point|heating)$"], prio=24)
cl("CL-082", "Diamond Hardness & Durability", P_SCI, A_EDU, I, [CR],
   "Whether diamonds scratch/chip/break, hardness comparisons (lab-grown vs natural, moissanite, titanium, harder-than-diamond).",
   patterns=[r"\b(scratch|scratched|chip|crack|break|smash|destroy|brittle|unbreakable|hardness|harder than diamond|stronger than diamond|hard as|strong|stronger|durable|cut glass)\b.*", r"^what is stronger diamond or titanium$", r"^engagement ring stone hardness$"], prio=8)
cl("CL-083", "Diamond Basics & General Facts", P_SCI, A_EDU, I, [],
   "General factual/encyclopedic queries about diamonds.",
   patterns=[r"^(facts about diamonds|wikipedia diamonds|diamond uses)$"], prio=61)
cl("CL-084", "Diamond Synonyms & Other Names", P_SCI, A_UNK, I, [],
   "Dictionary/thesaurus queries for the word 'diamond'.",
   patterns=[r"synonym", r"^(another word for diamond|another name for diamonds|other names for diamond|thesaurus diamond|diamond etymology|diamond in latin)$"], prio=27)
cl("CL-085", "Diamond Investment & Value Retention (General)", P_SCI, A_EDU, I, [CR, T],
   "Are diamonds a good investment / do they keep value (not lab-grown-specific).",
   patterns=[r"^(are diamonds a good investment|does the value of diamonds go up|does the price of diamonds fluctuate|is (it good to|investing in) .*diamonds?.*|does diamond rings have resale value|is it worth buying diamonds?( jewellery)?)$"], prio=62)
cl("CL-086", "Selling, Pawning & Trading In Diamonds", P_SCI, A_EDU, T, [I, CR],
   "Selling, pawning or trading in diamonds and diamond rings.",
   patterns=[r"\b(pawn|sell diamond|sell diamonds|trade in diamonds|good time to sell)\b"], prio=28)

# ---- Moissanite and alternatives ----
cl("CL-090", "Moissanite: General & Head Terms", P_ALT, A_GEM, M, [I, T],
   "Broad moissanite demand incl. meaning, natural vs lab-created moissanite, rough/raw, hardness and clarity chart. Stage 8: head term 'moissanite' MIXED; 'moissanite clarity chart' editorial.",
   patterns=[r"^moissanite$", r"\bmoissanite\b"], prio=90)
cl("CL-091", "Moissanite vs Diamond", P_ALT, A_GEM, CR, [I],
   "Is moissanite better than diamond, hardness/brilliance comparisons. Stage 8: 'is moissanite better than diamond' COMPARISON; 0 shared URLs with the moissanite-vs-lab-grown SERPs.",
   patterns=[r"moissanite.*(better than diamond|vs diamond|hardness vs diamond)", r"^is moissanite a good diamond alternative$", r"^can you tell moissanite from diamond$"], prio=4)
cl("CL-092", "Moissanite vs Lab-Grown Diamond", P_ALT, A_GEM, CR, [I],
   "Is a lab-grown diamond the same as moissanite / which is better / difference. Stage 8: two validated variants share 5 URLs.",
   patterns=[rf"moissanite.*{LG}", rf"{LG}.*moissanite", r"^are moissanites lab grown diamonds$", r"^what is better lab diamond or moissanite$", r"^what is better a lab grown diamond or moissanite$"], prio=3)
cl("CL-093", "Do Moissanite Pass a Diamond Tester?", P_ALT, A_GEM, I, [CR],
   "Will moissanite read as diamond on a tester. Stage 8: four validated variants share 4-5 top-10 URLs pairwise.",
   patterns=[r"moissanite.*(pass|test|tester)"], prio=2)
cl("CL-094", "Cubic Zirconia vs Diamond & Lab-Grown Diamond", P_ALT, A_GEM, CR, [I],
   "Cubic zirconia (CZ) compared to diamond / lab-grown diamond.",
   patterns=[r"\b(cubic zirconia|cz|zirconia)\b(?!.*(moissanite|enhancer))", r"^is cubic zirconia real diamond$"], prio=6)
cl("CL-095", "Diamond Simulants & Alternatives", P_ALT, A_GEM, CR, [I, T],
   "Diamond alternatives/simulants/substitutes and simulated diamonds.",
   patterns=[r"\b(simulant|simulants|simulated diamonds?|diamond alternatives?|diamond substitute|lab simulated diamonds|lab created diamond alternative)\b"], prio=71)
cl("CL-096", "Moissanite vs Other Stones (CZ, Sapphire, Morganite)", P_ALT, A_GEM, CR, [I],
   "Moissanite compared with cubic zirconia, sapphire or morganite.",
   patterns=[r"moissanite.*(zirconia|sapphire|morganite)", r"(zirconia|sapphire|morganite).*moissanite"], prio=1.5)

# ---- Gemstones ----
cl("CL-100", "Sapphire: Natural, Lab-Created & White Sapphire", P_GEM, A_GEM, M, [I, T, CR],
   "Natural and lab-created sapphire (incl. white sapphire).",
   patterns=[r"^(?!.*alpha sapphire)(?=.*\bsapphires?\b)(?!.*(moissanite|hardness))"], prio=9)
cl("CL-101", "Emerald: Natural & Lab-Grown", P_GEM, A_GEM, M, [I, T, CR],
   "Natural and lab-grown emerald. Stage 8: 'natural emerald' MIXED/LOW.",
   patterns=[r"\bemeralds?\b(?!.*(cut|asscher))"], prio=9)
cl("CL-102", "Lab-Created Gemstones (General & Other Stones)", P_GEM, A_GEM, M, [I, T],
   "Lab-created gemstones in general and specific lab stones (ruby, opal, quartz, alexandrite, topaz).",
   patterns=[r"^lab (grown|created) (gemstones?|gem|colored stones|quartz|opal|black opal|ruby|alexandrite rings)", r"^lab gemstones$", r"^topaz lab$", r"^lab grown (gem|gemstone|gemstones|opal|opal rough|ruby|quartz)", r"^can opals be lab grown$", r"^lab created alexandrite rings$"], prio=9)
cl("CL-103", "Natural Gemstones & Stones (Opal, Jade, Pearls & Others)", P_GEM, A_GEM, M, [I, T],
   "Natural gemstone identification/shopping for stones other than diamond, sapphire, emerald and moissanite.",
   patterns=[r"^(natural|real) (opal|jade|pearls?|topaz|amethyst|citrine|alexandrite|gemstones?|peridot|ruby|moonstone|garnet)", r"^natural gemstone company$", r"^garnet natural$", r"^real natural pearl$", r"^natural alexandrite stone$",
             r"^natural (citrine|jade|opal|topaz|amethyst) ?(stone)?$", r"^natural peridot ring$", r"^natural ruby gemstone$", r"^real (jade|moonstone)$", r"^emerald natural stone$"], prio=75)
cl("CL-104", "Morganite Rings & Jewellery", P_GEM, A_GEM, T, [CR, I],
   "Morganite ring/jewellery demand (8,100). Stage 8: 'morganite rings' is a CATEGORY SERP (HIGH).",
   patterns=[r"\bmorganite\b(?!.*moissanite)"], prio=7)
cl("CL-105", "Coloured Gemstone Rings & Jewellery (Tanzanite, Moldavite & Others)", P_GEM, A_GEM, T, [CR, I],
   "Ring/jewellery queries for specific coloured or unusual gemstones.",
   patterns=[r"^(tanzanite (rings|diamonds)|moldavite ring|ammolite ring|chrome diopside ring|iolite jewelry|rhodochrosite ring|turquoise diamond|spinel diamonds|jade diamond|opal diamond|fordite rings|meteorite diamonds|gemstone rings)$"], prio=77)

# ---- Metals ----
cl("CL-110", "Gold Karat: 14K vs 18K (and 10K)", P_MET, A_MET, CR, [I],
   "Gold purity choice and value: 14K vs 18K, is 14K good, 10K worth. Stage 8: the two 14K-vs-18K variants share 7 URLs; HOD holds Stage 3 rankings for this family.",
   patterns=[r"\b(14k|18k|10k|14 kt|10 kt)\b", r"^10 kt rings$", r"^is 14k diamond good$"], prio=29)
cl("CL-111", "Rhodium Plating & Replating Rings", P_MET, A_MET, I, [T, CR],
   "Rhodium plating and re-plating/dipping rings in white or yellow gold. Stage 8: 'rhodium plating ring' editorial; 'rhodium ring' UNCLEAR/OTHER.",
   patterns=[r"\brhodium\b", r"^can you (dip|replate)", r"^can white gold ring be changed to yellow gold$", r"^can you dip a"], prio=16)
cl("CL-112", "Jewellery Metals: Types, Best Metal & Mixing", P_MET, A_MET, I, [CR],
   "Which metal to choose, types of jewellery metals and alloys, hypoallergenic metals, sterling silver, mixing gold and silver.",
   patterns=[r"^(best metal for rings|types of metals for rings|types of jewelry metals|jewelry alloys|hypoallergenic jewelry metals|can a diamond be set in sterling silver|can you wear silver bracelet with gold necklace|is a sterling silver ring worth anything|is 6 ice jewelry real|is rose gold good for engagement rings|is a 10k gold ring worth anything|diamond metals)$"], prio=63)
cl("CL-113", "Tungsten & Titanium Wedding Bands", P_MET, A_MET, I, [CR, T],
   "Suitability of tungsten/titanium/alternative metals for wedding bands. Stage 8: 'is tungsten/titanium good for wedding bands' editorial (HIGH) but the two SERPs share 0 URLs.",
   patterns=[r"^is (tungsten|titanium) good for wedding bands$", r"^tungsten promise rings?$", r"^do iridium bands stack$", r"^iridium bands$"], prio=64)
cl("CL-114", "Alternative Material & Novelty Rings (Cobalt, Tantalum, Uranium, Glow & Others)", P_MET, A_MET, T, [I],
   "Rings/jewellery in unusual metals or novelty materials.",
   patterns=[r"^(cobalt|tantalum|osmium|rhenium|zinc|uranium|hematite|ferrite|pyrite) rings?$", r"^uranium glass ring$", r"^(strontium aluminate ring|tritium jewelry|molecule jewelry|mineralogy jewelry|mineral bands|carbon glow rings|alloy ring)$"], prio=65, ambiguous_ok=True)
cl("CL-115", "Jewellery Tarnish, Water & Everyday Wear", P_MET, A_MET, I, [],
   "Will jewellery tarnish, go green, tolerate showers/water, rust; wearing engagement rings and diamond jewellery daily.",
   patterns=[r"\b(tarnish|waterproof|turn your finger green|shower|rust|wet)\b", r"^do you wear engagement ring everyday$"], prio=13)

# ---- Rings / settings / earrings ----
cl("CL-120", "Side-Stone Engagement Rings", P_RING, A_ER, T, [CR],
   "Side-stone engagement ring category demand. Stage 8: CATEGORY SERP (HIGH); HOD holds a Stage 3 ranking on a category page.",
   patterns=[r"^side stones? engagement rings$"], prio=13)
cl("CL-121", "Diamond Ring Setting Types", P_RING, A_ER, I, [CR],
   "Types of diamond settings, setting height/pressure setting, ring enhancers. Stage 8: 'types of diamond settings' editorial (HIGH).",
   patterns=[r"\b(settings?|setting|enhancers?|milgrain)\b", r"^do (real )?diamonds (need holes to breathe|have breathing holes)$", r"^does halo make diamond look bigger$"], prio=78)
cl("CL-122", "Engagement Ring Buying Questions (Returns, Wearing & Alternatives)", P_RING, A_ER, I, [CR],
   "Practical engagement-ring questions: returns, whether rings need a diamond, men's engagement rings.",
   patterns=[r"^(can engagement rings be returned|can you return an engagement ring|do engagement rings have to be diamond|do men get engagement rings too)$"], prio=79)
cl("CL-123", "Mixed Metal Rings", P_RING, A_MET, T, [CR],
   "Mixed-metal ring shopping. Stage 8: CATEGORY SERP (HIGH); Stage 5 area was Engagement Rings, cluster placed under Materials/Metals by subject.",
   patterns=[r"^mixed metal rings?$"], prio=80)
cl("CL-124", "Ring Sizing & Resizing", P_RING, A_ER, I, [T],
   "Ring size, resizing and removal questions (men's vs women's sizes, resizing metals, band thickness).",
   patterns=[r"\bresized?\b", r"^can you make a ring smaller$", r"^are mens and womens ring sizes the same$", r"^ring band thickness$", r"^can titanium rings be cut off$", r"^where can i get my ring resized$"], prio=81)
cl("CL-125", "Diamond Stud Earrings", P_RING, A_EAR, M, [I, T, CR],
   "Diamond stud earring queries: lab-diamond studs, stud settings/sizes, converting earrings.",
   patterns=[r"\b(earrings?|studs?)\b"], prio=14)

cl("CL-087", "Cutting, Recutting & Reshaping Diamonds", P_SCI, A_EDU, I, [],
   "Whether a diamond can be cut, recut or reshaped, by a jeweler or by other means.",
   patterns=[r"^can (you|a jeweler) (cut|recut|reshape) (a )?diamonds?$", r"^can (you cut diamond with water|water cut diamonds)$", r"^can a jeweler cut a diamond$"], prio=66, ambiguous_ok=True)
cl("CL-088", "Diamond Facets, Refraction & Optics", P_SCI, A_EDU, I, [],
   "How diamond facets and light refraction work.",
   patterns=[r"^diamond (facet|refraction|surfaces)$"], prio=67, ambiguous_ok=True)
cl("CL-089", "Treated & Enhanced Diamonds (Irradiation, Post-Growth Treatment)", P_SCI, A_4C, I, [CR],
   "Diamond treatments: irradiation, clarity enhancement, post-growth treatment.",
   patterns=[r"^irradiated diamonds$", r"^diamond post growth treatment$", r"^should i buy clarity enhanced diamonds$"], prio=34, ambiguous_ok=True)


# Keywords forced to UNCLUSTERED_REVIEW where SERP/semantic evidence shows dual meaning (evidence text recorded).
FORCE_REVIEW = {
    "asl diamond shape": "Stage 5 strategic seed, but the query appears to be about a sign-language handshape or geometry, not jewellery; meaning unverified",
    "is kite a diamond shape": "Stage 5 strategic seed, but the query appears to be a geometry question, not jewellery; meaning unverified",
    "diamond stone": "Stage 8 SERP mixes an NBA player (basketball-reference/ESPN), sharpening stones and GIA: dual meaning, SERP overrides wording",
    "diamond rust": "Likely the game 'Rust' or a non-jewellery meaning; question forms ('do diamonds rust') are clustered instead",
    "cut alpha sapphire": "Meaning unclear (not a standard jewellery term)",
    "diamond crystal": "Dual meaning (Diamond Crystal salt brand vs crystalline diamond); no SERP evidence",
    "rough impact diamonds": "Meaning unclear (impact/meteorite diamond vs game term); no SERP evidence",
    "impact diamonds": "Meaning unclear (impact/meteorite diamond vs game term); no SERP evidence",
    "lab grown diamond corp": "Possible company name; not verified as a brand",
}
