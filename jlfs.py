import asyncio, os, sys, socket, requests, urllib3, subprocess, platform, re, time
from urllib.parse import urlparse, urljoin
from datetime import datetime
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("\033[1;31m[!] Modul 'bs4' belum terinstal. Jalankan: pip install beautifulsoup4\033[0m")
    sys.exit()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ─────────────────────── COLORS ───────────────────────
RED, GREEN, YELLOW, BLUE, CYAN, WHITE, RESET, BOLD = (
    "\033[1;31m", "\033[1;32m", "\033[1;33m", "\033[1;34m",
    "\033[1;36m", "\033[1;37m", "\033[0m", "\033[1m"
)
ORANGE = "\033[1;33m"
MAGENTA = "\033[1;35m"

# ─────────────────────── YOUR IDENTITY ───────────────────────
USER_NAME   = "Luis"
USER_HANDLE = "luis"
USER_ROLE   = "Owner"
TOOL_NAME   = "Luis-Web-Scanner V1.0"
TOOL_POWER  = "Luis-Engine"
TOOL_REPO   = "github.com/luis"


class WebScanner:
    def __init__(self):
        self.target, self.domain, self.target_ip = "", "", "Detecting..."
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36'
        })
        self.timeout = 10
        self.semaphore = asyncio.Semaphore(20)
        self.scan_results = []
        self.info_results = {
            "subdomains": set(),
            "forms": [],
            "tech": set(),
            "paths": set()
        }
        self.firewall = "Not Detected / Unknown"
        self.server_loc = "Unknown"
        self.base_path = os.path.dirname(os.path.abspath(__file__))

        self.dir_wordlist   = self._load_list_from_file('wordlists/common_dirs.txt')
        self.sub_wordlist   = self._load_list_from_file('wordlists/common_subs.txt')
        self.sqli_payloads  = self._load_list_from_file('payloads/sqli.txt')
        self.xss_payloads   = self._load_list_from_file('payloads/xss.txt')
        self.lfi_payloads   = self._load_list_from_file('payloads/lfi.txt')

    def _load_list_from_file(self, file_path):
        full_path = os.path.join(self.base_path, file_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"{RED}[!] File tidak ditemukan: {full_path}. "
                  f"Beberapa fitur mungkin tidak berfungsi.{RESET}")
            return []

    def _get_sys_info(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
        except Exception:
            ip = "Disconnected"

        if os.path.exists("/system/build.prop"):
            model = subprocess.getoutput("getprop ro.product.model") or "Android"
        else:
            model = platform.node() or "Linux"

        batt = "N/A"
        if subprocess.call("command -v termux-battery-status", shell=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            try:
                batt_raw = subprocess.getoutput("termux-battery-status")
                batt = re.search(r'"percentage":\s*(\d+)', batt_raw).group(1) + "%"
            except Exception:
                pass

        shell_env = os.environ.get("MSYSTEM", "")
        if shell_env:
            env_tag = f"Git Bash ({shell_env})"
        elif os.name == "posix" and "ANDROID_ROOT" in os.environ:
            env_tag = "Termux"
        elif os.name == "nt":
            env_tag = "Windows CMD/PowerShell"
        else:
            env_tag = platform.system()

        return ip, model, batt, env_tag

    def banner(self):
        os.system("clear" if os.name == "posix" else "cls")
        ip_addr, model_dev, battery, env_tag = self._get_sys_info()

        # ── ROSARY / CROSS BANNER (replaces the old skull) ──
        print(f"{YELLOW}{BOLD}              †                ")
        print(f"              |                ")
        print(f"           ___|___             ")
        print(f"              |                ")
        print(f"              |                ")
        print(f"           .-\"\"\"\"-.            ")
        print(f"         .'  o o   '.          ")
        print(f"        /   o o o    \\         ")
        print(f"       |  o o o o o   |        ")
        print(f"       |   o o o o    |        ")
        print(f"        \\   o o o    /         ")
        print(f"         '.  o o  .'           ")
        print(f"           '-...-'             ")
        print(f"              |                ")
        print(f"              |                ")
        print(f"             _|_               ")
        print(f"            (   )              ")
        print(f"{CYAN}        ✝  AVE  MARIA  ✝       {RESET}")
        print(f"{YELLOW}     ─────────────────────     {RESET}")
        print(f"{CYAN}   WELCOME {USER_NAME.upper()} — ROSARY MODE{RESET}")
        print(f"{GREEN}──────────────────────────────────────────────{RESET}")
        print(f"{BLUE}  Tool    : {RED}{TOOL_NAME}{RESET}")
        print(f"{BLUE}  Power   : {GREEN}{TOOL_POWER}{RESET}")
        print(f"{BLUE}  Author  : {RED}{USER_NAME}{RESET}")
        print(f"{BLUE}  Repo    : {YELLOW}{TOOL_REPO}{RESET}")
        print(f"{GREEN}──────────────────────────────────────────────{RESET}")
        print(f"{BLUE}  User    : {RED}{USER_NAME} ({USER_ROLE}){RESET}")
        print(f"{BLUE}  OS      : {GREEN}{model_dev[:20]}{RED} ({battery}){RESET}")
        print(f"{BLUE}  Shell   : {GREEN}{env_tag}{RESET}")
        print(f"{BLUE}  Local IP: {YELLOW}{ip_addr}{RESET}")
        print(f"{BLUE}  Target  : {ORANGE}{self.domain if self.domain else 'Ready'}{RESET}")
        print(f"{BLUE}  TGT IP  : {YELLOW}{self.target_ip}{RESET}")
        print(f"{GREEN}══════════════════════════════════════════════{RESET}")
        print(f"{MAGENTA}  Hello, {USER_NAME}! ({USER_HANDLE}@{env_tag}) — pray & hack ethically.{RESET}")

    # ───────────── helpers ─────────────
    def _add_vuln(self, type, url, severity, details):
        finding = {"type": type, "url": url, "severity": severity, "details": details}
        self.scan_results.append(finding)
        sev_color = {"High": RED, "Medium": ORANGE, "Low": YELLOW}.get(severity, WHITE)
        print(f"    {sev_color}[VULN] {type} | {url} | {details}{RESET}")

    def _add_info(self, type, details):
        finding = {"type": type, "details": details}
        if finding not in self.info_results.get("info_findings", []):
            self.info_results.setdefault("info_findings", []).append(finding)
            print(f"    {BLUE}[INFO] {type} | {details}{RESET}")

    async def _fetch(self, url, params=None, data=None, method='GET'):
        async with self.semaphore:
            try:
                loop = asyncio.get_running_loop()
                if method.upper() == 'POST':
                    return await loop.run_in_executor(
                        None,
                        lambda: self.session.post(url, params=params, data=data,
                                                  timeout=self.timeout,
                                                  verify=False, allow_redirects=True))
                return await loop.run_in_executor(
                    None,
                    lambda: self.session.get(url, params=params,
                                             timeout=self.timeout,
                                             verify=False, allow_redirects=True))
            except requests.exceptions.RequestException:
                return None

    # ───────────── phases ─────────────
    async def get_target_intel(self):
        print(f"\n{YELLOW}[*] PHASE 1: GATHERING TARGET INTELLIGENCE...{RESET}")
        try:
            loc_req = requests.get(f"http://ip-api.com/json/{self.target_ip}", timeout=5).json()
            if loc_req.get('status') == 'success':
                self.server_loc = f"{loc_req.get('city')}, {loc_req.get('country')}"
        except Exception:
            pass

        try:
            r = await self._fetch(self.target)
            if r:
                server = r.headers.get("Server", "Unknown")
                powered = r.headers.get("X-Powered-By", "Unknown")
                self.info_results["tech"].add(f"Server: {server}")
                if powered != "Unknown":
                    self.info_results["tech"].add(f"Language/Framework: {powered}")

                if "wp-content" in r.text:
                    self.info_results["tech"].add("CMS: WordPress")
                if "joomla" in r.text.lower():
                    self.info_results["tech"].add("CMS: Joomla")

                h_str = str(r.headers).lower()
                if "cloudflare" in h_str:   self.firewall = "Cloudflare WAF"
                elif "mod_security" in h_str: self.firewall = "ModSecurity"
                elif "sucuri" in h_str:      self.firewall = "Sucuri CloudProxy"
                elif "akamai" in h_str:      self.firewall = "Akamai WAF"

                self._check_security_headers(r.headers)
        except Exception:
            pass
        print(f"    {GREEN}[INFO] Intelligence gathering complete.{RESET}")

    def _check_security_headers(self, headers):
        print(f"    {CYAN}[TEST] Checking for security headers...{RESET}")
        security_headers = {
            "Strict-Transport-Security": "Enforces HTTPS.",
            "Content-Security-Policy": "Prevents XSS and data injection attacks.",
            "X-Content-Type-Options": "Prevents MIME-sniffing attacks.",
            "X-Frame-Options": "Protects against Clickjacking attacks."
        }
        for header, detail in security_headers.items():
            if header not in headers:
                self._add_info("Missing Security Header",
                               f"Header '{header}' is missing. Recommended to prevent: {detail}")

    async def subdomain_hunter(self):
        print(f"\n{YELLOW}[*] PHASE 2: SUBDOMAIN ENUMERATION...{RESET}")
        base_domain = self.domain.replace("www.", "")

        async def check_sub(s):
            target_sub = f"{s}.{base_domain}"
            try:
                loop = asyncio.get_running_loop()
                ip = await loop.run_in_executor(None, socket.gethostbyname, target_sub)
                self.info_results["subdomains"].add(f"{target_sub} ({ip})")
                print(f"    {GREEN}[SUB] Found: {target_sub} ({ip}){RESET}")
            except socket.gaierror:
                pass

        await asyncio.gather(*[check_sub(s) for s in self.sub_wordlist])
        print(f"    {GREEN}[INFO] Subdomain scan complete.{RESET}")

    async def form_hunter(self, url, html):
        print(f"\n{YELLOW}[*] PHASE 4: ANALYZING FORMS...{RESET}")
        soup = BeautifulSoup(html, "html.parser")
        forms = soup.find_all("form")
        if not forms:
            print(f"    {WHITE}[INFO] No forms found on the main page.{RESET}")
            return

        for i, form in enumerate(forms):
            action_path = form.get("action", "")
            action_url = urljoin(url, action_path)
            method = form.get("method", "GET").upper()
            inputs = []
            is_login = False
            has_csrf = False

            for tag in form.find_all(["input", "textarea", "select"]):
                t_type = tag.get("type", "text")
                name = tag.get("name", "unknown")
                inputs.append(f"{name}({t_type})")
                if t_type == "password": is_login = True
                if "csrf" in name.lower() or "token" in name.lower(): has_csrf = True

            if is_login and method == "GET":
                self._add_vuln("Sensitive Data Exposure", action_url, "Medium",
                               "Login form submits credentials via GET method.")
            if not has_csrf and method == "POST":
                self._add_vuln("Missing CSRF Protection", action_url, "Medium",
                               "Form may be vulnerable to Cross-Site Request Forgery.")

            form_info = f"FORM #{i+1} | {method} -> {action_path} | Inputs: {', '.join(inputs)}"
            self.info_results["forms"].append(form_info)
        print(f"    {GREEN}[INFO] Form analysis complete.{RESET}")

    async def _test_sqli(self, url, params=None, method='GET'):
        print(f"    {CYAN}[TEST] Checking for SQL Injection on {url}{RESET}")
        db_errors = ["sql syntax", "mysql", "unclosed quotation mark", "odbc", "oracle"]
        key = list(params.keys())[0]
        try:
            r_true = await self._fetch(url, params={key: "' OR '1'='1"}, method=method)
            r_false = await self._fetch(url, params={key: "' OR '1'='2"}, method=method)
            if r_true and r_false and len(r_true.text) != len(r_false.text):
                self._add_vuln("SQL Injection (Boolean-based)", url, "High",
                               f"Parameter '{key}' seems vulnerable.")
                return
        except Exception:
            pass

        for payload in self.sqli_payloads:
            test_params = params.copy()
            test_params[key] = payload
            r = await self._fetch(url, params=test_params, method=method)
            if r and any(err in r.text.lower() for err in db_errors):
                self._add_vuln("SQL Injection (Error-based)", url, "High",
                               f"Parameter '{key}' returned a DB error for payload: {payload}")
                break

    async def _test_xss(self, url, params=None, method='GET'):
        print(f"    {CYAN}[TEST] Checking for Reflected XSS on {url}{RESET}")
        key = list(params.keys())[0]
        for payload in self.xss_payloads:
            test_params = params.copy()
            test_params[key] = payload
            r = await self._fetch(url, params=test_params, method=method)
            if r and payload in r.text:
                self._add_vuln("Cross-Site Scripting (Reflected)", url, "Medium",
                               f"Parameter '{key}' reflected payload: {payload}")
                break

    async def _test_lfi(self, url, params=None, method='GET'):
        print(f"    {CYAN}[TEST] Checking for Local File Inclusion on {url}{RESET}")
        lfi_evidence = ["root:x:0:0", "[boot loader]", "java.io.FileNotFoundException"]
        key = list(params.keys())[0]
        for payload in self.lfi_payloads:
            test_params = params.copy()
            test_params[key] = payload
            r = await self._fetch(url, params=test_params, method=method)
            if r and any(e in r.text for e in lfi_evidence):
                self._add_vuln("Local File Inclusion (LFI)", url, "High",
                               f"Parameter '{key}' seems vulnerable with payload: {payload}")
                break

    async def vulnerability_scanner(self, url, html):
        print(f"\n{YELLOW}[*] PHASE 5: ACTIVE VULNERABILITY SCANNING...{RESET}")
        soup = BeautifulSoup(html, "html.parser")
        tasks = []

        for form in soup.find_all("form"):
            action_url = urljoin(url, form.get("action", ""))
            method = form.get("method", "GET").upper()
            for inp in form.find_all("input", {"name": True}):
                if inp.get("type") not in ["submit", "button", "hidden"]:
                    params = {inp.get("name"): "test"}
                    tasks += [self._test_sqli(action_url, params, method),
                              self._test_xss(action_url, params, method),
                              self._test_lfi(action_url, params, method)]

        for link in soup.find_all("a", href=True):
            href = link.get("href")
            if "?" in href:
                full_url = urljoin(url, href)
                parsed_url = urlparse(full_url)
                if parsed_url.netloc == self.domain:
                    for qp in parsed_url.query.split('&'):
                        if "=" in qp:
                            param_name = qp.split("=")[0]
                            params = {param_name: "test"}
                            base = full_url.split('?')[0]
                            tasks += [self._test_sqli(base, params),
                                      self._test_xss(base, params),
                                      self._test_lfi(base, params)]

        if tasks:
            await asyncio.gather(*tasks)
        else:
            print(f"    {WHITE}[INFO] No parameters found to test for SQLi/XSS.{RESET}")

    async def start(self):
        self.banner()
        start_time = time.time()

        self.target = input(f"{CYAN}{USER_NAME}, enter Target URL > {WHITE}").strip()
        if not self.target:
            return
        if not self.target.startswith("http"):
            self.target = "http://" + self.target
        self.domain = urlparse(self.target).netloc

        try:
            loop = asyncio.get_running_loop()
            self.target_ip = await loop.run_in_executor(None, socket.gethostbyname, self.domain)
        except Exception:
            self.target_ip = "Error"

        self.banner()
        await self.get_target_intel()
        await self.subdomain_hunter()

        print(f"\n{YELLOW}[*] PHASE 3: DIRECTORY & FILE BRUTEFORCE...{RESET}")

        async def check_path(p):
            url = f"{self.target.rstrip('/')}/{p}"
            r = await self._fetch(url)
            if r and r.status_code in [200, 403]:
                print(f"    {GREEN}[PATH] Found: {url} (Status: {r.status_code}){RESET}")
                self.info_results["paths"].add(f"{url} [{r.status_code}]")
                if any(k in p for k in ['.env', '.git', '.bak', '.sql', '.zip']):
                    self._add_vuln("Sensitive File Exposure", url, "High",
                                   f"Potentially sensitive file found: {p}")

        await asyncio.gather(*[check_path(p) for p in self.dir_wordlist])

        r = await self._fetch(self.target)
        if r:
            await self.form_hunter(self.target, r.text)
            await self.vulnerability_scanner(self.target, r.text)

        scan_duration = time.time() - start_time

        print(f"\n{GREEN}══════════════ {USER_NAME.upper()}'S FINAL REPORT ══════════════{RESET}")
        print(f" {BLUE}TARGET IP   : {YELLOW}{self.target_ip}{RESET}")
        print(f" {BLUE}SERVER LOC  : {WHITE}{self.server_loc}{RESET}")
        print(f" {BLUE}FIREWALL    : {RED}{self.firewall}{RESET}")

        if self.info_results["tech"]:
            print(f"\n {CYAN}[WEB TECHNOLOGIES DETECTED]{RESET}")
            for tech in sorted(self.info_results["tech"]):
                print(f"  {WHITE}» {tech}{RESET}")

        if self.scan_results:
            print(f"\n {RED}[VULNERABILITIES SUMMARY]{RESET}")
            severities = {"High": [], "Medium": [], "Low": []}
            for vuln in self.scan_results:
                severities.get(vuln["severity"], []).append(vuln)

            for sev, color in [("High", RED), ("Medium", ORANGE), ("Low", YELLOW)]:
                if severities[sev]:
                    print(f"  {color}--- {sev.upper()} RISK ---{RESET}")
                    for v in severities[sev]:
                        print(f"    {color}» [{v['type']}] {v['url']}{RESET}\n      Details: {v['details']}")
        else:
            print(f"\n  {GREEN}[INFO] No critical vulnerabilities detected based on this scan.{RESET}")

        print(f"\n {CYAN}[ADDITIONAL INFORMATION]{RESET}")
        if self.info_results["subdomains"]:
            print(f"  {WHITE}--- Found Subdomains ---{RESET}")
            for s in sorted(self.info_results["subdomains"]):
                print(f"    » {s}")
        if self.info_results["paths"]:
            print(f"  {WHITE}--- Found Paths ---{RESET}")
            for p in sorted(self.info_results["paths"]):
                print(f"    » {p}")
        if self.info_results.get("info_findings"):
            print(f"  {WHITE}--- Informational Findings ---{RESET}")
            for i in self.info_results["info_findings"]:
                print(f"    {BLUE}» [{i['type']}] {i['details']}{RESET}")

        print(f"\n{GREEN}═════════════════════════════════════════════════════════{RESET}")
        print(f"{CYAN}Scan completed in {scan_duration:.2f} seconds. Nice work, {USER_NAME}.{RESET}")

        self._generate_html_report(scan_duration)

    def _generate_html_report(self, scan_duration):
        report_name = f"report_{self.domain}_{USER_HANDLE}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

        html_style = """
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1a1a1a; color: #e0e0e0; margin: 20px; }
            h1, h2, h3 { color: #e8491d; border-bottom: 2px solid #e8491d; padding-bottom: 5px; }
            .container { background-color: #2c2c2c; padding: 20px; border-radius: 8px; box-shadow: 0 0 15px rgba(0,0,0,0.5); }
            .summary-grid { display: grid; grid-template-columns: 150px 1fr; gap: 5px 15px; margin-bottom: 20px; }
            .summary-grid strong { color: #50a3a2; }
            .vuln-card { border: 1px solid #444; border-left: 5px solid; border-radius: 5px; margin-bottom: 15px; padding: 15px; background-color: #333; }
            .vuln-card.high { border-left-color: #e74c3c; }
            .vuln-card.medium { border-left-color: #f39c12; }
            .vuln-card.low { border-left-color: #f1c40f; }
            .vuln-card h3 { margin-top: 0; color: #e0e0e0; border: none; }
            .vuln-details { margin-top: 10px; }
            .info-list { list-style: none; padding-left: 0; }
            .info-list li { background-color: #333; padding: 8px; border-radius: 4px; margin-bottom: 5px; }
            code { background-color: #111; color: #f1c40f; padding: 2px 5px; border-radius: 3px; }
            footer { text-align: center; margin-top: 30px; font-size: 0.9em; color: #888; }
        </style>
        """

        html_content = (f"<!DOCTYPE html><html><head><title>{USER_NAME}'s Web Scanner Report: "
                        f"{self.domain}</title>{html_style}</head><body>")
        html_content += f"<div class='container'><h1>{USER_NAME}'s Web Scanner Report</h1>"

        html_content += "<h2>Scan Summary</h2><div class='summary-grid'>"
        html_content += f"<strong>Owner:</strong><div>{USER_NAME} ({USER_HANDLE})</div>"
        html_content += f"<strong>Target:</strong><div>{self.target}</div>"
        html_content += f"<strong>IP Address:</strong><div>{self.target_ip}</div>"
        html_content += f"<strong>Server Location:</strong><div>{self.server_loc}</div>"
        html_content += f"<strong>WAF Detected:</strong><div>{self.firewall}</div>"
        html_content += f"<strong>Scan Date:</strong><div>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>"
        html_content += f"<strong>Scan Duration:</strong><div>{scan_duration:.2f} seconds</div>"
        html_content += "</div>"

        html_content += "<h2>Vulnerabilities Found</h2>"
        if self.scan_results:
            severities = {"High": [], "Medium": [], "Low": []}
            for vuln in self.scan_results:
                severities.get(vuln["severity"], []).append(vuln)
            for sev, vulns in severities.items():
                for v in vulns:
                    html_content += f"<div class='vuln-card {sev.lower()}'>"
                    html_content += f"<h3>[{sev.upper()}] {v['type']}</h3>"
                    html_content += f"<div class='vuln-details'><strong>URL:</strong> <code>{v['url']}</code><br>"
                    html_content += f"<strong>Details:</strong> {v['details']}</div></div>"
        else:
            html_content += "<p>No vulnerabilities found in this scan.</p>"

        html_content += "<h2>Additional Information</h2>"
        info_sections = {
            "Web Technologies": self.info_results["tech"],
            "Informational Findings": [f"<strong>{i['type']}:</strong> {i['details']}"
                                       for i in self.info_results.get("info_findings", [])],
            "Found Subdomains": self.info_results["subdomains"],
            "Found Sensitive Paths": self.info_results["paths"],
            "Found Forms": self.info_results["forms"]
        }
        for title, items in info_sections.items():
            if items:
                html_content += f"<h3>{title}</h3><ul class='info-list'>"
                for item in sorted(list(items)):
                    html_content += f"<li>{item}</li>"
                html_content += "</ul>"

        html_content += f"<footer>Report generated by {USER_NAME} ({USER_HANDLE}) — {TOOL_NAME}</footer>"
        html_content += "</div></body></html>"

        try:
            with open(report_name, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"\n{GREEN}[SUCCESS] {USER_NAME}, your HTML report is saved to: {report_name}{RESET}")
        except Exception as e:
            print(f"\n{RED}[ERROR] Could not save HTML report: {e}{RESET}")


if __name__ == "__main__":
    try:
        scanner = WebScanner()
        asyncio.run(scanner.start())
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Aborted by {USER_NAME}.{RESET}")
    except Exception as e:
        print(f"\n{RED}[ERROR] {e}{RESET}")