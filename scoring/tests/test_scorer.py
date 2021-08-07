#!/usr/bin/env python3

import unittest

import yaml

# Path hackery
import pathlib
import sys
ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from score import Scorer


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

    def test_single_claim_docking_area(self):
        self.assertScores({
            'ABC': 1,
            'DEF': 0,
        }, [
            {
                'zone': 0,
                'token_index': 42,
                'location': 'docking_area',
                'time': 4.432,
            },
        ])

    def test_single_claim_raised_area(self):
        self.assertScores({
            'ABC': 3,
            'DEF': 0,
        }, [
            {
                'zone': 0,
                'token_index': 42,
                'location': 'zone_0_raised_area',
                'time': 4.432,
            },
        ])

    def test_single_claim_wrong_raised_area(self):
        self.assertScores({
            'ABC': 0,
            'DEF': 0,
        }, [
            {
                'zone': 0,
                'token_index': 42,
                'location': 'zone_1_raised_area',
                'time': 4.432,
            },
        ])

    def test_moved_back_to_arena(self):
        self.assertScores({
            'ABC': 0,
            'DEF': 0,
        }, [
            {
                'zone': 0,
                'token_index': 42,
                'location': 'zone_1_raised_area',
                'time': 4,
            },
            {
                'zone': 0,
                'token_index': 42,
                'location': 'arena',
                'time': 5,
            },
        ])

    def test_two_claims_same_area(self):
        self.assertScores({
            'ABC': 1,
            'DEF': 1,
        }, [
            {
                'zone': 0,
                'token_index': 42,
                'location': 'docking_area',
                'time': 4,
            },
            {
                'zone': 1,
                'token_index': 13,
                'location': 'docking_area',
                'time': 5,
            },
        ])

    def test_multiple_tokens(self):
        self.assertScores({
            'ABC': 4,
            'DEF': 1,
        }, [
            {
                'zone': 0,
                'token_index': 43,
                'location': 'docking_area',
                'time': 1,
            },
            {
                'zone': 0,
                'token_index': 42,
                'location': 'docking_area',
                'time': 4,
            },
            {
                'zone': 0,
                'token_index': 43,
                'location': 'zone_0_raised_area',
                'time': 5,
            },
            {
                'zone': 1,
                'token_index': 13,
                'location': 'docking_area',
                'time': 5,
            },
        ])


if __name__ == '__main__':
    unittest.main()
