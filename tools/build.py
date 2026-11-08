"""Build the MechItAll Legal Center into public/.

    python3 tools/build.py

Sources (edit these, never the files in public/):
  content/site.json            company details and the general effective date
  content/apps.json            the list of apps
  content/general/*.html       text that applies to every app
  content/apps/<id>/<doc>.html each app's own section of each document

Documents an app can have: terms, privacy, delete, guidelines, safety,
child-safety, licenses. Only terms and privacy are required.
"""
import html, json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
OUT = ROOT / "public"

SITE = json.loads((CONTENT / "site.json").read_text())
APPS = json.loads((CONTENT / "apps.json").read_text())["apps"]

# doc key -> (file name, page title, short label)
DOCS = {
    "terms": ("terms.html", "Terms of Service", "Terms"),
    "privacy": ("privacy.html", "Privacy Policy", "Privacy"),
    "delete": ("delete-account.html", "Delete your account or data", "Delete account"),
    "guidelines": ("guidelines.html", "Community Guidelines", "Community guidelines"),
    "safety": ("safety.html", "Safety", "Safety"),
    "child-safety": ("child-safety.html", "Child Safety Standards", "Child safety"),
    "licenses": ("licenses.html", "Licenses", "Licenses"),
}
COMMUNITY_DOCS = ("guidelines", "safety", "child-safety")


def app_docs(app):
    d = CONTENT / "apps" / app["id"]
    return [k for k in DOCS if (d / f"{k}.html").exists()]


def read(path):
    return path.read_text(encoding="utf-8")


def fill(text, link):
    """Replace {{...}} placeholders. `link(doc)` returns a URL for a doc key."""
    addr = SITE["address"]
    values = {
        "company": SITE["company"], "company_long": SITE["company_long"],
        "email": SITE["email"], "registration": SITE["registration"],
        "address_line": ", ".join(addr), "address_html": "<br>".join(addr),
        "effective": SITE["effective"],
    }
    text = re.sub(r"\{\{link:([a-z-]+)\}\}", lambda m: link(m.group(1)), text)
    return re.sub(r"\{\{([a-z_]+)\}\}", lambda m: values[m.group(1)], text)


# ---- link resolvers -------------------------------------------------------

def root_link(doc):
    """Links from a page in the site root."""
    if doc == "legal-notice":
        return "legal-notice.html"
    if doc in COMMUNITY_DOCS:
        return "community.html"
    return DOCS[doc][0]


def app_link_from_root(app):
    """Links inside an app's fragment when shown on a root page."""
    def link(doc):
        if doc == "legal-notice":
            return "legal-notice.html"
        return f"apps/{app['id']}/{DOCS[doc][0]}"
    return link


def app_page_link(app):
    """Links on a page in apps/<id>/ (general text and the app's own text)."""
    have = set(app_docs(app)) | {"delete"}
    def link(doc):
        if doc == "legal-notice":
            return "../../legal-notice.html"
        if doc in have:
            return DOCS[doc][0]
        return "../../" + root_link(doc)
    return link


# ---- page shell -------------------------------------------------------------

def toc(items):
    if not items:
        return ""
    lis = "".join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in items)
    return f'<nav class="toc" aria-label="On this page"><div class="toc-title">On this page</div><ol>{lis}</ol></nav>'


def sections_of(fragment):
    return re.findall(r'<section id="([^"]+)">\s*<h2>(.*?)</h2>', fragment, flags=re.S)


def page(title, body, depth=0, crumb=None, current=None, meta=None, description=""):
    up = "../" * depth
    nav = [("index.html", "Legal Center"), ("terms.html", "Terms"), ("privacy.html", "Privacy"),
           ("delete-account.html", "Delete account"), ("community.html", "Community & safety"),
           ("licenses.html", "Licenses"), ("legal-notice.html", "Legal notice")]
    cur = ' aria-current="page"'
    nav_html = " ".join(
        f'<a href="{up}{href}"{cur if href == current and depth == 0 else ""}>{label}</a>'
        for href, label in nav)
    crumb_html = f'<div class="crumb">{crumb}</div>' if crumb else ""
    meta_html = f'<div class="updated">{meta}</div>' if meta else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · MechItAll</title>
<meta name="description" content="{html.escape(description or title)}">
<link rel="stylesheet" href="{up}assets/legal.css">
</head>
<body>
<main class="wrap">
<header class="top" id="top">
  <a class="wordmark" href="{up}index.html">MechItAll</a>
  <div class="kicker">Legal Center</div>
</header>
{crumb_html}
<h1 class="title">{title}</h1>
{meta_html}
{body}
<footer class="legal-nav">
  <nav aria-label="Legal documents">{nav_html}</nav>
  <div>{SITE["company"]} · <a href="mailto:{SITE["email"]}">{SITE["email"]}</a></div>
</footer>
</main>
</body>
</html>
"""


def write(rel, text):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def app_block(app, doc, link, heading_id=None, heading=None):
    frag = fill(read(CONTENT / "apps" / app["id"] / f"{doc}.html"), link)
    hid = heading_id or app["id"]
    head = heading or html.escape(app["name"])
    sub = html.escape(app["about"])
    return (f'<section class="app" id="{hid}">\n<h2><span class="app-name">{head}</span>'
            f'<span class="app-about">{sub}</span></h2>\n{frag}\n</section>')


GENERAL_META = (f"Effective date: {SITE['effective']}<br>Applies to all apps and games made by "
                f"{SITE['company']}, and these web pages")


# ---- root pages -------------------------------------------------------------

def build_combined(doc, general_name, title, description):
    general = fill(read(CONTENT / "general" / f"{general_name}.html"), root_link) if general_name else ""
    apps = [a for a in APPS if (CONTENT / "apps" / a["id"] / f"{doc}.html").exists()]
    items = [(i, re.sub("<[^>]+>", "", t)) for i, t in sections_of(general)]
    items += [(a["id"], a["name"]) for a in apps]
    lede, rest = split_lede(general)
    blocks = []
    if rest:
        blocks.append('<div class="part-label">General terms for every app</div>' if doc == "terms" else
                      '<div class="part-label">For every app</div>' if doc == "privacy" else "")
        blocks.append(rest)
    if doc in ("terms", "privacy"):
        blocks.append('<div class="part-label">App sections</div>')
    for a in apps:
        blocks.append(app_block(a, doc, app_link_from_root(a)))
    body = lede + toc(items) + "\n".join(blocks)
    write(DOCS[doc][0], page(title, body, current=DOCS[doc][0], meta=GENERAL_META, description=description))


def split_lede(fragment):
    m = re.match(r'\s*(<div class="lede">.*?</div>)(.*)', fragment, flags=re.S)
    return (m.group(1), m.group(2)) if m else ("", fragment)


def build_community():
    general = fill(read(CONTENT / "general/community.html"), root_link)
    blocks, items = [], []
    for a in APPS:
        for doc in COMMUNITY_DOCS:
            if (CONTENT / "apps" / a["id"] / f"{doc}.html").exists():
                hid = f"{a['id']}-{doc}"
                items.append((hid, f"{a['name']}: {DOCS[doc][2]}"))
                blocks.append(app_block(a, doc, app_link_from_root(a), heading_id=hid,
                                        heading=f"{html.escape(a['name'])} · {DOCS[doc][1]}"))
    body = general + toc(items) + "\n".join(blocks)
    write("community.html", page("Community & Safety", body, current="community.html", meta=GENERAL_META,
                                 description="Community guidelines, safety tips and child safety standards for MechItAll apps."))


def build_notice():
    body = fill(read(CONTENT / "general/legal-notice.html"), root_link)
    write("legal-notice.html", page("Legal notice", body, current="legal-notice.html",
                                    description="Provider information for MechItAll LLC (Impressum)."))


def build_index():
    rows = []
    for a in APPS:
        docs = app_docs(a) + (["delete"] if "delete" not in app_docs(a) else [])
        links = " · ".join(f'<a href="apps/{a["id"]}/{DOCS[d][0]}">{DOCS[d][2]}</a>'
                           for d in DOCS if d in docs)
        rows.append(f'<tr><td><a href="apps/{a["id"]}/index.html"><strong>{html.escape(a["name"])}</strong></a>'
                    f'<div class="muted">{html.escape(a["about"])}</div></td>'
                    f'<td>{a["min_age"]}+</td><td>{links}</td></tr>')
    body = f"""<div class="lede">
<p>All legal documents for the apps and games made by {SITE['company']} in one place. Each document has a general part that applies to every app and a section for each app.</p>
<p>Questions? Email <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
</div>
<h2>Documents</h2>
<ul class="doclist">
<li><a href="terms.html">Terms of Service</a>: general terms and each app's terms</li>
<li><a href="privacy.html">Privacy Policy</a>: what each app collects and why, and your rights</li>
<li><a href="delete-account.html">Delete your account or data</a>: steps for each app</li>
<li><a href="community.html">Community &amp; safety</a>: community guidelines, safety tips and child safety standards</li>
<li><a href="licenses.html">Licenses</a>: open-source software in our apps</li>
<li><a href="legal-notice.html">Legal notice</a>: company details (Impressum)</li>
</ul>
<h2>Our apps</h2>
<div class="table-wrap"><table>
<tr><th>App</th><th>Age</th><th>Documents</th></tr>
{''.join(rows)}
</table></div>"""
    write("index.html", page("Legal Center", body, current="index.html", meta=GENERAL_META,
                             description="Terms, privacy and other legal documents for all MechItAll apps."))


# ---- per-app pages ----------------------------------------------------------

def build_app_pages(app):
    link = app_page_link(app)
    docs = app_docs(app)
    crumb = (f'<a href="../../index.html">Legal Center</a> › '
             f'<a href="index.html">{html.escape(app["name"])}</a>')
    for doc in docs:
        frag = fill(read(CONTENT / "apps" / app["id"] / f"{doc}.html"), link)
        title = f"{app['name']} {DOCS[doc][1]}"
        if doc in ("terms", "privacy"):
            general = fill(read(CONTENT / "general" / f"{doc}.html"), link)
            lede, rest = split_lede(general)
            items = [(i, re.sub("<[^>]+>", "", t)) for i, t in sections_of(rest)] + [(app["id"], f"{app['name']} section")]
            part = "General terms for every MechItAll app" if doc == "terms" else "For every MechItAll app"
            body = (lede + toc(items) + f'<div class="part-label">{part}</div>' + rest +
                    f'<div class="part-label">{html.escape(app["name"])}</div>' +
                    app_block(app, doc, link))
            meta = (f"General part effective {SITE['effective']}. The {html.escape(app['name'])} section shows its own date.<br>"
                    f"Applies to {html.escape(app['name'])}" + (f" ({app['package']})" if app.get("package") else "") +
                    f", by {SITE['company']}")
        else:
            body = frag
            meta = f"Applies to {html.escape(app['name'])}, by {SITE['company']}"
        if app.get("translations") and doc == "privacy":
            langs = " · ".join(f'<a href="{u}">{html.escape(l)}</a>' for l, u in app["translations"].items())
            body = f'<p class="langs">Other languages: {langs}</p>' + body
        write(f"apps/{app['id']}/{DOCS[doc][0]}", page(title, body, depth=2, crumb=crumb, meta=meta))
    # app index
    lis = "".join(f'<li><a href="{DOCS[d][0]}">{DOCS[d][1]}</a></li>' for d in DOCS if d in docs)
    body = (f'<div class="lede"><p>{html.escape(app["about"])}. Platforms: {html.escape(app["platforms"])}. '
            f'Minimum age: {app["min_age"]}.</p><p><a href="{app["home"]}">{html.escape(app["name"])} website</a></p></div>'
            f'<ul class="doclist">{lis}<li><a href="../../legal-notice.html">Legal notice</a></li></ul>')
    write(f"apps/{app['id']}/index.html", page(f"{app['name']} legal documents", body, depth=2,
                                               crumb='<a href="../../index.html">Legal Center</a>'))


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    (OUT / ".nojekyll").write_text("")
    build_index()
    build_combined("terms", "terms", "Terms of Service", "Terms of Service for all MechItAll apps.")
    build_combined("privacy", "privacy", "Privacy Policy", "How MechItAll apps handle personal information.")
    build_combined("delete", "delete", "Delete your account or data", "How to delete your account or data in each MechItAll app.")
    build_combined("licenses", "licenses", "Licenses", "Open-source software used in MechItAll apps.")
    build_community()
    build_notice()
    for app in APPS:
        build_app_pages(app)
    write("404.html", page("Page not found", '<p>That page doesn\'t exist. Go to the <a href="/">Legal Center</a>.</p>'))
    print("built", sum(1 for _ in OUT.rglob("*.html")), "pages into", OUT)


if __name__ == "__main__":
    main()
