def getAPI(baseURL, type, plan, loc, date):
    if all(v is not None for v in [type, plan, loc, date]):  # Check that every element is not None
        return f"{baseURL}/{type}/{plan}/{loc}/{date}"
    else:
        return None
