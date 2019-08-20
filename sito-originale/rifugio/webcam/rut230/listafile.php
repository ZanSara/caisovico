<?php
function dir_list($directory = FALSE) {
  $dirs= array();
  $files = array();
  if ($handle = opendir("./" . $directory))
  {
    while ($file = readdir($handle))
    {
      if (is_dir("./{$directory}/{$file}"))
      {
        if ($file != "." & $file != "..") $dirs[] = $file;
      }
      else
      {
        if ($file != "." & $file != "..") $files[] = $file;
      }
    }
  }
  closedir($handle);

  reset($dirs);
  sort($dirs);
  reset($dirs);

  reset($files);
  sort($files);
  reset($files);

  echo "<strong>Cartelle:</strong>\n<ul>";
  while(list($key, $value) = each($dirs))
  {
    $d++;
    echo "<li><a href=\"{$value}\">{$value}/</a>\n";
  }
  echo "</ul>\n";
  echo "<strong>Files:</strong>\n<ul>";
  while(list($key, $value) = each($files))
  {
    $f++;
    echo "<li><a href=\"{$directory}{$value}\">{$value}</a>\n";
  }
  echo "</ul>\n";
  if (!$d) $d = "0";
  if (!$f) $f = "0";
  echo "Sono presenti <strong>{$d}</strong> cartelle e <strong>{$f}</strong> file(s).</strong>\n";
}
dir_list("./");
?>
