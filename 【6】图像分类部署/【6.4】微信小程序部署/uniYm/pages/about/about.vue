<template>
	<view>
	<view class="content">
		<image class="logo" src="/static/三叶青.jpg"></image>
		<view class="text-area">
			<text class="title">{{title}}</text>
		</view>
	</view>
	
	<!--开发者信息区域-->
	<view id="developerView">
	    <view class="developerItemView">
	        <view>开发者邮箱</view>
	        <view>wht226004434@qq.com</view>
	    </view>
		<view class="developerItemView">
		    <view>GitHub</view>
		    <view>https://github.com/xingyun-dev</view>
		</view>
		<view class="developerItemView">
		    <view>CSDN博客</view>
		    <view>@星石传说</view>
		</view>
	 <view class="developerItemView">
	        <view>三叶识青网页版</view>
	        <view style="display: flex; align-items: center;">
	            <view>https://www.whtuu.cn</view>
	            <button @click="redirectToWeb" style="background-color:aqua;height: 80%;">前往</button>
	        </view>
	    </view>

	</view>
	<view id="qrCodeView">
	    <text style="font-size: 20px; color: #d0d5ff; font-weight: bold; text-shadow: 2px 2px 4px #000000;background-color: azure;">
	            @三叶识青，是一款基于三叶青产地在线识别的微信小程序，
				目前产地暂时共分为五大省份：云南省、广西省、浙江省、贵州省、陕西省。
				通过识别不同产地的三叶青块根、叶片图片进行分类。
                小程序的主要功能包括：首页、图库、我的、图像识别、历史记录等。</p>
	    </text>
	</view>

</view>
</template>

<script>
	export default {
	  methods: {
	    redirectToWeb() {
	      uni.navigateTo({
	        url: '/pages/WebView/WebView?url=https://www.whtuu.cn'
	      });
	    }
	  }
	};
</script>

<style>
	/*区域*/
	#qrCodeView{
	    width:700rpx;
	    margin:250rpx auto 60rpx;
	    text-align: center;
	    /* font-size:26rpx; */
	}
	
	/*开发者信息区域*/
	#developerView{
	    padding:0 40rpx;
	}
	.developerItemView{
	    padding-bottom: 30rpx;   
	}
	.developerItemView > view:nth-child(1){
	    font-size: 30rpx;
	    color: #87cefa;
	    padding-bottom: 20rpx;
	}
	.developerItemView > view:nth-child(2){
	    font-size: 26rpx;
	    color:#888;
	}
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