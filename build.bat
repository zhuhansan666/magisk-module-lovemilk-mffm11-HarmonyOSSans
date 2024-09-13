set workdir=%~dp0%
@REM cd 是为了避免压缩包内由文件夹
cd mffm11_v2024.04.04_HarmonyOSSans/
7z a ../dist/mffm11_v2024.04.04_HarmonyOSSans.zip ./*
cd %workdir%
