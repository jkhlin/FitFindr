"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Every scenario below is run five times by run_eval.py, so "the same item more
than once" (criterion 4) is just one scenario with a query that always picks
the same listing.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1: all three tools run and a
        # fit card comes back.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # Criterion 3 — state. Any normal query works; what's checked is that
        # the id the loop selected (trace step "select_item") is the id that
        # reached suggest_outfit (its trace input). A different item from
        # criterion 4's, so the two aren't riding on the same listing.
        "name": "selected item reaches suggest_outfit",
        "query": "denim jacket under $50",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # Criterion 4 — the fit card. The same query five times always selects
        # the same listing (Y2K Baby Tee, $18.00), so any difference between
        # tries is the model's wording and not a different input.
        "name": "fit card mentions price, 2+ sentences",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Criterion 5 — the price ceiling. Picked because the ceiling really
        # does remove things: without it this query returns ten listings from
        # $12 to $45, and one result sits exactly at $20, so it also tests
        # that "under $20" is inclusive of $20.
        "name": "price ceiling is respected",
        "query": "vintage tee under $20",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        # Diagnostic — not one of the five.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
