# -*- coding: utf-8 -*-
"""
SWEN20003 Object Oriented Software Development
Master Publication-Grade DK Study Companion Generator (Full Edition)
Compiles each module into a guaranteed 1-page A3 landscape spread,
then merges into one publication-grade master volume.
"""

import os
import subprocess
import fitz
import shutil

BASE_DIR = r"C:\Users\kakur\Desktop\COMP20003_Project 2"
OUT_PDF = r"C:\Users\kakur\Desktop\SWEN20003_DK_Study_Companion_Full.pdf"
COURSE_PDF = r"C:\Users\kakur\Desktop\University\Semester_Current\SWEN20003_OOSD\SWEN20003_DK_Study_Companion_Full.pdf"
TEMP_PROFILE = r"C:\Users\kakur\AppData\Local\Temp\edge_swen_companion_profile"
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
    min-width: 58px;
  }
  .array-index {
    font-family: 'JetBrains Mono', monospace;
    font-size: 6.2pt;
    font-weight: 700;
    color: #64748B;
    margin-bottom: 1px;
  }
  .array-val {
    min-width: 58px;
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
    temp_html = os.path.join(BASE_DIR, "temp_swen_spread.html")
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
# MODULE 1: Java Memory, Privacy Leaks & Immutable Classes
# ==============================================================================
modules.append({
    "name": "Module 1 · Java Memory, Privacy Leaks & Immutability",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>010</b> | SWEN20003 STUDY COMPANION &nbsp;·&nbsp; MODULE 1: JAVA MEMORY, PRIVACY LEAKS & IMMUTABILITY</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §1.1 &ndash; §1.3] &nbsp;|&nbsp; <b>011</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 1 · <b>Immutability &amp; Defensive Copy: Worked Guide</b></h1>
        <div class="subtitle">Reference Aliasing, Privacy Leaks &amp; 5-Step Immutability Fix &nbsp;·&nbsp; <span class="spec-ref">CROSS-REF SPEC §1.2</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] CORE MUST-KNOW</span>
        <span class="exam-stamp-sub">IMMUTABILITY · 10-14 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Breaking &amp; Fixing an "Immutable" Class (Past Exam Archetype)</span>
        <span class="marks">10 MARKS EXAM Q</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>Exam Code:</b> <code>public final class Person { private final String name; private final List&lt;String&gt; hobbies;</code><br/>
        <code>public Person(String n, List&lt;String&gt; h) { this.name = n; this.hobbies = h; /* Line A */ }</code><br/>
        <code>public List&lt;String&gt; getHobbies() { return hobbies; /* Line B */ } }</code><br/>
        <b>Tasks:</b> (a) Write Java code showing how a caller mutates <code>Person</code>'s internal list. (b) Fix Line A and Line B using Defensive Copying.
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">STEP 1 (PART A)</span> Exploit Constructor Aliasing (Line A) OR Getter Leak (Line B)</div>
        <div class="step-desc">
          Even though <code>private final List&lt;String&gt; hobbies</code> prevents reassigning the pointer, the <code>ArrayList</code> object on the Heap is still <b>mutable</b>!<br/>
          &bull; <b>Attack 1 (Via Constructor Input Reference):</b><br/>
          <code>List&lt;String&gt; ext = new ArrayList&lt;&gt;(List.of("Reading")); Person p = new Person("Sarah", ext);</code><br/>
          <code>ext.add("Hacked!"); // Mutates p.hobbies directly because this.hobbies == ext (0x4000)!</code><br/>
          &bull; <b>Attack 2 (Via Getter Return Reference):</b><br/>
          <code>p.getHobbies().clear(); // Directly wipes out internal list via leaked reference!</code>
        </div>
      </div>

      <div class="array-strip-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1px;">
          <span style="font-size: 6.7pt; font-weight: 800; color: #0F172A;"><span class="step-pill red">BEFORE FIX</span> Reference Aliasing (Both Pointers Hit Same Heap Address 0x4000)</span>
          <span style="font-size: 6.3pt; color: #DC2626; font-weight: 800;">PRIVACY LEAK!</span>
        </div>
        <div class="array-strip">
          <div class="array-cell-box"><span class="array-index">Caller: ext</span><div class="array-val danger-cell">0x4000 &rarr;</div></div>
          <div class="array-cell-box"><span class="array-index">Heap 0x4000</span><div class="array-val active-swap">["Reading"]</div></div>
          <div class="array-cell-box"><span class="array-index">Person.hobbies</span><div class="array-val danger-cell">&larr; 0x4000</div></div>
          <div class="array-cell-box"><span class="array-index">p.getHobbies()</span><div class="array-val danger-cell">&larr; 0x4000</div></div>
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">STEP 2 (PART B)</span> Apply Defensive Copying on Input (Line A) &amp; Output (Line B)</div>
        <div class="step-desc">
          Allocate a <b>brand-new independent Heap collection</b> whenever mutable data crosses the class boundary:<br/>
          &bull; <b>Line A Fix (Constructor):</b> <code>this.hobbies = new ArrayList&lt;&gt;(hobbies);</code> &nbsp;<i>(Allocates fresh list at 0x8000)</i><br/>
          &bull; <b>Line B Fix (Getter):</b> <code>return new ArrayList&lt;&gt;(this.hobbies);</code> &nbsp;<i>(Returns fresh copy at 0x9000; 0x8000 is 100% shielded!)</i>
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">WHY STRING NEEDS NO COPY</div>
        <div class="sticky-content">
          <code>String</code>, <code>Integer</code>, <code>Double</code>, and <code>LocalDate</code> are <b>already immutable</b> in Java! Sharing their references is 100% safe; only copy mutable objects (<code>List</code>, <code>Date</code>, arrays, custom objects with setters).
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">WHY MARK CLASS "FINAL"?</div>
        <div class="sticky-content">
          An immutable class MUST be declared <code>public final class</code> so no malicious subclass can extend it and override getters to return mutable state!
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> String Constant Pool &amp; Wrapper Cache Trace (== vs .equals)</span>
        <span class="marks">HIGH-YIELD TRACE</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>Exam Code Trace:</b> Determine the exact boolean output (<code>true</code> or <code>false</code>) for each comparison below and justify using JVM Heap vs Constant Pool mechanics.
      </div>

      <table class="exam-table">
        <thead>
          <tr>
            <th>Java Code Snippet</th>
            <th>Result</th>
            <th>Step-by-Step JVM Memory Justification</th>
          </tr>
        </thead>
        <tbody>
          <tr class="highlight-row">
            <td><code>String a = "OOSD";<br/>String b = "OOSD";<br/>System.out.print(a == b);</code></td>
            <td><b>true</b></td>
            <td>Both string literals are interned in the <b>String Constant Pool</b>. <code>a</code> and <code>b</code> point to the exact same pooled address (<code>0x1010 == 0x1010</code>).</td>
          </tr>
          <tr>
            <td><code>String c = new String("OOSD");<br/>System.out.print(a == c);</code></td>
            <td><b>false</b></td>
            <td><code>new String(...)</code> explicitly allocates a <b>brand-new object on the main Heap</b> (<code>0x2050</code>). Reference check <code>0x1010 == 0x2050</code> is <b>false</b>!</td>
          </tr>
          <tr class="highlight-row">
            <td><code>System.out.print(a.equals(c));</code></td>
            <td><b>true</b></td>
            <td><code>String.equals()</code> overrides <code>Object.equals()</code> to compare character-by-character sequence (<code>"OOSD"</code> vs <code>"OOSD"</code>).</td>
          </tr>
          <tr>
            <td><code>Integer x = 100, y = 100;<br/>System.out.print(x == y);</code></td>
            <td><b>true</b></td>
            <td>Autoboxing calls <code>Integer.valueOf(100)</code>. JVM caches <code>Integer</code> objects in range <b>[-128, 127]</b>, returning the same cached address!</td>
          </tr>
          <tr>
            <td><code>Integer u = 200, v = 200;<br/>System.out.print(u == v);</code></td>
            <td><b>false</b></td>
            <td><code>200</code> is outside <b>[-128, 127]</b>! Autoboxing allocates two separate Heap objects (<code>new Integer(200)</code>). <code>u == v</code> compares addresses &rarr; <b>false</b>!</td>
          </tr>
        </tbody>
      </table>

      <div class="point-header" style="margin-top: 4px;">
        <span><span class="spec-ref purple">WORKED EXAMPLE 3</span> Pass-By-Value Reference Trap in Methods</span>
        <span class="marks">CONCEPTUAL CORE</span>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">RULE</span> Java is 100% Pass-By-Value (Copies the Reference Value!)</div>
        <div class="step-desc">
          <code>void modify(Student s1, Student s2) { s1.setGpa(4.0f); s2 = new Student("Bob", 2.0f); }</code><br/>
          &bull; <b>Caller:</b> <code>Student a = new Student("Alice", 3.0f); Student b = new Student("Eve", 3.5f); modify(a, b);</code><br/>
          &bull; <b>Trace on <code>a</code>:</b> <code>s1</code> receives a copy of address <code>0x5000</code>. Calling <code>s1.setGpa(4.0f)</code> dereferences <code>0x5000</code> and mutates Alice's heap object &rarr; <b><code>a.getGpa()</code> becomes 4.0!</b><br/>
          &bull; <b>Trace on <code>b</code>:</b> Reassigning <code>s2 = new Student(...)</code> only points local variable <code>s2</code> to a new address <code>0x6000</code>. Caller's variable <code>b</code> still points to <code>0x5004</code> ("Eve", 3.5) &rarr; <b><code>b</code> is UNCHANGED!</b>
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">ENCAPSULATION DEFINITION (2017 Q1a)</div>
        <div class="sticky-content">
          <b>Encapsulation</b> bundles data (attributes) and methods operating on that data into one class, while <b>Information Hiding</b> restricts direct external access using <code>private</code> fields and controlled <code>public</code> getters/setters.
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">SHALLOW VS DEEP COPY</div>
        <div class="sticky-content">
          If a list contains mutable objects (e.g. <code>List&lt;Student&gt;</code>), <code>new ArrayList&lt;&gt;(list)</code> only copies references (shallow copy)! Full immutability requires cloning each element: <code>for (Student s : list) copy.add(new Student(s));</code>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">010</span> SWEN20003 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: IMMUTABILITY & DEFENSIVE COPY</div>
  <div>WORKED EXAMPLE: STRING POOL, WRAPPERS & PASS-BY-VALUE &nbsp;·&nbsp; <span class="page-num">011</span></div>
</div>
""" + COMMON_FOOT
})

# ==============================================================================
# MODULE 2: Inheritance, Polymorphism & Method Dispatch
# ==============================================================================
modules.append({
    "name": "Module 2 · Inheritance, Polymorphism & Dispatch",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>020</b> | SWEN20003 STUDY COMPANION &nbsp;·&nbsp; MODULE 2: INHERITANCE, POLYMORPHISM & METHOD DISPATCH</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §2.1 &ndash; §2.3] &nbsp;|&nbsp; <b>021</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 2 · <b>Polymorphism &amp; Dispatch: Worked Guide</b></h1>
        <div class="subtitle">Overriding vs Overloading, Static vs Dynamic Binding &nbsp;·&nbsp; <span class="spec-ref">CROSS-REF SPEC §2.2</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] CORE MUST-KNOW</span>
        <span class="exam-stamp-sub">DISPATCH TRACE · 8-12 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Overriding vs Overloading Dispatch Trace (Past Exam Archetype)</span>
        <span class="marks">8 MARKS EXAM TRAP</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>Class Hierarchy:</b><br/>
        <code>class Base { public void print(int x) { System.out.println("Base int: " + x); } &nbsp; public void show() { System.out.println("Base show"); } }</code><br/>
        <code>class Derived extends Base { public void print(double x) { System.out.println("Derived double: " + x); } &nbsp; @Override public void show() { System.out.println("Derived show"); } }</code><br/>
        <b>Execution:</b> <code>Base obj = new Derived(); &nbsp; obj.show(); &nbsp; obj.print(5);</code> &mdash; Trace exact output &amp; justify!
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">STEP 1</span> Identify Static (Declared) Type vs Dynamic (Actual) Type</div>
        <div class="step-desc">
          In <code>Base obj = new Derived();</code>:<br/>
          &bull; <b>Static Declared Type of <code>obj</code> = <code>Base</code></b> (Known at compile-time by `javac`).<br/>
          &bull; <b>Dynamic Actual Type of <code>obj</code> = <code>Derived</code></b> (Actual object living on Heap at runtime).
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">STEP 2</span> Trace Call 1: <code>obj.show();</code> &rarr; Prints <code>"Derived show"</code></div>
        <div class="step-desc">
          1. <b>Compile-Time Check:</b> Compiler checks static type <code>Base</code>. Does <code>Base</code> have <code>void show()</code>? YES.<br/>
          2. <b>Override Check:</b> <code>Derived.show()</code> has the <b>exact same signature</b> (<code>show()</code>) as <code>Base.show()</code> &rarr; <b>Method Overriding</b>!<br/>
          3. <b>Run-Time Dynamic Binding:</b> JVM looks at actual heap object (<code>Derived</code>) and executes <code>Derived.show()</code> &rarr; <b><code>"Derived show"</code></b>.
        </div>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">STEP 3</span> Trace Call 2: <code>obj.print(5);</code> &rarr; Prints <code>"Base int: 5"</code> (THE TRAP!)</div>
        <div class="step-desc">
          1. <b>Overload vs Override:</b> <code>Derived.print(double)</code> has a <b>different parameter type</b> from <code>Base.print(int)</code>. It <b>OVERLOADS</b> (does NOT override!) <code>print</code>.<br/>
          2. <b>Compile-Time Static Binding:</b> Overload resolution happens 100% at compile-time using ONLY the <b>Static Type (<code>Base</code>)</b>!<br/>
          3. Inside <code>Base</code>, the ONLY method is <code>print(int)</code>. The compiler hard-binds the call to <code>Base.print(int)</code>. Since <code>print(int)</code> is NOT overridden in <code>Derived</code>, runtime executes <code>Base.print(5)</code> &rarr; <b><code>"Base int: 5"</code></b>!
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">2-STAGE DISPATCH GOLDEN RULE</div>
        <div class="sticky-content">
          <b>Stage 1 (Compile-Time):</b> Compiler uses <b>Static Type</b> to pick the method signature (resolves all Overloading).<br/>
          <b>Stage 2 (Run-Time):</b> JVM uses <b>Dynamic Type</b> ONLY if that exact signature was Overridden!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">ALWAYS WRITE @OVERRIDE</div>
        <div class="sticky-content">
          If the developer wrote <code>@Override</code> above <code>print(double x)</code> in <code>Derived</code>, the compiler would immediately flag an error, catching the accidental overload bug!
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> Subclass Constructor Chaining &amp; <code>super()</code> (2016 Exam Q1)</span>
        <span class="marks">10 MARKS CODING</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>2016 Exam Q1:</b> Given immutable <code>Person(String firstName, String lastName)</code>, write subclass <code>Student extends Person</code> with immutable <code>String studentID</code> (initialized once at creation) and mutable <code>float gpa</code>.
      </div>

      <div class="array-strip-container" style="border-color: #0284C7; background: #F0F9FF;">
        <div style="font-size: 6.7pt; font-weight: 800; color: #0369A1; margin-bottom: 2px;">
          <span class="step-pill blue">FULL SCORE CODE</span> Constructor Chaining + Mixed Mutability Pattern
        </div>
        <pre class="mono" style="margin: 0; line-height: 1.18; font-size: 5.7pt; color: #0F172A;">
public class Student extends Person {
    private final String studentID; // Immutable -> final + NO setter
    private float gpa;              // Mutable -> private + get/set

    public Student(String fName, String lName, String id, float gpa) {
        super(fName, lName);        // MUST BE LINE 1! Calls Person()
        this.studentID = id;
        this.gpa = gpa;
    }
    public String getStudentID() { return this.studentID; } // Getter
    public float getGpa()        { return this.gpa; }
    public void setGpa(float gpa){ this.gpa = gpa; }        // Setter
}</pre>
      </div>

      <div class="point-header" style="margin-top: 4px;">
        <span><span class="spec-ref purple">DECISION MATRIX</span> Abstract Class vs Interface Selection Guide</span>
        <span class="marks">EXAM DESIGN Q</span>
      </div>

      <table class="exam-table">
        <thead>
          <tr>
            <th>Feature / Scenario</th>
            <th>Abstract Class (<code>extends</code>)</th>
            <th>Interface (<code>implements</code>)</th>
          </tr>
        </thead>
        <tbody>
          <tr class="highlight-row">
            <td><b>Semantic Relationship</b></td>
            <td><b>"IS-A"</b> taxonomy (<code>Doctor</code>, <code>Receptionist</code> extend <code>Staff</code>)</td>
            <td><b>"CAN-DO"</b> capability across unrelated classes (<code>Comparable</code>, <code>Sortable</code>)</td>
          </tr>
          <tr>
            <td><b>Instance Variables (State)</b></td>
            <td><b>YES:</b> Can declare <code>private/protected</code> non-final instance fields (e.g. <code>id</code>, <code>name</code>)</td>
            <td><b>NO:</b> Cannot hold instance state! All variables are <code>public static final</code> constants</td>
          </tr>
          <tr>
            <td><b>Constructors</b></td>
            <td><b>YES:</b> Has constructors invoked via <code>super(...)</code> to initialize shared fields</td>
            <td><b>NO:</b> Interfaces cannot have constructors and cannot be instantiated</td>
          </tr>
          <tr>
            <td><b>Multiple Inheritance</b></td>
            <td><b>Single class inheritance only</b> (<code>class A extends B</code>)</td>
            <td><b>Multiple type inheritance</b> (<code>class A implements I1, I2, I3</code>)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">IMPLICIT SUPER() COMPILE ERROR</div>
        <div class="sticky-content">
          If superclass <code>Person</code> defines <code>Person(String n)</code>, Java <b>removes the default no-arg constructor</b>! If <code>Student</code> forgets <code>super(n)</code> on Line 1, compilation fails!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">SAFE DOWNCASTING PATTERN</div>
        <div class="sticky-content">
          Before calling a subclass-only method on a <code>Person p</code> reference, ALWAYS check:<br/>
          <code>if (p instanceof Student) { Student s = (Student) p; s.setGpa(4.0f); }</code>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">020</span> SWEN20003 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: OVERRIDING VS OVERLOADING</div>
  <div>WORKED EXAMPLE: CONSTRUCTOR CHAINING & ABSTRACT VS INTERFACE &nbsp;·&nbsp; <span class="page-num">021</span></div>
</div>
""" + COMMON_FOOT
})

# ==============================================================================
# MODULE 3: UML Class Diagrams & OO Design Principles
# ==============================================================================
modules.append({
    "name": "Module 3 · UML Class Diagrams & OO Design",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>030</b> | SWEN20003 STUDY COMPANION &nbsp;·&nbsp; MODULE 3: UML CLASS DIAGRAMS & OO DESIGN PRINCIPLES</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §3.1 &ndash; §3.3] &nbsp;|&nbsp; <b>031</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 3 · <b>UML Class Diagrams: Worked Design Guide</b></h1>
        <div class="subtitle">Aggregation vs Composition Diamonds &amp; Text-to-UML Translation &nbsp;·&nbsp; <span class="spec-ref">CROSS-REF SPEC §3.2</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] CORE MUST-KNOW</span>
        <span class="exam-stamp-sub">UML DIAGRAMMING · 18-24 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Aggregation (Hollow ◇) vs Composition (Solid ◆)</span>
        <span class="marks">8 MARKS EXAM Q</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>Past Exam Prompt:</b> Distinguish Aggregation and Composition in (a) visual UML symbol, (b) lifecycle dependency, and (c) classify Pair 1: <i>University &amp; Department</i> and Pair 2: <i>Department &amp; Professor</i>.
      </div>

      <div class="array-strip-container" style="border-color: #334155; background: #F8FAFC;">
        <div style="font-size: 6.8pt; font-weight: 800; color: #0F172A; margin-bottom: 2px;">
          <span class="step-pill">VECTOR NOTATION MAP</span> Whole-Part Diamond Placement &amp; Lifecycle Comparison
        </div>
        <pre class="mono" style="margin: 0; line-height: 1.16; font-size: 5.6pt; color: #0F172A;">
[1] COMPOSITION (Strong / Same Lifecycle — University closes =&gt; Depts destroyed):
┌────────────┐ 1       1..* ┌────────────┐
│ University │◆────────────&gt;│ Department │  (FILLED BLACK DIAMOND at Whole)
└────────────┘              └────────────┘
[2] AGGREGATION (Weak / Independent — Dept closes =&gt; Professors still exist):
┌────────────┐ 0..*    1..* ┌────────────┐
│ Department │◇────────────&gt;│ Professor  │  (HOLLOW WHITE DIAMOND at Whole)
└────────────┘              └────────────┘</pre>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">STEP-BY-STEP</span> Complete 6-Relationship UML Arrow Dictionary</div>
        <div class="step-desc">
          1. <b>Inheritance (IS-A):</b> <code>Sub ──────&#9655; Super</code> (Solid line, hollow triangle pointing to Superclass).<br/>
          2. <b>Realization (Implements):</b> <code>Class - - - -&#9655; &laquo;interface&raquo;</code> (Dashed line, hollow triangle).<br/>
          3. <b>Composition (Strong HAS-A):</b> <code>Whole &#9670;──────&gt; Part</code> (Solid line, <b>filled black diamond</b> at Whole).<br/>
          4. <b>Aggregation (Weak HAS-A):</b> <code>Whole &#9671;──────&gt; Part</code> (Solid line, <b>hollow white diamond</b> at Whole).<br/>
          5. <b>Directed Association:</b> <code>A ──────&gt; B</code> (Solid line, open arrow: A holds field of type B).<br/>
          6. <b>Dependency (Uses):</b> <code>A - - - -&gt; B</code> (Dashed line, open arrow: B is a method parameter or local variable).
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">DIAMOND PLACEMENT TRAP</div>
        <div class="sticky-content">
          Students lose marks by drawing the diamond on the <i>Part</i> end! <b>Rule:</b> The diamond (&#9671; or &#9670;) ALWAYS touches the <b>Whole / Container class</b> (e.g. <code>DeathStar &#9670;─── DefenceItem</code>).
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">NO REDUNDANT LIST ATTRIBUTES</div>
        <div class="sticky-content">
          In UML diagrams, if you draw an association line <code>Course ───&gt; 0..* Student</code>, do <b>NOT</b> also write <code>- students: List&lt;Student&gt;</code> inside the box (or keep both consistent as taught in tutes).
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> Translating Prose Spec to UML Class Diagram (2016 Q4 / 2017 Q3)</span>
        <span class="marks">20 MARKS WORKFLOW</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>2016 Exam Q4 (Medical Practice):</b> <i>"Practice employs two types of staff: Receptionists and Doctors (all share employeeNumber, name, address, phone; Doctors have regNumber; Receptionists have lastTrainingDate, provider). Patients register (patientNumber, name) and book Appointments with a Doctor (date, attended, treatmentCost). Practice tracks patient count."</i>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">STEP 1</span> Extract Nouns &rarr; Classes &amp; Shared Hierarchy (Inheritance)</div>
        <div class="step-desc">
          "Two types of staff: Receptionists and Doctors" sharing 4 attributes &rarr; Create abstract superclass <b><code>Staff</code></b> with <code>- employeeNumber: int</code>, <code>- name: String</code>, etc. Subclasses <b><code>Doctor</code></b> and <b><code>Receptionist</code></b> inherit via <code>──────&#9655; Staff</code>!
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">STEP 2</span> Spot Association Classes / Many-to-Many Mediators (<code>Appointment</code>)</div>
        <div class="step-desc">
          A <code>Patient</code> books an <code>Appointment</code> with a <code>Doctor</code>, and each appointment stores <code>date: LocalDate</code>, <code>attended: boolean</code>, <code>cost: double</code>.<br/>
          &bull; Model <b><code>Appointment</code></b> as its own class!<br/>
          &bull; Multiplicities: <code>Patient "1" &larr;──── "0..*" Appointment "0..*" ────&gt; "1" Doctor</code> (1 Patient has 0..* Appointments; each Appointment is for exactly 1 Patient and 1 Doctor).
        </div>
      </div>

      <div class="array-strip-container" style="border-color: #16A34A; background: #F0FDF4;">
        <div style="font-size: 6.7pt; font-weight: 800; color: #166534; margin-bottom: 1px;">
          <span class="step-pill green">VECTOR ARCHITECTURE</span> Medical Practice UML Class Diagram Blueprint
        </div>
        <pre class="mono" style="margin: 0; line-height: 1.15; font-size: 5.5pt; color: #0F172A;">
┌───────────────┐ 1  0..* ┌────────────────┐     ┌───────────────┐
│MedicalPractice│◇───────&gt;│Staff {abstract}│&lt;────┤    Doctor     │
├───────────────┤         ├────────────────┤ &#9655;   ├───────────────┤
│- patCnt : int │         │- empNum: String│ │   │- regNo: String│
└───────┬───────┘         │- name : String │ │   └───────▲───────┘
      1 │ ◆               └────────────────┘ │         1 │
        │ 0..*                               │   ┌───────┴───────┐
        ▼                       ┌────────────┴──┐│  Appointment  │
┌───────────────┐ 1        0..* │ Receptionist  │├───────────────┤
│    Patient    │&lt;──────────────┤───────────────┤│- dt: LocalDate│
├───────────────┤               │- trainDt: Date││- att: boolean │
│- patNo: String│               │- prov: String ││- cost: double │
└───────────────┘               └───────────────┘└───────────────┘</pre>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">WHY UML IS USEFUL (2017 Q1b)</div>
        <div class="sticky-content">
          <b>1. Visual Abstraction &amp; Blueprint:</b> Lets developers spot design flaws (tight coupling, missing classes) BEFORE writing expensive code.<br/>
          <b>2. Standardized Communication:</b> Language-independent notation understood across teams.
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">COHESION VS COUPLING (2017 Q1d)</div>
        <div class="sticky-content">
          &bull; <b>Cohesion:</b> How focused a single class's responsibilities are (Want <b>HIGH</b>).<br/>
          &bull; <b>Coupling:</b> How heavily classes depend on each other's internals (Want <b>LOW</b>).
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">030</span> SWEN20003 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: AGGREGATION VS COMPOSITION</div>
  <div>WORKED EXAMPLE: TEXT-TO-UML CLASS DIAGRAM TRANSLATION &nbsp;·&nbsp; <span class="page-num">031</span></div>
</div>
""" + COMMON_FOOT
})

# ==============================================================================
# MODULE 4: SOLID Design Principles & Refactoring Traces
# ==============================================================================
modules.append({
    "name": "Module 4 · SOLID Principles & Refactoring",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>040</b> | SWEN20003 STUDY COMPANION &nbsp;·&nbsp; MODULE 4: SOLID DESIGN PRINCIPLES & REFACTORING</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §4.1] &nbsp;|&nbsp; <b>041</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 4 · <b>SOLID Principles: Worked Refactoring Guide</b></h1>
        <div class="subtitle">Diagnosing Code Smells &amp; Step-by-Step SOLID Refactoring &nbsp;·&nbsp; <span class="spec-ref">CROSS-REF SPEC §4.1</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] CORE MUST-KNOW</span>
        <span class="exam-stamp-sub">DESIGN CRITIQUE · 10-16 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Diagnosing &amp; Refactoring SOLID Violations (Past Exam Archetype)</span>
        <span class="marks">10 MARKS CRITIQUE</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>Exam Code under Critique:</b><br/>
        <code>public class OrderProcessor { public void processOrder(Order order) {</code><br/>
        <code>&nbsp;&nbsp;if (order.getType().equals("VIP")) order.setPrice(order.getPrice() * 0.8);</code><br/>
        <code>&nbsp;&nbsp;else if (order.getType().equals("STUDENT")) order.setPrice(order.getPrice() * 0.9);</code><br/>
        <code>&nbsp;&nbsp;Database.execute("INSERT INTO orders VALUES (" + order.getId() + ")");</code><br/>
        <code>&nbsp;&nbsp;EmailSender.send(order.getCustomerEmail(), "Order Confirmed"); } }</code>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">VIOLATION 1</span> Single Responsibility Principle (SRP) &mdash; "God Method"</div>
        <div class="step-desc">
          &bull; <b>Why it violates SRP:</b> <code>OrderProcessor</code> has <b>three unrelated reasons to change</b>: (1) discount business rules change, (2) database SQL schema changes, or (3) email notification format changes.<br/>
          &bull; <b>How to Refactor:</b> Extract three cohesive classes: <code>DiscountCalculator</code> (pricing), <code>OrderRepository</code> (database persistence), and <code>EmailNotificationService</code> (messaging).
        </div>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">VIOLATION 2</span> Open/Closed Principle (OCP) &mdash; Hardcoded Type Chain</div>
        <div class="step-desc">
          &bull; <b>Why it violates OCP:</b> Every time a new order tier is introduced (e.g. <code>"SENIOR"</code> or <code>"STAFF"</code>), a developer must open and modify <code>OrderProcessor.processOrder()</code> to add another <code>else if</code> branch, risking breaking existing logic.<br/>
          &bull; <b>How to Refactor:</b> Introduce a <b><code>DiscountStrategy</code> interface</b> with <code>double applyDiscount(double price)</code>. Implement <code>VipDiscount</code>, <code>StudentDiscount</code>. Adding a new tier only requires adding a new class!
        </div>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">VIOLATION 3</span> Dependency Inversion Principle (DIP) &mdash; Static Concrete Coupling</div>
        <div class="step-desc">
          &bull; <b>Why it violates DIP:</b> High-level <code>OrderProcessor</code> is tightly coupled to low-level concrete <code>Database</code> and <code>EmailSender</code>.<br/>
          &bull; <b>How to Refactor:</b> Depend on abstractions (<code>OrderRepository</code>, <code>Notifier</code> interfaces) injected via the constructor!
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">INSTANT EXAM SMELL DETECTOR</div>
        <div class="sticky-content">
          &bull; <b>Long <code>if/else</code> on type string or <code>instanceof</code></b> &rarr; Violates <b>OCP</b> (Fix with Strategy/Polymorphism).<br/>
          &bull; <b>Class does Calc + DB + UI/Email</b> &rarr; Violates <b>SRP</b> (Split into separate classes).
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">THREE PILLARS OF GOOD DESIGN (2016 Q5)</div>
        <div class="sticky-content">
          <b>1. Abstraction:</b> Hide complexity behind interfaces.<br/>
          <b>2. Inheritance:</b> Reuse common base code.<br/>
          <b>3. Delegation:</b> Compose helper objects for flexible runtime behaviour.
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> Clean SOLID Refactored Code &amp; Liskov / ISP Proofs</span>
        <span class="marks">FULL REFACTORING</span>
      </div>

      <div class="array-strip-container" style="border-color: #16A34A; background: #F0FDF4;">
        <div style="font-size: 6.7pt; font-weight: 800; color: #166534; margin-bottom: 2px;">
          <span class="step-pill green">AFTER REFACTORING</span> 100% Compliant with SRP + OCP + DIP
        </div>
        <pre class="mono" style="margin: 0; line-height: 1.16; font-size: 5.8pt; color: #0F172A;">
public interface DiscountStrategy { double computePrice(double raw); }
public class VipDiscount implements DiscountStrategy {
    public double computePrice(double raw) { return raw * 0.8; }
}
public class OrderProcessor {                   // Orchestrator (SRP)
    private final OrderRepository repo;         // Abstraction (DIP)
    private final NotificationService notifier; // Abstraction (DIP)

    public OrderProcessor(OrderRepository r, NotificationService n) {
        this.repo = r; this.notifier = n;
    }
    public void processOrder(Order o, DiscountStrategy d) { // Open (OCP)
        o.setPrice(d.computePrice(o.getPrice()));
        repo.save(o);
        notifier.notifyCustomer(o.getCustomerEmail(), "Confirmed");
    }
}</pre>
      </div>

      <div class="point-header" style="margin-top: 4px;">
        <span><span class="spec-ref purple">WORKED EXAMPLE 3</span> Liskov Substitution (LSP) &amp; Interface Segregation (ISP)</span>
        <span class="marks">CONCEPTUAL MASTERY</span>
      </div>

      <table class="exam-table">
        <thead>
          <tr>
            <th>Principle</th>
            <th>Classic Violation Code Example</th>
            <th>Why It Breaks &amp; Correct OO Fix</th>
          </tr>
        </thead>
        <tbody>
          <tr class="highlight-row">
            <td><b>Liskov Substitution (LSP)</b></td>
            <td><code>class Bird { void fly() {...} }</code><br/><code>class Penguin extends Bird {</code><br/><code>&nbsp;&nbsp;void fly() { throw new Error(); } }</code></td>
            <td>Passing a <code>Penguin</code> to a method expecting a <code>Bird</code> crashes the program! Subtype violates base contract.<br/><b>Fix:</b> Separate <code>Bird</code> and interface <code>Flyable</code>.</td>
          </tr>
          <tr>
            <td><b>LSP (Rectangle / Square)</b></td>
            <td><code>class Square extends Rectangle</code><br/>Overriding <code>setWidth(w)</code> to also set <code>height = w</code>.</td>
            <td>Client code executing <code>r.setWidth(5); r.setHeight(4); assert(r.area() == 20);</code> fails (gets 16)!<br/><b>Fix:</b> Both implement immutable <code>Shape</code> interface.</td>
          </tr>
          <tr class="highlight-row">
            <td><b>Interface Segregation (ISP)</b></td>
            <td><code>interface SmartDevice {</code><br/><code>&nbsp;&nbsp;void print(); void fax(); void scan(); }</code><br/>Implemented by <code>BasicPrinter</code>.</td>
            <td><code>BasicPrinter</code> is forced to implement empty/throwing <code>fax()</code> and <code>scan()</code> methods.<br/><b>Fix:</b> Segregate into <code>Printable</code>, <code>Faxable</code>, <code>Scannable</code>.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">INHERITANCE VS DELEGATION</div>
        <div class="sticky-content">
          <b>Inheritance (White-box reuse):</b> Fixed at compile-time; tightly couples subclass to parent implementation.<br/>
          <b>Delegation (Black-box reuse):</b> Object forwards call to an interface field; swappable at runtime!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">DEPENDENCY INJECTION BENEFIT</div>
        <div class="sticky-content">
          Passing <code>OrderRepository</code> into the constructor makes <b>Unit Testing trivial</b>: in tests, pass a <code>MockOrderRepository</code> without touching a real SQL database!
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">040</span> SWEN20003 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: SRP, OCP & DIP DIAGNOSIS</div>
  <div>WORKED EXAMPLE: REFACTORED CODE, LSP & ISP &nbsp;·&nbsp; <span class="page-num">041</span></div>
</div>
""" + COMMON_FOOT
})

# ==============================================================================
# MODULE 5: Gang of Four (GoF) Design Patterns
# ==============================================================================
modules.append({
    "name": "Module 5 · GoF Design Patterns",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>050</b> | SWEN20003 STUDY COMPANION &nbsp;·&nbsp; MODULE 5: GANG OF FOUR (GoF) DESIGN PATTERNS</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §4.2] &nbsp;|&nbsp; <b>051</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 5 · <b>GoF Design Patterns: Worked Implementation</b></h1>
        <div class="subtitle">Strategy, Observer, State, Singleton &amp; Template Method &nbsp;·&nbsp; <span class="spec-ref">CROSS-REF SPEC §4.2</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] CORE MUST-KNOW</span>
        <span class="exam-stamp-sub">PATTERNS · 16-24 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Strategy Pattern Complete Implementation (2016 Q1g / 2017 Q2)</span>
        <span class="marks">14-16 MARKS EXAM Q</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>2016 Exam Q1(3g):</b> <i>"Course class must display enrolled students using two interchangeable strategies: Name-based Strategy and GPA-based Strategy. Write Java code for the Strategy interface, Concrete Strategies, and Course delegation."</i>
      </div>

      <div class="array-strip-container" style="border-color: #0284C7; background: #F0F9FF;">
        <div style="font-size: 6.7pt; font-weight: 800; color: #0369A1; margin-bottom: 1px;">
          <span class="step-pill blue">FULL JAVA CODE</span> 3 Participants: Strategy Interface + Concrete Strategies + Context
        </div>
        <pre class="mono" style="margin: 0; line-height: 1.14; font-size: 5.7pt; color: #0F172A;">
// 1. Strategy Interface (Defines abstract algorithm contract)
public interface DisplayStrategy {
    void display(List&lt;Student&gt; students);
}
// 2. Concrete Strategies (Encapsulate interchangeable algorithms)
public class NameDisplayStrategy implements DisplayStrategy {
    @Override public void display(List&lt;Student&gt; students) {
        System.out.println("Students ordered by Last Name");
    }
}
public class GpaDisplayStrategy implements DisplayStrategy {
    @Override public void display(List&lt;Student&gt; students) {
        System.out.println("Students ordered by GPA");
    }
}
// 3. Context Class (Holds Strategy reference &amp; delegates execution)
public class Course {
    private ArrayList&lt;Student&gt; students = new ArrayList&lt;&gt;();
    private DisplayStrategy strategy;
    public void setStrategy(DisplayStrategy s) { this.strategy = s; }
    public void displayStudents() {
        if (this.strategy != null) this.strategy.display(students);
    }
}</pre>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">EXAM COMPARISON</span> Strategy Pattern vs Template Method Pattern</div>
        <div class="step-desc">
          &bull; <b>Strategy (Composition / "HAS-A"):</b> Swaps the <i>entire algorithm</i> at runtime via <code>setStrategy()</code>. Uses interface delegation.<br/>
          &bull; <b>Template Method (Inheritance / "IS-A"):</b> Base class defines a <code>public final void generateReport()</code> skeleton calling fixed steps (<code>open()</code>, <code>close()</code>) and <code>protected abstract void writeBody()</code> overridden by subclasses at compile-time!
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">SINGLETON VS PUBLIC STATIC FIELD</div>
        <div class="sticky-content">
          Why not <code>public static Logger instance = new Logger();</code>?<br/>
          1. <b>Lazy Creation:</b> Singleton creates only when first needed.<br/>
          2. <b>Protection:</b> Public field can be overwritten (<code>Logger.instance = null</code>).<br/>
          3. <b>Encapsulation:</b> <code>getInstance()</code> can later be changed to return a pool of 2 loggers without breaking callers!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">JAVA BUILT-IN PATTERNS</div>
        <div class="sticky-content">
          &bull; <code>java.util.Comparator</code> &rarr; <b>Strategy Pattern</b>.<br/>
          &bull; <code>java.util.Iterator</code> &rarr; <b>Iterator Pattern</b>.<br/>
          &bull; <code>AbstractList</code> / <code>ArrayList</code> &rarr; <b>Template Method</b>.
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 2</span> Pattern Selection &amp; Justification Matrix (Past Exam Archetype)</span>
        <span class="marks">10 MARKS SELECTION</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>Exam Scenarios:</b> Select the exact GoF pattern and write a 3-point architectural justification:
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">SCENARIO 1</span> Mokepon Battle Conditions (Asleep, Poisoned, Confused, Normal)</div>
        <div class="step-desc">
          &bull; <b>Selected Pattern:</b> <b>State Pattern</b>.<br/>
          &bull; <b>Justification:</b> (1) The Mokepon's turn behaviour changes completely based on its active internal condition; (2) conditions dynamically transition from one to another during battle (e.g., <code>Asleep &rarr; Normal</code>); (3) encapsulating each condition as a <code>ConditionState</code> class eliminates massive state-checking <code>if/else</code> blocks inside <code>Mokepon</code>.
        </div>
      </div>

      <div class="worked-step-card purple-bar">
        <div class="step-title"><span class="step-pill purple">SCENARIO 2</span> Weather Station / Student Enrolment Broadcasting to Multiple Systems</div>
        <div class="step-desc">
          &bull; <b>Selected Pattern:</b> <b>Observer Pattern</b>.<br/>
          &bull; <b>Justification:</b> (1) Establishes a <b>one-to-many</b> dependency between Subject (<code>WeatherStation</code> / <code>EnrolmentSystem</code>) and multiple Observers (<code>Timetable</code>, <code>Billing</code>, <code>LMS</code>); (2) Subject automatically notifies all registered observers on state change without knowing their concrete classes (<b>Loose Coupling</b>); (3) new observers can be attached at runtime with zero modifications to Subject (<b>Open/Closed Principle</b>).
        </div>
      </div>

      <div class="array-strip-container" style="border-color: #7C3AED; background: #F5F3FF;">
        <div style="font-size: 6.7pt; font-weight: 800; color: #5B21B6; margin-bottom: 1px;">
          <span class="step-pill purple">VECTOR UML MAP</span> Strategy (1-to-1 Algorithm) vs Observer (1-to-Many Broadcast)
        </div>
        <pre class="mono" style="margin: 0; line-height: 1.15; font-size: 5.5pt; color: #0F172A;">
[STRATEGY: 1 Context -&gt; 1 Strategy]   [OBSERVER: 1 Subject -&gt; 0..* Observers]
┌──────────┐     ┌───────────────┐    ┌────────────┐ 1  0..* ┌──────────────┐
│ Context  │◇───&gt;│ &laquo;interface&raquo;   │    │  Subject   │────────&gt;│ &laquo;interface&raquo;  │
├──────────┤     │ Strategy      │    ├────────────┤         │ Observer     │
│- strat   │     ├───────────────┤    │- obs: List │         ├──────────────┤
│+ doWork()│     │+ execute()    │    │+ notify()  │         │+ update()    │
└──────────┘     └───────▲───────┘    └────────────┘         └──────▲───────┘
                         &#9655;                                          &#9655;
                 ┌───────┴───────┐                          ┌───────┴───────┐
              StratA          StratB                     ScreenObs      MobileObs</pre>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">STRATEGY VS STATE DISTINCTION</div>
        <div class="sticky-content">
          <b>Strategy:</b> Client/caller actively chooses &amp; injects an algorithm (e.g. sort order); strategies don't know about each other.<br/>
          <b>State:</b> Object's internal state transitions automatically during execution (e.g. Poisoned &rarr; Fainted).
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">WHY USE DESIGN PATTERNS? (2017 Q1c)</div>
        <div class="sticky-content">
          <b>1. Proven Quality &amp; Reusability:</b> Tested solutions to recurring problems that prevent maintainability bugs.<br/>
          <b>2. Shared Vocabulary:</b> Saying "Observer Pattern" communicates the entire architecture instantly.
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">050</span> SWEN20003 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: STRATEGY & TEMPLATE METHOD</div>
  <div>WORKED EXAMPLE: STATE, OBSERVER & SINGLETON &nbsp;·&nbsp; <span class="page-num">051</span></div>
</div>
""" + COMMON_FOOT
})

# ==============================================================================
# MODULE 6: Generics, Collections, Streams, Exceptions & Testing
# ==============================================================================
modules.append({
    "name": "Module 6 · Generics, Collections, Streams & Testing",
    "html": COMMON_HEAD + """
<div class="running-top">
  <div class="left-tag"><b>060</b> | SWEN20003 STUDY COMPANION &nbsp;·&nbsp; MODULE 6: GENERICS, COLLECTIONS, STREAMS & TESTING</div>
  <div class="right-tag">[CROSS-REF CHEATSHEET: §5.1 &ndash; §6.3] &nbsp;|&nbsp; <b>061</b></div>
</div>

<div class="spread-container">
  <div class="page-left">
    <div class="title-row">
      <div class="title-block">
        <h1>Topic 6 · <b>Generics &amp; Collections: Worked Coding Guide</b></h1>
        <div class="subtitle">Bounded Generics, Nested HashMaps, Comparable &amp; Streams &nbsp;·&nbsp; <span class="spec-ref">CROSS-REF SPEC §5.1–5.3</span></div>
      </div>
      <div class="exam-stamp">
        <span class="exam-stamp-badge">[!!!] CORE MUST-KNOW</span>
        <span class="exam-stamp-sub">JAVA DEVELOPMENT · 20-36 MARKS</span>
      </div>
    </div>

    <div>
      <div class="point-header">
        <span><span class="spec-ref orange">WORKED EXAMPLE 1</span> Bounded Generics &amp; Nested HashMap (2017 Exam Q6 — 20 Marks!)</span>
        <span class="marks">20 MARKS HARD Q</span>
      </div>
      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.6pt; margin: 2px 0;">
        <b>2017 Exam Q6:</b> Given <code>interface Categoriser&lt;In, Out&gt; { Out categorise(In input); }</code>.<br/>
        (a) Write <code>StringCategoriser</code> returning the 1st letter of a String. (b) Write generic <code>CategorisedMap&lt;K, V, C extends Categoriser&lt;V, K&gt;&gt;</code> holding a <code>HashMap&lt;K, ArrayList&lt;V&gt;&gt;</code> and <code>put(V value)</code>, <code>getCategoryCount(V value)</code>.
      </div>

      <div class="array-strip-container" style="border-color: #0284C7; background: #F0F9FF;">
        <div style="font-size: 6.7pt; font-weight: 800; color: #0369A1; margin-bottom: 1px;">
          <span class="step-pill blue">FULL SCORE CODE</span> Complete 20-Mark Solution (2017 Final Exam Q6)
        </div>
        <pre class="mono" style="margin: 0; line-height: 1.13; font-size: 5.7pt; color: #0F172A;">
// Part (a): Implement Generic Interface with Concrete Types
public class StringCategoriser implements Categoriser&lt;String, String&gt; {
    @Override public String categorise(String input) {
        return input.substring(0, 1);
    }
}
// Part (b) &amp; (c): Bounded Generic Class + Nested HashMap
public class CategorisedMap&lt;K, V, C extends Categoriser&lt;V, K&gt;&gt; {
    private HashMap&lt;K, ArrayList&lt;V&gt;&gt; map;
    private C categoriser;

    public CategorisedMap(C categoriser) {
        this.map = new HashMap&lt;&gt;();
        this.categoriser = categoriser;
    }
    public void put(V value) {
        K key = this.categoriser.categorise(value); // 1. Compute key K
        if (!this.map.containsKey(key)) {           // 2. Init bucket
            this.map.put(key, new ArrayList&lt;V&gt;());
        }
        this.map.get(key).add(value);               // 3. Append value
    }
    public int getCategoryCount(V value) {
        K key = this.categoriser.categorise(value);
        if (!this.map.containsKey(key)) return 0;   // Guard null bucket
        return this.map.get(key).size();
    }
}</pre>
      </div>

      <div class="worked-step-card green-bar">
        <div class="step-title"><span class="step-pill green">WORKED EXAMPLE 2</span> Descending <code>compareTo</code> &amp; Best Card Removal (2017 Exam Q4)</div>
        <div class="step-desc">
          &bull; <b>Descending <code>Comparable&lt;Card&gt;</code>:</b> <code>public int compareTo(Card other) { return other.getRank().getPoints() - this.getRank().getPoints(); }</code> <i>(Note: if question says "c1 worth less than c2 &rarr; negative", use <code>this.points - other.points</code>!)</i><br/>
          &bull; <b>Play Best Card (Return &amp; Remove):</b> <code>Collections.sort(hand); return hand.remove(hand.size() - 1);</code> (or index 0 if sorted descending).
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">GENERIC "EXTENDS" KEYWORD RULE</div>
        <div class="sticky-content">
          In a generic type parameter bound <code>&lt;C extends Categoriser&lt;V, K&gt;&gt;</code>, Java ALWAYS uses the keyword <b><code>extends</code></b> even when <code>Categoriser</code> is an interface (never write <code>implements</code> inside <code>&lt;...&gt;</code>)!
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">SAFE REMOVAL BY ID (2016 Q1e)</div>
        <div class="sticky-content">
          To remove a student by <code>studentID</code> from an <code>ArrayList</code>:<br/>
          <code>Iterator&lt;Student&gt; it = list.iterator(); while(it.hasNext()) { if(it.next().getId().equals(id)) it.remove(); }</code>
        </div>
      </div>
    </div>
  </div>

  <div class="page-right">
    <div>
      <div class="point-header">
        <span><span class="spec-ref green">WORKED EXAMPLE 3</span> Java Stream Pipeline Line-by-Line Analysis (2017 Exam Q1f)</span>
        <span class="marks">4 MARKS STREAM Q</span>
      </div>

      <div style="background: #F1F5F9; border-left: 3px solid #475569; padding: 2.5px 6px; font-size: 6.7pt; margin: 2px 0;">
        <b>2017 Exam Q1(f):</b> Describe the exact purpose and behaviour of each line in the following stream pipeline:<br/>
        <code>List&lt;Member&gt; result = members.stream()</code><br/>
        <code>&nbsp;&nbsp;.filter(m -&gt; m.isActive()) &nbsp; .filter(m -&gt; m.getFollowers() &gt; 100000)</code><br/>
        <code>&nbsp;&nbsp;.sorted((m1, m2) -&gt; m1.getFollowers() - m2.getFollowers()) &nbsp; .collect(Collectors.toList());</code>
      </div>

      <table class="exam-table">
        <thead>
          <tr>
            <th>Pipeline Stage</th>
            <th>Stream Operation Type &amp; Exact Behaviour</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>members.stream()</code></td>
            <td><b>Source Stage:</b> Creates a sequential Stream of <code>Member</code> objects from the <code>members</code> collection without mutating the original list.</td>
          </tr>
          <tr class="highlight-row">
            <td><code>.filter(m -&gt; m.isActive())</code></td>
            <td><b>Intermediate Op 1:</b> Retains ONLY <code>Member</code> elements where <code>isActive()</code> returns <code>true</code>; discards inactive members.</td>
          </tr>
          <tr>
            <td><code>.filter(m -&gt; m.getFollowers() &gt; 100000)</code></td>
            <td><b>Intermediate Op 2:</b> Further filters the stream to keep ONLY active members with strictly more than 100,000 followers.</td>
          </tr>
          <tr class="highlight-row">
            <td><code>.sorted((m1, m2) -&gt; ...)</code></td>
            <td><b>Stateful Intermediate Op:</b> Sorts the surviving members in <b>ascending order</b> of their follower count using a lambda <code>Comparator</code>.</td>
          </tr>
          <tr>
            <td><code>.collect(Collectors.toList())</code></td>
            <td><b>Terminal Operation:</b> Triggers pipeline execution and packages the filtered, sorted stream elements into a brand-new <code>List&lt;Member&gt;</code> assigned to <code>result</code>.</td>
          </tr>
        </tbody>
      </table>

      <div class="point-header" style="margin-top: 4px;">
        <span><span class="spec-ref purple">WORKED EXAMPLE 4</span> Writing Exam Test Cases &amp; Exception Handling (2017 Q3b)</span>
        <span class="marks">6 MARKS TESTING</span>
      </div>

      <div class="worked-step-card">
        <div class="step-title"><span class="step-pill blue">TEMPLATE</span> How to Write a Full-Mark Software Test Case in Exam (2017 Q3b)</div>
        <div class="step-desc">
          Every worded test case in SWEN20003 MUST explicitly state <b>3 components</b>:<br/>
          1. <b>Component / Behaviour Tested:</b> e.g., <i>"Testing <code>DefenceItem.addSoldier()</code> minimum staffing validation and total staff counter."</i><br/>
          2. <b>Concrete Test Input:</b> e.g., <i>"Create a <code>LaserTurret</code> requiring <code>minSoldiers = 3</code>, and assign only 2 <code>Soldier</code> objects to it."</i><br/>
          3. <b>Expected Output / Result:</b> e.g., <i>"<code>isOperational()</code> should return <code>false</code> (or throw <code>InsufficientStaffException</code>), and count equals 2."</i>
        </div>
      </div>

      <div class="worked-step-card red-bar">
        <div class="step-title"><span class="step-pill red">EXCEPTION RULE</span> Checked vs Unchecked &amp; Catch Block Ordering</div>
        <div class="step-desc">
          &bull; <b>Checked (<code>IOException</code>):</b> Must be caught or declared in <code>throws</code>. &bull; <b>Unchecked (<code>NullPointerException</code>, <code>IllegalArgumentException</code>):</b> Subclasses of <code>RuntimeException</code>; indicate programmer bugs.<br/>
          &bull; <b>Catch Order:</b> ALWAYS catch specific subclass (<code>FileNotFoundException</code>) BEFORE parent (<code>IOException</code>), and <code>finally</code> ALWAYS runs!
        </div>
      </div>
    </div>

    <div class="sub-grid-2">
      <div class="sticky-note yellow">
        <div class="sticky-tape"></div>
        <div class="sticky-title">AUTOMATED VS MANUAL TESTING</div>
        <div class="sticky-content">
          Why prefer automated testing (JUnit)?<br/>
          <b>1. Regression Safety:</b> Runs thousands of tests in seconds after every code refactor.<br/>
          <b>2. Consistency:</b> Eliminates human fatigue/oversight on boundary edge cases.
        </div>
      </div>
      <div class="sticky-note green">
        <div class="sticky-tape"></div>
        <div class="sticky-title">HASHMAP EQUALS &amp; HASHCODE</div>
        <div class="sticky-content">
          If you use a custom class (e.g. <code>Pair&lt;K1, K2&gt;</code> in 2016 Q3) as a <code>HashMap</code> key, you MUST override both <code>equals()</code> AND <code>hashCode()</code> so equal pairs map to the same bucket!
        </div>
      </div>
    </div>
  </div>
</div>

<div class="running-bottom">
  <div><span class="page-num">060</span> SWEN20003 STUDY COMPANION &nbsp;·&nbsp; WORKED EXAMPLE: BOUNDED GENERICS & NESTED HASHMAP</div>
  <div>WORKED EXAMPLE: STREAM PIPELINES, EXCEPTIONS & AUTOMATED TESTING &nbsp;·&nbsp; <span class="page-num">061</span></div>
</div>
""" + COMMON_FOOT
})

# Compile each spread individually to guarantee exactly 1 page per spread
master_doc = fitz.open()

print("Compiling individual SWEN20003 spreads to guarantee strict 1-page per spread...")
for idx, mod in enumerate(modules):
    temp_pdf = os.path.join(BASE_DIR, f"temp_swen_spread_{idx+1}.pdf")
    compile_spread(mod["html"], temp_pdf)
    mod_doc = fitz.open(temp_pdf)
    print(f"[{mod['name']}] compiled with {len(mod_doc)} page(s).")
    master_doc.insert_pdf(mod_doc, from_page=0, to_page=0)
    mod_doc.close()

master_doc.save(OUT_PDF)
print(f"SWEN20003 Master Full Edition saved to: {OUT_PDF} (Total spreads: {len(master_doc)})")

os.makedirs(os.path.dirname(COURSE_PDF), exist_ok=True)
shutil.copy2(OUT_PDF, COURSE_PDF)
print(f"Copied to course folder: {COURSE_PDF}")

for i in range(len(master_doc)):
    pix = master_doc[i].get_pixmap(dpi=130)
    prev_path = os.path.join(BASE_DIR, f"swen_spread_{i+1}.png")
    pix.save(prev_path)
    print(f"Rendered preview: {prev_path}")

master_doc.close()
print("SWEN20003 Study Companion pipeline complete!")
