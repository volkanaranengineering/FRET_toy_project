# HTTP HEAD — no body and optional correct Content-Length

## Sources
- output/pdf/research_revision_v3/artifact/http_case.py and paper.tex §119–121.
- RFC 9110 sections 9.3.2 and 8.6: https://www.rfc-editor.org/rfc/rfc9110.html

## Assumptions and unresolved inputs
- Snapshot is taken after a complete successful HTTP/1.1 response. Same stable resource and representation as paired GET; no compression, transfer coding, proxies or concurrent changes.
- Content-Length may be absent. A raw-socket recorder is needed to detect an illegal HEAD body.
- GET body correctness is a test-fixture control, not a newly attributed RFC requirement.

## Signals
- `head_complete`: bool: completed HEAD observation
- `head_bytes`: integer >=0: raw HEAD content octets
- `length_present`: bool: Content-Length present
- `head_length`: integer >=0 when present: parsed field value
- `get_bytes`: integer >=0: paired GET content length

### HTTP-01

whenever head_complete the HttpServer shall immediately satisfy (head_bytes = 0)

HEAD response has no content.

FRET infinite-trace formula:

```text
(G (head_complete -> (head_bytes = 0)))
```

### HTTP-02

whenever (head_complete & length_present) the HttpServer shall immediately satisfy (head_length = get_bytes)

If present, Content-Length matches the corresponding GET.

FRET infinite-trace formula:

```text
(G ((head_complete & length_present) -> (head_length = get_bytes)))
```
