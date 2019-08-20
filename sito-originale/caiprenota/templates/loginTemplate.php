<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Login Area Riservata - CAI Sovico</title>
     
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link href="<? echo STATICS ?>/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <link href="<? echo STATICS ?>/css/loginStyle.css" rel="stylesheet">
    <link href="<? echo STATICS ?>/css/calendarStyle.css" rel="stylesheet">
    
    <script src="<? echo STATICS ?>/javascript/jQuery/jquery-1.11.2.min.js"></script>
    <script src="<? echo STATICS ?>/bootstrap/js/bootstrap.min.js"></script>

  </head>

  <body class="text-center" >
    <div style="width:100%;color:#eee;margin-bottom:20px;">
        <h1 style="font-size:40pt;text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black;">Area Riservata</h1>
    </div>
    <div class="container">

      <form class="form-signin text-center shadow1" method='post'>
        <h3 class="form-signin-heading">Inserisci le tue credenziali</h3>
        <label for="username" class="sr-only">Username</label>
        <input type="text" id="username" name="username" class="form-control" placeholder="Username" required autofocus>
        <label for="password" class="sr-only">Password</label>
        <input type="password" id="password" name="password" class="form-control" placeholder="Password" required>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Accedi</button>
      
      
      
        <? if (parent::__get("FEEDBACK") != "Missing parameter" and parent::__get("SUCCESS") == 0){
            echo '<div class="alert alert-danger">';
            echo '<p style="color:#e00;">';
            echo parent::__get("FEEDBACK");
            echo "</p>";
            echo '</div>';
        } ?>
      
      </form>

    </div> <!-- /container -->
    
    

  </body>
</html>

