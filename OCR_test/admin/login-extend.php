<?php
session_start();
include('includes/config.php');
$sql ="SELECT UserName, Password FROM admin WHERE UserName='{$_SESSION['user']}' and Password=md5('{$_SESSION['pass']}')";
//$query= $dbh -> prepare($sql);
//$query->bind_param("ss",$email,$password);

//$query-> bindParam(':email', $email);//, PDO::PARAM_STR);
//$query-> bindParam(':password', $password);//, PDO::PARAM_STR);
//$query-> execute();
$result = mysqli_query($dbh,$sql);
$ret = mysqli_num_rows($result);
if($ret)
{
$_SESSION['alogin']=$_SESSION['user'];
echo "<script type='text/javascript'> document.location = 'dashboard.php'; </script>";
} else{
  
  echo "<script>alert('Invalid Details');</script>";

}
?>
<!DOCTYPE html>
<html>
<head>
	<title>lala</title>
</head>
<body>
	<h1><?php echo $_SESSION['pass'] ?></h1>
</body>
</html>