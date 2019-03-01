$(document).ready(function() {
	$("#loginSubmit").bind("click", function() {
				var gameId = $("#gameId").val();
				var agent = $("#agent").val();
				var server = $("#server").val();
				var username = $("#username").val();

				if (gameId == null || gameId == "") {
					alert("游戏id 不能为空!");
					return false;
				}

				if (agent == null || agent == "") {
					alert("平台 不能为空!");
					return false;
				}

				if (server == null || server == "") {
					alert("区服 不能为空!");
					return false;
				}

				if (username == null || username == "") {
					alert("帐号不能为空!");
					return false;
				}

				var pass = $("#pass").val();
				$.ajax({
							"type" : "POST",
							"url" : "/MPP/quickLoginManage/quickLoginSubmit.action",
							"dataType" : "json",
							"data" : {
								gameId : gameId,
								agent : agent,
								server : server,
								username : username,
								pass : pass
							},
							"success" : function(msg) {
								$("#ip").val(msg["ip"]);
								$("#loginUrl").val(msg["loginUrl"]);
								$("#loginUrl2").val(msg["loginUrl2"]);
							}
						});

			});
	$("#rechargeSubmit").bind("click", function() {
		var gameId = $("#gameId").val();
		var agent = $("#agent").val();
		var server = $("#server").val();
		var username = $("#username").val();

		if (gameId == null || gameId == "") {
			alert("游戏id 不能为空!");
			return false;
		}

		if (agent == null || agent == "") {
			alert("平台 不能为空!");
			return false;
		}

		if (server == null || server == "") {
			alert("区服 不能为空!");
			return false;
		}

		if (username == null || username == "") {
			alert("帐号不能为空!");
			return false;
		}

		$.ajax({
					"type" : "POST",
					"url" : "/MPP/rechargeTestManage/rechargeTestSubmit.action",
					"dataType" : "json",
					"data" : {
						gameId : gameId,
						agent : agent,
						server : server,
						username : username
					},
					"success" : function(msg) {
						$("#loginUrl").val(msg["loginUrl"]);
						$("#loginUrl2").val(msg["loginUrl2"]);
					}
				});

	});
	$("#agentMake").bind("click", function() {
		var gameId = $("#gameId").val();
		var agent = $("#agent").val();
		var agentName = $("#agentName").val();
		var domain = $("#gameDomainList").val();
		var cdn = $("#CDNList").val();
		var isMake = 0;
		if($("#isMake").is(":checked")){
			isMake = 1;
		}
		if (gameId == null || gameId == "") {
			alert("游戏id 不能为空!");
			return false;
		}

		if (agent == null || agent == "") {
			alert("平台 不能为空!");
			return false;
		}

		if (agentName == null || agentName == "") {
			alert("平台 名称不能为空!");
			return false;
		}

		location.href = "/MPP/agentManage/agentManage.action?gameId=" + gameId
				+ "&agent=" + agent + "&agentName=" + agentName + "&domain="+domain+"&cdn="+cdn+"&isMake="+isMake;

	});
	
	$("#makeActionCard").bind("click", function() {
		var gameId = $("#gameId").val();
		var agent = $("#agent").val();
		var dis = $("#dis").val();
		var count = $("#count").val();
		var cardId = $("#cardId").val();
		var serverId = $("#serverId").val();
		var type = "0";
		var ad = "0";
		var limitTime = "0";
		if(gameId==="1"||gameId==="2"||gameId==="3"){
			type = $("#type").val();	
		}else if(gameId==="4"||gameId==="5"){
		 	ad = $("#ad").val();
			limitTime = $("#limitTime").val();
			if(limitTime===null||limitTime===""){
				limitTime = 12;
			}
		}
		
		
		if (gameId == null || gameId == "") {
			alert("游戏id 不能为空!");
			return false;
		}

		if (agent == null || agent == "") {
			alert("平台 不能为空!");
			return false;
		}

		if (count == null || count == "") {
			alert("数量不能为空!");
			return false;
		}else if(count>20000){
			alert("每次生成不能超过20000条");
			return false;
		}
		
		if (cardId == null || cardId == "") {
			alert("CardId不能为空!");
			return false;
		}
		if (serverId == null || serverId == "") {
			serverId = "0";
		}
		

		$.ajax({
				"type" : "POST",
				"url" : "/MPP/makeActionCard/makeActionCardSubmit.action",
				"dataType" : "json",
				"contentType" : "application/x-www-form-urlencoded; charset=utf-8", 
				"data" : {
					gameId : gameId,
					agent : agent,
					serverId : serverId,
					dis : dis,
					count : count,
					cardId : cardId,
					type : type,
					ad : ad,
					limitTime : limitTime
				},
				"success" : function(msg) {
					$("#showLog").val("点击" + msg["msg"]);
					$("#inFile").val("1");		
				}
		});
		
		

	});
	
	
	$("#showActionCard").bind("click", function() {
		var inFile = $("#inFile").val();
		if(inFile==null || inFile==""){
			alert("请先生成媒体卡");
		}else{
			window.open("/MPP/makeActionCard/showActionCard.action");
		}
		
	});
	
	

	$("#gameId").change(function() {
		var gameId = $("#gameId").val();
		var type = $("#hidetype").val();
		if (type == "login") {
			location.href = "/MPP/quickLoginManage/quickLoginManage.action?gameId="
					+ gameId;
		} else if (type == "recharge") {
			location.href = "/MPP/rechargeTestManage/rechargeTestManage.action?gameId="
					+ gameId;
		} else if(type=="agentManage") {
			// 切换游戏域名和CDN,暂时写死在这里
			if(gameId==="1"){
				$("#gameDomainList option").remove();
				$("#gameDomainList").append("<option>17wan7.com</option>");
				$("#gameDomainList").append("<option>mlwanwan.com</option>");
				$("#CDNList option").remove();
				$("#CDNList").append("<option>res.q.37wan.com</option>");
				$("#CDNList").append("<option>res.q.17wan7.com</option>");
				$("#CDNList").append("<option>res.twgmeiqmr.17wan7.com</option>");
			}else if(gameId==="2"){
				$("#gameDomainList option").remove();
				$("#gameDomainList").append("<option>17wan7.com</option>");
				$("#CDNList option").remove();
				$("#CDNList").append("<option>res.lycj.37wan.com</option>");
				$("#CDNList").append("<option>res.lycj.17wan7.com</option>");
				$("#CDNList").append("<option>res.twgmeilycj.17wan7.com</option>");			
			}else if(gameId==="3"){
				$("#gameDomainList option").remove();
				$("#CDNList option").remove();
			}else if(gameId==="4"){
				$("#gameDomainList option").remove();
				$("#gameDomainList").append("<option>mlwanwan.com</option>");
				$("#CDNList option").remove();
				$("#CDNList").append("<option>resmlj.mlwanwan.com</option>");
			}else if(gameId==="5"){
				$("#gameDomainList option").remove();
				$("#gameDomainList").append("<option>17wan7.com</option>");
				$("#gameDomainList").append("<option>mlwanwan.com</option>");
				$("#CDNList option").remove();
				$("#CDNList").append("<option>res.zsj.17wan7.com</option>");
				$("#CDNList").append("<option>res.zsj.mlwanwan.com</option>");
			}
		}else if(type = "makeActionCard"){
			location.href = "/MPP/makeActionCard/makeActionCard.action?gameId="
					+ gameId;
		}
	});
	
	
	//版本查看按钮
	$("#btn1").bind("click", function() {
		var gameId = $("#gameId").val();	
		location.href = "/MPP/showGameVer/showGameVer.action?gameId="+gameId+"&ver="+"GVER";
		
	});
	
	$("#btn2").bind("click", function() {
		var gameId = $("#gameId").val();
		location.href = "/MPP/showGameVer/showGameVer.action?gameId="+gameId+"&ver="+"GLVER";
		
	});
	
	$("#btn3").bind("click", function() {
		var gameId = $("#gameId").val();	
		location.href = "/MPP/showGameVer/showGameVer.action?gameId="+gameId+"&ver="+"JAVAVER";
		
	});
	
	$("#btn4").bind("click", function() {
		var gameId = $("#gameId").val();	
		location.href = "/MPP/showGameVer/showGameVer.action?gameId="+gameId+"&ver="+"javajarver";
		
	});
	
	$("#btn5").bind("click", function() {
		var gameId = $("#gameId").val();
		if(gameId==4){
			location.href = "/MPP/showGameVer/showGameVer.action?gameId="+gameId+"&ver="+"DATAVER";
		}else if(gameId==5){
			location.href = "/MPP/showGameVer/showGameVer.action?gameId="+gameId+"&ver="+"dataresver";
		}
		
	});
	
	$("#btn6").bind("click", function() {
		var gameId = $("#gameId").val();
		if(gameId==4){
			location.href = "/MPP/showGameVer/showGameVer.action?gameId="+gameId+"&ver="+"GAMEDATA_VER";
		}else if(gameId==5){
			location.href = "/MPP/showGameVer/showGameVer.action?gameId="+gameId+"&ver="+"gamedataver";
		}
		
		
	});
	
	
	//解压角色数据
	
	$("#extractRoleSubmit").bind("click", function() {
		var gameId = $("#gameId").val();
		var roleInfo = $("#roleInfo").val()
		
		$.ajax({
			"type" : "POST",
			"url" : "/MPP/extractRoleInfo/extractRoleInfoSubmit.action",
			"dataType" : "json",
			"contentType" : "application/x-www-form-urlencoded; charset=utf-8", 
			"data" : {
				gameId : gameId,
				roleInfo : roleInfo,
			},
			"success" : function(msg) {
				$("#outPutData").val(msg['msg']);	
			}
	});
		
	});
	
	
});

function checkInput() {

}
function getloginUrl() {

}
