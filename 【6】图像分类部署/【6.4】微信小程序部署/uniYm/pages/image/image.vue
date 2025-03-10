<template>
	<view>
		<view class="content">
			<image class="logo" src="/static/三叶青.jpg"></image>
			<view class="text-area">
				<text class="title">{{title}}</text>
			</view>
		</view>
		<uni-list>
			 <uni-list-item title="块根图像分类"  showArrow thumb="/static/img/botany.png" thumb-size="base" clickable @click="goSb(0)" />
			 <!-- <uni-list-item title="视频预测"  showArrow thumb="/static/img/animal.png" thumb-size="base" clickable @click="goSb(1)" /> -->
			 <uni-list-item title="叶片图像分类"  showArrow thumb="/static/img/car.png" thumb-size="base" clickable @click="goSb(1)" />
			
		</uni-list>
	</view>
	
</template>

<script>
	export default {
		data() {
			return {
				title: '三叶青图像分类',
				src: ''
			}
		},
		onLoad() {
			
		},
		mounted() {
			
		},
		methods: {
			// qclocal(){
			// 	uni.getStorage({
			// 		key:'historys',
			// 		success:function(){
			// 			uni.showLoading({
			// 			    title: '删除中'
			// 			});
			// 			uni.removeStorage({
			// 			    key: 'historys',
			// 			    success: function () {
			// 					uni.hideLoading();
			// 			       uni.showToast({
			// 			           title: '清除成功',
			// 			           duration: 1500
			// 			       });
			// 			    }
			// 			});
			// 		},
			// 		fail:function(){
			// 			uni.showToast({
			// 				image: '/static/img/tanqi.png',
			// 			    title: '您还没有识别哦',
			// 			    duration: 1500
			// 			});
			// 		}
			// 	})
			// },
			goSb(i){

				uni.navigateTo({
					url:'../apiuse/apiuse?type='+i
				})
				
				// if(i==1){
				// uni.navigateTo({
				// 	url:'../ceshi'
				// })
				// }
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

