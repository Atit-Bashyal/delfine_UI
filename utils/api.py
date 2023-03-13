def getAPI(baseURL, type, plan, loc, date):
    # e.g. http://127.0.0.1:8000/fetch_forecast/wind/short_term/merkel/2019-02-22/
    if all(v is not None for v in [type, plan, loc, date]):  # Check that every element is not None
        return f"{baseURL}/fetch_forecast/{type}/{plan}/{loc}/{date}"
    else:
        return ""
