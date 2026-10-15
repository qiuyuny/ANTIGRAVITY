# -*- coding: utf-8 -*-
"""
MAST20026 Real Analysis
Open-Book / Reference Cheat Sheet & Proof Manual (Spec Edition)
Part I: Visual Topic Tree Index | Part II: Axioms, Proof Templates, Counterexamples & Convergence Matrices
"""

import shutil
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted,
    HRFlowable, PageBreak, Table, TableStyle
)
from reportlab.lib import colors

pdfmetrics.registerFont(TTFont('SegoeUI', 'C:/Windows/Fonts/segoeui.ttf'))
pdfmetrics.registerFont(TTFont('SegoeUIBold', 'C:/Windows/Fonts/segoeuib.ttf'))
pdfmetrics.registerFont(TTFont('Consolas', 'C:/Windows/Fonts/consola.ttf'))
pdfmetrics.registerFont(TTFont('ConsolasBold', 'C:/Windows/Fonts/consolab.ttf'))

title_style = ParagraphStyle(
    'TitleStyle', fontName='SegoeUIBold', fontSize=14.5, leading=19,
    textColor=colors.black, spaceAfter=3
)
sub_style = ParagraphStyle(
    'SubStyle', fontName='Consolas', fontSize=8.8, leading=11.5,
    textColor=colors.HexColor('#333333'), spaceAfter=7
)
h2_style = ParagraphStyle(
    'H2Style', fontName='SegoeUIBold', fontSize=10.8, leading=14,
    textColor=colors.white, backColor=colors.black,
    borderPadding=(4, 6, 4, 6), spaceBefore=10, spaceAfter=5
)
h3_style = ParagraphStyle(
    'H3Style', fontName='SegoeUIBold', fontSize=9.6, leading=12.8,
    textColor=colors.black, backColor=colors.HexColor('#E8E8E8'),
    borderPadding=(2, 4, 2, 4), spaceBefore=7, spaceAfter=4
)
code_style = ParagraphStyle(
    'CodeStyle', fontName='Consolas', fontSize=7.7, leading=10.0,
    textColor=colors.black, backColor=colors.HexColor('#F6F6F6'),
    borderPadding=4.5, leftIndent=4, rightIndent=4, spaceBefore=2, spaceAfter=4
)
tree_style = ParagraphStyle(
    'TreeStyle', fontName='Consolas', fontSize=7.9, leading=10.2,
    textColor=colors.black
)
th_style = ParagraphStyle(
    'THStyle', fontName='SegoeUIBold', fontSize=8.3, leading=10.8,
    textColor=colors.black
)
td_text_style = ParagraphStyle(
    'TDTextStyle', fontName='SegoeUI', fontSize=8.1, leading=10.8,
    textColor=colors.black
)

def clean_and_esc(s):
    replacements = [
        ('⌊', 'floor('), ('⌋', ')'), ('⌈', 'ceil('), ('⌉', ')'),
        ('⇔', ' iff '), ('⟺', ' iff '), ('⟹', ' => '), ('⇒', ' => '),
        ('∀', 'for all '), ('∃', 'there exists '),
        ('∈', ' in '), ('∉', ' not in '), ('⊆', ' subset of '), ('⊂', ' subset of '),
        ('≤', '<='), ('≥', '>='), ('→', '->'), ('≠', '!='), ('∖', '\\'),
        ('∞', 'inf'), ('∑', 'sum'), ('∫', 'int'), ('√', 'sqrt'),
        ('ε', 'eps'), ('δ', 'delta'), ('α', 'alpha'), ('β', 'beta'), ('ρ', 'rho'),
        ('⁰', '^0'), ('¹', '^1'), ('²', '^2'), ('³', '^3'), ('⁴', '^4'), ('ⁿ', '^n'),
        ('₀', '_0'), ('₁', '_1'), ('₂', '_2'), ('₃', '_3'), ('ₙ', '_n'), ('ₖ', '_k')
    ]
    s = str(s)
    for k, v in replacements:
        s = s.replace(k, v)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = s.replace("&lt;br/&gt;", "<br/>").replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
    s = s.replace("\n", "<br/>")
    return s

def make_table(headers, rows, col_widths=None):
    data = [[Paragraph(clean_and_esc(h), th_style) for h in headers]]
    for r in rows:
        data.append([Paragraph(clean_and_esc(c), td_text_style) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DFDFDF')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 0.6, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.2),
        ('LEFTPADDING', (0, 0), (-1, -1), 4.5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4.5),
    ]))
    return t

TREE_TEXT = """[!!!] = Core / Must-know    [!! ] = Important / Frequent    [!  ] = Basic / Edge case

[0.0] MAST20026 REAL ANALYSIS — COMPLETE EXAM SYLLABUS
│
├── [1.0] Logic, Propositional Calculus & Axioms of Real Numbers
│   ├── [1.1] Propositional Logic & Truth Tables (Always Q1!)
│   │   ├── [1.1.1] Connectives (~, ^, v, =>, <=>) & Vacuous Truth       [!!!]
│   │   ├── [1.1.2] 4-Row Truth Table construction & row deduction       [!!!]
│   │   ├── [1.1.3] Equivalent single-connective statement matching      [!!!]
│   │   └── [1.1.4] Quantifier negation (forall <-> exists) & contrapos. [!! ]
│   │
│   └── [1.2] Field & Order Axioms of R (Always Q2!)
│       ├── [1.2.1] Addition Axioms (A1-A5) & Multiplication (M1-M5, D)  [!!!]
│       ├── [1.2.2] Order Axioms (O1-O2, OA, OM) & Completeness (C)      [!!!]
│       └── [1.2.3] Line-by-line formal axiom cancellation/zero proofs   [!!!]
│
├── [2.0] Completeness, Supremum / Infimum & Topology of R
│   ├── [2.1] Upper/Lower Bounds, Supremum & Infimum (Always Q3!)
│   │   ├── [2.1.1] Upper bound definition & Least Upper Bound (sup)     [!!!]
│   │   ├── [2.1.2] Analytic eps-characterization of sup S (x > sup S-e) [!!!]
│   │   └── [2.1.3] Proofs of sup(A+B) = sup A + sup B & sup(kA)=k sup A [!!!]
│   │
│   └── [2.2] Limit Points (Accumulation Points) & Density
│       ├── [2.2.1] Limit point definition: (L-eps, L+eps) \\ {L} != empty[!!!]
│       ├── [2.2.2] Constructing sets with specific limit point sets     [!!!]
│       └── [2.2.3] Archimedean Property & Density of Q and R\\Q in R     [!!!]
│
├── [3.0] Sequences of Real Numbers
│   ├── [3.1] Formal Sequence Convergence & Limit Laws
│   │   ├── [3.1.1] Formal eps-N limit definition & proof template       [!!!]
│   │   ├── [3.1.2] Squeeze Theorem & algebra of limits                  [!! ]
│   │   └── [3.1.3] Divergent sequence counterexample construction (Q4)  [!!!]
│   │
│   └── [3.2] Recursive Sequences, MCT & Cauchy Sequences (Always Q5!)
│       ├── [3.2.1] Principle of Mathematical Induction (PMI) boundedness[!!!]
│       ├── [3.2.2] Monotonicity via difference factoring (x_{n+1}-x_n)  [!!!]
│       ├── [3.2.3] Monotone Convergence Theorem (MCT) & Fixed-Point L   [!!!]
│       └── [3.2.4] Subsequences, Bolzano-Weierstrass & Cauchy equivalence[!!!]
│
├── [4.0] Limits of Functions, Continuity & Differentiation
│   ├── [4.1] Formal Function Limits & Continuity (Always Q6!)
│   │   ├── [4.1.1] Formal eps-delta & eps-M (x -> inf) limit proofs     [!!!]
│   │   ├── [4.1.2] Discontinuity negation proof at jump/split point     [!!!]
│   │   └── [4.1.3] Sequential characterization of continuity            [!! ]
│   │
│   ├── [4.2] Global Continuity Theorems on [a, b]
│   │   ├── [4.2.1] Intermediate Value Theorem (IVT) root existence      [!! ]
│   │   └── [4.2.2] Extreme Value Theorem (EVT) & Uniform Continuity     [!! ]
│   │
│   └── [4.3] Differentiability, Mean Value Theorem & Taylor's Theorem
│       ├── [4.3.1] First-principles derivative & Rolle's / MVT          [!! ]
│       └── [4.3.2] Taylor polynomial T_k(x) & Lagrange Remainder bound  [!!!]
│
├── [5.0] Riemann Integration & Darboux Sums (Always Q7!)
│   ├── [5.1] Partitions, Lower Sums L(f,P) & Upper Sums U(f,P)
│   │   ├── [5.1.1] Explicit calculation of L(f,P) & U(f,P) on partition [!!!]
│   │   └── [5.1.2] Upper Integral vs Lower Integral & Integrability     [!!!]
│   │
│   └── [5.2] Rational / Irrational Split (Dirichlet-Type) Functions
│       ├── [5.2.1] Density of Q and R\\Q on arbitrary partition P        [!!!]
│       ├── [5.2.2] Bounding Upper Integral > Lower Integral (Non-integ.)[!!!]
│       └── [5.2.3] Fundamental Theorem of Calculus (FTC Parts 1 & 2)    [!! ]
│
└── [6.0] Infinite Series, Power Series & Sequences of Functions (Q8 & Q9!)
    ├── [6.1] Convergence Tests for Infinite Series (Always Q8a!)
    │   ├── [6.1.1] Divergence Test, Geometric Series & p-Series Test    [!!!]
    │   ├── [6.1.2] Direct Comparison Test & Ratio Test                  [!!!]
    │   └── [6.1.3] Alternating Series Test (AST) & Absolute Convergence [!!!]
    │
    ├── [6.2] Power Series & Radius/Interval of Convergence (Always Q8b!)
    │   ├── [6.2.1] Ratio formula for Radius of Convergence R            [!!!]
    │   └── [6.2.2] Endpoint testing at x = -R and x = +R                [!!!]
    │
    └── [6.3] Pointwise vs Uniform Convergence of Function Sequences (Q9b!)
        ├── [6.3.1] Pointwise limit f(x) = lim_{n->inf} f_n(x)           [!!!]
        ├── [6.3.2] Supremum norm M_n = sup |f_n(x) - f(x)| -> 0 proof   [!!!]
        └── [6.3.3] Preservation of continuity/integrals & Weierstrass M [!! ]"""

def build_pdf(target_path):
    doc = SimpleDocTemplate(
        target_path, pagesize=A4,
        leftMargin=26, rightMargin=26, topMargin=24, bottomMargin=24
    )
    W = A4[0] - 52
    s = []

    s.append(Paragraph("MAST20026 REAL ANALYSIS EXAM CHEAT SHEET & REFERENCE MANUAL", title_style))
    s.append(Paragraph("Part I: Visual Topic Tree Index  |  Part II: Axioms, Proof Templates, Counterexamples & Convergence Matrices", sub_style))
    s.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceAfter=6))

    # Scope Table
    s.append(make_table(
        ["IN-SCOPE (Core 9-Question Exam Blueprint)", "OUT-OF-SCOPE (Never Tested / Avoid Wasting Time)"],
        [[
            "• Q1: Truth Tables, Logical Deduction & Equivalent Connective<br/>"
            "• Q2: Step-by-step Formal Proof from Field/Order Axioms of R<br/>"
            "• Q3: Upper Bounds & Supremum Proofs (sup(A+B), sup(kA))<br/>"
            "• Q4: Constructing Specific Counterexamples (Limit points, Sequences)<br/>"
            "• Q5: Recursive Sequence Induction, Monotonicity, MCT & Cauchy<br/>"
            "• Q6: Formal eps-M / eps-delta Limit & Discontinuity Negation Proof<br/>"
            "• Q7: Riemann Sums L(f,P), U(f,P) & Q / (R\\Q) Non-Integrability<br/>"
            "• Q8: Infinite Series Tests (Comparison, AST, Ratio) & Power Series R<br/>"
            "• Q9: Taylor Polynomial Lagrange Remainder & Uniform Convergence",
            "• Metric Spaces, General Topological Spaces or Open Ball Topologies<br/>"
            "• Lebesgue Measure, Lebesgue Integration or Fourier Series<br/>"
            "• Multivariable Calculus, Partial Derivatives or Multiple Integrals<br/>"
            "• Complex Analysis or Contour Integration<br/>"
            "• Memorizing Axiom Numbers (Axioms A1-M5, O1-OM are printed on Q2!)<br/>"
            "• Using eps-N proofs inside Q8 Series questions (explicitly exempted)"
        ]],
        col_widths=[W*0.54, W*0.46]
    ))
    s.append(Spacer(1, 5))

    s.append(Paragraph("PART I · VISUAL TOPIC TREE INDEX", h2_style))
    s.append(Preformatted(TREE_TEXT, tree_style))

    s.append(PageBreak())
    s.append(Paragraph("PART II · REFERENCE TABLES, AXIOMS & STEP-BY-STEP PROOF TEMPLATES", h2_style))

    # ================= MODULE 1 =================
    s.append(Paragraph("[1.0] Logic, Truth Tables (Q1) & Axioms of the Real Numbers (Q2)", h3_style))
    s.append(make_table(
        ["Index & Topic", "Core Rule / Axiom Table", "Exam Scoring Requirement & Pitfalls"],
        [
            ["[1.1.1] Connectives &\nImplication Rule", "• ~p (NOT)  |  p ^ q (AND: true iff both T)  |  p v q (OR: false iff both F)\n• p => q (IMPLIES): FALSE ONLY WHEN p = T and q = F!\n  Whenever p = F, (p => q) is automatically TRUE (Vacuous Truth)!", "Standard 4 rows for (p, q): (T,T), (T,F), (F,T), (F,F).\nLogical Equivalence: p => q  <=>  (~p) v q  <=>  (~q) => (~p)\nNegation of (p => q) is: p ^ (~q)"],
            ["[1.1.2] Q1(b) & Q1(c)\nJustification Rules", "• Q1(b): Cross-check rows where given premises are T; state exact line numbers (e.g. 'Only Line 2 and Line 4 have q = F, and Line 2 has compound = F, so by Line 4, p must be F').", "• Q1(c): Compare final truth column against standard 1-connective columns: p => q (T,F,T,T), q => p (T,T,F,T), p ^ q (T,F,F,F), p v q (T,T,T,F), ~p, ~q."],
            ["[1.2.1] Field Axioms\n(Printed on Exam Q2)", "• A1/M1 (Closure): x+y in R, xy in R\n• A2/M2 (Commutative): x+y = y+x  |  xy = yx\n• A3/M3 (Associative): (x+y)+z = x+(y+z)  |  (xy)z = x(yz)", "• A4/M4 (Identity): x + 0 = x  |  1 * x = x\n• A5/M5 (Inverse): exists (-x) s.t. x+(-x)=0  |  for x!=0, exists 1/x s.t. x*(1/x)=1\n• D (Distributive): x(y + z) = xy + xz"],
            ["[1.2.2] Order Axioms", "• O1 (Trichotomy): exactly one of x < y, y < x, x = y holds\n• O2 (Transitivity): x < y and y < z => x < z", "• OA (Order-Add): x < y => x + z < y + z\n• OM (Order-Mult): x > 0 and y > 0 => xy > 0"]
        ],
        col_widths=[W*0.22, W*0.42, W*0.36]
    ))
    s.append(Spacer(1, 3))
    s.append(Preformatted(
"""/* [1.2.3] Q2 Formal Axiom Proof Template 1: Cancellation Law (Assume a + b = a + c, prove b = c) */
1. Since a in R, by Axiom A5 there exists (-a) in R such that a + (-a) = 0.
2. Since a + b = a + c, adding (-a) to both sides gives: (-a) + (a + b) = (-a) + (a + c).   [Substitution]
3. By Axiom A3 (Associativity):   ((-a) + a) + b = ((-a) + a) + c.
4. By Axiom A2 (Commutativity):   (a + (-a)) + b = (a + (-a)) + c.
5. By Step 1 (Axiom A5):          0 + b = 0 + c.
6. By Axiom A2 and Axiom A4 (Additive Identity x + 0 = x):  b = c.  [Q.E.D.]""", code_style))

    # ================= MODULE 2 =================
    s.append(Paragraph("[2.0] Completeness, Supremum Proofs (Q3) & Counterexample Bank (Q4)", h3_style))
    s.append(make_table(
        ["Index & Concept", "Formal Definition / Characterization", "Exam Proof Strategy"],
        [
            ["[2.1.1] Upper Bound\n& Supremum (sup S)", "• alpha is an Upper Bound of S  <=>  for all x in S, x <= alpha.\n• alpha = sup S (Least Upper Bound) iff:\n  (1) alpha is an upper bound of S, AND\n  (2) For any upper bound M of S, alpha <= M.", "• Golden Trick to prove sup S <= M:\n  Simply prove that M is an upper bound of S! Then since sup S is the LEAST upper bound, sup S <= M follows immediately!"],
            ["[2.1.2] Analytic eps-\nCharacterization", "Assume alpha is an upper bound of S. Then:\nalpha = sup S  <=>  for all eps > 0, there exists x in S such that x > alpha - eps.", "Use this when proving sup(kA) = k sup A (with k > 0): let eps > 0, since sup A - eps/k is not an upper bound of A, pick x in A with x > sup A - eps/k, multiply by k!"],
            ["[2.2.1] Limit Point\n(Accumulation Point)", "L in R is a limit point of subset E subset of R iff:\nFor every eps > 0, ((L - eps, L + eps) \\ {L}) intersect E != empty.\n(Equivalently: there exists a sequence x_n in E \\ {L} with lim x_n = L).", "• Finite sets have NO limit points (limit point set = empty).\n• Limit point of {1/n : n in N+} is {0}.\n• Limit point of {2 + 1/n : n in N+} is the single-element set {2}."]
        ],
        col_widths=[W*0.22, W*0.42, W*0.36]
    ))
    s.append(Spacer(1, 3))
    s.append(make_table(
        ["[2.2.2 / 3.1.3] Q4 High-Frequency Exam Prompt ('Provide a specific example...')", "Ready-to-Write Concrete Example & 1-Line Justification"],
        [
            ["1. Infinite subset E subset of R whose set of limit points is {c} (e.g. {2})", "Let E = { 2 + 1/n : n in N+ }. Since lim_{n->inf} (2 + 1/n) = 2 with terms distinct from 2, 2 is the unique limit point."],
            ["2. Infinite subset E subset of R whose set of limit points is {a, b} (e.g. {0, 1})", "Let E = { 1/n : n in N+ } union { 1 + 1/n : n in N+ }. The two subsequences accumulate at 0 and 1 respectively."],
            ["3. Sequence (a_n) where (a_n)^2 converges to K (e.g. 16), but (a_n) diverges", "Let a_n = 4 * (-1)^n. Then (a_n)^2 = 16 -> 16 (converges), while a_n alternates between -4 and 4 (diverges)."],
            ["4. Two divergent sequences (x_n), (y_n) whose sum (x_n + y_n) converges to L (e.g. 3)", "Let x_n = 3 + (-1)^n and y_n = -(-1)^n. Both oscillate and diverge, but x_n + y_n = 3 -> 3 (converges)."],
            ["5. Two divergent sequences (x_n), (y_n) whose product (x_n * y_n) converges to 1", "Let x_n = (-1)^n and y_n = (-1)^n. Both diverge, but x_n * y_n = ((-1)^n)^2 = 1 -> 1."],
            ["6. Bounded sequence that diverges (not Cauchy) but has convergent subsequences", "Let x_n = (-1)^n. Bounded in [-1, 1], diverges; even subsequence x_{2k} = 1 -> 1, odd x_{2k-1} = -1 -> -1."],
            ["7. Decreasing sequence of positive terms a_n -> 0 whose series sum a_n DIVERGES", "Let a_n = 1/n (Harmonic series) or a_n = 1/sqrt(n). Here a_n -> 0, but sum_{n=1}^inf (1/n) diverges (p = 1 <= 1)."]
        ],
        col_widths=[W*0.48, W*0.52]
    ))

    s.append(PageBreak())

    # ================= MODULE 3 =================
    s.append(Paragraph("[3.0] Sequences: Formal eps-N Proofs & Recursive MCT / Cauchy (Q5)", h3_style))
    s.append(Preformatted(
"""/* [3.1.1] Formal eps-N Sequence Limit Proof Template: Prove lim_{n->inf} (2n + 1)/(n + 3) = 2 */
[Scratch Work]: |(2n+1)/(n+3) - 2| = |(2n+1 - 2n - 6)/(n+3)| = 5/(n+3) < 5/n. Want 5/n < eps <=> n > 5/eps.
[Formal Proof]: Let eps > 0 be given. Choose N = ceil(5 / eps) (or by Archimedean property, pick N in N+ with N > 5/eps).
                Then for all n > N, we have:
                    |(2n + 1)/(n + 3) - 2| = |-5| / (n + 3) = 5 / (n + 3) < 5 / n < 5 / N <= 5 / (5 / eps) = eps.
                Therefore, by definition of the limit, lim_{n->inf} (2n + 1)/(n + 3) = 2.  [Q.E.D.]""", code_style))
    s.append(Spacer(1, 3))
    s.append(make_table(
        ["[3.2] Q5 Recursive Sequence 3-Part Blueprint (13 Marks)", "Exact Step-by-Step Write-Up & Formula"],
        [
            ["Part (a): Boundedness by Induction [5 marks]\nProve a <= x_n < b for all n in N+\n(e.g. x_1 = 0, x_{n+1} = 9/(6 - x_n), prove 0 <= x_n < 3)",
             "1. Base Case (n = 1): State x_1 = 0, which clearly satisfies 0 <= 0 < 3. Thus true for n = 1.\n"
             "2. Inductive Hypothesis: Suppose 0 <= x_k < 3 holds for some k in N+.\n"
             "3. Inductive Step (n = k + 1): Chain inequalities from IH: 0 <= x_k < 3  =>  -3 < -x_k <= 0  =>  3 < 6 - x_k <= 6\n"
             "   =>  1/6 <= 1/(6 - x_k) < 1/3  =>  9/6 <= 9/(6 - x_k) < 9/3  =>  0 <= 1.5 <= x_{k+1} < 3.\n"
             "4. Mandatory Closing Sentence: 'By the Principle of Mathematical Induction, 0 <= x_n < 3 holds for all n in N+.'"],
            ["Part (b): Monotonicity [4-5 marks]\nCompute x_{n+1} - x_n and determine sign",
             "1. Combine over common denominator: x_{n+1} - x_n = 9/(6 - x_n) - x_n = (9 - 6x_n + x_n^2)/(6 - x_n) = (x_n - 3)^2 / (6 - x_n).\n"
             "2. Analyze signs using Part (a) bound (0 <= x_n < 3): Since x_n != 3, numerator (x_n - 3)^2 > 0; denominator 6 - x_n > 3 > 0.\n"
             "3. Conclusion: Since x_{n+1} - x_n > 0 for all n in N+, (x_n) is strictly monotone increasing!"],
            ["Part (c): Cauchy & Limit L [3-4 marks]\nIs (x_n) Cauchy? Find lim x_n",
             "1. MCT: Since (x_n) is monotone increasing and bounded above by 3, by the Monotone Convergence Theorem (MCT), (x_n) converges to some limit L in R.\n"
             "2. Cauchy: Since every convergent sequence in R is a Cauchy sequence, YES, (x_n) is Cauchy.\n"
             "3. Fixed-Point Limit: Taking n -> inf on both sides of x_{n+1} = 9/(6 - x_n) gives L = 9/(6 - L) => L^2 - 6L + 9 = 0 => (L - 3)^2 = 0 => L = 3."]
        ],
        col_widths=[W*0.32, W*0.68]
    ))

    # ================= MODULE 4 =================
    s.append(Paragraph("[4.0] Function Limits, Discontinuity (Q6) & Taylor's Theorem (Q9a)", h3_style))
    s.append(make_table(
        ["Index & Proof Type", "Formal Quantifier Definition", "Exam Template & Selection Rule"],
        [
            ["[4.1.1] Limit as x -> inf\n(eps-M Proof, Q6a)", "lim_{x->inf} f(x) = L  <=>\nfor all eps > 0, there exists M in R such that for all x > M, |f(x) - L| < eps.", "For piecewise f(x) = 2x/(x+1) when x >= 1 (prove lim = 2):\n• Simplify |2x/(x+1) - 2| = 2/(x+1) < 2/x < eps <=> x > 2/eps.\n• Choose M = max{1, 2/eps} (ensures x > 1 branch AND 2/x < eps)!"],
            ["[4.1.1] Limit as x -> a\n(eps-delta Proof)", "lim_{x->a} f(x) = L  <=>\nfor all eps > 0, there exists delta > 0 s.t. 0 < |x - a| < delta => |f(x) - L| < eps.", "For nonlinear polynomial (e.g. x^2 near a = 3): factor |x^2 - 9| = |x - 3||x + 3|.\nRestrict delta <= 1 first so |x - 3| < 1 => 2 < x < 4 => |x + 3| < 7. Then choose delta = min{1, eps / 7}!"],
            ["[4.1.2] Discontinuity at x = a\n(Negation Proof, Q6b)", "f is NOT continuous at x = a  <=>\nthere exists eps_0 > 0 such that for all delta > 0, there exists x in R with |x - a| < delta AND |f(x) - f(a)| >= eps_0.", "For piecewise jump at a = 1 (e.g. f(x) = 3x - 5 for x < 1, and f(1) = 1):\n1. Left limit is 3(1)-5 = -2; f(1) = 1. Jump gap = |1 - (-2)| = 3.\n2. Pick concrete eps_0 = 1 (or 1/2). Let arbitrary delta > 0 be given.\n3. Pick x = 1 - min{delta/2, 1/2} < 1. Then |x - 1| < delta, and f(x) = 3x - 5 < -2, so |f(x) - f(1)| = 1 - (3x - 5) = 6 - 3x > 3 > eps_0 = 1!"],
            ["[4.3.2] Taylor's Theorem\n& Lagrange Remainder (Q9a)", "T_k(x) = sum_{m=0}^k [f^(m)(a) / m!] (x - a)^m\nRemainder: R_k(x) = f(x) - T_k(x) = [f^(k+1)(c) / (k+1)!] (x - a)^(k+1)\nfor some c strictly between a and x.", "Example (g(x) = cos(x) - 1 at a = 0, degree k = 3):\n• g(0)=0, g'(0)=0, g''(0)=-1, g'''(0)=0 => T_3(x) = -x^2 / 2.\n• (k+1)=4th derivative: g^(4)(c) = cos(c). Since |cos(c)| <= 1 for all c in R,\n  |g(x) - T_3(x)| = |cos(c) / 4!| |x|^4 <= |x|^4 / 24 = x^4 / 24."]
        ],
        col_widths=[W*0.23, W*0.36, W*0.41]
    ))

    s.append(PageBreak())

    # ================= MODULE 5 =================
    s.append(Paragraph("[5.0] Riemann Integration, Darboux Sums & Dirichlet Non-Integrability (Q7)", h3_style))
    s.append(make_table(
        ["[5.1 / 5.2] Q7 3-Part Exam Blueprint (13 Marks)", "Formulas, Density Citation & Full-Mark Justification"],
        [
            ["Part (a): Concrete Partition Calculation [4 marks]\nGiven g(x) on [a, b] and explicit partition P = {x_0, x_1, ..., x_n}, compute L(g, P) and U(g, P)",
             "• Subinterval i is I_i = [x_{i-1}, x_i] with width Delta x_i = x_i - x_{i-1}.\n"
             "• m_i = inf_{x in I_i} g(x)   and   M_i = sup_{x in I_i} g(x).\n"
             "  (If g is increasing on I_i: m_i = g(x_{i-1}), M_i = g(x_i). If decreasing: m_i = g(x_i), M_i = g(x_{i-1})).\n"
             "• Lower Sum: L(g, P) = sum_{i=1}^n m_i * Delta x_i     |     Upper Sum: U(g, P) = sum_{i=1}^n M_i * Delta x_i."],
            ["Part (b): Arbitrary Partition on Q vs R\\Q Function [4 marks]\nLet f(x) = { h(x) >= 0 if x in Q ;  0 if x not in Q } on [0, 2].\nCompute L(f, P) for ANY partition P = {x_0, ..., x_n}",
             "1. Cite Density of Irrationals: 'By the density of the irrationals (R \\ Q) in R, every subinterval [x_{i-1}, x_i] contains at least one irrational number x, where f(x) = 0.'\n"
             "2. Since f(x) >= 0 everywhere on [0, 2], we have m_i = inf_{x in [x_{i-1}, x_i]} f(x) = 0 for every i = 1, ..., n.\n"
             "3. Therefore, L(f, P) = sum_{i=1}^n 0 * (x_i - x_{i-1}) = 0. Consequently, the Lower Riemann Integral is sup_P L(f, P) = 0!"],
            ["Part (c): Positive Lower Bound on Upper Integral & Non-Integrability [5 marks]\nFor f(x) = { 4 - x^2 if x in Q ; 0 if x not in Q } on [0, 2],\nbound Upper Integral > 0 and prove f is NOT integrable",
             "1. Cite Density of Rationals: By the density of Q in R, on any subinterval inside [0, 1], M_i = sup f(x) >= inf_{x in [0,1] intersect Q} (4 - x^2) = 4 - 1^2 = 3.\n"
             "   (Or simpler: for any partition P, let P' = P union {1}. On [0, 1], since 4 - x^2 >= 3 on Q, every subinterval of P' in [0, 1] has M_i >= 3, so U(f, P) >= U(f, P') >= 3 * (1 - 0) = 3 > 0).\n"
             "2. Thus the Upper Riemann Integral satisfies inf_P U(f, P) >= 3 > 0.\n"
             "3. Since Upper Integral (>= 3) != Lower Integral (= 0), f is NOT Riemann integrable on [0, 2]!"]
        ],
        col_widths=[W*0.34, W*0.66]
    ))

    # ================= MODULE 6 =================
    s.append(Paragraph("[6.0] Infinite Series, Power Series (Q8) & Uniform Convergence (Q9b)", h3_style))
    s.append(make_table(
        ["[6.1] Series Test", "Formula / Hypotheses to Check", "Conclusion & Exam Application"],
        [
            ["1. Divergence Test", "Compute lim_{n->inf} a_n", "If lim a_n != 0 (or DNE), series sum a_n DIVERGES! (If lim = 0, test is inconclusive)"],
            ["2. Geometric Series", "sum_{n=0}^inf a * r^n", "Converges to a / (1 - r) iff |r| < 1;  Diverges if |r| >= 1"],
            ["3. p-Series Test", "sum_{n=1}^inf (1 / n^p)", "CONVERGES iff p > 1 (e.g. 1/n^2, 1/n^3);  DIVERGES iff p <= 1 (e.g. 1/n, 1/sqrt(n))"],
            ["4. Direct Comparison\nTest (a_n >= 0)", "• To prove Convergence: find 0 <= a_n <= b_n where sum b_n converges\n• To prove Divergence: find 0 <= b_n <= a_n where sum b_n diverges", "Example (2025 Q8): 4 / (n^3 + 5). Since n^3 + 5 > n^3 > 0 for all n >= 1,\n0 < 4 / (n^3 + 5) < 4 / n^3. Since sum 4(1/n^3) converges (p = 3 > 1), series converges!"],
            ["5. Alternating Series\nTest (AST)", "For sum (-1)^n b_n with b_n > 0, check 3 conditions:\n(1) b_n > 0  |  (2) (b_n) is decreasing (b_{n+1} <= b_n)  |  (3) lim_{n->inf} b_n = 0", "Example: sum (-1)^n / sqrt(n + 3). Here b_n = 1/sqrt(n+3) > 0, strictly decreasing since sqrt(n+4) > sqrt(n+3), and lim b_n = 0 => CONVERGES by AST!"],
            ["6. Ratio Test", "Compute L = lim_{n->inf} |a_{n+1} / a_n|", "• L < 1 => Converges absolutely   • L > 1 (or inf) => Diverges   • L = 1 => Inconclusive\nUse whenever a_n contains factorials (n!) or exponentials (c^n)!"],
            ["[6.2] Power Series\nsum c_n (x - a)^n", "1. Radius R = lim_{n->inf} |c_n / c_{n+1}|  (or apply Ratio Test |(x-a)| * L < 1)\n2. Test left endpoint x = a - R and right endpoint x = a + R separately!", "Example: sum (2^n / sqrt(n)) x^n. R = lim |(2^n/sqrt(n)) / (2^{n+1}/sqrt(n+1))| = 1/2.\n• At x = -1/2: sum (-1)^n / sqrt(n) -> Converges by AST!\n• At x = +1/2: sum 1 / sqrt(n) -> Diverges (p = 1/2 <= 1)!  Interval I = [-1/2, 1/2)."]
        ],
        col_widths=[W*0.21, W*0.41, W*0.38]
    ))
    s.append(Spacer(1, 3))
    s.append(Preformatted(
"""/* [6.3.2] Q9(b) Uniform Convergence Supremum Proof Template: f_n(x) = x^2 / (n + x^2) on [0, 1] */
1. Pointwise Limit: Fix x in [0, 1]. Since 0 <= x^2 <= 1, as n -> inf, lim_{n->inf} x^2 / (n + x^2) = 0.
                    Thus the pointwise limit function is f(x) = 0 for all x in [0, 1].
2. Uniform Convergence (M_n Bound): For all x in [0, 1], since x^2 <= 1 and n + x^2 >= n > 0, we have:
                    |f_n(x) - f(x)| = |x^2 / (n + x^2) - 0| = x^2 / (n + x^2) <= 1 / n.
   Therefore, M_n = sup_{x in [0,1]} |f_n(x) - f(x)| <= 1 / n.
   Since lim_{n->inf} (1 / n) = 0, by Squeeze Theorem lim_{n->inf} M_n = 0. Hence f_n -> f uniformly on [0, 1]. [Q.E.D.]""", code_style))

    doc.build(s)

out1 = r"C:\Users\kakur\Desktop\MAST20026_Full_Exam_Spec.pdf"
out2 = r"C:\Users\kakur\Desktop\University\Semester_Current\MAST20026_Analysis\MAST20026_Full_Exam_Spec.pdf"

build_pdf(out1)
shutil.copyfile(out1, out2)
print("MAST20026 Full Exam Spec PDF generated successfully!")

