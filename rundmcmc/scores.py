import numpy


def mean_median(partition, proportion_column_name):
    data = list(partition[proportion_column_name].values())
    return numpy.mean(data) - numpy.median(data)


def mean_thirdian(partition, proportion_column_name):
    data = list(partition[proportion_column_name].values())
    return numpy.mean(data) - numpy.percentile(data, 33)


def normalized_efficiency_gap(partition, proportion_column_name):
    """Right now this is the turnout-normalized version (just `2t-s`)."""
    vote_shares_by_district = list(partition[proportion_column_name].values())
    seats = len([votes for votes in vote_shares_by_district if votes > 0])
    seats_share = seats / len(vote_shares_by_district)
    total_vote_share = numpy.mean(vote_shares_by_district)
    return 2 * total_vote_share - seats_share


def efficiency_gap(partition, col1='PR_DV08', col2='PR_RV08'):
    party1 = partition[col1]
    party2 = partition[col2]
    wasted_votes_by_part = {part: wasted_votes(party1[part], party2[part])
                            for part in party1}
    total_votes = sum(party1.values()) + sum(party2.values())
    numerator = sum(waste1 - waste2 for waste1, waste2 in wasted_votes_by_part.values())
    return numerator / total_votes


def wasted_votes(party1_votes, party2_votes):
    total_votes = party1_votes + party2_votes
    if party1_votes > party2_votes:
        party1_waste = party1_votes - total_votes / 2
        party2_waste = party2_votes
    else:
        party2_waste = party2_votes - total_votes / 2
        party1_waste = party1_votes
    return party1_waste, party2_waste


def final_report():
    with open('../tests/test_run.txt') as f:
        f = f.read()
        print(f)