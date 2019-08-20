<?php
	include("Model.php");

	class PublicModel extends Model {
	
	    private $firstday, $lastday, $today;
	    
	    
	    // Sets some date variables reused later in the class.
	    public function customConstructor(){

	        $this->firstday = self::correct_date('01-06-'.$this->getYear(), $this->getYear());
            $this->lastday = self::correct_date('01-10-'.$this->getYear(), $this->getYear());
           
            $this->today = date('z') - $this->firstday;
            
	    }
	    
	    
	    // Some utility getters
	    public function getFirstDay(){
	        return $this->firstday;
	    }
	    public function getLastDay(){
	        return $this->lastday;
	    }
	    public function getToday(){
	        return $this->today;
	    }
	    
	    
	    // Output a list of user-friendly date that fits the first column of the table
	    public function buildDates(){

            $dateColumn = array();
            
            for($absday = $this->firstday; $absday<$this->lastday; $absday++){
                $absdate = DateTime::createFromFormat('z', $absday);
               
                $day = $absdate->format('j');
                $weekday = $absdate->format('N');
                $month = $absdate->format('n');

                $monthname = self::convert_month($month);
                $weekdayname = self::convert_weekday($weekday);
                
                $dateColumn[] = array($absday, $day, $monthname, $month, $weekdayname);
            }
            return $dateColumn;
        }
        
        
        // Convert weekday number into weekday name
	    public function convert_weekday($weekdaynum){
            
            switch ($weekdaynum):
                case '1':
                    return 'L';
                case '2':
                case '3':
                    return 'M';
                case '4':
                    return 'G';
                case '5':
                    return 'V';
                case '6':
                    return 'S';
                case '7':
                    return 'D';
                default:
                    return '?';
            endswitch;
            
            return "?";
        }
        
        
        
        // Output the gestori list for the second column of the table.
        // Builds an entry for each day, so Template does not need to process anything.
        public function getGestori(){   
        
            $listaGestori = array();
            $gestori = array();
            
            for($absday = $this->firstday; $absday<$this->lastday; $absday++){
                $query = "  SELECT  * 
                            FROM    Pernottamenti 
                            WHERE 
                                    stagione = {$this->getYear()}
                                AND
                                    gestione = 1 
                                AND 
                                    giorno_inizio= {$absday}";
                $result = $this->mysqli->query($query);
		        if(!$result) {
			        throw new Exception("Errore inatteso durante il caricamento dei dati della gestione del giorno ".$absday-$this->firstday."."); // . $this->mysqli->error);
		        }
		        
		        while ($row = $result->fetch_array()) {
                    $gestori[] = $row;        // This appends the NEW gestione to $gestori, which is usually NOT empty!
                }
            
                $gestore = array();
                $gestore[] = sizeOf($gestori); // to let Template know how many gestori I found for that day.
                if (sizeOf($gestori) != 0){
                    $gestore[] = $gestori[0]['id']; 
                    $gestore[] = $gestori[0]['nome'];
                }
                
                // Remove from $gestori all gestori that are on their last day
                foreach($gestori as $g){
                    if ($g["giorno_inizio"]+ $g["durata"]-1 <= $absday){ 
                        $key = array_search($g, $gestori);
                        unset($gestori[$key]);
                        $gestori = array_values($gestori);
                    }
                }
                
                $listaGestori[] = $gestore;
            }
            return $listaGestori;
        }
        
        
        
        // Output the list of booking required to fill the table.
        // Builds an entry for each day, so Template does not need to process anything.
        public function getBookings(){
            
            $bookingsList = array();
            $bag = array();
            
            for($absday = $this->firstday; $absday<$this->lastday; $absday++){
                $query = "  SELECT  * 

                            FROM    Pernottamenti AS p 
                                INNER JOIN 
                                    Colori AS c 
                                ON  
                                    p.colore = c.ID
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
                        $pren[] = array( $booking['id'], $booking['colore']);
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
