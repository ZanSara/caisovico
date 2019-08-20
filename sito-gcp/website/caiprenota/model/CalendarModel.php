<?php

include("PublicModel.php");

	class CalendarModel extends PublicModel {

	    //private $firstday, $lastday, $today, $last_prenid, $next_row, $error_flag, $error_msg;
	    private $last_prenid, $next_row, $error_flag, $error_msg;

	    // Sets some date variables reused later in the class.
	    public function customConstructor(){

            parent::customConstructor();

            $last_prenid = 0;
            $next_row = 0;
	    }


	    // Some utility getters
	    public function getLastPrenid(){
	        return $this->last_prenid;
	    }
	    public function getNextRow(){
	        return $this->next_row;
	    }
	    public function getErrorFlag(){
	        return $this->error_flag;
	    }
	    public function getErrorMsg(){
	        return $this->error_msg;
	    }

	    // Error setter, in case
	    public function setError($error_msg){
	        $this->error_flag = true;
	        $this->error_msg = $error_msg;
	    }
	    public function resetError(){
	        $this->error_flag = false;
	        $this->error_msg = "[Nessun errore]";
	    }

	    // Output a list of user-friendly date that fits the first column of the table
	    public function buildDates(){

            $dateColumn = array();

            for($absday = $this->getFirstDay(); $absday<$this->getLastDay(); $absday++){
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

            for($absday = $this->getFirstDay(); $absday<$this->getLastDay(); $absday++){
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

            for($absday = $this->getFirstDay(); $absday<$this->getLastDay(); $absday++){
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




        // *************** RESERVATIONS MANAGEMENT *******************************

        // Perform a reservation into DB
        public function makeReservation($dati){

            $validData = self::validate($dati);
            self::checkFreeBeds(0, $validData);

            // Retrieve last color used
            $query = "  SELECT ID
                        FROM Colori
                        WHERE last IN (
                                        SELECT MAX(last)
                                        FROM Colori
                                      )";
            $result1 = $this->mysqli->query($query);
	        if(!$result1) {



		        throw new Exception("Errore inatteso durante il caricamento dei dati relativi all'ultimo colore."); // . $this->mysqli->error);
	        }
	        $last_color = $result1->fetch_array()[0];

	        // Retrieve count colors
	        $query = "  SELECT COUNT(*)
	                    FROM Colori";
            $result2 = $this->mysqli->query($query);
	        if(!$result2) {
		        throw new Exception("Errore inatteso durante il caricamento dei dati relativi ai colori."); // . $this->mysqli->error);
	        }
            $ncolor = $result2->fetch_array()[0];

            // Decide what's the next one to get
            if ($last_color >= $ncolor-1 ){
                $new_color = 0;
            }else{
                $new_color = $last_color+1;
            }

           // Actually write reservation in DB
	       // Fix this
	       $values = "(NULL, '".
	                    $validData['nome']."', '".
                        $validData['telefono']."', '".
                        $validData['provincia']."', '".
                        $validData['arrivo']."', '".
                        $this->getYear()."', '".
                        $validData['durata']."', '".
                        $validData['posti']."', '".
                        $validData['note']."', '".
                        $validData['gestione']."', '".
                        $validData['responsabile']."', '".
                        $new_color."')";

	       $query = "  INSERT INTO
	                        `Pernottamenti` (
	                            `id`,
	                            `nome`,
	                            `tel`,
	                            `provincia`,
	                            `giorno_inizio`,
	                            `stagione`,
	                            `durata`,
	                            `posti`,
	                            `note`,
	                            `gestione`,
	                            `responsabile`,
	                            `colore`)
                            VALUES
                                {$values}";
            $main_result = $this->mysqli->query($query);

            if (!$main_result) {
               throw new Exception("Errore interno durante la prenotazione:<br>la prenotazione NON è stata effettuata.<br>Avverti il webmaster.");//.$result);

            } else {

                $this->last_prenid = $this->mysqli->insert_id;

                $absdate = DateTime::createFromFormat('z', ($validData['arrivo']));
                $this->next_row = $absdate->format('j-m');



                // Update Last Color: the field 'last' should be bigger for the last used color
                $query = "  SELECT MAX(last)
                            FROM Colori";
                $result3 = $this->mysqli->query($query);
	            if(!$result3) {
		            throw new Exception("Errore inatteso durante il caricamento dell'ultimo colore.<br>la prenotazione È stata comunque effettuata.<br>Avverti il webmaster."); // . $this->mysqli->error);
	            }
                $max_last = $result3->fetch_array()[0] + 1;


                $query = "  UPDATE Colori
                            SET last = {$max_last}
                            WHERE ID = {$new_color}";

                $result4 = $this->mysqli->query($query);
	            if(!$result4) {
		            throw new Exception("Errore inatteso durante l'aggiornamento del colore.<br>la prenotazione È stata comunque effettuata.<br>Avverti il webmaster."); // . $this->mysqli->error);
	            }
            }

        }



        // Update a reservation into DB
        public function updateReservation($prenid, $dati){

           $validData = self::validate($dati);
           self::checkFreeBeds($prenid, $validData);

            // Update reservation in DB
           $query = "  UPDATE
                            `Pernottamenti`
                        SET
                            `nome` = '{$validData['nome']}',
                            `tel` = '{$validData['telefono']}',
                            `provincia` = '{$validData['provincia']}',
                            `giorno_inizio` = '{$validData['arrivo']}',
                            `durata` = '{$validData['durata']}',
                            `posti` = '{$validData['posti']}',
                            `note` = '{$validData['note']}',
                            `gestione` = '{$validData['gestione']}',
                            `responsabile` = '{$validData['responsabile']}'
                        WHERE
                            `ID` = '{$prenid}'";

            $result = $this->mysqli->query($query);
            if(!$result) {
                throw new Exception("Errore interno:<br>L'aggiornamento NON è stato effettuato.<br>Avverti il webmaster."); // . $this->mysqli->error);
            }
            // attenzione: se prenid non esiste nel DB, fallisce silenziosamente.

            $absdate = DateTime::createFromFormat('z', ($validData['arrivo']));
            $this->next_row = $absdate->format('j-m');

        }


        // Delete reservation into DB
        public function deleteReservation($prenid){
            $prenid = -1*$prenid;

            $query = "  DELETE FROM
                            Pernottamenti
                        WHERE
                            ID = {$prenid}";

            $result = $this->mysqli->query($query);
            if(!$result) {
	            throw new Exception("Errore interno al server.<br>La prenotazione NON è stata cancellata.<br>Avverti il webmaster."); // . $this->mysqli->error);
            }
            // attenzione: se prenid non esiste nel DB, fallisce silenziosamente.
        }





    // *************** SERVER-SIDE DATA VALIDATION ****************************
    // Throws errors only if js validation failed to spot bad data.

        public function validate($dati) {

            // Validate Nome Cliente
            $dati['nome'] = trim($dati['nome']);
            if ($dati['nome'] == '' or !preg_match('/^[\w,\s,àèéìòùÀÈÉÌÒÙ]+$/', $dati['nome'])){
                throw new Exception("Nome del cliente non valido");
            }

            // Validate Telefono
            $dati['telefono'] = trim($dati['telefono']);
            if ($dati['telefono'] == '' or !preg_match('/^[+]?([0-9]|[\s]|[-]|[(]|[)]){4,50}$/', $dati['telefono'])){
                throw new Exception("Numero di telefono non valido");
            }

            // "Validate Provincia" (this field can be empty)
            $dati['provincia'] = trim($dati['provincia']);

            // Validate Arrivo date and convert the date in a db-friendly number
            $exploded = explode(" ", $dati['arrivo']);

            if(count($exploded) != 3){
                throw new Exception("La data inserita non e' valida.");
            }
            if( $exploded[2] != $this->getYear() ){
                throw new Exception("La data inserita non appartiene a questa stagione.");
            }

            $exploded[1] = self::decode_month($exploded[1]); // Se non e' un mese valido, l'eccezione viene lanciata all'interno
            if( (int)$exploded[0] > 31 or ((int)$exploded[0] > 30 and ( $exploded[1] == "06" and $exploded[1] == "09") ) ){
                throw new Exception("Il giorno del mese inserito non e' valido.");
            }
            $imploded = implode("-", $exploded);
            $absdate = self::correct_date($imploded, $this->getYear());

            // Validate Durata (no longer than the whole season)
            $dati['durata'] = (int)$dati['durata'];
            if ($dati['durata'] <= 0 or $dati['durata']>= 122){
                throw new Exception("Durata della prenotazione non valida");
            }

            // Validate Posti (no more than the available beds, and only for clients)
            $dati['posti'] = (int)$dati['posti'];
            if (!$dati['gestione'] and ( $dati['posti'] <= 0 or $dati['posti'] > 16) ){
                echo $dati['gestione'];
                echo "<br>";
                echo $dati['posti'];
                throw new Exception("Numero di posti prenotati non valido");
            }

            // Validate Nome Responsabile
            if ($dati['responsabile']== '' or !preg_match('/^[\w,\s,àèéìòùÀÈÉÌÒÙ]+$/', $dati['responsabile'])){
                throw new Exception("Nome del responsabile non valido");
            }


            $validData = array( 'nome' => ($this->real_escape_string($dati['nome'])),
                                'telefono' => ($this->real_escape_string($dati['telefono'])),
                                'provincia' => ($this->real_escape_string($dati['provincia'])),
                                'arrivo' => $absdate,
                                'durata' => $dati['durata'],
                                'posti' => $dati['posti'],
                                'note' => ($this->real_escape_string($dati['note'])),
                                'gestione' => $dati['gestione'],
                                'responsabile' => ($this->real_escape_string($dati['responsabile']))
                              );
            return $validData;
        }


    // *************** DB ASSERTIONS ****************************************

        public function checkFreeBeds($prenid, $data){

            // Per ogni giorno in cui sto cercando di prenotare, controlla se il numero dei posti
            // occupati supera 16 (o se ci sono piu' di 0 gestori) e se trova riscontro,
            // aggiunge il giorno incriminato a dayslist
            $dayslist = array();
            for($giorno=$data['arrivo']; $giorno < ($data['arrivo']+$data['durata']); $giorno++ ){

                if($data['gestione']){
                    $what2Do = "COUNT(*)";
                }else{
                    $what2Do = "SUM(posti)";
                }


                $query = "  SELECT  {$what2Do}
                            FROM    Pernottamenti
                            WHERE
                                    stagione = {$this->getYear()}
                                AND
                                    id <> {$prenid}
                                AND
                                    giorno_inizio <= {$giorno}
                                AND
                                    (giorno_inizio + durata) > {$giorno}
                                AND
                                    gestione = {$data['gestione']}";
                $result = $this->mysqli->query($query);
		        if(!$result) {
			        throw new Exception("Errore inatteso durante il caricamento dei dati delle prenotazioni del giorno ".$giorno."."); // . $this->mysqli->error);
		        }
		        $prenotazioni = $result->fetch_array();

                if($data['gestione']){
                    if($prenotazioni[0] > 0){
                        $dayslist[] = DateTime::createFromFormat('z', $giorno);
                    }
                }else{
                    if($prenotazioni[0] + $data['posti'] > 16){
                        $dayslist[] = DateTime::createFromFormat('z', $giorno);
                    }
                }
            }

            // Se ho collezionato almeno un giorno in cui e' impossibile prenotare,
            // fa scattare l'eccezione.
            if(count($dayslist) > 0){
                $errorstring = "";
                foreach ($dayslist as $day){
                    $dateNumerical = explode("-", (string)$day->format('d-m-Y'));
                    $dateNumerical[1] = self::convert_month( $dateNumerical[1] );
                    $date = implode(" ", $dateNumerical);
                    $errorstring = $errorstring.'<br>'.$date;
                }

                if (!$data['gestione']){
                    throw new Exception("Impossibile prenotare!<br>Non ci sono abbastanza posti disponibili nelle date:<br>".$errorstring."<br><br>NON è stata registrata nessuna modifica: ripetere l'operazione.");
                }else{
                    throw new Exception("Attenzione!<br>C'è già un gestore in queste date:<br>".$errorstring."<br><br>NON è stata registrata nessuna modifica: ripetere l'operazione.");
                }
            }

        }




    }
?>
