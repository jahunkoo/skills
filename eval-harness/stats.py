"""Statistics for the with/without-skill comparison.

- perm_p: one-sided exact permutation test of mean(with) > mean(without) within one agent.
- stratified_p: the same test pooled over agents; arm labels are permuted only within each agent.
  The statistic is the sum of per-agent mean differences. Each agent's null distribution is enumerated
  exactly and the strata are combined by convolution, so the p value is exact even for 8 vs 8 in 3 strata.
- kappa, agreement: Cohen's kappa and the plain share of agreeing votes of two graders. Unreliable assertions are
  dropped on agreement, because kappa collapses when almost every vote is PASS (11 of 12 agreements can give κ = 0).
- pabak: prevalence- and bias-adjusted kappa, 2 × agreement − 1 (agreement below 70% is PABAK below 0.4).
- criteria: whether one agent meets the pre-registered criteria, and which ones it misses.
- relative_error_reduction: the share of the baseline's failures the skill removes, (with − without) / (1 − without).
- bootstrap_ci: 95% percentile interval of a pass-rate difference, resampling runs within each cell.
"""
import itertools
import random
import statistics
from collections import Counter

RULE = {"outcome_lift_min": 0.15, "regression_outcome": -0.15, "regression_quality": -0.5, "weak_p": 0.10,
        "holdout_rer_min": 0.6, "holdout_room_min": 0.10, "agreement_min": 0.70, "bootstrap": 10000, "seed": 20260930}
ROUND = 9  # distinct statistic values are compared after rounding, to keep float noise out of ties


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


def stratified_p(strata):
    """strata: list of (with_values, without_values), one pair per agent."""
    strata = [([x for x in a if x is not None], [x for x in b if x is not None]) for a, b in strata]
    strata = [(a, b) for a, b in strata if a and b]
    if not strata:
        return None
    observed = round(sum(statistics.mean(a) - statistics.mean(b) for a, b in strata), ROUND)
    total = Counter({0.0: 1})
    for a, b in strata:
        null, nxt = _null(a, b), Counter()
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


def criteria(d, p, rule=RULE):
    """d: {'outcome','quality','safety'} differences (with − without) for one agent.
    Returns {'met', 'weak_evidence', 'regression', 'failed'}: met means every pre-registered criterion holds."""
    if d.get("outcome") is None:
        return {"met": False, "weak_evidence": None, "regression": None, "failed": ["not measured"]}
    failed = []
    if d["outcome"] < rule["outcome_lift_min"]:
        failed.append(f"outcome pass-rate lift below {rule['outcome_lift_min'] * 100:.0f} points")
    if d.get("quality") is not None and d["quality"] < 0:
        failed.append("judge quality score lower with the skill")
    if d.get("safety") is not None and d["safety"] < 0:
        failed.append("safety pass rate lower with the skill")
    regression = (d["outcome"] <= rule["regression_outcome"] or (d.get("quality") is not None and d["quality"] <= rule["regression_quality"])
                  or (d.get("safety") is not None and d["safety"] < 0))
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
