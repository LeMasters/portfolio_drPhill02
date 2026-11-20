"""
Check that the Pages CMS configuration and every content file parse, and that each
key in a content file has a field in its .pages.yml form (so saving never drops a key).
Usage: python3 dev/check_content.py   (from the repository root; needs PyYAML)
"""
import glob, sys, yaml

ok = True
def fail(msg):
    global ok; ok = False; print("FAIL", msg)

try:
    cfg = yaml.safe_load(open(".pages.yml"))
except yaml.YAMLError as e:
    print("FAIL .pages.yml does not parse:\n", e); sys.exit(1)

def front_matter(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        return {}
    return yaml.safe_load(text.split("---", 2)[1]) or {}

for form in cfg["content"]:
    fields = {f["name"] for f in form.get("fields", [])}
    if form["type"] == "collection":
        files = sorted(glob.glob(form["path"] + "/*.md"))
        files = [f for f in files if not f.endswith("_index.md")]
    else:
        files = [form["path"]]
    for f in files:
        try:
            data = front_matter(f) if f.endswith(".md") else yaml.safe_load(open(f))
        except yaml.YAMLError as e:
            fail(f"{f} does not parse: {e}"); continue
        rows = data if isinstance(data, list) else [data or {}]
        for row in rows:
            extra = set(row) - fields
            if extra:
                fail(f"{f}: keys with no form field in '{form['name']}': {sorted(extra)}")
    print(f"ok   {form['label']:<11} {len(files)} file(s)")

print("\nAll content checks passed." if ok else "\nContent checks FAILED.")
sys.exit(0 if ok else 1)
