# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

A user types a plain-language thrifting request, like `vintage graphic tee
under $30, size M`. FitFindr parses out a description, a size, and a price
ceiling; searches the 40 mock listings for the best match; and, if it finds
one, asks the model to suggest an outfit pairing that item with pieces from
the user's own wardrobe and to write a short social-caption-style "fit card"
for it. If nothing in the data matches the request, it stops and says what to
change — a different size, a broader description, a higher price ceiling —
instead of guessing an outfit for an item that doesn't exist.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`
- **What it does:** Searches the listings data for items matching a description and optionally filters by size and maximum price. Size matching is case-insensitive and matches complete size values/tokens rather than arbitrary substrings. For example, `M` matches `S/M`, but `L` does not match `XL`, and `S` does not match `US 9`.
- **Inputs:** `description` (str), `size` (str | None), `max_price` (float | None)
- **Returns:** A list of matching listing dictionaries, ordered from best match to worst match. Each dictionary contains `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.
- **When it has nothing:** Returns an empty list `[]` when no listings match.

### `suggest_outfit`
- **What it does:** Suggests one or two outfits using the new thrifted item and items from the user's wardrobe.
- **Inputs:** `new_item` (dict), `wardrobe` (dict)
- **Returns:** A non-empty string containing outfit suggestions that use the new item and, when available, specific items from the user's wardrobe.
- **When it has nothing:** If the wardrobe has no items, returns general styling advice for the new item instead of returning an empty string or raising an error.

### `create_fit_card`
- **What it does:** Creates a short social-media-style caption for the thrifted item and suggested outfit.
- **Inputs:** `outfit` (str), `new_item` (dict)
- **Returns:** A two-to-four sentence caption that mentions the item, its price, its platform, and the outfit's overall vibe.
- **When it has nothing:** If `outfit` is empty or contains only whitespace, returns a descriptive message instead of raising an error.
---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message in the session saying that no matching listings were found and stop. Otherwise, take the first result and continue to `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex, in `agent.py::_parse_query`. Three passes over the query string, each removing what it matched before the next pass runs: a price-ceiling pattern (`under $30`, `below 30`, `$30 or less`, or a bare `$30`), then a `size X` pattern, then whatever's left — minus a short stopword list (`a`, `the`, `in`, `for`, ...) — becomes the `description` handed to `search_listings`.

**What moves through the session:** `query` → `parsed` (the dict from `_parse_query`: description/size/max_price) → `search_results` (what `search_listings` returned) → `selected_item` (the first result) → `outfit_suggestion` → `fit_card`, in that order. Each tool reads its input back out of the session rather than receiving it as a value passed straight from the previous call.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here are two quick ways to style that butterfly tee with what you already own:

**1. 2000s Streetwear**
Pair the baby tee with your **baggy straight-leg jeans** and **chunky white sneakers**. Throw on the **black cropped zip hoodie** over your shoulders and grab your **black crossbody bag** to lean into that throwback Y2K aesthetic.

**2. Casual Contrast**
Tuck the tee into your **wide-leg khaki trousers**, add the **brown leather belt**, and finish it off with your **chunky white sneakers**. It balances the fitted, girly top with relaxed, neutral bottoms.

  Fit card: I literally squealed when I scored this Y2K baby tee on depop for just $18.00! The butterfly print is *so* 2000s, and it looks insanely good paired with baggy jeans or tucked into wide-leg khakis. Honestly living out my Lizzie McGuire dreams in this one. ✨🦋

0 model calls this session, 2 served from cache
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Here are two easy ways to style those Vintage Levi's 501 Jeans using what's already in your closet:

**Outfit 1: Casual Streetwear**
*   **Top:** White ribbed tank top (tucked in)
*   **Outerwear:** Vintage black denim jacket worn over top
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Outfit 2: Cozy & Relaxed**
*   **Top:** Oversized grey crewneck sweatshirt
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt threaded through the jeans
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Honestly, the thrift gods were smiling on me when I stumbled on these vintage Levi's 501 jeans today. I'm picturing them slightly slouchy with crisp white sneakers and a beat-up leather jacket for that effortless 90s off-duty look. Grabbed them on depop for just $38.00 and I don't think I'll ever take them off!
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked Claude to implement `suggest_outfit` in `tools.py`, following the docstring already there (format the wardrobe into the prompt, handle the empty-wardrobe case separately).
- *What came back:* A working version, but the line that conditionally appended the item's brand used a nested f-string with an escaped quote inside the expression part — `f"{f', brand: {new_item[\"brand\"]}' if ... else ''}"`. That syntax is only legal from Python 3.12 onward.
- *What I changed:* `test.py` in this repo pins `MIN_PYTHON = (3, 11)`, so that line would crash for anyone on 3.11. I had it rewritten as a separate `brand_part` variable built with a plain f-string instead, and confirmed `python -c "import ast; ast.parse(open('tools.py').read())"` parses cleanly.

**Moment 2**

- *What I asked for:* I asked Claude to build `search_listings`'s size filter per the spec's own warning: a plain substring check (`size.lower() in listing["size"].lower()`) is wrong, because `"s" in "us 9"` and `"l" in "xl"` are both `True`.
- *What came back:* An implementation that splits the listing's `size` field on non-alphanumeric characters (so `"XL (oversized)"` becomes `["XL", "oversized"]`) and matches the requested size against those tokens exactly, case-insensitively, instead of doing a substring check.
- *What I changed:* I verified it directly rather than taking it on faith: `search_listings('sneakers', size='S')` against listings sized `"US 8"` and `"US 9"` returns `[]`, and `search_listings('tee', size='M')` correctly matches listings sized `"S/M"`. Both match what the docstring said should and shouldn't happen.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools and returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before `suggest_outfit` and names what to change | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. `selected_item` id is the id `suggest_outfit` received | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions the price and is at least 2 sentences | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Every result from a price-capped query is at or under the cap | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Run with `python run_eval.py --label before` — 6 scenarios × 5 tries, cache off,
`TEMPERATURE` 0.9. Full output: `results/run_2026-10-13_1553_before.md`.

**It was a real re-run, not cached answers.** The run reported 50 model calls and
no cache hits (15,457 prompt + 6,056 output tokens), and the five fit cards for
the same item differ from each other (see criterion 4 below) — they are five
different answers.

**How each try was scored** (against the criterion as written in `criteria.md`,
read back out of the saved log rather than from the console summary):

1. `session["error"]` is `None`, the trace has both `suggest_outfit` and `create_fit_card` steps, and a fit card came back.
2. `session["error"]` is set, the trace stops at step 2, and the message names what to change. No `suggest_outfit` or `create_fit_card` step appears.
3. The id in the trace's `select_item` step equals the id in the `suggest_outfit` step's input.
4. The card contains the selected item's price (`$18.00`) and has at least 2 sentences.
5. Every price in `session["search_results"]` is `<= parsed["max_price"]`. The query was chosen so the ceiling does something: without it, `vintage tee` returns ten listings from $12 to $45; with `under $20` it returns eight, the highest of them exactly $20.

**Real output from one try per criterion**, from `results/run_2026-10-13_1553_before.md`:

**Criterion 1** — try 1, `agent.py::run_agent` calling `tools.py::suggest_outfit` and `tools.py::create_fit_card`:

```
[1] parse_query
      in:  vintage graphic tee under $30
      out: description='vintage graphic tee', size=None, max_price=30.0
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] select_item
      in:  10 search results
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    first result, id=lst_002
[4] suggest_outfit
      in:  item id=lst_002, wardrobe items=10
      out: Here are two quick ways to style that butterfly tee with what you already own:  **1. 2000s Streetwear** *   **…
[5] create_fit_card
      in:  outfit (648 chars), item id=lst_002
      out: Found this absolute dream of a butterfly print baby tee scrolling on depop for just $18.00 and I am NEVER taki…
```

**Criterion 2** — try 1, `agent.py::run_agent`, the branch at the empty search result:

```
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: description='designer ballgown', size='XXS', max_price=5.0
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    branch: empty, stopping

session["error"]: No listings matched. I read your query as looking for 'designer ballgown', size XXS, under $5.00. Try a broader description, a different size, or raising the price.
```

**Criterion 3** — try 1, `agent.py::run_agent`, the two trace lines the check compares:

```
[3] select_item
      in:  7 search results
      out: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
      →    first result, id=lst_007
[4] suggest_outfit
      in:  item id=lst_007, wardrobe items=10
```

**Criterion 4** — all five fit cards for the same item (`tools.py::create_fit_card`, Y2K Baby Tee, $18.00, depop):

```
1. Found this absolute dream of a butterfly print baby tee scrolling on depop for just $18.00 and I’m literally never taking it off! It’s giving major 2000s mall-rat energy, whether you throw it on with baggy dark-wash denim and chunky sneaks or dress it down with wide-leg khakis and stompy combat boots. Run, don't walk, to grab this before I change my mind and keep it for myself! 🦋✨
2. Okay I am literally obsessed with this Y2K baby tee with the cutest little butterfly print I just snagged on depop for only $18.00! It’s giving major early 2000s pop star off-duty, and I can't wait to style it with baggy jeans and chunky sneakers or dress it down with some wide-leg khakis and combat boots. Grab it before I change my mind and keep it forever!! 🦋✨
3. Absolute literal scream when I scored this Y2K butterfly baby tee on depop for just $18.00! It’s giving major early-2000s pop star energy, and I’m so obsessed I might actually cry. Honestly can't wait to balance out the tiny fit with some baggy jeans and chunky sneaks this weekend. ✨🦋
4. Still screaming that I manifested this exact butterfly baby tee for just $18.00 on depop! It’s giving ultimate Y2K pop star off-duty, whether I'm leaning into baggy dark denim and chunky sneaks or dressing it down with wide-leg khakis and combat boots. Run, don't walk, to my shop before I change my mind and keep it forever!
5. Okay but I am losing my mind over this literal Y2K butterfly baby tee I just hunted down for only $18.00! The nostalgia hits so hard, and I’m already planning to throw it on with baggy jeans and my beat-up sneakers for that ultimate off-duty look. Snagged this beauty on depop and honestly, I might never take it off.
```

**Criterion 5** — try 1 of `vintage tee under $20`, `tools.py::search_listings` (reached through `mcp_server.py`):

```
- parsed: {'description': 'vintage tee', 'size': None, 'max_price': 20.0}
- search_result prices: [18.0, 19.0, 20.0, 12.0, 15.0, 16.0, 18.0, 14.0]
```

All five criteria were met on the first run, so there is no miss to diagnose yet.
That is a fact about these criteria as much as about the agent — see the
verdicts section.

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
$ python app.py ask 'vintage graphic tee under $30' --trace
[1] parse_query
      in:  vintage graphic tee under $30
      out: description='vintage graphic tee', size=None, max_price=30.0
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] select_item
      in:  10 search results
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    first result, id=lst_002
[4] suggest_outfit
      in:  item id=lst_002, wardrobe items=10
      out: Here are two quick ways to style that butterfly tee with what you already own:  **1. 2000s Streetwear** Pair t…
[5] create_fit_card
      in:  outfit (562 chars), item id=lst_002
      out: I literally squealed when I scored this Y2K baby tee on depop for just $18.00! The butterfly print is *so* 200…
```

**Empty search**

```
$ python app.py ask 'designer ballgown size XXS under $5' --trace
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: description='designer ballgown', size='XXS', max_price=5.0
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    branch: empty, stopping
```

Five steps against two: the empty run stops at the branch and never reaches
`suggest_outfit` or `create_fit_card`. Step 3 of the happy path records
`id=lst_002` and step 4 receives `item id=lst_002` — the same id on both sides
of the session, which is what criterion 3 checks.

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



### Failure modes, triggered on purpose

**1. Empty search** — `python app.py ask 'designer ballgown size XXS under $5'`

```
  No listings matched. I read your query as looking for 'designer ballgown', size XXS, under $5.00. Try a broader description, a different size, or raising the price.
```

Already handled by the branch in `agent.py::run_agent`. Stops with zero model
calls and names the three things the user can change.

**2. Empty wardrobe** — `python app.py ask 'denim jacket under $50' --empty-wardrobe`

```
  Outfit:   Since this is your first piece, let's build around it. Here are two ways to style that cropped Wrangler jacket:
  **1. The 90s Streetwear Look** Pair the light wash with baggy black cargo pants or wide-leg carpenter denim. ...
```

Already handled by the empty-wardrobe branch in `tools.py::suggest_outfit`: it
returned general styling advice, not a crash and not an empty string. (This
answer came from the build cache, so it shows the output but not a fresh call.)

**3. Model unavailable** — a corrupted `GEMINI_API_KEY`, then a query I hadn't asked before.

Before the fix, `agent.py` had no handler, so `generate.ModelUnavailable`
travelled out of `run_agent` and was only caught by the catch-all in
`app.py::main`. The user saw a bare `ModelUnavailable: ...` line, the run
returned no session, and the item the search had already found was lost.

After the fix, `run_agent` catches it around the two model-backed tools
(`suggest_outfit`, `create_fit_card`), keeps the session, and sets
`session["error"]`:

```
$ python app.py ask 'oversized wool blazer under $60' --trace
[1] parse_query
      in:  oversized wool blazer under $60
      out: description='oversized wool blazer', size=None, max_price=60.0
[2] search_listings (via MCP)
      in:  {'description': 'oversized wool blazer', 'size': None, 'max_price': 60.0}
      out: 7 items: Oversized Flannel Shirt — Plaid Red/Black, Knit Cardigan — Chunky Brown, Oversized Crewneck Sweatshirt — Vintage Navy … +4 more
[3] select_item
      in:  7 search results
      out: Oversized Flannel Shirt — Plaid Red/Black ($22.0, thredUp)
      →    first result, id=lst_003
[4] model unavailable
      out: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.goo…
      →    stopping

  I found 'Oversized Flannel Shirt — Plaid Red/Black', but couldn't reach the model to style it. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
```

I set the bad key as an environment variable for that one command rather than
editing `.env` (`config.py` calls `load_dotenv` without `override`, so a variable
already in the environment wins). Same failure, and the real key was never
touched.


---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
