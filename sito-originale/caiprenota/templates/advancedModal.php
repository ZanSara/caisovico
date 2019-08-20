    <!-- ADVANCED MODAL -->
    <div class="modal fade" id="Adv_Modal" tabindex="-1" role="dialog" aria-labelledby="Adv_ModalLabel">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header text-center">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            <h2 class="modal-title">Funzioni Avanzate</h2>
            <!--h4 class="modal-title" style="color:red;">Attenzione! Usare con cautela!</h4-->
          </div>

          <div class="modal-body">

            <div style="padding-left:5%;padding-right:5%;" >
              <div class="row">
                <a class="col-sm-3 btn btn-info" href="<? echo ROOT; ?>/prenotazioni/">Calendario</a>
                <p class="col-sm-8 ">Genera una tabella stampabile delle prenotazioni di ogni gestore.</p>
              </div>
              <hr>
              <div class="row">
                <a class="col-sm-3 btn btn-success" href="<? echo ROOT; ?>/ospiti/">Tabella Ospiti</a>
                <p class="col-sm-8">Genera una tabella stampabile di tutti gli ospiti che hanno pernottato al rifugio durate questa stagione.</p>
              </div>
              <!--hr>
              <div class="row">
                <a class="col-sm-3 btn btn-danger" href="erase-database-stage1">Svuota Database</a>
                <p class="col-sm-8">Svuota completamente il database delle prenotazioni.<br>ATTENZIONE! Questa operazione è IRREVERSIBILE!</p>
              </div-->
            </div>
            
            <div class="modal-footer center">
              <button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button>
            </div>

          </div>
          
        </div>
      </div>
    </div>
