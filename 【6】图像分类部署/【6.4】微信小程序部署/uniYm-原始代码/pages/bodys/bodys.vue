<template>
	<view>
		<view class="content">
			<image class="logo" src="/static/三叶青.jpg"></image>
			<view class="text-area">
				<text class="title">{{title}}</text>
			</view>
		</view>
		<uni-list>
			<uni-list-item title="块根图像分类批量" showArrow thumb="/static/img/keys.png" thumb-size="base" clickable @click="goSb(0)" />
			<uni-list-item title="叶片图像分类批量" showArrow thumb="/static/img/attrs.png" thumb-size="base" clickable @click="goSb(1)" />
		
		</uni-list>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				title: "批量处理"
			}
		},
		methods: {
			goSb(i){
			
				uni.navigateTo({
					url:'../piliang/piliang?type='+i
				})
				
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
