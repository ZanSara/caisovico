<?php 

include("config.php");

spl_autoload_register(function($controllerName) {
	if(file_exists("controller/" . $controllerName . ".php")) {
		include "controller/" . $controllerName . ".php";
	} else if(file_exists("model/" . $controllerName . ".php")) {
		include "model/" . $controllerName . ".php";
	} else if(file_exists("view/" . $controllerName . ".php")) {
		include "view/" . $controllerName . ".php";
	}
});

class FrontController {

	private $controller = DEFAULT_CONTROLLER;
	private $action = DEFAULT_ACTION;
	private $params = array();

	public function __construct() {
	    $this->parseUrl();
	}

	private function parseUrl() {
	    
	
		$path = trim(parse_url($_SERVER["REQUEST_URI"], PHP_URL_PATH), "/");
        $basePath = str_replace("/", "\/", trim(ROOT, "/")) . "\/";
		$path = preg_replace("/^" . $basePath . "(.*)/", "$1", $path);
		/*
		echo " path: ".$path;
		echo "<br>";
		echo " basePath: ".$basePath;
		echo "<br>";
		echo " regex: /^" . $basePath . "(.*)/";*/

		if(strlen($path) > 0) {
			$components = explode("/", $path, 3);
			
			if(isset($components[0])) {
			    //print("<br>Comp0: ".$components[0]);
			
				if(class_exists(ucfirst(strtolower($components[0])) . "Controller")) {
					$this->controller = ucfirst(strtolower($components[0])) . "Controller";
				} else {
					if(!isset($components[2])) {
						$components[2] = "";
					}
					$components[2] = $components[2] . $components[0];
				}
			}			
			if(isset($components[1])) {
			    //print("<br>Comp1: ".$components[1]);
			
				if(class_exists(ucfirst(strtolower($components[0])) . "Controller")) {
					$controllerName = ucfirst(strtolower($components[0])) . "Controller";
					if(method_exists(new $controllerName(array()), $components[1] . "Action")) {
						$this->action = strtolower($components[1]) . "Action";		
					} else {
						if(!isset($components[2])) {
							$components[2] = "";
						}
						$components[2] = $components[2] . $components[1];
					}
				} else {
					if(!isset($components[2])) {
						$components[2] = "";
					}
					$components[2] = $components[2] . $components[1];
				}
				
			}
			if(isset($components[2])) {
			    //print("<br>Comp2: ".$components[2]);
			
				$paramArray = explode("/", $components[2]);

				foreach ($paramArray as $param) {
					$this->params[] = $param;
				}
			}
		}
		
		//print_r($_SESSION);
	}

	public function run() {
		if(!TEST) {
			$controller = new $this->controller($this->params);
			$action = $this->action;
			$controller->$action();
		} else {
			include("tests/testMain.php");
		}
	}
}
?>
