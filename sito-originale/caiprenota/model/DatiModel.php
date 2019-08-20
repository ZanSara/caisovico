<?php
include("Model.php");

	class DatiModel extends Model {
	
        public function getDati($gestione, $prenid){
        
            $query = "  SELECT  * 
                        FROM    Pernottamenti 
                        WHERE 
                                id = {$prenid}";
            $result = $this->mysqli->query($query);
	        if(!$result) {
		        throw new Exception("Errore inatteso durante il caricamento dei dati della prenotazione numero ".$preind."."); // . $this->mysqli->error);
	        }
            $data = $result->fetch_array();

            if (!$data){
                throw new Exception("Dati della prenotazione non trovati");
            }
            
            // Convert data format
            $absdate = DateTime::createFromFormat('z', $data['giorno_inizio']);
            $day = $absdate->format('d');
            $month = $absdate->format('m');
            
            return json_encode(
                array(
                    "nome" => $data['nome'],
                    "tel" => $data['tel'],
                    "provincia" => $data['provincia'],
                    "prenid" => $data['id'],
                    "arrivo" => $day." ".self::convert_month($month)." ".$this->getYear(),
                    "durata" => $data['durata'],
                    "posti" => $data['posti'],
                    "resp" => $data['responsabile'],
                    "note" => $data['note'],
                    "gestione" => $data['gestione']
            )) ;
        }
    }
?>
