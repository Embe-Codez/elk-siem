def traffic_query(day):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": f"now-{day}d/d",
                                "lt": f"now-{day-1}d/d"
                            }
                        }
                    },
                    {
                        "term": {
                            "event.action": "allowed"
                        }
                    }
                ]
            }
        }
    }
    return query