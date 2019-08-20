<?php

$file = strip_tags($_GET['file']);

Header("Content-type: application; name=".$file);
Header("Content-Disposition: attachment; filename=".$file);
Header("Content-Description: Download Manager");
Header("Pragma: No-Cache");
Header("Expires: 0");
Header("Content-Length:".filesize($file));
readfile($file);

?> 
