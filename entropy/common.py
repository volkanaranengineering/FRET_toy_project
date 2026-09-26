"""Exact finite enumeration of a deliberately small FRET formula subset.

This is a companion analyzer, not the NASA FRET engine or an unbounded proof.
Unsupported syntax fails closed. Truth vectors are bounded semantic signatures.
"""
from pathlib import Path
from itertools import product
from functools import lru_cache
import hashlib
import json
import math
import re

ROOT = Path(__file__).resolve().parent


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n', encoding='utf-8', newline='\n')


def entropy(probabilities):
    ps = list(probabilities)
    if not ps or any(not math.isfinite(p) or p < 0 for p in ps) or not math.isclose(sum(ps), 1, abs_tol=1e-10):
        raise ValueError('Probabilities must be finite, nonnegative and sum to one.')
    return -math.fsum(p * math.log2(p) for p in ps if p > 0)


class Formula:
    """Parser for Boolean, strong X, bounded F, and finite release V."""
    def __init__(self, source):
        pattern = r'\s*(->|F\[\d+,\d+\]|[()!&|]|[A-Za-z_][A-Za-z_0-9]*)'
        self.tokens = []
        pos = 0
        while pos < len(source.rstrip()):
            m = re.match(pattern, source[pos:])
            if not m:
                raise ValueError('Unsupported formula syntax: ' + source[pos:])
            self.tokens.append(m.group(1)); pos += m.end()
        self.i = 0
        self.ast = self.expression(0)
        if self.i != len(self.tokens):
            raise ValueError('Unconsumed formula tokens')

    def expression(self, level):
        precedence = {'->': 1, '|': 2, '&': 3, 'V': 4}
        if self.i >= len(self.tokens):
            raise ValueError('Unexpected end of formula')
        token = self.tokens[self.i]; self.i += 1
        if token == '(':
            left = self.expression(0)
            if self.i >= len(self.tokens) or self.tokens[self.i] != ')':
                raise ValueError('Missing closing parenthesis')
            self.i += 1
        elif token in ('!', 'X') or token.startswith('F['):
            left = (token, self.expression(5))
        elif token in ('request', 'response', 'LAST', 'TRUE', 'FALSE'):
            left = (token,)
        else:
            raise ValueError('Unsupported atom/operator: ' + token)
        while self.i < len(self.tokens):
            op = self.tokens[self.i]
            prec = precedence.get(op, -1)
            if prec < level:
                break
            self.i += 1
            right = self.expression(prec if op == '->' else prec + 1)
            left = (op, left, right)
        return left

    def evaluate(self, trace):
        if not trace:
            raise ValueError('Empty traces are outside this experiment')
        n = len(trace)

        @lru_cache(None)
        def ev(node, i):
            op = node[0]
            if op == 'request': return trace[i][0]
            if op == 'response': return trace[i][1]
            if op == 'LAST': return i == n - 1
            if op == 'TRUE': return True
            if op == 'FALSE': return False
            if op == '!': return not ev(node[1], i)
            if op == '&': return ev(node[1], i) and ev(node[2], i)
            if op == '|': return ev(node[1], i) or ev(node[2], i)
            if op == '->': return not ev(node[1], i) or ev(node[2], i)
            if op == 'X': return i + 1 < n and ev(node[1], i + 1)
            if op.startswith('F['):
                lo, hi = map(int, op[2:-1].split(','))
                if lo > hi: raise ValueError('Reversed temporal bounds')
                return any(ev(node[1], j) for j in range(i + lo, min(i + hi + 1, n)))
            if op == 'V':
                return ev(node[2], i) and (ev(node[1], i) or i == n - 1 or ev(node, i + 1))
            raise ValueError(op)
        return bool(ev(self.ast, 0))


def reference(trace, trigger, deadline):
    """Independent obligation-based reading of the FRET English description."""
    return all(
        any(trace[j][1] for j in range(i, min(len(trace), i + deadline + 1)))
        or len(trace) - 1 < i + deadline
        for i, (request, _) in enumerate(trace)
        if request and (trigger == 'holding' or i == 0 or not trace[i - 1][0])
    )


def load(horizon=6):
    if not isinstance(horizon, int) or not 1 <= horizon <= 8:
        raise ValueError('Exact enumeration supports horizons 1..8')
    config = json.loads((ROOT / 'inputs/analysis.json').read_text(encoding='utf-8'))
    project_path = ROOT / 'inputs/fret-project.json'
    rows = json.loads(project_path.read_text(encoding='utf-8'))['requirements']
    traces = list(product(((False, False), (False, True), (True, False), (True, True)), repeat=horizon))
    formulas = {r['reqid']: Formula(r['semantics']['ftExpanded']) for r in rows}
    vectors = {key: bytes(formula.evaluate(t) for t in traces) for key, formula in formulas.items()}
    meta = {'horizon': horizon, 'trace_count': len(traces), 'variables': ['request', 'response'],
            'domain': 'Boolean', 'distribution': 'uniform over all fixed-length Boolean traces',
            'environment_assumptions': [], 'tick_duration': 'unspecified; discrete steps only',
            'semantics': 'FRET ftExpanded finite semantics, including weak unfinished deadlines',
            'scope': 'exact at this horizon only; no unbounded equivalence or realizability claim',
            'project_sha256': hashlib.sha256(project_path.read_bytes()).hexdigest(),
            'compiler_sha256': config['compiler_sha256']}
    return config, rows, traces, vectors, meta


def group(candidates, vectors):
    entropy(c['prior'] for c in candidates)
    classes = {}
    for c in candidates:
        signature = vectors[c['id']]
        item = classes.setdefault(signature, {'members': [], 'probability': 0.0})
        item['members'].append(c['id']); item['probability'] += c['prior']
    entropy([c['probability'] for c in classes.values()])
    return list(classes.values())


def trace_json(trace):
    return [{'tick': i, 'request': bool(a), 'response': bool(b)} for i, (a, b) in enumerate(trace)]
