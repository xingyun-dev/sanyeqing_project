<template>
	<view class="content">
		<zdy-tabbar :current-page="4"></zdy-tabbar>
		<view class="content_image">
			<image :src="url" @click="changImg"></image>
		</view>
		
		<view class="content_botton">
			<view class="content_info" v-if="userinfo">
				<image :src="`https://www.whtuu.cn/api/avatar/${userinfo.avatar}`" mode=""></image>
				<view class="username">
					{{userinfo.nickname}}
				</view>
				<view class="username">
					注册邮箱：{{userinfo.username}}
				</view>
				
			</view>
			<view v-else class="noLogin">
				<image src="/static/叹气.png" mode="widthFix" @click="login_go()"></image>
				<view class="">点击图片登录</view>

				
			</view>
		</view>
		<!--  -->
		<view class="other">
			<uni-list>
				<uni-list-item showArrow title="对话笔记" clickable @click="goSb(1)"></uni-list-item>
				<uni-list-item showArrow title="我的图片" clickable @click="goSb(2)"></uni-list-item>
				<uni-list-item showArrow title="关于我们" clickable @click="goSb(3)"></uni-list-item>
				<uni-list-item showArrow title="退出登录" clickable @click="logout()"></uni-list-item>
			</uni-list>
		</view>
	</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				// 添加一个控制登录表单显示的数据属性
				showLoginForm: false,
				username: '',
				password: '',
				url: '',
				userinfo: null,  // 添加一个属性来保存用户信息
				collectNum: 0
			}
		},
		onShow() {
			this.userinfo = uni.getStorageSync('user');
			 // console.log(this.userinfo )
			this.url = uni.getStorageSync('url')
			let collect = uni.getStorageSync('collect')
			this.collectNum = collect.length;
		},
		methods: {
			changImg() {
				var self = this;
				uni.chooseImage({
					count: 1,
					sourceType: ['album'],
					success: function(res) {
						// console.log(JSON.stringify(res.tempFilePaths))
						uni.setStorage({
							key: 'url',
							data: res.tempFilePaths[0],
							success: function() {

								self.url = uni.getStorageSync('url');
								let collect = uni.getStorageSync('collect');
								self.collectNum = collect.length;
							}
						});
					}
				});
			},
			goSb(i) {

				if (i == 1) {
				
					uni.navigateTo({
						url: '/pages/comment/comment'
					})
					
				}
				if (i == 2) {
				    // 获取存储的用户信息
				    const user = uni.getStorageSync('user');
				    // 检查是否有用户信息
				    if (!user) {
				        // 没有用户信息，显示提示消息
				        uni.showToast({
				            title: '请先登录',
				            icon: 'none'
				        });
				        // 阻止页面跳转
				        return;
				    } else {
				        // 有用户信息，正常跳转页面
				        uni.navigateTo({
				            url: '/pages/image_zhanshi_my/image_zhanshi_my'
				        });
				    }
				}
				if (i == 3) {
					uni.navigateTo({
						url: '/pages/about/about'
					})
				}
			},
			login_go(){
				uni.navigateTo({
					url: '/pages/login/login'
				})
			},
			
			// 登出
			logout() {
				// 删除JWT
				uni.removeStorageSync('token');
				uni.removeStorageSync('user');
				//删除缓存 
				
				// 显示提示消息
				    uni.showToast({
				        title: '已退出登录',
				        icon: 'success'
				    });
			 // 延迟 3 秒后重新加载当前页面
			    setTimeout(() => {
			        uni.reLaunch({
			            url: '/pages/person/person'
			        });
			    }, 2000);
			}
		}
	}
</script>

<style lang="scss">
	page {
		background-color: #eee;
	}

	.content_image {
		image {
			// 高斯模糊
			// filter: blur(3rpx);
			width: 100%;
		}

		height: 300rpx;
		position: relative;
	}

	.content_botton {
		.noLogin {
			position: absolute;
			left: 45%;
			transform: translate(-50%);
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: space-around;
			margin-top: 15%;
			margin-left: 5%;
			border-radius: 20rpx;
			width: 90%;
			height: 250rpx;
			background-color: #fff;
			justify-content: center;
			align-items: center;
			position: relative;

			image {
				width: 100rpx;
				height: 100rpx;
				border-radius: 50%
			}
		}

		.content_info {
			position: relative;
			z-index: 999;
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: space-around;
			margin-top: 15%;
			margin-left: 5%;
			border-radius: 20rpx;
			width: 90%;
			height: 250rpx;
			background-color: #fff;

			image {
				margin-top: -40rpx;
				width: 130rpx;
				height: 130rpx;
				border-radius: 50%;
			}

			.username {}

			.select {
				display: flex;
				justify-content: space-between;

				view {
					padding: 0 40rpx;
				}
			}
		}

		.my_order {
			width: 90%;
			margin-top: 10rpx;
			margin-left: 5%;
			height: 280rpx;
			border-radius: 20rpx;
			background-color: #fff;

			.my_order_title {
				border-radius: 20rpx;
				padding-left: 20rpx;
				line-height: 80rpx;
				height: 80rpx;
			}

			.my_order_item {
				padding: 4.5%;
				float: left;

				.my_order_content {
					display: flex;
					flex-direction: column;
					align-items: center;
					justify-content: space-between;

					image {
						width: 80rpx;
						height: 50rpx;
					}
				}
			}
		}
	}

	.other {
		margin: 10rpx 40rpx;
		height: 190rpx;
		width: 90%;
		border-radius: 20rpx;
		background-color: #fff;

		.other_addres {
			height: 60rpx;
			padding: 20rpx 20rpx;
			border-bottom: 1rpx dashed gainsboro;
			display: flex;
			justify-content: space-between;

			image {
				width: 50rpx;
			}
		}

		.other_our {
			height: 60rpx;
			padding: 20rpx 20rpx;
			display: flex;
			justify-content: space-between;

			image {
				width: 50rpx;
			}
		}
	}
</style>