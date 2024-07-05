  <template>
    <view class="Index">
      <!-- 瀑布流布局列表 -->
      <view class="pubuBox">
        <view class="pubuItem">
          <view class="item-masonry" v-for="(item, index) in comList" :key="index">
            <image :src="item.img" mode="widthFix"></image>
            <view class="listtitle"> <!-- 这是没有高度的父盒子（下半部分） -->
              <view class="listtitle1">{{ item.name}}</view>  
            </view>
          </view>
        </view>
      </view>
    </view>
  </template>
  
  <script>
   export default {
     data() {
       return {
         // userinfo: null,  // 添加一个属性来保存用户信息
         userid: uni.getStorageSync('user').userid,  // 获取保存的用户 id
         comList: [], //将初始值设为空数组
       };
     },
     onLoad() {
         // this.userinfo = uni.getStorageSync('user');
         this.getComList();
     },
     methods: {
         getComList() {
           console.log(this.comList)  // 修改这里
           uni.request({
             url: ``,  // 修改接口地址并添加 userid 参数
             method: 'GET',
             success: (response) => {
               this.comList = response.data.map(image => {
                 return {
                   img: '' + image.photos_name+'.png', // Assume that the response contains an array of objects with "photos_name" property
                   name: image.photos_name
                 };
               });
             },
             fail: (error) => {
               console.log(this.comList)  // 修改这里
               console.error(error);
             }
           });
         },
       },
       onShow() {},
   };
  </script>

 
 <style scoped="scoped" lang="scss">
 	//瀑布流
 	page {
 		background-color: #eee;
 		height: 100%;
 	}
 
 	.pubuBox {
 		padding: 22rpx;
 	}
 
 	.pubuItem {
 		column-count: 2;
 		column-gap: 20rpx;
 	}
 
 	.item-masonry {
 		box-sizing: border-box;
 		border-radius: 15rpx;
 		overflow: hidden;
 		background-color: #fff;
 		break-inside: avoid;
 		/*避免在元素内部插入分页符*/
 		box-sizing: border-box;
 		margin-bottom: 20rpx;
 		box-shadow: 0px 0px 28rpx 1rpx rgba(78, 101, 153, 0.14);
 	}
 
 	.item-masonry image {
 		width: 100%;
 	}
 
 	.listtitle {
 		padding-left: 22rpx;
 		font-size: 24rpx;
 		padding-bottom: 22rpx;
 
 		.listtitle1 {
 			line-height: 39rpx;
 			text-overflow: -o-ellipsis-lastline;
 			overflow: hidden;
 			text-overflow: ellipsis;
 			display: -webkit-box;
 			-webkit-line-clamp: 2;
 			line-clamp: 2;
 			-webkit-box-orient: vertical;
 			min-height: 39rpx;
 			max-height: 78rpx;
 		}
 
 		.listtitle2 {
 			color: #ff0000;
 			font-size: 32rpx;
 			line-height: 32rpx;
 			font-weight: bold;
 			padding-top: 22rpx;
 
 			.listtitle2son {
 				font-size: 32rpx;
 			}
 		}
 
 		.listtitle3 {
 			font-size: 28rpx;
 			color: #909399;
 			line-height: 32rpx;
 			padding-top: 22rpx;
 		}
 	}
 
 	.Index {
 		width: 100%;
 		height: 100%;
 	}
 </style>
 
