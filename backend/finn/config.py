import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
CACHE = DATA / "cache"
SNAPSHOT = DATA / "snapshot"
CACHE.mkdir(parents=True, exist_ok=True)

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

# Mock portfolio: 18 names across sectors and sizes. bse = BSE scrip code.
PORTFOLIO = [
    ("RELIANCE", "Reliance Industries", "Conglomerate", "500325"),
    ("TCS", "Tata Consultancy Services", "IT", "532540"),
    ("INFY", "Infosys", "IT", "500209"),
    ("KPITTECH", "KPIT Technologies", "IT / Auto-tech", "542651"),
    ("HDFCBANK", "HDFC Bank", "Banks", "500180"),
    ("ICICIBANK", "ICICI Bank", "Banks", "532174"),
    ("BAJFINANCE", "Bajaj Finance", "NBFC", "500034"),
    ("BHARTIARTL", "Bharti Airtel", "Telecom", "532454"),
    ("MARUTI", "Maruti Suzuki", "Auto", "532500"),
    ("TITAN", "Titan Company", "Consumer", "500114"),
    ("ASIANPAINT", "Asian Paints", "Consumer", "500820"),
    ("TRENT", "Trent", "Retail", "500251"),
    ("DMART", "Avenue Supermarts", "Retail", "540376"),
    ("SUNPHARMA", "Sun Pharma", "Pharma", "524715"),
    ("LT", "Larsen & Toubro", "Capital goods", "500510"),
    ("POLYCAB", "Polycab India", "Capital goods", "542652"),
    ("HAL", "Hindustan Aeronautics", "Defence", "541154"),
    ("PIDILITIND", "Pidilite Industries", "Chemicals", "500331"),
]
RESEARCH_DEMO = ["TCS", "ASIANPAINT", "TITAN", "KPITTECH", "BAJFINANCE"]
BSE_CODES = {t: b for t, _, _, b in PORTFOLIO}
NAMES = {t: n for t, n, _, _ in PORTFOLIO}
SECTORS = {t: s for t, _, s, _ in PORTFOLIO}

LLM_BASE = os.getenv("FINN_LLM_BASE_URL", "https://api.openai.com/v1")
LLM_KEY = os.getenv("FINN_LLM_API_KEY", "")
LLM_CHEAP = os.getenv("FINN_LLM_CHEAP_MODEL", "gpt-4o-mini")
LLM_STRONG = os.getenv("FINN_LLM_STRONG_MODEL", "gpt-4o")
