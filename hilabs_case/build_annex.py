from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from data import *

wb = Workbook()
HDR = PatternFill("solid", fgColor="1F3A5F")
INP = PatternFill("solid", fgColor="FFF4CC")
thin = Side(style="thin", color="CCCCCC")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)


def sheet(title, headers, rows, widths, first=False):
    ws = wb.active if first else wb.create_sheet()
    ws.title = title
    ws.append(headers)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = HDR
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for r in rows:
        ws.append(list(r))
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = BOX
    ws.freeze_panes = "A2"
    return ws


# 1 README
ws = sheet("README", ["Item", "Detail"], [
    ("Purpose", "Annex to the HiLabs APM case deck: synthetic data for 5 fictional patients, plus the models behind the numbers in the deck."),
    ("Scenario date", "Monday 9 Nov 2026, 8:00 am (the moment the case manager opens the workbench)."),
    ("Data", "Entirely fictional. Names, IDs, phone numbers (555-01xx), facilities and results are invented. No PHI."),
    ("Sheets", "Patients (summary + 8 am line) | Synthetic_Records (all datasets, imperfections) | Priority_Score (live formulas) | Time_Model (live formulas) | Dataset_Inventory | Insight_Combos | Metrics | Assumptions_Sources"),
    ("Yellow cells", "Inputs you can change; dependent cells recalculate."),
    ("Imperfections", "Planted per patient: conflicting med lists, delayed claims, wrong/dead phones, stale SDOH, duplicate legacy case, name-variant alerts, rejected pharmacy claim, appointment outside measure window."),
], [22, 120], first=True)

# 2 Patients
sheet("Patients", ["ID", "Member ID", "Name (fictional)", "Profile", "Scenario stressed", "What the case manager should see and do at 8 am Monday"],
      [(p["pid"], p["mid"], p["name"], p["demo"], p["scenario"], p["line"]) for p in PATIENTS],
      [6, 11, 18, 34, 28, 110])

# 3 Records
rows = []
for p in PATIENTS:
    for r in p["records"]:
        rows.append((p["pid"], p["name"]) + r)
sheet("Synthetic_Records",
      ["Patient", "Name", "Dataset", "Sample record", "Event / as-of date", "Received by plan", "Planted imperfection", "How the product handles it"],
      rows, [7, 16, 26, 70, 14, 16, 50, 46])

# 4 Priority score (live formulas)
ws = wb.create_sheet("Priority_Score")
ws.append(["Transparent next-best-queue score (0-100). Inputs are 0-5 (yellow). Weights editable. Score = sum(weight x input/5)."])
ws["A1"].font = Font(bold=True)
ws.append([])
ws.append(["Component", "Weight"] + [p["pid"] + " " + p["name"].split()[0] for p in PATIENTS])
for c in ws[3]:
    c.font = Font(bold=True, color="FFFFFF"); c.fill = HDR; c.alignment = Alignment(wrap_text=True)
order = [0, 1, 2, 4, 3]  # data.scores order: urgency, acuity, gap, social, recency -> weights order
labels = {0: SCORE_WEIGHTS[0], 1: SCORE_WEIGHTS[1], 2: SCORE_WEIGHTS[2], 3: SCORE_WEIGHTS[3], 4: SCORE_WEIGHTS[4]}
# weights rows: urgency, acuity, gap, recency, social ; scores tuple: urgency, acuity, gap, social, recency
for i, (lab, w) in enumerate(SCORE_WEIGHTS):
    idx = {0: 0, 1: 1, 2: 2, 3: 4, 4: 3}[i]
    ws.append([lab, w] + [p["scores"][idx] for p in PATIENTS])
    for col in range(2, 3 + len(PATIENTS)):
        ws.cell(row=4 + i, column=col).fill = INP
ws.append(["TOTAL SCORE", "=SUM(B4:B8)"] + [f"=ROUND(SUMPRODUCT($B$4:$B$8,{get_column_letter(3+j)}4:{get_column_letter(3+j)}8)/5,0)" for j in range(5)])
ws.append(["RANK (1 = work first)", ""] + [f"=RANK({get_column_letter(3+j)}9,$C$9:$G$9)" for j in range(5)])
for r in (9, 10):
    for c in ws[r]:
        c.font = Font(bold=True)
ws.append([])
ws.append(["Why these scores"])
ws["A12"].font = Font(bold=True)
why = [
    "P1: contact clock expires Tue; HF + CKD, new drug blocked, no contact this episode -> top.",
    "P4: 7-day psych follow-up window closes Tue; no meds; housing unstable; text channel works.",
    "P3: ED yesterday; chronic pattern; last 9 attempts failed, but a new number exists (high recency since last contact).",
    "P5: ED fall; polypharmacy; caregiver strain; 7-day ED follow-up window (FMC) not yet closing.",
    "P2: slow-burn rising risk; best handled as proactive evening call; still gets queued before it becomes an ED visit.",
]
for t in why:
    ws.append([t])
ws.column_dimensions["A"].width = 56
for col in "BCDEFG":
    ws.column_dimensions[col].width = 15

# 5 Time model (live formulas)
ws = wb.create_sheet("Time_Model")
ws.append(["Maria's day: baseline vs workbench (minutes in an 8-hour / 480-minute shift)"])
ws["A1"].font = Font(bold=True, size=12)
ws.append(["Shift minutes", 480]); ws["B2"].fill = INP
ws.append(["Case touches per day - baseline", TOUCHES_BASE]); ws["B3"].fill = INP
ws.append(["Case touches per day - with workbench", TOUCHES_TARGET]); ws["B4"].fill = INP
ws.append([])
hdr = ["Activity", "Min per touch (base)", "Min per touch (target)", "Fixed min (base)", "Fixed min (target)",
       "Total min today", "% of day today", "Total min with workbench", "% of day with workbench", "Category", "How I estimated it", "Confidence"]
ws.append(hdr)
for c in ws[6]:
    c.font = Font(bold=True, color="FFFFFF"); c.fill = HDR; c.alignment = Alignment(wrap_text=True, vertical="center")
r0 = 7
for i, (lab, pb, pt, fb, ft, cat, why_, conf) in enumerate(TIME_ROWS):
    r = r0 + i
    ws.append([lab, pb, pt, fb, ft, f"=B{r}*$B$3+D{r}", f"=F{r}/$B$2", f"=C{r}*$B$4+E{r}", f"=H{r}/$B$2", cat, why_, conf])
    for col in (2, 3, 4, 5):
        ws.cell(row=r, column=col).fill = INP
rc = r0 + len(TIME_ROWS)
rl = rc - 1
ws.append(["Real conversations & clinical judgment (remainder)", "", "", "", "",
           f"=$B$2-SUM(F{r0}:F{rl})", f"=F{rc}/$B$2", f"=$B$2-SUM(H{r0}:H{rl})", f"=H{rc}/$B$2", "value",
           "Cross-check: ~4 connected calls x ~15 min = 60 min today; model gives the same.", "Medium"])
ws.append(["TOTAL", "", "", "", "", f"=SUM(F{r0}:F{rc})", f"=SUM(G{r0}:G{rc})", f"=SUM(H{r0}:H{rc})", f"=SUM(I{r0}:I{rc})"])
ws.append([])
ws.append(["Share of day lost to data hunting + documentation + outreach friction + triage", "", "", "", "",
           f"=SUM(F{r0}:F{r0+3})", f"=F{rc+3}/$B$2", f"=SUM(H{r0}:H{r0+3})", f"=H{rc+3}/$B$2"])
ws.append(["Minutes freed per day by workbench (waste rows)", "", "", "", "", f"=F{rc+3}-H{rc+3}"])
for r in range(r0, rc + 4):
    for col in (7, 9):
        ws.cell(row=r, column=col).number_format = "0%"
    for c in ws[r]:
        c.alignment = Alignment(wrap_text=True, vertical="top")
for col, w in zip("ABCDEFGHIJKL", [52, 12, 12, 11, 11, 12, 11, 14, 14, 14, 80, 12]):
    ws.column_dimensions[col].width = w
ws.append([])
ws.append(["Sensitivity: if documentation per touch is 6 min instead of 8, waste share falls ~7 pts, still >60% of the day. Validate in pilot by time-and-motion."])

# 6 Inventory
sheet("Dataset_Inventory",
      ["ID", "Dataset", "Source", "What it tells the clinician", "Freshness", "Expected quality problems -> how handled", "Priority", "Decision it enables (Maria test)"],
      DATASETS, [6, 28, 34, 46, 16, 60, 16, 46])

# 7 Combos
sheet("Insight_Combos", ["Insight", "Datasets combined", "What the nurse sees", "What she does differently"],
      COMBOS, [28, 60, 70, 50])

# 8 Metrics
sheet("Metrics", ["Metric", "Baseline (assumed)", "Pilot target", "How measured"], METRICS, [48, 24, 36, 48])

# 9 assumptions & sources
ws = sheet("Assumptions_Sources", ["Type", "Text"],
           [("Assumption", a) for a in ASSUMPTIONS] + [("Source", s) for s in SOURCES], [14, 150])

wb.save("HiLabs_Case_Annex_Synthetic_Patients.xlsx")
print("saved")
