    <!-- ERROR ALERT -->
    <div class="modal fade" id="ErrorModal" data-error="0" tabindex="-1" role="dialog" aria-labelledby="ErrorModalLabel">
    
    <!-- data-error="<? if($this->error) {?>1<?}else{?>0<?}?>" -->
    
      <div class="modal-dialog modal-sm" role="document">
        <div class="modal-content text-center">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            <h3 class="modal-title" style='color:red;'><b>ERRORE</b></h3>
          </div>

          <div class="modal-body center" style='background:#FFE0E0'>
            <p id='errModal-message'><? echo $this->EXCEPTION; ?></p>
          </div>

          <div class="modal-footer text-center">
              <button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button>
          </div>

        </div>
      </div>
    </div>
