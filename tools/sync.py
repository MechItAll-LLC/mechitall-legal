"""Re-imports one app's legal pages from its own repository into content/apps/<app>/.

Until an app links to the Legal Center, its own pages (in its repo) are what players see, so they
stay the source and this copies them in. After the switch, edit content/apps/<app>/ directly and
turn the app's own pages into redirects (REDIRECTS.md).

    python3 tools/sync.py <app> [<app> ...]      # show what would change
    python3 tools/sync.py <app> --write          # write it

Uses the extraction rules in migrate.py and the local checkouts in tools/local_sources.json.
Needs: pip install beautifulsoup4 lxml
"""
import difflib, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import migrate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LOCAL = json.loads((ROOT / "tools/local_sources.json").read_text(encoding="utf-8"))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    write = "--write" in sys.argv
    if not args:
        sys.exit(__doc__)
    for app in args:
        cfg = migrate.SRC[app]
        root = Path(LOCAL[app])
        for doc, f in cfg["docs"].items():
            src = root / f
            if not src.exists():
                print(f"{app}/{doc}: missing {src}")
                continue
            new = migrate.extract(app, doc, src)
            dest = ROOT / "content/apps" / app / f"{doc}.html"
            old = dest.read_text(encoding="utf-8") if dest.exists() else ""
            if new == old:
                print(f"{app}/{doc}: up to date")
                continue
            diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(), f"content/{app}/{doc}", f"{src}", lineterm="", n=0))
            print(f"{app}/{doc}: {len(diff)} changed lines" + (" (written)" if write else ""))
            if not write:
                print("\n".join(d[:200] for d in diff[:40]))
            else:
                dest.write_text(new, encoding="utf-8")


if __name__ == "__main__":
    main()
