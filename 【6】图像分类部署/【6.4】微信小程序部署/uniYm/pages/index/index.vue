<template>
	<view>

		<zdy-tabbar :current-page="0"></zdy-tabbar>
		
		<view class="content">
			<image class="logo" src="/static/三叶青.jpg"></image>
			<view class="text-area">
				<text class="title">{{title}}</text>
			</view>
		</view>
		<uni-list>
			 <uni-list-item title="图像分类"  showArrow thumb="/static/img/分类.png" thumb-size="base" clickable @click="goSb(2)" />
			 <!-- <uni-list-item title="目标检测"  showArrow thumb="/static/img/检测.png" thumb-size="base" clickable @click="goSb(1)" /> -->
			 <uni-list-item title="批量处理"  showArrow thumb="/static/img/批量.png" thumb-size="base" clickable @click="goSb(3)" />
			 <uni-list-item title="三叶识青网页版"  showArrow thumb="/static/img/mianim.png" thumb-size="base" clickable @click="goSb(4)" />
			 <uni-list-item title="清空历史"  showArrow thumb="/static/img/垃圾桶.png" thumb-size="base" clickable @click="qclocal()" />
		</uni-list>
	</view>
	
</template>

<script>
	export default {
		data() {
			return {
				title: '三叶青识别工具',
				src: ''
			}
		},
		onLoad() {
			
		},
		mounted() {
		},
		methods: {
			qclocal(){
				uni.getStorage({
					key:'historys',
					success:function(){
						uni.showLoading({
						    title: '删除中'
						});
						uni.removeStorage({
						    key: 'historys',
						    success: function () {
								uni.hideLoading();
						       uni.showToast({
						           title: '清空成功',
						           duration: 1500
						       });
						    }
						});
					},
					fail:function(){
						uni.showToast({
							image: '/static/img/tanqi.png',
						    title: '您还没有识别哦',
						    duration: 1500
						});
					}
				})
			},
			goSb(i){
				// 图像分类
				if(i==2){
					uni.navigateTo({
						url:'../image/image'
					})
				}
				// 批量处理
				if(i==3){
					uni.navigateTo({
						url:'../bodys/bodys'  
					})
				}
				// 提供反馈
				if(i==4){
					uni.navigateTo({
						url: '/pages/WebView/WebView?url=https://www.whtuu.cn'
					})
				}
			}
		}
	}
</script>

<style>
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.logo {
		height: 200rpx;
		width: 200rpx;
		margin-top: 70rpx;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 50rpx;
		border-radius: 200px;
	}
	
	
	.logo {
	    position: relative;
	    display: inline-block;
	}
	
	.logo::after {
	    content: "";
	    position: absolute;
	    top: 0;
	    left: 0;
	    width: 100%;
	    height: 100%;
	    background: rgba(205, 248, 233, 0.2); /* aquamarine with 20% opacity */
	    z-index: 1;
	}


	.text-area {
		margin-bottom: 40rpx;
		display: flex;
		justify-content: center;
	}

	.title {
		font-size: 36rpx;
		color: #8f8f94;
	}
</style>
