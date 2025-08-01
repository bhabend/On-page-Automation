def audit_seo_rules(data):
    issues = []
    score = 100

    # Title check
    title = data.get('title', '')
    if not title:
        issues.append("❌ Missing title tag.")
        score -= 10
    elif not (50 <= len(title) <= 60):
        issues.append(f"⚠️ Title length is {len(title)} characters.")
        score -= 5

    # Meta description check
    meta = data.get('meta_description', '')
    if not meta:
        issues.append("❌ Missing meta description.")
        score -= 10

    # H1 tag check
    h1s = data.get('h1', [])
    if len(h1s) == 0:
        issues.append("❌ No H1 tag found.")
        score -= 10
    elif len(h1s) > 1:
        issues.append(f"⚠️ Multiple H1 tags found ({len(h1s)}).")
        score -= 5

    # Canonical tag check
    if not data.get('canonical'):
        issues.append("⚠️ No canonical tag found.")
        score -= 5

    # Alt tag check
    if data.get('images_missing_alt', 0) > 0:
        issues.append(f"⚠️ {data['images_missing_alt']} images missing alt attributes.")
        score -= 5

    # Robots tag
    if not data.get('robots'):
        issues.append("⚠️ No meta robots tag found.")

    # Score bounds
    if score < 0:
        score = 0

    return score, issues
