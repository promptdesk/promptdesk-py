import json

def canonical_json_stringify(data):
    def replacer(obj):
        if isinstance(obj, dict):
            return {key: obj[key] for key in sorted(obj)}
        else:
            return obj

    return json.dumps(data, default=replacer, sort_keys=True)