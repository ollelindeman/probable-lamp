# Security Improvements TODO

Identified during security review of `custom_components/sopor_nu`.

## L1 — URL-encode API-provided values in `sensor.py`

**File**: `custom_components/sopor_nu/sensor.py`

The `configuration_url` is constructed by embedding `station_id` and `municipality_code`
directly into an f-string without URL encoding. Values originate from the external API,
so a compromised or spoofed API endpoint could inject unexpected characters.

**Fix**: Use `urllib.parse.quote()` on both values:
```python
from urllib.parse import quote
configuration_url=f"https://www.sopor.nu/haer-aatervinner-du/hitta-aatervinningen/?avs={quote(str(station_id), safe='')}&kommun={quote(str(municipality_code), safe='')}"
```

---

## L2 — Add test coverage

No test files exist (`test_*.py`, `conftest.py`). Without tests, future changes could
silently break exception handling, remove input validation, disable timeouts, or
introduce blocking calls.

**Fix**: Add `pytest-homeassistant-custom-component` based tests covering:
- Malformed / unexpected JSON from the API
- HTTP 4xx and 5xx API responses
- Request timeout simulation
- Duplicate config entry prevention

---

## L3 — Pin an upper bound on `aiohttp` in `manifest.json`

`aiohttp>=3.8.0` accepts any future major release, including potentially breaking ones.

**Fix**: Constrain to a known-compatible range, e.g. `aiohttp>=3.8.0,<4.0`.
Re-evaluate when aiohttp 4.x stabilises.

---

## L4 — Explicitly handle non-JSON API responses in `api.py`

`resp.json()` is called without checking `Content-Type`. An HTML error page or
unexpected response format raises `aiohttp.ContentTypeError`, which is caught
upstream — but this is implicit rather than deliberate.

**Fix**: Pass `content_type=None` to suppress aiohttp's content-type check and
handle the resulting `ValueError` / `json.JSONDecodeError` explicitly, or check
`resp.content_type` before calling `.json()`.
