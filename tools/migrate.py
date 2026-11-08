"""One-time migration: pull each app's existing legal pages into editable fragments.

Reads the original per-app HTML pages listed in tools/sources.json and writes
content/apps/<app>/<doc>.html. Sections that the General Terms / General Privacy
Policy now cover (contact details, governing law, "changes" boilerplate) are left
out; everything app-specific is kept word for word.

Run once; after that, edit the fragments in content/ directly.
"""
import json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = Path(__file__).resolve().parent.parent
SRC = json.loads((ROOT / "tools/sources.json").read_text())

# Section headings (lower-case) left out of the app fragments because the
# general documents cover them. Keyed by doc, then app ("*" = every app).
EXCLUDE = {
    "terms": {
        "*": {"contact"},
        "bewildoor": {"governing law", "changes to these terms"},
        "low-flying-ducks": {"governing law", "changes to these terms"},
        "holds": {"governing law", "changes to these terms"},
        "bgrc": {"governing law", "changes to these terms"},
    },
    "privacy": {
        "*": {"contact", "who we are", "who is responsible"},
        "bewildoor": {"changes"},
        "low-flying-ducks": {"changes"},
        "holds": {"changes"},
        "bgrc": {"changes"},
        "polyloqui": {"changes"},
    },
}

# Old file names -> doc keys in the new site.
DOC_ALIASES = {
    "terms": "terms", "terms-of-service": "terms",
    "privacy": "privacy", "privacy-policy": "privacy",
    "account-deletion": "delete", "delete-account": "delete",
    "community-guidelines": "guidelines", "guidelines": "guidelines",
    "safety": "safety", "child-safety": "child-safety", "licenses": "licenses",
}

# Pages that stay on each app's own site (home pages, translations, tools).
OLD_HOST = {
    "artograffi": "https://doodle-86b98.web.app/",
    "bewildoor": "https://bewildoor-842e4.web.app/",
    "low-flying-ducks": "https://low-flying-ducks.web.app/",
    "polyloqui": "https://earshot-9vub.onrender.com/",
    "questeryng": "https://questeryng.web.app/",
    "holds": "https://holds-60f4e.web.app/",
    "bgrc": "https://mechitall-llc.github.io/bgrc-releases/",
}

# Text fixes applied while migrating (app, old, new).
TEXT_FIXES = [
    ("polyloqui", "Contact us through the developer email on Polyloqui's Google Play page.",
     "Email contact@mechitall.com."),
    # Governing law now lives in the General Terms, so name the surviving sections.
    ("bewildoor", "Sections 8 and 9 continue after these terms end.",
     "Section 8 and the General Terms on governing law continue after these terms end."),
    ("bgrc", "Sections 4, 8 and 9 continue after these terms end.",
     "Sections 4 and 8 and the General Terms on governing law continue after these terms end."),
    ("holds", "Sections 10 and 11 continue after these terms end.",
     "Section 10 and the General Terms on governing law continue after these terms end."),
    ("low-flying-ducks", "Sections 5, 11 and 12 continue after these terms end.",
     "Sections 5 and 11 and the General Terms on governing law continue after these terms end."),
]


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40]


def map_href(app, href):
    if href.startswith(("http:", "https:", "mailto:", "tel:", "#")):
        return href
    path = href.lstrip("./").lstrip("/")
    stem, _, frag = path.partition("#")
    if stem == "impressum" or stem == "impressum.html":
        return "{{link:legal-notice}}"
    base = re.sub(r"\.html$", "", stem)
    if base in DOC_ALIASES:  # English page of a doc we now host
        return "{{link:%s}}" % DOC_ALIASES[base] + (("#" + frag) if frag else "")
    return OLD_HOST[app] + path  # translations, home pages, tools stay put


def clean(node):
    for bad in node.select("a.backtotop, nav.toc, footer, script, form + .note"):
        bad.decompose()
    for c in node.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for num in node.select("span.num"):  # keep section numbers: the text refers to them
        num.replace_with(num.get_text(strip=True).rstrip(".") + ". ")


def extract(app, doc, path):
    soup = BeautifulSoup(Path(path).read_text(encoding="utf-8"), "lxml")
    main = soup.find("main") or soup.body
    clean(main)
    for a in main.find_all("a", href=True):
        a["href"] = map_href(app, a["href"])
    h1 = main.find("h1")
    excl = EXCLUDE.get(doc, {}).get("*", set()) | EXCLUDE.get(doc, {}).get(app, set())

    # Everything between the h1 and the first h2 is the app's intro (dates, lede).
    intro, node = [], h1.next_sibling
    while node is not None and not (getattr(node, "name", None) == "h2" or
                                    (getattr(node, "name", None) == "section" and node.find("h2"))):
        if getattr(node, "name", None) not in (None, "header"):
            intro.append(node)
        node = node.next_sibling

    sections = []
    for h2 in main.find_all("h2"):
        title = h2.get_text(" ", strip=True)
        if title.lower() in excl:
            continue
        parent = h2.parent
        if parent.name == "section":
            body = [c for c in parent.children if c is not h2]
            sid = parent.get("id") or slug(title)
        else:
            body, n = [], h2.next_sibling
            while n is not None and getattr(n, "name", None) != "h2":
                if getattr(n, "name", None) == "footer":
                    break
                body.append(n)
                n = n.next_sibling
            sid = h2.get("id") or slug(title)
        html = "".join(str(b) for b in body).strip()
        sections.append((f"{app}-{doc}-{sid}", title, html))

    out = []
    if intro:
        out.append('<div class="app-intro">\n' + "\n".join(str(n) for n in intro).strip() + "\n</div>")
    for sid, title, html in sections:
        out.append(f'<section id="{sid}">\n<h3>{title}</h3>\n{html}\n</section>')
    text = "\n\n".join(out) + "\n"
    for fapp, old, new in TEXT_FIXES:
        if fapp == app:
            text = text.replace(old, new)
    # Demote any h3 inside sections so headings stay in order (h3 -> h4).
    text = re.sub(r"(<section id=\"[^\"]+\">\n<h3>.*?</h3>\n)(.*?)(\n</section>)",
                  lambda m: m.group(1) + re.sub(r"<(/?)h3\b", r"<\1h4", m.group(2)) + m.group(3),
                  text, flags=re.S)
    return text


def main():
    for app, cfg in SRC.items():
        outdir = ROOT / "content/apps" / app
        outdir.mkdir(parents=True, exist_ok=True)
        for doc, f in cfg["docs"].items():
            text = extract(app, doc, Path(cfg["root"]) / f)
            (outdir / f"{doc}.html").write_text(text, encoding="utf-8")
            print(f"{app}/{doc}: {len(text)} chars")


if __name__ == "__main__":
    main()
