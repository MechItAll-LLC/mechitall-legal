# MechItAll Legal Center

Terms, privacy policies and other legal documents for every MechItAll LLC app, in one place.
Each document has a **general part** that applies to every app and a **section per app**.

## Layout

| Path | What |
|---|---|
| `content/site.json` | Company name, address, email, registration, effective date of the general parts |
| `content/apps.json` | The list of apps (name, one-line description, package id, minimum age, home page) |
| `content/general/*.html` | General Terms, general Privacy Policy, Legal notice, and short intros for the other pages |
| `content/apps/<id>/<doc>.html` | Each app's own section: `terms`, `privacy`, `delete`, and optional `guidelines`, `safety`, `child-safety`, `licenses` |
| `assets/legal.css` | Styles |
| `tools/build.py` | Builds the site into `public/` |
| `tools/migrate.py` | One-time import of the old per-app pages (already run; kept for reference) |
| `public/` | The built site. Don't edit by hand; run the build. |

Placeholders you can use in any content file: `{{email}}`, `{{company}}`, `{{address_line}}`,
`{{link:terms}}`, `{{link:privacy}}`, `{{link:delete}}`, `{{link:guidelines}}`, `{{link:safety}}`,
`{{link:child-safety}}`, `{{link:licenses}}`, `{{link:legal-notice}}`. Links resolve to the right page
for wherever the text is shown.

## Build

    python3 tools/build.py

Needs only Python 3. Then open `public/index.html` in a browser.

## Add a new app

1. Add an entry to `content/apps.json`.
2. Create `content/apps/<id>/terms.html` and `privacy.html` (copy a similar app's files and edit them).
   Only write what is specific to the app; the general parts already cover contact details,
   governing law, rights, children, security and changes.
3. Add `delete.html` (steps to delete data) and any of `guidelines.html`, `safety.html`,
   `child-safety.html`, `licenses.html` the app needs.
4. Run the build, commit and push. The app's pages appear at `apps/<id>/...`.

## Addresses to use in apps and store listings

For each app, use its own pages (they contain the general part plus that app's section):

    https://legal.mechitall.com/apps/<id>/privacy.html
    https://legal.mechitall.com/apps/<id>/terms.html
    https://legal.mechitall.com/apps/<id>/delete-account.html

The combined pages (`/terms.html`, `/privacy.html`, ...) show every app, with an anchor per app
(for example `/privacy.html#bewildoor`).

## Publish (GitHub Pages)

1. Create the repository `MechItAll-LLC/mechitall-legal` on GitHub (public) and push this folder.
2. Repository → Settings → Pages → Source: **GitHub Actions**. The workflow in
   `.github/workflows/pages.yml` builds and publishes on every push to `main`.
3. Custom domain: in Settings → Pages enter `legal.mechitall.com`. In your domain's DNS (Turbify),
   add a `CNAME` record: host `legal`, value `mechitall-llc.github.io`. When the check passes,
   tick **Enforce HTTPS**.

See `REDIRECTS.md` for pointing the old per-app addresses here.
