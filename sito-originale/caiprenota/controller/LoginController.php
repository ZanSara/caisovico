<?php

class LoginController extends Controller {

	private $model, $view;

	public function __construct($params) {
		$this->params = $params;
	}
	

	public function baseAction() {
	    
	    $this->model = new LoginModel();
	    $this->view = new LoginView();
	    
	    $success = -1;
	    // Process an eventual POST call
		if ($_SERVER['REQUEST_METHOD'] == 'POST'){
		    $success = self::processLogin();
		}
		$params = array("SUCCESS" => $success,
                        "FEEDBACK" => "Login fallito. Inserisci nuovamente le tue credenziali." );
	    $this->view->addParams($params);
	    $this->view->show();
	    
	}
	
	
	public function processLogin() {
        
	    $username = $_POST['username'];
        $password = $_POST['password']; // The hashed password.
     
        if ($this->model->login($username, $password) == true) {
            // Login succeeded
            return 1;
        } else {
            // Login failed
            return 0;
        }
        return 0;
	}
    
}
?>
