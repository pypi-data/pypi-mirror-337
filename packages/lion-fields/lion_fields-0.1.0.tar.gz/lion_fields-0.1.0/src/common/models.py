from __future__ import annotations

import hashlib

from pydantic import BaseModel, ConfigDict


class HashableModel(BaseModel):
    """a hashable frozen pydantic model"""

    model_config = ConfigDict(frozen=True, use_enum_values=True)

    def __hash__(self):
        json_str = self.model_dump_json(exclude_unset=True)
        return int(hashlib.md5(json_str.encode("utf-8")).hexdigest(), 16)
