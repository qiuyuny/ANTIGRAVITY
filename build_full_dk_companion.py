# -*- coding: utf-8 -*-
"""
COMP20003 Algorithms and Data Structures
Master Publication-Grade DK Study Companion Generator (Full Edition)
Covers all 7 Syllabus Modules with Step-by-Step Concrete Worked Examples,
High-Contrast Print-Optimized Memory Strips, and Cheatsheet Cross-References.
"""

import os
import subprocess
import fitz

BASE_DIR = r"C:\Users\kakur\Desktop\COMP20003_Project 2"
OUT_PDF = r"C:\Users\kakur\Desktop\COMP20003_DK_Study_Companion_Full.pdf"
COURSE_PDF = r"C:\Users\kakur\Desktop\University\Semester_Current\COMP20003_Algo\COMP20003_DK_Study_Companion_Full.pdf"
TEMP_PROFILE = r"C:\Users\kakur\AppData\Local\Temp\edge_full_companion_profile"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

COMMON_CSS = """
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
    page-break-after: always;
  }

  .spread-page {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    page-break-after: always;
    page-break-inside: avoid;
  }

  body {
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    color: #0F172A;
    background: #FFFFFF;
    font-size: 7.4pt;
    line-height: 1.28;
  }

  code, pre, .mono {
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 7.0pt;
    font-weight: 700;
  }

  /* Running Header */
  .running-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1.8px solid #0F172A;
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
"""

print("Writing full companion builder script...")

