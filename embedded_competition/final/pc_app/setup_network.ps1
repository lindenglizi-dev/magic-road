param(
 [Parameter(Mandatory=$true)][int]$InterfaceIndex,
 [string]$LocalAddress='192.168.137.1',
 [string]$BoardAddress='192.168.137.2',
 [Parameter(Mandatory=$true)][string]$Report,
 [switch]$Elevated
)
$ErrorActionPreference='Stop'
function Write-Result($value){
 $json=$value | ConvertTo-Json -Depth 5
 [IO.File]::WriteAllText($Report,$json,[Text.UTF8Encoding]::new($false))
}
try {
 $localIp=[Net.IPAddress]::Parse($LocalAddress)
 $boardIp=[Net.IPAddress]::Parse($BoardAddress)
 if($localIp.AddressFamily -ne 'InterNetwork' -or $boardIp.AddressFamily -ne 'InterNetwork' -or $LocalAddress -eq $BoardAddress){throw 'Invalid local/board IPv4 addresses'}
 $admin=([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
 if(!$admin){
  if($Elevated){throw 'Windows did not grant administrator rights'}
  $arguments='-NoProfile -ExecutionPolicy Bypass -File "{0}" -InterfaceIndex {1} -LocalAddress "{2}" -BoardAddress "{3}" -Report "{4}" -Elevated' -f $PSCommandPath,$InterfaceIndex,$LocalAddress,$BoardAddress,$Report
  $process=Start-Process -FilePath "$env:SystemRoot/System32/WindowsPowerShell/v1.0/powershell.exe" -ArgumentList $arguments -Verb RunAs -WindowStyle Hidden -Wait -PassThru
  exit $process.ExitCode
 }
 $adapter=Get-NetAdapter -Physical | Where-Object {$_.ifIndex -eq $InterfaceIndex -and $_.InterfaceType -eq 6 -and $_.PhysicalMediaType -eq '802.3' -and $_.Status -eq 'Up'}
 if(!$adapter){throw 'Selected interface is not an active physical Ethernet adapter'}
 $other=Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object {$_.IPAddress -eq $LocalAddress -and $_.InterfaceIndex -ne $InterfaceIndex}
 if($other){throw 'Requested address is already assigned to a different interface'}
 $stored=Get-NetIPAddress -InterfaceIndex $InterfaceIndex -AddressFamily IPv4 -PolicyStore PersistentStore -ErrorAction SilentlyContinue | Where-Object {$_.IPAddress -eq $LocalAddress -and $_.PrefixLength -eq 24}
 if(!$stored){
  $response=& netsh interface ipv4 add address "name=$($adapter.Name)" "address=$LocalAddress" mask=255.255.255.0 store=persistent 2>&1
  if($LASTEXITCODE -ne 0){throw "netsh failed: $response"}
 }
 $active=Get-NetIPAddress -InterfaceIndex $InterfaceIndex -AddressFamily IPv4 -PolicyStore ActiveStore -ErrorAction SilentlyContinue | Where-Object {$_.IPAddress -eq $LocalAddress -and $_.PrefixLength -eq 24}
 if(!$active){
  $response=& netsh interface ipv4 add address "name=$($adapter.Name)" "address=$LocalAddress" mask=255.255.255.0 store=active 2>&1
  if($LASTEXITCODE -ne 0){throw "netsh active address failed: $response"}
 }
 $ready=$false
 for($i=0;$i -lt 15;$i++){
  $active=Get-NetIPAddress -InterfaceIndex $InterfaceIndex -AddressFamily IPv4 -PolicyStore ActiveStore -ErrorAction SilentlyContinue | Where-Object {$_.IPAddress -eq $LocalAddress}
  if($active.AddressState -eq 'Preferred'){$ready=$true;break}
  if($active.AddressState -eq 'Duplicate'){throw 'Duplicate IP address detected on the Ethernet segment'}
  Start-Sleep -Milliseconds 500
 }
 $stored=Get-NetIPAddress -InterfaceIndex $InterfaceIndex -AddressFamily IPv4 -PolicyStore PersistentStore -ErrorAction SilentlyContinue | Where-Object {$_.IPAddress -eq $LocalAddress}
 if(!$ready -or !$stored){throw 'Address did not become preferred in both active and persistent configuration'}
 Write-Result @{ok=$true;interface=$adapter.Name;index=$InterfaceIndex;address=$LocalAddress;prefix=24;persistent=$true}
 exit 0
}catch{
 Write-Result @{ok=$false;error=$_.Exception.Message}
 exit 1
}
