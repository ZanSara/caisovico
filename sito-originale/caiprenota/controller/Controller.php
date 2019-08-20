<?php
abstract class Controller {
	protected $params;

	function __construct($params) {
		$this->params = $params;
	}

	public abstract function baseAction();
}
?>
