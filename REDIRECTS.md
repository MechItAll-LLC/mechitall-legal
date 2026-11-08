# Pointing the old addresses here

Do this **after** the Legal Center is live at https://legal.mechitall.com, so nothing points at a page that doesn't exist yet.

1. Change the privacy policy, terms and account-deletion URLs in each app's Google Play Console listing (App content → Privacy policy; Data safety → Data deletion) and in each app's code to the new addresses below.
2. Then add the redirects so old links people saved, and older app versions, still land on the right page.

Translated pages (artograffi and Questeryng) stay on their current sites for now; only the English pages move.

## artograffi

New addresses: `https://legal.mechitall.com/apps/artograffi/privacy.html`, `https://legal.mechitall.com/apps/artograffi/terms.html`, `https://legal.mechitall.com/apps/artograffi/delete-account.html`

Add to the `hosting` block of `C:\dev\artograffi\firebase.json`, then `firebase deploy --only hosting`:

```json
"redirects": [
  {
    "source": "/privacy-policy",
    "destination": "https://legal.mechitall.com/apps/artograffi/privacy.html",
    "type": 301
  },
  {
    "source": "/privacy-policy.html",
    "destination": "https://legal.mechitall.com/apps/artograffi/privacy.html",
    "type": 301
  },
  {
    "source": "/terms-of-service",
    "destination": "https://legal.mechitall.com/apps/artograffi/terms.html",
    "type": 301
  },
  {
    "source": "/terms-of-service.html",
    "destination": "https://legal.mechitall.com/apps/artograffi/terms.html",
    "type": 301
  },
  {
    "source": "/account-deletion",
    "destination": "https://legal.mechitall.com/apps/artograffi/delete-account.html",
    "type": 301
  },
  {
    "source": "/account-deletion.html",
    "destination": "https://legal.mechitall.com/apps/artograffi/delete-account.html",
    "type": 301
  },
  {
    "source": "/community-guidelines",
    "destination": "https://legal.mechitall.com/apps/artograffi/guidelines.html",
    "type": 301
  },
  {
    "source": "/community-guidelines.html",
    "destination": "https://legal.mechitall.com/apps/artograffi/guidelines.html",
    "type": 301
  },
  {
    "source": "/safety",
    "destination": "https://legal.mechitall.com/apps/artograffi/safety.html",
    "type": 301
  },
  {
    "source": "/safety.html",
    "destination": "https://legal.mechitall.com/apps/artograffi/safety.html",
    "type": 301
  },
  {
    "source": "/impressum",
    "destination": "https://legal.mechitall.com/legal-notice.html",
    "type": 301
  },
  {
    "source": "/impressum.html",
    "destination": "https://legal.mechitall.com/legal-notice.html",
    "type": 301
  }
]
```

## bewildoor

New addresses: `https://legal.mechitall.com/apps/bewildoor/privacy.html`, `https://legal.mechitall.com/apps/bewildoor/terms.html`, `https://legal.mechitall.com/apps/bewildoor/delete-account.html`

Add to the `hosting` block of `C:\dev\bewildoor\firebase.json`, then `firebase deploy --only hosting`:

```json
"redirects": [
  {
    "source": "/privacy",
    "destination": "https://legal.mechitall.com/apps/bewildoor/privacy.html",
    "type": 301
  },
  {
    "source": "/privacy.html",
    "destination": "https://legal.mechitall.com/apps/bewildoor/privacy.html",
    "type": 301
  },
  {
    "source": "/terms",
    "destination": "https://legal.mechitall.com/apps/bewildoor/terms.html",
    "type": 301
  },
  {
    "source": "/terms.html",
    "destination": "https://legal.mechitall.com/apps/bewildoor/terms.html",
    "type": 301
  },
  {
    "source": "/account-deletion",
    "destination": "https://legal.mechitall.com/apps/bewildoor/delete-account.html",
    "type": 301
  },
  {
    "source": "/account-deletion.html",
    "destination": "https://legal.mechitall.com/apps/bewildoor/delete-account.html",
    "type": 301
  },
  {
    "source": "/licenses",
    "destination": "https://legal.mechitall.com/apps/bewildoor/licenses.html",
    "type": 301
  },
  {
    "source": "/licenses.html",
    "destination": "https://legal.mechitall.com/apps/bewildoor/licenses.html",
    "type": 301
  },
  {
    "source": "/impressum",
    "destination": "https://legal.mechitall.com/legal-notice.html",
    "type": 301
  },
  {
    "source": "/impressum.html",
    "destination": "https://legal.mechitall.com/legal-notice.html",
    "type": 301
  }
]
```

## low-flying-ducks

New addresses: `https://legal.mechitall.com/apps/low-flying-ducks/privacy.html`, `https://legal.mechitall.com/apps/low-flying-ducks/terms.html`, `https://legal.mechitall.com/apps/low-flying-ducks/delete-account.html`

Add to the `hosting` block of `C:\dev\low_flying_ducks\firebase.json`, then `firebase deploy --only hosting`:

```json
"redirects": [
  {
    "source": "/privacy",
    "destination": "https://legal.mechitall.com/apps/low-flying-ducks/privacy.html",
    "type": 301
  },
  {
    "source": "/privacy.html",
    "destination": "https://legal.mechitall.com/apps/low-flying-ducks/privacy.html",
    "type": 301
  },
  {
    "source": "/terms",
    "destination": "https://legal.mechitall.com/apps/low-flying-ducks/terms.html",
    "type": 301
  },
  {
    "source": "/terms.html",
    "destination": "https://legal.mechitall.com/apps/low-flying-ducks/terms.html",
    "type": 301
  },
  {
    "source": "/account-deletion",
    "destination": "https://legal.mechitall.com/apps/low-flying-ducks/delete-account.html",
    "type": 301
  },
  {
    "source": "/account-deletion.html",
    "destination": "https://legal.mechitall.com/apps/low-flying-ducks/delete-account.html",
    "type": 301
  },
  {
    "source": "/impressum",
    "destination": "https://legal.mechitall.com/legal-notice.html",
    "type": 301
  },
  {
    "source": "/impressum.html",
    "destination": "https://legal.mechitall.com/legal-notice.html",
    "type": 301
  }
]
```

## questeryng

New addresses: `https://legal.mechitall.com/apps/questeryng/privacy.html`, `https://legal.mechitall.com/apps/questeryng/terms.html`, `https://legal.mechitall.com/apps/questeryng/delete-account.html`

Add to the `hosting` block of `C:\dev\questeryng\firebase.json`, then `firebase deploy --only hosting`:

```json
"redirects": [
  {
    "source": "/privacy",
    "destination": "https://legal.mechitall.com/apps/questeryng/privacy.html",
    "type": 301
  },
  {
    "source": "/privacy.html",
    "destination": "https://legal.mechitall.com/apps/questeryng/privacy.html",
    "type": 301
  },
  {
    "source": "/terms",
    "destination": "https://legal.mechitall.com/apps/questeryng/terms.html",
    "type": 301
  },
  {
    "source": "/terms.html",
    "destination": "https://legal.mechitall.com/apps/questeryng/terms.html",
    "type": 301
  },
  {
    "source": "/delete-account",
    "destination": "https://legal.mechitall.com/apps/questeryng/delete-account.html",
    "type": 301
  },
  {
    "source": "/delete-account.html",
    "destination": "https://legal.mechitall.com/apps/questeryng/delete-account.html",
    "type": 301
  },
  {
    "source": "/guidelines",
    "destination": "https://legal.mechitall.com/apps/questeryng/guidelines.html",
    "type": 301
  },
  {
    "source": "/guidelines.html",
    "destination": "https://legal.mechitall.com/apps/questeryng/guidelines.html",
    "type": 301
  },
  {
    "source": "/safety",
    "destination": "https://legal.mechitall.com/apps/questeryng/safety.html",
    "type": 301
  },
  {
    "source": "/safety.html",
    "destination": "https://legal.mechitall.com/apps/questeryng/safety.html",
    "type": 301
  },
  {
    "source": "/child-safety",
    "destination": "https://legal.mechitall.com/apps/questeryng/child-safety.html",
    "type": 301
  },
  {
    "source": "/child-safety.html",
    "destination": "https://legal.mechitall.com/apps/questeryng/child-safety.html",
    "type": 301
  }
]
```

## holds

New addresses: `https://legal.mechitall.com/apps/holds/privacy.html`, `https://legal.mechitall.com/apps/holds/terms.html`, `https://legal.mechitall.com/apps/holds/delete-account.html`

Add to the `hosting` block of `C:\dev\holds\firebase.json`, then `firebase deploy --only hosting`:

```json
"redirects": [
  {
    "source": "/privacy",
    "destination": "https://legal.mechitall.com/apps/holds/privacy.html",
    "type": 301
  },
  {
    "source": "/privacy.html",
    "destination": "https://legal.mechitall.com/apps/holds/privacy.html",
    "type": 301
  },
  {
    "source": "/terms",
    "destination": "https://legal.mechitall.com/apps/holds/terms.html",
    "type": 301
  },
  {
    "source": "/terms.html",
    "destination": "https://legal.mechitall.com/apps/holds/terms.html",
    "type": 301
  },
  {
    "source": "/account-deletion",
    "destination": "https://legal.mechitall.com/apps/holds/delete-account.html",
    "type": 301
  },
  {
    "source": "/account-deletion.html",
    "destination": "https://legal.mechitall.com/apps/holds/delete-account.html",
    "type": 301
  },
  {
    "source": "/community-guidelines",
    "destination": "https://legal.mechitall.com/apps/holds/guidelines.html",
    "type": 301
  },
  {
    "source": "/community-guidelines.html",
    "destination": "https://legal.mechitall.com/apps/holds/guidelines.html",
    "type": 301
  },
  {
    "source": "/child-safety",
    "destination": "https://legal.mechitall.com/apps/holds/child-safety.html",
    "type": 301
  },
  {
    "source": "/child-safety.html",
    "destination": "https://legal.mechitall.com/apps/holds/child-safety.html",
    "type": 301
  },
  {
    "source": "/licenses",
    "destination": "https://legal.mechitall.com/apps/holds/licenses.html",
    "type": 301
  },
  {
    "source": "/licenses.html",
    "destination": "https://legal.mechitall.com/apps/holds/licenses.html",
    "type": 301
  },
  {
    "source": "/impressum",
    "destination": "https://legal.mechitall.com/legal-notice.html",
    "type": 301
  },
  {
    "source": "/impressum.html",
    "destination": "https://legal.mechitall.com/legal-notice.html",
    "type": 301
  }
]
```

## polyloqui

New addresses: `https://legal.mechitall.com/apps/polyloqui/privacy.html`, `https://legal.mechitall.com/apps/polyloqui/terms.html`, `https://legal.mechitall.com/apps/polyloqui/licenses.html`

The legal pages are served by the room server on Render (`public/privacy.html`, `public/terms.html`, `public/licenses.html`). Replace each with a redirect, or add 301 routes in the server for `/privacy`, `/terms` and `/licenses`. Also update the links inside the app and the web version.

## bgrc

New addresses: `https://legal.mechitall.com/apps/bgrc/privacy.html`, `https://legal.mechitall.com/apps/bgrc/terms.html`, `https://legal.mechitall.com/apps/bgrc/delete-account.html`

GitHub Pages can't send real redirects. In `MechItAll-LLC/bgrc-releases`, replace `privacy.html`, `terms.html` and `account-deletion.html` with a page like this (change the address for each):

```html
<!doctype html><meta charset="utf-8"><title>Moved</title>
<meta http-equiv="refresh" content="0; url=https://legal.mechitall.com/apps/bgrc/privacy.html">
<link rel="canonical" href="https://legal.mechitall.com/apps/bgrc/privacy.html">
<p>This page moved to <a href="https://legal.mechitall.com/apps/bgrc/privacy.html">https://legal.mechitall.com/apps/bgrc/privacy.html</a>.</p>
```

Also update `store/PLAY_CONSOLE.md` and the links in BGRC's `web/` pages.
