#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HOZOO MD - TikTok Mass Reporter (INLINE COOKIES)
Owner: NIGHT X NICK
Version: 2.0
Mode: Hardcore Unrestricted
"""

import os, sys, json, time, random, string, threading, requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================
# ===  TARUH COOKIES AKUN LO DI SINI (TANPA FOLDER)  =========
# ===  Bisa string cookie mentah, atau JSON, campur aja  =====
# ============================================================
COOKIES_POOL = [
    # --- AKUN 1 (format string) ---
    """tt_csrf_token=gUle1K9q-FDZK6Y_oE0RRKFDltaxquni6iMk; tiktok_webapp_theme_source=auto; tiktok_webapp_theme=dark; s_v_web_id=verify_mvxewd8e_8viViO62_Xppp_4NQN_APIK_NzjON2gpVQsI; d_ticket=90a48b422c8b749b7b2c8fb96589b4fa8b093; multi_sids=7689720884119438344%3Aaa2f60ab7956f47b6763453f2be825e4; sessionid=aa2f60ab7956f47b6763453f2be825e4; uid_tt_ss=e1883a551524c2968a2b5fff41c9c7013d143ac263727465ece52ac2e34ab144; uid_tt=e1883a551524c2968a2b5fff41c9c7013d143ac263727465ece52ac2e34ab144; sid_tt=aa2f60ab7956f47b6763453f2be825e4; tt-target-idc=alisg; store-country-code=id; store-country-code-src=uid; store-idc=alisg; tt-target-idc-sign=lh9nC9__l6qgK4wXHxW1fK3vg3t5nhMTj0h_dKaYVR-IvsenUCxsvqRfjOjSgPw_amk8AyVmX6QFfWAF-qYJsaPVOj9JgdAIOI8Vi8BGr3lpiyW5hkdOafnuBy5xzlbaHZRLAi_ULN-KG_d5NuwerQCJ-_oMz-gTVWZgk0lU5F6xBg8ks8G0FP61jiL2BS6Fn0fzY8Evd3yyhzzUGh9MreC3BB_gjpRdP6LVpKyi0iZc29Cdevg6jdvB0wHBK2KlLZ1oKkgQuSyO_Wg48KsdojcpP5wYVEejAd0z6-Gw0LUdmaroqTBic5tDh-W-yxbQg5abgoFIkefwUiC23EKb2XmedKB1NzPphfcBIrOTj2zm_wXyltx3pCtbfF5RDic5jYi_1ivbgwVAGtVUWbkMRDR-5EbJ2yj_Sd7ZT-MOHG7ixdlvxoTyVuiZLtPayE_qtqgNj2kGm03oHl-uEdQPwhJdxYHcRhMVtF9Y-83WuvRz7OO2Hb6KX02qBi4AgSKt; sessionid_ss=aa2f60ab7956f47b6763453f2be825e4; last_login_method=email; tt_chain_token=cD4V5PcVObtqoxi1ARb9RQ==; x-web-secsdk-uid=44e2be44-9c39-4d81-a505-411710d7e4e7; odin_tt=2c3ae47883d33fbdf979d36b614e95d19fac814f3034cf6ff6a7bbb531e58cef6f7c10fd82dc298a5ec46a59cffbecb6186d69ccf8b5a3ccfcec3a05d4e933cf93017ad44465693c9c8633ece886c7cb; ttwid=1%7CkPpWAy2ZeU376v-9yVrq0Hh54fpDVvecLuKgNwoGfIw%7C1793513090%7C2110476b815e569521b6c5e43ec6a9792daa23902a6bcf55e77df2ae23fc5166; sid_guard=aa2f60ab7956f47b6763453f2be825e4%7C1793513091%7C15551982%7CFri%2C+30-Apr-2027+06%3A04%3A33+GMT; msToken=WyT9h6btF9No91Wc765RMax4pR-O4WV-4rJ7YYgDr9nmkazwWbJvfq1ZpqzngNZqOJLipuyhHsMnrcn5JpjnFYHUiyQAoqLTnKzkstIhQbaoh4AsQ6niS2GHxjLt3S87vVe9om0sBwWWYFvj216uDpNcd1nEv38g9xhzIpvAdjqJ""",

    # --- TAMBAHIN AKUN 2 DI SINI ---
    # """sessionid=ISI_SESSIONID_AKUN2; tt_csrf_token=ISI_TOKEN_AKUN2; uid_tt=ISI_UID_AKUN2;""",

    # --- TAMBAHIN AKUN 3 DI SINI ---
    # """sessionid=ISI_SESSIONID_AKUN3; tt_csrf_token=ISI_TOKEN_AKUN3; uid_tt=ISI_UID_AKUN3;""",

    # --- Contoh format JSON ---
    # '{"sessionid":"xxx","tt_csrf_token":"yyy","uid_tt":"zzz"}',
]

# ============================================================
# CONFIG
# ============================================================
LOG_FILE = "hozoo_report_log.txt"

class C:
    R="\033[91m"; G="\033[92m"; Y="\033[93m"; B="\033[94m"
    M="\033[95m"; C="\033[96m"; W="\033[97m"; RST="\033[0m"; BD="\033[1m"

REPORT_TYPES = {
    "1":  ("Spam",                    "reportType_spam"),
    "2":  ("Konten Tidak Pantas",     "reportType_inappropriate"),
    "3":  ("Pelecehan / Bullying",    "reportType_harassment"),
    "4":  ("Ujaran Kebencian",        "reportType_hate_speech"),
    "5":  ("Kekerasan / Berbahaya",   "reportType_violence"),
    "6":  ("Konten Seksual",          "reportType_sexual_content"),
    "7":  ("Penipuan / Scam",         "reportType_fraud"),
    "8":  ("Akun Palsu / Fake",       "reportType_fake_account"),
    "9":  ("Pelanggaran Hak Cipta",   "reportType_copyright"),
    "10": ("Informasi Salah",         "reportType_misinformation"),
    "11": ("Narkoba",                 "reportType_drugs"),
    "12": ("Perjudian",               "reportType_gambling"),
    "13": ("Terrorisme",              "reportType_terrorism"),
    "14": ("Lainnya",                 "reportType_other"),
    "15": ("RANDOM SEMUA",            "random"),
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Mobile Safari/537.36",
]

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    cmap = {"INFO":C.C, "OK":C.G, "ERR":C.R, "WARN":C.Y, "SYS":C.M, "REP":C.B}
    col = cmap.get(level, C.W)
    print(f"{col}[{ts}][{level}] {msg}{C.RST}")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}][{level}] {msg}\n")
    except Exception:
        pass

def parse_cookie(raw):
    """Parse cookie mentah string / JSON jadi dict"""
    raw = raw.strip()
    if not raw:
        return None
    # coba JSON
    if raw.startswith("{"):
        try:
            d = json.loads(raw)
            if isinstance(d, dict) and d:
                return d
        except Exception:
            pass
    # parse string
    cd = {}
    for part in raw.split(";"):
        part = part.strip()
        if "=" in part:
            k, v = part.split("=", 1)
            k, v = k.strip(), v.strip()
            if k:
                cd[k] = v
    return cd if cd else None

def load_accounts():
    """Load semua cookie dari COOKIES_POOL internal"""
    accounts = []
    for idx, raw in enumerate(COOKIES_POOL, 1):
        cd = parse_cookie(raw)
        if not cd:
            log(f"Akun #{idx}: cookie kosong/gagal parse, skip.", "WARN")
            continue
        if not any(k in cd for k in ("sessionid", "sessionid_ss")):
            log(f"Akun #{idx}: tidak ada sessionid, skip.", "WARN")
            continue
        accounts.append({"name": f"akun{idx}", "cookies": cd})
        log(f"Akun #{idx} loaded ({len(cd)} cookies)", "OK")
    return accounts

def build_session(cookie_dict):
    s = requests.Session()
    s.headers.update({
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://www.tiktok.com",
        "Referer": "https://www.tiktok.com/",
        "Sec-Ch-Ua": '"Not:A-Brand";v="8", "Chromium";v="156"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Connection": "keep-alive",
    })
    for k, v in cookie_dict.items():
        try:
            s.cookies.set(k, v, domain=".tiktok.com")
        except Exception:
            pass
    return s

def get_csrf(session):
    for name in ("tt_csrf_token", "csrf_token"):
        for c in session.cookies:
            if c.name == name and c.value:
                return c.value
    token = ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=32))
    session.cookies.set("tt_csrf_token", token, domain=".tiktok.com")
    return token

def resolve_user_id(session, username_or_id):
    if username_or_id.isdigit() and len(username_or_id) > 8:
        return username_or_id
    username = username_or_id.lstrip("@")
    try:
        r = session.get(
            "https://www.tiktok.com/api/user/detail/",
            params={"aid":"1988", "uniqueId":username},
            timeout=15
        )
        if r.status_code == 200:
            uid = r.json().get("userInfo", {}).get("user", {}).get("id")
            if uid:
                return str(uid)
    except Exception:
        pass
    return None

def get_report_reasons(session):
    try:
        r = session.get(
            "https://www.tiktok.com/api/report/reasons/",
            params={"aid":"1988", "reportType":"user"},
            timeout=15
        )
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def send_report(session, account_name, target_uid, reason_list, target_type="user"):
    csrf = get_csrf(session)
    reason = random.choice(reason_list) if isinstance(reason_list, list) else reason_list
    url = "https://www.tiktok.com/api/report/user/"
    if target_type == "video":
        url = "https://www.tiktok.com/api/report/video/"

    payload = {
        "aid": "1988",
        "reportType": "user",
        "objectId": target_uid,
        "reasonId": reason,
        "reasonText": "",
        "locale": "id",
        "csrf_token": csrf,
        "extra": json.dumps({
            "reportReason": reason,
            "source": "web",
            "targetUserId": target_uid,
            "objectId": target_uid,
        })
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "X-Secsdk-Csrf-Token": csrf,
        "Referer": f"https://www.tiktok.com/@{target_uid}",
    }
    try:
        r = session.post(url, data=payload, headers=headers, timeout=20)
        ok = r.status_code in (200, 204)
        if ok:
            log(f"[{account_name}] ✔ REPORT OK → {target_uid} | reason={reason}", "REP")
        else:
            log(f"[{account_name}] ✖ gagal {r.status_code} | reason={reason}", "ERR")
        return ok
    except Exception as e:
        log(f"[{account_name}] ✖ EXC: {e}", "ERR")
        return False

def report_worker(account, target_uid, reason_list, cycles, delay_range, stop_event, stats, lock):
    session = build_session(account["cookies"])
    name = account["name"]
    resolved = resolve_user_id(session, target_uid) or target_uid
    get_report_reasons(session)

    for i in range(cycles):
        if stop_event.is_set():
            break
        ok = send_report(session, name, resolved, reason_list)
        with lock:
            stats["total"] += 1
            if ok:
                stats["ok"] += 1
            else:
                stats["fail"] += 1
        time.sleep(random.uniform(delay_range[0], delay_range[1]))
    log(f"[{name}] worker selesai ({cycles} percobaan)", "SYS")

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""{C.M}{C.BD}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║            ██╗  ██╗ ██████╗ ███████╗ ██████╗  ██████╗      ║
║            ██║  ██║██╔═══██╗╚══███╔╝██╔═══██╗██╔═══██╗     ║
║            ███████║██║   ██║  ███╔╝ ██║   ██║██║   ██║     ║
║            ██╔══██║██║   ██║ ███╔╝  ██║   ██║██║   ██║     ║
║            ██║  ██║╚██████╔╝███████╗╚██████╔╝╚██████╔╝     ║
║            ╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝      ║
║                     ███╗   ███╗██████╗                     ║
║                     ████╗ ████║██╔══██╗                    ║
║                     ██╔████╔██║██║  ██║                    ║
║                     ██║╚██╔╝██║██║  ██║                    ║
║                     ██║ ╚═╝ ██║██████╔╝                    ║
║                     ╚═╝     ╚═╝╚═════╝                     ║
║                                                           ║
║       TIKTOK MASS REPORTER  |  INLINE COOKIES             ║
║       Owner: NIGHT X NICK  |  v2.0 HARDCORE               ║
╚═══════════════════════════════════════════════════════════╝{C.RST}
""")

def show_accounts(accounts):
    print(f"\n{C.C}{C.BD}┌─ AKUN BOT ({len(accounts)}) ─┐{C.RST}")
    if not accounts:
        print(f"{C.R}  (kosong) isi COOKIES_POOL di dalam script!{C.RST}")
    else:
        for i, a in enumerate(accounts, 1):
            print(f"{C.G}  [{i}] {a['name']} ({len(a['cookies'])} cookies){C.RST}")
    print(f"{C.C}└──────────────┘{C.RST}")

def show_report_types():
    print(f"\n{C.Y}{C.BD}┌─ JENIS REPORT ─┐{C.RST}")
    for k, (lbl, _) in REPORT_TYPES.items():
        print(f"{C.W}  [{k:>2}] {lbl}{C.RST}")
    print(f"{C.Y}└─────────────────┘{C.RST}")

def main():
    banner()
    log("HOZOO MD TikTok Reporter v2.0 start", "SYS")
    accounts = load_accounts()
    if not accounts:
        log("Tidak ada akun valid di COOKIES_POOL! Edit script dulu.", "ERR")
        input("Enter untuk keluar...")
        return
    show_accounts(accounts)

    target_input = input(f"\n{C.B}[?] User ID / Username target: {C.RST}").strip()
    if not target_input:
        log("Target kosong.", "ERR"); return
    target_uid = target_input.lstrip("@")

    show_report_types()
    choice = input(f"\n{C.B}[?] Pilih jenis report (1-15): {C.RST}").strip()
    if choice not in REPORT_TYPES:
        log("Pilihan salah.", "ERR"); return
    label, code = REPORT_TYPES[choice]
    log(f"Report: {label} ({code})", "SYS")

    if code == "random":
        reason_list = [v for _, v in REPORT_TYPES.values() if v != "random"]
    else:
        reason_list = [code]

    try:
        cycles = int(input(f"{C.B}[?] Report/akun (default 10): {C.RST}").strip() or "10")
    except ValueError:
        cycles = 10
    try:
        dmin = float(input(f"{C.B}[?] Delay min (0.5): {C.RST}").strip() or "0.5")
        dmax = float(input(f"{C.B}[?] Delay max (2.0): {C.RST}").strip() or "2.0")
    except ValueError:
        dmin, dmax = 0.5, 2.0
    if dmax < dmin: dmin, dmax = dmax, dmin

    print(f"\n{C.Y}{C.BD}─── RINGKASAN ───{C.RST}")
    print(f"  Target     : {C.G}{target_uid}{C.RST}")
    print(f"  Report     : {C.G}{label}{C.RST}")
    print(f"  Akun       : {C.G}{len(accounts)}{C.RST}")
    print(f"  Cycle/akun : {C.G}{cycles}{C.RST}")
    print(f"  Delay      : {C.G}{dmin}-{dmax}s{C.RST}")
    print(f"  Total est. : {C.G}{len(accounts)*cycles} report{C.RST}\n")

    if input(f"{C.B}[?] Mulai? (y/n): {C.RST}").strip().lower() not in ("y","ya","yes"):
        log("Batal.", "WARN"); return

    stop_event = threading.Event()
    stats = {"total":0, "ok":0, "fail":0}
    lock = threading.Lock()
    log(f"Spam report ke {target_uid} pakai {len(accounts)} akun...", "SYS")
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=len(accounts)) as ex:
        futures = [ex.submit(report_worker, a, target_uid, reason_list, cycles, (dmin,dmax), stop_event, stats, lock) for a in accounts]
        try:
            for f in as_completed(futures): pass
        except KeyboardInterrupt:
            log("Interrupted!", "WARN"); stop_event.set()

    print()
    log("═══ HASIL AKHIR ═══", "SYS")
    log(f"Total percobaan : {stats['total']}", "SYS")
    log(f"Berhasil        : {stats['ok']}", "OK")
    log(f"Gagal           : {stats['fail']}", "ERR")
    log(f"Durasi          : {time.time()-t0:.1f}s", "SYS")
    log(f"Log file        : {LOG_FILE}", "SYS")
    print(f"\n{C.G}{C.BD}MISSION COMPLETE. HOZOO MD out 🔥{C.RST}")
    input("\nEnter untuk keluar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.Y}Dibatalkan.{C.RST}"); sys.exit(0)
