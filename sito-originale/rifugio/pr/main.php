<!DOCTYPE html>
<html lang="it">
  <head>
    <meta charset="utf-8">
    <title>Prenotazioni - CAI Sovico</title>

    <link href="static/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <link href="style.css" rel="stylesheet">
    <script src="static/javascript/jQuery/jquery-1.11.2.min.js"></script>
    <script src="static/bootstrap/js/bootstrap.min.js"></script>
    <script src="funzioni.js"></script>

  </head>
  <body>

    <?
    $ris = 0;
    if ($_GET) {
        $ris = $_GET['ris'];
    };
    ?>

    <div class="title shadow1">
        <h2>Prenotazioni Stagione 2016</h2>
        <h4>Rifugio M. Del Grande - R. Camerini</h4>
        <p>ATTENZIONE: I tipi di sistemazione (letto, brandina, bivacco etc...)
        sono provvisori e la disposizione effettiva dei posti letto verrà
        concordata con i gestori una volta giunti al Rifugio.</p>
    </div>

    <div class="row">

        <div id="calendario-box" class="calendario-outer-box shadow2">

          <table id="tableid" style="overflow:hidden;">
              <tr><td>
                <div class='scrollable'>
                <table class="calendario">
                    <tr>
                        <td class='giorno' style="border: 1px solid #fff;">Data</td>
                        <? if ($ris==1)
                            echo("<td class='gestore' style='border: 1px solid #fff;'>Gestore</td>")
                        ?>
                        <td class='letto'></td>
                        <td class='letto'></td>
                        <td class='letto'></td>
                        <td class='letto'>Letto</td>
                        <td class='letto'></td>
                        <td class='letto'></td>
                        <td class='bivacco' style="border-left: 1px solid #fff;"></td>
                        <td class='bivacco'>Bivacco</td>
                        <td class='bivacco'></td>
                        <td class='bivacco'></td>
                        <td class="brandina" style="border-left: 1px solid #fff;">Brandina</td>
                        <td class="brandina"></td>
                        <td class="materasso" style="border-left: 1px solid #fff;"></td>
                        <td class="materasso">Materasso</td>
                        <td class="materasso"></td>
                        <td class="materasso"></td>
                    </tr>
                </table>
                </div>
              </td></tr>
              <tr><td>
                <div class="calendario-inner-box scrollable">
                <table class="calendario grid">
                  <colgroup>
                        <col class='giorno'>
                        <? if ($ris == 1)
                            echo("<col class='gestore'>")
                        ?>
                        <col class='letto'>
                        <col class='letto'>
                        <col class='letto'>
                        <col class='letto'>
                        <col class='letto'>
                        <col class='letto'>
                        <col class="bivacco">
                        <col class="bivacco">
                        <col class="bivacco">
                        <col class="bivacco">
                        <col class="brandina">
                        <col class="brandina">
                        <col class="materasso">
                        <col class="materasso">
                        <col class="materasso">
                        <col class="materasso">
                  </colgroup>
                  <tbody>
    <?

    $today = array();
    $today['absday'] = '5';
    $firstweekday = 4;





    // Start building the table
    $daysum = 122;
    $calendario = array();
    $gestioni = array();
    $colori = array(
        "#00A823",
        "#00D1C5",
        "#0061D1",
        "#7E38FF",
        "#DA38FF",
        "#FF387A",
        "#FF0D0A",
        "#FF781A",
        "#EB9F00",
        "#6E6E6E",
        "#1F1F1F",
        "#703200"
    );
    $lastcolor = 0;

    for($i=0; $i<$daysum; $i++){
        $gestioni[$i] = 0;
        $calendario[$i] = array();
        for($j=0; $j<17; $j++){
            $calendario[$i][$j] = 0;
        }
    }

    for($absday = 0; $absday<$daysum; $absday++){
        if ($absday - 30 >= 0){
            if ($absday - 61 >= 0){
                if ($absday - 92 >= 0){
                    $month = 9;
                    $monthname = "Set";
                    $day = $absday - 91;
                }else{
                    $month = 8;
                    $monthname = "Ago";
                    $day = $absday - 60;
                }
            }else{
                $month = 7;
                $monthname = "Lug";
                $day = $absday - 29;
            }
        }else{
            $month = 6;
            $monthname = "Giu";
            $day = $absday + 1;
        }

        // Building tr
        echo("<tr id='".$day."-".$month."'");
        if( $day == 1 ) echo ("style='border-top: 4px solid black;'");
        if( $absday == $daysum-1 ) echo ("style='border-bottom: 4px solid grey;'");
        if( $today['absday'] == $absday) echo("id='today' class='border'");
        echo(">");

        // Building Date td
        echo("<td ");
        if( ($firstweekday+$absday-1) % 7 == 6 ) echo("style='color:red;'");
        if( $month == 8 and $day==15 ) echo("style=color:red;");
        echo(">".$day." ".$monthname." / ".$absday);
        echo("</td>");

        // Building Gestore td
        if ($ris == 1){
            echo("<td ");
            echo(">");
            echo("<a id='".$absday."-G' href='javascript:getData(".$gestioni[$absday].", 1)' onblur='javascript:hideBox()'><div>");
            echo($gestioni[$absday]);
            echo("</div></a>");
            echo("</td>");
        }

        // Some hardcoded placeholder bookings
        $calendario[4][3] = array(1, '#00A823', 0);
        $calendario[4][1] = array(1, '#00A823', 0);
        $calendario[4][2] = array(1, '#00A823', 0);
        $calendario[5][3] = array(1, '#00A823', 0);
        $calendario[5][1] = array(1, '#00A823', 0);
        $calendario[5][2] = array(1, '#00A823', 0);
        $calendario[4][4] = array(2, '#00D1C5', 0);
        $calendario[5][4] = array(2, '#00D1C5', 0);
        $calendario[6][0] = array(3, '#0061D1', 1);
        $calendario[4][0] = array(3, '#0061D1', 1);
        $calendario[5][0] = array(3, '#0061D1', 1);


        // Filling the rest of the table
        for($i=0; $i<16; $i++){
            if ($calendario[$absday][$i] != 0){
                echo("<td style='background:".$calendario[$absday][$i][1].";'>");
                if ($ris == 1 ) echo("<a id='".$absday."-".$i."' href='javascript:getData(".$calendario[$absday][$i][0].", 0)' onblur='javascript:hideBox()' ><div>");
                echo("<b>".$calendario[$absday][$i][0]."</b></div></a></td>");
            }else{
                echo ("<td></td>");
            }
        }
    }?>
                </tr>
              </tbody>
            </table>
            </div>
            </td></tr>
          </tbody>
          </table>

          </div>
        </div>

    <? if ($ris==1){ ?>

        <div id="data-box" class="one-third" style="display:none;">
          <div id="left-box" class="inner-box white shadow2">
              <h3 id='left-box-num'>Prenotazione № </h3>
              <p id='left-box-nome'><b>Nome Cliente</b>:</p>
              <p id='left-box-tel'><b>№ Telefono</b>:</p>
              <p id='left-box-arrivo'><b>Data Arrivo</b>:</p>
              <p id='left-box-durata'><b>Durata</b>:</p>
              <p id='left-box-posti'><b>Posti prenotati</b>:</p>
              <p id='left-box-resp'><b>Responsabile</b>:</p>
              <button type="button" class="btn btn-success" onclick="javascript:modifyBooking()">Modifica Dati</button>
              <button type="button" class="btn btn-danger" onclick="javascript:deleteBooking()">Elimina Prenotazione</button>
          </div>
        </div>

    <? } ?>



        <div id="new-booking" class="float-center white shadow1">
          <div id="form-box" class="inner-box">
              <div class="center">
                <h2>Nuova Prenotazione</h2>
              </div>
              <form id='form'>
                  <input type="text" name="nome" placeholder="Nome Cliente">
                  <input type="text" name="telefono" placeholder="№ Telefono">
                  <input type="text" name="arrivo" placeholder="Data Arrivo" id="datepick">
                  <input type="text" name="durata" placeholder="Durata (notti)">
                  <input type="text" name="posti" placeholder="Posti prenotati">
                  <input type="text" name="responsabile" placeholder="Responsabile">
                  <button type="button" class="btn btn-success" onclick="javascript:submitBooking()">Salva</button>
                  <button type="button" class="btn btn-danger" onclick="javascript:hideBooking()">Annulla</button>
              </form>
          </div>
        </div>




        <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <div class="modal-header center">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h2 class="modal-title" id="myModalLabel">Nuova Prenotazione</h2>
              </div>
              <div class="modal-body">
                <form>
                  <div class="form-group">
                    <input type="text" class="form-control" id="nome" placeholder="Nome Cliente">
                  </div>
                  <div class="form-group">
                    <input type="text" class="form-control" id="telefono" placeholder="№ Telefono">
                  </div>
                  <div class="form-group">
                    <input type="text" class="form-control" id="arrivo" placeholder="Data di Arrivo">
                  </div>
                  <div class="form-group">
                    <input type="text" class="form-control" id="durata" placeholder="Durata del Soggiorno">
                  </div>
                  <div class="form-group">
                    <input type="text" class="form-control" id="posti" placeholder="Posti Prenotati">
                  </div>
                  <div class="form-group">
                    <input type="text" class="form-control" id="responsabile" placeholder="Responsabile Prenotazione">
                  </div>
                  <div class="checkbox">
                    <label>
                      <input type="checkbox"> Sono gestori
                    </label>
                  </div>
              </div>
              <div class="modal-footer center">
                <button type="button" class="btn btn-primary">Salva</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button>
                </form>
              </div>
            </div>
          </div>
        </div>





        <footer>
          <div class="footer-div">
            <? if ($ris == 1){ ?>
            <a href="javascript:makeBooking()" class="btn btn-success">Nuova Prenotazione Mio</a>
            <a href="javascript:makeBooking()" class="btn btn-danger" data-toggle="modal" data-target="#myModal">Nuova Prenotazione Bootstrap</a>
            <a href="main.php?ris=0" class="btn btn-danger" style='position:relative;float:right;'</a>Logout</a>
            <? }else{ ?>
            <a href="main.php?ris=1" class="btn btn-success">Area Riservata</a>
            <? } ?>
          </div>
        </footer>

      </div>

        <link href="static/css/datepickr.css" rel="stylesheet">
        <script type="text/javascript" src="static/javascript/datepickr.min.js"></script>
        <script type="text/javascript">
            new datepickr('arrivo', {
                'dateFormat': 'd/m/Y'
            });
        </script>

  </body>
</html>
