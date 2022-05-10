Function ADResolve ([String[]]$list) {
    ForEach($userSurname in $list)
	{
		$userAccountNameList = (Get-ADUser -Filter {Surname -eq $userSurname}).SamAccountName
		if($userAccountNameList.Length -eq 0)
		{
			Write-Host User with given surname is not found
		}else
		{
			$deadUserList = @()
			foreach($userAccountName in $userAccountNameList)
			{
				$user = Get-ADUser $userAccountName 
				if($user.DistinguishedName.Contains("deadlist"))
				{
					Write-Host User: $user.SamAccountName is in DeadList
					$deadUserList += $user
				}else{
					Write-Host User is not in DeadList
					Write-Host Get-aduser $user
					$answer = (Read-Host "Disable and add to deadlist? Y(Yes|1), N(No)")
					$answer = $answer.ToLower()
					if(($answer -eq "y") -or ($answer -eq "yes") -or ($answer -eq "1"))
					{
						Get-aduser $user.SamAccountName | Disable-ADAccount
						Get-aduser $user.SamAccountName | Move-ADObject -TargetPath 'OU=deadlist,DC=fmv,DC=lan'
						Write-Host Done!
					}else{
						if(($answer -eq "n") -or ($answer -eq "no"))
						{
							Write-Host Goodbye!
						}
					}
				}
			}
		}
	}
}
#C = A - B
Write-Host C = A - B
$aPath = Read-Host "Please enter A file"
if(Test-Path -Path $aPath)
{
	$bPath = Read-Host "Please enter B file"
	if( Test-Path -Path $bPath)
	{
		[string[]]$aSource = Get-Content -Path $aPath
		[string[]]$bSource = Get-Content -Path $bPath
		$aSource = $aSource | ForEach-Object {$PSItem.toLower()}
		$bSource = $bSource | ForEach-Object {$PSItem.toLower()}
		$a = $aSource
		$b = $bSource
		$a = $a | ForEach-Object {$PSItem.split(" ")[0..2] -join(" ")}
		$b = $b | ForEach-Object {$PSItem.split(" ")[0..2] -join(" ")}
		$c = ($a | ? {$_ -notin $b})| ForEach-Object {$PSItem.split(" ")[0]}
		Write-Host step 1: C items not in live list -fore DarkBlue
		$index = 1
		$waitForResolve = @()
		$c | ForEach-Object{ 
			Write-Host $index".[Loking for "$PSItem"]"
			$user = Get-ADUser -Filter {Surname -eq $PSItem} -SearchBase "ou=deadlist,dc=fmv,dc=lan"
			if($user -eq $NULL)
			{
				if((Get-ADUser -Filter {Surname -eq $PSItem} -SearchBase "ou=Unit,dc=fmv,dc=lan") -eq $NULL){
					Write-Host User is not exists -fore yellow
				}else{
					Write-Host User is alive -fore red
					$waitForResolve += $PSItem
				}
			}else{
				Write-Host User in deadlist -fore green
			}
			Write-Host _________________________
			$index++
		}
		ADResolve $waitForResolve
		Write-Host step 2: B items in live list -fore DarkBlue
		$bSamAccountNameList = @()
		$b | ForEach-Object{
			$userSurname = $PSItem.split(" ")[0]
			$user = Get-ADUser -Filter {Surname -eq $userSurname} -SearchBase "ou=Unit,dc=fmv,dc=lan"
			$samAccountName = $user.SamAccountName
			$bSamAccountNameList += $samAccountName
			if($user -eq $NULL){
				Write-Host User $userSurname is not exists -fore red
			}else{
				Write-Host User $samAccountName is alive -fore green
			}
		}
		Write-Host  step 3: show last users -fore DarkBlue
		$waitForResolve = @()
		$liveUsers = (Get-ADUser -Filter * -SearchBase "ou=Unit,dc=fmv,dc=lan").SamAccountName
		$lastUsers = $liveUsers | ? {$_ -notin $bSamAccountNameList}
		$lastUsers | ForEach-Object{
			$user = Get-ADUser $PSItem
			$distinguishedName = $user.DistinguishedName.toLower()
			$samAccountName = $user.SamAccountName.toLower()
			if ($distinguishedName.Contains("robots")){
				Write-Host User $user.SamAccountName is robot -fore green
			}elseif ($samAccountName -eq "mri")
			{
				Write-Host User $user.SamAccountName is $user.Name -fore green
			}elseif ($samAccountName -eq "ca")
			{
				Write-Host User $user.SamAccountName is $user.Name -fore green
			}elseif ($samAccountName -eq "stock")
			{
				Write-Host User $user.SamAccountName is $user.Name -fore green
			}elseif ($samAccountName -eq "zhdanov.o")
			{
				Write-Host User $user.SamAccountName is $user.Name -fore green
			}elseif ($samAccountName -eq "skoraya")
			{
				Write-Host User $user.SamAccountName is $user.Name -fore green
			}elseif ($samAccountName -eq "cctv")
			{
				Write-Host User $user.SamAccountName is $user.Name -fore green
			}elseif ($samAccountName -eq "nurse")
			{
				Write-Host User $user.SamAccountName is $user.Name -fore green
			}elseif ($samAccountName -eq "meeting")
			{
				Write-Host User $user.SamAccountName is $user.Name -fore green
			}elseif ($samAccountName -eq "security")
			{
				Write-Host User $user.SamAccountName is $user.Name -fore green
			}elseif ($samAccountName -eq "out1c")
			{
				Write-Host User $user.SamAccountName is $user.Name -fore green
			}
			else
			{
				$waitForResolve += $user.Surname
				Write-Host User $user.SamAccountName $user.Name is exists -fore red
			}
		}
		Write-Host step 4: last users not in live list -fore DarkBlue
		ADResolve $waitForResolve
	}else{
		Write-Host File not found -fore red
	}
}else{
	Write-Host File not found -fore red
}