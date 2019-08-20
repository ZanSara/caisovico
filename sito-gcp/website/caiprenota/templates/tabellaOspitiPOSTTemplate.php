    
    <h2> <?echo $this->Titolo?> </h2>
    <hr>
    
    <p>In questa stagione ci sono state in totale <b><? echo $this->NumPrenotazioni ?> </h2> prenotazioni</b>, di cui <? echo $this->NumGestioni ?> </h2> gestioni.</p>
    
    <a class="btn btn-default" href="<? echo ROOT ?>/calendar/#<? echo date('j-n', strtotime('yesterday')); ?>">Torna Indietro</a>
    <hr>

    <table class="table table-bordered">
      <tr class="active">
		    <td>Num. Pren.</td>
        <td>Nome Cliente</td>
        <td>№ Telefono</td>
        <td>Provincia</td>
        <td>Data Arrivo</td>
        <td>Durata Soggiorno</td>
        <td>Posti Prenotati</td>
        <td>È una gestione?</td>
        <td>Nome Responsabile</td>
        <td>Note</td>
      </tr>
      
      
    <?
        foreach( $this->Data as $data) {
            
            //print_r($data);
            
            $absdate = DateTime::createFromFormat('z', $data['giorno_inizio']);
            $day = $absdate->format('d-m');

            if ($data['gestione']){
                echo("
                <tr class='danger'>
                ");
            }else{
                echo("
                <tr>
                ");
            }

            echo("
			      <td>".$data['id']."</td>
                  <td>".$data['nome']."</td>
                  <td>".$data['tel']."</td>
                  <td>".$data['provincia']."</td>
                  <td>".$day."-".$this->Year."</td>
                  <td>".$data['durata']."</td>
            ");

            if ($data['gestione']){
                echo("
                <td>X</td>
                <td>Sì</td>
                ");
            }else{
                echo("
                <td>".$data['posti']."</td>
                <td>No</td>
                ");
            }

            echo("
                  <td>".$data['responsabile']."</td>
                  <td>".$data['note']."</td>
                <tr>
            ");
        }
    ?>

        </table>
    
    <a class="btn btn-default" href="<? echo ROOT ?>/calendar/#<? echo date('j-n', strtotime('yesterday')); ?>">Torna Indietro</a>
    
