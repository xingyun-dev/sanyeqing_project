<template>
	<view>
		<zdy-tabbar :current-page="2"></zdy-tabbar>
		<view class="content" :class="{bgs:(imgSrc!=''),ybgs:(imgSrc=='')}">
			<image :src="imgSrc"></image>
		</view>
		<helang-compress ref="helangCompress"></helang-compress>
		<view class="box" v-if="isHas">
			<t-table>
				<t-tr>
					<t-th>序号</t-th>
					<t-th>类型</t-th>
					<t-th>可能性</t-th>
				</t-tr>
				<t-tr v-for="(item,index) in tableList" :key="item.name">
					<t-td>{{ index + 1 }}</t-td>
					<t-td>{{ item.name }}</t-td>
					<t-td>{{ item.score | dealVal}}</t-td>
				</t-tr>
			</t-table>
		</view>
		<button type="primary" @click="togglePopup" style="width: 70%;margin-left: 15%;margin-top: 10%;"
			v-if="showSubmitButton">提交预测结果</button>
		<view v-if="showPopup" class="popup">
			<view class="content_tan">
				<view class="line1">
					<view>识别结果(如果不修改，默认提交预测结果)</view>
				</view>
				<view class="line2">
					<view>预测结果：{{ highestProbabilityResult }}</view>
					<view>修改结果：<input v-model="userResult" /></view>
				</view>
			</view>
			<view class="btn-group">
				<view class="btn_position">
					<view class="cancel" @click="cancel">取消</view>
					<view class="submit" @click="submit">确认</view>
				</view>
			</view>
		</view>
		<view v-if="showPopup" class="mask" @click="togglePopup"></view>
	</view>
</template>

<script>
	import tTable from '@/components/t-table/t-table.vue';
	import tTh from '@/components/t-table/t-th.vue';
	import tTr from '@/components/t-table/t-tr.vue';
	import tTd from '@/components/t-table/t-td.vue';
	import helangCompress from '@/components/helang-compress/helang-compress';
	export default {
		components: {
			tTable,
			tTh,
			tTr,
			tTd,
			helangCompress
		},
		filters: {
			dealVal(val) {
				let str = (parseFloat(val) * 100).toString();
				str = str.substr(0, 5) + "%";
				return str;
			}
		},
		data() {
			return {
				imgSrc: '',
				// type: 0,
				tableList: [],
				isHas: false,
				title: "",
				showSubmitButton: false, // 新增
				showPopup: false,
				highestProbabilityResult:'',  //预测结果
				userResult: '',  //修改结果
			}
		},
		onLoad(res) {
			// console.log(res.type)
			let title = "";
			this.type = res.type;
			if (res.type == 0) {
				title = "三叶青块根识别"
			}
			if (res.type == 1) {
				title = "三叶青叶片识别"
			}
		
			uni.setNavigationBarTitle({
				title: title
			});
			this.title = title;
		},
		mounted() {
		    let vm = this;
		    uni.getStorage({
		        key: 'imagePath',
		        success: function(res) {
		            var imagePath = res.data;  // 这就是图片的路径
		            // 压缩图片
		            // vm.$refs.helangCompress.compress({
		            //     src: imagePath,
		            //     maxSize: 800,
		            //     fileType: 'jpg',
		            //     quality: 0.85,
		            //     minSize: -1
		            // }).then(res => {
		                // 将图片路径赋给 imgSrc，以便在模板中显示图片
		                vm.imgSrc = imagePath;
		                // 上传图片到服务器
		                uni.uploadFile({
		                    url: '',
							// url:"http://127.0.0.1:8086/file",
		                    // filePath: res,
							filePath: imagePath,  // 使用原图路径
		                    fileType: 'image',
		                    name: 'file',
		                    formData: {
		                        'type': vm.type // 注意这里应该是 vm.type，不是 _this.type
		                    },
		                    success: (request) => {
		                        uni.showLoading({
		                            title: '加载中'
									
		                        });
		
		                        if (request.statusCode == '413') {
		                            uni.hideLoading();
		                            uni.showToast({
		                                title: '图片过大,请更换图片再次尝试',
		                                icon: 'none',
		                                duration: 1500
		                            });
		                            return;
		                        }
		                        uni.hideLoading();
		
		                        // 解析服务器返回的识别结果
		                        let str = unescape(request.data.replace(/\\u/g, "%u"));
		                        let s = JSON.parse(str);
		
		                        let cl = s.result;
		                        // if (vm.type == 2) {
		                        //     cl.forEach((item, index) => {
		                        //         cl[index].score = item.probability
		                        //     })
		                        // }
		                        vm.tableList = cl;
		                        uni.hideLoading();
		                        vm.isHas = true;
		                        // 显示提交预测结果的按钮
		                        vm.showSubmitButton = true;
		
		                        let names = s.result[0].name;
		                        let historyData = "";
		                        let date = new Date();
		                        let year = date.getFullYear();
		                        let month = date.getMonth() + 1;
		                        let day = date.getDate();
		                        let hour = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
		                        let minute = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
		                        let second = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();
		                        month >= 1 && month <= 9 ? (month = "0" + month) : "";
		                        day >= 0 && day <= 9 ? (day = "0" + day) : "";
		                        let timer = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
		                        uni.getStorage({
		                            key: 'historys',
		                            success: function(ress) {
		                                console.log(ress)
		                                let dOne = JSON.parse(ress.data);
		                                dOne.unshift({
		                                    date: timer,
		                                    type: vm.title,
		                                    onebe: names
		                                });
		                                uni.setStorage({
		                                    key: 'historys',
		                                    data: JSON.stringify(dOne)
		                                })
		                            },
		                            fail: function() {
		                                let yd = [];
		                                yd.unshift({
		                                    date: timer,
		                                    type: vm.title,
		                                    onebe: names
		                                })
		                                uni.setStorage({
		                                    key: 'historys',
		                                    data: JSON.stringify(yd)
		                                })
		                            }
		                        });
		                    }
		                // });
		            });
		        }
		    });
		},
		
	  methods: {
		  togglePopup() {
		  	this.showPopup = !this.showPopup;
		  	this.highestProbabilityResult = this.tableList[0].name;
		  },
		  submit() {
		  	// this.showPopup = false;
		  	let result = this.userResult || this.highestProbabilityResult;
		  	// 然后你可以使用 `result` 做任何你需要的事情，例如发送到服务器
		  	let timestamp = new Date().getTime();
		  	let filename = result + "-" + timestamp+".png";
		  	
		  	uni.uploadFile({
		  		url: '',
				// url: 'http://127.0.0.1:8086/save',
		  		filePath: this.imgSrc,
		  		name: 'file',
		  		formData: {
		  			'filename': filename  // 传递文件名到服务器
		  		},
		  		success: (uploadFileRes) => {
		  			// console.log(uploadFileRes.data);
		  			// ... 处理上传后的操作 ...
		  			// 显示成功消息
		  			uni.showToast({
		  								title: '成功提交，感谢您的支持！',
		  								icon: 'success',
		  								duration: 2000
		  							});
		  		}
		  	});
		  	this.showPopup = false;
		  },
		  cancel() {
		  	this.showPopup = false;
		  },
	  }
	}
</script>


<style lang="scss">
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.bgs {
		background-color: #4CD964;
	}

	.ybgs {
		background-color: #C0C0C0;
	}


	.popup {
		position: fixed;
		bottom: 0;
		left: 0;
		width: 100%;
		height: 25%;  /* 调整这个值到你需要的高度 */
		background-color: #fff;
		box-sizing: border-box;
		z-index: 999;
	}
 
	
	.mask {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
		z-index: 888;
	}
 
	
	.content_tan {
		.line1 {
			background-color:#00ff7f;
			text-align: center;
			padding: 20rpx;
		}
 
		.line2 {
			padding: 30rpx;
 
			view {
				margin-bottom: 20rpx;
			}
		}
	}
	
	.btn-group {
		box-shadow: 0px -2px 6px rgba(0, 0, 0, 0.5); 
		.btn_position {
			display: flex;
			width: 100%;
			.cancel {
				width: 50%;
				text-align: center;
				padding: 25rpx 0;
				color: #519fe7;
			}
 
			.submit {
				width: 50%;
				background-color: #519fe7;
				text-align: center;
				padding: 25rpx 0;
				color: #fff;
			}
		}
 
	}


</style>