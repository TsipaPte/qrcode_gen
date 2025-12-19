"""Модуль, проверяющий корректность работы программы"""

from functions import detect_text_type

# URL Happy Tests + Немного протоколов

assert detect_text_type("subdomain.google.com") == "https://subdomain.google.com"
assert detect_text_type("google.com") == "https://google.com"
assert detect_text_type("mail.extend.google.com") == "https://mail.extend.google.com"
assert detect_text_type("https://subdomain.google.com") == "https://subdomain.google.com"
assert detect_text_type("https://google.com") == "https://google.com"
assert detect_text_type("https://mail.extend.google.com") == "https://mail.extend.google.com"
assert detect_text_type("site.ru") == "https://site.ru"

# URL Sad Tests

assert detect_text_type("subdomain.google..com") != "https://subdomain.google..com"
assert detect_text_type("google.") != "https://google."
assert detect_text_type("com") != "https://com"
assert detect_text_type("ill$egal.domain") != "https://ill$egal.domain"

# URL | Данные после домена

assert detect_text_type("google.com/") == "https://google.com/"
assert detect_text_type("google.com/index.html") == "https://google.com/index.html"
assert detect_text_type("subdomain.example.com/directory/subdirectory/file") == "https://subdomain.example.com/directory/subdirectory/file"
assert detect_text_type("domain.site/////") == "https://domain.site/////" # По стандарту, множество "/" разрешены

# Email | Happy Test

assert detect_text_type("vasya@mail.google.com") == "mailto:vasya@mail.google.com"
assert detect_text_type("vasya123@gmail.org") == "mailto:vasya123@gmail.org"
assert detect_text_type("почта@кириллица.доменное.имя") == "mailto:почта@кириллица.доменное.имя"

# Email | Sad Test

assert detect_text_type("illegal@dom....in") != "mailto:illegal@dom....in"
assert detect_text_type("without-domain@") != "mailto:without-domain@"
assert detect_text_type("@") != "mailto:@"
assert detect_text_type("sp aces@domain.zone") != "mailto:sp aces@domain.zone"

print("OK | All tests passed.")
