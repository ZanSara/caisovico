 <!-- MAIN TABLE -->
    <div class="row">
        <div id="calendario-box" class="calendario-outer-box shadow2">
          <table id="tableid" style="overflow:hidden;">
              <tr><td>
                <div class='scrollable'>
                <table class="calendario">
                    <tr>
                        <td class='giorno' style="border: 1px solid #fff;">Data</td>
                        <td class='gestore' style="border: 1px solid #fff;">Gestore</td>
                        <td class='letto'></td>
                        <td class='letto'></td>
                        <td class='letto'></td>
                        <td class='letto'></td>
                        <td class='letto'>Letti</td>
                        <td class='letto'></td>
                        <td class='letto'></td>
                        <td class='letto'></td>
                        <td class='letto'></td>
                        <td class='letto'></td>
                        <td class="emergenza" style="border-left: 1px solid #fff;"></td>
                        <td class="emergenza">Emergenza</td>
                        <td class="emergenza"></td>
                        <td class="emergenza"></td>
                        <td class="emergenza"></td>
                        <td class="emergenza"></td>
                    </tr>
                </table>
                </div>
              </td></tr>
              <tr><td>
                <div class="calendario-inner-box scrollable">
                <table class="calendario grid">
                  <colgroup>
                        <col class='giorno'>
                        <col class='gestore'>
                        <col class='letto'>
                        <col class='letto'>
                        <col class='letto'>
                        <col class='letto'>
                        <col class='letto'>
                        <col class='letto'>
                        <col class="letto">
                        <col class="letto">
                        <col class="letto">
                        <col class="letto">
                        <col class="emergenza">
                        <col class="emergenza">
                        <col class="emergenza">
                        <col class="emergenza">
                        <col class="emergenza">
                        <col class="emergenza">
                  </colgroup>
                  <tbody>
                  
                  <?
                    for($d = 0; $d < ($this->LastDay - $this->FirstDay); $d++){
                    
                        $fulldate = $this->Dates[$d];
                        
                        $absday = $fulldate[0];
                        $day = $fulldate[1];
                        $monthname = $fulldate[2][0].$fulldate[2][1].$fulldate[2][2]; // fix me
                        $monthnum = $fulldate[3];
                        $weekday = $fulldate[4];
                  
                        // Building tr
                        echo("<tr id='".$day."-0".$monthnum."'");
                            if( $day == 1 ) echo ("style='border-top: 4px solid black;'");
                            if( $absday == $this->LastDay-1 ) echo ("style='border-bottom: 4px solid #000;'");
                            if( $this->Today == $absday) echo("id='today' class='border'");
                        echo(">");

                        // Building Date td
                        echo("<td ");
                            if( $weekday == "S" ) echo("style='color:blue;'");
                            if( $weekday == "D" ) echo("style='color:red;'");
                            if( $monthname == "Ago" and $day==15 ) echo("style=color:red;text-decoration:underline;");
                        echo(">");
                            echo($day." ".$monthname." ".$weekday );//." / ".$absday);
                        echo("</td>");
                    
                    
                        // Building Gestore td
                        $gestore = $this->Gestori[$d];
                        $numGestori = $gestore[0];                        
                        if ($numGestori == 0){
                            echo("<td class='nogestore'>Nessuno!</td>");

                        } else {
                            $idGestore = $gestore[1];
                            $nomeGestore = $gestore[2];
                           
                            echo("<td class='P".$idGestore."' ");
                            if($numGestori > 1){
                                echo(" style='border:4px solid red;'");
                            }
                            if($idGestore == $this->LastPrenID){
                                echo(" style='border:4px solid yellow;'");
                            }
                            echo(">");
                            echo("<a id='".$absday."-G' onclick='javascript:openNewBookingModal(1, ".$idGestore.", 1);' ><div class='gestore-div'>");
                            echo($nomeGestore);
                            echo("</div></a>");
                            echo("</td>");
                        }
                        
                        
                        // Filling the rest of the table
                        $bookings = $this->Bookings[$d];
                        
                        $tot = 0;
                        foreach($bookings as $cell){
                            $tot++;
                            echo("<td class='P".$cell[0]."' style='background:".$cell[1].";");
                            if($cell[0] == $this->LastPrenID){
                                echo("border: yellow 4px solid;'>");
                            }else{
                                echo("'>");
                            }
                            echo("<a onclick='javascript:openNewBookingModal(1, ".$cell[0].", 0);' ><div class='booking-div'>");//<div style='border: red 1px solid;'>");
                            echo('P'.$cell[0]);
                            echo("</div></a>");
                            echo("</td>");
                        }
                        for(;$tot<16; $tot++){
                            echo ("<td></td>");
                        }

                        // Close tr
                        echo ("</tr>");       
                    
                    }
                                     
                  ?>
                  
                  </tbody>
                </table>
              </div>
            </td></tr>
          </tbody>
        </table>
        
        
        <!-- Move me somewhere else! -->
        <script type="text/javascript">

            // ************* STILL TO DO **************************************************************
            
            // Open Error_Modal in case of PHP errors (like "No more beds on these days")
            //if( $("#ErrorModal").data("error") ){
            //    $("#ErrorModal").modal("show");
            //}
            // Open Id_Modal in case of success of the registration
            //if( $("#IdModal").data("open") ){
            //    $("#IdModal").modal("show");
            //}
            
            // Reset Find_Modal when closed
            $("#FindModal").on("hidden.bs.modal", function (event) {
                resetFindModal();
            });

        </script>
        
        
      </div>
    </div>
