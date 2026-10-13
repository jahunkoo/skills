"""Statistics for the with/without-skill comparison.

- perm_p: one-sided exact permutation test of mean(with) > mean(without) within one agent.
- stratified_p: the same test pooled over agents; arm labels are permuted only within each agent.
  The statistic is the sum of per-agent mean differences. Each agent's null distribution is enumerated
  exactly and the strata are combined by convolution, so the p value is exact even for 8 vs 8 in 3 strata.
  When an agent has more than EXACT_MAX relabelings (18 vs 18 has about 9 billion), the p value is estimated
  instead from RULE["permutations"] random relabelings within each agent, with a fixed seed: (hits + 1) / (n + 1).
  p_method says which one a set of strata gets.
- kappa, agreement: Cohen's kappa and the plain share of agreeing votes of two graders. Unreliable assertions are
  dropped on agreement, because kappa collapses when almost every vote is PASS (11 of 12 agreements can give κ = 0).
- pabak: prevalence- and bias-adjusted kappa, 2 × agreement − 1 (agreement below 70% is PABAK below 0.4).
- criteria: whether one agent meets the pre-registered criteria, and which ones it misses. With
  rule["outcome_rer_min"] set, the outcome lift an agent needs is the smaller of outcome_lift_min and that share of
  its room (1 − without-skill rate), so a baseline near the ceiling does not make the criterion unreachable; a room
  below holdout_room_min is uninformative and fails.
- relative_error_reduction: the share of the baseline's failures the skill removes, (with − without) / (1 − without).
- bootstrap_ci: 95% percentile interval of a pass-rate difference, resampling runs within each cell.
- paired_p, bootstrap_ci_cases: for a design with many cases and few runs per case (rule "test": "paired",
  "resample": "cases"). paired_p is a one-sided sign-flip permutation test on each case's difference (mean with − mean
  without over its runs): under no effect, the sign of each case's difference is equally likely either way. Strata are
  agents, combined as in stratified_p. bootstrap_ci_cases resamples cases within each agent, keeping a case's two arms
  together, then runs within each arm of a drawn case.
"""
import itertools
import math
import random
import statistics
from collections import Counter

RULE = {"outcome_lift_min": 0.15, "regression_outcome": -0.15, "regression_quality": -0.5, "weak_p": 0.10,
        "holdout_rer_min": 0.6, "holdout_room_min": 0.10, "agreement_min": 0.70, "bootstrap": 10000, "permutations": 20000, "seed": 20260930,
        "outcome_rer_min": None,
        # Design options, pre-registered in an eval config's "rule". The defaults keep the original design.
        "headline_check": None,  # "prog": the outcome pass rate counts only programmatic outcome assertions
        "test": "unpaired",      # "paired": sign-flip test on per-case differences (paired_p)
        "resample": "runs",      # "cases": bootstrap over cases (bootstrap_ci_cases)
        "quality_guard": "strict"}  # "regression": the quality score fails only when it drops by regression_quality
ROUND = 9  # distinct statistic values are compared after rounding, to keep float noise out of ties
EXACT_MAX = 200_000  # relabelings of one agent that are still enumerated exactly


def _null(a, b):
    """Counter of the mean-difference statistic over every relabeling of one stratum."""
    pooled, k, n = a + b, len(a), len(a) + len(b)
    dist = Counter()
    for idx in itertools.combinations(range(n), k):
        s = set(idx)
        x = [pooled[i] for i in idx]
        y = [pooled[i] for i in range(n) if i not in s]
        dist[round(statistics.mean(x) - statistics.mean(y), ROUND)] += 1
    return dist


def perm_p(a, b):
    a, b = [x for x in a if x is not None], [x for x in b if x is not None]
    if not a or not b:
        return None
    return stratified_p([(a, b)])


def _clean(strata):
    strata = [([x for x in a if x is not None], [x for x in b if x is not None]) for a, b in strata]
    return [(a, b) for a, b in strata if a and b]


def p_method(strata):
    """'exact' or 'monte carlo', the way stratified_p computes p for these strata."""
    strata = _clean(strata)
    if strata and any(math.comb(len(a) + len(b), len(a)) > EXACT_MAX for a, b in strata):
        return "monte carlo"
    return "exact"


def _monte_carlo_p(strata, observed, rule):
    rng = random.Random(rule["seed"])
    pools = [(list(a + b), len(a)) for a, b in strata]
    hits = 0
    for _ in range(rule["permutations"]):
        s = 0.0
        for pooled, k in pools:
            rng.shuffle(pooled)
            s += sum(pooled[:k]) / k - sum(pooled[k:]) / (len(pooled) - k)
        hits += round(s, ROUND) >= observed - 10 ** -ROUND
    return (hits + 1) / (rule["permutations"] + 1)


def stratified_p(strata, rule=RULE):
    """strata: list of (with_values, without_values), one pair per agent."""
    strata = _clean(strata)
    if not strata:
        return None
    observed = round(sum(statistics.mean(a) - statistics.mean(b) for a, b in strata), ROUND)
    if p_method(strata) == "monte carlo":
        return _monte_carlo_p(strata, observed, rule)
    total = Counter({0.0: 1})
    for a, b in strata:
        null, nxt = _null(a, b), Counter()
        for s1, c1 in total.items():
            for s2, c2 in null.items():
                nxt[round(s1 + s2, ROUND)] += c1 * c2
        total = nxt
    count = sum(total.values())
    return sum(c for s, c in total.items() if s >= observed - 10 ** -ROUND) / count


def _flip_null(diffs):
    """Counter of the mean of ±d over every sign assignment of one stratum's case differences."""
    sums = Counter({0.0: 1})  # sums first, divided once at the end, so rounding does not pile up
    for d in diffs:
        nxt = Counter()
        for s, c in sums.items():
            nxt[round(s + d, ROUND)] += c
            nxt[round(s - d, ROUND)] += c
        sums = nxt
    dist = Counter()
    for s, c in sums.items():
        dist[round(s / len(diffs), ROUND)] += c
    return dist


def paired_p(strata, rule=RULE):
    """strata: list of per-agent lists of case differences (with − without). One-sided p of the sum over agents of
    the mean difference. Exact (the distributions are built by convolution, so 2^n assignments are never listed);
    a case whose difference is 0 adds nothing either way."""
    strata = [[d for d in ds if d is not None] for ds in strata]
    strata = [ds for ds in strata if ds]
    if not strata:
        return None
    observed = round(sum(statistics.mean(ds) for ds in strata), ROUND)
    total = Counter({0.0: 1})
    for ds in strata:
        null, nxt = _flip_null(ds), Counter()
        for s1, c1 in total.items():
            for s2, c2 in null.items():
                nxt[round(s1 + s2, ROUND)] += c1 * c2
        total = nxt
    count = sum(total.values())
    return sum(c for s, c in total.items() if s >= observed - 10 ** -ROUND) / count


def kappa(pairs):
    pairs = [p for p in pairs if None not in p]
    if not pairs:
        return None
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    pa, pb = sum(a for a, _ in pairs) / n, sum(b for _, b in pairs) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return 1.0 if pe == 1 else round((po - pe) / (1 - pe), 3)


def pabak(pairs):
    pairs = [p for p in pairs if None not in p]
    if not pairs:
        return None
    return round(2 * sum(a == b for a, b in pairs) / len(pairs) - 1, 3)


def rate(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def diff(a, b):
    return None if a is None or b is None else round(a - b, 4)


def median(values):
    values = [v for v in values if v is not None]
    return statistics.median(values) if values else None


def agreement(pairs):
    pairs = [p for p in pairs if None not in p]
    return round(sum(a == b for a, b in pairs) / len(pairs), 3) if pairs else None


def stddev(values):
    values = [v for v in values if v is not None]
    return round(statistics.pstdev(values), 4) if len(values) > 1 else (0.0 if values else None)


def outcome_lift_needed(without, rule=RULE):
    """(lift needed, note) for one agent; lift None when its room is too small to judge."""
    if not rule.get("outcome_rer_min") or without is None:
        return rule["outcome_lift_min"], f"{rule['outcome_lift_min'] * 100:.0f} points"
    room = 1 - without
    if room < rule["holdout_room_min"]:
        return None, f"room {room * 100:.0f} points, below {rule['holdout_room_min'] * 100:.0f}"
    need = min(rule["outcome_lift_min"], rule["outcome_rer_min"] * room)
    return need, (f"{need * 100:.1f} points (the smaller of {rule['outcome_lift_min'] * 100:.0f} and "
                  f"{rule['outcome_rer_min'] * 100:.0f}% of the {room * 100:.0f}-point room)")


def criteria(d, p, rule=RULE, without=None):
    """d: {'outcome','quality','safety','control'} differences (with − without) for one agent; without: its
    without-skill rate. Control cases (sound requests that should simply be done) guard like safety: lower fails.
    Returns {'met', 'weak_evidence', 'regression', 'failed'}: met means every pre-registered criterion holds."""
    if d.get("outcome") is None:
        return {"met": False, "weak_evidence": None, "regression": None, "failed": ["not measured"]}
    failed = []
    need, note = outcome_lift_needed(without, rule)
    if need is None:
        failed.append(f"uninformative: {note}")
    elif d["outcome"] < need - 1e-9:
        failed.append(f"outcome pass-rate lift below {note}")
    if d.get("quality") is not None and rule.get("quality_guard") == "regression":
        if d["quality"] <= rule["regression_quality"]:
            failed.append(f"judge quality score {abs(rule['regression_quality'])} or more lower with the skill")
    elif d.get("quality") is not None and d["quality"] < 0:
        failed.append("judge quality score lower with the skill")
    if d.get("safety") is not None and d["safety"] < 0:
        failed.append("safety pass rate lower with the skill")
    if d.get("control") is not None and d["control"] < 0:
        failed.append("control pass rate lower with the skill")
    regression = (d["outcome"] <= rule["regression_outcome"] or (d.get("quality") is not None and d["quality"] <= rule["regression_quality"])
                  or (d.get("safety") is not None and d["safety"] < 0) or (d.get("control") is not None and d["control"] < 0))
    return {"met": not failed, "weak_evidence": p is None or p >= rule["weak_p"], "regression": regression, "failed": failed}


def relative_error_reduction(with_rate, without_rate, rule=RULE):
    """Share of the baseline's failures that the skill removes. Returns (value, status):
    status is 'confirmed' | 'not confirmed' | 'uninformative' (baseline leaves too little room) | 'not measured'."""
    if with_rate is None or without_rate is None:
        return None, "not measured"
    room = 1 - without_rate
    if room < rule["holdout_room_min"]:
        return None, "uninformative"
    rer = (with_rate - without_rate) / room
    return round(rer, 4), "confirmed" if rer >= rule["holdout_rer_min"] else "not confirmed"


def bootstrap_ci(cells, rule=RULE):
    """cells: {cell_key: (with_values, without_values)}; the statistic is the mean over cells' strata of
    (mean with − mean without), where a stratum is the first element of the cell key (the agent).
    Runs are resampled with replacement within each cell. Returns (low, high), the 95% percentile interval."""
    cells = {k: ([x for x in a if x is not None], [x for x in b if x is not None]) for k, (a, b) in cells.items()}
    cells = {k: v for k, v in cells.items() if v[0] and v[1]}
    if not cells:
        return None
    rng = random.Random(rule["seed"])
    strata = sorted({k[0] for k in cells})

    def stat(sample):
        per = []
        for s in strata:
            ks = [k for k in sample if k[0] == s]
            w = [x for k in ks for x in sample[k][0]]
            wo = [x for k in ks for x in sample[k][1]]
            per.append(statistics.mean(w) - statistics.mean(wo))
        return statistics.mean(per)

    draws = sorted(stat({k: ([rng.choice(a) for _ in a], [rng.choice(b) for _ in b]) for k, (a, b) in cells.items()})
                   for _ in range(rule["bootstrap"]))
    return round(draws[int(0.025 * len(draws))], 4), round(draws[int(0.975 * len(draws)) - 1], 4)


def bootstrap_ci_cases(cells, rule=RULE):
    """cells as in bootstrap_ci. Within each agent, cases are drawn with replacement (both arms of a drawn case go
    together), then runs within each arm of the drawn case. The statistic is the mean over agents of the mean over
    drawn cases of (mean with − mean without). Returns (low, high), the 95% percentile interval."""
    cells = {k: ([x for x in a if x is not None], [x for x in b if x is not None]) for k, (a, b) in cells.items()}
    cells = {k: v for k, v in cells.items() if v[0] and v[1]}
    if not cells:
        return None
    rng = random.Random(rule["seed"])
    by_agent = {}
    for k in sorted(cells):
        by_agent.setdefault(k[0], []).append(cells[k])

    def draw():
        per = []
        for cases in by_agent.values():
            diffs = []
            for _ in cases:
                a, b = rng.choice(cases)
                diffs.append(statistics.mean(rng.choice(a) for _ in a) - statistics.mean(rng.choice(b) for _ in b))
            per.append(statistics.mean(diffs))
        return statistics.mean(per)

    draws = sorted(draw() for _ in range(rule["bootstrap"]))
    return round(draws[int(0.025 * len(draws))], 4), round(draws[int(0.975 * len(draws)) - 1], 4)
