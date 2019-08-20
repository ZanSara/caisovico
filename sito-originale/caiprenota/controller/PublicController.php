<?php

class PublicController extends Controller {

	private $model, $view;

	public function __construct($params) {
		$this->params = $params;
	}

	public function baseAction() {
	    
	    $this->view = new PublicView();
		$this->model = new PublicModel();

        // Pass here what's needed into the View/Template rendering
		$params = array("Year" => ($this->model->getYear()),
		    "Today" => ($this->model->getToday()),
		    "FirstDay" => ($this->model->getFirstDay()),
		    "LastDay" => ($this->model->getLastDay()),
		    "Dates" => ($this->model->buildDates()),
		    "Gestori" => ($this->model->getGestori()),
		    "Bookings" => ($this->model->getBookings()),
			"Private" => 0,
		     );
			
		$this->view->addParams($params);
		$this->view->show();
	}
	
}
?>
