<?php

class DatiController extends Controller {

	private $model, $view;

	public function __construct($params) {
		$this->params = $params;
	}
	

	public function baseAction() {
	    
	    $this->model = new DatiModel();
	    $this->view = new JSONView();
	    
	    $this->model->protectPage();
	    
	    if(!isset($_GET['gestione']) || !isset($_GET['prenid'])){
	        echo "ERRORE: uno dei due parametri non e' settato.";
	        return;
	    }
	    
		$params = array("JSON" => ($this->model->getDati($_GET['gestione'], $_GET['prenid'])) );
		
		$this->view->addParams($params);
		$this->view->show();
	}
    
}
?>
