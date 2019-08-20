<?php

class RegisterController extends Controller {

	private $model, $view;

	public function __construct($params) {
		$this->params = $params;
	}
	

	public function baseAction() {
	    
	    $this->model = new RegisterModel();
	    $this->view = new RegisterView();
	    
	    $this->model->protectPage();
		
	    // Process an eventual POST call
		if ($_SERVER['REQUEST_METHOD'] == 'POST'){
		    self::processRegister();
		}
	    
	    $this->view->show();
	}
	
	
	public function processRegister() {

	    $username = $_POST['username'];
        $password = $_POST['password'];
        
        $params = array("FEEDBACK" => $this->model->register($username, $password) );
	    $this->view->addParams($params);
	    
	}
    
}
?>
