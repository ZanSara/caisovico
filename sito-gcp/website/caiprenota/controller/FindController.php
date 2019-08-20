<?php

class FindController extends Controller {

	private $model, $view;

	public function __construct($params) {
		$this->params = $params;
	}
	

	public function baseAction() {
	    
	    $this->model = new FindModel();
	    $this->view = new JSONView();
	    
	    $this->model->protectPage();
	    
	    $formdata = array();
	    $fields = ['id', 'nome', 'tel', 'provincia', 'giorno_inizio', 'durata', 'posti', 'responsabile', 'note'];
	    $vals =   ['int', 'string', 'string', 'string', 'int', 'int', 'int', 'string', 'string'];
	    
	    for($i=0; $i<count($fields); $i++ ){
	        if(isset($_GET[$fields[$i]]) && $_GET[$fields[$i]]!= ""){
	            $formdata[$fields[$i]] = [$fields[$i],  $_GET[$fields[$i]], $vals[$i]];
	        }
	    }
	    
	    try{
	        $dati = $this->model->findBookings($formdata);
	    }catch (Exception $e){
	        $dati = "[]";
	    }
		$params = array("JSON" => $dati );
		
		$this->view->addParams($params);
		$this->view->show();
	}
    
}
?>
