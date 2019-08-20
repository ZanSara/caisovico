<?php

class OspitiController extends Controller {

	private $model, $view;

	public function __construct($params) {
		$this->params = $params;
	}

	public function baseAction() {
	    
	    $this->view = new OspitiView();
		$this->model = new OspitiModel();
		
		$this->model->protectPage();
		
        // Pass here what's needed into the View/Template rendering
		$params = array("Year" => ($this->model->getYear()),
		                "Titolo"=> "Lista Ospiti al Rifugio Del Grande - Stagione ".$this->model->getYear()
		                );
		     
		// Process an eventual POST call
		if ($_SERVER['REQUEST_METHOD'] == 'POST'){
		
		    $params = array_merge($params, array("METHOD" => "POST"));
		    self::processCall();
		    
		} else {
		    $params = array_merge($params, array("METHOD" => "GET"));
		}
			
		$this->view->addParams($params);
		$this->view->show();
	}
	
	
	// Operates on bookings, depending on the type of incoming data
	public function processCall() {
	    
        $this->model->setInizio($_POST['inizio']);
        $this->model->setFine($_POST['fine']);
        
        $this->view->addParams( array(
		                "NumPrenotazioni" => ($this->model->getNumPren()),
		                "NumGestioni" => ($this->model->getNumGest()),
		                "Data" => ($this->model->getData())
		                ));
    }
    
}
?>
