    <script type="text/javascript">
    // jQuery validation plugin settings

        var now     = new Date();
        var year    = now.getFullYear();

        $.validator.addMethod("customData", function(value) {
        var re = new RegExp("^(((0[1-9]|1[0-9]|2[0-9]|30)-(0[6-9]))|((31)-(0[7-8])))-"+year+"$")
            return re.test(value);
        }, 'Inserire una data di arrivo valida (GG-MM-AAAA) compresa tra 01-06-'+year+' e 30-09-'+year);

        $().ready(function() {
            $("#booking-form").validate({
                //debug: true,
                errorElement: "li",
                errorContainer: $("#message-alert"),
                errorPlacement: function(error) {
                  $("#message-alert").show();
                    $("#message-alert").append(error);
                }
            });
        });
    </script>
    
    <h2><? echo($this->Titolo) ?></h2>
    <hr>

      <form id='booking-form' class='form-horizontal' method='POST'>
        <div id="message-alert" class="alert alert-danger" role="alert" style='display:none; padding-left:10%;padding-right:10%;'></div>

        <div class="form-group">
          <label class="col-sm-3 control-label">Data di Inizio</label>
          <div class="col-sm-9" >
              <input id="inizio" type="text" class="form-control" name="inizio" placeholder="Giorno-Mese-Anno" value="01-06-<? echo (date('Y')); ?>"
              data-rule-required="true" data-msg-required="Inserire una data di inizio gestione"
              data-rule-customData="true">
          </div>
        </div>
        <div class="form-group">
          <label class="col-sm-3 control-label">Data di Fine</label>
          <div class="col-sm-9" >
              <input id="fine" type="text" class="form-control" name="fine" placeholder="Giorno-Mese-Anno" value="30-09-<? echo (date('Y')); ?>"
              data-rule-required="true" data-msg-required="Inserire una data di fine gestione"
              data-rule-customData="true">
          </div>
        </div>
        <div class="form-group col-sm-3">
        </div>
        <div class="form-group col-sm-9 pull-right">
          <input class="btn btn-default" type="submit" value="Invia">
          <a class="btn btn-default" href="<? echo ROOT ?>/calendar/#<? echo date('j-n', strtotime('yesterday')); ?>">Torna Indietro</a>
        </div>
      </form>
