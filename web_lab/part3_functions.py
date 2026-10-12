# Laboratorul 4 - Partea 3: Functii proprii (exercitiile 21-34)
# Student: Daniel Perjesco

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


# EXERCITIUL 21: prima versiune
# La exercitiul 23 o redefinim pentru a adauga un parametru implicit.
def fetch(url):
    """Returneaza obiectul de raspuns HTTP."""
    time.sleep(1)
    return requests.get(url, timeout=TIMEOUT)


# EXERCITIUL 22
def get_status(url):
    """Returneaza codul de stare HTTP pentru URL."""
    return fetch(url).status_code


# EXERCITIUL 23: versiunea finala a lui fetch()
def fetch(url, timeout=10):
    """Returneaza raspunsul HTTP; timeout este optional."""
    time.sleep(1)
    return requests.get(url, timeout=timeout)


# EXERCITIUL 24
def get_title(html):
    """Returneaza textul dintre <title> si </title>, daca exista."""
    begin = html.find("<title>")
    end = html.find("</title>")
    if begin == -1 or end == -1 or end < begin:
        return ""
    begin += len("<title>")
    return html[begin:end].strip()


# EXERCITIUL 26: adaugam type hints (redefinim get_status)
def get_status(url: str) -> int:
    """Returneaza codul HTTP; adnotarile nu sunt validari runtime."""
    return fetch(url).status_code


# EXERCITIUL 27
def page_exists(url):
    """Returneaza bool: raspuns sub 400 sau False la eroare de cerere."""
    try:
        return fetch(url).status_code < 400
    except requests.RequestException:
        return False


# EXERCITIUL 28
def check_paths(base, paths):
    """Returneaza un dictionar {path: cod}, None daca reteaua esueaza."""
    results = {}
    for path in paths:
        try:
            results[path] = get_status(base.rstrip("/") + path)
        except requests.RequestException:
            results[path] = None
    return results


# EXERCITIUL 29
def get_header(url, name, default="lipseste"):
    """Returneaza valoarea unui antet HTTP sau valoarea implicita."""
    return fetch(url).headers.get(name, default)


# EXERCITIUL 30
def security_headers(url):
    """Verifica prezenta a cinci antete de securitate HTTP."""
    names = [
        "Strict-Transport-Security", "Content-Security-Policy",
        "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy",
    ]
    response = fetch(url)
    return {name: name in response.headers for name in names}


# EXERCITIUL 31
def score_headers(results):
    """Returneaza scorul de prezenta a antetelor, ca '3/5'."""
    return f"{sum(results.values())}/{len(results)}"


# EXERCITIUL 32
def fetch_robots(base):
    """Returneaza textul robots.txt sau None la HTTP/eroare de retea."""
    try:
        response = fetch(base.rstrip("/") + "/robots.txt")
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def disallowed_paths(robots_text):
    """Colecteaza valorile tuturor liniilor Disallow: din robots.txt."""
    if robots_text is None:
        return []
    values = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            values.append(line.split(":", 1)[1].strip())
    return values


# EXERCITIUL 33
def response_times(*urls):
    """Masurarea duratelor GET; None inseamna eroare de retea."""
    values = {}
    for url in urls:
        time.sleep(1)
        start = time.perf_counter()
        try:
            requests.get(url, timeout=TIMEOUT)
            values[url] = time.perf_counter() - start
        except requests.RequestException:
            values[url] = None
    return values


# EXERCITIUL 34
def log(message, **details):
    """Afiseaza un mesaj si detaliile date ca argumente cu nume."""
    parts = [message]
    for key, value in details.items():
        parts.append(f"{key}={value}")
    print(" | ".join(parts))


def test(nr, functie):
    """Ruleaza un exercitiu fara a opri restul la o eroare de retea."""
    print(f"\n=== EXERCITIUL {nr} ===")
    try:
        functie()
    except requests.RequestException as eroare:
        print("Cererea HTTP a esuat:", eroare)
    except Exception as eroare:
        print("Eroare:", type(eroare).__name__, eroare)


if __name__ == "__main__":
    test(21, lambda: print("Cod:", fetch(BASE_URL).status_code))
    test(22, lambda: [print(p, get_status(BASE_URL + p))
                      for p in ["/", "/robots.txt", "/sitemap.xml"]])
    test(23, lambda: (print("implicit:", fetch(BASE_URL).status_code),
                      print("timeout=3:", fetch(BASE_URL, timeout=3).status_code)))
    test(24, lambda: print(get_title(fetch(BASE_URL).text)))
    test(25, lambda: help(get_title))
    # Adnotarile nu opresc apelul: biblioteca raporteaza URL invalid.
    test(26, lambda: print(get_status(123)))
    test(27, lambda: (print(page_exists(BASE_URL)),
                      print(page_exists("https://this-domain-does-not-exist.invalid"))))
    test(28, lambda: print(check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"])))
    test(29, lambda: print(get_header(BASE_URL, name="Server")))
    test(30, lambda: print(security_headers(BASE_URL)))
    test(31, lambda: print(score_headers(security_headers(BASE_URL))))
    test(32, lambda: print(disallowed_paths(fetch_robots(BASE_URL))))
    test(33, lambda: print(response_times(BASE_URL, BASE_URL + "/robots.txt")))
    test(34, lambda: log("verificat", url=BASE_URL, status=200))
    # print afiseaza; return pune valoarea la dispozitia apelantului.
