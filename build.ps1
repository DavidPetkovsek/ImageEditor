Set-Location -Path $PSScriptRoot
New-Item -ItemType Directory -Force -Path build
Set-Location -Path build
cmake .. -G Ninja
ninja