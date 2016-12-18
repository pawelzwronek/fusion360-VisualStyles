@prompt $g

set dst="VisualStyles_v1.2.2"

rmdir /S /Q %dst%
mkdir %dst%
mkdir %dst%\resources

copy VisualStyles_dev.py  %dst%\VisualStyles.py
xcopy /e resources %dst%\resources

pause
