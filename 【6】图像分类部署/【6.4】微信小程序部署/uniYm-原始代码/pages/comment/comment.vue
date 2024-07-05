<template>
	<view class="chat">
		<scroll-view :style="{height: `${windowHeight-inputHeight}rpx`}" id="scrollview" scroll-y="true"
			:scroll-top="scrollTop" class="scroll-view">
			<!-- 聊天主体 -->
			<view id="msglistview" class="chat-body">
				<!-- 聊天记录 -->
				<view v-for="(item,index) in msgList" :key="index">
					<!-- 自己发的文本消息 -->
					<view class="item self" v-if="item.type === 'text'">
						<!-- 文字内容 -->
						<view class="content right">
							{{item.userContent}}
						</view>
						<!-- 头像 -->
						<view class="avatar">
						</view>
					</view>
					<!-- 自己发的图片消息 -->
					<view class="item self" v-if="item.type === 'image'">
						<!-- 图片内容 -->
						<view class="image right">
							<image :src="item.userImage"></image>
						</view>
						<!-- 头像 -->
						<view class="avatar">
						</view>
					</view>
					<!-- 机器人发的消息 -->
					<view class="item Ai" v-if="item.botContent != ''">
						<!-- 头像 -->
						<view class="avatar">
						</view>
						<!-- 文字内容 -->
						<view class="content left">
							{{item.botContent}}
						</view>
					</view>
				</view>
			</view>

		</scroll-view>
		<!-- 底部消息发送栏 -->
		<!-- 用来占位，防止聊天消息被发送框遮挡 -->
		<view class="chat-bottom" :style="{height: `${inputHeight}rpx`}">
			<view class="send-msg" :style="{bottom:`${keyboardHeight}rpx`}">
				<view class="uni-textarea">
					<textarea v-model="chatMsg" maxlength="300" confirm-type="send" @confirm="handleSend"
						:show-confirm-bar="false" :adjust-position="false" @linechange="sendHeight" @focus="focus"
						@blur="blur" auto-height></textarea>
				</view>
				<button @click="handleSend" class="send-btn">发送</button>
				<view class="flex-item">
				  <picker mode="selector" :range="options" @change="handleSelectChange">
				    <view class="picker">
				      <image src="/static/设置.png" mode="aspectFit" style="width: 25px; height: 25px;"></image>
				      <!-- {{selectedOption}} -->
				    </view>
				  </picker>
				</view>
			</view>
			
		</view>
	</view>
</template>
<script>
	export default {
		data() {
			return {
				options: ['上传图片', '清除历史消息'],
				selectedOption: "操作",
				//键盘高度
				keyboardHeight: 0,
				//底部消息发送高度
				bottomHeight: 0,
				//滚动距离
				scrollTop: 0,
				userId: '',
				//发送的消息
				chatMsg: "",
				msgList: [{
						type: 'text', // 添加type属性
						botContent: "hello！在这里你可以写下......？",
						botImage: "", // 添加botImage字段
						recordId: 0,
						titleId: 0,
						userContent: "你好啊👻",
						userImage: "", // 添加userImage字段
						userId: 0,
						msg: ""
					},
					{
						type: 'text', // 添加type属性
						botContent: "CSDN: @星石传说;\n  Github: @https://github.com/xingyun-dev;\n  三叶识青网页：@https://www.whtuu.cn",
						botImage: "", // 添加botImage字段
						recordId: 0,
						titleId: 0,
						userContent: "我是xxx🐬",
						userImage: "", // 添加userImage字段
						userId: 0,
						msg: ""
					},
				]
			}
		},
		updated() {
			//页面更新时调用聊天消息定位到最底部
			this.scrollToBottom();
		},
		computed: {
			windowHeight() {
				return this.rpxTopx(uni.getSystemInfoSync().windowHeight)
			},
			// 键盘弹起来的高度+发送框高度
			inputHeight() {
				return this.bottomHeight + this.keyboardHeight
			}
		},
		onLoad() {
			// 从本地缓存中获取消息
			const storedMsgList = uni.getStorageSync('msgList');
			if (storedMsgList) {
				this.msgList = storedMsgList;
			}

			uni.onKeyboardHeightChange(res => {
				this.keyboardHeight = this.rpxTopx(res.height - 30)
				if (this.keyboardHeight < 0) this.keyboardHeight = 0;
			})
		},

		onUnload() {
			uni.offKeyboardHeightChange()
		},
		methods: {
			focus() {
				this.scrollToBottom()
			},
			blur() {
				this.scrollToBottom()
			},
			// px转换成rpx
			rpxTopx(px) {
				let deviceWidth = wx.getSystemInfoSync().windowWidth
				let rpx = (750 / deviceWidth) * Number(px)
				return Math.floor(rpx)
			},
			// 监视聊天发送栏高度
			sendHeight() {
				setTimeout(() => {
					let query = uni.createSelectorQuery();
					query.select('.send-msg').boundingClientRect()
					query.exec(res => {
						this.bottomHeight = this.rpxTopx(res[0].height)
					})
				}, 10)
			},
			// 滚动至聊天底部
			scrollToBottom(e) {
				setTimeout(() => {
					let query = uni.createSelectorQuery().in(this);
					query.select('#scrollview').boundingClientRect();
					query.select('#msglistview').boundingClientRect();
					query.exec((res) => {
						if (res[1].height > res[0].height) {
							this.scrollTop = this.rpxTopx(res[1].height - res[0].height)
						}
					})
				}, 15)
			},
			handleSend() {
				if (!this.chatMsg || !/^\s+$/.test(this.chatMsg)) {
					let obj = {
						type: 'text', // 添加type属性
						botContent: "",
						recordId: 0,
						titleId: 0,
						userContent: this.chatMsg,
						userId: 0
					}
					this.msgList.push(obj);
					uni.setStorageSync('msgList', this.msgList);
					this.chatMsg = '';
					this.scrollToBottom()
				} else {
					uni.showToast({
						title: '不能发送空白消息',
						icon: 'none'
					});
				}
			},

			chooseImage() {
				uni.chooseImage({
					success: (chooseImageRes) => {
						const tempFilePaths = chooseImageRes.tempFilePaths;
						let msg = {
							type: 'image', // 添加type属性
							userContent: "",
							userImage: tempFilePaths[0],
							userId: 0,
							botContent: "",
							botImage: "",
							recordId: 0,
							titleId: 0,
						}
						this.msgList.push(msg);
						uni.setStorageSync('msgList', this.msgList);
					}
				});
			},

			clearHistory() {
			  // 只删除前10个消息，但保留最开始的三条
			  if (this.msgList.length > 13) {
			    this.msgList.splice(3, 10);
			  } else if (this.msgList.length > 3) {
			    this.msgList.splice(3, this.msgList.length - 3);
			  }
			  // 更新本地存储中的消息列表
			  uni.setStorageSync('msgList', this.msgList);
			},
			 handleSelectChange(e) {
			      this.selectedOption = this.options[e.target.value];
			      switch (this.selectedOption) {
			        case '上传图片':
			          this.chooseImage();
			          break;
			        case '清除历史消息':
			          this.clearHistory();
			          break;
			        default:
			          break;
			      }
			    },
		}
	}
</script>
<style lang="scss" scoped>
	$chatContentbgc: #C2DCFF;
	$sendBtnbgc: #4F7DF5;

	view,
	button,
	text,
	input,
	textarea {
		margin: 0;
		padding: 0;
		box-sizing: border-box;
	}

	/* 聊天消息 */
	.chat {
		.scroll-view {
			::-webkit-scrollbar {
				display: none;
				width: 0 !important;
				height: 0 !important;
				-webkit-appearance: none;
				background: transparent;
				color: transparent;
			}

			// background-color: orange;
			background-color: #F6F6F6;

			.chat-body {
				display: flex;
				flex-direction: column;
				padding-top: 23rpx;
				// background-color:skyblue;

				.self {
					justify-content: flex-end;
				}

				.item {
					display: flex;
					padding: 23rpx 30rpx;
					// background-color: greenyellow;

					.right {
						background-color: $chatContentbgc;
					}

					.left {
						background-color: #FFFFFF;
					}

					// 聊天消息的三角形
					.right::after {
						position: absolute;
						display: inline-block;
						content: '';
						width: 0;
						height: 0;
						left: 100%;
						top: 10px;
						border: 12rpx solid transparent;
						border-left: 12rpx solid $chatContentbgc;
					}

					.left::after {
						position: absolute;
						display: inline-block;
						content: '';
						width: 0;
						height: 0;
						top: 10px;
						right: 100%;
						border: 12rpx solid transparent;
						border-right: 12rpx solid #FFFFFF;
					}

					.content {
						position: relative;
						max-width: 486rpx;
						border-radius: 8rpx;
						word-wrap: break-word;
						padding: 24rpx 24rpx;
						margin: 0 24rpx;
						border-radius: 5px;
						font-size: 32rpx;
						font-family: PingFang SC;
						font-weight: 500;
						color: #333333;
						line-height: 42rpx;
					}

					.avatar {
						display: flex;
						justify-content: center;
						width: 78rpx;
						height: 78rpx;
						background: #ede4ff;
						border-radius: 8rpx;
						overflow: hidden;

						image {
							align-self: center;
						}

					}
				}
			}
		}

		/* 底部聊天发送栏 */
		.chat-bottom {
			width: 100%;
			height: 177rpx;
			background: #F4F5F7;
			transition: all 0.1s ease;


			.send-msg {
				display: flex;
				align-items: flex-end;
				padding: 16rpx 30rpx;
				width: 100%;
				min-height: 177rpx;
				position: fixed;
				bottom: 0;
				background: #EDEDED;
				transition: all 0.1s ease;
			}

			.uni-textarea {
				padding-bottom: 70rpx;

				textarea {
					width: 537rpx;
					min-height: 75rpx;
					max-height: 500rpx;
					background: #FFFFFF;
					border-radius: 8rpx;
					font-size: 32rpx;
					font-family: PingFang SC;
					color: #333333;
					line-height: 43rpx;
					padding: 5rpx 8rpx;
				}
			}

			.send-btn {
				display: flex;
				align-items: center;
				justify-content: center;
				margin-bottom: 70rpx;
				margin-left: 25rpx;
				width: 150rpx;
				height: 75rpx;
				background: $sendBtnbgc;
				border-radius: 8rpx;
				font-size: 28rpx;
				font-family: PingFang SC;
				font-weight: 500;
				color: #FFFFFF;
				line-height: 28rpx;
			}
			.flex-item{
				display: flex;
				align-items: center;
				justify-content: center;
				margin-bottom: 70rpx;
				margin-left: 25rpx;
				width: 100rpx;
				height: 75rpx;
				border-radius: 8rpx;
				font-size: 28rpx;
				font-family: PingFang SC;
				font-weight: 500;
				color: #FFFFFF;
				line-height: 28rpx;
			}


		}
	}
</style>