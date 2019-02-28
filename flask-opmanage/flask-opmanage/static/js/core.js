/*
**  HoorayOS开源桌面应用框架
**  作者：胡尐睿丶
**  地址：http://hoorayos.com
**  我希望能将这项目继续开源下去，所以请手下留情，保留以上这段版权信息，授权用户可删除代码中任何信息
*/

var version   = '2.1.1';        //版本号
var ajaxUrl   = 'ajax.php';     //所有ajax操作指向页面
var zoomlevel = 1;
var TEMP      = {};
var HROS      = {};
var desk = $(".desktop-container").attr("id").split("-")[1];
HROS.CONFIG = {
	memberID        : 0,        //用户id
	desk            : desk,        //当前显示桌面
	dockPos         : 'top',    //应用码头位置，参数有：top,left,right
	appXY           : 'y',      //图标排列方式，参数有：x,y
	appButtonTop    : 20,       //快捷方式top初始位置
	appButtonLeft   : 20,       //快捷方式left初始位置
	createIndexid   : 1,        //z-index初始值
	windowMinWidth  : 215,      //窗口最小宽度
	windowMinHeight : 59,       //窗口最小高度
	wallpaper       : '',       //壁纸
	wallpaperWidth  : 0,        //壁纸宽度
	wallpaperHeight : 0,        //壁纸高度
	wallpaperType   : '',       //壁纸显示类型，参数有：tianchong,shiying,pingpu,lashen,juzhong
	wallpaperState  : 1         //1系统壁纸 2自定义壁纸 3网络壁纸
};