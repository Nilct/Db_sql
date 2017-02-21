<?php
try {
  $db = new PDO("pgsql:host=localhost;dbname=bigdata", "postgres");
  echo 'Connexion OK';
}
catch(PDOException $e) {
  $db = null;
  echo 'ERREUR DB: ' . $e->getMessage();
}

if($db) {
  echo json_encode("connexion ok");
}
?>
