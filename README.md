# Lovemilk-MFFMv11-HarmonyOSSans
> 此模块可以将系统默认字体修改为 HarmonyOS Sans (简体中文 / 斜体) 和 JetBrains Mono NL (Monospace 字体) 字体 <br>
> 此模块由 [mistu01/mffmv11](https://github.com/mistu01/mffmv11) 模板修改而来. <br>
[上游模板项目的 READMD](./TEMPLATE-README.md)

## 安装前须知 (从模板项目复制, 请自行翻译) / Important Info Before Installation:
As of new changes the installation logic has changed dated: `11/22/2023` for seamless installation across KSU/Magisk/Newer android versions. With no font or font related module (that modifies `fonts.xml`) installed (if installed any uninstall all of them and reboot) open any Terminal app eg. `Termux` run this following command with root permission. 
```
su -c '
[ ! -d /sdcard/MFFM/fontsxml ] && mkdir -p /sdcard/MFFM/fontsxml
cp /system/etc/fonts.xml /sdcard/MFFM/fontsxml/fonts.xml
cp /product/etc/fonts_customization.xml /sdcard/MFFM/fontsxml/fonts_customization.xml'
```
You only need to do this once. Repeat this only if you change ROM! After this you are ready to install, update, dirty install, install `MFFMv12` modules without any trouble. 

### 简单概括: 您需要在安装前使用 Termux 运行上面代码块的指令

## 下载发行版中最新版本的 .zip 文件, 后直接刷入 Magisk / APatch / KSU 等框架重启后方可使用
