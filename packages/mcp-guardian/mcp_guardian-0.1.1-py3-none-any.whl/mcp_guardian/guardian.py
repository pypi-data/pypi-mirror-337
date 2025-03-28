import json
import re
import httpx
from datetime import datetime
from typing import Any, Set, Optional, Dict, Union

class MCPGuardian:
    """
    MCPGuardian performs security checks (auth, rate-limit, WAF scanning)
    and logs requests/responses. It does NOT call the tool function itself;
    that is handled by the runner. Instead, it returns whether the call is OK
    or not, plus any error messages or logs.
    """

    def __init__(
        self,
        valid_tokens: Optional[Set[str]] = None,
        logfile_path: str = "mcp_guardian.log",
        remote_log_url: Optional[str] = None,
        max_requests_per_token: int = 5
    ):
        """
        Args:
            valid_tokens: A set of allowed tokens for demonstration
            logfile_path: Local file path for logging
            remote_log_url: If provided, attempts to POST logs to this endpoint
            max_requests_per_token: Simple rate limit threshold
        """
        self.valid_tokens = valid_tokens or {"mysecrettoken123"}
        self.logfile_path = logfile_path
        self.remote_log_url = remote_log_url
        self.max_requests_per_token = max_requests_per_token

        self.usage_counts: Dict[str, int] = {}  # track usage per token

    def check_and_log(
        self,
        tool_name: str,
        kwargs: Dict[str, Any]
    ) -> Union[str, None]:
        """
        Main security check method.
        Returns None if call is allowed, or a string error if blocked.
        
        Steps:
         1) Validate token
         2) Rate-limiting
         3) WAF scanning
         4) Log request
        """
        # 1. Extract token
        token = kwargs.pop("token", None)

        # 2. Validate token
        if not self._validate_token(token):
            msg = "Unauthorized (invalid token)."
            self._log_event(f"REJECT AUTH | tool={tool_name} | reason={msg}")
            return msg

        # 3. Rate limit
        if self._is_rate_limited(token):
            msg = "Too Many Requests (rate-limited)."
            self._log_event(f"REJECT RATE | tool={tool_name} | token={token}")
            return msg

        # 4. WAF scanning
        if self._waf_scan_request(tool_name, kwargs):
            msg = "Request blocked by WAF scanning."
            self._log_event(f"REJECT WAF | tool={tool_name} | token={token} | args={kwargs}")
            return msg

        # 5. Log the request
        self._log_event(f"INVOKE | tool={tool_name} | token={token} | args={kwargs}")

        # If none of the checks failed, put the token back into kwargs
        # so the tool function can see it if needed (optional).
        kwargs["token"] = token
        return None

    def log_response(self, tool_name: str, token: str, response: Any):
        """Log the response from the tool call."""
        self._log_event(f"RESPONSE | tool={tool_name} | token={token} | resp={response}")

    # ----------------------
    # Internal Helpers
    # ----------------------
    def _validate_token(self, token: str) -> bool:
        return token in self.valid_tokens

    def _is_rate_limited(self, token: str) -> bool:
        current_count = self.usage_counts.get(token, 0)
        if current_count >= self.max_requests_per_token:
            return True
        self.usage_counts[token] = current_count + 1
        return False

    def _waf_scan_request(self, tool_name: str, kwargs: dict) -> bool:
        payload_str = tool_name + " " + json.dumps(kwargs)
        suspicious_patterns = [
            r"(drop\s+table)",
            r"(<script>)",
            r"(rm\s+-rf)",
            r"(;--)"
        ]
        for pattern in suspicious_patterns:
            if re.search(pattern, payload_str, flags=re.IGNORECASE):
                return True
        return False

    def _log_event(self, message: str):
        # Log to a local file
        timestamp = datetime.utcnow().isoformat()
        entry = f"[{timestamp}] {message}\n"
        if self.logfile_path:
            with open(self.logfile_path, "a", encoding="utf-8") as f:
                f.write(entry)

        # Optionally log to remote endpoint
        if self.remote_log_url:
            try:
                data = {"timestamp": timestamp, "log": message}
                httpx.post(self.remote_log_url, json=data, timeout=5.0)
            except Exception:
                pass
