/*
**  全局视图
*/
HROS.appmanage = (function(){
	return {
		init : function(){
			$('#amg_dock_container').html('').append($('#dock-container .dock-applist li').clone());
			$('#desk .desktop-container').each(function(i){
				$('#amg_folder_container .folderItem:eq(' + i + ') .folderInner').html('');
				$(this).children('.appbtn:not(.add)').each(function(){
					$('#amg_folder_container .folderItem:eq(' + i + ') .folderInner').append($(this).clone());
				});
			});
			$('#desktop').hide();
			$('#appmanage').show();
			$('#amg_folder_container .folderItem').show().addClass('folderItem_turn');
			$('#amg_folder_container').height($(document).height() - 80);
			$('#appmanage .amg_close').off('click').on('click', function(){
				HROS.appmanage.close();
			});
			
			HROS.appmanage.appresize();
			var width = 100/$('.folderItem').length;
			
			$('.folderItem').css("width",width+"%");
			
			HROS.appmanage.move();
			//HROS.appmanage.getScrollbar();
			//HROS.appmanage.moveScrollbar();
		},
		getScrollbar : function(){
			setTimeout(function(){
				$('#amg_folder_container .folderItem').each(function(){
					var desk = $(this).find('.folderInner'), deskrealh = parseInt(desk.children('.appbtn:last').css('top')) + 41, scrollbar = desk.next('.scrollBar');
					//先清空所有附加样式
					scrollbar.hide();
					desk.scrollTop(0);
					if(desk.height() / deskrealh < 1){
						scrollbar.height(desk.height() / deskrealh * desk.height()).css('top', 0).show();
					}
				});
			},500);
		},
		moveScrollbar : function(){
			/*
			**  手动拖动
			*/
			$('.scrollBar').on('mousedown', function(e){
				var y, cy, deskrealh, moveh;
				var scrollbar = $(this), desk = scrollbar.prev('.folderInner');
				deskrealh = parseInt(desk.children('.appbtn:last').css('top')) + 41;
				moveh = desk.height() - scrollbar.height();
				y = e.clientY - scrollbar.offset().top;
				$(document).on('mousemove', function(e){
					//减80px是因为顶部dock区域的高度为80px，所以计算移动距离需要先减去80px
					cy = e.clientY - y - 80 < 0 ? 0 : e.clientY - y - 80 > moveh ? moveh : e.clientY - y - 80;
					scrollbar.css('top', cy);
					desk.scrollTop(cy / desk.height() * deskrealh);
				}).on('mouseup', function(){
					$(this).off('mousemove').off('mouseup');
				});
			});
			/*
			**  鼠标滚轮
			*/
			$('#amg_folder_container .folderInner').off('mousewheel').on('mousewheel', function(event, delta){
				var desk = $(this), deskrealh = parseInt(desk.children('.appbtn:last').css('top')) + 41, scrollupdown;
				/*
				**  delta == -1   往下
				**  delta == 1    往上
				*/
				if(delta < 0){
					scrollupdown = desk.scrollTop() + 120 > deskrealh - desk.height() ? deskrealh - desk.height() : desk.scrollTop() + 120;
				}else{
					scrollupdown = desk.scrollTop() - 120 < 0 ? 0 : desk.scrollTop() - 120;
				}
				desk.stop(false, true).animate({
					scrollTop : scrollupdown
				}, 300);
				desk.next('.scrollBar').stop(false, true).animate({
					top : scrollupdown / deskrealh * desk.height()
				}, 300);
			});
		},
		resize : function(){
			$('#amg_folder_container').height($(document).height() - 80);
			HROS.appmanage.getScrollbar();
		},
		appresize : function(){
			var manageDockGrid = HROS.grid.getManageDockAppGrid();
			$('#amg_dock_container li').each(function(i){
				$(this).css({
					'left' : manageDockGrid[i]['startX'],
					'top' : 10
				});
			});
			for(var i = 0; i < 5; i++){
				var manageAppGrid = HROS.grid.getManageAppGrid();
				$('#amg_folder_container .folderItem:eq(' + i + ') .folderInner li').each(function(j){
					$(this).css({
						'left' : 0,
						'top' : manageAppGrid[j]['startY']
					}).attr('desk', i);
				});
			}
		},
		close : function(){
			$('#amg_dock_container').html('');
			$('#amg_folder_container .folderInner').html('');
			$('#desktop').show();
			$('#appmanage').hide();
			$('#amg_folder_container .folderItem').removeClass('folderItem_turn');
			HROS.app.get();
		},
		move : function(){
			
			$('#amg_folder_container').off('mousedown', 'li.appbtn:not(.add)').on('mousedown', 'li.appbtn:not(.add)', function(e){
				e.preventDefault();
				e.stopPropagation();
				if(e.button == 0 || e.button == 1){
					var oldobj = $(this), x, y, cx, cy, dx, dy, lay, obj = $('<li id="shortcut_shadow2">' + oldobj.html() + '</li>');
					dx = cx = e.clientX;
					dy = cy = e.clientY;
					x = dx - oldobj.offset().left;
					y = dy - oldobj.offset().top;
					//绑定鼠标移动事件
					$(document).on('mousemove', function(e){
						
						cx = e.clientX <= 0 ? 0 : e.clientX >= $(document).width() ? $(document).width() : e.clientX;
						cy = e.clientY <= 0 ? 0 : e.clientY >= $(document).height() ? $(document).height() : e.clientY;
						
					}).on('mouseup', function(){
						
						//判断是否移动图标，如果没有则判断为click事件
						if(dx == cx && dy == cy){
							HROS.appmanage.close();
							switch(oldobj.attr('type')){
								case 'widget':
								case 'pwidget':
									HROS.widget.create(oldobj);
									break;
								case 'app':
								case 'papp':
								case 'folder':
									HROS.window.mycreate(oldobj);
									break;
							}
							return false;
						}
						
					});
				}
				return false;
			});
		}
	}
})();