<?php
/****************************************************************************************************** */
/* RASDRIVE GLOBAL */
/****************************************************************************************************** */
session_start();
set_include_path(dirname(__FILE__));

include_once 'config.php';

//Adds all classes in folder "Model" in form "name.class.php"
function __autoload($class_name) {
	require_once 'model/'.$class_name.'.class.php';
}


