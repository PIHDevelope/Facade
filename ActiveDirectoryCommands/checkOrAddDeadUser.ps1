.\config.ps1
while($true){
	$userSurname = (Read-Host "Please enter surname of user")
	$userSurname = $userSurname + "*"
	$userAccountNameList = (Get-ADUser -Filter {Surname -like $userSurname})
	if($userAccountNameList.Length -eq 0)
	{
		Write-Host User with given surname is not found
	}else{
		$deadUserList = @()
		foreach($user in $userAccountNameList)
		{
			if($user.DistinguishedName.Contains($DEADLIST_MARK))
			{
				$user | select SamAccountName, name | Format-Table
				$deadUserList += $user | select SamAccountName, name
			}else{
				Write-Host in DeadList
				$user | select SamAccountName, name | Format-Table
				$answer = (Read-Host "Disable and add to deadlist? Y(Yes|1), N(No)")
				$answer = $answer.ToLower()
				if(($answer -eq "y") -or ($answer -eq "yes") -or ($answer -eq "1")){
					Get-aduser $user.SamAccountName | Disable-ADAccount | Move-ADObject -TargetPath $DEADLIST_OU
					Write-Host Done!
				}else{
					if(($answer -eq "n") -or ($answer -eq "no")){
						Write-Host Cancel!
					}
				}
			}
		}
	}
}