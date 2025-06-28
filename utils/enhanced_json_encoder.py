from dataclasses import asdict
from datetime import datetime
import json


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if hasattr(o, "__dataclass_fields__"):
            return asdict(o)
        return super().default(o)

