class Scorer:
    def __init__(self, teams_data, arena_data):
        pass

    def calculate_scores(self):
        raise NotImplementedError


if __name__ == '__main__':
    import libproton
    libproton.main(Scorer)
