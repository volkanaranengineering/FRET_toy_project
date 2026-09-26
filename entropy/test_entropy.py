"""Independent finite-semantics cross-checks and scientific edge cases."""
import math
import unittest
from common import ROOT, Formula, entropy, group, load, reference, write_json
from run_all import module, DIRECTORIES


class EntropyTests(unittest.TestCase):
    comparisons = 0

    @classmethod
    def setUpClass(cls):
        cls.data = load(6)

    def test_generated_formula_against_obligation_oracle(self):
        checked = 0
        for h in range(1, 7):
            config, rows, traces, vectors, _ = self.data if h == 6 else load(h)
            for candidates in config['hypotheses'].values():
                for c in candidates:
                    expected = bytes(reference(t, c['trigger'], c['deadline']) for t in traces)
                    self.assertEqual(vectors[c['id']], expected, (h, c['id']))
                    checked += len(traces)
        EntropyTests.comparisons = checked

    def test_mass_preserving_alias(self):
        config, _, _, vectors, _ = self.data
        for cs in config['hypotheses'].values():
            collapsed = [dict(cs[0], prior=0.5), cs[2], cs[3]]
            a, b = group(cs, vectors), group(collapsed, vectors)
            self.assertEqual([c['probability'] for c in a], [c['probability'] for c in b])
            self.assertAlmostEqual(entropy(c['probability'] for c in a), 1.5)

    def test_probability_validation(self):
        for bad in ([], [0, 0], [-1, 2], [float('nan'), 1], [float('inf')], [0.2, 0.2]):
            with self.assertRaises(ValueError): entropy(bad)
        self.assertEqual(entropy([1, 0]), 0)

    def test_short_horizon_equivalence_is_not_global(self):
        config, _, _, vectors, _ = load(2)
        for cs in config['hypotheses'].values(): self.assertEqual(len(group(cs, vectors)), 1)
        for cs in self.data[0]['hypotheses'].values(): self.assertEqual(len(group(cs, self.data[3])), 3)

    def test_empty_and_unsupported_inputs(self):
        for text in ('G request', 'request + response', 'unknown', '(request', 'request response'):
            with self.assertRaises(ValueError): Formula(text)
        with self.assertRaises(ValueError): Formula('request').evaluate([])
        with self.assertRaises(ValueError): load(0)
        with self.assertRaises(ValueError): load(9)

    def test_finite_boundary_and_trigger_difference(self):
        self.assertTrue(reference([(True, False)] * 3, 'holding', 3))
        self.assertFalse(reference([(True, False)] * 4, 'holding', 3))
        trace = [(True, True)] + [(True, False)] * 4
        self.assertTrue(reference(trace, 'rising', 3))
        self.assertFalse(reference(trace, 'holding', 3))
        self.assertTrue(Formula('(! request) V response').evaluate([(True, True)]))
        self.assertFalse(Formula('X request').evaluate([(True, False)]))

    def test_constraint_information(self):
        behavior = module(DIRECTORIES[1])
        r = behavior.analyze(self.data)
        when, whenever = r['results']
        self.assertGreater(when['admissible_traces'], whenever['admissible_traces'])
        self.assertEqual(r['conjunction']['admissible_traces'], whenever['admissible_traces'])
        self.assertEqual(when['marginal_given_other']['information_bits'], 0)
        self.assertIsNone(behavior.measure(16, 0)['entropy_bits'])
        self.assertEqual(behavior.measure(16, 4)['information_bits'], 2)
        self.assertEqual(behavior.measure(0, 0)['status'], 'inconsistent context')

    def test_questions_and_posteriors(self):
        r = module(DIRECTORIES[2]).analyze(self.data)
        for row in r['results']:
            # REQ-002 candidates form an implication chain: no trace isolates
            # the middle, 0.5-probability meaning from both extremes.
            expected = 1 if row['reqid'] == 'REQ-001' else entropy([0.25, 0.75])
            self.assertAlmostEqual(row['questions'][0]['expected_information_gain_bits'], expected)
            for q in row['questions']:
                self.assertGreater(q['expected_information_gain_bits'], 0)
                self.assertLessEqual(q['expected_information_gain_bits'], 1 + 1e-12)
                for answer in ('yes', 'no'):
                    self.assertAlmostEqual(sum(q[answer]['posterior']), 1)
                trace = [(t['request'], t['response']) for t in q['trace']]
                rows = {r['reqid']: r for r in self.data[1]}
                flags = [Formula(rows[c['members'][0]]['semantics']['ftExpanded']).evaluate(trace) for c in row['classes']]
                self.assertEqual(flags, q['accepts_by_class'])


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(EntropyTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    write_json(ROOT / 'validation.json', {'status': 'PASS' if result.wasSuccessful() else 'FAIL',
               'test_methods': result.testsRun, 'formula_oracle_comparisons': EntropyTests.comparisons,
               'horizons_checked': [1, 2, 3, 4, 5, 6],
               'scope': 'Independent bounded obligation oracle vs generated FRET formula evaluator; mathematical edge cases. Not external model checking or user-study validation.'})
    raise SystemExit(0 if result.wasSuccessful() else 1)
