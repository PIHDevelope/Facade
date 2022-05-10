while($true){
	$userSurname = (Read-Host Please enter surname of user);
	$userSurname = $userSurname + "*";
	$userList = (Get-ADUser -Filter {Surname -like $userSurname} -properties TelephoneNumber) | Sort-Object Enabled, Name ;
	if($userList.Length -eq 0)
	{
		Write-Host User with given surname is not found
	}else{
		$userSamAccountNameList = @()
		$userListResult = @()
		foreach($user in $userList)
		{
			$userSamAccountNameList += ($user | select SamAccountName);
			$userListResult += ($user | select SamAccountName, Name, Enabled, TelephoneNumber, DistinguishedName);
		}
		$userListResult | Format-Table
	}
}