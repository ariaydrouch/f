from pdfkit import *
from data import *

d = Deck("HiLabs_Case_Deck_Case_Management_Workbench.pdf")

# model numbers
def model():
    rows = []
    for lab, pb, pt, fb, ft, cat, why, conf in TIME_ROWS:
        rows.append((lab, pb * TOUCHES_BASE + fb, pt * TOUCHES_TARGET + ft, cat))
    b = sum(r[1] for r in rows); t = sum(r[2] for r in rows)
    return rows, 480 - b, 480 - t
MROWS, CONV_B, CONV_T = model()
WASTE_B = sum(r[1] for r in MROWS if r[3] == "waste")
WASTE_T = sum(r[2] for r in MROWS if r[3] == "waste")

# ============================================================ 1 TITLE + SUMMARY
d.slide("Case Management Workbench: giving Maria her clinical judgment back",
        "HiLabs APM case  |  MVP for a Medicare Advantage / Medicaid health plan  |  Deck + Excel annex (5 synthetic patients, live models)", "Summary")
d.rect(28, 66, 560, 150, fill=GRAY, r=6)
d.text(40, 74, 540, "The answer in 30 seconds", 11, NAVY, True)
d.text(40, 92, 540,
       "<b>1. Problem.</b> An RN with 48 cases loses ~%d%% of a 480-min day to hunting data, re-typing documentation, redialling bad numbers and triaging her own queue. Only ~%d%% is real conversation.<br/><br/>"
       "<b>2. Product.</b> A web workbench with three screens: <b>Today queue</b> (who, why now, what next), <b>Member 360</b> (one trustworthy picture: every fact has a source, an as-of date and a conflict flag), "
       "<b>Outreach &amp; documentation</b> (best number/time/channel; notes and assessments pre-filled).<br/><br/>"
       "<b>3. Principle.</b> AI drafts and ranks; the nurse confirms and decides. Nothing is auto-sent, auto-diagnosed or auto-closed."
       % (round(100 * WASTE_B / 480), round(100 * CONV_B / 480)), 10, INK, lead=12.6)
# big numbers
bx = 610
for i, (big, small, col) in enumerate([
        ("%d%%" % round(100 * WASTE_B / 480), "of Maria's day lost to data hunting, documentation, outreach friction and triage (model, medium confidence)", RED),
        ("%d%% > %d%%" % (round(100 * CONV_B / 480), round(100 * CONV_T / 480)), "share of day in real conversations: baseline vs design model (pilot commitment: >= 25%)", TEAL),
        ("21 / 5", "datasets inventoried / fictional patients, each with 8-10 records and planted imperfections", NAVY)]):
    yy = 66 + i * 52
    d.rect(bx, yy, 322, 46, fill=white, stroke=MID, r=5)
    d.text(bx + 8, yy + 8, 110, big, 17, col, True, lead=20)
    d.text(bx + 124, yy + 7, 192, small, 8, INK, lead=9.6)
# storyline
steps = [("A  Understand", "Persona, day in the life, ranked pain, where time goes"),
         ("B  Data strategy", "21 datasets, each tied to a decision; 5 insight recipes"),
         ("C  Synthetic patients", "5 scenarios, imperfections that break naive designs"),
         ("D  Product design", "Queue, Member 360, Outreach/Doc; AI vs human"),
         ("E  Prioritize & measure", "MVP cut, metrics w/ baselines, risks, pilot & pricing")]
for i, (a, b) in enumerate(steps):
    x = 28 + i * 181
    d.rect(x, 232, 173, 52, fill=NAVY if i % 2 == 0 else TEAL, r=5)
    d.text(x + 8, 238, 160, a, 9.5, white, True)
    d.text(x + 8, 254, 160, b, 8, white, lead=9.6)
d.text(28, 298, 900, "What I would build first, and what I deliberately leave out", 11, NAVY, True)
d.text(28, 316, 440,
       "<b>Build first (MVP).</b><br/>"
       "&bull; ADT-triggered <b>queue with a clock</b> (2-business-day contact, 7-day follow-up) and a transparent score<br/>"
       "&bull; <b>Member 360</b> on 9 must-have datasets with freshness banners and side-by-side medication conflicts<br/>"
       "&bull; <b>Contact graph</b>: rank phone numbers by source, recency and past success; recommend channel and time<br/>"
       "&bull; <b>Pre-filled assessment and note draft</b> with citations; one confirm click", 9.5, INK, lead=12.6)
d.text(490, 316, 440,
       "<b>Leave out (on purpose).</b><br/>"
       "&bull; Autonomous outreach or auto-closing cases: trust and compliance risk too high for v1<br/>"
       "&bull; Diagnosis or treatment suggestions: we flag conflicts for the clinician, never resolve them<br/>"
       "&bull; Rebuilding the EHR or claims portal: link out, do not replicate<br/>"
       "&bull; Member-facing app, wearables, Medicaid LTSS feeds: Phase 2 / Later<br/>"
       "&bull; More predictive models: the data-assembly gap is bigger than the prediction gap", 9.5, INK, lead=12.6)
d.rect(28, 440, 904, 64, fill=LTEAL, r=6)
d.text(40, 448, 880,
       "<b>The test I applied to every item:</b> what would Maria do differently because she saw this?  "
       "Example: Eleanor Marsh (HF, discharged Fri) - <i>discharge alert + new-drug pharmacy reject + PA status</i> tells Maria her new heart-failure drug was never dispensed and nobody has filed the PA. "
       "She calls today, instead of discovering it on day 7 or after a readmission (~1 in 5 Medicare discharges is readmitted within 30 days).", 9.5, INK, lead=12.6)
d.foot("Sources: HiLabs case brief; Jencks et al. NEJM 2009 (30-day readmission 19.6%); CMS TCM 99495/99496. Full source list and assumptions in annex sheet 'Assumptions_Sources'.")

# ============================================================ 2 PERSONA / DAY IN LIFE
d.slide("A. Understand: Maria is the best clinical sensor in the plan, and her day is spent on plumbing",
        "Persona (case manager only) and a day in her life. Her instinct about a med list that does not add up is the scarce asset.", "A. Understand")
d.rect(28, 66, 260, 300, fill=GRAY, r=6)
d.circle(58, 98, 20, NAVY)
d.text(40, 90, 36, "<font color='white'>MR</font>", 13, white, True, align=1)
d.text(86, 82, 195, "Maria R., RN, 20 yrs ICU", 10.5, NAVY, True)
d.text(86, 98, 195, "Complex case manager at a Medicare Advantage plan; telephonic; 48 active cases", 7.5, SOFT)
d.text(40, 122, 240,
       "<b>Job to be done</b><br/>Get each member safely through a transition: right meds, right follow-up, right services, before the next ED visit.<br/><br/>"
       "<b>Strengths</b><br/>Clinical pattern-recognition; rapport; knows the community resources.<br/><br/>"
       "<b>Needs from software</b><br/>1) Tell me who needs me today and why. 2) Show one reliable picture, with how old each fact is. 3) Get me to a connected call. 4) Do not make me type it twice.<br/><br/>"
       "<b>Success looks like</b><br/>Contact within 2 business days, med reconciliation done, visit within 7 days, no preventable readmission.<br/><br/>"
       "<b>Fears</b><br/>Missing a deadline; trusting wrong data; an audit finding.", 8.6, INK, lead=10.8)
# timeline
tx = 306
d.text(tx, 66, 620, "Monday in Maria's life (from the case brief; times illustrative)", 10, NAVY, True)
events = [("8:00", "6 discharge alerts since Fri; claims show nothing yet; picks a case by gut feel", RED),
          ("8:20", "Opens claims portal, auth system, pharmacy file, HIE, old notes, own spreadsheet for ONE member", RED),
          ("9:10", "Phone on file is disconnected; searches three systems for another number", AMBER),
          ("9:40", "Latest claim is 45 days old; alert says 'admitted', not why", AMBER),
          ("10:30", "Two systems disagree on meds (duplicate statin? stopped ACE-inhibitor?)", RED),
          ("11:15", "40-field assessment to close the contact; same facts re-typed into plan and audit form", AMBER),
          ("13:30", "Three voicemails; caregiver number is buried in a free-text note", AMBER),
          ("15:00", "Two real conversations so far today. Instinct barely used.", RED),
          ("17:30", "Charting after hours (assumed ~45 min)", AMBER)]
yy = 86
d.line(tx + 38, yy + 4, tx + 38, yy + 9 * 31 - 14, MID, 1.2)
for t, e, col in events:
    d.circle(tx + 38, yy + 6, 4.5, col)
    d.text(tx, yy, 32, t, 8, NAVY, True, align=2)
    d.text(tx + 52, yy, 570, e, 9.4, INK, lead=11)
    yy += 31
d.rect(tx, 372, 626, 40, fill=LRED, r=5)
d.text(tx + 8, 377, 612, "<b>What a bad day costs:</b> six members with a 2-business-day clock, of whom Maria reaches ~2 by mid-afternoon; every unreached discharge is a lost chance to catch a missing medication before it becomes a readmission, and a missed HEDIS TRC / TCM window for the plan.", 8.6, INK, lead=10.4)
d.rect(28, 376, 260, 36, fill=LTEAL, r=5)
d.text(36, 382, 246, "<b>Opportunity:</b> every red dot above is a data or workflow problem, not a clinical one.", 8.6, INK, lead=10.6)
d.text(28, 428, 900, "Why this persona only", 10.5, NAVY, True)
d.text(28, 446, 900,
       "Per the brief, the case manager is the user. Supervisors, nurses on other programs and members matter, but a queue that works for Maria also gives supervisors "
       "visible capacity and gives members faster contact. I model Maria at 48 cases (the complex-case range is 30-60); the transitions-of-care nurse at 60-100+ cases feels the same pain with shorter cycles, so the design scales to her.", 9.2, INK, lead=11.6)
d.foot("Sources: HiLabs case brief (Maria scenario, workload ranges). Times other than those quoted in the brief are illustrative; after-hours charting is an assumption to validate.")

# ============================================================ 3 PAIN + TIME
d.slide("A. Understand: ~%d%% of her day goes to data, typing, dialling and triage; ~%d%% is real conversation" % (round(100 * WASTE_B / 480), round(100 * CONV_B / 480)),
        "Pain points ranked by impact (minutes lost + clinical risk) and a time model with assumptions shown. Live version in annex sheet 'Time_Model'.", "A. Understand")
d.text(28, 64, 480, "Pain points ranked by impact", 10, NAVY, True)
rows = [["#", "Pain point", "Min/day", "Clinical risk", "Evidence"]]
for r, p, m, risk, ev in PAINS:
    rows.append([str(r), p, str(m) if m else "indirect", risk, ev])
fills = {}
for i, (r, p, m, risk, ev) in enumerate(PAINS, 1):
    fills[(i, 3)] = {"Highest": LRED, "High": LAMB, "Medium": LTEAL}[risk]
yb = d.table(28, 80, [18, 170, 42, 48, 190], rows, 7.6, col_bold=(), fills=fills)
d.text(28, yb + 6, 470,
       "<b>Ranking logic.</b> Impact = minutes lost x frequency + clinical risk of the failure. Documentation costs the most minutes; <b>conflicting meds</b> costs the fewest minutes but the most harm, "
       "so it gets a first-class design treatment (side-by-side, never silently merged). Stale data and conflicts are 'indirect': they do not take minutes, they take correctness.", 8.4, INK, lead=10.4)
# bar chart
cx, cy = 540, 82
d.text(cx, 64, 390, "Where 480 minutes go: today vs with workbench (model)", 10, NAVY, True)
colors = {"waste": [RED, HexColor('#E0736C'), HexColor('#EBA09A'), HexColor('#F3C7C3')],
          "value-support": AMBER, "other": MID}
def stack(xc, vals, title):
    d.text(xc - 10, cy, 130, title, 8, SOFT, True, align=1)
    y0 = cy + 14
    scale = 225 / 480
    wi = 0
    for lab, mins, cat in vals:
        h = mins * scale
        if cat == "waste":
            col = colors["waste"][wi % 4]; wi += 1
        elif cat == "value-support":
            col = AMBER
        elif cat == "other":
            col = MID
        else:
            col = TEAL
        d.rect(xc, y0, 110, h, fill=col, r=0)
        if h > 10:
            d.text(xc + 2, y0 + h / 2 - 4.5, 106, "<font color='white'>%d min</font>" % round(mins), 7.5, white, True, align=1)
        y0 += h
base = [(r[0], r[1], r[3]) for r in MROWS] + [("Conversations", CONV_B, "value")]
targ = [(r[0], r[2], r[3]) for r in MROWS] + [("Conversations", CONV_T, "value")]
stack(cx, base, "TODAY")
stack(cx + 135, targ, "WITH WORKBENCH")
lx = cx + 262
shorts = ["Assemble context", "Documentation", "Outreach friction", "Queue triage", "Coordination", "Huddles/other", "REAL CONVERSATIONS"]
cols = [colors["waste"][0], colors["waste"][1], colors["waste"][2], colors["waste"][3], AMBER, MID, TEAL]
for i, (s, col) in enumerate(zip(shorts, cols)):
    d.rect(lx, cy + 20 + i * 18, 9, 9, fill=col, r=2)
    d.text(lx + 13, cy + 19 + i * 18, 120, s, 7.2, INK, lead=8)
d.rect(lx, cy + 150, 126, 60, fill=LTEAL, r=5)
d.text(lx + 5, cy + 154, 118, "<b>%d min</b> of waste freed per day (%d to %d); conversation share %d%% to %d%% (model). Pilot commitment: only >= 25%%."
       % (WASTE_B - WASTE_T, WASTE_B, WASTE_T, round(100 * CONV_B / 480), round(100 * CONV_T / 480)), 7.4, INK, lead=8.8)
# assumptions
d.rect(28, 330, 904, 150, fill=GRAY, r=6)
d.text(38, 336, 600, "How I got the numbers, and how sure I am", 9.5, NAVY, True)
arows = [["Activity", "Today formula", "Assumption and basis", "Confidence"],
         ["Assemble context", "6.0 min x 16 touches = 96", "~1 min per screen x 6-7 systems (brief); 16 touches = about a third of 48 cases + 6 new alerts", "Medium"],
         ["Documentation", "8.0 min x 16 touches = 128", "Call note ~5 min; full 40-field assessment ~15 min on ~1 in 3 touches; consistent with 25-35% of nursing time in documentation reviews (Moy 2021)", "Medium"],
         ["Outreach friction", "4.5 min x 16 = 72", "~2.5 attempts per touch x ~1.8 min lookup/dial/voicemail; ~30% attempts connect (assumption)", "Low-Medium"],
         ["Triage / spreadsheet", "35 min fixed", "Morning queue scan + after each alert wave", "Medium"],
         ["Conversations", "remainder = %d min" % CONV_B, "Cross-check: ~4 connected calls x 15 min = 60 min; matches '2 real conversations by 3 pm'", "Medium"]]
d.table(38, 352, [100, 140, 520, 80], arows, 7.2, hfill=NAVY)
d.text(38, 456, 880, "<b>Sensitivity:</b> if documentation is 6 min/touch instead of 8, waste share is still ~62%. Targets assume 20 touches/day with the workbench and that the nurse confirms every AI draft. To be validated by shadowing 5-8 nurses (time-and-motion) in week 1 of the pilot.", 7.6, INK, lead=9.2)
d.foot("Sources: HiLabs case brief; Moy et al. JAMIA 2021 (nurse documentation burden); Sinsky et al. Ann Intern Med 2016. All per-touch minutes are my estimates, flagged for pilot validation.")

# ============================================================ 4-5 DATA INVENTORY
def inv_rows(sub):
    rows = [["Dataset", "Source", "What it tells Maria  ->  decision it enables", "Freshness", "Expected quality problem  ->  how handled", "Priority"]]
    fills = {}
    for i, (id_, n, src, tells, fresh, qual, pr, dec) in enumerate(sub, 1):
        rows.append(["%s  %s" % (id_, n), src, "%s  <b>-> %s</b>" % (tells, dec), fresh, qual, pr])
        fills[(i, 5)] = LTEAL if pr.startswith("MVP") else (LAMB if pr.startswith("Phase") else GRAY)
    return rows, fills

for part, (sub, ttl) in enumerate([(DATASETS[:11], "B. Data strategy (1/2): triggers, clinical truth and reachability are the must-haves"),
                                   (DATASETS[11:], "B. Data strategy (2/2): prioritisation, social context and capacity round out the picture")]):
    d.slide(ttl, "Every dataset is tied to a decision. MVP = must-have for the first release; Phase 2 / Later = valuable but costlier or lower frequency. Full 21-row table in annex.", "B. Data strategy")
    rows, fills = inv_rows(sub)
    yb = d.table(28, 64, [116, 116, 268, 72, 272, 60], rows, 8.2 if part == 0 else 8.8, pad=3.4 if part == 0 else 4.5, fills=fills, col_bold=(0,))
    if part == 1:
        d.rect(28, yb + 12, 904, 52, fill=LTEAL, r=5)
        d.text(38, yb + 18, 884,
               "<b>Design rule for data trust.</b> Every value in the UI carries <b>source + as-of date</b>; every claim-derived fact carries a <b>'data through'</b> banner; conflicts show <b>both values</b> and who said what; "
               "an event not yet visible is drawn as a <b>ghost item ('not received yet')</b>, never as absence. ADT triggers; claims confirm; pharmacy and clinical records explain.", 9, INK, lead=11.5)
    d.foot("Sources: ADT/HIE alert vendors (Collective Medical, PointClick), HL7 v2 ADT, C-CDA/FHIR; NCQA HEDIS; AHC-HRSN / PRAPARE; 42 CFR Part 2; TCPA. Freshness figures are typical industry ranges, not plan-specific measurements.")

# ============================================================ 6 COMBINATIONS
d.slide("B. Data strategy: value comes from combinations, not single feeds",
        "Five 'insight recipes' that the engine computes and the queue shows as a one-line reason. Each ends in an action Maria would not otherwise have taken today.", "B. Data strategy")
y = 66
for i, (name, ds, see, do) in enumerate(COMBOS):
    d.rect(28, y, 904, 62, fill=white if i % 2 else GRAY, stroke=MID, r=5, lw=0.5)
    d.text(36, y + 8, 120, "<b>%s</b>" % name, 9.6, NAVY, lead=11.5)
    d.text(160, y + 8, 215, "<font color='#5A6675'>INPUTS</font><br/>%s" % ds, 8.2, INK, lead=10)
    d.text(392, y + 8, 280, "<font color='#D2453D'>WHAT THE NURSE SEES</font><br/>%s" % see, 8.8, INK, lead=10.6)
    d.text(690, y + 8, 235, "<font color='#16908A'>WHAT SHE DOES DIFFERENTLY</font><br/><b>%s</b>" % do, 8.8, INK, lead=10.6)
    d.text(374, y + 24, 14, ">", 14, TEAL, True)
    y += 68
d.rect(28, y + 2, 904, 80, fill=LBLUE, r=5)
d.text(38, y + 9, 884,
       "<b>How an insight is built (so it is auditable):</b> rule or model fires  >  evidence list (dataset, record, as-of date)  >  confidence (High: confirmed in 2 sources; Medium: one source or may be missing cash fills; Low: inferred)  >  suggested action.<br/>"
       "<b>Example of explicit uncertainty:</b> 'No metformin fill since 12 Jun (PDC 54%) - confidence Medium: cash or discount-card fills are invisible. Ask: where do you fill it?'<br/>"
       "<b>Deliberately not built:</b> a generic 'risk score' tile with no reason. A number without a reason is not actionable and erodes trust.", 8.6, INK, lead=11)
d.foot("Sources: NCQA HEDIS TRC/FUH/FMC; CMS Part D adherence (PDC >= 80%); AGS Beers Criteria; Cutler et al. BMJ Open 2018 (non-adherence cost).")

# ============================================================ 7 SYNTHETIC PATIENTS
d.slide("C. Five synthetic patients, each planted with imperfections that break a naive design",
        "Each has 8-10 records across datasets (annex sheet 'Synthetic_Records'). Rank = transparent score (annex 'Priority_Score'). Scenario date: Mon 9 Nov 2026, 8:00 am.", "C. Synthetic patients")
scores = {}
for p in PATIENTS:
    w = [30, 25, 20, 10, 15]  # urgency, acuity, gap, social, recency in tuple order
    s = p["scores"]
    scores[p["pid"]] = round(30 * s[0] / 5 + 25 * s[1] / 5 + 20 * s[2] / 5 + 10 * s[3] / 5 + 15 * s[4] / 5)
imp = {
 "P1": "Conflicting med lists (lisinopril vs new drug); ADT says 'Home', summary says 'Home + home health'; inpatient claim not yet received; PA reject",
 "P2": "Duplicate legacy case (M-30027 / M-30072); disconnected home phone; A1c result 3 wks late; foot-wound claim 19 days late; cash fills may hide adherence",
 "P3": "Name-variant alerts (82% match); 2 of 3 phones dead; ADT 6 ED visits vs claims 4; newest number sits in pharmacy profile; stale 'unable to reach' case",
 "P4": "Stale 'stable housing' screen vs newer note; Rx sent to old-address pharmacy; follow-up booked day 8; conflicting med lists; returned mail; prepaid phone",
 "P5": "Duplicate statins at 2 pharmacies; caregiver number only in free text; landline she cannot hear; ED claim missing; LTSS data monthly (hours under-delivered)",
}
rows = [["Rank / score", "Patient and scenario", "Data-sets", "Planted imperfections", "'8 am Monday': what Maria should see and do"]]
order = sorted(PATIENTS, key=lambda p: -scores[p["pid"]])
for rk, p in enumerate(order, 1):
    rows.append(["#%d  (%d)" % (rk, scores[p["pid"]]),
                 "<b>%s %s</b><br/>%s<br/><i>%s</i>" % (p["pid"], p["name"], p["demo"], p["scenario"]),
                 "%d datasets" % len(p["records"]), imp[p["pid"]], p["short"]])
d.table(28, 64, [52, 215, 52, 295, 290], rows, 8.6, pad=7, col_bold=())
d.rect(28, 424, 904, 80, fill=LTEAL, r=5)
d.text(38, 430, 884,
       "<b>Why these five.</b> They stress different parts of the design: P1 clock + conflicting meds + blocked drug (Member 360 and queue clock); P2 slow-burn rising risk with uncertain adherence (confidence labels); "
       "P3 reachability failure (contact graph); P4 behavioral health + stale SDOH + channel choice (SMS, window logic, consent masking); P5 polypharmacy + caregiver + dual-eligible data lag (multi-source, caregiver as contact).<br/>"
       "<b>Score = 30% deadline urgency + 25% acuity + 20% active blocker + 15% time since last real contact + 10% social vulnerability.</b> The score orders the queue; the 'why' text, not the number, is what Maria reads.", 8.6, INK, lead=10.8)
d.foot("All names, member IDs, phone numbers (555-01xx), facilities and results are invented. No real PHI. Score inputs and rationale: annex sheet 'Priority_Score'.")

exec(open("deck_part2.py").read())
d.save()
print("pages", d.n)
