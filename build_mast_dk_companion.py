# -*- coding: utf-8 -*-
"""
MAST20026 Real Analysis
Master Publication-Grade DK Study Companion Generator (Full Edition)
Compiles each module into a guaranteed 1-page A3 landscape spread,
then merges into one publication-grade master volume.
"""

import os
import subprocess
import fitz
import shutil

BASE_DIR = r"C:\Users\kakur\Desktop\COMP20003_Project 2"
OUT_PDF = r"C:\Users\kakur\Desktop\MAST20026_DK_Study_Companion_Full.pdf"
COURSE_PDF = r"C:\Users\kakur\Desktop\University\Semester_Current\MAST20026_Analysis\MAST20026_DK_Study_Companion_Full.pdf"
TEMP_PROFILE = r"C:\Users\kakur\AppData\Local\Temp\edge_mast_companion_profile"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

COMMON_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@500;700;800&display=swap');

  @page {
    size: 420mm 297mm landscape;
    margin: 5mm 9mm 4mm 9mm;
  }

  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  html, body {
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;
  }

  body {
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    color: #0F172A;
    background: #FFFFFF;
    font-size: 7.2pt;
    line-height: 1.26;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  code, pre, .mono {
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 6.8pt;
    font-weight: 700;
  }

  /* Running Header */
  .running-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1.6px solid #0F172A;
    padding-bottom: 2px;
    margin-bottom: 3px;
    font-size: 7.0pt;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: #475569;
    text-transform: uppercase;
  }
  .running-top .left-tag b { color: #0F172A; margin-right: 4px; }
  .running-top .right-tag b { color: #0F172A; margin-left: 4px; }

  /* 2-Page Spread Layout */
  .spread-container {
    display: grid;
    grid-template-columns: 49.3% 49.3%;
    column-gap: 1.4%;
    position: relative;
    flex: 1;
  }

  /* Center Fold Line */
  .spread-container::after {
    content: "";
    position: absolute;
    top: -2px;
    bottom: -2px;
    left: 50%;
    width: 1px;
    background: linear-gradient(to bottom, rgba(203,213,225,0.2), rgba(148,163,184,0.6), rgba(203,213,225,0.2));
  }

  .page-left { padding-right: 6px; display: flex; flex-direction: column; justify-content: space-between; }
  .page-right { padding-left: 6px; display: flex; flex-direction: column; justify-content: space-between; }

  /* Section Title Block */
  .title-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 3px;
  }
  .title-block h1 {
    font-size: 19.0pt;
    font-weight: 300;
    letter-spacing: -0.03em;
    color: #0F172A;
    margin: 0;
    line-height: 1.05;
  }
  .title-block h1 b { font-weight: 800; color: #0284C7; }
  .title-block .subtitle {
    font-size: 7.5pt;
    font-weight: 700;
    color: #475569;
    margin-top: 1px;
  }

  /* Architectural Exam Stamp */
  .exam-stamp {
    border: 1.6px dashed #DC2626;
    border-radius: 4px;
    padding: 2px 6px;
    text-align: center;
    transform: rotate(1deg);
    background: #FEF2F2;
    box-shadow: 0 1px 3px rgba(220,38,38,0.10);
    flex-shrink: 0;
  }
  .exam-stamp-badge {
    font-size: 7.2pt;
    font-weight: 800;
    color: #DC2626;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    display: block;
    line-height: 1.2;
  }
  .exam-stamp-sub {
    font-size: 5.9pt;
    font-weight: 800;
    color: #991B1B;
    letter-spacing: 0.03em;
    display: block;
  }

  /* Reference Cross-Linking Badge */
  .spec-ref {
    display: inline-block;
    background: #0284C7;
    color: #FFFFFF;
    font-size: 6.5pt;
    font-weight: 800;
    padding: 1px 5px;
    border-radius: 3px;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    vertical-align: middle;
  }
  .spec-ref.orange { background: #EA580C; }
  .spec-ref.green { background: #16A34A; }
  .spec-ref.purple { background: #7C3AED; }

  /* Section Headings */
  .point-header {
    font-size: 8.2pt;
    font-weight: 800;
    color: #0F172A;
    margin: 2px 0 1px 0;
    display: flex;
    align-items: center;
    border-bottom: 1.5px solid #CBD5E1;
    padding-bottom: 1px;
  }
  .point-header span.marks {
    margin-left: auto;
    font-size: 6.4pt;
    font-weight: 800;
    color: #DC2626;
    background: #FEE2E2;
    padding: 1px 4px;
    border-radius: 8px;
    border: 1px solid #FCA5A5;
  }

  /* High-Contrast Memory / Data Cell Strips */
  .array-strip-container {
    background: #F8FAFC;
    border: 1.5px solid #CBD5E1;
    border-radius: 4px;
    padding: 3.5px 6px;
    margin: 2px 0;
  }
  .array-strip {
    display: flex;
    align-items: center;
    gap: 4px;
    margin: 2px 0;
  }
  .array-cell-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 54px;
  }
  .array-index {
    font-family: 'JetBrains Mono', monospace;
    font-size: 6.2pt;
    font-weight: 700;
    color: #64748B;
    margin-bottom: 1px;
  }
  .array-val {
    min-width: 54px;
    padding: 0 5px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.4pt;
    font-weight: 800;
    color: #0F172A;
    background: #FFFFFF;
    border: 1.8px solid #334155;
    border-radius: 3px;
  }
  .array-val.active-swap { background: #FEF08A; border-color: #CA8A04; color: #854D0E; }
  .array-val.new-key { background: #BAE6FD; border-color: #0284C7; color: #0369A1; }
  .array-val.final-root { background: #DCFCE7; border-color: #16A34A; color: #15803D; }
  .array-val.danger-cell { background: #FEE2E2; border-color: #DC2626; color: #991B1B; }

  /* Step Badge */
  .step-pill {
    display: inline-block;
    background: #0F172A;
    color: #FFFFFF;
    font-size: 6.4pt;
    font-weight: 800;
    padding: 1px 5px;
    border-radius: 10px;
    margin-right: 4px;
    vertical-align: middle;
  }
  .step-pill.blue { background: #0284C7; }
  .step-pill.red { background: #DC2626; }
  .step-pill.green { background: #16A34A; }
  .step-pill.purple { background: #7C3AED; }

  /* Step Card */
  .worked-step-card {
    background: #FFFFFF;
    border: 1.2px solid #E2E8F0;
    border-left: 3.5px solid #0284C7;
    border-radius: 4px;
    padding: 2.5px 5px;
    margin: 2px 0;
  }
  .worked-step-card.red-bar { border-left-color: #DC2626; }
  .worked-step-card.green-bar { border-left-color: #16A34A; }
  .worked-step-card.purple-bar { border-left-color: #7C3AED; }
  .worked-step-card .step-title {
    font-size: 7.0pt;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 1px;
  }
  .worked-step-card .step-desc {
    font-size: 6.6pt;
    line-height: 1.20;
    color: #334155;
  }
  .worked-step-card .step-desc b { color: #0F172A; }

  /* Academic Comparison Table */
  table.exam-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 6.6pt;
    margin: 2px 0;
  }
  table.exam-table th {
    background: #F1F5F9;
    color: #334155;
    font-weight: 800;
    text-align: left;
    padding: 2px 4px;
    border: 1px solid #CBD5E1;
    font-size: 6.4pt;
    text-transform: uppercase;
    letter-spacing: 0.02em;
  }
  table.exam-table td {
    padding: 1.8px 4px;
    border: 1px solid #E2E8F0;
    color: #1E293B;
    line-height: 1.18;
  }
  table.exam-table tr:nth-child(even) { background: #F8FAFC; }
  table.exam-table tr.highlight-row { background: #E0F2FE; font-weight: 600; }
  table.exam-table tr.highlight-row td { border-color: #BAE6FD; color: #0369A1; }

  /* Washi Tape Sticky Notes */
  .sticky-note {
    border-radius: 3px;
    padding: 3px 6px;
    position: relative;
    box-shadow: 1px 2px 4px rgba(0,0,0,0.03);
    margin: 2px 0;
  }
  .sticky-note.yellow { background: #FEF9C3; border: 1.2px solid #FDE047; }
  .sticky-note.green { background: #DCFCE7; border: 1.2px solid #86EFAC; }
  
  .sticky-tape {
    position: absolute;
    top: -3px;
    left: 45%;
    width: 26px;
    height: 5px;
    background: rgba(255,255,255,0.75);
    border: 1px solid rgba(0,0,0,0.1);
  }
  .sticky-title {
    font-size: 6.7pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    margin-bottom: 1px;
  }
  .sticky-note.yellow .sticky-title { color: #854D0E; }
  .sticky-note.green .sticky-title { color: #166534; }
  .sticky-content { font-size: 6.5pt; line-height: 1.20; color: #1E293B; }

  /* Sub Grid 2 */
  .sub-grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5px;
  }

  /* Running Bottom */
  .running-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1.8px solid #0F172A;
    padding-top: 2px;
    margin-top: 2px;
    font-size: 6.9pt;
    font-weight: 800;
    color: #475569;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  .running-bottom .page-num { color: #0F172A; font-weight: 800; margin-right: 4px; }
</style>
</head>
<body>
"""

COMMON_FOOT = """
</body>
</html>
"""

def compile_spread(html_content, temp_pdf_path):
    temp_html = os.path.join(BASE_DIR, "temp_mast_spread.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        EDGE_PATH, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        f"--user-data-dir={TEMP_PROFILE}",
        f"--print-to-pdf={temp_pdf_path}", f"file:///{temp_html}"
    ]
    subprocess.run(cmd, capture_output=True, text=True)

modules = []

# ==============================================================================
# MODULE 1: Logic, Truth Tables (Exam Q1) & Field Axioms of R (Exam Q2)
# ==============================================================================
modules.append({
    "name": "Module 1 · Logic, Truth Tables & Field Axioms",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>010</b> | MAST20026 STUDY COMPANION &nbsp;·&nbsp; MODULE 1: LOGIC, TRUTH TABLES & AXIOMS OF R</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §1.1 &ndash; §1.2] &nbsp;|&nbsp; <b>011</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 1 · <b>Logic &amp; Truth Tables: Worked Exam Guide</b></h1>
        <div class="subtitle">4-Row Truth Table Construction, Row Deduction &amp; Equivalence &nbsp;·&nbsp; <span class="spec-ref">CROSS-REF SPEC §1.1</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] ALWAYS QUESTION 1</span>
        <span class="exam-stamp-sub">PROPOSITIONAL LOGIC · 9 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Complete 2025 S1 Question 1 Walkthrough (9 Marks)</span>
        <span class="marks">9 MARKS GUARANTEED</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>2025 S1 Exam Q1:</b> Let <i>p</i> and <i>q</i> be primitive statements.<br/>
        (a) [4 marks] Write a truth table for <code>q &rArr; (p &or; (&sim;q))</code>. &nbsp; (b) [2 marks] If <i>q</i> is true and <code>q &rArr; (p &or; (&sim;q))</code> is true, what can you conclude about <i>p</i>? Justify by citing specific lines. &nbsp; (c) [3 marks] Find a logically equivalent statement with at most one connective.
      </div>

      <table class="exam-table">
        <thead>
          <tr>
            <th>Row #</th>
            <th><i>p</i></th>
            <th><i>q</i></th>
            <th>&sim;<i>q</i></th>
            <th><i>p</i> &or; (&sim;<i>q</i>)</th>
            <th><i>q</i> &rArr; (<i>p</i> &or; (&sim;<i>q</i>))</th>
            <th>Reference: <i>q</i> &rArr; <i>p</i></th>
          </tr>
        </thead>
        <tbody>
          <tr class="highlight-row">
            <td><b>Line 1</b></td>
            <td><b>T</b></td>
            <td><b>T</b></td>
            <td>F</td>
            <td>T &or; F = <b>T</b></td>
            <td>T &rArr; T = <b>T</b> &nbsp;(Matches Part b!)</td>
            <td><b>T</b></td>
          </tr>
          <tr>
            <td><b>Line 2</b></td>
            <td><b>T</b></td>
            <td><b>F</b></td>
            <td>T</td>
            <td>T &or; T = <b>T</b></td>
            <td>F &rArr; T = <b>T</b> &nbsp;(Vacuous Truth)</td>
            <td><b>T</b></td>
          </tr>
          <tr>
            <td><b>Line 3</b></td>
            <td><b>F</b></td>
            <td><b>T</b></td>
            <td>F</td>
            <td>F &or; F = <b>F</b></td>
            <td>T &rArr; F = <b>F</b> &nbsp;(Eliminated in b!)</td>
            <td><b>F</b></td>
          </tr>
          <tr>
            <td><b>Line 4</b></td>
            <td><b>F</b></td>
            <td><b>F</b></td>
            <td>T</td>
            <td>F &or; T = <b>T</b></td>
            <td>F &rArr; T = <b>T</b> &nbsp;(Vacuous Truth)</td>
            <td><b>T</b></td>
          </tr>
        </tbody>
      </table>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">STEP 2 (PART B)</span> Word-for-Word Full-Mark Justification Template</div>
        <div class="step-desc">
          &bull; "We are given that <i>q</i> is <b>T</b> and the compound statement <code>q &rArr; (p &or; (&sim;q))</code> is <b>T</b>.<br/>
          &bull; Looking at the truth table from Part (a), <i>q</i> is <b>T</b> only on <b>Line 1</b> and <b>Line 3</b>.<br/>
          &bull; However, on <b>Line 3</b> the compound statement is <b>F</b>, so Line 3 is ruled out.<br/>
          &bull; Thus only <b>Line 1</b> satisfies both premises, and on Line 1 we see that <b><i>p</i> must be True (T)</b>."
        </div>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">STEP 3 (PART C)</span> Finding the 1-Connective Equivalent Statement</div>
        <div class="step-desc">
          The final column has truth values <b>(T, T, F, T)</b> (false only on Line 3 where <i>q</i> = T and <i>p</i> = F).<br/>
          Comparing this with the truth table of <b><code>q &rArr; p</code></b>, which also has column <b>(T, T, F, T)</b>, their columns are identical in every row. Therefore, <code>q &rArr; (p &or; (&sim;q))</code> is logically equivalent to <b><code>q &rArr; p</code></b>!
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">VACUOUS TRUTH GOLDEN RULE</div>
        <div class="sticky-content">
          An implication <code>A &rArr; B</code> is <b>FALSE ONLY WHEN A = T and B = F</b>! Whenever the hypothesis <code>A = F</code>, <code>F &rArr; T</code> and <code>F &rArr; F</code> are BOTH <b>TRUE</b>!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">1-CONNECTIVE LOOKUP FINGERPRINTS</div>
        <div class="sticky-content">
          For rows (TT, TF, FT, FF):<br/>
          &bull; <code>p &rArr; q</code>: <b>(T, F, T, T)</b> &nbsp;|&nbsp; <code>q &rArr; p</code>: <b>(T, T, F, T)</b><br/>
          &bull; <code>&sim;p</code>: <b>(F, F, T, T)</b> &nbsp;|&nbsp; <code>p &and; q</code>: <b>(T, F, F, F)</b>
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> Formal Proof from Field Axioms of R (2024/2025 Exam Q2)</span>
        <span class="marks">8 MARKS GUARANTEED</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>Exam Q2 Rule:</b> Every single step must cite exactly one Axiom code (<code>A1-A5</code>, <code>M1-M5</code>, <code>D</code>, <code>O1-O2</code>, <code>OA</code>, <code>OM</code>). Never skip parentheses (<code>A3/M3</code>) or order swaps (<code>A2/M2</code>)!
      </div>

      <div class="array-strip-container" style="border-color: #0284C7; background: #F0F9FF;">
        <div style="font-size: 6.7pt; font-weight: 800; color: #0369A1; margin-bottom: 1px;">
          <span class="step-pill blue">WORKED PROOF A</span> Multiplicative Cancellation: Assume <i>a &ne; 0</i> and <i>ab = ac</i>. Prove <i>b = c</i>.
        </div>
        <pre class="mono" style="margin: 0; line-height: 1.18; font-size: 5.6pt; color: #0F172A;">
Step 1: Since a &ne; 0, by M5 &exist;(1/a) &isin; R\{0} with a &middot; (1/a) = 1.
Step 2: From ab = ac (Premise), multiply both sides by (1/a):
        (1/a) &middot; (ab) = (1/a) &middot; (ac).
Step 3: By Axiom M3 (Associativity): ((1/a)&middot;a)&middot;b = ((1/a)&middot;a)&middot;c.
Step 4: By Axiom M2 (Commutativity): (a&middot;(1/a))&middot;b = (a&middot;(1/a))&middot;c.
Step 5: Substitute a &middot; (1/a) = 1 (Step 1):     1 &middot; b = 1 &middot; c.
Step 6: By Axiom M4 (Identity 1x = x):         b = c.  [Q.E.D.]</pre>
      </div>

      <div class="array-strip-container" style="border-color: #16A34A; background: #F0FDF4; margin-top: 4px;">
        <div style="font-size: 6.7pt; font-weight: 800; color: #166534; margin-bottom: 1px;">
          <span class="step-pill green">WORKED PROOF B</span> Zero Multiplication Property: Prove <i>0 &middot; x = 0</i> for all <i>x &isin; R</i>.
        </div>
        <pre class="mono" style="margin: 0; line-height: 1.18; font-size: 5.6pt; color: #0F172A;">
Step 1: By Axiom A4 (Additive identity), 0 + 0 = 0.
Step 2: Multiply by x and apply M2:   x &middot; (0 + 0) = x &middot; 0.
Step 3: By Axiom D (Distributivity):  x &middot; 0 + x &middot; 0 = x &middot; 0.
Step 4: By Axiom A4 on RHS:           x &middot; 0 + x &middot; 0 = x &middot; 0 + 0.
Step 5: By Axiom A5, &exist;-(x&middot;0) &isin; R with (x&middot;0) + (-(x&middot;0)) = 0.
Step 6: Add -(x&middot;0) to both sides and apply A3 &amp; A5:
        x&middot;0 + 0 = 0 &rArr; x&middot;0 = 0 (by A4) &rArr; 0&middot;x = 0 (by M2). [Q.E.D.]</pre>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">WORKED PROOF C</span> Order Axiom Inequality: If <i>0 &lt; a &lt; b</i>, prove <i>a&sup2; &lt; b&sup2;</i></div>
        <div class="step-desc">
          1. Since <code>0 &lt; a</code> and <code>a &lt; b</code>, by Axiom <b>OA</b> (adding <code>-a</code>) and <b>OM</b> (multiplying by positive <code>a &gt; 0</code>): <code>a &middot; a &lt; b &middot; a</code>, i.e., <code>a&sup2; &lt; ab</code>.<br/>
          2. Since <code>0 &lt; a</code> and <code>a &lt; b</code>, by Axiom <b>O2</b> (Transitivity), <code>0 &lt; b</code>. By <b>OM</b> (multiplying <code>a &lt; b</code> by <code>b &gt; 0</code>): <code>ab &lt; b&sup2;</code>.<br/>
          3. By Axiom <b>O2</b> (Transitivity) on <code>a&sup2; &lt; ab</code> and <code>ab &lt; b&sup2;</code>: <b><code>a&sup2; &lt; b&sup2;</code></b>!
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">COMMON Q2 DEDUCTION TRAP</div>
        <div class="sticky-content">
          Axiom A5 states <code>x + (-x) = 0</code> (with <code>-x</code> on the RIGHT). If your proof has <code>(-a) + a</code>, you MUST cite <b>Axiom A2 (Commutativity)</b> to flip it to <code>a + (-a)</code> before replacing it with <code>0</code>!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">HOW TO NEGATE QUANTIFIERS</div>
        <div class="sticky-content">
          To negate a statement: flip every <code>&forall; &harr; &exist;</code>, keep domain conditions (<code>&isin; R</code>), and negate the predicate:<br/>
          <code>&sim;(&forall;&epsilon;&gt;0, &exist;&delta;&gt;0 : P &rArr; Q) &hArr; &exist;&epsilon;&gt;0, &forall;&delta;&gt;0 : P &and; (&sim;Q)</code>!
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">010</span> MAST20026 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: TRUTH TABLES (Q1)</div>
  <div>WORKED EXAMPLE: FORMAL PROOFS FROM AXIOMS OF R (Q2) &nbsp;·&nbsp; <span class="page-num">011</span></div>
</div>
""" + COMMON_FOOT
})

# ==============================================================================
# MODULE 2: Completeness, Supremum Proofs (Exam Q3) & Counterexamples (Exam Q4)
# ==============================================================================
modules.append({
    "name": "Module 2 · Supremum Proofs & Counterexample Construction",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>020</b> | MAST20026 STUDY COMPANION &nbsp;·&nbsp; MODULE 2: SUPREMUM PROOFS (Q3) & COUNTEREXAMPLES (Q4)</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §2.1 &ndash; §2.2] &nbsp;|&nbsp; <b>021</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 2 · <b>Supremum &amp; Bounds: Worked Proof Guide</b></h1>
        <div class="subtitle">Additive Sets sup(A+B) &amp; Scaled Sets sup(kA) &nbsp;·&nbsp; <span class="spec-ref">CROSS-REF SPEC §2.1</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] ALWAYS QUESTION 3</span>
        <span class="exam-stamp-sub">SUPREMUM PROOFS · 9-10 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Complete Proof of <code>sup(A + B) = sup A + sup B</code> (2025 S1 Q3)</span>
        <span class="marks">9 MARKS EXAM Q</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>2025 S1 Q3:</b> Let <i>A, B &sub; R</i> be non-empty and bounded above. Define <code>A + B = {x + y : x &isin; A, y &isin; B}</code>.<br/>
        (a) [3 marks] Show that if <i>&alpha;</i> is an upper bound of <i>A</i> and <i>&beta;</i> is an upper bound of <i>B</i>, then <i>&alpha; + &beta;</i> is an upper bound of <i>A + B</i>.<br/>
        (b) [6 marks] Show that <code>sup(A + B) = sup A + sup B</code>.
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">PART (a) PROOF</span> Prove <i>&alpha; + &beta;</i> is an Upper Bound of <i>A + B</i> [3 Marks]</div>
        <div class="step-desc">
          1. Let <code>z &isin; A + B</code> be arbitrary. By definition of <code>A + B</code>, there exist <code>x &isin; A</code> and <code>y &isin; B</code> such that <code>z = x + y</code>.<br/>
          2. Since <code>&alpha;</code> is an upper bound of <code>A</code>, we have <code>x &le; &alpha;</code>. Since <code>&beta;</code> is an upper bound of <code>B</code>, we have <code>y &le; &beta;</code>.<br/>
          3. Adding the two inequalities yields <code>z = x + y &le; &alpha; + &beta;</code>. Since this holds for all <code>z &isin; A + B</code>, <code>&alpha; + &beta;</code> is an upper bound of <code>A + B</code>. &blacksquare;
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">PART (b) PROOF</span> Two-Way Inequality Method OR &epsilon;-Approximation Method [6 Marks]</div>
        <div class="step-desc">
          &bull; <b>Direction 1 (<code>sup(A + B) &le; sup A + sup B</code>):</b> Since <code>sup A</code> is an upper bound of <i>A</i> and <code>sup B</code> is an upper bound of <i>B</i>, by Part (a), <code>sup A + sup B</code> is an upper bound of <code>A + B</code>. Since <code>sup(A + B)</code> is the <i>least</i> upper bound of <code>A + B</code>, we immediately have <b><code>sup(A + B) &le; sup A + sup B</code></b>.<br/>
          &bull; <b>Direction 2 (<code>sup(A + B) &ge; sup A + sup B</code> — Method A: &epsilon;-Doorstep Trick):</b><br/>
          Let <code>&epsilon; &gt; 0</code> be arbitrary. Since <code>sup A - &epsilon;/2 &lt; sup A</code>, it is not an upper bound of <i>A</i>, so <b>there exists <code>x &isin; A</code></b> with <code>x &gt; sup A - &epsilon;/2</code>. Similarly, <b>there exists <code>y &isin; B</code></b> with <code>y &gt; sup B - &epsilon;/2</code>.<br/>
          Then <code>x + y &isin; A + B</code>, so <code>sup(A + B) &ge; x + y &gt; (sup A + sup B) - &epsilon;</code>. Since this holds for all <code>&epsilon; &gt; 0</code>, <b><code>sup(A + B) &ge; sup A + sup B</code></b>. Combining both directions gives equality! &blacksquare;
        </div>
      </div>

      <div class="worked-step-card purple-bar">
        <div class="step-title"><span class="step-pill purple">ALTERNATIVE</span> Scaled Set Proof: <code>sup(kA) = k sup A</code> for <i>k &gt; 0</i></div>
        <div class="step-desc">
          1. By Part (a) with <code>&alpha; = sup A</code>, <code>k sup A</code> is an upper bound of <code>kA</code>, so <code>sup(kA) &le; k sup A</code>.<br/>
          2. Conversely, since <code>sup(kA)</code> is an upper bound of <code>kA</code>, for all <code>x &isin; A</code> we have <code>kx &le; sup(kA) &rArr; x &le; sup(kA)/k</code>. Thus <code>sup(kA)/k</code> is an upper bound of <i>A</i>, so <code>sup A &le; sup(kA)/k &rArr; k sup A &le; sup(kA)</code>!
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">QUANTIFIER TRAP IN SUP PROOF</div>
        <div class="sticky-content">
          When dropping below <code>sup A</code> to <code>sup A - &epsilon;</code>, NEVER write "for all <code>x &isin; A</code>"! Only <b>at least one element</b> pierces above <code>sup A - &epsilon;</code>: you MUST write <b>"there exists <code>x &isin; A</code>" (<code>&exist;x &isin; A</code>)</b>!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">WHAT IF k &lt; 0? (NEGATIVE SCALE)</div>
        <div class="sticky-content">
          Multiplying an inequality by <code>k &lt; 0</code> <b>flips the inequality sign</b>, turning upper bounds into lower bounds: for <code>k &lt; 0</code>, <b><code>sup(kA) = k &middot; inf A</code></b> and <b><code>inf(kA) = k &middot; sup A</code></b>!
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> Constructing Specific Examples &amp; Limit Points (Exam Q4 — 12 Marks)</span>
        <span class="marks">12 MARKS GUARANTEED</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>Exam Q4 Pattern:</b> "For each situation, provide a <b>specific example</b> (explicit formula/set) and <b>briefly justify</b> your answer." (3 parts &times; 4 marks = 12 marks).
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">CASE 1 (LIMIT POINTS)</span> Infinite subset <i>E &sub; R</i> whose set of limit points is <code>{2}</code></div>
        <div class="step-desc">
          &bull; <b>Specific Example:</b> Let <b><code>E = { 2 + 1/n : n &isin; N+ }</code></b>.<br/>
          &bull; <b>Justification:</b> <i>E</i> is an infinite subset of <i>R</i>. Since <code>lim_{n&rarr;&infin;} (2 + 1/n) = 2</code> and every element <code>2 + 1/n &ne; 2</code>, every open neighbourhood <code>(2 - &epsilon;, 2 + &epsilon;)</code> contains infinitely many points of <i>E</i>, so <code>2</code> is a limit point. For any <code>L &ne; 2</code>, choosing <code>&epsilon; = |L - 2|/2</code> isolates <i>L</i> from almost all terms, so no other limit point exists. Thus the set of limit points is <code>{2}</code>.
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">CASE 2 (SEQUENCES)</span> Sequence <i>(a<sub>n</sub>)</i> where <i>(a<sub>n</sub>)&sup2; &rarr; 16</i>, but <i>(a<sub>n</sub>)</i> diverges</div>
        <div class="step-desc">
          &bull; <b>Specific Example:</b> Let <b><code>a_n = 4 &middot; (-1)^n</code></b> for each <code>n &isin; N+</code>.<br/>
          &bull; <b>Justification:</b> For every <code>n &isin; N+</code>, <code>(a_n)&sup2; = 16 &middot; ((-1)^n)&sup2; = 16</code>, which is a constant sequence converging to <code>16</code>. However, <code>(a_n)</code> alternates between <code>-4</code> (odd <i>n</i>) and <code>+4</code> (even <i>n</i>); since two subsequences converge to different limits (<code>-4 &ne; 4</code>), <code>(a_n)</code> diverges.
        </div>
      </div>

      <div class="worked-step-card purple-bar">
        <div class="step-title"><span class="step-pill purple">CASE 3 (CANCELLATION)</span> Two divergent sequences <i>(x<sub>n</sub>), (y<sub>n</sub>)</i> whose sum <i>(x<sub>n</sub> + y<sub>n</sub>) &rarr; 3</i></div>
        <div class="step-desc">
          &bull; <b>Specific Example:</b> Let <b><code>x_n = 3 + (-1)^n</code></b> and <b><code>y_n = -(-1)^n = (-1)^{n+1}</code></b>.<br/>
          &bull; <b>Justification:</b> Both <code>(x_n)</code> (oscillating between 2 and 4) and <code>(y_n)</code> (oscillating between 1 and -1) diverge. However, for all <code>n &isin; N+</code>, their sum is the constant sequence <code>x_n + y_n = 3 + (-1)^n - (-1)^n = 3</code>, which converges to <code>3</code>!
        </div>
      </div>

      <table class="exam-table">
        <thead>
          <tr>
            <th>Bonus Q4 Exam Prompts</th>
            <th>Exact Example to Write Down</th>
          </tr>
        </thead>
        <tbody>
          <tr class="highlight-row">
            <td>Set <i>E</i> with <b>two</b> limit points <code>{0, 5}</code></td>
            <td><code>E = { 1/n : n &isin; N+ } &cup; { 5 + 1/n : n &isin; N+ }</code></td>
          </tr>
          <tr>
            <td>Continuous <i>f</i> on <code>(0, 1)</code> that is <b>not bounded</b></td>
            <td><code>f(x) = 1 / x</code> on open interval <code>(0, 1)</code> (EVT fails on open intervals!)</td>
          </tr>
          <tr class="highlight-row">
            <td>Continuous <i>f</i> at <code>x = 0</code> that is <b>not differentiable</b> at <code>0</code></td>
            <td><code>f(x) = |x|</code> (Left derivative = -1 &ne; Right derivative = +1 at <i>x = 0</i>)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">NEVER DRAW PICTURES ONLY IN Q4</div>
        <div class="sticky-content">
          In Q4, markers require an <b>explicit mathematical formula</b> (e.g. <code>a_n = 4(-1)^n</code>). Vague prose like "a sequence that jumps back and forth" scores 0/4!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">LIMIT POINT VS SUPREMUM</div>
        <div class="sticky-content">
          A supremum does NOT have to be a limit point! For <code>S = {1/n} &cup; {5}</code>, <code>sup S = 5</code> (isolated point), while the only limit point is <code>0</code>!
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">020</span> MAST20026 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: SUPREMUM PROOFS (Q3)</div>
  <div>WORKED EXAMPLE: COUNTEREXAMPLES & LIMIT POINTS (Q4) &nbsp;·&nbsp; <span class="page-num">021</span></div>
</div>
""" + COMMON_FOOT
})

# ==============================================================================
# MODULE 3: Sequences: Formal eps-N Proofs & Recursive MCT / Cauchy (Exam Q5)
# ==============================================================================
modules.append({
    "name": "Module 3 · Sequences, eps-N & Recursive MCT (Q5)",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>030</b> | MAST20026 STUDY COMPANION &nbsp;·&nbsp; MODULE 3: SEQUENCES, &epsilon;-N PROOFS & RECURSIVE MCT (Q5)</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §3.1 &ndash; §3.2] &nbsp;|&nbsp; <b>031</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 3 · <b>Sequences &amp; MCT: Worked Proof Guide</b></h1>
        <div class="subtitle">Formal &epsilon;-N Proofs &amp; 13-Mark Recursive Sequence Blueprint &nbsp;·&nbsp; <span class="spec-ref">CROSS-REF SPEC §3.1–3.2</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] ALWAYS QUESTION 5</span>
        <span class="exam-stamp-sub">RECURSIVE MCT · 13 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Formal &epsilon;-N Sequence Limit Proof (Scratch Work &rarr; Formal Proof)</span>
        <span class="marks">8 MARKS CORE SKILL</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>Exam Problem:</b> Using the formal <code>&epsilon;-N</code> definition of a limit, prove that <code>lim_{n&rarr;&infin;} (2n + 1) / (n + 3) = 2</code>.
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">STAGE 1 (DRAFT PAPER)</span> Backwards Scratch Work to Bound <code>|x_n - L|</code> by a Simple <code>C / n</code></div>
        <div class="step-desc">
          1. <b>Combine Fraction:</b> <code>|(2n + 1)/(n + 3) - 2| = |(2n + 1 - 2n - 6)/(n + 3)| = |-5 / (n + 3)| = 5 / (n + 3)</code>.<br/>
          2. <b>Shrink Denominator to Make Fraction Larger:</b> Since <code>n + 3 &gt; n &gt; 0</code>, dropping <code>+3</code> gives <code>5 / (n + 3) &lt; 5 / n</code>.<br/>
          3. <b>Solve for <i>n</i>:</b> We force <code>5 / n &lt; &epsilon; &hArr; n &gt; 5 / &epsilon;</code>. Thus our threshold is <b><code>N = &lceil;5 / &epsilon;&rceil;</code></b> (or any integer <code>N &gt; 5/&epsilon;</code>)!
        </div>
      </div>

      <div class="array-strip-container" style="border-color: #16A34A; background: #F0FDF4;">
        <div style="font-size: 6.7pt; font-weight: 800; color: #166534; margin-bottom: 1px;">
          <span class="step-pill green">STAGE 2 (EXAM SCRIPT)</span> Word-for-Word Formal Proof Write-Up (Copy This Structure!)
        </div>
        <pre class="mono" style="margin: 0; line-height: 1.18; font-size: 6.2pt; color: #0F172A;">
Proof: Let &epsilon; &gt; 0 be given. By the Archimedean Property, choose N &isin; N+
such that N &gt; 5 / &epsilon; (which implies 5 / N &lt; &epsilon;).
Then for all integers n &gt; N, we have:
    | (2n + 1)/(n + 3) - 2 | = | (2n + 1 - 2(n + 3)) / (n + 3) |
                             = 5 / (n + 3)
                             &lt; 5 / n          (since n + 3 &gt; n &gt; 0)
                             &lt; 5 / N          (since n &gt; N &gt; 0)
                             &lt; 5 / (5 / &epsilon;) = &epsilon;.
Therefore, by the formal definition, lim_{n&rarr;&infin;} (2n + 1)/(n + 3) = 2.  &blacksquare;</pre>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">DENOMINATOR TRAP</span> What if Denominator Has a Minus Sign? e.g. <code>(3n + 1) / (2n - 5)</code></div>
        <div class="step-desc">
          You CANNOT write <code>1 / (2n - 5) &lt; 1 / (2n)</code> because subtracting 5 makes the denominator <i>smaller</i> (fraction larger)!<br/>
          <b>Fix:</b> Restrict <code>n &ge; 5</code> so that <code>2n - 5 &ge; n</code>, and then choose <code>N = max{5, &lceil;C / &epsilon;&rceil;}</code>!
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">NEVER SOLVE FOR n IN FORMAL PROOF</div>
        <div class="sticky-content">
          In the formal write-up, NEVER start with <code>|x_n - L| &lt; &epsilon;</code> and work backwards! You MUST state <code>Let &epsilon; &gt; 0</code>, define <code>N</code> first, and chain <code>|x_n - L| = ... &lt; &epsilon;</code> forward!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">CONVERGENT &hArr; CAUCHY IN R</div>
        <div class="sticky-content">
          In the real numbers <i>R</i>, a sequence <code>(x_n)</code> is a <b>Cauchy sequence if and only if it converges</b>! Once MCT proves convergence, Cauchy is automatic!
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> Recursive Sequence, Induction, MCT &amp; Cauchy (2025 S1 Q5 — 13 Marks!)</span>
        <span class="marks">13 MARKS EXAM Q</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>2025 S1 Q5:</b> Let <code>x_1 = 0</code> and <code>x_{n+1} = 9 / (6 - x_n)</code> for <code>n &isin; N+</code>.<br/>
        (a) [5 marks] Prove by induction that <code>0 &le; x_n &lt; 3</code> for all <code>n &isin; N+</code>. &nbsp; (b) [5 marks] Is <code>(x_n)</code> monotone increasing, decreasing, or neither? &nbsp; (c) [3 marks] Is <code>(x_n)</code> Cauchy? Find <code>lim_{n&rarr;&infin;} x_n</code>.
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">PART (a) [5 MARKS]</span> Mathematical Induction for Boundedness <code>0 &le; x_n &lt; 3</code></div>
        <div class="step-desc">
          &bull; <b>Base Case (<i>n = 1</i>):</b> <code>x_1 = 0</code>, which satisfies <code>0 &le; 0 &lt; 3</code>. Thus the statement holds for <code>n = 1</code>.<br/>
          &bull; <b>Inductive Hypothesis:</b> Assume <code>0 &le; x_k &lt; 3</code> holds for some integer <code>k &isin; N+</code>.<br/>
          &bull; <b>Inductive Step (<i>n = k + 1</i>):</b> From <code>0 &le; x_k &lt; 3</code>, negate to get <code>-3 &lt; -x_k &le; 0</code>. Add 6 to get <code>3 &lt; 6 - x_k &le; 6</code>.<br/>
          Taking reciprocals reverses inequalities: <code>1/6 &le; 1 / (6 - x_k) &lt; 1/3</code>. Multiplying by 9 gives:<br/>
          <code>9/6 &le; 9 / (6 - x_k) &lt; 9/3 &rArr; 0 &le; 1.5 &le; x_{k+1} &lt; 3</code>. Thus the statement holds for <code>n = k + 1</code>.<br/>
          &bull; <b>Conclusion:</b> By the Principle of Mathematical Induction, <code>0 &le; x_n &lt; 3</code> for all <code>n &isin; N+</code>. &blacksquare;
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">PART (b) [5 MARKS]</span> Monotonicity via Algebraic Difference <code>x_{n+1} - x_n</code></div>
        <div class="step-desc">
          Compute the difference and put over a common denominator:<br/>
          <code>x_{n+1} - x_n = 9 / (6 - x_n) - x_n = [ 9 - x_n(6 - x_n) ] / (6 - x_n) = (x_n&sup2; - 6x_n + 9) / (6 - x_n) = (x_n - 3)&sup2; / (6 - x_n)</code>.<br/>
          From Part (a), <code>0 &le; x_n &lt; 3</code> for all <code>n &isin; N+</code>:<br/>
          &bull; Numerator: Since <code>x_n &lt; 3</code> (so <code>x_n &ne; 3</code>), <b><code>(x_n - 3)&sup2; &gt; 0</code></b>.<br/>
          &bull; Denominator: Since <code>x_n &lt; 3</code>, <b><code>6 - x_n &gt; 6 - 3 = 3 &gt; 0</code></b>.<br/>
          Thus <code>x_{n+1} - x_n &gt; 0</code> for all <code>n &isin; N+</code>, so <code>(x_n)</code> is <b>strictly monotone increasing</b>! &blacksquare;
        </div>
      </div>

      <div class="worked-step-card purple-bar">
        <div class="step-title"><span class="step-pill purple">PART (c) [3 MARKS]</span> MCT, Cauchy Justification &amp; Fixed-Point Limit Calculation</div>
        <div class="step-desc">
          1. Since <code>(x_n)</code> is monotone increasing (Part b) and bounded above by 3 (Part a), by the <b>Monotone Convergence Theorem (MCT)</b>, <code>(x_n)</code> converges to some real limit <code>L &isin; R</code>.<br/>
          2. Since every convergent sequence in <i>R</i> is Cauchy, <b>YES, <code>(x_n)</code> is a Cauchy sequence</b>.<br/>
          3. Taking <code>n &rarr; &infin;</code> on both sides of <code>x_{n+1} = 9 / (6 - x_n)</code> yields <code>L = 9 / (6 - L) &rArr; 6L - L&sup2; = 9 &rArr; (L - 3)&sup2; = 0 &rArr; <b>L = 3</b></code>. &blacksquare;
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">MANDATORY PMI CLOSING SENTENCE</div>
        <div class="sticky-content">
          In Part (a), you MUST write the final concluding sentence citing <b>"By the Principle of Mathematical Induction..."</b> or Melbourne Uni markers deduct 1 mark!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">TWO ROOTS IN QUADRATIC LIMIT?</div>
        <div class="sticky-content">
          If solving <code>L = g(L)</code> gives two roots (e.g. <code>L = 1</code> and <code>L = 4</code>), use your Part (a) bound (e.g. <code>0 &le; x_n &le; 2 &rArr; 0 &le; L &le; 2</code>) to reject the extraneous root!
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">030</span> MAST20026 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: FORMAL &epsilon;-N SEQUENCE PROOF</div>
  <div>WORKED EXAMPLE: RECURSIVE SEQUENCE INDUCTION, MCT & CAUCHY (Q5) &nbsp;·&nbsp; <span class="page-num">031</span></div>
</div>
""" + COMMON_FOOT
})

# ==============================================================================
# MODULE 4: Function Limits, Discontinuity (Exam Q6) & Riemann Sums (Exam Q7)
# ==============================================================================
modules.append({
    "name": "Module 4 · Function Limits (Q6) & Riemann Integration (Q7)",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>040</b> | MAST20026 STUDY COMPANION &nbsp;·&nbsp; MODULE 4: FUNCTION LIMITS, DISCONTINUITY (Q6) & RIEMANN SUMS (Q7)</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §4.1 &ndash; §5.2] &nbsp;|&nbsp; <b>041</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 4 · <b>Function Limits &amp; Discontinuity (Q6)</b></h1>
        <div class="subtitle">Formal &epsilon;-M Limit Proof &amp; &epsilon;-&delta; Discontinuity Negation &nbsp;·&nbsp; <span class="spec-ref">CROSS-REF SPEC §4.1</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] ALWAYS QUESTION 6</span>
        <span class="exam-stamp-sub">LIMITS & CONTINUITY · 11 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Piecewise &epsilon;-M Limit &amp; &epsilon;-&delta; Discontinuity (2025 S1 Q6 — 11 Marks)</span>
        <span class="marks">11 MARKS EXAM Q</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>2025 S1 Q6 Archetype:</b> Let <code>f : R &rarr; R</code> be defined by <code>f(x) = 3x - 5</code> if <code>x &lt; 1</code>, and <code>f(x) = 2x / (x + 1)</code> if <code>x &ge; 1</code>.<br/>
        (a) [6 marks] Using the <code>&epsilon;-M</code> definition of limits, show that <code>lim_{x&rarr;&infin;} f(x) = 2</code>.<br/>
        (b) [5 marks] Using the <code>&epsilon;-&delta;</code> definition of continuity, show that <code>f</code> is <b>not continuous</b> at <code>x = 1</code>.
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">PART (a) [6 MARKS]</span> Formal <code>&epsilon;-M</code> Proof for <code>lim_{x&rarr;&infin;} f(x) = 2</code></div>
        <div class="step-desc">
          &bull; <b>Scratch Work:</b> For <code>x &ge; 1</code>, <code>f(x) = 2x/(x+1)</code>. Distance: <code>|2x/(x+1) - 2| = |-2/(x+1)| = 2/(x+1) &lt; 2/x</code>. To make <code>2/x &lt; &epsilon;</code>, we need <code>x &gt; 2/&epsilon;</code>. To also stay in the <code>x &ge; 1</code> branch, pick <b><code>M = max{1, 2/&epsilon;}</code></b>!<br/>
          &bull; <b>Formal Proof Write-Up:</b><br/>
          "Let <code>&epsilon; &gt; 0</code> be given. Choose <b><code>M = max{1, 2/&epsilon;}</code></b>. Then for all <code>x &gt; M</code>, since <code>x &gt; M &ge; 1</code>, we have <code>f(x) = 2x/(x+1)</code> and <code>x &gt; 2/&epsilon; &gt; 0</code>. Therefore:<br/>
          <code>|f(x) - 2| = |2x/(x+1) - 2| = 2 / (x + 1) &lt; 2 / x &lt; 2 / M &le; 2 / (2/&epsilon;) = &epsilon;</code>.<br/>
          Hence, by the definition of the limit at infinity, <code>lim_{x&rarr;&infin;} f(x) = 2</code>." &blacksquare;
        </div>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">PART (b) [5 MARKS]</span> Discontinuity Proof at Jump Point <code>x = 1</code> (Negation of &epsilon;-&delta;)</div>
        <div class="step-desc">
          &bull; <b>Step 1 (Compute Jump Gap):</b> At <code>a = 1</code>, <code>f(1) = 2(1)/(1+1) = 1</code>. As <code>x &rarr; 1^-</code>, <code>3x - 5 &rarr; -2</code>. Jump gap = <code>|1 - (-2)| = 3</code>. Pick <b><code>&epsilon;_0 = 1</code></b> (any positive number <code>&le; 3</code> works!).<br/>
          &bull; <b>Step 2 (Formal Proof Write-Up):</b><br/>
          "To prove <i>f</i> is discontinuous at <code>a = 1</code>, we show: <code>&exist;&epsilon;_0 &gt; 0</code> such that <code>&forall;&delta; &gt; 0, &exist;x &isin; R</code> with <code>|x - 1| &lt; &delta;</code> and <code>|f(x) - f(1)| &ge; &epsilon;_0</code>.<br/>
          Choose <b><code>&epsilon;_0 = 1 &gt; 0</code></b>. Let arbitrary <code>&delta; &gt; 0</code> be given.<br/>
          Choose <b><code>x = 1 - &delta;/2</code></b>. Then <code>|x - 1| = |-&delta;/2| = &delta;/2 &lt; &delta;</code>.<br/>
          Moreover, since <code>x = 1 - &delta;/2 &lt; 1</code>, we use the left branch <code>f(x) = 3x - 5 &lt; 3(1) - 5 = -2</code>.<br/>
          Since <code>f(1) = 1</code>, we have:<br/>
          <code>|f(x) - f(1)| = |f(x) - 1| = 1 - f(x) &gt; 1 - (-2) = 3 &gt; 1 = &epsilon;_0</code>.<br/>
          Therefore, <i>f</i> is not continuous at <code>x = 1</code>." &blacksquare;
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">WHY M = max{1, 2/&epsilon;} IS MANDATORY</div>
        <div class="sticky-content">
          In piecewise functions, if you only write <code>M = 2/&epsilon;</code>, when <code>&epsilon; = 10</code> you get <code>M = 0.2</code>, which falls into the WRONG branch (<code>x &lt; 1</code>)! Including <code>max{1, ...}</code> guarantees <code>x &gt; 1</code>!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">DISCONTINUITY VIA SEQUENCES</div>
        <div class="sticky-content">
          If the question does NOT force the <code>&epsilon;-&delta;</code> definition, you can also pick sequence <code>x_n = 1 - 1/n &rarr; 1</code> where <code>f(x_n) = 3(1-1/n)-5 &rarr; -2 &ne; f(1) = 1</code>!
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> Riemann Sums &amp; Rational/Irrational Non-Integrability (2025 S1 Q7)</span>
        <span class="marks">13 MARKS EXAM Q</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>2025 S1 Q7 Archetype:</b> (a) [4 marks] For <code>g(x) = x&sup2; + 1</code> on <code>[0, 3]</code> and <code>P_0 = {0, 1, 2, 3}</code>, compute <code>L(g, P_0)</code> and <code>U(g, P_0)</code>.<br/>
        (b) [4 marks] Let <code>f(x) = 4 - x&sup2;</code> if <code>x &isin; Q</code>, and <code>0</code> if <code>x &notin; Q</code> on <code>[0, 2]</code>. Compute <code>L(f, P)</code> for any partition <i>P</i>.<br/>
        (c) [5 marks] Find a positive lower bound for <code>Upper Integral &int;_0^2 f</code> and prove <i>f</i> is not Riemann integrable on <code>[0, 2]</code>.
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">PART (a) [4 MARKS]</span> Concrete Partition Sum on <code>P_0 = {0, 1, 2, 3}</code></div>
        <div class="step-desc">
          Subintervals are <code>I_1=[0,1], I_2=[1,2], I_3=[2,3]</code>, each of width <code>&Delta;x_i = 1</code>. Since <code>g(x) = x&sup2; + 1</code> is strictly increasing on <code>[0, 3]</code>, <code>m_i = g(x_{i-1})</code> and <code>M_i = g(x_i)</code>:<br/>
          &bull; Values: <code>g(0)=1, g(1)=2, g(2)=5, g(3)=10</code>.<br/>
          &bull; <b>Lower Sum:</b> <code>L(g, P_0) = 1(1) + 2(1) + 5(1) = <b>8</b></code>. &nbsp;|&nbsp; <b>Upper Sum:</b> <code>U(g, P_0) = 2(1) + 5(1) + 10(1) = <b>17</b></code>.
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">PART (b) [4 MARKS]</span> Arbitrary Partition Lower Sum <code>L(f, P) = 0</code> via Density of Irrationals</div>
        <div class="step-desc">
          Let <code>P = {x_0, x_1, ..., x_n}</code> be any partition of <code>[0, 2]</code>.<br/>
          1. On <code>[0, 2]</code>, for <code>x &isin; Q</code> we have <code>4 - x&sup2; &ge; 4 - 2&sup2; = 0</code>, and for <code>x &notin; Q</code> we have <code>f(x) = 0</code>. Thus <code>f(x) &ge; 0</code> everywhere.<br/>
          2. <b>By the density of the irrational numbers (<code>R \ Q</code>) in <i>R</i></b>, every subinterval <code>[x_{i-1}, x_i]</code> contains at least one irrational number <code>z_i &notin; Q</code>, where <code>f(z_i) = 0</code>.<br/>
          3. Thus <code>m_i = inf_{x &isin; [x_{i-1}, x_i]} f(x) = 0</code> for all <code>i</code>, giving <b><code>L(f, P) = &sum; 0 &middot; &Delta;x_i = 0</code></b>!
        </div>
      </div>

      <div class="worked-step-card purple-bar">
        <div class="step-title"><span class="step-pill purple">PART (c) [5 MARKS]</span> Bounding Upper Integral &gt; 0 &amp; Proving Non-Integrability</div>
        <div class="step-desc">
          1. For any partition <i>P</i> of <code>[0, 2]</code>, refine it to <code>P' = P &cup; {1}</code> (refining decreases upper sums: <code>U(f, P) &ge; U(f, P')</code>).<br/>
          2. Consider the subintervals of <code>P'</code> lying inside <code>[0, 1]</code>. <b>By the density of <i>Q</i> in <i>R</i></b>, every subinterval inside <code>[0, 1]</code> contains a rational number <code>q &isin; Q</code>, where <code>f(q) = 4 - q&sup2; &ge; 4 - 1&sup2; = 3</code>. Thus <code>M_i &ge; 3</code> on <code>[0, 1]</code>.<br/>
          3. Since <code>M_i &ge; 0</code> on <code>[1, 2]</code>, we have <code>U(f, P) &ge; U(f, P') &ge; 3 &middot; (1 - 0) + 0 &middot; (2 - 1) = 3</code>.<br/>
          4. Taking the infimum over all partitions <i>P</i> gives <b><code>Upper Integral &ge; 3 &gt; 0</code></b>. Since <code>Lower Integral = sup_P L(f,P) = 0 &ne; Upper Integral</code>, <b><i>f</i> is NOT Riemann integrable on <code>[0, 2]</code></b>! &blacksquare;
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">MAGIC PHRASE FOR FULL MARKS</div>
        <div class="sticky-content">
          Whenever a function splits into <code>x &isin; Q</code> and <code>x &notin; Q</code>, you MUST explicitly write the phrase: <b>"By the density of the rationals <i>Q</i> (and irrationals <i>R \ Q</i>) in <i>R</i>..."</b>!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">WHEN DOES Q vs R\Q INTEGRATE?</div>
        <div class="sticky-content">
          Only at a single point where the two branches intersect (e.g. if <code>4 - x&sup2; = 0</code> at <code>x = 2</code>), the jump is 0 at that point, but over any interval of length &gt; 0 with gap &gt; 0, it is non-integrable!
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">040</span> MAST20026 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: &epsilon;-M LIMIT & DISCONTINUITY (Q6)</div>
  <div>WORKED EXAMPLE: RIEMANN SUMS & DIRICHLET NON-INTEGRABILITY (Q7) &nbsp;·&nbsp; <span class="page-num">041</span></div>
</div>
""" + COMMON_FOOT
})

# ==============================================================================
# MODULE 5: Infinite Series, Power Series (Exam Q8) & Taylor / Uniform Convergence (Exam Q9)
# ==============================================================================
modules.append({
    "name": "Module 5 · Series, Power Series (Q8) & Taylor / Uniform Convergence (Q9)",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>050</b> | MAST20026 STUDY COMPANION &nbsp;·&nbsp; MODULE 5: INFINITE SERIES, POWER SERIES (Q8) & TAYLOR / UNIFORM CONVERGENCE (Q9)</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §4.3 &amp; §6.1 &ndash; §6.3] &nbsp;|&nbsp; <b>051</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 5 · <b>Series &amp; Power Series: Worked Exam Guide</b></h1>
        <div class="subtitle">Comparison, AST, Ratio Test &amp; Interval of Convergence &nbsp;·&nbsp; <span class="spec-ref">CROSS-REF SPEC §6.1–6.2</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] ALWAYS QUESTION 8</span>
        <span class="exam-stamp-sub">SERIES & POWER SERIES · 14 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Infinite Series Tests &amp; Power Series Interval (2025 S1 Q8 — 14 Marks)</span>
        <span class="marks">14 MARKS EXAM Q</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>2025 S1 Q8 Archetype:</b> (a) [6 marks] Prove whether each series converges or diverges: (i) <code>&sum;_{n=1}^&infin; 4 / (n&sup3; + 5)</code>, (ii) <code>&sum;_{n=1}^&infin; (-1)^n / &radic;(n + 3)</code>.<br/>
        (b) [8 marks] Find the radius of convergence <i>R</i> and interval of convergence <i>I</i> for <code>&sum;_{n=1}^&infin; (2^n / &radic;n) x^n</code>.
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">PART (a)(i) [3 MARKS]</span> Direct Comparison Test with a Convergent <i>p</i>-Series</div>
        <div class="step-desc">
          1. For all <code>n &ge; 1</code>, we have <code>n&sup3; + 5 &gt; n&sup3; &gt; 0</code>, which implies <code>0 &lt; 4 / (n&sup3; + 5) &lt; 4 / n&sup3;</code>.<br/>
          2. The series <code>&sum;_{n=1}^&infin; (1 / n&sup3;)</code> is a <b><i>p</i>-series with <code>p = 3 &gt; 1</code></b>, so it converges (and thus <code>&sum; 4/n&sup3;</code> converges).<br/>
          3. Therefore, by the <b>Direct Comparison Test</b>, <code>&sum;_{n=1}^&infin; 4 / (n&sup3; + 5)</code> <b>converges</b>! &blacksquare;
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">PART (a)(ii) [3 MARKS]</span> Alternating Series Test (AST) 3-Point Checklist</div>
        <div class="step-desc">
          Write the series as <code>&sum;_{n=1}^&infin; (-1)^n b_n</code> where <code>b_n = 1 / &radic;(n + 3)</code>. We check the 3 AST hypotheses:<br/>
          1. <b>Positivity:</b> <code>b_n = 1 / &radic;(n + 3) &gt; 0</code> for all <code>n &ge; 1</code>.<br/>
          2. <b>Monotone Decreasing:</b> Since <code>n + 4 &gt; n + 3 &gt; 0</code>, we have <code>&radic;(n + 4) &gt; &radic;(n + 3) &rArr; b_{n+1} &lt; b_n</code> for all <code>n &ge; 1</code>.<br/>
          3. <b>Limit is Zero:</b> <code>lim_{n&rarr;&infin;} b_n = lim_{n&rarr;&infin;} 1 / &radic;(n + 3) = 0</code>.<br/>
          Therefore, by the <b>Alternating Series Test</b>, the series <b>converges</b>! &blacksquare;
        </div>
      </div>

      <div class="worked-step-card purple-bar">
        <div class="step-title"><span class="step-pill purple">PART (b) [8 MARKS]</span> Power Series Radius <i>R</i> + Both Endpoints Check</div>
        <div class="step-desc">
          &bull; <b>Step 1 (Radius of Convergence <i>R</i>):</b> Here <code>c_n = 2^n / &radic;n</code>. Compute the ratio limit:<br/>
          <code>R = lim_{n&rarr;&infin;} |c_n / c_{n+1}| = lim_{n&rarr;&infin;} [ (2^n / &radic;n) &middot; (&radic;(n+1) / 2^{n+1}) ] = (1/2) &middot; lim_{n&rarr;&infin;} &radic;(1 + 1/n) = <b>1/2</b></code>.<br/>
          Thus the power series converges absolutely for <code>|x| &lt; 1/2</code> and diverges for <code>|x| &gt; 1/2</code>.<br/>
          &bull; <b>Step 2 (Test Right Endpoint <code>x = +1/2</code>):</b> Substitute <code>x = 1/2</code>:<br/>
          <code>&sum;_{n=1}^&infin; (2^n / &radic;n)(1/2)^n = &sum;_{n=1}^&infin; 1 / n^{1/2}</code>, which is a <b><i>p</i>-series with <code>p = 1/2 &le; 1</code> &rarr; DIVERGES!</b><br/>
          &bull; <b>Step 3 (Test Left Endpoint <code>x = -1/2</code>):</b> Substitute <code>x = -1/2</code>:<br/>
          <code>&sum;_{n=1}^&infin; (2^n / &radic;n)(-1/2)^n = &sum;_{n=1}^&infin; (-1)^n / &radic;n</code>. Since <code>1/&radic;n &gt; 0</code> is decreasing and <code>&rarr; 0</code>, it <b>CONVERGES by AST!</b><br/>
          &bull; <b>Conclusion:</b> Radius <b><code>R = 1/2</code></b>, and Interval of Convergence is <b><code>I = [-1/2, 1/2)</code></b>! &blacksquare;
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">ENDPOINT TESTING IS HALF THE MARKS!</div>
        <div class="sticky-content">
          In an 8-mark Power Series question, finding <code>R = 1/2</code> is worth only 4 marks; testing <code>x = +R</code> and <code>x = -R</code> and writing the exact bracket <code>[-1/2, 1/2)</code> is worth the other 4 marks!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">RATIO TEST ON FACTORIALS</div>
        <div class="sticky-content">
          For <code>a_n = 2^n / n!</code>, <code>|a_{n+1}/a_n| = [2^{n+1}/(n+1)!] &middot; [n!/2^n] = 2 / (n + 1) &rarr; 0 &lt; 1</code> &rarr; Converges by Ratio Test!
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> Taylor's Theorem &amp; Uniform Convergence (Exam Q9 — 10 Marks)</span>
        <span class="marks">10 MARKS FINAL Q</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>Exam Q9 Archetype:</b> (a) [5 marks] Let <code>g(x) = cos(x) - 1</code>. Compute degree 3 Taylor polynomial <code>T_3(x)</code> centered at <code>0</code>, and use Taylor's Theorem to show <code>|g(x) - T_3(x)| &le; x^4 / 24</code> for all <code>x &isin; R</code>.<br/>
        (b) [5 marks] For <code>f_n(x) = x&sup2; / (n + x&sup2;)</code> on <code>[0, 1]</code>, find the pointwise limit <i>f(x)</i> and prove <code>f_n &rarr; f</code> uniformly on <code>[0, 1]</code>.
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">PART (a) [5 MARKS]</span> Taylor Polynomial <code>T_3(x)</code> &amp; Lagrange Remainder Bound</div>
        <div class="step-desc">
          1. <b>Compute Derivatives at <code>a = 0</code>:</b><br/>
          <code>g(x) = cos(x) - 1 &rArr; g(0) = 0</code>; &nbsp; <code>g'(x) = -sin(x) &rArr; g'(0) = 0</code>;<br/>
          <code>g''(x) = -cos(x) &rArr; g''(0) = -1</code>; &nbsp; <code>g'''(x) = sin(x) &rArr; g'''(0) = 0</code>; &nbsp; <code>g^{(4)}(x) = cos(x)</code>.<br/>
          2. <b>Assemble <code>T_3(x)</code>:</b> <code>T_3(x) = g(0) + g'(0)x + [g''(0)/2!]x&sup2; + [g'''(0)/3!]x&sup3; = <b>-x&sup2; / 2</b></code>.<br/>
          3. <b>Apply Taylor's Theorem (Lagrange Remainder for <code>k = 3</code>):</b><br/>
          For any <code>x &isin; R</code>, by Taylor's Theorem there exists <code>c</code> between <code>0</code> and <code>x</code> such that:<br/>
          <code>g(x) - T_3(x) = R_3(x) = [ g^{(4)}(c) / 4! ] x^4 = [ cos(c) / 24 ] x^4</code>.<br/>
          Taking absolute values and using <code>|cos(c)| &le; 1</code> for all <code>c &isin; R</code>:<br/>
          <b><code>|g(x) - T_3(x)| = |cos(c)| &middot; |x|^4 / 24 &le; 1 &middot; x^4 / 24 = x^4 / 24</code></b>. &blacksquare;
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">PART (b) [5 MARKS]</span> Pointwise Limit &amp; Uniform Convergence via Supremum Norm <code>M_n</code></div>
        <div class="step-desc">
          1. <b>Pointwise Limit <code>f(x)</code>:</b> Fix any <code>x &isin; [0, 1]</code>. Since <code>x&sup2;</code> is constant with respect to <i>n</i> and <code>n + x&sup2; &rarr; &infin;</code> as <code>n &rarr; &infin;</code>, we have:<br/>
          <code>f(x) = lim_{n&rarr;&infin;} f_n(x) = lim_{n&rarr;&infin;} x&sup2; / (n + x&sup2;) = <b>0</b></code>. Thus <code>f(x) = 0</code> for all <code>x &isin; [0, 1]</code>.<br/>
          2. <b>Uniform Convergence Bound (Eliminate <i>x</i> uniformly!):</b><br/>
          For every <code>x &isin; [0, 1]</code>, the numerator satisfies <code>0 &le; x&sup2; &le; 1</code>, and the denominator satisfies <code>n + x&sup2; &ge; n &gt; 0</code>. Therefore:<br/>
          <code>|f_n(x) - f(x)| = | x&sup2; / (n + x&sup2;) - 0 | = x&sup2; / (n + x&sup2;) &le; 1 / n</code> &nbsp; for all <code>x &isin; [0, 1]</code>.<br/>
          3. Taking the supremum over <code>x &isin; [0, 1]</code> gives:<br/>
          <code>0 &le; M_n = sup_{x &isin; [0, 1]} |f_n(x) - f(x)| &le; 1 / n</code>.<br/>
          Since <code>lim_{n&rarr;&infin;} (1 / n) = 0</code>, by the Squeeze Theorem <code>lim_{n&rarr;&infin;} M_n = 0</code>. Hence <b><code>(f_n)</code> converges uniformly to <code>f = 0</code> on <code>[0, 1]</code></b>! &blacksquare;
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">HOW TO DISPROVE UNIFORM CONVERGENCE</div>
        <div class="sticky-content">
          To show <code>f_n(x) = x^n</code> on <code>[0, 1]</code> is <b>NOT</b> uniformly convergent: each <code>f_n</code> is continuous, but the pointwise limit <code>f(x) = 0</code> (on <code>[0,1)</code>) and <code>1</code> (at <code>x=1</code>) is discontinuous! (Uniform limit of continuous functions must be continuous).
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">TAYLOR DEGREE k REMAINDER INDEX</div>
        <div class="sticky-content">
          For degree <code>k</code> polynomial <code>T_k(x)</code>, the Lagrange remainder ALWAYS uses the <b><code>(k + 1)</code>-th derivative</b> divided by <b><code>(k + 1)!</code></b>: for <code>T_3(x)</code>, use <code>g^{(4)}(c) / 4!</code>!
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">050</span> MAST20026 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: SERIES & POWER SERIES (Q8)</div>
  <div>WORKED EXAMPLE: TAYLOR'S THEOREM & UNIFORM CONVERGENCE (Q9) &nbsp;·&nbsp; <span class="page-num">051</span></div>
</div>
""" + COMMON_FOOT
})

# Compile each spread individually to guarantee exactly 1 page per spread
master_doc = fitz.open()

print("Compiling individual MAST20026 spreads to guarantee strict 1-page per spread...")
for idx, mod in enumerate(modules):
    temp_pdf = os.path.join(BASE_DIR, f"temp_mast_spread_{idx+1}.pdf")
    compile_spread(mod["html"], temp_pdf)
    mod_doc = fitz.open(temp_pdf)
    print(f"[{mod['name']}] compiled with {len(mod_doc)} page(s).")
    master_doc.insert_pdf(mod_doc, from_page=0, to_page=0)
    mod_doc.close()

master_doc.save(OUT_PDF)
print(f"MAST20026 Master Full Edition saved to: {OUT_PDF} (Total spreads: {len(master_doc)})")

os.makedirs(os.path.dirname(COURSE_PDF), exist_ok=True)
shutil.copy2(OUT_PDF, COURSE_PDF)
print(f"Copied to course folder: {COURSE_PDF}")

for i in range(len(master_doc)):
    pix = master_doc[i].get_pixmap(dpi=130)
    prev_path = os.path.join(BASE_DIR, f"mast_spread_{i+1}.png")
    pix.save(prev_path)
    print(f"Rendered preview: {prev_path}")

master_doc.close()
print("MAST20026 Study Companion pipeline complete!")
