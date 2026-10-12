# Laboratorul 4 - Partea 1: Importuri (exercitiile 1-8)
# Student: Daniel Perjesco

import time
import urllib.request
import urllib.error
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


def exercitiul_1():
    """Verifica versiunea si diferentele de import."""
    print("Versiunea requests:", requests.__version__)
    # requests este instalata separat (pip); urllib.request este standard.


def exercitiul_2():
    """Compara doua stiluri de import."""
    from requests import get
    # 'import requests' arata clar originea functiei.
    # 'from requests import get' permite apelul direct, mai scurt.
    time.sleep(1)
    a = requests.get(BASE_URL, timeout=TIMEOUT)
    print("requests.get:", a.status_code)
    time.sleep(1)
    b = get(BASE_URL, timeout=TIMEOUT)
    print("get:", b.status_code)


def exercitiul_3():
    """Foloseste un alias."""
    import requests as rq
    # Alias-urile standard, clare, sporesc lizibilitatea.
    # Alias-urile arbitrare pot face codul mai greu de citit.
    time.sleep(1)
    raspuns = rq.get(BASE_URL, timeout=TIMEOUT)
    print("rq.get:", raspuns.status_code)


def exercitiul_4():
    """Citeste pagina cu urllib.request (fara requests)."""
    time.sleep(1)
    try:
        with urllib.request.urlopen(BASE_URL, timeout=TIMEOUT) as raspuns:
            print("Status urllib:", raspuns.status)
            html = raspuns.read().decode("utf-8", errors="replace")
            print("Primele 200 caractere:", html[:200])
    except urllib.error.HTTPError as eroare:
        # De exemplu 403: raspunsul este o pagina de eroare, nu pagina dorita.
        print("Status urllib:", eroare.code, "-", eroare.reason)
        print("Serverul a refuzat cererea; nu afisam eroarea ca pagina principala.")
    except urllib.error.URLError as eroare:
        print("Eroare de conexiune/SSL urllib:", eroare.reason)


def exercitiul_5():
    """Exploreaza numele din modul."""
    print(dir(requests))
    # get = functie; Session = clasa; exceptions = modul.


def exercitiul_6():
    """Consulta documentatia si seteaza timeout."""
    help(requests.get)
    # timeout este transmis prin kwargs catre cererea HTTP.
    time.sleep(1)
    raspuns = requests.get(BASE_URL, timeout=TIMEOUT)
    print("Cerere cu timeout:", raspuns.status_code)


def exercitiul_7():
    """Compara timpul total si response.elapsed."""
    time.sleep(1)
    start = time.perf_counter()
    raspuns = requests.get(BASE_URL, timeout=TIMEOUT)
    end = time.perf_counter()
    print("perf_counter:", round(end - start, 4), "secunde")
    print("response.elapsed:", raspuns.elapsed.total_seconds(), "secunde")


def exercitiul_8():
    """Trateaza un modul lipsa."""
    try:
        import bs4  
        print("bs4 este instalat.")
    except ImportError:
        print("Instalati modulul cu: pip install beautifulsoup4")
    # Modul = unitate importabila; pachet = organizare de module;
    # biblioteca = colectie de functionalitati reutilizabile.


if __name__ == "__main__":
    exercitii = [ exercitiul_1, exercitiul_2, exercitiul_3, exercitiul_4,exercitiul_5, exercitiul_6, exercitiul_7, exercitiul_8,]
    for numar, exercitiu in enumerate(exercitii, 1):
        print(f"\n=== EXERCITIUL {numar} ===")
        try:
            exercitiu()
        except requests.RequestException as eroare:
            print("Cererea requests nu a putut fi finalizata:", eroare)
        except Exception as eroare:
            print("Eroare in exercitiu:", type(eroare).__name__, eroare)
