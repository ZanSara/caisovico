<?php
	include_once("config.php");

	abstract class View {
		private $params = array();

		public function __get($name) {
			if($name == "params") {
				return $this->params;
			}
			if(array_key_exists($name, $this->params)) {
				return $this->params[$name];
			}

			return "Missing parameter";
		}

		public function __set($name, $value) {
			$this->params[$name] = $value;
		}

		public function addParams($params) {
			$this->params = array_merge($this->params, $params);
		}

		public abstract function show();
	}
?>