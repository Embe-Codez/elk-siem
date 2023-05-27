query = {
    "query": {
        "bool": {
            "must": [
                {
                    "range": {
                        "@timestamp": {
                            "gte": "now-{}d/d".format(day),
                            "lt": "now-{}d/d".format(day - 1)
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