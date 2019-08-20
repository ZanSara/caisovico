<?php
include("Model.php");

	class OspitiModel extends Model {
	
	    private $giornoInizio, $giornoFine;
	    
	    public function setInizio($dataInizio){
	        $this->giornoInizio = self::correct_date($dataInizio, $this->getYear());
	    }
	    public function setFine($dataFine){
	        $this->giornoFine = self::correct_date($dataFine, $this->getYear());
	    }
	    
	    
	    
	    public function getNumPren(){
            $query = "  SELECT  COUNT(*) 
                        FROM    Pernottamenti
                        WHERE 
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
	    
	    
	    public function getNumGest(){
	        $query = "  SELECT  COUNT(*) 
                        FROM    Pernottamenti
                        WHERE
                                stagione = {$this->getYear()}
                            AND 
                                gestione = 1 
                            AND 
                            NOT (
                                giorno_inizio+durata-1 <  {$this->giornoInizio}
                            OR 
                                giorno_inizio > {$this->giornoFine})";
            $result = $this->mysqli->query($query);
	        if(!$result) {
		        throw new Exception("Errore inatteso durante il caricamento del conto delle gestioni."); // . $this->mysqli->error);
	        }
	        return $result->fetch_array()[0];
	    }
	    
	    
	    public function getData(){
	        $query = "  SELECT  * 
                        FROM    Pernottamenti
                        WHERE
                                stagione = {$this->getYear()}
                            AND 
                            NOT (
                                giorno_inizio+durata-1 <  {$this->giornoInizio}
                            OR 
                                giorno_inizio > {$this->giornoFine})
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
	    
        
    }
?>
