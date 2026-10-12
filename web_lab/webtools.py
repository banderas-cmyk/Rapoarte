# Laboratorul 4 - Partea 5: Modul reutilizabil (exercitiile 44-50)
# Student: Daniel Perjesco

import json
import re
import socket
import ssl
import time
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# EXERCITIUL 47
DEFAULT_HEADERS = {"User-Agent": "WebLab-Student"}

# EXERCITIUL 44 + EXERCITIUL 47
def fetch(url, timeout=TIMEOUT):
    """Efectueaza GET cu timeout si antetele cerute in laborator."""
    time.sleep(1)
    return requests.get(url, timeout=timeout, headers=DEFAULT_HEADERS)


# EXERCITIUL 44
def get_status(url):
    """Returneaza codul HTTP al raspunsului."""
    return fetch(url).status_code


# EXERCITIUL 44
def get_title(html):
    """Extrage textul din <title>, daca eticheta exista."""
    start = html.find("<title>")
    end = html.find("</title>")
    if start == -1 or end == -1 or end < start:
        return ""
    return html[start + len("<title>"):end].strip()


# EXERCITIUL 44
def security_headers(url):
    """Returneaza prezenta a cinci antete de securitate."""
    response = fetch(url)
    names = [
        "Strict-Transport-Security", "Content-Security-Policy",
        "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy",
    ]
    return {name: name in response.headers for name in names}


# EXERCITIUL 49
def check_paths(base, paths):
    """Verifica cele trei cai permise; None marcheaza eroarea de retea."""
    results = {}
    for path in paths:
        try:
            results[path] = get_status(base.rstrip("/") + path)
        except requests.RequestException:
            results[path] = None
    return results


# EXERCITIUL 50 - functii ajutatoare reutilizate
def score_headers(results):
    """Returneaza scorul 'numar_prezente/numar_total'."""
    return f"{sum(results.values())}/{len(results)}"


def fetch_robots(base):
    """Returneaza robots.txt sau None pentru HTTP>=400/eroare retea."""
    try:
        response = fetch(base.rstrip("/") + "/robots.txt")
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def disallowed_paths(robots_text):
    """Extrage valorile liniilor Disallow din robots.txt."""
    if robots_text is None:
        return []
    paths = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            paths.append(line.split(":", 1)[1].strip())
    return paths


def resolve(hostname):
    """Rezolva un domeniu in IPv4."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname):
    """Numara zilele intregi ramase pana la expirarea certificatului TLS."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as tls:
            certificate = tls.getpeercert()
    expiry_ts = ssl.cert_time_to_seconds(certificate["notAfter"])
    expiry = datetime.fromtimestamp(expiry_ts, tz=timezone.utc)
    return (expiry - datetime.now(timezone.utc)).days


def extract_links(html):
    """Extrage href-urile intre ghilimele duble, fara duplicate."""
    return list(dict.fromkeys(re.findall(r'href="([^"]+)"', html)))


def split_links(links, domain):
    """Returneaza (interne, externe) prin compararea domeniului."""
    internal, external = [], []
    base = "https://" + domain + "/"
    for link in links:
        full = urljoin(base, link)
        if urlparse(full).netloc.lower() == domain.lower():
            internal.append(full)
        else:
            external.append(full)
    return internal, external


# EXERCITIUL 50 - proiect final
def site_report(url):
    """Afiseaza si salveaza raportul chiar daca unele verificari esueaza."""
    parsed = urlparse(url)
    hostname = parsed.hostname
    if (hostname != "cybercor.org" or parsed.scheme != "https"
            or parsed.path not in ("", "/") or parsed.query or parsed.fragment):
        raise ValueError("Laboratorul permite doar URL-ul https://cybercor.org")

    report = {
        "requested_url": url,
        "status": None, "final_url": None, "title": None,
        "ip": None, "redirects": [], "security_score": None,
        "certificate_days_left": None, "internal_links": 0,
        "external_links": 0, "disallowed_paths": [], "errors": [],
    }
    html = None
    try:
        response = fetch(url)
        report["status"] = response.status_code
        report["final_url"] = response.url
        if response.status_code < 400:
            html = response.text
            report["title"] = get_title(html)
        else:
            report["errors"].append(f"Pagina a raspuns cu HTTP {response.status_code}; nu analizam pagina de eroare ca HTML normal.")
    except requests.RequestException as err:
        report["errors"].append("Cerere pagina principala: " + str(err))

    try:
        report["ip"] = resolve(hostname)
    except OSError as err:
        report["errors"].append("DNS: " + str(err))

    try:
        # Cerinta: verificam lantul care incepe de la HTTP simplu.
        time.sleep(1)
        r = requests.get("http://" + hostname, timeout=TIMEOUT, headers=DEFAULT_HEADERS)
        report["redirects"] = [
            {"status": item.status_code, "url": item.url} for item in r.history
        ]
        report["http_final_url"] = r.url
    except requests.RequestException as err:
        report["errors"].append("Redirectionari: " + str(err))

    try:
        results = security_headers(url)
        report["security_score"] = score_headers(results)
    except requests.RequestException as err:
        report["errors"].append("Antete: " + str(err))

    try:
        report["certificate_days_left"] = cert_days_left(hostname)
    except (OSError, ssl.SSLError, ValueError, KeyError) as err:
        report["errors"].append("Certificat TLS: " + str(err))

    if html is not None:
        links = extract_links(html)
        internal, external = split_links(links, hostname)
        report["internal_links"] = len(internal)
        report["external_links"] = len(external)

    report["disallowed_paths"] = disallowed_paths(fetch_robots(url))

    print(f"=== Raport site: {url} ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    with open("report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)
    print("Salvat in report.json")
    return report


# EXERCITIUL 46 - bloc principal
if __name__ == "__main__":
    try:
        print("Autotest:", get_status(BASE_URL))
    except requests.RequestException as err:
        print("Autotest indisponibil:", err)
