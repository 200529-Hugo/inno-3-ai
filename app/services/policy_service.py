from typing import Any

from app.config import POLICIES


class PolicyService:
    @staticmethod
    def get(provision: str) -> dict[str, Any] | None:
        return POLICIES.get(provision)
