<?php
include("Model.php");

	class FindModel extends Model {
	
        public function findBookings($formdata){
        
            // Converte la data in formato DB
            if( isset($formdata['giorno_inizio']) && $formdata['giorno_inizio'][1]!= "" && $formdata['giorno_inizio'][1]!=null ){

                //echo($formdata['arrivo'][1]);
                $exploded = explode(" ", $formdata['giorno_inizio'][1]);
                if(count($exploded) != 3){
                    throw new Exception("La data inserita non e' valida.");
                }
                if( $exploded[2] != self::getYear() ){
                    throw new Exception("La data inserita non appartiene a questa stagione.");
                }
                $exploded[1] = self::decode_month($exploded[1]); // Se non e' un mese valido, l'eccezione viene lanciata all'interno
                if( (int)$exploded[0] > 31 or ((int)$exploded[0] > 30 and ( $exploded[1] != "06" and $exploded[1] != "09") ) ){
                    throw new Exception("Il giorno del mese inserito non e' valido.");
                }
                $imploded = implode("-", $exploded);
                $formdata['giorno_inizio'][1] = self::correct_date($imploded, $this->getYear());
                //echo "x".$formdata['giorno_inizio'][1];
            }

		    
            //print_r($formdata);
            //echo(count($formdata));
            //echo "<br>";
            // Compila la query e la esegue
            $year = self::getYear();
            $query = "  SELECT * 
                        FROM Pernottamenti 
                        WHERE 
                            stagione = '{$year}'";
            
            if(count($formdata)>0){
                $query .= " AND ";
                
                foreach($formdata as $key => $elem) {
                    if($elem[1] != null || $elem[1] != ""){
                        
                        if($elem[2]=='string'){
                            $query .= "{$elem[0]} LIKE '%{$elem[1]}%' OR ";
                        }
                        if($elem[2]=='int'){
                            $query .= "{$elem[0]} = '{$elem[1]}' OR ";
                        }
                    }
                }
                $query .= " False ";
                //$query = substr($query, 0, -3);
            }
            
            //echo $query;
            //echo "<br>";
            
            $result = $this->mysqli->query($query);
	        if(!$result) {
		        throw new Exception("Errore inatteso durante il caricamento dei dati della ricerca."); // . $this->mysqli->error);
	        }

            //$data = $result->fetch_all(MYSQLI_ASSOC); // Crashes on server, for some reason.
			$data = [];
			while ($row = $result->fetch_array(MYSQLI_ASSOC)) {
                $data[] = $row; 
            }
           
            // Corregge nuovamente la data in output
            for($i=0; $i<count($data); $i++){
                $datetime = DateTime::createFromFormat('z', $data[$i]['giorno_inizio']);
                $datestring = $datetime->format('j-m-Y');
                $exploded = explode("-", $datestring);
                $exploded[1] = self::convert_month($exploded[1]);
                $imploded = implode(" ", $exploded);
                $data[$i]['giorno_inizio'] = $imploded;
            }
            
            return json_encode($data);
        }
    }
?>
