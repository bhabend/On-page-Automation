def score_page(data):
    score = 100

    if data["Title"] == "Missing" or not (50 <= len(data["Title"]) <= 60):
        score -= 10
    if data["Meta Description"] == "Missing":
        score -= 10
    if data["H Tags"]["H1"] == [] or len(data["H Tags"]["H1"]) > 1:
        score -= 10
    if data["Missing Alts"] > 0:
        score -= 5
    if data["Performance Score"] != "Error" and data["Performance Score"] < 80:
        score -= 10

    return score
