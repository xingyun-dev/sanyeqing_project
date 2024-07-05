<template>
	<view class="tabbar-container">
		<block>
			<view class="tabbar-item" v-for="(item, index) in tabbarList"
				:class="[item.centerItem ? ' center-item' : '']" @click="changeItem(item)">
				<view class="item-top">
					<image :src="currentItem == item.id ? item.selectIcon : item.icon"></image>
				</view>
				<view class="item-bottom" :class="[currentItem == item.id ? 'item-active' : '']">
					<text>{{ item.text }}</text>
				</view>
			</view>
		</block>
	</view>
</template>

<script>
	export default {
		props: {
			currentPage: {
				type: Number,
				default: 0
			}
		},
		data() {
			return {
				currentItem: 0,
				tabbarList: [{
						id: 0,
						path: '/pages/index/index',
						icon: '/static/首页.png',
						selectIcon: '/static/首页.png',
						text: '首页',
						centerItem: false
					},
					{
						id: 1,
						path: '/pages/image_zhanshi/image_zhanshi',
						icon: '/static/图库.png',
						selectIcon: '/static/图库.png',
						text: '图库',
						centerItem: false
					},
					{
						id: 2,
						path: '/pages/photo/photo',
						icon: '/static/拍照.png',
						selectIcon: '/static/拍照.png',
						text: '识别',
						centerItem: true
					},
					{
						id: 3,
						path: '/pages/mine/mine',
						icon: '/static/历史记录.png',
						selectIcon: '/static/历史记录.png',
						text: '历史记录',
						centerItem: false
					},
					{
						id: 4,
						path: '/pages/person/person',
						icon: '/static/我的.png',
						selectIcon: '/static/我的.png',
						text: '我的',
						centerItem: false
					}
				]
			};
		},
		mounted() {
			this.currentItem = this.currentPage;
			uni.hideTabBar();
		},
		methods: {
			// changeItem(item) {
			// 	let _this = this;
			// 	if (item.text === '识别') {
			// 		uni.chooseImage({
			// 			count: 1, // 默认9
			// 			sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机
			// 			success: function(res) {
			// 				// console.log(res);
			// 				// 获取图片的路径
			// 				var imagePath = res.tempFilePaths[0];
			// 				console.log(imagePath)

			// 				// 保存图片的路径
			// 				uni.setStorage({
			// 					key: 'imagePath',
			// 					data: imagePath,
			// 					success: function() {
			// 						// 跳转到新的页面
			// 						uni.navigateTo({
			// 							url: '/pages/shibie/shibie'
			// 						});
			// 					}
			// 				});
			// 			}
			// 		});
			// 	} else {
			// 		uni.switchTab({
			// 			url: item.path
			// 		});
			// 	}
			// }
			changeItem(item) {
			    let _this = this;
			    if (item.text === '识别') {
			        // 显示动作菜单
			        uni.showActionSheet({
			            itemList: ['三叶青块根识别', '三叶青叶片识别'],
			            success: function(res) {
			                console.log(res.tapIndex);  // 用户点击的菜单项索引
			                // 根据用户的选择设置类型
			                _this.type = res.tapIndex;
			                // 然后进行拍照
			                _this.takePhoto();
			            },
			            fail: function(res) {
			                console.log(res.errMsg);
			            }
			        });
			    } else {
			        uni.switchTab({
			            url: item.path
			        });
			    }
			},
			
			takePhoto() {
			        let _this = this;
			        uni.chooseImage({
			            count: 1, // 默认9
			            sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机
			            success: function(res) {
			                // 获取图片的路径
			                var imagePath = res.tempFilePaths[0];
			                // console.log(imagePath)
			
			                // 保存图片的路径
			                uni.setStorage({
			                    key: 'imagePath',
			                    data: imagePath,
			                    success: function() {
			                        // 保存类型
			                        uni.setStorage({
			                            key: 'type',
			                            data: _this.type,
			                            success: function() {
			                                // 跳转到新的页面
			                                uni.navigateTo({
			                                    url: '/pages/shibie/shibie?type='+_this.type
			                                });
			                            }
			                        });
			                    }
			                });
			            }
			        });
			    }
			
		}
	};
</script>
<style>
	view {
		padding: 0;
		margin: 0;
		box-sizing: border-box;
	}

	.tabbar-container {
		position: fixed;
		bottom: 0;
		left: 0;
		width: 100%;
		height: 110rpx;
		box-shadow: 0 0 5px #999;
		display: flex;
		align-items: center;
		padding: 5rpx 0;
		color: #999999;
	}

	.tabbar-container .tabbar-item {
		width: 20%;
		height: 100rpx;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		text-align: center;
	}

	.tabbar-container .item-active {
		color: #f00;
	}

	.tabbar-container .center-item {
		display: block;
		position: relative;
	}

	.tabbar-container .tabbar-item .item-top {
		width: 70rpx;
		height: 70rpx;
		padding: 10rpx;
	}

	.tabbar-container .center-item .item-top {
		flex-shrink: 0;
		width: 100rpx;
		height: 100rpx;
		position: absolute;
		top: -50rpx;
		left: calc(50% - 50rpx);
		border-radius: 50%;
		box-shadow: 0 0 5px #999;
		background-color: #ffffff;
	}

	.tabbar-container .tabbar-item .item-top image {
		width: 100%;
		height: 100%;
	}

	.tabbar-container .tabbar-item .item-bottom {
		font-size: 28rpx;
		width: 100%;
	}

	.tabbar-container .center-item .item-bottom {
		position: absolute;
		bottom: 5rpx;
	}
</style>