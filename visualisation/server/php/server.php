<?php

if ($_SERVER['REQUEST_METHOD'] == 'POST'){
  // $data  = json_decode($_POST['data'], true);
  // print_r($_POST);
  try {
    $db = new PDO("pgsql:host=127.0.0.1:5432;dbname=bigdata", "", "");
    echo 'Connexion OK';
  }
  catch(PDOException $e) {
    $db = null;
    echo 'ERREUR DB: ' . $e->getMessage();
  }

  if($db) {
    echo json_encode("connexion ok");
  }
  echo json_encode($_POST);
}


?>
