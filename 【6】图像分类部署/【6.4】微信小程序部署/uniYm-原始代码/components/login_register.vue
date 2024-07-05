<template>
	<view class="content">
		<view class="mainTop">
			<view class="mianTaber" v-for="(item,index) in taberList" :key="item.idso" @click="getTar(index)"
				:class="{'borderBottom':contin==index}">{{item.text}}</view>
		</view>
		<view class="mainCenter" v-if="contin==0">
			<view class="mainCenBox">
				<input type="text" maxlength="50" placeholder="请输入邮箱地址" v-model="phoneNumber">
				<view class="mainInp">
					<input :type="passworif" placeholder="请输入密码" maxlength="28" v-model="password">
					<view class="poerter" style="padding-right: 20rpx;" @click="getshouBox"><text
							v-if="shouBox==false">显示</text><text v-else>隐藏</text></view>
				</view>
			</view>
			<view class="mainBtnBox">
				<view class="mainBtn" @click="login">
					登录
				</view>
			</view>
		</view>
		<view class="mainCenter" v-if="contin==1">
			<view class="mainCenBox">
				<input type="text" maxlength="50" placeholder="请输入邮箱地址" v-model="phoneNumber">
				<view class="mainInp">
					<input type="number" placeholder="请输入验证码" maxlength="15" v-model="codeNumber">
					<!-- <view class="poerterii" style="padding-right: 20rpx;">
						<text v-if="shoins==61" @click="sendEmail">获取验证码</text>
						<text v-else>重新发送</text>
					</view> -->
					<view class="poerterii" style="padding-right: 20rpx;" @click="shoins==61 ? sendEmail() : null">
						<text v-if="shoins==61">获取验证码</text>
						<text v-else>重新发送</text>
					</view>
				</view>
				<view class="mainInp">
					<input :type="passworif" placeholder="请输入密码" maxlength="28" v-model="password">
					<view class="poerter" style="padding-right: 20rpx;" @click="getshouBox"><text
							v-if="shouBox==false">显示</text><text v-else>隐藏</text></view>
				</view>
			</view>
			<view class="mainBtnBox zuche">
				<view class="mainBtn" @click="register">立即注册</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				taberList: [{
						text: '登录',
						idso: 1
					},
					{
						text: '注册',
						idso: 2
					}
				],
				contin: 0,
				shouBox: false,
				shoins: 61,
				passworif: 'password',
				phoneNumber: '',
				password: '',
				codeNumber: ''
			}
		},
		methods: {
			getTar(e) {
				this.contin = e
			},
			getshouBox() {
				this.shouBox = !this.shouBox
				if (this.shouBox == false) {
					this.passworif = "password"
				} else {
					this.passworif = "text"
				}
			},
			login() {
				// console.log(this.phoneNumber, this.password)
				// Validate inputs
				if (!this.phoneNumber || !this.password) {
					// Show error message
					uni.showToast({
						title: '请正确输入所有必要的信息',
						icon: 'error'
					});
					return;
				}

				let data = {
					username: this.phoneNumber,
					password: this.password
				}
				let jsonData = JSON.stringify(data);
				console.log(jsonData)

				uni.request({
					url: '',
					data: jsonData,
					method: 'POST',
					header: {
						'Content-Type': 'application/json'
					},
					success: (res) => {
						if (res.data.access_token) {
							// 登录成功
							// 你可以在这里做一些状态更新或者页面跳转
							uni.showToast({
								title: '登录成功',
								icon: 'success'
							});
							uni.setStorageSync('token', res.data.access_token);
							// 将用户名保存到本地

							this.getUserInfo(res.data.access_token);
							// console.log(res.data.user_info)
							setTimeout(() => {
								uni.navigateBack({
									delta: 1 // 返回的页面数，如果 delta 大于现有页面数，则返回到首页。
								});
							}, 1000); // 延迟1秒
						} else {
							// 登录失败
							// 你可以在这里显示错误信息
							console.log(res.data)
							uni.showToast({
								title: '登录失败',
								icon: 'error'
							});
						}
					},
					fail: (err) => {
						// 请求失败
						// 你可以在这里处理网络错误
						uni.showToast({
							title: '网络请求失败，请检查您的网络设置',
							icon: 'error'
						});
					}
				});
			},
			getUserInfo(token) {
				uni.request({
					url: '',
					method: 'GET',
					header: {
						'Authorization': 'Bearer ' + token
					},
					success: (res) => {
						if (res.data.user_info) {
							// 获取用户信息成功
							uni.setStorageSync('user', res.data.user_info);
							// console.log(res.data.user_info)
						} else {
							// 获取用户信息失败
							console.log(res.data)
						}
					},
					fail: (err) => {
						// 请求失败
						// 你可以在这里处理网络错误
						uni.showToast({
							title: '网络请求失败，请检查您的网络设置',
							icon: 'error'
						});
					}
				});
			},


			register() {
				// Validate inputs
				// console.log(this.phoneNumber)
				if (!this.phoneNumber || !this.password || !this.codeNumber) {
					// Show error message
					uni.showToast({
						title: '请正确输入所有必要的信息',
						icon: 'error'
					});
					return;
				}

				let data = {
					username: this.phoneNumber,
					password: this.password,
					ecode: this.codeNumber
				}
				let jsonData = JSON.stringify(data);
				// console.log(jsonData)

				uni.request({
					url: '',
					data: jsonData,
					method: 'POST',
					header: {
						'Content-Type': 'application/json'
					},
					success: (res) => {
						if (res.data.access_token) {
							// 注册成功
							uni.showToast({
								title: '注册成功',
								icon: 'success'
							});
							uni.setStorageSync('token', res.data.access_token);
							// 将用户名保存到本地
							this.getUserInfo(res.data.access_token);
							setTimeout(() => {
								uni.navigateBack({
									delta: 1 // 返回的页面数，如果 delta 大于现有页面数，则返回到首页。
								});
							}, 1000); // 延迟1秒
						} else {
							// 注册失败
							// console.log(res)
							uni.showToast({
								title: '注册失败',
								icon: 'error'
							});
						}
					},
					fail: (err) => {
						// 请求失败
						// 你可以在这里处理网络错误
						uni.showToast({
							title: '网络请求失败，请检查您的网络设置',
							icon: 'error'
						});
					}
				});
			},
			sendEmail() {
				// console.log('sendEmail was called')
				// Validate input
				if (this.shoins != 61 || !this.phoneNumber) {
					// Show error message
					uni.showToast({
						title: '请输入注册邮箱',
						icon: 'error'
					});
					return;
				}

				let data = {
					email: this.phoneNumber
				}
				let jsonData = JSON.stringify(data);

				uni.request({
					url: '',
					data: jsonData,
					method: 'POST',
					header: {
						'Content-Type': 'application/json'
					},
					success: (res) => {
						if (res.data.msg === "Email sent") {
							// 邮件发送成功
							uni.showToast({
								title: '邮件发送成功，请查收你的邮箱',
								icon: 'success'
							});
							this.shoins = 60;
							this.startCountdown();


						} else {
							uni.showToast({
								title: '邮件发送失败',
								icon: 'error'
							});

						}
					},
					fail: (err) => {
						// 请求失败
						// 你可以在这里处理网络错误
						uni.showToast({
							title: '网络请求失败，请检查您的网络设置',
							icon: 'error'
						});
					}
				});
			},
			startCountdown() {
				let timer = this.shoins;
				let intervalId = setInterval(() => {
					if (timer > 0) {
						timer--;
						this.shoins = timer;
					} else {
						clearInterval(intervalId);
						this.shoins = 61;
					}
				}, 1000);
			}
		}
	}
</script>


<style lang="scss" scoped>
	@keyframes yes {
		0% {
			opacity: 0;
			bottom: -200rpx;
		}

		50% {
			opacity: .5;
		}

		100% {
			opacity: 1;
			bottom: 0;
		}
	}

	.content {
		position: fixed;
		left: 0;
		bottom: 0;
		width: 100%;
		// height: 55%;
		border-top-right-radius: 50rpx;
		border-top-left-radius: 50rpx;
		box-sizing: border-box;
		padding: 30rpx;
		background-color: #c6f6ff;
		animation: yes .5s linear;

		.mainTop {
			display: flex;
			align-items: center;
			justify-content: space-around;

			.mianTaber {
				padding: 20rpx;
				width: 50%;
				display: flex;
				align-items: center;
				justify-content: center;
				color: #444;
				font-weight: bold;
				font-size: 34rpx;
				padding-bottom: 10rpx;
			}

			.borderBottom {
				color: #ff6600;
				transition: all 1s linear;

				&:before {
					content: '';
					width: 20rpx;
					height: 20rpx;
					margin-right: 15rpx;
					border-bottom: 6rpx solid #ff6600;
					border-right: 6rpx solid #ff6600;
					transform: rotate(-45deg);
				}

				&:after {
					content: '';
					width: 20rpx;
					height: 20rpx;
					margin-left: 15rpx;
					border-bottom: 6rpx solid #ff6600;
					border-left: 6rpx solid #ff6600;
					transform: rotate(45deg);
				}
			}
		}

		.mainCenter {
			padding-top: 20rpx;

			.mainCenBox {
				input {
					width: 75%;
					margin: auto;
					border: solid 1rpx #999;
					margin-top: 40rpx;
					padding: 20rpx 30rpx;
					border-radius: 20rpx;
				}

				.mainInp {
					position: relative;

					.poerterii {
						position: absolute;
						top: 50%;
						right: -20rpx;
						transform: translate(-50%, -50%);
						color: #ff6600;
					}

					.poerter {
						position: absolute;
						top: 50%;
						right: 30rpx;
						transform: translate(-50%, -50%);

						text {
							color: #999;
						}

						.mr {
							padding-right: 30rpx !important;
						}
					}
				}
			}

			.zuche {
				.mainBtn {
					color: #fff !important;
					background-color: #ff6600 !important;
					margin-bottom: 100rpx !important;
				}
			}

			.mainBtnBox {
				padding-top: 60rpx;

				.mainBtn {
					margin: auto;
					width: 75%;
					text-align: center;
					padding: 30rpx;
					border-radius: 30rpx;
					margin-bottom: 20rpx;
					border: #ff6600 solid 3rpx;
					background-color: #ff6600;
					font-size: 34rpx;
					color: #fff;

					&:nth-last-child(1) {
						color: #333;
						background-color: transparent;
					}
				}
			}
		}

		.iconifbt {
			padding: 55rpx 0 30rpx;

			.log_luit {
				font-size: 30rpx;

				text {
					color: #ff6600;
				}
			}
		}
	}
</style>