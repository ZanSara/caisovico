<?php session_start();
include "frontController.php";

$controller = new FrontController();
$controller->run();

?>
