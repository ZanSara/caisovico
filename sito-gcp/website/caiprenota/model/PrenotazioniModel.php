<?php
include("Model.php");

	class PrenotazioniModel extends Model {
	
	    private $dataInizio, $dataFine, $giornoInizio, $giornoFine;
	   
	    
	    // Some utility getters
	    public function getDataInizio(){
	        return $this->dataInizio;
	    }
	    public function getDataFine(){
	        return $this->dataFine;
	    }
	    public function getGiornoInizio(){
	        return $this->giornoInizio;
	    }
	    public function getGiornoFine(){
	        return $this->giornoFine;
	    }
	    
	    public function setInizio($dataInizio){
	        $this->dataInizio = $dataInizio;
	        $this->giornoInizio = self::correct_date($dataInizio, $this->getYear());
	    }
	    public function setFine($dataFine){
	        $this->dataFine = $dataFine;
	        $this->giornoFine = self::correct_date($dataFine, $this->getYear());
	    }
	    
	    
	    
	    public function getNumClienti(){
            $query = "  SELECT  COUNT(*) 
                        FROM    Pernottamenti
                        WHERE
                                gestione = 0
                            AND
                                stagione = {$this->getYear()}
                            AND 
                            NOT (
                                giorno_inizio+durata-1 <  {$this->giornoInizio}
                            OR 
                                giorno_inizio > {$this->giornoFine} )";
            $result = $this->mysqli->query($query);
	        if(!$result) {
		        throw new Exception("Errore inatteso durante il caricamento del conto dei pernottamenti."); // . $this->mysqli->error);
	        }
	        return $result->fetch_array()[0];
	    }
	    
	    
	    
	    public function getDatiClienti(){
	        $query = "  SELECT  * 
                        FROM    Pernottamenti
                        WHERE
                                gestione = 0
                            AND
                                stagione = {$this->getYear()}
                            AND 
                            NOT (
                                giorno_inizio+durata-1 <  {$this->giornoInizio}
                            OR 
                                giorno_inizio > {$this->giornoFine} )
                            ORDER BY 
                                giorno_inizio";
            $result = $this->mysqli->query($query);
	        if(!$result) {
		        throw new Exception("Errore inatteso durante il caricamento dei dati degli ospiti."); // . $this->mysqli->error);
	        }
			//$data = $result->fetch_all(MYSQLI_ASSOC); // Crashes on server, for some reason.
			while ($row = $result->fetch_array(MYSQLI_ASSOC)) {
                $data[] = $row; 
            }
	        return $data ;
	    }
	    
	    
	    
	    public function getPrenotazioni(){
            
            $bookingsList = array();
            $bag = array();
            
            for($absday = $this->giornoInizio; $absday<$this->giornoFine+1; $absday++){
                $query = "  SELECT  * 
                            FROM    Pernottamenti
                            WHERE 
                                    stagione = {$this->getYear()}
                                AND
                                    gestione = 0
                                AND 
                                    giorno_inizio= {$absday}";
                $result = $this->mysqli->query($query);
		        if(!$result) {
			        throw new Exception("Errore inatteso durante il caricamento dei dati delle prenotazioni del giorno ".$absday-$this->firstday."."); // . $this->mysqli->error);
		        }
		        
                while ($row = $result->fetch_array()) {
                    $bag[] = $row; // This appends the NEW bookings to $bag, which is usually NOT empty!
                }
                
                $pren = array();
                // For each booking in the bag and for each bed they booked, set ID and color for that cell.
                foreach($bag as $booking){
                    for($p = 0; $p<$booking['posti']; $p++){
                        $pren[] = $booking['id'];
                    }
                    
                    if ($booking['giorno_inizio']+ $booking['durata']-1 <= $absday){
                        $key = array_search($booking, $bag);  // need to look for it, because the index is not normalized...
                        unset($bag[$key]);  // pop from array
                        $bag = array_values($bag); // fix indices
                    }
                }
                $bookingsList[] = $pren;   
            }
            return $bookingsList;
        }

        
    }
?>
