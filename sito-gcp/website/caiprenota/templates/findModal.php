    <!-- FIND MODAL -->
    <div class="modal fade" id="FindModal" tabindex="-1" role="dialog" aria-labelledby="FindModalLabel" data-fillme=0, data-prenid=0, data-gestione=0>
      <div class="modal-dialog" role="document">
        <div class="modal-content">

          <div class="modal-header text-center">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            <h2 id="FM_dataTitle" class="modal-title">Cerca</h2>
            <h2 id="FM_loadingTitle" class="modal-title" style='display:none;'>Caricamento...</h2>
          </div>

          <div class="modal-body">
                      
          <!-- Find Interface -->  
          <!--form id='find-form' class='form-horizontal' method='GET'-->
            <div id="FM_warning" class="alert alert-warning" role="alert" style="padding-left:10%;padding-right:10%;">
              <p>Attenzione! Se non compili nessun campo, ti verranno mostrate tutte le prenotazioni di questa stagione.</p>
            </div>
            <div id="FM_formBox" class="modal-databox" >
              <div class="row" >
                <label class="col-sm-3 control-label">Numero Pren.</label>
                <div class="col-sm-9" >
                    <input id="FM_id" type="text" class="mod-prenid form-control" name="prenid" placeholder="Numero Prenotazione">
                </div>
              </div>
              <div class="row" >
                <label class="col-sm-3 control-label">Nome Cliente</label>
                <div class="col-sm-9" >
                    <input id="FM_nome" type="text" class="mod-nome form-control" name="nome" placeholder="Nome Cliente">
                </div>
              </div>
              <div class="row">
                <label class="col-sm-3 control-label">№ Telefono</label>
                <div class="col-sm-9" >
                    <input id="FM_tel" type="text" class="mod-tel form-control" name="telefono" placeholder="№ Telefono">
                </div>
              </div>
              <div class="row">
                <label class="col-sm-3 control-label">Data di Arrivo</label>
                <div class="col-sm-9" >
                    <input id="FM_arrivo" type="text" class="mod-arrivo form-control" name="arrivo" placeholder="Giorno-Mese-Anno">
                </div>
              </div>
              
              <div class="center" style="padding: 15px;">
              <a href=# class="btn btn-default" onclick="javascript:$('#findothers').toggle();">Parametri Avanzati</a>
              </div>
                
              <div id="findothers" style='display:none;'>
                  <div class="row">
                    <label class="col-sm-3 control-label">Provincia</label>
                    <div class="col-sm-9" >
                        <input id="FM_prov" type="text" class="mod-prov form-control" name="provincia" placeholder="Codice Provincia">
                    </div>
                  </div>
                  <div class="row">
                    <label class="col-sm-3 control-label">Durata Soggiorno</label>
                    <div class="col-sm-9" >
                        <input id="FM_durata" type="text" class="mod-durata form-control" name="durata" placeholder="Durata del Soggiorno">
                    </div>
                  </div>
                  <div class="row">
                    <label class="col-sm-3 control-label">Posti Prenotati</label>
                    <div class="col-sm-9" >
                        <input id="FM_posti" type="text" class="mod-posti form-control" name="posti" placeholder="Posti Prenotati">
                    </div>
                  </div>
                  <div class="row">
                    <label class="col-sm-3 control-label">Responsabile</label>
                    <div class="col-sm-9" >
                        <input id="FM_resp" type="text" class="mod-resp form-control" name="responsabile" placeholder="Responsabile Prenotazione">
                    </div>
                  </div>
                  <div class="row">
                    <label class="col-sm-3 control-label">Note</label>
                    <div class="col-sm-9" >
                        <textarea id="FM_note" type="textarea" rows="3" class="mod-note form-control" name="note" placeholder="Note..."></textarea>
                    </div>
                  </div>
                </div>
              
                
              </div> <!-- modal-databox -->
              
              <img id="FM_spinningWheel" class="loading" src="<? echo STATICS ?>/images/spinningwheel.gif" style='width:40%; margin-left:30%;margin-right:30%; display:none;' />
              <div id="FM_errorAlert" class="alert alert-danger" role="alert" style='display:none; text-align:center;'></div>
              <!--div id="FM_message-alert" class="alert alert-danger" role="alert" style='display:none; padding-left:10%;padding-right:10%;'></div-->


              <!-- Results Interface -->
              <div id="FM_resultsBox" class="text-center" style='display:none;'>
                  <p>Ho trovato <b><span id="FM_NumResults"></span></b> prenotazioni che corrispondono ai tuoi criteri di ricerca.<p>
                  
                  <table id="FM_resultsTable" class="table table-hover center">
                    <tr>
                       <th>Numero</th>
                       <th>Nome</th>
                       <th>Telefono</th>
                       <th>Arrivo</th>
                       <th>Durata</th>
                       <th>Posti</th>
                       <th></th>
                    <tr>
                  </table>
              </div>

              <div id="FM_formFooter" class="modal-footer center">
                <button id="FM_CercaBtn" class="btn btn-primary" onclick="javascript:collectAndFind();">Cerca</button>
                <button class="btn btn-default" data-dismiss="modal" >Chiudi</button>
              </div>
              <div id="FM_resultsFooter" class="modal-footer center" style='display:none;'>
                <button class="btn btn-default" data-dismiss="modal" >Chiudi</button>
              </div>
              <div id="FM_errFooter" class="text-center" style='display:none;'>
                <button class="btn btn-danger" data-dismiss="modal">Chiudi</button>
              </div>

          <!--/form-->
          </div>
          
        </div>
      </div>
    </div>
