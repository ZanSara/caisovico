<!DOCTYPE html>
<html>
	<body style="font-family: 'Lucida Console', Monaco, monospace">
		<?php
			spl_autoload_register(function($controllerName) {
				if(file_exists("controller/" . $controllerName . ".php")) {
					include "controller/" . $controllerName . ".php";
				} else if(file_exists("model/" . $controllerName . ".php")) {
					include "model/" . $controllerName . ".php";
				} else if(file_exists("view/" . $controllerName . ".php")) {
					include "view/" . $controllerName . ".php";
				} else if(file_exists("tests/" . $controllerName . ".php")) {
					include "tests/" . $controllerName . ".php";
				}
			});

			$test = new UserModelTest();
			$test->run();
			$test = new MapModelTest();
			$test->run();
			$test = new SuperregionModelTest();
			$test->run();
			$test = new AdminUserModelTest();
			$test->run();
		?>
	</body>
</html>