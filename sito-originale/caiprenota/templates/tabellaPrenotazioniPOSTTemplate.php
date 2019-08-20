    
    <h2><? echo $this->Titolo ?></h2>
    <hr>
    
    <p>Dal <? echo $this->DataInizio ?> al <? echo $this->DataFine ?> ci sono in totale <b><? echo $this->NumClienti ?> prenotazioni</b>.</p>
    
    <div class="noprint">
      <a class="btn btn-default" href="javascript:window.print()">Stampa la pagina</a>
      <!-- CHANGE ME WHEN DEPLOYING!!! -->
      <a class="btn btn-default" href="prenotazioni">Cambia Date</a>
      <a class="btn btn-default" href="<? echo ROOT ?>/calendar/#<? echo date('j-n', strtotime('yesterday')); ?>">Torna Indietro</a>
    </div>

    <h3>Calendario:</h3>
    <table class="table table-bordered calendario" style='border:1px solid black;'>
        
<?
    for($g=0; $g<($this->GiornoFine - $this->GiornoInizio+1); $g++){

        $absdate = DateTime::createFromFormat('z', ($g+$this->GiornoInizio));
        $day = $absdate->format('d-m');
                  
        echo("<tr>");
        echo("<td class='warning'>".$day."</td>");
                       
        // Filling the rest of the table
        $bookings = $this->TabellaPrenotazioni[$g];
        $tot = 0;
        foreach($bookings as $cell){
            $tot++;
            echo("<td class='active'>№".$cell."</td>");
        }
        for(;$tot<16; $tot++){
            echo ("<td></td>");
        }
        echo ("</tr>");
    }
?>


    </table>

    <hr>

    <h3>Lista Clienti:</h3>

    <table class="table table-bordered">
      <tr class="active">
        <td>№</td>
        <td>Nome Cliente</td>
        <td>№ Telefono</td>
        <td>Provincia</td>
        <td>Data Arrivo</td>
        <td>Data Partenza</td>
        <td>Durata Soggiorno</td>
        <td>Posti Prenotati</td>
        <td>Nome Responsabile</td>
        <td>Note</td>
      </tr>
        
<?
     foreach ($this->DatiClienti as $data) {

        $absdate = DateTime::createFromFormat('z', $data['giorno_inizio']);
        $dayInizio = $absdate->format('d-m');

        $absdate = DateTime::createFromFormat('z', $data['giorno_inizio']+$data['durata']);
        $dayFine = $absdate->format('d-m');

        echo("
            <tr>
              <td>".$data['id']."</td>
              <td>".$data['nome']."</td>
              <td>".$data['tel']."</td>
              <td>".$data['provincia']."</td>
              <td>".$dayInizio."-".$this->Year."</td>
              <td>".$dayFine."-".$this->Year."</td>
              <td>".$data['durata']."</td>
              <td>".$data['posti']."</td>
              <td>".$data['responsabile']."</td>
              <td>".$data['note']."</td>
            <tr>
        ");
    }
?> 
        
    </table>
    
    <a class="btn btn-default" href="<? echo ROOT ?>/calendar/#<? echo date('j-n', strtotime('yesterday')); ?>">Torna Indietro</a>
    
