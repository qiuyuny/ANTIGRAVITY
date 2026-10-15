# -*- coding: utf-8 -*-
"""
COMP20003 Algorithms and Data Structures
Master Publication-Grade DK Study Companion Generator (Full Edition)
Compiles each module into a guaranteed 1-page A3 landscape spread,
then merges into one publication-grade master volume.
"""

import os
import subprocess
import fitz
import shutil

BASE_DIR = r"C:\Users\kakur\Desktop\COMP20003_Project 2"
OUT_PDF = r"C:\Users\kakur\Desktop\COMP20003_DK_Study_Companion_Full.pdf"
COURSE_PDF = r"C:\Users\kakur\Desktop\University\Semester_Current\COMP20003_Algo\COMP20003_DK_Study_Companion_Full.pdf"
TEMP_PROFILE = r"C:\Users\kakur\AppData\Local\Temp\edge_full_companion_profile"
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
    font-size: 19.5pt;
    font-weight: 300;
    letter-spacing: -0.03em;
    color: #0F172A;
    margin: 0;
    line-height: 1.05;
  }
  .title-block h1 b { font-weight: 800; color: #0284C7; }
  .title-block .subtitle {
    font-size: 7.6pt;
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
    padding: 3px 5px;
    margin: 2px 0;
  }
  .array-strip {
    display: flex;
    align-items: center;
    gap: 3px;
    margin: 1px 0;
  }
  .array-cell-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 32px;
  }
  .array-index {
    font-family: 'JetBrains Mono', monospace;
    font-size: 6.2pt;
    font-weight: 700;
    color: #64748B;
    margin-bottom: 1px;
  }
  .array-val {
    width: 32px;
    height: 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.8pt;
    font-weight: 800;
    color: #0F172A;
    background: #FFFFFF;
    border: 1.8px solid #334155;
    border-radius: 3px;
  }
  .array-val.active-swap { background: #FEF08A; border-color: #CA8A04; color: #854D0E; }
  .array-val.new-key { background: #BAE6FD; border-color: #0284C7; color: #0369A1; }
  .array-val.final-root { background: #DCFCE7; border-color: #16A34A; color: #15803D; }

  /* Step Badge */
  .step-pill {
    display: inline-block;
    background: #0F172A;
    color: #FFFFFF;
    font-size: 6.5pt;
    font-weight: 800;
    padding: 1px 5px;
    border-radius: 10px;
    margin-right: 4px;
    vertical-align: middle;
  }
  .step-pill.blue { background: #0284C7; }
  .step-pill.red { background: #DC2626; }
  .step-pill.green { background: #16A34A; }

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
    temp_html = os.path.join(BASE_DIR, "temp_spread.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        EDGE_PATH, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        f"--user-data-dir={TEMP_PROFILE}",
        f"--print-to-pdf={temp_pdf_path}", f"file:///{temp_html}"
    ]
    subprocess.run(cmd, capture_output=True, text=True)

# Define each module spread content
modules = []

# Module 1: C Memory, Pointers & Linked Lists
modules.append({
    "name": "Module 1 · C Memory & Pointers",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>010</b> | COMP20003 STUDY COMPANION &nbsp;·&nbsp; MODULE 1: C MEMORY & POINTERS</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §1.1 &ndash; §1.3] &nbsp;|&nbsp; <b>011</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 1 · <b>C Memory &amp; Pointers: Worked Execution Guide</b></h1>
        <div class="subtitle">Dynamic Allocation, String Boundaries &amp; Base Address Invariant &nbsp;·&nbsp; <span class="spec-ref">CROSS-REF SPEC §1.2</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] CORE MUST-KNOW</span>
        <span class="exam-stamp-sub">MEMORY & POINTERS · 15 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> String Duplication (malloc, strlen + 1, free Base-Address)</span>
        <span class="marks">LETHAL EXAM TRAP</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.8pt; margin: 2px 0;">
        <b>Past Exam Prompt:</b> <i>"Given string <code>s = \\"Algo\\"</code>. Allocate exact heap memory, duplicate characters, and show why calling <code>free()</code> after pointer traversal causes undefined heap corruption."</i>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">STEP 1</span> Allocate Exact Memory: <code>strlen(s) + 1</code></div>
        <div class="step-desc">
          <code>strlen(\\"Algo\\") = 4</code> (counts printable characters only!).<br/>
          To store null terminator <code>\\'\\0\\'</code>, allocation MUST be: <code>malloc(strlen(s) + 1) = 5 bytes</code>!<br/>
          <b>Omitting +1:</b> Causes buffer overflow overwrite into adjacent heap chunks &rarr; Memory Corruption!
        </div>
      </div>

      <div class="array-strip-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1px;">
          <span style="font-size: 6.8pt; font-weight: 800; color: #0F172A;"><span class="step-pill">MEMORY MAP</span> 5 Contiguous Heap Bytes (Base Address = 0x1000)</span>
          <span style="font-size: 6.4pt; color: #64748B;">char *base_ptr = 0x1000</span>
        </div>
        <div class="array-strip">
          <div class="array-cell-box"><span class="array-index">0x1000</span><div class="array-val final-root">\\'A\\'</div></div>
          <div class="array-cell-box"><span class="array-index">0x1001</span><div class="array-val">\\'l\\'</div></div>
          <div class="array-cell-box"><span class="array-index">0x1002</span><div class="array-val">\\'g\\'</div></div>
          <div class="array-cell-box"><span class="array-index">0x1003</span><div class="array-val">\\'o\\'</div></div>
          <div class="array-cell-box"><span class="array-index">0x1004</span><div class="array-val active-swap">\\'\\0\\'</div></div>
        </div>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">STEP 2</span> The Base-Address Invariant for <code>free(ptr)</code></div>
        <div class="step-desc">
          Suppose code traverses the string with: <code>while (*p) p++;</code>. Now pointer <code>p = 0x1004</code>.<br/>
          <b>FATAL BUG:</b> Calling <code>free(p)</code> passes an interior address! The C runtime heap manager only tracks the <b>allocation header</b> immediately preceding <code>0x1000</code>.<br/>
          <b>Rule:</b> You MUST save and pass the original base address: <code>free(base_ptr); base_ptr = NULL;</code>
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">DANGLING POINTER TRAP</div>
        <div class="sticky-content">
          <code>free(p)</code> releases memory back to OS, but <b>variable p still holds the old address!</b> Dereferencing <code>*p</code> afterwards is Undefined Behavior. Always set <code>p = NULL;</code>!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">SIZEOF STRUCT PADDING</div>
        <div class="sticky-content">
          Never hardcode struct sizes! Hardware word alignment inserts padding bytes. Always use <code>sizeof(struct student)</code> instead of summing field sizes.
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> Linked List Head Modification (Double Pointer <code>node_t **</code>)</span>
        <span class="marks">CRITICAL MECHANIC</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.8pt; margin: 2px 0;">
        <b>Past Exam Prompt:</b> <i>"Write a C function to delete the head of a singly linked list. Explain why <code>void deleteHead(node_t *head)</code> fails, and show the exact double pointer rewiring trace."</i>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">DIAGNOSIS</span> Why Single Pointer <code>(node_t *head)</code> Fails</div>
        <div class="step-desc">
          C parameters are strictly <b>pass-by-value</b>! The function receives a local copy of the head pointer. Reassigning <code>head = head-&gt;next;</code> only changes the local copy inside the function frame; the caller's head variable in <code>main()</code> remains completely unchanged!
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">SOLUTION</span> Double Pointer Rewiring Trace <code>(node_t **head_ref)</code></div>
        <div class="step-desc">
          Pass the memory address of the caller's head variable: <code>deleteHead(&amp;head);</code><br/>
          1. <b>Dereference once:</b> <code>node_t *old_head = *head_ref;</code> (points to 1st node).<br/>
          2. <b>Rewire caller's pointer:</b> <code>*head_ref = old_head-&gt;next;</code> (caller's head now points to 2nd node!).<br/>
          3. <b>Release memory:</b> <code>free(old_head);</code>. No memory leaks, caller successfully updated!
        </div>
      </div>

      <div class="array-strip-container" style="border-color: #86EFAC; background: #F0FDF4;">
        <div style="font-size: 6.8pt; font-weight: 800; color: #166534; margin-bottom: 2px;">
          <span class="step-pill" style="background: #16A34A;">VECTOR MAP</span> Double Pointer Indirection Flow
        </div>
        <pre class="mono" style="margin: 0; line-height: 1.15; font-size: 7.2pt; color: #0F172A;">
   Caller Frame (main):             Heap Memory:
   [ &head ] (0x7FFF)               [ Node 1 ] &rarr; [ Node 2 ] &rarr; NULL
        &darr;                               &uarr;             &uarr;
   deleteHead(head_ref):                |             |
   head_ref = 0x7FFF                    |             |
   *head_ref = old_head-&gt;next;  ========+=============+
   free(old_head);              (Node 1 safely reclaimed!)
        </pre>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">DYNAMIC ARRAY REALLOCATION</div>
        <div class="sticky-content">
          When array is full, double capacity: <code>new_cap = cap * 2</code>. Geometric doubling achieves <b>amortized O(1) append time</b>! Linear increment (+10) degrades append to <i>O</i>(<i>N</i>).
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">C MEMORY LEAKS CHECKLIST</div>
        <div class="sticky-content">
          Every successful <code>malloc()</code> must have exactly one corresponding <code>free()</code>. For linked lists, free nodes sequentially from head to tail: save <code>next</code> before calling <code>free(curr)</code>!
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">010</span> COMP20003 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: MALLOC & BASE ADDRESS</div>
  <div>WORKED EXAMPLE: DOUBLE POINTER LINKED LIST &nbsp;·&nbsp; <span class="page-num">011</span></div>
</div>
""" + COMMON_FOOT
})

# Module 2: Asymptotic Complexity & Recurrences
modules.append({
    "name": "Module 2 · Complexity & Recurrences",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>020</b> | COMP20003 STUDY COMPANION &nbsp;·&nbsp; MODULE 2: ASYMPTOTIC COMPLEXITY & RECURRENCES</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §2.1 &ndash; §2.3] &nbsp;|&nbsp; <b>021</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 2 · <b>Complexity &amp; Loops: Worked Analysis Guide</b></h1>
        <div class="subtitle">Loop Summations, Geometric Stepping &amp; Big-O Formal Bounds &nbsp;·&nbsp; <span class="spec-ref purple">CROSS-REF SPEC §2.2</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] CORE MUST-KNOW</span>
        <span class="exam-stamp-sub">COMPLEXITY ANALYSIS · 15 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Nested Loops with Geometric Step (i *= 2)</span>
        <span class="marks">HIGH EXAM YIELD</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.8pt; margin: 2px 0;">
        <b>Past Exam Code Snippet:</b><br/>
        <code>for (int i = 1; i &lt;= N; i *= 2) { for (int j = 0; j &lt; N; j++) { sum += A[i][j]; } }</code><br/>
        <b>Exam Task:</b> Formulate the exact summation, evaluate the closed-form bound, and state the tight Big-&Theta; complexity.
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">STEP 1</span> Trace Loop Iteration Frequencies</div>
        <div class="step-desc">
          &bull; <b>Outer Loop:</b> Value of <code>i</code> takes values <code>1, 2, 4, 8, ..., 2^k &le; N</code>.<br/>
          Solving <code>2^k &le; N</code> yields <code>k &le; &lfloor;log&sub2; N&rfloor;</code>. The outer loop executes exactly <b>&lfloor;log&sub2; N&rfloor; + 1 times</b>.<br/>
          &bull; <b>Inner Loop:</b> For every iteration of <code>i</code>, <code>j</code> runs from 0 to <code>N-1</code>, doing exactly <b>N iterations</b>.
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">STEP 2</span> Formulate and Evaluate Closed-Form Sum</div>
        <div class="step-desc">
          <code>Total Operations = &sum;_{k=0}^{\lfloor\log_2 N\rfloor} N = N &times; (&lfloor;\log_2 N\rfloor + 1) = N \log_2 N + N</code>.<br/>
          Dropping lower-order terms and constant coefficients &rarr; <b>Tight Bound: &Theta;(N log N)</b>!
        </div>
      </div>

      <div class="array-strip-container" style="border-color: #CBD5E1;">
        <div style="font-size: 6.8pt; font-weight: 800; color: #0F172A; margin-bottom: 2px;">
          <span class="step-pill">FORMAL BOUNDS</span> Mathematical Definitions Reference
        </div>
        <table class="exam-table" style="margin: 0;">
          <thead>
            <tr>
              <th>Notation</th>
              <th>Formal Mathematical Definition</th>
              <th>Exam Intuition</th>
            </tr>
          </thead>
          <tbody>
            <tr><td><b>Big-O: <i>O</i>(g(n))</b></td><td>&exist; <i>c</i> &gt; 0, <i>n</i>&sub0; &gt; 0 s.t. 0 &le; <i>f</i>(<i>n</i>) &le; <i>c</i> &middot; <i>g</i>(<i>n</i>), &forall; <i>n</i> &ge; <i>n</i>&sub0;</td><td><b>Upper bound</b> (Worst-case ceiling)</td></tr>
            <tr><td><b>Big-&Omega;: &Omega;(g(n))</b></td><td>&exist; <i>c</i> &gt; 0, <i>n</i>&sub0; &gt; 0 s.t. 0 &le; <i>c</i> &middot; <i>g</i>(<i>n</i>) &le; <i>f</i>(<i>n</i>), &forall; <i>n</i> &ge; <i>n</i>&sub0;</td><td><b>Lower bound</b> (Best-case floor)</td></tr>
            <tr class="highlight-row"><td><b>Big-&Theta;: &Theta;(g(n))</b></td><td><i>f</i>(<i>n</i>) &isin; <i>O</i>(<i>g</i>(<i>n</i>)) AND <i>f</i>(<i>n</i>) &isin; &Omega;(<i>g</i>(<i>n</i>)) simultaneously</td><td><b>Asymptotically tight</b> (Exact growth rate)</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">COMMON SUMMATION FORMULA</div>
        <div class="sticky-content">
          &bull; Arithmetic: <code>&sum;_{i=1}^N i = N(N+1)/2 &isin; &Theta;(N&sup2;)</code>.<br/>
          &bull; Geometric: <code>&sum;_{i=0}^k 2^i = 2^{k+1} - 1 &isin; &Theta;(2^k)</code>.<br/>
          &bull; Harmonic: <code>&sum;_{i=1}^N 1/i &isin; &Theta;(log N)</code>.
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">GROWTH HIERARCHY</div>
        <div class="sticky-content">
          <code>1 &lt; log log N &lt; log N &lt; &radic;N &lt; N &lt; N log N &lt; N&sup2; &lt; N&sup3; &lt; 2^N &lt; N!</code><br/>
          Polynomial always beats logarithmic; exponential crushes polynomial!
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> Recurrence Relation Unrolling (Repeated Substitution)</span>
        <span class="marks">MATHEMATICAL PROOF</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.8pt; margin: 2px 0;">
        <b>Past Exam Recurrence:</b> <code>T(N) = 2 T(N / 2) + cN</code>, with base case <code>T(1) = d</code>. (Divide-and-conquer pattern).<br/>
        <b>Exam Task:</b> Solve using repeated substitution (unrolling). Show step 1, 2, general pattern at step k, base case, and final Big-&Theta;.
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">STEP 1 &amp; 2</span> Substitute T(N/2) and T(N/4)</div>
        <div class="step-desc">
          &bull; <b>Step 1:</b> <code>T(N) = 2 [ 2 T(N/4) + c(N/2) ] + cN = 4 T(N/4) + 2cN</code>.<br/>
          &bull; <b>Step 2:</b> <code>T(N) = 4 [ 2 T(N/8) + c(N/4) ] + 2cN = 8 T(N/8) + 3cN</code>.
        </div>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">STEP 3</span> Identify General Invariant at Step k</div>
        <div class="step-desc">
          <code>T(N) = 2^k T(N / 2^k) + k &middot; cN</code>.<br/>
          The base case is reached when <code>N / 2^k = 1 &rarr; 2^k = N &rarr; k = \log_2 N</code>.
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">STEP 4</span> Substitute Base Case and Conclude</div>
        <div class="step-desc">
          Substitute <code>2^k = N</code> and <code>k = \log_2 N</code>:<br/>
          <code>T(N) = N &middot; T(1) + (\log_2 N) &middot; cN = d &middot; N + c &middot; N \log_2 N</code>.<br/>
          Leading term dominates &rarr; <b>Strict Linear-Logarithmic Bound: &Theta;(N log N)</b>!
        </div>
      </div>

      <!-- Master Theorem Decision Box -->
      <div class="array-strip-container" style="border-color: #86EFAC; background: #F0FDF4;">
        <div style="font-size: 6.8pt; font-weight: 800; color: #166534; margin-bottom: 2px;">
          <span class="step-pill" style="background: #16A34A;">MASTER THEOREM</span> Standard Form: <code>T(N) = a T(N / b) + f(N)</code> with critical exponent <code>c_{crit} = \log_b a</code>
        </div>
        <table class="exam-table" style="margin: 0;">
          <thead>
            <tr>
              <th>Case</th>
              <th>Condition Comparison</th>
              <th>Asymptotic Solution</th>
              <th>Classic Example</th>
            </tr>
          </thead>
          <tbody>
            <tr><td><b>Case 1: Leaves Dominate</b></td><td><code>f(N) = O(N^{c_{crit} - \epsilon})</code></td><td><code>T(N) = &Theta;(N^{\log_b a})</code></td><td>Strassen Matrix: <i>T(N)=7T(N/2)+O(N&sup2;) &rarr; &Theta;(N^{2.81})</i></td></tr>
            <tr class="highlight-row"><td><b>Case 2: Balanced Work</b></td><td><code>f(N) = &Theta;(N^{c_{crit}} \log^k N)</code></td><td><code>T(N) = &Theta;(N^{\log_b a} \log^{k+1} N)</code></td><td><b>Mergesort:</b> <i>T(N)=2T(N/2)+cN &rarr; &Theta;(N log N)</i></td></tr>
            <tr><td><b>Case 3: Root Dominates</b></td><td><code>f(N) = &Omega;(N^{c_{crit} + \epsilon})</code> + regularity</td><td><code>T(N) = &Theta;(f(N))</code></td><td><i>T(N)=2T(N/2)+N&sup2; &rarr; &Theta;(N&sup2;)</i></td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">MASTER THEOREM PITFALL</div>
        <div class="sticky-content">
          Cannot apply Master Theorem if <code>a</code> is not constant (e.g. <code>T(N) = 2^N T(N/2)</code>) or if <code>f(N)</code> is not polynomial (e.g. <code>T(N) = 2T(N/2) + N / \log N</code>). Use unrolling!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">BINARY SEARCH RECURRENCE</div>
        <div class="sticky-content">
          <code>T(N) = T(N/2) + O(1)</code> &rarr; <code>a = 1, b = 2, c_{crit} = \log_2 1 = 0</code>. Case 2 gives <b>&Theta;(log N)</b>!
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">020</span> COMP20003 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: LOOP SUMMATION</div>
  <div>WORKED EXAMPLE: RECURRENCE UNROLLING &nbsp;·&nbsp; <span class="page-num">021</span></div>
</div>
""" + COMMON_FOOT
})


# Module 3: Trees & AVL
modules.append({
    "name": "Module 3 · AVL Balanced Trees",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>030</b> | COMP20003 STUDY COMPANION &nbsp;·&nbsp; MODULE 3: BALANCED SEARCH TREES</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §3.1 &ndash; §3.4] &nbsp;|&nbsp; <b>031</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 3 · <b>AVL Trees: Worked Balance & Rotation Guide</b></h1>
        <div class="subtitle">Step-by-step Balance Factors &amp; Pointer Rewiring &nbsp;·&nbsp; <span class="spec-ref purple">CROSS-REF SPEC §3.3</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] CORE MUST-KNOW</span>
        <span class="exam-stamp-sub">AVL ROTATIONS · 15-20 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> AVL Balance Factor &amp; Single Right (LL) Rotation</span>
        <span class="marks">CRITICAL MECHANIC</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.8pt; margin: 2px 0;">
        <b>Past Exam Prompt:</b> <i>"Given a valid AVL tree with keys <code>[30, 20]</code>. Key <b>10</b> is inserted. Compute Balance Factor BF = H(left) - H(right) for every ancestor, identify the imbalance type, and draw the rotated tree."</i>
      </div>

      <div style="background: #EFF6FF; border: 1.2px solid #BFDBFE; border-radius: 4px; padding: 2.5px 6px; margin: 2px 0; font-size: 6.7pt;">
        <b>AVL Invariant:</b> For every node, balance factor <code>BF &isin; {-1, 0, +1}</code>. If <code>|BF| &ge; 2</code>, the tree is INVALID and requires an immediate rotation at the <b>lowest unbalanced ancestor</b>!
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">STEP 1</span> BST Insert Key 10 &amp; Compute Balance Factors</div>
        <div class="step-desc">
          &bull; Node 10 inserted as left child of 20. Height = 0, <code>BF(10) = 0</code>.<br/>
          &bull; Parent 20: Left height = 0, right = -1 &rarr; <code>BF(20) = 0 - (-1) = +1</code> (OK).<br/>
          &bull; Root 30: Left child height = 1, right = -1 &rarr; <b><code>BF(30) = 1 - (-1) = +2 &ge; 2 (IMBALANCE!)</code></b>
        </div>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">STEP 2</span> Classify Imbalance: <b>LL Case (Left-Left)</b></div>
        <div class="step-desc">
          Imbalance discovered at node <b>30</b>. Cause: new key was inserted into the <b>Left</b> subtree of its <b>Left</b> child (20 &rarr; 10).<br/>
          <b>Prescription:</b> Exactly <b>ONE Single Right Rotation</b> around node 30!
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">STEP 3</span> Execute Single Right Rotation (Clockwise)</div>
        <div class="step-desc">
          1. Node <b>20</b> rises to become the new root of this subtree.<br/>
          2. Node <b>30</b> is pushed down to become the <b>right child</b> of 20.<br/>
          3. Any right subtree of 20 (if present) is handed over to become the left subtree of 30.<br/>
          <b>Result:</b> Root = <b>20</b>, Left Child = <b>10</b>, Right Child = <b>30</b>. All BFs are now <b>0</b>!
        </div>
      </div>

      <div class="array-strip-container" style="background: #F8FAFC; border-color: #86EFAC;">
        <div style="font-size: 6.8pt; font-weight: 800; color: #166534; margin-bottom: 2px;">
          <span class="step-pill" style="background: #16A34A;">VECTOR MAP</span> Before Rotation (Chain) vs After Rotation (Balanced)
        </div>
        <pre class="mono" style="margin: 0; line-height: 1.15; font-size: 7.2pt; color: #0F172A;">
   BEFORE (LL Imbalance at 30):           AFTER (Single Right Rotation):
         30 [BF = +2]  &larr; Pivot                     20 [BF = 0]
        /                                         /    \
      20 [BF = +1]             ======&gt;          10      30
     /                                        [BF=0]  [BF=0]
   10 [BF = 0]                                (Balanced O(log N) Height!)
        </pre>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">ROTATION DECISION MATRIX</div>
        <div class="sticky-content">
          &bull; <b>BF(Root) = +2, BF(Left) = +1</b> &rarr; <b>LL</b>: Single Right.<br/>
          &bull; <b>BF(Root) = -2, BF(Right) = -1</b> &rarr; <b>RR</b>: Single Left.<br/>
          &bull; <b>BF(Root) = +2, BF(Left) = -1</b> &rarr; <b>LR</b>: Double (Left then Right).<br/>
          &bull; <b>BF(Root) = -2, BF(Right) = +1</b> &rarr; <b>RL</b>: Double (Right then Left).
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">HEIGHT vs DEPTH FORMULA</div>
        <div class="sticky-content">
          <b>Empty tree height = -1</b>, Leaf height = 0.<br/>
          <code>Height(u) = 1 + max(Height(left), Height(right))</code>.<br/>
          Always recalculate heights from bottom up!
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> LR Double Rotation Step-by-Step (The "Zig-Zag" Case)</span>
        <span class="marks">MOST TESTED TRAP</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.8pt; margin: 2px 0;">
        <b>Past Exam Prompt:</b> <i>"Given tree with keys <code>[30, 10]</code>. Key <b>20</b> is inserted. Show why a single rotation fails, trace the two constituent rotations, and write the final tree structure."</i>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">DIAGNOSIS</span> Why Single Rotation FAILS on Zig-Zag (LR)</div>
        <div class="step-desc">
          Node 20 is inserted as the <b>right child of 10</b>. Root 30 has <code>BF = +2</code>, but child 10 has <code>BF = -1</code> (opposite signs!).<br/>
          A single right rotation around 30 produces an equally crooked tree. A <b>Double Rotation</b> is mathematically mandatory!
        </div>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">PHASE 1</span> Left Rotation on Child Node 10 (Straightens Zig-Zag into LL)</div>
        <div class="step-desc">
          Rotate child node <b>10 counter-clockwise</b>:<br/>
          &bull; Node <b>20</b> rises to become the left child of 30.<br/>
          &bull; Node <b>10</b> becomes the left child of 20.<br/>
          <b>State:</b> The tree is now a straight <b>LL configuration</b>: <code>30 &rarr; 20 &rarr; 10</code>!
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">PHASE 2</span> Right Rotation on Root Node 30 (Restores Balance)</div>
        <div class="step-desc">
          Rotate root node <b>30 clockwise</b> around 20:<br/>
          &bull; Node <b>20</b> ascends to become the global root!<br/>
          &bull; Node <b>30</b> descends to become the right child of 20.<br/>
          &bull; Node <b>10</b> remains the left child of 20.<br/>
          <b>Final Valid AVL:</b> Root = <b>20</b>, Left = <b>10</b>, Right = <b>30</b>. Perfectly balanced!
        </div>
      </div>

      <div class="array-strip-container" style="background: #F8FAFC; border-color: #86EFAC;">
        <div style="font-size: 6.8pt; font-weight: 800; color: #166534; margin-bottom: 2px;">
          <span class="step-pill" style="background: #16A34A;">VECTOR MAP</span> Phase 1 &amp; Phase 2 Double Rotation Flow
        </div>
        <pre class="mono" style="margin: 0; line-height: 1.15; font-size: 7.2pt; color: #0F172A;">
   RAW INSERT (LR):           PHASE 1 (Rotate Left 10):      PHASE 2 (Rotate Right 30):
        30 [BF=+2]                     30 [BF=+2]                    20 [BF=0]
       /                              /                             /    \
     10 [BF=-1]    ======&gt;          20 [BF=+1]    ======&gt;         10      30
       \                           /                            [BF=0]  [BF=0]
        20 [BF=0]                10 [BF=0]                     (PERFECT BALANCE!)
        </pre>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">EXAMINER 2-CHILD DELETION TRICK</div>
        <div class="sticky-content">
          To delete node with 2 children: <b>swap with In-order Successor</b> (smallest key in right subtree) OR <b>In-order Predecessor</b> (largest in left). Then delete the leaf!
        </div>
      </div>
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">TIME COMPLEXITY SUMMARY</div>
        <div class="sticky-content">
          &bull; <b>Search:</b> <i>O</i>(log <i>N</i>) worst-case.<br/>
          &bull; <b>Insert:</b> <i>O</i>(log <i>N</i>) search + at most <b>1 rotation</b> (single or double) &rarr; <i>O</i>(log <i>N</i>).<br/>
          &bull; <b>Delete:</b> <i>O</i>(log <i>N</i>) search + up to <b><i>O</i>(log <i>N</i>) rotations</b> up to root!
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">030</span> COMP20003 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: LL SINGLE ROTATION</div>
  <div>WORKED EXAMPLE: LR DOUBLE ROTATION &nbsp;·&nbsp; <span class="page-num">031</span></div>
</div>
""" + COMMON_FOOT
})

# Module 4: Binary Heap (from our tested worked example)
modules.append({
    "name": "Module 4 · Priority Queues & Heaps",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>040</b> | COMP20003 STUDY COMPANION &nbsp;·&nbsp; MODULE 4: PRIORITY QUEUES & HEAPS</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §4.1 &ndash; §4.3] &nbsp;|&nbsp; <b>041</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 4 · <b>The Binary Heap: Worked Trace Guide</b></h1>
        <div class="subtitle">Concrete Worked Examples with Numbers &nbsp;·&nbsp; <span class="spec-ref">CROSS-REF SPEC §4.2.4</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] CORE MUST-KNOW</span>
        <span class="exam-stamp-sub">WORKED TRACES · 15-20 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Up-Heap (Insert 15 into Max-Heap of size N = 6)</span>
        <span class="marks">HIGH EXAM YIELD</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.8pt; margin: 2px 0;">
        <b>Past Exam Prompt:</b> <i>"Given a 1-based max-heap array <code>A = [16, 14, 10, 8, 7, 9]</code>. Trace inserting <b>15</b>. Show every comparison, pointer index, and the final array state."</i>
      </div>

      <div class="array-strip-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1px;">
          <span style="font-size: 6.8pt; font-weight: 800; color: #0F172A;"><span class="step-pill">STATE 0</span> Initial Array (N = 6, Valid Max-Heap)</span>
          <span style="font-size: 6.4pt; color: #64748B;">Root at index 1</span>
        </div>
        <div class="array-strip">
          <div class="array-cell-box"><span class="array-index">i = 1</span><div class="array-val">16</div></div>
          <div class="array-cell-box"><span class="array-index">i = 2</span><div class="array-val">14</div></div>
          <div class="array-cell-box"><span class="array-index">i = 3</span><div class="array-val">10</div></div>
          <div class="array-cell-box"><span class="array-index">i = 4</span><div class="array-val">8</div></div>
          <div class="array-cell-box"><span class="array-index">i = 5</span><div class="array-val">7</div></div>
          <div class="array-cell-box"><span class="array-index">i = 6</span><div class="array-val">9</div></div>
          <div class="array-cell-box"><span class="array-index">i = 7</span><div class="array-val" style="border-style: dashed; color: #94A3B8;">&empty;</div></div>
        </div>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">STEP 1</span> Append Key at Frontier <code>A[N+1]</code> &rarr; <code>N = 7</code></div>
        <div class="step-desc">
          Put <b>15</b> at next open slot <code>A[7]</code>. Parent is at index <code>&lfloor;7 / 2&rfloor; = 3</code> (holding value <b>10</b>).<br/>
          <b>Comparison 1:</b> Compare <code>A[7]</code> (15) with parent <code>A[3]</code> (10). Since <b>15 &gt; 10</b>, heap order is violated &rarr; <b>SWAP <code>A[7]</code> and <code>A[3]</code>!</b>
        </div>
      </div>

      <div class="array-strip-container">
        <div style="font-size: 6.8pt; font-weight: 800; color: #CA8A04; margin-bottom: 1px;">
          <span class="step-pill" style="background: #CA8A04;">STATE 1</span> After First Swap (15 moved to index 3, 10 pushed to index 7)
        </div>
        <div class="array-strip">
          <div class="array-cell-box"><span class="array-index">i = 1</span><div class="array-val">16</div></div>
          <div class="array-cell-box"><span class="array-index">i = 2</span><div class="array-val">14</div></div>
          <div class="array-cell-box"><span class="array-index">i = 3</span><div class="array-val active-swap">15</div></div>
          <div class="array-cell-box"><span class="array-index">i = 4</span><div class="array-val">8</div></div>
          <div class="array-cell-box"><span class="array-index">i = 5</span><div class="array-val">7</div></div>
          <div class="array-cell-box"><span class="array-index">i = 6</span><div class="array-val">9</div></div>
          <div class="array-cell-box"><span class="array-index">i = 7</span><div class="array-val active-swap">10</div></div>
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">STEP 2</span> Sift Up &amp; Verify Root Invariant</div>
        <div class="step-desc">
          Current index of 15 is <code>i = 3</code>. Parent is at index <code>&lfloor;3 / 2&rfloor; = 1</code> (holding value <b>16</b>).<br/>
          <b>Comparison 2:</b> Compare <code>A[3]</code> (15) with parent <code>A[1]</code> (16). Since <b>15 &le; 16</b>, heap order is satisfied &rarr; <b>STOP!</b>
        </div>
      </div>

      <div class="array-strip-container" style="border-color: #86EFAC; background: #F0FDF4;">
        <div style="font-size: 6.8pt; font-weight: 800; color: #166534; margin-bottom: 1px;">
          <span class="step-pill" style="background: #16A34A;">FINAL</span> Resulting Array: <code>[16, 14, 15, 8, 7, 9, 10]</code> &nbsp;&bull;&nbsp; Total Comparisons = <b>2</b>
        </div>
        <div class="array-strip">
          <div class="array-cell-box"><span class="array-index">i = 1</span><div class="array-val final-root">16</div></div>
          <div class="array-cell-box"><span class="array-index">i = 2</span><div class="array-val">14</div></div>
          <div class="array-cell-box"><span class="array-index">i = 3</span><div class="array-val new-key">15</div></div>
          <div class="array-cell-box"><span class="array-index">i = 4</span><div class="array-val">8</div></div>
          <div class="array-cell-box"><span class="array-index">i = 5</span><div class="array-val">7</div></div>
          <div class="array-cell-box"><span class="array-index">i = 6</span><div class="array-val">9</div></div>
          <div class="array-cell-box"><span class="array-index">i = 7</span><div class="array-val">10</div></div>
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">UP-HEAP ASYMMETRY RULE</div>
        <div class="sticky-content">
          <b>Comparisons per level = exactly 1.</b> Node only checks its single parent. Worst-case comparisons &le; &lfloor;log&sub2; <i>N</i>&rfloor; = 2 comparisons for <i>N</i> = 7!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">CHEATSHEET RAPID ANCHOR</div>
        <div class="sticky-content">
          &bull; <b>Leaf Indices:</b> &lfloor;7/2&rfloor; + 1 = 4 &rarr; Indices 4, 5, 6, 7 are leaves.<br/>
          &bull; <b>Formulas Table:</b> See <code>COMP20003_Full_Exam_Spec.pdf</code> &sect;4.2.2.
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> Floyd's Bottom-Up <code>makeHeap</code> (N = 7, &Theta;(N) Trace)</span>
        <span class="marks">MATHEMATICAL PROOF</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.8pt; margin: 2px 0;">
        <b>Past Exam Prompt:</b> <i>"Given raw unsorted array <code>A = [4, 10, 3, 5, 1, 9, 2]</code>. Trace Floyd's bottom-up build algorithm. Show which node is downheaped first, every pass, and the final valid max-heap."</i>
      </div>

      <div style="background: #EFF6FF; border: 1.2px solid #BFDBFE; border-radius: 4px; padding: 2.5px 6px; margin: 2px 0; font-size: 6.7pt;">
        <b>Execution Axiom:</b> Leaves require 0 downheaps! Loop begins strictly at <b>last internal node</b>:
        <code>i_start = &lfloor;7 / 2&rfloor; = 3</code>. Order: <code>downheap(3)</code> &rarr; <code>downheap(2)</code> &rarr; <code>downheap(1)</code>.
      </div>

      <div class="array-strip-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1px;">
          <span style="font-size: 6.8pt; font-weight: 800; color: #0F172A;"><span class="step-pill">STATE 0</span> Raw Unsorted Array (Before Heapify)</span>
          <span style="font-size: 6.4pt; color: #64748B;">Internal nodes: 1, 2, 3</span>
        </div>
        <div class="array-strip">
          <div class="array-cell-box"><span class="array-index">i = 1</span><div class="array-val">4</div></div>
          <div class="array-cell-box"><span class="array-index">i = 2</span><div class="array-val">10</div></div>
          <div class="array-cell-box"><span class="array-index">i = 3</span><div class="array-val active-swap">3</div></div>
          <div class="array-cell-box"><span class="array-index">i = 4</span><div class="array-val">5</div></div>
          <div class="array-cell-box"><span class="array-index">i = 5</span><div class="array-val">1</div></div>
          <div class="array-cell-box"><span class="array-index">i = 6</span><div class="array-val active-swap">9</div></div>
          <div class="array-cell-box"><span class="array-index">i = 7</span><div class="array-val">2</div></div>
        </div>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">PASS 1</span> <code>i = 3</code>: Subtree rooted at <code>A[3] = 3</code> (Children: <code>A[6] = 9</code>, <code>A[7] = 2</code>)</div>
        <div class="step-desc">
          1. <b>Compare children:</b> 9 vs 2 &rarr; larger child is <b>9</b> at index 6.<br/>
          2. <b>Compare with parent:</b> 9 &gt; 3 &rarr; <b>SWAP <code>A[3]</code> and <code>A[6]</code>!</b> Array: <code>[4, 10, <b>9</b>, 5, 1, <b>3</b>, 2]</code>. (2 comparisons)
        </div>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">PASS 2</span> <code>i = 2</code>: Subtree rooted at <code>A[2] = 10</code> (Children: <code>A[4] = 5</code>, <code>A[5] = 1</code>)</div>
        <div class="step-desc">
          1. <b>Compare children:</b> 5 vs 1 &rarr; larger child is <b>5</b> at index 4.<br/>
          2. <b>Compare with parent:</b> 10 &ge; 5 &rarr; <b>No violation! No swap!</b> Array stays: <code>[4, 10, 9, 5, 1, 3, 2]</code>. (2 comparisons)
        </div>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">PASS 3</span> <code>i = 1</code>: Subtree rooted at <code>A[1] = 4</code> (Two-level Domino Downheap!)</div>
        <div class="step-desc">
          &bull; <b>Level 1:</b> Compare children 10 vs 9 &rarr; larger 10. Compare 10 &gt; 4 &rarr; <b>SWAP <code>A[1]</code> &amp; <code>A[2]</code>!</b><br/>
          &bull; <b>Level 2 (Follow 4 to index 2):</b> Children are 5 and 1. Larger is 5. Compare 5 &gt; 4 &rarr; <b>SWAP <code>A[2]</code> &amp; <code>A[4]</code>!</b>
        </div>
      </div>

      <div class="array-strip-container" style="border-color: #86EFAC; background: #F0FDF4;">
        <div style="font-size: 6.8pt; font-weight: 800; color: #166534; margin-bottom: 1px;">
          <span class="step-pill" style="background: #16A34A;">FINAL</span> Built Max-Heap: <code>[10, 5, 9, 4, 1, 3, 2]</code> &nbsp;&bull;&nbsp; Root is Global Max (10)
        </div>
        <div class="array-strip">
          <div class="array-cell-box"><span class="array-index">i = 1</span><div class="array-val final-root">10</div></div>
          <div class="array-cell-box"><span class="array-index">i = 2</span><div class="array-val">5</div></div>
          <div class="array-cell-box"><span class="array-index">i = 3</span><div class="array-val">9</div></div>
          <div class="array-cell-box"><span class="array-index">i = 4</span><div class="array-val">4</div></div>
          <div class="array-cell-box"><span class="array-index">i = 5</span><div class="array-val">1</div></div>
          <div class="array-cell-box"><span class="array-index">i = 6</span><div class="array-val">3</div></div>
          <div class="array-cell-box"><span class="array-index">i = 7</span><div class="array-val">2</div></div>
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">DOWN-HEAP ASYMMETRY RULE</div>
        <div class="sticky-content">
          <b>Comparisons per level = exactly 2.</b><br/>
          &bull; <i>Comp 1:</i> Compare left vs right child to pick the winner.<br/>
          &bull; <i>Comp 2:</i> Compare the winner against the parent node.
        </div>
      </div>
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">LETHAL 0-MARKS TRAP</div>
        <div class="sticky-content">
          <b>Pitfall:</b> Writing Floyd takes <i>O</i>(<i>N</i> log <i>N</i>) because it calls downheap <i>N</i>/2 times.<br/>
          <b>Full Mark:</b> Height is low for most nodes! &sum; (<i>h</i> / 2<sup><i>h</i></sup>) converges to 2 &rarr; <b>strict &Theta;(<i>N</i>) linear time</b>.
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">040</span> COMP20003 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: UP-HEAP TRACE</div>
  <div>WORKED EXAMPLE: FLOYD HEAPIFY TRACE &nbsp;·&nbsp; <span class="page-num">041</span></div>
</div>
""" + COMMON_FOOT
})

# Module 5: Hash Tables
modules.append({
    "name": "Module 5 · Hash Tables & Collisions",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>050</b> | COMP20003 STUDY COMPANION &nbsp;·&nbsp; MODULE 5: HASH TABLES & COLLISIONS</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §5.1 &ndash; §5.2] &nbsp;|&nbsp; <b>051</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 5 · <b>Hash Tables: Worked Collision & Probe Guide</b></h1>
        <div class="subtitle">Exact Probe Counts &amp; Clustering Avoidance &nbsp;·&nbsp; <span class="spec-ref orange">CROSS-REF SPEC §5.2</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] CORE MUST-KNOW</span>
        <span class="exam-stamp-sub">PROBE TRACES · 10-15 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Linear Probing Insertion &amp; Probe Counting (M = 7)</span>
        <span class="marks">PROBE COUNT FORMULA</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.8pt; margin: 2px 0;">
        <b>Past Exam Prompt:</b> <i>"Given hash table size M = 7 with hash function h(k) = k mod 7. Insert keys <code>[10, 17, 24, 8]</code> using Linear Probing. Record each probe count and show final table state."</i>
      </div>

      <div style="background: #EFF6FF; border: 1.2px solid #BFDBFE; border-radius: 4px; padding: 2.5px 6px; margin: 2px 0; font-size: 6.7pt;">
        <b>Probe Formula:</b> <code>h_i(k) = (h(k) + i) mod M</code> for <code>i = 0, 1, 2, ...</code><br/>
        <b>CRITICAL EXAM RULE:</b> A "probe" is counted for <b>EVERY slot inspected</b>, including the home slot and the final empty slot where insertion succeeds!
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">KEY 10</span> <code>h(10) = 10 mod 7 = 3</code></div>
        <div class="step-desc">Slot 3 is empty. Insert 10 at <code>T[3]</code>. <b>Probes = 1</b> (inspected slot 3).</div>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">KEY 17</span> <code>h(17) = 17 mod 7 = 3</code> (Collision!)</div>
        <div class="step-desc">
          &bull; Probe 1: Slot 3 occupied by 10 &rarr; collision!<br/>
          &bull; Probe 2: Try <code>(3 + 1) mod 7 = 4</code>. Slot 4 is empty. Insert 17 at <code>T[4]</code>. <b>Probes = 2</b>.
        </div>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">KEY 24</span> <code>h(24) = 24 mod 7 = 3</code> (Double Collision!)</div>
        <div class="step-desc">
          &bull; Probe 1: Slot 3 occupied (10).<br/>
          &bull; Probe 2: Slot 4 occupied (17).<br/>
          &bull; Probe 3: Try <code>(3 + 2) mod 7 = 5</code>. Slot 5 is empty. Insert 24 at <code>T[5]</code>. <b>Probes = 3</b>.
        </div>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">KEY 8</span> <code>h(8) = 8 mod 7 = 1</code></div>
        <div class="step-desc">Slot 1 is empty. Insert 8 at <code>T[1]</code>. <b>Probes = 1</b>.</div>
      </div>

      <div class="array-strip-container" style="border-color: #CA8A04;">
        <div style="font-size: 6.8pt; font-weight: 800; color: #854D0E; margin-bottom: 1px;">
          <span class="step-pill" style="background: #CA8A04;">FINAL TABLE</span> Primary Cluster formed at slots 3, 4, 5 &bull; Total Probes = 1 + 2 + 3 + 1 = <b>7</b>
        </div>
        <div class="array-strip">
          <div class="array-cell-box"><span class="array-index">0</span><div class="array-val" style="color: #94A3B8;">&empty;</div></div>
          <div class="array-cell-box"><span class="array-index">1</span><div class="array-val">8</div></div>
          <div class="array-cell-box"><span class="array-index">2</span><div class="array-val" style="color: #94A3B8;">&empty;</div></div>
          <div class="array-cell-box"><span class="array-index">3</span><div class="array-val active-swap">10</div></div>
          <div class="array-cell-box"><span class="array-index">4</span><div class="array-val active-swap">17</div></div>
          <div class="array-cell-box"><span class="array-index">5</span><div class="array-val active-swap">24</div></div>
          <div class="array-cell-box"><span class="array-index">6</span><div class="array-val" style="color: #94A3B8;">&empty;</div></div>
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">PRIMARY CLUSTERING FLAW</div>
        <div class="sticky-content">
          Linear probing causes adjacent occupied slots to merge into long runs. Any key that lands anywhere in the cluster must traverse the whole cluster!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">LOAD FACTOR &alpha; LIMITS</div>
        <div class="sticky-content">
          <code>&alpha; = N / M</code>. In Linear Probing, &alpha; MUST be &le; 1.0 (performance degrades drastically when &alpha; &gt; 0.7). In Separate Chaining, &alpha; can exceed 1.0!
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> Double Hashing Step-by-Step (Eliminating Clustering)</span>
        <span class="marks">EXAM MANDATORY RULES</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.8pt; margin: 2px 0;">
        <b>Past Exam Prompt:</b> <i>"Given M = 7, h1(k) = k mod 7, and secondary hash h2(k) = 5 - (k mod 5). Insert keys <code>[10, 17]</code> using Double Hashing. Show how collision resolution jumps differ from linear probing."</i>
      </div>

      <div style="background: #FFF1F2; border: 1.2px solid #FECDD3; border-radius: 4px; padding: 2.5px 6px; margin: 2px 0; font-size: 6.7pt;">
        <b>THE TWO MANDATORY RULES FOR h2(k):</b><br/>
        1. <b><code>h2(k) &ne; 0</code> for all keys</b> (otherwise step size is 0 &rarr; infinite loop on same slot!).<br/>
        2. <b><code>gcd(h2(k), M) == 1</code></b> (step size and table size must be coprime so ALL M slots are reachable).
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">KEY 10</span> <code>h1(10) = 10 mod 7 = 3</code></div>
        <div class="step-desc">Slot 3 is empty. Insert 10 at <code>T[3]</code>. <b>Probes = 1</b>.</div>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">KEY 17</span> <code>h1(17) = 3</code> (Collision!) &rarr; Calculate Custom Step <code>h2(17)</code></div>
        <div class="step-desc">
          &bull; Probe 1: Slot 3 occupied by 10.<br/>
          &bull; Step calculation: <code>h2(17) = 5 - (17 mod 5) = 5 - 2 = 3</code>.<br/>
          &bull; Probe 2: Try <code>(h1 + 1 &times; h2) mod M = (3 + 3) mod 7 = 6</code>.<br/>
          &bull; Slot 6 is empty! Insert 17 at <code>T[6]</code>. <b>Probes = 2</b>.
        </div>
      </div>

      <div class="array-strip-container" style="border-color: #16A34A; background: #F0FDF4;">
        <div style="font-size: 6.8pt; font-weight: 800; color: #166534; margin-bottom: 1px;">
          <span class="step-pill" style="background: #16A34A;">SCATTERED RESULT</span> Keys dispersed across table without forming consecutive clusters!
        </div>
        <div class="array-strip">
          <div class="array-cell-box"><span class="array-index">0</span><div class="array-val" style="color: #94A3B8;">&empty;</div></div>
          <div class="array-cell-box"><span class="array-index">1</span><div class="array-val" style="color: #94A3B8;">&empty;</div></div>
          <div class="array-cell-box"><span class="array-index">2</span><div class="array-val" style="color: #94A3B8;">&empty;</div></div>
          <div class="array-cell-box"><span class="array-index">3</span><div class="array-val active-swap">10</div></div>
          <div class="array-cell-box"><span class="array-index">4</span><div class="array-val" style="color: #94A3B8;">&empty;</div></div>
          <div class="array-cell-box"><span class="array-index">5</span><div class="array-val" style="color: #94A3B8;">&empty;</div></div>
          <div class="array-cell-box"><span class="array-index">6</span><div class="array-val new-key">17</div></div>
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">SEARCH DELETION TOMBSTONE TRAP</div>
        <div class="sticky-content">
          In open addressing, you CANNOT simply set a slot to empty when deleting! A vacant slot terminates future searches prematurely. You MUST mark it as <b>TOMBSTONE (Deleted)</b>!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">AVERAGE SEARCH COMPLEXITY</div>
        <div class="sticky-content">
          &bull; <b>Separate Chaining:</b> Successful search &asymp; <code>1 + &alpha;/2</code>.<br/>
          &bull; <b>Linear Probing:</b> Successful &asymp; <code>0.5 &times; (1 + 1/(1-&alpha;))</code>.<br/>
          Always choose <b>M = Prime</b> to break patterns!
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">050</span> COMP20003 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: LINEAR PROBING</div>
  <div>WORKED EXAMPLE: DOUBLE HASHING TRACE &nbsp;·&nbsp; <span class="page-num">051</span></div>
</div>
""" + COMMON_FOOT
})

# Module 6: Sorting
modules.append({
    "name": "Module 6 · Sorting Algorithms",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>060</b> | COMP20003 STUDY COMPANION &nbsp;·&nbsp; MODULE 6: SORTING ALGORITHMS</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §6.1 &ndash; §6.5] &nbsp;|&nbsp; <b>061</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 6 · <b>Quicksort: Hoare Partition Worked Guide</b></h1>
        <div class="subtitle">Two-Pointer Inversion Swaps &amp; Pivot Invariant &nbsp;·&nbsp; <span class="spec-ref">CROSS-REF SPEC §6.3</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] CORE MUST-KNOW</span>
        <span class="exam-stamp-sub">HOARE TRACE · 15-20 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Hoare Two-Pointer Partition Step-by-Step</span>
        <span class="marks">EXAM TRACE PROTOCOL</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.8pt; margin: 2px 0;">
        <b>Past Exam Prompt:</b> <i>"Given subarray <code>A = [5, 3, 8, 4, 2, 7, 1, 9]</code>. Pivot is leftmost item p = 5. Trace Hoare's two-pointer partition. Show every pointer movement of L and R, all element swaps, and final pivot position."</i>
      </div>

      <div class="array-strip-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1px;">
          <span style="font-size: 6.8pt; font-weight: 800; color: #0F172A;"><span class="step-pill">STATE 0</span> Initial Array (Pivot p = A[0] = 5, L = 1, R = 7)</span>
        </div>
        <div class="array-strip">
          <div class="array-cell-box"><span class="array-index">0 (P)</span><div class="array-val final-root">5</div></div>
          <div class="array-cell-box"><span class="array-index">1 (L)</span><div class="array-val">3</div></div>
          <div class="array-cell-box"><span class="array-index">2</span><div class="array-val">8</div></div>
          <div class="array-cell-box"><span class="array-index">3</span><div class="array-val">4</div></div>
          <div class="array-cell-box"><span class="array-index">4</span><div class="array-val">2</div></div>
          <div class="array-cell-box"><span class="array-index">5</span><div class="array-val">7</div></div>
          <div class="array-cell-box"><span class="array-index">6</span><div class="array-val">1</div></div>
          <div class="array-cell-box"><span class="array-index">7 (R)</span><div class="array-val">9</div></div>
        </div>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">STEP 1</span> Advance Pointers to Find Inversion</div>
        <div class="step-desc">
          &bull; Advance <b>L right</b> while <code>A[L] &lt; p</code>: Skips 3 (&lt;5). Stops on <b>8</b> at <code>L = 2</code> (8 &ge; 5).<br/>
          &bull; Advance <b>R left</b> while <code>A[R] &gt; p</code>: Skips 9 (&gt;5), skips 7 (&gt;5). Stops on <b>1</b> at <code>R = 6</code> (1 &le; 5).<br/>
          Since <code>L &lt; R</code> (2 &lt; 6), an inversion exists &rarr; <b>SWAP <code>A[2]</code> and <code>A[6]</code>!</b>
        </div>
      </div>

      <div class="array-strip-container">
        <div style="font-size: 6.8pt; font-weight: 800; color: #CA8A04; margin-bottom: 1px;">
          <span class="step-pill" style="background: #CA8A04;">STATE 1</span> After First Swap (8 and 1 swapped)
        </div>
        <div class="array-strip">
          <div class="array-cell-box"><span class="array-index">0 (P)</span><div class="array-val final-root">5</div></div>
          <div class="array-cell-box"><span class="array-index">1</span><div class="array-val">3</div></div>
          <div class="array-cell-box"><span class="array-index">2</span><div class="array-val active-swap">1</div></div>
          <div class="array-cell-box"><span class="array-index">3</span><div class="array-val">4</div></div>
          <div class="array-cell-box"><span class="array-index">4</span><div class="array-val">2</div></div>
          <div class="array-cell-box"><span class="array-index">5</span><div class="array-val">7</div></div>
          <div class="array-cell-box"><span class="array-index">6</span><div class="array-val active-swap">8</div></div>
          <div class="array-cell-box"><span class="array-index">7</span><div class="array-val">9</div></div>
        </div>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">STEP 2</span> Advance Pointers until Crossover</div>
        <div class="step-desc">
          &bull; Advance L: Skips 4 (&lt;5), skips 2 (&lt;5). Stops on <b>7</b> at <code>L = 5</code>.<br/>
          &bull; Advance R: Stops on <b>2</b> at <code>R = 4</code>.<br/>
          <b>Pointers have crossed (L &gt; R, 5 &gt; 4)!</b> STOP scanning immediately!
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">STEP 3</span> Swap Pivot with R</div>
        <div class="step-desc">
          Swap pivot <code>A[0]</code> (5) with boundary element <code>A[R]</code> (<code>A[4] = 2</code>)!<br/>
          <b>Final Partitioned Array:</b> <code>[2, 3, 1, 4, <b>5</b>, 7, 8, 9]</code>. Pivot 5 is in its permanent sorted place!
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">PIVOT CHOICE &amp; WORST CASE</div>
        <div class="sticky-content">
          Fixed end pivot on pre-sorted input causes <code>0 / (N-1)</code> splits &rarr; <b>&Theta;(<i>N</i>&sup2;) worst case!</b><br/>
          <b>Fix:</b> Median-of-Three (first, mid, last) guarantees expected <i>O</i>(<i>N</i> log <i>N</i>).
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">HOARE VS LOMUTO TRAP</div>
        <div class="sticky-content">
          Hoare partition takes on average <b>3&times; fewer swaps</b> than Lomuto single-pointer partition. Lomuto degrades severely on duplicate keys!
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">MASTER MATRIX</span> Complete 7-Algorithm Comparison</span>
        <span class="marks">HIGH EXAM YIELD</span>
      </div>

      <table class="exam-table">
        <thead>
          <tr>
            <th>Algorithm</th>
            <th>Best Time</th>
            <th>Avg Time</th>
            <th>Worst Time</th>
            <th>Aux Space</th>
            <th>Stable?</th>
            <th>In-Place?</th>
            <th>Adaptive?</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><b>Selection Sort</b></td><td>&Theta;(<i>N</i>&sup2;)</td><td>&Theta;(<i>N</i>&sup2;)</td><td>&Theta;(<i>N</i>&sup2;)</td><td><i>O</i>(1)</td><td>No</td><td>Yes</td><td>No</td></tr>
          <tr class="highlight-row"><td><b>Insertion Sort</b></td><td><b>&Theta;(<i>N</i>)</b></td><td>&Theta;(<i>N</i>&sup2;)</td><td>&Theta;(<i>N</i>&sup2;)</td><td><i>O</i>(1)</td><td><b>Yes</b></td><td><b>Yes</b></td><td><b>Yes (sorted)</b></td></tr>
          <tr><td><b>Quicksort</b></td><td>&Theta;(<i>N</i> log <i>N</i>)</td><td>&Theta;(<i>N</i> log <i>N</i>)</td><td>&Theta;(<i>N</i>&sup2;)</td><td><i>O</i>(log <i>N</i>)</td><td>No</td><td>Yes</td><td>No</td></tr>
          <tr><td><b>Mergesort (Array)</b></td><td>&Theta;(<i>N</i> log <i>N</i>)</td><td>&Theta;(<i>N</i> log <i>N</i>)</td><td>&Theta;(<i>N</i> log <i>N</i>)</td><td><b><i>O</i>(<i>N</i>)</b></td><td><b>Yes</b></td><td>No</td><td>No</td></tr>
          <tr class="highlight-row"><td><b>Mergesort (List)</b></td><td>&Theta;(<i>N</i> log <i>N</i>)</td><td>&Theta;(<i>N</i> log <i>N</i>)</td><td>&Theta;(<i>N</i> log <i>N</i>)</td><td><b><i>O</i>(1)</b></td><td><b>Yes</b></td><td><b>Yes</b></td><td><b>Natural: Yes</b></td></tr>
          <tr><td><b>Heapsort</b></td><td>&Theta;(<i>N</i> log <i>N</i>)</td><td>&Theta;(<i>N</i> log <i>N</i>)</td><td>&Theta;(<i>N</i> log <i>N</i>)</td><td><i>O</i>(1)</td><td>No</td><td>Yes</td><td>No</td></tr>
        </tbody>
      </table>

      <div class="point-header" style="margin-top: 4px;">
        <span><span class="spec-ref purple">WORKED EXAMPLE 2</span> Two-Pointer Merge Step-by-Step</span>
        <span class="marks">MERGE TRACE</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2px 6px; font-size: 6.7pt; margin: 2px 0;">
        Merge two sorted halves <code>L = [2, 5, 8]</code> and <code>R = [3, 4, 9]</code> into auxiliary array <code>B</code>.
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">STEP 1</span> Compare <code>L[0] = 2</code> vs <code>R[0] = 3</code></div>
        <div class="step-desc">2 &le; 3 &rarr; Copy 2 to <code>B[0]</code>. Increment L pointer. <code>B = [2]</code>.</div>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">STEP 2</span> Compare <code>L[1] = 5</code> vs <code>R[0] = 3</code></div>
        <div class="step-desc">3 &lt; 5 &rarr; Copy 3 to <code>B[1]</code>. Increment R pointer. <code>B = [2, 3]</code>.</div>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">STEP 3</span> Compare <code>L[1] = 5</code> vs <code>R[1] = 4</code></div>
        <div class="step-desc">4 &lt; 5 &rarr; Copy 4 to <code>B[2]</code>. Increment R pointer. <code>B = [2, 3, 4]</code>.</div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">STEP 4</span> Flush Remaining Elements</div>
        <div class="step-desc">Compare 5 vs 9 &rarr; Copy 5, then 8, then leftover 9. <b>Final:</b> <code>[2, 3, 4, 5, 8, 9]</code>. Exactly <b>&Theta;(<i>N</i>) time</b>!</div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">WHY HEAPSORT IS UNSTABLE</div>
        <div class="sticky-content">
          Swapping the root with the last leaf element <code>A[N]</code> jumps equal elements over large spans of memory, completely destroying original relative order!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">CUTOFF TO INSERTION SORT</div>
        <div class="sticky-content">
          Stopping Quicksort recursion when subarray size &le; 10 and finishing with Insertion Sort boosts CPU cache speed, but <b>DOES NOT change asymptotic Big-O</b>!
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">060</span> COMP20003 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: HOARE PARTITION</div>
  <div>WORKED EXAMPLE: TWO-POINTER MERGE &nbsp;·&nbsp; <span class="page-num">061</span></div>
</div>
""" + COMMON_FOOT
})

# Module 7: Graphs & Dijkstra
modules.append({
    "name": "Module 7 · Graphs & Dijkstra",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>070</b> | COMP20003 STUDY COMPANION &nbsp;·&nbsp; MODULE 7: GRAPHS & SHORTEST PATHS</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §7.1 &ndash; §7.4] &nbsp;|&nbsp; <b>071</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 7 · <b>Dijkstra: Worked State Matrix Trace Guide</b></h1>
        <div class="subtitle">Step-by-Step Priority Queue Relaxation &amp; Path Recovery &nbsp;·&nbsp; <span class="spec-ref">CROSS-REF SPEC §7.3</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] CORE MUST-KNOW</span>
        <span class="exam-stamp-sub">DIJKSTRA TRACE · 15-20 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Dijkstra Execution Log Matrix (Vertices A, B, C, D)</span>
        <span class="marks">EXAM RELAXATION TABLE</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.8pt; margin: 2px 0;">
        <b>Past Exam Graph:</b> 4 vertices with directed edges: <code>(A&rarr;B: 2)</code>, <code>(A&rarr;C: 5)</code>, <code>(B&rarr;C: 1)</code>, <code>(B&rarr;D: 6)</code>, <code>(C&rarr;D: 2)</code>. Start vertex: <b>A</b>.<br/>
        <b>Exam Task:</b> Fill the strict execution trace table. Record which vertex is finalized at each step and all distance relaxations.
      </div>

      <div style="background: #EFF6FF; border: 1.2px solid #BFDBFE; border-radius: 4px; padding: 2.5px 6px; margin: 2px 0; font-size: 6.7pt;">
        <b>Edge Relaxation Axiom:</b> If <code>dist[u] + weight(u, v) &lt; dist[v]</code>, update: <code>dist[v] = dist[u] + weight(u, v)</code> and set <code>prev[v] = u</code>!
      </div>

      <table class="exam-table">
        <thead>
          <tr>
            <th>Iteration</th>
            <th>Pop Min (u)</th>
            <th>Relax Edges (u &rarr; v)</th>
            <th>dist[A]</th>
            <th>dist[B]</th>
            <th>dist[C]</th>
            <th>dist[D]</th>
            <th>Finalized Set S</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>Init</b></td>
            <td>&mdash;</td>
            <td>Initialize start vertex A</td>
            <td><b>0</b></td>
            <td>&infin;</td>
            <td>&infin;</td>
            <td>&infin;</td>
            <td>&empty;</td>
          </tr>
          <tr class="highlight-row">
            <td><b>Step 1</b></td>
            <td><b>A (dist=0)</b></td>
            <td>Relax (A,B)=2 &rarr; <b>B: 2</b><br/>Relax (A,C)=5 &rarr; <b>C: 5</b></td>
            <td>0*</td>
            <td><b>2 (A)</b></td>
            <td><b>5 (A)</b></td>
            <td>&infin;</td>
            <td>{A}</td>
          </tr>
          <tr>
            <td><b>Step 2</b></td>
            <td><b>B (dist=2)</b></td>
            <td>Relax (B,C)=2+1=3 &lt; 5 &rarr; <b>C: 3</b><br/>Relax (B,D)=2+6=8 &rarr; <b>D: 8</b></td>
            <td>0*</td>
            <td>2*</td>
            <td><b>3 (B)</b></td>
            <td><b>8 (B)</b></td>
            <td>{A, B}</td>
          </tr>
          <tr class="highlight-row">
            <td><b>Step 3</b></td>
            <td><b>C (dist=3)</b></td>
            <td>Relax (C,D)=3+2=5 &lt; 8 &rarr; <b>D: 5</b></td>
            <td>0*</td>
            <td>2*</td>
            <td>3*</td>
            <td><b>5 (C)</b></td>
            <td>{A, B, C}</td>
          </tr>
          <tr>
            <td><b>Step 4</b></td>
            <td><b>D (dist=5)</b></td>
            <td>No outgoing edges</td>
            <td>0*</td>
            <td>2*</td>
            <td>3*</td>
            <td>5*</td>
            <td>{A, B, C, D}</td>
          </tr>
        </tbody>
      </table>

      <div class="array-strip-container" style="border-color: #16A34A; background: #F0FDF4;">
        <div style="font-size: 6.8pt; font-weight: 800; color: #166534; margin-bottom: 1px;">
          <span class="step-pill" style="background: #16A34A;">PATH RECOVERY</span> Backtrack <code>prev[]</code> pointers from destination D:
        </div>
        <div style="font-size: 6.8pt; color: #14532D; line-height: 1.25;">
          <code>D &larr; (prev[D]=C) &larr; (prev[C]=B) &larr; (prev[B]=A)</code> &rarr; <b>Shortest Path: A &rarr; B &rarr; C &rarr; D (Total Cost = 5)</b>.
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">NEGATIVE EDGE FATAL FLAW</div>
        <div class="sticky-content">
          Dijkstra assumes once a vertex is finalized in <code>S</code>, its distance can NEVER decrease. A negative edge breaks this greedy invariant! Use <b>Bellman-Ford</b> for negative edges.
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">TIME COMPLEXITY BOUNDS</div>
        <div class="sticky-content">
          &bull; <b>Binary Heap PQ:</b> <i>O</i>((|V| + |E|) log |V|).<br/>
          &bull; <b>Dense Array PQ:</b> <i>O</i>(|V|&sup2;) &rarr; optimal for dense graphs (|E| &asymp; |V|&sup2;)!
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> BFS vs DFS Queue/Stack Trace Protocol</span>
        <span class="marks">CORE TRAVERSAL</span>
      </div>

      <table class="exam-table">
        <thead>
          <tr>
            <th>Property</th>
            <th>Breadth-First Search (BFS)</th>
            <th>Depth-First Search (DFS)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>Underlying Data Structure</b></td>
            <td><b>Queue (FIFO)</b></td>
            <td><b>Stack (LIFO)</b> or Function Call Stack</td>
          </tr>
          <tr>
            <td><b>Exploration Pattern</b></td>
            <td>Concentric ripples (level by level)</td>
            <td>Deep plunge down a path until dead end</td>
          </tr>
          <tr class="highlight-row">
            <td><b>Shortest Path Guarantee</b></td>
            <td><b>Guarantees minimum hops</b> on unweighted graphs!</td>
            <td><b>NO guarantee</b> of shortest path</td>
          </tr>
          <tr>
            <td><b>Memory Space Bound</b></td>
            <td><i>O</i>(branching factor ^ depth) (Can be huge)</td>
            <td><i>O</i>(maximum path depth) (Memory frugal)</td>
          </tr>
          <tr>
            <td><b>Signature Exam Application</b></td>
            <td>Shortest path in unweighted mazes / networks</td>
            <td>Topological Sort on DAGs, Cycle Detection</td>
          </tr>
        </tbody>
      </table>

      <div class="point-header" style="margin-top: 4px;">
        <span><span class="spec-ref purple">MINIMUM SPANNING TREE</span> Prim vs Kruskal Battle</span>
        <span class="marks">DESIGN CHOICE</span>
      </div>

      <table class="exam-table">
        <thead>
          <tr>
            <th>Dimension</th>
            <th>Prim's Algorithm</th>
            <th>Kruskal's Algorithm</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>Strategy</b></td>
            <td><b>Vertex-based:</b> Grows a single tree outwards</td>
            <td><b>Edge-based:</b> Sorts all edges, joins forests</td>
          </tr>
          <tr>
            <td><b>Helper Data Structure</b></td>
            <td>Priority Queue (Min-Heap)</td>
            <td><b>Disjoint Set (Union-Find)</b> with path compression</td>
          </tr>
          <tr class="highlight-row">
            <td><b>Time Complexity</b></td>
            <td><i>O</i>(|E| log |V|)</td>
            <td><i>O</i>(|E| log |E|) = <i>O</i>(|E| log |V|)</td>
          </tr>
          <tr>
            <td><b>Best Suited For</b></td>
            <td><b>Dense graphs</b> (|E| &asymp; |V|&sup2;)</td>
            <td><b>Sparse graphs</b> (|E| &asymp; |V|)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">GRAPH REPRESENTATION BOUNDS</div>
        <div class="sticky-content">
          &bull; <b>Adjacency Matrix:</b> Space &Theta;(|V|&sup2;). Edge check <i>O</i>(1). Iterate neighbours &Theta;(|V|).<br/>
          &bull; <b>Adjacency List:</b> Space &Theta;(|V| + |E|). Iterate neighbours &Theta;(deg(u)). Optimal for sparse!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">TOPOLOGICAL SORT RULE</div>
        <div class="sticky-content">
          Valid ONLY on <b>Directed Acyclic Graphs (DAGs)</b>! Reverse of DFS post-order finish times gives valid topological order.
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">070</span> COMP20003 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: DIJKSTRA MATRIX</div>
  <div>WORKED EXAMPLE: BFS/DFS & MST &nbsp;·&nbsp; <span class="page-num">071</span></div>
</div>
""" + COMMON_FOOT
})

# Compile each spread individually to guarantee exactly 1 page per spread
master_doc = fitz.open()

print("Compiling individual spreads to guarantee strict 1-page per spread...")
for idx, mod in enumerate(modules):
    temp_pdf = os.path.join(BASE_DIR, f"temp_spread_{idx+1}.pdf")
    compile_spread(mod["html"], temp_pdf)
    mod_doc = fitz.open(temp_pdf)
    print(f"[{mod['name']}] compiled with {len(mod_doc)} page(s).")
    
    # Append strictly the first page (the complete landscape spread)
    master_doc.insert_pdf(mod_doc, from_page=0, to_page=0)

# Save merged master volume
master_doc.save(OUT_PDF)
print(f"Master Full Edition saved to: {OUT_PDF} (Total spreads: {len(master_doc)})")

# Copy to course folder
os.makedirs(os.path.dirname(COURSE_PDF), exist_ok=True)
shutil.copy2(OUT_PDF, COURSE_PDF)
print(f"Copied to course folder: {COURSE_PDF}")

# Render previews for each spread
for i in range(len(master_doc)):
    pix = master_doc[i].get_pixmap(dpi=130)
    prev_path = os.path.join(BASE_DIR, f"master_spread_{i+1}.png")
    pix.save(prev_path)
    print(f"Rendered preview: {prev_path}")

print("Master Study Companion pipeline complete!")
