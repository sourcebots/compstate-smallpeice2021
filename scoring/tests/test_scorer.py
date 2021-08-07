#!/usr/bin/env python3

import unittest

import yaml

# Path hackery
import pathlib
import sys
ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from score import MaximumExtentScorer as Scorer


class ScorerTests(unittest.TestCase):
    longMessage = True

    def construct_scorer(self, token_claims):
        return Scorer(
            self.teams_data,
            {'other': {'token_claims': token_claims}},
        )

    def assertScores(self, expected_scores, token_claims):
        scorer = self.construct_scorer(token_claims)
        actual_scores = scorer.calculate_scores()

        self.assertEqual(expected_scores, actual_scores, "Wrong scores")

    def setUp(self):
        self.teams_data = {
            'ABC': {'zone': 0},
            'DEF': {'zone': 1},
        }

    def test_template(self):
        template_path = ROOT / 'template.yaml'
        with template_path.open() as f:
            data = yaml.load(f)

        teams_data = data['teams']
        arena_data = data.get('arena_zones')
        extra_data = data.get('other')

        scorer = Scorer(teams_data, arena_data)
        scores = scorer.calculate_scores()

        self.assertEqual(
            teams_data.keys(),
            scores.keys(),
            "Should return score values for every team",
        )

    def test_no_actions(self):
        self.assertScores({
            'ABC': 0,
            'DEF': 0,
        }, [])


if __name__ == '__main__':
    unittest.main()
