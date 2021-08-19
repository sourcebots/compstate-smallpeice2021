import pprint

POINTS_FOR_LOCATION = {
    # Location -> get points callable
    'arena': lambda _: 0,
    'docking_area': lambda _: 1,
    'zone_0_raised_area': lambda token_owner: 3 if token_owner == 0 else 0,
    'zone_1_raised_area': lambda token_owner: 3 if token_owner == 1 else 0,
}


class Scorer:
    # Assumption: we will trust the *ordering* of the entries in the data we
    # are given and *ignore* the actual 'time' values. We defer handling of
    # equivalent-time operations to the token controller.

    def __init__(self, teams_data, arena_data):
        self._zone_to_tla = {
            info['zone']: tla
            for tla, info in teams_data.items()
        }

        # Token Claims look like this:
        # {
        #     'zone': 0 | 1,
        #     'token_index': int,
        #     'location': 'arena' | 'docking_area' | 'zone_0_raised_area' | 'zone_1_raised_area',
        #     'time': float,
        # }
        self._token_claims = arena_data['other']['token_claims']

    def calculate_scores(self):
        # Mapping from token -> (owning zone, location)
        end_state = {
            claim['token_index']: (claim['zone'], claim['location'])
            for claim in self._token_claims
        }
        pprint.pprint(end_state)

        last_claim = self._token_claims[-1]
        last_claim_time = last_claim['time']
        assert last_claim_time > 120, "Last claim before end of match"

        bad_claims = [
            x
            for x in self._token_claims
            if x['time'] == last_claim_time
        ]
        bad_claim_tokens = [x['token_index'] for x in bad_claims]
        pprint.pprint(bad_claims)

        tokens_set = set(end_state.keys())
        bad_tokens_set = set(bad_claim_tokens)
        missing = bad_tokens_set - tokens_set
        extra = tokens_set - bad_tokens_set
        assert not missing and not extra, f'{missing=}, {extra=}'

        print(f"Remove the last {len(bad_claims)}, they have timestamp {last_claim_time}")
        print()

        points_per_zone = {0: 0, 1: 0}
        for owner, location in end_state.values():
            points_per_zone[owner] += POINTS_FOR_LOCATION[location](owner)

        return {
            tla: points_per_zone[zone]
            for zone, tla in self._zone_to_tla.items()
        }


if __name__ == '__main__':
    import libproton
    libproton.main(Scorer)
