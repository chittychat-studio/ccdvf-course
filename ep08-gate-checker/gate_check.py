# gate_check.py - CCDV-F EP 08 companion.
# Reads a requirements record and a
# release file, then prints what blocks
# the next gate. Exit code 1 if anything
# is flagged, so a pipeline stops there.
# Never calls the Anthropic API.
import json
import sys

# Words that make a wish, not a check.
VAGUE = ("faster", "better", "easy")
# The four questions nobody says aloud.
INFRA = ("latency", "scale",
         "residency", "identity")

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def check(req, rel):
    out = []
    # Move 1: requirements you can test.
    for r in req["functional"]:
        text = r["text"].lower()
        bad = [w for w in VAGUE
               if w in text]
        if bad:
            msg = f'vague "{bad[0]}"'
            out.append(("FLAG",
                        f"{r['id']}: {msg}"))
    have = req["infrastructure"]
    miss = [k for k in INFRA
            if not have.get(k)]
    if miss:
        out.append(("FLAG", "missing: "
                    + ", ".join(miss)))
    else:
        out.append(("PASS",
                    "infra: all four"))
    # The design gate: residency.
    rule = have["residency"]["region"]
    runs = rel["platform"]["region"]
    if runs != rule:
        out.append(("FLAG",
            f"residency: {runs} not {rule}"))
    # The release gate: pin, then eval.
    if rel["model"] == rel["tested"]:
        out.append(("PASS", "model: pinned"))
    else:
        out.append(("FLAG", "model: untested"))
    if rel["eval"] != "passed":
        out.append(("FLAG", "eval: not passed"))
    return out

def main():
    folder = (sys.argv[1] if len(sys.argv) > 1
              else "fixtures/ravi-plan")
    req = load(f"{folder}/requirements.json")
    rel = load(f"{folder}/release.json")
    results = check(req, rel)
    for status, msg in results:
        print(status, msg)
    flagged = any(s == "FLAG"
                  for s, _ in results)
    sys.exit(1 if flagged else 0)

if __name__ == "__main__":
    main()
