# Laboratorul 4 - Partea 4: Module standard (exercitiile 35-43)
# Student: Daniel Perjesco

import re
import hashlib
import json
import socket
import ssl
import time
import requests
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser
from datetime import datetime, timezone

BASE_URL = "https://cybercor.org"
TIMEOUT = 10


def fetch(url):
    """Efectueaza cererea GET doar pentru resursele laboratorului."""
    time.sleep(1)
    return requests.get(url, timeout=TIMEOUT)


# EXERCITIUL 35
def descompune_url(url):
    """Afiseaza componentele unui URL fara conexiune de retea."""
    parsed = urlparse(url)
    print("scheme:", parsed.scheme)
    print("netloc:", parsed.netloc)
    print("path:", parsed.path)
    print("query:", parsed.query)
    print("fragment:", parsed.fragment)


# EXERCITIUL 36
def completeaza_url(base, links):
    """Returneaza URL-uri absolute construite din referinte relative."""
    return [urljoin(base, link) for link in links]


# EXERCITIUL 37
def extract_links(html):
    """Extrage href-urile cu ghilimele duble, fara duplicate."""
    return list(dict.fromkeys(re.findall(r'href="([^"]+)"', html)))


# EXERCITIUL 38
def split_links(links, domain):
    """Separa linkurile cu netloc identic de celelalte legaturi."""
    internal, external = [], []
    base = "https://" + domain + "/"
    for link in links:
        full = urljoin(base, link)
        if urlparse(full).netloc.lower() == domain.lower():
            internal.append(full)
        else:
            external.append(full)
    return internal, external


# EXERCITIUL 39
class ImageFinder(HTMLParser):
    """Colecteaza src pentru elementele HTML img."""

    def __init__(self):
        """Initializeaza parserul si lista rezultatelor."""
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Proceseaza etichetele deschise identificate de parser."""
        if tag == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)


def test_image_finder():
    """Verifica parserul pe un HTML cunoscut inaintea paginii reale."""
    test_html = """<html><body>
    <img src="/logo.png" alt="Logo">
    <IMG SRC="poza.jpg">
    <img alt="imagine fara src">
    <img src="https://cdn.example.com/banner.webp" />
    <a href="/despre">Aceasta nu este o imagine</a>
    </body></html>"""
    finder = ImageFinder()
    finder.feed(test_html)
    print("Imagini test:", finder.images)
    assert finder.images == [
        "/logo.png", "poza.jpg", "https://cdn.example.com/banner.webp"
    ], "Parserul nu a gasit exact imaginile asteptate"
    print("Testul a trecut!")


# EXERCITIUL 40
def page_fingerprint(url):
    """Returneaza hash-ul SHA-256 al corpului paginii (nu al unei erori 403)."""
    response = fetch(url)
    response.raise_for_status()
    return hashlib.sha256(response.content).hexdigest()


# EXERCITIUL 41
def save_headers(url, filename="headers.json"):
    """Salveaza antetele in JSON si le citeste inapoi."""
    response = fetch(url)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(dict(response.headers), file, indent=2, ensure_ascii=False)
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    print("Content-Type:", data.get("Content-Type", "lipseste"))
    if response.status_code >= 400:
        print("Atentie: antetele provin dintr-un raspuns HTTP", response.status_code)


# EXERCITIUL 42
def resolve(hostname):
    """Returneaza o adresa IPv4 obtinuta prin DNS."""
    return socket.gethostbyname(hostname)


# EXERCITIUL 43
def cert_days_left(hostname):
    """Returneaza zilele intregi pana la expirarea certificatului TLS."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
            cert = secure_sock.getpeercert()
    expires = ssl.cert_time_to_seconds(cert["notAfter"])
    expires_at = datetime.fromtimestamp(expires, tz=timezone.utc)
    return (expires_at - datetime.now(timezone.utc)).days


def run(nr, fn):
    """Continua laboratorul si daca o verificare esueaza."""
    print(f"\n=== EXERCITIUL {nr} ===")
    try:
        fn()
    except (requests.RequestException, socket.error, ssl.SSLError, OSError, ValueError) as eroare:
        print("Verificarea nu s-a putut finaliza:", eroare)


if __name__ == "__main__":
    run(35, lambda: descompune_url("https://cybercor.org/path?x=1#top"))
    run(36, lambda: print(completeaza_url(BASE_URL,
                                         ["/about", "contact.html", "../index.html"])))
    run(37, lambda: print(extract_links(fetch(BASE_URL).text)))
    run(38, lambda: print(split_links(extract_links(fetch(BASE_URL).text),
                                      "cybercor.org")))
    def run_39():
        """Testeaza parserul pe text si apoi pe pagina reala."""
        test_image_finder()
        response = fetch(BASE_URL)
        finder = ImageFinder()
        finder.feed(response.text)
        print(len(finder.images), "imagini gasite")
        for src in finder.images:
            print(src)
        print("Tag-uri <img (estimare):", response.text.lower().count("<img"))
    run(39, run_39)
    def run_40():
        """Compara doua amprente SHA-256."""
        a = page_fingerprint(BASE_URL)
        b = page_fingerprint(BASE_URL)
        print("Prima:", a, "\nA doua:", b, "\nIdentice:", a == b)
    run(40, run_40)
    run(41, lambda: save_headers(BASE_URL))
    run(42, lambda: print("IP:", resolve("cybercor.org")))
    run(43, lambda: print("Zile pana la expirare:", cert_days_left("cybercor.org")))
    # handle_starttag este apelata de HTMLParser.feed(), nu direct de noi.
