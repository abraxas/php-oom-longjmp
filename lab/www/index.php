<?php
header('Content-Type: text/plain; charset=UTF-8');
header('X-Lab-Marker: CVE-2026-109618');
echo 'CVE-2026-109618-ALIVE'
    . ' php=' . PHP_VERSION
    . ' sapi=' . PHP_SAPI
    . ' memory_limit=' . ini_get('memory_limit')
    . ' peak=' . memory_get_peak_usage(true)
    . ' files=' . (string) count($_FILES)
    . ' post=' . (string) count($_POST)
    . ' cl=' . (string) ($_SERVER['CONTENT_LENGTH'] ?? 'none')
    . "\n";
