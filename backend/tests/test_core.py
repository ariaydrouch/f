import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from finn.classify import classify, tier  # noqa: E402
from finn.research import _call_quarter, guidance_quotes  # noqa: E402


def test_results_outrank_routine():
    assert classify("Audited Financial Results For The Quarter Ended 30Th September", "")[0] == "results"
    assert classify("Audited Financial Results For The Quarter", "results")[1] >= 90
    assert tier(classify("ESOP allotment", "")[1]) == "routine"


def test_newspaper_ad_demoted():
    cat, score = classify("Newspaper Publication", "Unaudited Financial Results published")
    assert cat == "results" and score < 40


def test_mgmt_and_fundraise():
    assert classify("Change in Directorate", "appointed CFO")[0] == "management_change"
    assert classify("Intimation of Repayment of Commercial Paper", "redeemed")[1] < 40
    assert classify("Meeting updates", "opens QIP, floor price set")[1] >= 80


def test_guidance_extraction_and_disclaimer():
    t = ("This call may contain forward-looking statements and risks that the company faces which could differ. "
         "We expect revenue growth of 12% to 14% in the next fiscal year driven by strong order books. "
         "We do not provide any specific revenue guidance as a matter of policy.")
    g = guidance_quotes(t)
    assert any("12% to 14%" in q for q in g["quotes"])
    assert g["no_explicit_guidance"]


def test_call_quarter_mapping():
    cols = ["Dec 2025", "Mar 2026", "Jun 2026", "Sep 2026"]
    assert _call_quarter("Oct 2026", cols) == "Sep 2026"
    assert _call_quarter("Jan 2026", cols) == "Dec 2025"
