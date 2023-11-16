$exe = 'python'
$venv = 'D:\projects\local_assistant\venv\Scripts\'
$script = 'Activate.ps1'
$py_script = 'D:\projects\local_assistant\assistant\main.py'

cd $venv
& .\$script

& $exe $py_script
pause