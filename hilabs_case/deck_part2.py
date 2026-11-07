
def frame(x, y, w, h, title):
    d.rect(x, y, w, h, fill=white, stroke=NAVY, r=6, lw=1.2)
    d.rect(x, y, w, 20, fill=NAVY, r=6)
    d.rect(x, y + 12, w, 8, fill=NAVY, r=0)
    for i in range(3):
        d.circle(x + 10 + i * 9, y + 10, 2.6, white)
    d.text(x + 44, y + 6, w - 60, "<font color='white'>%s</font>" % title, 7.6, white, True)


def annot(x, y, items, w=290, size=8.2):
    for n, head, body in items:
        d.badge(x + 7, y + 8, n)
        h = d.text(x + 20, y + 1, w - 20, "<b>%s</b> %s" % (head, body), size, INK, lead=size * 1.25)
        y += h + 9
    return y


def btn(x, y, w, s, fill=TEAL, size=6.6, h=14):
    d.rect(x, y, w, h, fill=fill, r=3)
    d.text(x, y + (h - size) / 2 - 0.5, w, "<font color='white'>%s</font>" % s, size, white, True, align=1)


# ============================================================ 8 WORK QUEUE
d.slide("D. Product design (1/3): Today queue answers 'who, why now, what next' above the fold",
        "Wireframe at 8:00 am Monday for Maria; five of her 48 cases shown (the synthetic patients). Ordered by clock first, then score.", "D. Product design")
fx, fy, fw = 28, 64, 612
frame(fx, fy, fw, 436, "workbench.plan.com / today")
d.text(fx + 10, fy + 28, 300, "Today  |  Mon 9 Nov  |  Maria R.", 9.5, NAVY, True)
cx = fx + 230
for s, f, c in [("48 active", LBLUE, NAVY), ("6 new alerts", LBLUE, NAVY), ("3 clocks <= 2 days", LRED, RED), ("capacity 96%", LAMB, INK)]:
    cx += d.chip(cx, fy + 28, s, f, c, 6.8, h=12) + 4
d.text(fx + 10, fy + 44, 590, "<font color='#5A6675'>Feeds: ADT live 07:58  |  Pharmacy 06:00  |  Clinical 2 d  |  Claims through 26 Oct (lag 14 d)</font>", 6.8, SOFT)
hy = fy + 60
d.rect(fx + 6, hy, fw - 12, 14, fill=GRAY, r=2)
for x, s in [(10, "#"), (40, "MEMBER  ·  WHY NOW"), (262, "CLOCK"), (344, "REACH (best number / channel / time)"), (470, "NEXT BEST ACTION")]:
    d.text(fx + x, hy + 3, 200, s, 6.2, SOFT, True)
qrows = [
 ("1", "91", "Eleanor Marsh, 78F, HF", "HF discharge Fri. New HF drug <b>rejected (PA)</b>. Med lists conflict.", ["ADT", "Rx", "UM", "Clinical"],
  "Contact due Tue 10 Nov", RED, "Mobile verified 12 Oct. Call now", GREEN, "Call now: file PA, confirm meds", "ADT 14h"),
 ("2", "85", "Danielle Okafor, 34F, BH", "Psych discharge <b>day 6</b>. No Rx picked up. Follow-up booked day 8.", ["ADT", "Rx", "Appt"],
  "Window ends Tue 10 Nov", RED, "SMS works; voice poor. Text first", AMBER, "Text, then call: rebook by Tue", "ADT 5d"),
 ("3", "74", "Tyrell Brooks, 47M, asthma", "<b>6th ED visit</b> in 5 mo (Sat 02:10). No controller inhaler since Jun.", ["ADT", "Rx", "Claims"],
  "ED follow-up by Fri 13", AMBER, "2 of 3 numbers dead. Try #3 (new), text", AMBER, "Text #3 + call 11:00", "ADT 30h"),
 ("4", "68", "Mabel Ostrander, 83F, D-SNP", "ED fall Thu. <b>2 statins + Beers drug</b>. Caregiver strain high.", ["ADT", "Rx", "Caregiver"],
  "ED follow-up by Fri 13", AMBER, "Landline unanswered. Call Lena after 7 pm", AMBER, "Evening call; pharmacist review", "ADT 3d"),
 ("5", "56", "Ramon Delgado, 66M, T2DM", "A1c 9.4, <b>60-day metformin gap</b>, new foot-wound claim.", ["Labs", "Rx", "Claims"],
  "Proactive (rising risk)", MID, "Home line dead. Mobile after 5 pm (ES)", AMBER, "Evening call (ES): PCP + podiatry", "Claims 19d"),
]
y = hy + 18
d.text(fx + 10, y, 300, "<font color='#D2453D'><b>CLOCK-DRIVEN</b></font>", 6.4, RED, True)
y += 10
for i, (rk, sc, nm, why, chips, clock, ccol, reach, rcol, nba, fresh) in enumerate(qrows):
    if i == 2:
        d.text(fx + 10, y, 300, "<font color='#E8A02F'><b>DUE THIS WEEK</b></font>", 6.4, AMBER, True)
        y += 10
    if i == 4:
        d.text(fx + 10, y, 300, "<font color='#5A6675'><b>PROACTIVE (rising risk)</b></font>", 6.4, SOFT, True)
        y += 10
    rh = 58
    d.rect(fx + 6, y, fw - 12, rh - 3, fill=white, stroke=MID, r=3, lw=0.5)
    d.text(fx + 10, y + 7, 22, "<b>%s</b>" % rk, 13, NAVY, True)
    d.text(fx + 10, y + 27, 26, "%s" % sc, 7, SOFT)
    d.text(fx + 40, y + 5, 215, "<b>%s</b>" % nm, 8.8, NAVY)
    d.text(fx + 40, y + 17, 215, why, 7.4, INK, lead=8.8)
    cxx = fx + 40
    for ch in chips:
        cxx += d.chip(cxx, y + 40, ch, LBLUE, NAVY, 5.8, h=9, padx=3) + 3
    d.chip(cxx + 2, y + 40, fresh, LAMB if "d" in fresh and fresh.endswith("d") else LTEAL, SOFT, 5.8, h=9, padx=3, bold=False)
    d.chip(fx + 262, y + 8, clock, LRED if ccol == RED else (LAMB if ccol == AMBER else GRAY), ccol if ccol != MID else SOFT, 6, h=11)
    d.circle(fx + 348, y + 14, 3.6, rcol)
    d.text(fx + 356, y + 8, 108, reach, 7.2, INK, lead=8.6)
    btn(fx + 468, y + 8, 128, nba, TEAL, 6.4, 18)
    d.text(fx + 468, y + 31, 130, "<font color='#5A6675'>why? evidence &gt;   dismiss with reason</font>", 5.8, SOFT)
    y += rh
d.text(fx + 10, y + 3, 590, "<font color='#5A6675'>Grey chips = dataset not received yet. Scores shown small: the reason sentence is the product. Rows 6-48 scroll below; nothing urgent hides there.</font>", 6.4, SOFT)

ax = 656
d.text(ax, 64, 280, "How to read it", 10, NAVY, True)
ey = annot(ax, 82, [
    (1, "Above the fold = the day.", "Top 5 members, each with a one-line reason and a clock. Grouped by deadline before risk, because a missed 2-business-day window cannot be recovered."),
    (2, "Score is a sort key.", "30% deadline, 25% acuity, 20% active blocker, 15% time since last contact, 10% social vulnerability. Top 3 drivers on hover. Max ~8 'due today' vs her capacity to avoid alert fatigue."),
    (3, "Reach column.", "Best number, channel and time from the contact graph, so she never redials a dead number."),
    (4, "Source chips + freshness.", "Tap a chip to see the evidence record and as-of date. Feeds banner shows claims lag."),
    (5, "Next best action (NBA).", "One per member; a button that starts the call or text and opens the 360."),
], 280, 8.6)
d.rect(ax, ey + 2, 276, 120, fill=LTEAL, r=5)
d.text(ax + 8, ey + 7, 262,
       "<b>How NBA is chosen (rules first, model second).</b><br/>trigger (ADT discharge) &gt; program playbook (HF transition) &gt; "
       "check each playbook step against data (fill? visit booked? auth?) &gt; check barriers (phone, SDOH, language) &gt; <b>pick the earliest unmet step that has a deadline</b>.<br/>"
       "<b>AI assists:</b> writes the 'why now' sentence from structured facts and cites sources. <b>Nurse:</b> accepts, snoozes or dismisses with a reason; dismissals retune ranking weekly.", 7.8, INK, lead=9.6)
d.foot("Design basis: transitions-of-care timing (CMS TCM 2 business days / 7-14 day visit; HEDIS TRC, FUH, FMC); alert-fatigue evidence (Ancker et al. 2017). Patient rows are synthetic (annex).")

# ============================================================ 9 MEMBER 360
d.slide("D. Product design (2/3): Member 360 shows one picture, with the age, source and conflicts of every fact",
        "Wireframe for Eleanor Marsh (P1) at 8:05 am. Reading order follows Maria's workflow: situation, what happened when, what is wrong with the meds, what to do.", "D. Product design")
frame(fx, fy, fw, 436, "workbench.plan.com / member / M-30011")
d.rect(fx + 6, fy + 24, fw - 12, 30, fill=GRAY, r=3)
d.text(fx + 12, fy + 28, 330, "<b>Eleanor Marsh</b>  78F  |  M-30011  |  MA-HMO  |  English  |  PCP Dr. S. Iyer", 7.8, NAVY)
cxx = fx + 12
for s, f, c in [("HF program", LBLUE, NAVY), ("Readmit risk 0.41 (up)", LRED, RED), ("Day 3 after discharge", LAMB, INK), ("Contact due Tue 10 Nov", LRED, RED)]:
    cxx += d.chip(cxx, fy + 41, s, f, c, 6.2, h=10) + 3
d.text(fx + 380, fy + 28, 224, "<font color='#5A6675'>ADT 14h  |  Clinical 2d  |  Pharmacy 1d</font><br/><font color='#E8A02F'><b>Claims through 26 Oct (lag 14d)</b></font>", 6.8, SOFT, lead=8.6, align=2)
# left: situation
lx0 = fx + 8
d.text(lx0, fy + 62, 190, "SITUATION  <font color='#16908A'>(AI draft, confirm)</font>", 6.6, NAVY, True)
sit = [("Admitted 2-6 Nov, HF exacerbation, EF 25%", ["ADT", "Clinical"], LBLUE),
       ("New sacubitril/valsartan <b>not dispensed</b>: claim rejected, PA required, none filed", ["Rx", "UM"], LRED),
       ("PCP list still shows <b>lisinopril</b>; discharge list stopped it", ["Clinical", "HIE"], LAMB)]
sy = fy + 74
for t, ch, f in sit:
    d.rect(lx0, sy, 190, 52, fill=f, r=3)
    d.text(lx0 + 5, sy + 4, 180, t, 7.6, INK, lead=9)
    cx2 = lx0 + 5
    for c_ in ch:
        cx2 += d.chip(cx2, sy + 39, c_, white, NAVY, 5.8, h=9, padx=3) + 3
    btn(lx0 + 118, sy + 37, 30, "Confirm", GREEN, 5.4, 11)
    btn(lx0 + 152, sy + 37, 30, "Edit", SOFT, 5.4, 11)
    sy += 56
d.text(lx0, sy + 2, 190, "GAPS AND BARRIERS", 6.6, NAVY, True)
d.text(lx0, sy + 13, 190, "&bull; No PCP visit booked (cardiology is day 14)<br/>&bull; Home-health auth pending since 6 Nov<br/>&bull; Home scale: unknown, ask<br/>&bull; Husband 84, hearing impaired<br/>&bull; Lives with spouse; transport OK (Mar, stale)", 7, INK, lead=8.6)
# center: timeline
tx0 = fx + 206
d.text(tx0, fy + 62, 205, "WHAT HAPPENED WHEN  <font color='#5A6675'>(12 Oct to 9 Nov)</font>", 6.6, NAVY, True)
lanes = ["ADT", "Claims", "Pharmacy", "Clinical", "Auth / UM", "Contacts"]
ly0 = fy + 80
lane_h = 35
x_a, x_b = tx0 + 44, tx0 + 205
def xd(day):  # day offset from 12 Oct (0) to 9 Nov (28)
    return x_a + (x_b - x_a) * day / 28
for i, ln in enumerate(lanes):
    yy2 = ly0 + i * lane_h
    d.text(tx0, yy2 + 9, 42, ln, 6.4, SOFT, True)
    d.line(x_a, yy2 + 14, x_b, yy2 + 14, MID, 0.5)
d.rect(xd(14), ly0 + 1 * lane_h + 3, xd(28) - xd(14), 22, fill=GRAY, stroke=MID, r=2, dash=(2, 2))
d.text(xd(14) + 2, ly0 + lane_h + 7, xd(28) - xd(14) - 4, "not yet visible (claims lag)", 5.6, SOFT, align=1)
d.rect(xd(21), ly0 + 6, xd(25) - xd(21), 10, fill=RED, r=2)
d.text(xd(21) - 12, ly0 + 17, 70, "2-6 Nov admit", 5.6, RED)
d.circle(xd(2), ly0 + lane_h + 14, 3, NAVY); d.text(xd(2) - 12, ly0 + lane_h + 18, 60, "cardiology 14 Oct", 5.4, SOFT)
d.circle(xd(7), ly0 + 2 * lane_h + 14, 3, GREEN); d.text(xd(7) - 8, ly0 + 2 * lane_h + 18, 60, "furosemide 19 Oct", 5.4, SOFT)
d.circle(xd(25), ly0 + 2 * lane_h + 14, 4, RED); d.text(xd(25) - 52, ly0 + 2 * lane_h + 18, 60, "REJECT 6 Nov (PA)", 5.4, RED)
d.circle(xd(26), ly0 + 3 * lane_h + 14, 3, NAVY); d.text(xd(26) - 60, ly0 + 3 * lane_h + 18, 70, "discharge summary 7 Nov", 5.4, SOFT)
d.circle(xd(25), ly0 + 4 * lane_h + 14, 3.5, AMBER); d.text(xd(25) - 60, ly0 + 4 * lane_h + 18, 70, "home health pending", 5.4, SOFT)
d.circle(xd(0), ly0 + 5 * lane_h + 14, 3, GREEN); d.text(xd(0) - 4, ly0 + 5 * lane_h + 18, 90, "call connected 12 Oct", 5.4, SOFT)
d.text(xd(28) - 52, ly0 + 5 * lane_h + 5, 56, "<font color='#D2453D'>no contact this episode</font>", 5.4, RED, align=2)
d.text(tx0, ly0 + 6 * lane_h + 2, 205, "<font color='#5A6675'>Hollow / grey = expected but not received. Absence is never shown as 'no event'.</font>", 6, SOFT, lead=7.4)
# right: med rec
mx = fx + 420
d.text(mx, fy + 62, 190, "MEDICATION RECONCILIATION", 6.6, NAVY, True)
mrows = [["Drug", "Discharge 6 Nov", "PCP list 3 Oct", "Last fill"],
         ["Sac/val", "24/26 BID (new)", "-", "REJECTED PA"],
         ["Lisinopril", "STOPPED", "10 mg daily", "-"],
         ["Furosemide", "40 mg BID", "20 mg daily", "40 mg, 19 Oct"],
         ["Carvedilol", "12.5 mg BID", "12.5 mg BID", "12 Sep (gap?)"],
         ["Spironol.", "25 mg (new)", "-", "none"]]
fl = {(1, 3): LRED, (2, 1): LRED, (2, 2): LRED, (3, 1): LAMB, (3, 2): LAMB, (4, 3): LAMB}
mb = d.table(mx, fy + 74, [50, 50, 46, 44], mrows, 6.2, pad=2, zebra=False, fills=fl)
d.text(mx, mb + 3, 188, "<font color='#D2453D'><b>Red</b></font> = conflict or blocked, <font color='#E8A02F'><b>amber</b></font> = needs check. Both values stay visible with source and date. <b>Product never picks a winner</b>; Maria confirms with member and prescriber.<br/>Fill confidence: High (PBM claim). Carvedilol: Medium (discharge supply possible).", 6.8, INK, lead=8.2)
# bottom NBA
by = fy + 332
d.rect(fx + 6, by, fw - 12, 98, fill=LTEAL, r=4)
d.text(fx + 12, by + 5, 300, "NEXT BEST ACTIONS  <font color='#5A6675'>(ordered by deadline; each one-click)</font>", 6.8, NAVY, True)
cards = [("1  File the prior auth", "Task to UM with discharge summary attached; ask prescriber about lisinopril overlap.", "Create task"),
         ("2  Call Eleanor now (mobile, verified)", "Prompts: weight today? scale at home? symptoms? who picks up meds? which pills in the cabinet?", "Start call"),
         ("3  Book PCP visit by Fri 13 Nov", "In-network PCP slots; offer ride; chase home-health auth.", "Find slots")]
for i, (h_, b_, bt) in enumerate(cards):
    x_ = fx + 12 + i * 197
    d.rect(x_, by + 20, 190, 72, fill=white, stroke=MID, r=3, lw=0.5)
    d.text(x_ + 5, by + 24, 180, "<b>%s</b>" % h_, 7.6, NAVY, lead=9)
    d.text(x_ + 5, by + 44, 180, b_, 7.2, INK, lead=8.8)
    btn(x_ + 5, by + 74, 60, bt, TEAL, 6, 13)
d.text(ax, 64, 280, "How to read it", 10, NAVY, True)
annot(ax, 82, [
    (1, "Header = status and freshness.", "Program, risk with trend, clock, and the age of every feed at all times. Claims 'data through' is amber by design."),
    (2, "Situation = AI draft with receipts.", "Three lines max, each with source chips. Nurse taps Confirm or Edit; only confirmed lines enter the case record."),
    (3, "Timeline with ghosts.", "One lane per dataset. Grey zone shows where claims cannot yet see; hollow markers show expected-but-missing items."),
    (4, "Medication reconciliation.", "Source-by-source columns; conflicts coloured; confidence on fills (cash fills may be invisible). No auto-merge: this is Maria's clinical judgment moment."),
    (5, "Actions at the bottom.", "Each action is a task with owner and deadline, created in one click; drives the queue."),
], 280, 8.6)
d.foot("Design basis: HEDIS TRC (med reconciliation, patient engagement), Part D adherence (PDC); AGS Beers. Clinical statements are decision prompts for the nurse and prescriber, not advice generated by the product.")

# ============================================================ 10 OUTREACH + DOC
d.slide("D. Product design (3/3): Outreach and documentation turn a call into a record, not a second job",
        "Wireframe for Danielle Okafor (P4), day 6 after psychiatric discharge. Left: reach her. Right: document once, confirm once.", "D. Product design")
frame(fx, fy, fw, 436, "workbench.plan.com / member / M-30058 / outreach + documentation")
d.rect(fx + 6, fy + 24, fw - 12, 22, fill=GRAY, r=3)
d.text(fx + 12, fy + 29, 590, "<b>Danielle Okafor</b>  34F  |  Marketplace Silver  |  English  |  Post-psych discharge day 6  |  <font color='#D2453D'><b>BH consent: limited sharing (notes masked for non-BH roles)</b></font>", 7, NAVY)
ox = fx + 8
d.text(ox, fy + 52, 280, "OUTREACH  <font color='#5A6675'>(contact graph)</font>", 6.8, NAVY, True)
d.rect(ox, fy + 64, 288, 44, fill=LTEAL, r=3)
d.text(ox + 5, fy + 68, 280, "<b>Recommended: text now, call 12:00-14:00.</b> Texting got a reply on 4 Nov; 2 voicemails; prepaid phone often out of minutes. Consent to SMS on file.", 7.4, INK, lead=9)
nrows = [["#", "Number / channel", "Source", "Evidence"],
         ["1", "555-0161 mobile (prepaid)", "Enrollment", "2 voicemail; <b>SMS reply 4 Nov</b>"],
         ["2", "555-0188 (friend)", "Call centre 30 Oct", "Unverified; ask consent first"],
         ["3", "Mailing address", "Enrollment", "Returned 21 Oct: do not use"]]
nb = d.table(ox, fy + 114, [14, 100, 70, 104], nrows, 6.9, pad=2.6, zebra=False, fills={(1, 3): LTEAL, (3, 3): LRED})
d.text(ox, nb + 5, 280, "SMS DRAFT  <font color='#16908A'>(AI, you review and send)</font>", 6.6, NAVY, True)
d.rect(ox, nb + 16, 288, 52, fill=white, stroke=MID, r=3)
d.text(ox + 5, nb + 20, 278, "\"Hi Danielle, this is Maria, a nurse from your health plan. I am checking in after your hospital stay. Can I call you today? Reply YES or tell me a better time. Reply STOP to opt out.\"", 7.2, INK, lead=8.8)
btn(ox + 200, nb + 54, 40, "Edit", SOFT, 5.8, 11); btn(ox + 244, nb + 54, 40, "Send", TEAL, 5.8, 11)
d.text(ox, nb + 76, 280, "CALL PROMPTS  <font color='#5A6675'>(from the data; order is Maria's)</font>", 6.6, NAVY, True)
d.text(ox, nb + 88, 285, "&bull; Safety check first (follow your protocol)<br/>&bull; Meds: quetiapine + sertraline not picked up. Why? Which pharmacy is near you now?<br/>&bull; Follow-up booked day 8 (11 Nov): can we move it to Tue 10 Nov by video?<br/>&bull; Housing: friend's place per 30 Oct note; confirm current location<br/>&bull; Transport / phone minutes: any barrier?", 7.3, INK, lead=9.4)
# right: documentation
dx = fx + 308
d.text(dx, fy + 52, 280, "DOCUMENTATION  <font color='#5A6675'>(live during the call)</font>", 6.8, NAVY, True)
d.text(dx, fy + 64, 296, "BH follow-up assessment: <b>38 fields</b>", 7.2, NAVY, True)
d.rect(dx, fy + 76, 296, 10, fill=GRAY, r=2)
d.rect(dx, fy + 76, 296 * 24 / 38, 10, fill=GREEN, r=2)
d.rect(dx + 296 * 24 / 38, fy + 76, 296 * 8 / 38, 10, fill=AMBER, r=0)
d.rect(dx + 296 * 32 / 38, fy + 76, 296 * 6 / 38, 10, fill=RED, r=2)
d.text(dx, fy + 90, 296, "<font color='#2E9E5B'><b>24 pre-filled</b></font> (confirm)   <font color='#E8A02F'><b>8 stale</b></font> (re-ask)   <font color='#D2453D'><b>6 to ask</b></font>", 6.6, INK)
arows = [["Field", "Value", "State"],
         ["Discharge date, facility", "3 Nov, inpatient psych", "Filled: ADT"],
         ["Discharge meds", "sertraline 100, quetiapine 100", "Filled: summary"],
         ["Meds taken since discharge", "?", "Ask"],
         ["Housing", "'Stable' (Jun) vs 'friend's place' (30 Oct)", "Stale: conflict"],
         ["Phone / SMS consent", "Mobile, SMS yes", "Filled: confirm"],
         ["Safety screen result", "?", "Ask (never auto-filled)"]]
fl2 = {(1, 2): LTEAL, (2, 2): LTEAL, (3, 2): LRED, (4, 2): LAMB, (5, 2): LTEAL, (6, 2): LRED}
ab = d.table(dx, fy + 104, [88, 128, 80], arows, 6.8, pad=2.6, zebra=False, fills=fl2)
d.text(dx, ab + 5, 296, "NOTE DRAFT  <font color='#16908A'>(AI from your quick tags; not saved until you sign)</font>", 6.6, NAVY, True)
d.rect(dx, ab + 16, 296, 62, fill=white, stroke=MID, r=3)
d.text(dx + 5, ab + 20, 286, "<font color='#5A6675'>[Draft]</font> Called member day 6 post-discharge. Reports <i>[you fill]</i>. Discharge meds not yet obtained; Rx to be re-sent to <i>[pharmacy]</i>. Follow-up moved to <i>[date]</i>. Barriers: <i>[housing, phone minutes]</i>. Plan: <i>[next contact]</i>.", 7.2, INK, lead=8.8)
d.text(dx, ab + 84, 296, "CARE PLAN  <font color='#16908A'>(auto-updated, confirm)</font>", 6.6, NAVY, True)
d.text(dx, ab + 95, 296, "Goal: attend psychiatry visit by 10 Nov  |  Barrier: phone, transport  |  Intervention: telehealth, ride, Rx to nearby pharmacy", 7.2, INK, lead=8.8)
btn(dx + 160, fy + 405, 136, "Review, sign and file (once)", TEAL, 6.8, 18)
d.text(dx, fy + 408, 150, "<font color='#5A6675'>One entry writes assessment, plan, call log and audit export.</font>", 6, SOFT, lead=7)
d.text(ax, 64, 280, "How to read it", 10, NAVY, True)
annot(ax, 82, [
    (1, "Channel, time, number: a recommendation with the reason.", "Ranked from source, recency and past success (cross-source: pharmacy, provider, call centre). Dead numbers are demoted automatically."),
    (2, "SMS and call prompts.", "Drafted from the data, sent only by the nurse, only with consent on file (TCPA). Prompts follow clinical order; she chooses."),
    (3, "Assessment pre-filled with states.", "Green: from records, confirm. Amber: stale or conflicting, re-ask. Red: only the member can answer, never auto-filled (e.g. safety screen)."),
    (4, "Note and care plan are drafts.", "Structured quick-tags in, narrative out, with blanks where a clinical fact is needed. Nothing is saved until she signs."),
    (5, "Write once, file once.", "One sign-off updates assessment, plan, call log and audit form. Removes the same-fact-four-times burden."),
], 280, 8.6)
d.foot("Design basis: CMS TCM / HEDIS FUH 7-day follow-up; TCPA consent for SMS; 42 CFR Part 2 and plan BH consent rules (role-based masking); NCQA/URAC case-management documentation expectations.")

# ============================================================ 11 WALKTHROUGH + AI BOUNDARY
d.slide("D. Walkthrough: three patients through the screens, and where AI stops and the nurse starts",
        "Same three screens, three different stories. Each step names the data that makes it possible.", "D. Product design")
wrows = [["Patient", "1  Queue (8:00)", "2  Member 360 (8:05)", "3  Outreach / documentation (8:15+)", "What Maria does differently vs today"],
         ["<b>P1 Eleanor Marsh</b><br/>HF discharge, conflicting meds",
          "Rank 1 (91). Clock: contact due Tue. Why: HF discharge, new drug rejected (PA).",
          "Rx lane shows REJECT 6 Nov; claims lane greyed (lag). Med table: lisinopril stopped vs still on PCP list.",
          "Mobile verified. Call prompts: weight, scale, meds in cabinet. PA task to UM; PCP visit by Fri 13.",
          "Finds the blocked drug on day 3, not day 7 or at readmission. Flags the overlap to the prescriber instead of discovering it later."],
         ["<b>P3 Tyrell Brooks</b><br/>Frequent ED, unreachable",
          "Rank 3 (74). Why: 6th ED visit (ADT), no controller fill. Reach: 2 of 3 numbers dead.",
          "ADT shows 6 ED visits vs claims 4 (match 82% flagged). Contact graph: #3 from pharmacy profile, never tried.",
          "Text #3, call 11:00; ask pharmacy and PCP to relay; Medicaid recertification (30 Nov) as the reason to talk.",
          "Stops redialling dead numbers (9 failed attempts). First connect comes from a number found in another system."],
         ["<b>P4 Danielle Okafor</b><br/>BH + housing",
          "Rank 2 (85). Clock: window ends Tue. Reach: SMS works, voice poor.",
          "Appointments lane: follow-up day 8 outside 7-day window. Housing badge: stale screen conflicts with 30 Oct note.",
          "SMS first; assessment 24/38 pre-filled; safety screen left for her; care plan goal 'psychiatry visit by 10 Nov'.",
          "Rebooks inside the window; fixes the pharmacy location; does not re-ask what the plan already knows."]]
wb_ = d.table(28, 64, [88, 168, 190, 210, 248], wrows, 8.8, pad=6, col_bold=())
y = wb_ + 14
d.text(28, y, 700, "Human-in-the-loop: what is automated, what is suggested, what the nurse decides", 11, NAVY, True)
brows = [["Automated (no review needed)", "AI-drafted, nurse must confirm", "Nurse decides", "Never done by the product"],
         ["Record matching and dedupe; freshness and 'data through' labels; adherence (PDC) maths; contact-number ranking; score calculation; clock calculation.",
          "'Situation' summary; next best action; SMS draft; note draft; assessment pre-fill; phone numbers lifted from free text; merge candidates for duplicate cases.",
          "What the member said; med reconciliation outcome; risk and safety assessment; care plan goals; whether to escalate; closing or transitioning the case.",
          "Diagnose or advise treatment; send messages without consent; auto-resolve conflicting data; write unconfirmed text into the record; auto-close a case."]]
bb = d.table(28, y + 16, [226, 226, 226, 226], brows, 9, pad=6, zebra=False, col_bold=(), fills={(1, 0): LTEAL, (1, 1): LAMB, (1, 2): LBLUE, (1, 3): LRED})
d.text(28, bb + 8, 900,
       "<b>Trust mechanics:</b> every AI line cites its source records; edits and dismissals are logged and reviewed weekly with a nurse advisory group; the product shows what it does not know ('not received yet', 'confidence: medium') instead of filling gaps; "
       "accepted-without-edit rate and override reasons are tracked as product metrics.", 9.4, INK, lead=12)
d.foot("Synthetic patients: annex sheet 'Synthetic_Records'. Score values from annex 'Priority_Score'.")

# ============================================================ 12 PRIORITISE & MEASURE
d.slide("E. Prioritize and measure: ship the smallest thing that gives Maria her mornings back, then prove it in a pilot",
        "MVP cut and logic, success metrics with baselines and targets, risks with mitigations, and a pilot / go-to-market sketch.", "E. Prioritize & measure")
d.text(28, 62, 440, "MVP vs later", 9.5, NAVY, True)
mv = [["MVP (12-16 wks, 1 program)", "Phase 2", "Later"],
      ["Queue with clock + reason + score; Member 360 on D1-D5, D7, D9-D12, D21; contact graph; med conflict view; AI summary, note and assessment pre-fill with confirm; SMS with consent",
       "SDOH closed-loop referrals; care gaps (HEDIS); network search + booking; benefits; caregiver profile; scheduling feeds; labs trends",
       "RPM / wearables; Medicaid LTSS feeds; voice-to-note; member app; predictive dialer; multi-language auto-outreach"]]
mb2 = d.table(28, 76, [200, 125, 115], mv, 8, pad=4, zebra=False, col_bold=(), fills={(1, 0): LTEAL, (1, 1): LAMB, (1, 2): GRAY})
d.text(28, mb2 + 5, 440,
       "<b>Prioritisation logic.</b> Rank each capability by (decisions it changes x frequency x clinical risk) / (integration effort x data-quality risk). "
       "ADT + pharmacy + discharge summary score highest: they create the clock and explain the event, and the plan already holds them. Scheduling and wearables score low: high effort, patchy data. "
       "<b>Cut line:</b> if it does not change a decision on Monday at 8 am, it is Phase 2.", 8.2, INK, lead=10)
gy = mb2 + 82
d.rect(28, gy, 440, 500 - gy, fill=LBLUE, r=5)
d.text(36, gy + 5, 424, "Pilot and go-to-market (brownie points)", 9, NAVY, True)
d.text(36, gy + 20, 424,
       "<b>Buyer.</b> Economic: CMO / VP Care Management; also Stars and Quality lead (TRC, FUH, adherence). Champion: Director of Case Management. Target: regional MA / D-SNP / Medicaid plan, 150-500k members, already ingesting claims and ADT.<br/>"
       "<b>Pilot.</b> 12 weeks, one program (transitions of care + HF/COPD), ~25 nurses (~1,200 active cases), shadow 8 nurses for baseline in weeks 1-2, matched control team. Go/no-go gates: prep time -50%, TOC 2-day contact >= 80%, nurse NPS positive.<br/>"
       "<b>Pricing signal (assumption).</b> Per-nurse-seat SaaS, ~$400-600/seat/month (~$5-7k/yr) vs ~$110-130k fully loaded RN. A 20% capacity gain on 25 nurses is ~5 FTE (~$0.6M/yr), plus Stars / readmission upside; land with seats, expand with PMPM tiers.", 8.6, INK, lead=11)
tl = [("Wk 1-2", "Shadow 8 nurses; baseline"), ("Wk 3-4", "Connect ADT, Rx, CCD; go live for 5 nurses"), ("Wk 5-12", "Scale to 25; weekly review"), ("Wk 12", "Readout vs control; go/no-go")]
for i, (a_, b_) in enumerate(tl):
    xx = 36 + i * 107
    d.rect(xx, 500 - 62, 101, 52, fill=white, stroke=MID, r=4, lw=0.6)
    d.text(xx + 5, 500 - 58, 92, "<b>%s</b>" % a_, 8, TEAL)
    d.text(xx + 5, 500 - 45, 92, b_, 7.4, INK, lead=8.8)
mx2 = 484
d.text(mx2, 62, 450, "Success metrics (baselines are assumptions to be confirmed in pilot week 1)", 9.5, NAVY, True)
mt = [["Metric", "Baseline", "Pilot target"]] + [[m[0], m[1], m[2]] for m in METRICS]
mtb = d.table(mx2, 76, [200, 90, 158], mt, 8, pad=3.4, col_bold=())
d.text(mx2, mtb + 8, 450, "Risks and mitigations", 9.5, NAVY, True)
rr = [["Risk", "Mitigation"]] + [[r[0], r[1]] for r in RISKS]
d.table(mx2, mtb + 22, [110, 338], rr, 7.8, pad=3.4, col_bold=(0,), hfill=RED)
d.foot("Sources: BLS / public RN salary ranges (assumed $110-130k loaded); SaaS seat-pricing norms; NCQA HEDIS; CMS Star Ratings. Pricing and ROI are directional, not quotes. Metric details in annex sheet 'Metrics'.")
