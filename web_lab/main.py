# Laboratorul 4 - Partea 5: Program principal (exercitiile 44-50)
# Student: Daniel Perjesco

# EXERCITIUL 44
import webtools

# EXERCITIUL 45
from webtools import get_title, security_headers
# Daca am defini ulterior aici alta functie get_title,
# numele importat ar fi acoperit de functia locala.

# EXERCITIUL 47
from webtools import DEFAULT_HEADERS

# EXERCITIUL 48
import argparse

# EXERCITIUL 49
import csv
from datetime import datetime
from urllib.parse import urlparse
import requests


def save_csv(url):
    """Creeaza report.csv cu path, status si checked_at."""
    paths = ["/", "/robots.txt", "/sitemap.xml"]
    results = webtools.check_paths(url, paths)
    with open("report.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["path", "status", "checked_at"])
        for path, status in results.items():
            writer.writerow([path, status if status is not None else "eroare",
                             datetime.now().isoformat()])
    print("Salvat in report.csv")


def main():
    """Citeste URL-ul, scrie CSV si genereaza raportul JSON."""
    parser = argparse.ArgumentParser(description="L4 - Analiza site cybercor.org")
    parser.add_argument("url", help="URL-ul cerut (https://cybercor.org)")
    args = parser.parse_args()
    url = args.url
    parsed = urlparse(url)
    if (parsed.scheme != "https" or parsed.hostname != "cybercor.org"
            or parsed.path not in ("", "/") or parsed.query or parsed.fragment):
        parser.error("Exercitiile laboratorului sunt limitate la https://cybercor.org")

    print("DEFAULT_HEADERS:", DEFAULT_HEADERS)
    # Ex. 44 - apel explicit al modulului propriu.
    try:
        response = webtools.fetch(url)
        if response.status_code < 400:
            print("Titlu (ex. 44):", webtools.get_title(response.text))
            print("Titlu (ex. 45):", get_title(response.text))
        else:
            print("Pagina a returnat HTTP", response.status_code,
                  "; titlul ei nu poate fi presupus.")
    except requests.RequestException as err:
        print("Titlul nu este disponibil:", err)

    # Ex. 45 - import direct al functiei security_headers.
    try:
        print("Antete de securitate:", security_headers(url))
    except requests.RequestException as err:
        print("Antetele nu sunt disponibile:", err)

    save_csv(url)       # Ex. 49
    webtools.site_report(url)  # Ex. 50


if __name__ == "__main__":
    main()
