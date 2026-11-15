"""Announcement taxonomy + priority scoring. Rules first (free, instant); LLM only for enrichment."""
import re

# (category, regex, base priority 0-100). First match wins, so order matters.
RULES = [
    ("results", r"financial results|quarterly results|unaudited.*results|audited.*results|results for the (quarter|year)|outcome of board meeting.*results|investor presentation|results presentation|shareholder letter", 88),
    ("management_change", r"appointment|resign|cessation|re-?appoint|change in (directors?|management)|senior management|\bCEO\b|\bCFO\b|managing director|key managerial", 80),
    ("M&A", r"acqui|merger|amalgamation|demerger|scheme of arrangement|joint venture|stake (sale|purchase)|subsidiary|divest|takeover|slump sale", 82),
    ("fund_raise", r"rights issue|qip|qualified institutions|preferential|buy-?back|commercial paper|non-?convertible|fund ?rais|allotment of (equity|securities)|\bNCD", 72),
    ("litigation", r"litigation|lawsuit|court|tribunal|nclt|penalty|fine\b|show cause|sebi order|regulatory action|insolvency|search and seizure|gst (demand|order)|income tax (demand|order)", 76),
    ("credit_rating", r"credit rating|rating (update|action|assigned|reaffirm|upgrade|downgrade)", 55),
    ("dividend", r"dividend", 62),
    ("bonus_split", r"bonus (issue|shares)|stock split|sub-?division of", 66),
    ("capex", r"capex|capital expenditure|new plant|capacity expansion|greenfield|brownfield|commission(ing)?", 60),
    ("pledging", r"pledge|encumbrance", 58),
    ("insider_trading", r"insider|trading window|sast|regulation 29|regulation 7\(|disclosure under sebi \(prohibition", 40),
    ("earnings_call", r"earnings call|conference call|con-?call|transcript|audio recording", 45),
    ("investor_meetings", r"analyst|institutional investor|investor meet|investor conference", 30),
    ("agm_egm", r"\bagm\b|\begm\b|annual general meeting|extra-?ordinary general", 35),
    ("postal_ballot", r"postal ballot|e-?voting", 35),
    ("press_release", r"press release|order win|bags? order|wins? order|new order|partnership|launch|collaborat|clarification|rumou?r", 50),
    ("unclassified", r".*", 10),
]

LABELS = {
    "results": "Results", "M&A": "M&A", "fund_raise": "Fund raise", "management_change": "Mgmt change",
    "litigation": "Litigation", "insider_trading": "Insider", "earnings_call": "Earnings call",
    "investor_meetings": "Investor mtg", "credit_rating": "Rating", "dividend": "Dividend",
    "bonus_split": "Bonus/Split", "capex": "Capex", "press_release": "News", "postal_ballot": "Postal ballot",
    "agm_egm": "AGM/EGM", "pledging": "Pledge", "unclassified": "Routine",
}
ALL_CATEGORIES = list(LABELS)
DEFAULT_WATCH = ["results", "M&A", "management_change", "fund_raise", "litigation", "dividend", "bonus_split", "pledging"]

ROUTINE = r"esop|employee stock|certificate under regulation|compliance certificate|newspaper (publication|advertisement)|trading window|loss of share certificate|duplicate share|scrutinizer|reg\.? ?74|reg\.? ?40|esg|business responsibility|auditor"


def classify(title: str, summary: str = "") -> tuple[str, int]:
    text = f"{title} {summary}"
    if re.search(r"transcript|audio recording|earnings call", title, re.I):
        return "earnings_call", 45
    if re.search(r"newspaper", title, re.I) and re.search(r"results", text, re.I):
        return "results", 35
    if re.search(r"reference to the financial results issued by|results of (parent|holding)", title, re.I):
        return "press_release", 52
    if re.search(r"^(audited|unaudited|financial results|outcome of board meeting)", title.strip(), re.I) and re.search(r"results", text, re.I):
        return "results", 96
    if re.search(ROUTINE, text, re.I) and not re.search(r"financial results", text, re.I):
        return "unclassified", 8
    for cat, rx, base in RULES:
        if re.search(rx, text, re.I):
            score = base
            if cat == "results" and re.search(r"intimation|prior intimation|notice of|schedule", text, re.I):
                score = 40
            if cat == "earnings_call" and re.search(r"intimation|schedule|notice", text, re.I):
                score = 28
            if cat == "management_change" and re.search(r"re-?appoint", text, re.I):
                return cat, 58
            if cat == "fund_raise" and re.search(r"repay|redeem|redemption|matur", text, re.I):
                return cat, 30
            if cat == "fund_raise" and re.search(r"qip|opens|floor price|warrant|rights issue", text, re.I):
                score = 84
            if cat == "management_change" and re.search(r"CEO|CFO|managing director|chairman|MD\b", text, re.I):
                score = min(95, score + 10)
            if cat == "press_release" and re.search(r"order|crore|₹|rs\.", text, re.I):
                score = min(75, score + 15)
            return cat, score
    return "unclassified", 10


def tier(score: int) -> str:
    return "must" if score >= 70 else "notable" if score >= 40 else "routine"
