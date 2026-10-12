# Laboratorul 4 - Partea 2: Metode si atribute (exercitiile 9-20)
# Student: Daniel Perjesco

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


def get_page(url, method="GET"):
    """Trimite doar GET/HEAD si pastreaza o pauza intre cereri."""
    time.sleep(1)
    try:
        if method == "HEAD":
            return requests.head(url, timeout=TIMEOUT)
        return requests.get(url, timeout=TIMEOUT)
    except requests.RequestException as eroare:
        print("Eroare de retea:", eroare)
        return None


def exercitiul_9(response):
    """Afiseaza atributele raspunsului."""
    if response is None:
        return
    print("status_code:", response.status_code)  # atribut
    print("ok:", response.ok)                  # atribut
    print("url:", response.url)                # atribut
    print("encoding:", response.encoding)      # atribut


def exercitiul_10():
    """Verifica raspunsul si trateaza eroarea HTTP."""
    home = get_page(BASE_URL)
    if home is not None:
        try:
            home.raise_for_status()
            print("Pagina principala nu a raportat eroare HTTP.")
        except requests.HTTPError as eroare:
            print("Eroare HTTP pentru pagina principala:", eroare)
    bad = get_page(BASE_URL + "/this-page-does-not-exist")
    if bad is not None:
        try:
            bad.raise_for_status()
            print("Cod pentru pagina test:", bad.status_code)
        except requests.HTTPError as eroare:
            print("Pagina test a returnat eroare HTTP:", eroare)


def exercitiul_11(response):
    """Listeaza antetele."""
    if response is None:
        return
    for nume, valoare in response.headers.items():
        print(f"{nume}: {valoare}")


def exercitiul_12(response):
    """Citeste antete prin get()."""
    if response is None:
        return
    print("Server:", response.headers.get("Server", "lipseste"))
    print("Content-Type:", response.headers.get("Content-Type", "lipseste"))
    print("content-type:", response.headers.get("content-type", "lipseste"))
    # response.headers nu diferentiaza majusculele in numele antetelor.


def exercitiul_13(response):
    """Numara sub-sirul cyber."""
    if response is None:
        return
    print("cyber apare de", response.text.lower().count("cyber"), "ori")
    # lower() returneaza str, pe care apelam direct count().


def exercitiul_14(response):
    """Extrage titlul cu find() si slicing."""
    if response is None:
        return
    html = response.text
    open_at = html.find("<title>")
    close_at = html.find("</title>")
    if open_at == -1 or close_at == -1 or close_at < open_at:
        print("Titlul nu a fost gasit (posibil raspuns de eroare).")
        return
    start = open_at + len("<title>")
    print("Titlul:", html[start:close_at].strip())


def exercitiul_15(response):
    """Numara liniile si pe cea mai lunga."""
    if response is None:
        return
    lines = response.text.splitlines()
    print("Numar linii:", len(lines))
    print("Cea mai lunga:", len(max(lines, key=len)) if lines else 0)


def exercitiul_16(response):
    """Verifica schema URL final."""
    if response is None:
        return
    print("Conexiune securizata" if response.url.startswith("https://")
          else "Conexiune nesecurizata")


def exercitiul_17():
    """Inspecteaza redirectionarile de la http://."""
    response = get_page("http://cybercor.org")
    if response is None:
        return
    for redirect in response.history:
        print(redirect.status_code, redirect.url)
    print("URL final:", response.url)


def exercitiul_18():
    """Compara dimensiunile corpului HEAD si GET."""
    head = get_page(BASE_URL, method="HEAD")
    get = get_page(BASE_URL)
    if head is not None and get is not None:
        print("HEAD (octeti):", len(head.content))
        print("GET  (octeti):", len(get.content))
    # HEAD are antete, dar fara corp; GET poate include corpul.


def exercitiul_19(response):
    """Afiseaza numele si Secure pentru cookie-uri."""
    if response is None:
        return
    if not response.cookies:
        print("Niciun cookie setat")
    else:
        for cookie in response.cookies:
            print("Nume:", cookie.name, "Secure:", cookie.secure)


def exercitiul_20():
    """Trimite User-Agent personalizat doar spre httpbin."""
    with requests.Session() as session:
        session.headers.update({"User-Agent": "WebLab-Student"})
        time.sleep(1)
        try:
            resp = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
            resp.raise_for_status()
            date = resp.json()
            print("Antete returnate:", date)
            print("User-Agent receptionat:", date.get("headers", {}).get("User-Agent"))
        except (requests.RequestException, ValueError) as eroare:
            print("Nu am putut confirma antetul:", eroare)


if __name__ == "__main__":
    response = get_page(BASE_URL)
    exercitii = [
        (9, lambda: exercitiul_9(response)), (10, exercitiul_10),
        (11, lambda: exercitiul_11(response)),
        (12, lambda: exercitiul_12(response)),
        (13, lambda: exercitiul_13(response)),
        (14, lambda: exercitiul_14(response)),
        (15, lambda: exercitiul_15(response)),
        (16, lambda: exercitiul_16(response)),
        (17, exercitiul_17), (18, exercitiul_18),
        (19, lambda: exercitiul_19(response)), (20, exercitiul_20),
    ]
    for nr, ex in exercitii:
        print(f"\n=== EXERCITIUL {nr} ===")
        ex()
    # text este atribut str; json() este metoda care interpreteaza JSON.
