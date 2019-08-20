<?php

class LogoutController extends Controller {

	private $model, $view;

	public function __construct($params) {
		$this->params = $params;
	}
	

	public function baseAction() {
	    
	    $this->model = new LogoutModel();
	    $this->view = new LogoutView();
	    
	    $this->model->protectPage();
	    $this->model->logout();
	    
	    $this->view->show();
	}
	   
}
?>
