from urllib.parse import urlsplit

from checker import (SITES, build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check,)


def main():
    # Extragem gazda și calea din SITES, fără alte adrese scrise în cod.
    page = urlsplit(SITES[1])

    print("\nPartea 1: Funcții ajutătoare")
    print("build_url, cale fără /:", build_url(page.netloc, page.path.lstrip("/")))
    print("build_url, cale cu /:", build_url(page.netloc, page.path))
    print("is_https, HTTPS:", is_https(SITES[0]))
    print("is_https, HTTP:", is_https(SITES[9]))

    print("\n Partea 2: Trimiterea unei cereri")
    print("show_response, pagină obișnuită:", SITES[0])
    show_response(SITES[0])
    print("show_response, site inexistent:", SITES[9])
    show_response(SITES[9])

    print("\n Partea 3: Verificarea fiecărei adrese")
    for url in SITES:
        print("check_site:", url, "->", check_site(url))

    print("\n Partea 4: Scanare și rezumat")
    scan_sites()

    print("\n Partea 5: Antete de securitate")
    for index in (0, 10, 11, 9):
        url = SITES[index]
        print("check_headers:", url, "->", check_headers(url))

    print("\nPartea 6: Încercări repetate")
    for index in (3, 6, 7, 9, 12):
        url = SITES[index]
        print("retry_check, maximum 3 încercări:", url, "->", retry_check(url))
    print("retry_check, maximum 2 încercări:", SITES[7], "->", retry_check(SITES[7], attempts=2))


if __name__ == "__main__":
    main()
