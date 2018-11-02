<?php
    header('Content-Type: applications/json');
    $pdo=new PDO("mysql:dbname=Sistema;host=127.0.0.1","root","");


    $accion=(isset($_GET['accion']))?$_GET['accion']:'leer';
    switch($accion){
        case 'signin':
            //Instruccion sign
            $sentenciaSQL = $pdo->prepare("INSERT INTO registros(username,password) VALUES(:username,:password)");

            $respuesta=$sentenciaSQL->execute(array(
                "ID" => $_POST['id'],
                "username" => $_POST['username'],
                "password" => $_POST['password'],
            ));
            echo json_encode($respuesta);
            break;




        default:
            //seleccioar eventos del calendario
            $sentenciaSQL= $pdo->prepare("SELECT * FROM registros");
            $sentenciaSQL->execute();

            $resultado= $sentenciaSQL->fetchAll(PDO::FETCH_ASSOC);
            echo json_encode($resultado);
            break;

    }


?>