# Switching the apps to the Legal Center

The Legal Center is live at https://legal.mechitall.com, but the apps and their store listings still link to
each app's own pages. Switch one app at a time, in this order:

1. **Content is current.** Run `python3 tools/sync.py <app>`. It must say "up to date" for every page; if not,
   run it with `--write`, check the diff, build (`python3 tools/build.py`), commit and push.
2. **The app links here.** Change the in-app links (table below) to
   `https://legal.mechitall.com/apps/<id>/privacy.html`, `terms.html`, `delete-account.html` and any others the
   app has, and release the app.
3. **Store listings.** Play Console › App content › Privacy policy, and Data safety › Data deletion URL. Also
   update the app's own copies of the listing (paths below), the itch.io page where there is one, and any
   app store "support" links.
4. **Redirects.** Only after 1–3: add the redirects from `REDIRECTS.md`, so saved links and older app versions
   still arrive at the right page.
5. **Source of truth moves here.** Edit `content/apps/<id>/` from now on, and delete the app's own copies
   (keep the translated pages, which stay on the app's site for now).

`python3 tools/sync.py` needs `pip install beautifulsoup4 lxml` and the checkouts in `tools/local_sources.json`.

## Where each app links to its legal pages

| App | In-app links | Store and docs | Status |
|---|---|---|---|
| artograffi | `lib/widgets/legal_document.dart`, `functions/src/index.ts` (emails), `android/app/src/main/AndroidManifest.xml` | `CLAUDE.md`, Play Console | Not switched |
| Bewildoor | `scripts/ui/panels/about_panel.gd`: switches with the remote config key `legal_center` (no release needed, see Bewildoor `docs/PLAY_STORE.md`) | `store/listing.md`, `store/data-safety.md`, `itch/description.md` | Prepared, not switched |
| BGRC | the `web/` pages | `store/PLAY_CONSOLE.md`, `bgrc-releases` pages | Not switched |
| H.O.L.D.S. | `scripts/online/online.gd`, `scripts/ui/panels/forum_panel.gd` | `store/listing.md`, `store/data-safety.md`, `store/PLAY_CONSOLE.md`, `store/OPEN_RELEASE.md` | Not switched |
| Low Flying Ducks | `lib/app/legal.dart` (one base URL) | `store/listing.md` | Not switched |
| Polyloqui | `app/android/app/src/main/AndroidManifest.xml`, the room server's `public/` pages | `store/LISTING.md`, `store/PLAY_CONSOLE.md` | Not switched |
| Questeryng | `lib/utils/constants.dart` (`termsUrl`, `privacyUrl`) | `docs/play/app-content.md`, `docs/play/data-safety.md`, `docs/play/store-listing.md` | Not switched |

Paths are relative to each app's repository under `C:\dev`.

## Content check (November 11, 2026)

- Every app's Legal Center pages match the app's own current pages (`tools/sync.py`), after Bewildoor's
  November 11 update (crash reports, Google Play Games, rating prompt, settings file).
- Every app has terms, privacy and a data deletion page. The built site has no broken internal links or
  unfilled placeholders.
- Each app's privacy page was checked against its SDKs (Firebase products, sign-in, purchases, push, location,
  crash reporting, analytics, moderation services); every one in use is described.
- `apps.json` now lists Polyloqui's (`com.polyloqui.app`) and Questeryng's (`com.sidequestapp.sidequest`)
  package names.
