DATA = {
    # Location -> (Owner, Points if owner matches)
    'arena':              (None, 0),
    'docking_area':       (None, 1),
    'zone_0_raised_area': (0,    3),
    'zone_1_raised_area': (1,    3),
}


class Scorer:
    # Assumption: we will trust the *ordering* of the entries in the data we
    # are given and *ignore* the actual 'time' values. We defer handling of
    # equialent-time operations to the token controller.

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
        def points_for_location(owner, location):
            location_owner, points = DATA[location]
            if location_owner is None:
                # Shared area, everyone gets points
                return points
            if location_owner == owner:
                # Owner specific area which matches
                return points
            return 0

        # Mapping from token -> (owning zone, location)
        end_state = {
            claim['token_index']: (claim['zone'], claim['location'])
            for claim in self._token_claims
        }

        points_per_zone = {0: 0, 1: 0}
        for tok, (owner, location) in end_state.items():
            points_per_zone[owner] += points_for_location(owner, location)

        return {
            tla: points_per_zone[zone]
            for zone, tla in self._zone_to_tla.items()
        }


if __name__ == '__main__':
    import libproton
    libproton.main(Scorer)
