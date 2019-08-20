    <!-- NEW BOOKING MODAL -->
    <div class="modal fade" id="newBookingModal" tabindex="-1" role="dialog" aria-labelledby="newBookingModalLabel" data-fillme=0, data-prenid=0, data-gestione=0>
      <div class="modal-dialog" role="document">
        <div class="modal-content">

          <div class="modal-header center-text">
            <!-- modal titles -->
            <h2 id="nBM-dataTitle" class="modal-dataTitle modal-title">Prenotazione</h2>
            <h2 id="nBM-loadingTitle" class="modal-title" style='display:none;'>Caricamento...</h2>
            <h2 id="nBM-errorTitle" class="modal-title" style='display:none;'>Errore!</h2>
            <!-- top buttons -->
            <a id="nBM-ModificaBtn" class="btn btn-warning" href="javascript:nBM_enableEditing();">Modifica</a>
            <button id="nBM-ChiudiTopBtn" class="btn btn-default" data-dismiss="modal">Chiudi</button>

          </div>

          <form id="nBM-form" class='form-horizontal' method='POST' onsubmit="return validate();">
            <div class="modal-body">
              
              <!-- main form -->
              <div id="nBM-mainForm" class="modal-databox" >
                <div class="form-group">
                    <div class="col-sm-offset-3 col-sm-9 checkbox">
                      <label>
                        <input id="nBM-gestioneChk" name='gestione' type="checkbox" onclick="javascript:toggleGestione();"> Sono gestori
                      </label>
                    </div>
                </div>
                <hr />
                <div class="form-group" >
                  <label class="col-sm-3 control-label">Nome Cliente</label>
                  <div class="col-sm-9" >
                      <input id="nBM-nome" type="text" class="form-control" name="nome" placeholder="Nome Cliente" readonly="readonly">
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-3 control-label">№ Telefono</label>
                  <div class="col-sm-9" >
                      <input id="nBM-tel" type="text" class="form-control" name="telefono" placeholder="№ Telefono" readonly="readonly"">
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-3 control-label">Provincia di Residenza</label>
                  <div class="col-sm-9" >
                      <input id="nBM-provincia" type="text" class="form-control" name="provincia" placeholder="Codice Provincia" readonly="readonly">
                      <!-- data-rule-required="true" data-msg-required="Inserire la provincia di residenza" -- RIMOSSO NELLA VERSIONE 2.3 -->
                  </div>
                </div>
                <hr/>
                <div class="form-group">
                  <label class="col-sm-3 control-label">Data di Arrivo</label>
                  <div class="col-sm-9">
                      <label id="nBM-arrivoLbl" class="control-label">Javascript not working...</label>
                      <script> 
                          $("#nBM-arrivoLbl").text( "Clicca sui bottoni per comporre la data" ); 
                      </script> 
                      <input id="nBM-arrivo" class="form-control hidden" type="text" name="arrivo" readonly="readonly">
                 </div>
                 <div id="nBM-arrivoBtn" class="col-sm-9 pull-right" style="padding:0;" style="display:hidden;">
                      <div class="col-sm-9" style="padding-right:2%; padding-top:2%;">
                        <?
                            $day = 0;
                            for($row = 0; $row < 4 ;$row++){
                                
                                echo '<div class="btn-group btn-group-justified" role="group" aria-label="..." style="margin-bottom:-1px;">';
                                for($num = 0; $num < 8 ;$num++){
                                    $day++;
                                    
                                    $day2digits = $day;
                                    if ($day < 10) { 
                                        $day2digits = "0".$day; 
                                    }
                                    
                                    echo '<a href="#" id="btnDay-'.$day2digits.'" class="btn btn-default" role="button" onclick="javascript:setDay('.$day2digits.')">'.$day2digits.'</a>';
                                }
                                echo "</div>";
                            }
                        ?>                     
                      </div>
                      <div class="col-sm-3" style="padding-left:2%; padding-top:2%;">
                        <div class="btn-group btn-group-vertical" role="group" aria-label="...">
                          <a href="#" id="btnMonth-Giu" class="btn btn-default" role="button" onclick="javascript:setMonth(6)">Giugno</a>
                          <a href="#" id="btnMonth-Lug" class="btn btn-default" role="button" onclick="javascript:setMonth(7)">Luglio</a>
                          <a href="#" id="btnMonth-Ago" class="btn btn-default" role="button" onclick="javascript:setMonth(8)">Agosto</a>
                          <a href="#" id="btnMonth-Set" class="btn btn-default" role="button" onclick="javascript:setMonth(9)">Settembre</a>
                        </div>
                      </div>
                  </div>
                </div>
                
                <div class="form-group">
                  <label class="col-sm-3 control-label">Durata del Soggiorno</label>
                  <div class="col-sm-9" >
                    <div class="input-group">
                      <input id="nBM-durata" type="text" class="form-control" name="durata" placeholder="Durata del Soggiorno" readonly="readonly">
                      <span class="input-group-addon">notti</span>
                    </div>
                  </div>
                </div>
                <div class="form-group" id="nBM-linePosti">
                  <label class="col-sm-3 control-label">Posti Prenotati</label>
                  <div class="col-sm-9" >
                      <label id="nBM-postiLbl" class="control-label">Javascript not working...</label>
                      <script> 
                          $("#nBM-postiLbl").text( "Clicca sul numero di posti prenotati" ); 
                      </script>
                      <input id="nBM-posti" type="text" class="form-control hidden" name="posti" placeholder="Posti Prenotati" readonly="readonly">
                      <div id="nBM-postiBtn" style="display:hidden; padding-top:2%;" >
                        <?
                            $bed = 0;
                            for($row = 0; $row < 2 ;$row++){
                                
                                echo '<div class="btn-group btn-group-justified" role="group" aria-label="...">';
                                for($num = 0; $num < 8 ;$num++){
                                    $bed++;
                                    echo '<a href="#" id="btnPosti-'.$bed.'" class="btn btn-default" role="button" onclick="javascript:setPosti('.$bed.')">'.$bed.'</a>';
                                }
                                echo "</div>";
                            }
                        ?>
                      </div>
                  </div>
                </div>
                
                <hr/>
                <div class="form-group">
                  <label class="col-sm-3 control-label">Responsabile Prenotazione</label>
                  <div class="col-sm-9" >
                      <input id="nBM-resp" type="text" class="form-control" name="responsabile" placeholder="Responsabile Prenotazione" readonly="readonly">
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-3 control-label">Note</label>
                  <div class="col-sm-9" >
                      <textarea id="nBM-note" type="textarea" rows="3" class="form-control" name="note" placeholder="Note..." readonly="readonly"></textarea>
                  </div>
                </div>
                <div class="hidden">
                  <input id="nBM-prenid" name='prenid' type="text" readonly="readonly">
                </div>
              </div> <!-- modal-databox -->
              
              <!-- User feedback -->
              <div id="nBM-jsFeedback" class="alert alert-danger" role="alert" style="display:none; padding-left:10%;padding-right:10%;"></div>
              
              <!-- Loading box -->
              <img id="nBM-spinningWheel" class="spinningWheel" src="<? echo STATICS ?>/images/spinningwheel.gif"style='display:none;' />
              
              <!-- Error reporting elements-->
              <div id="nBM-errorBox" style='display:none;'>
                <div id="nBM-errorAlert" class="alert alert-danger center-text" role="alert" ></div>
              </div>
              
              <!-- Footer -->
              <div class="modal-footer center-text">
                <input id="nBM-SalvaBtn" class="btn btn-primary" disabled="disabled" type="submit" style="display:none;" value='Salva'>
                <a id="nBM-EliminaBtn" class="btn btn-danger" href="javascript:prepareDelete()" style="display:none;">Elimina</a>

                <!-- This one should be always visible - thus no ID -->
                <button class="btn btn-default" data-dismiss="modal">Chiudi</button>
              </div>
              

            </div>
          </form>
        </div>
      </div>
    </div>
    
    
    <script type="text/javascript">

        // Reset NewB_Modal when closed
        $("#newBookingModal").on("hidden.bs.modal", function (event) {
            
            // Reset titles
            $("#nBM-dataTitle").show();
            $("#nBM-dataTitle").text("Prenotazione");
            $("#nBM-loadingTitle").hide();
            $("#nBM-errorTitle").hide();
            
            // Reset Top Buttons
            $("#nBM-ChiudiTopBtn").hide();
            $("#nBM-ModificaBtn").hide();
            
            // Reset body
            $("#nBM-errorBox").hide();
            $("#nBM-spinningWheel").hide();
            $("#nBM-mainForm").show();
            $("#newBookingModal form")[0].reset();
            $("#newBookingModal input").prop("readonly", true);
            $("#newBookingModal textarea").prop("readonly", true);
            $("#nBM-gestioneChk").prop("disabled", "" );
            $("#nBM-gestioneChk").prop("checked", "" );
            $("#nBM-linePosti").show();
            
            // Reset labels
            $("#nBM-arrivoLbl").text("Clicca sui bottoni per comporre la data");
            $("#nBM-postiLbl").text("Clicca sul numero di posti prenotati");
            
            // Show buttons
            $("#nBM-arrivoBtn").hide();
            $("#nBM-postiBtn").hide();

            // Reset footer
            $("nBM-SalvaBtn").hide();
            $("nBM-EliminaBtn").hide();
        });
        
    </script>
