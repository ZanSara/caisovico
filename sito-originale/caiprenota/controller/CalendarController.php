<?php

class CalendarController extends Controller {

	private $model, $view;

	public function __construct($params) {
	    $this->params = $params;
	}

	public function baseAction() {
	    
	    $this->view = new CalendarView();
		$this->model = new CalendarModel();
		
		$this->model->protectPage();
		
		// Process an eventual POST call
		if ($_SERVER['REQUEST_METHOD'] == 'POST'){
		    self::processBooking();
		}

        // Pass here what's needed into the View/Template rendering
		$params = array("Year" => ($this->model->getYear()),
		    "Today" => ($this->model->getToday()),
		    "FirstDay" => ($this->model->getFirstDay()),
		    "LastDay" => ($this->model->getLastDay()),
		    "Dates" => ($this->model->buildDates()),
		    "Gestori" => ($this->model->getGestori()),
		    "Bookings" => ($this->model->getBookings()),
		    "Private" => 1,
		    "LastPrenID" => ($this->model->getLastPrenid()),
		    "NextRow" => ($this->model->getNextRow()),
		    "ErrorFlag" => ($this->model->getErrorFlag()),
		    "ErrorMsg" => ($this->model->getErrorMsg()),
		     );
			
		$this->view->addParams($params);
		$this->view->show();
	}
	
	
	// Operates on bookings, depending on the type of incoming data
	public function processBooking() {
	
	    if(!isset($_POST['prenid'] ) ){
	        throw new Exception("ID della prenotazione non ricevuto.");
	    }
	    $prenid = (int)$_POST['prenid'];
	    
	    try{
	    
	        if($prenid < 0){
                //echo "<br>delbookig!<br>";
                $this->model->deleteReservation($prenid);
                return;
            }
	
	        // Preprocess POST data
	        if(isset($_POST['gestione'])){
                $gestione = 1;
                $posti = 0;
            } else {
                $gestione = 0;
                $posti = (int)$_POST['posti'];
            }
            if(isset($_POST['provincia'])){
                $provincia = $_POST['provincia'];
            } else {
                $provincia = "";
            }
            $dati = array(  "nome" => $_POST['nome'],
                            "telefono" => $_POST['telefono'],
                            "provincia" => $provincia,
                            "arrivo" => $_POST['arrivo'],
                            "durata" => $_POST['durata'],
                            "posti" => $posti,
                            "note" => $_POST['note'],
                            "gestione" => $gestione,
                            "responsabile" => $_POST['responsabile']);
                            
            if ( $prenid == null ||  $prenid == "" ||  $prenid == 0 ){
                //echo "<br>makeReservation!<br>";
                $this->model->makeReservation($dati);
                //$open = 1;
                
            } else {
                //echo "<br>updateReservation!<br>";
                $this->model->updateReservation($prenid, $dati);
                //$last_prenid = (int)$_POST['prenid'];
            }
        }catch (Exception $e){
            
            $this->view->addParams( array( "EXCEPTION" => $e->getMessage() ));
        }
          
	}
}
?>
