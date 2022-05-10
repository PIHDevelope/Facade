while($true){
	$login = (Read-Host Please enter login of user);
	try{
		Write-Host User: (Get-ADUser $login)
	}catch{
		Write-Host User with given login is not found
	}
}