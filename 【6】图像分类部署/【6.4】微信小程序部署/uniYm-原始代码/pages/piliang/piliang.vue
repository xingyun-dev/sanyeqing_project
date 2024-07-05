<template>
	<view>
		<swiper autoplay @change="updateIndex" class="content":class="{bgs:(imgSrc!=''),ybgs:(imgSrc=='')}" style="height: 30vh;">
		    <swiper-item v-for="(imgSrc, index) in uploadedImages" :key="index" style="display: flex; justify-content: center; align-items: center;">
		        <image :src="imgSrc"></image>
		    </swiper-item>
		</swiper>
		<view style="display: flex; justify-content: center; align-items: center;">当前图片序号：{{ currentIndex + 1 }}</view>  <!-- +1 是因为序号从 0 开始 -->
		<helang-compress ref="helangCompress"></helang-compress>
		<button type="primary" @click="upfile()" style="width: 70%;margin-left: 15%;margin-top: 10%;">提交图片</button>
		<button type="primary" @click="togglePopup" style="width: 70%;margin-left: 15%;margin-top: 10%;"
			v-if="showSubmitButton">提交预测结果</button>
		<view class="box" v-if="isHas">
			<t-table>
				<t-tr>
					<t-th>序号</t-th>

					<t-th>top_1可能性</t-th>
					<t-th>top_2可能性</t-th>
					<t-th>top_3可能性</t-th>
				</t-tr>
				<t-tr v-for="row in tableList" :key="row.index">
				    <t-td>{{ row.index }}</t-td>
					<t-td>{{ row.top1 && (row.top1.name + ': ' + (row.top1.score * 100).toFixed(2) + '%') }}</t-td>
					<t-td>{{ row.top2 && (row.top2.name + ': ' + (row.top2.score * 100).toFixed(2) + '%') }}</t-td>
					<t-td>{{ row.top3 && (row.top3.name + ': ' + (row.top3.score * 100).toFixed(2) + '%') }}</t-td>
				</t-tr>
			</t-table>
		</view>
		
		<view v-if="showPopup" class="popup">
			<view class="content_tan">
				<view class="line1">
					<view>识别结果(如果不修改，默认提交预测结果)</view>
				</view>
				<view class="line2">
					<view style="display: flex; justify-content: center; align-items: center;">请谨慎提交批量处理结果！</view>
					<button type="warn" @click="openEditPage" style="width: 50%;">展开修改</button>
				</view>
			</view>
			<view class="btn-group">
				<view class="btn_position">
					<view class="cancel" @click="cancel">取消</view>
					<view class="submit" @click="submit">直接提交</view>
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
		data() {
			return {
				imgSrc: '',
				// type: 0,
				tableList: [],
				isHas: false,
				title: "",
				showSubmitButton: false, // 新增
				showPopup: false,
				showEditPopup: false,
				userResult: '',  //修改结果
			    currentIndex: 0,  // 新增
				uploadedImages: [],  // 图像轮播图
			}
		},
		onLoad(res) {
			console.log(res.type)
			let title = "";
			this.type = res.type;
			if (res.type == 0) {
				title = "块根图像分类批量"
			}
			if (res.type == 1) {
				title = "叶片图像分类批量"
			}

			uni.setNavigationBarTitle({
				title: title
			});
			this.title = title;
		},
		methods: {

			// process() {
			// 	if (this.type == 0) {
			// 		this.upfile();
			// 	}
			// },
			updateIndex(event) {
			        this.currentIndex = event.detail.current;
			    },
			
			openEditPage() {
			   uni.setStorageSync('tableList', JSON.stringify(this.tableList));
			   uni.setStorageSync('uploadedImages', JSON.stringify(this.uploadedImages));
			   uni.navigateTo({
			           url: '/pages/bodys/Edit'
			       });
			    },
			
			
			
			togglePopup() {
				this.showPopup = !this.showPopup;
				// this.highestProbabilityResult = this.tableList[0].name;
			},
			submit() {
			    let vm = this;
			
			    for (let i = 0; i < vm.tableList.length; i++) {
			        let result = vm.tableList[i].top1.name; // 使用每个图片的最高预测结果
			        let timestamp = new Date().getTime();
			         let filename = result + "-" + timestamp + "-" + i+".png"; // 添加序列号到文件名
			
			        uni.uploadFile({
			            // url:"http://127.0.0.1:8086/save",
						url: '',
			            filePath: vm.uploadedImages[i],
			            name: 'file',
			            formData: {
			                'filename': filename
			            },
			            success: (uploadFileRes) => {
			                console.log(uploadFileRes.data);
			                uni.showToast({
			                    title: '成功提交，感谢您的支持！',
			                    icon: 'success',
			                    duration: 2000
			                });
			            },
			            fail: (error) => {
			                console.log('上传失败：', error);
			                uni.showToast({
			                    title: '上传失败',
			                    icon: 'none',
			                    duration: 2000
			                });
			            }
			        });
			    }
			
			    vm.showPopup = false;
			},
			
		
			cancel() {
				this.showPopup = false;
			},
			
			async upfile() {
			    let vm = this;
			
			    uni.chooseImage({
			        count: 120,
			        success: async function(ress) {
			            // console.log(ress)
			            for (let imgSrc of ress.tempFilePaths) { // 遍历所有图片
			                let s; // 定义 s 在循环内
			                vm.imgSrc = imgSrc;
			                vm.uploadedImages.push(imgSrc); // 添加图片到轮播图
			                // await vm.$refs.helangCompress.compress({
			                //     src: imgSrc,
			                //     maxSize: 800,
			                //     fileType: 'jpg',
			                //     quality: 0.85,
			                //     minSize: -1
			                // }).then(async (res) => {
			                    await new Promise((resolve, reject) => {
			                        uni.uploadFile({
			                            // sizeType: ['compressed'],
										sizeType: ['original'],  // 上传原图
			                            // url:"http://127.0.0.1:8086/file",
										url: '',
			                            // filePath: res,
										filePath: imgSrc,  // 使用原始图片路径
			                            fileType: 'image',
			                            name: 'file',
			                            formData: {
			                                'type': vm.type
			                            },
			                            success: (request) => {
			                                if (request.statusCode == '413') {
			                                    console.log('d12dw')
			                                    uni.hideLoading();
			                                    uni.showToast({
			                                        title: '图片过大,请更换图片再次尝试',
			                                        icon: 'none',
			                                        duration: 1500
			                                    });
			                                    reject();
			                                    return;
			                                }
			
			                                let str = unescape(request.data.replace(/\\u/g, "%u"));
			                                s = JSON.parse(str) // 在这里更新 s 的值
			
			                                let cl = s.result;
			                                // if (vm.type == 2) {
			                                //     cl.forEach((item, index) => {
			                                //         cl[index].score = item.probability
			                                //     })
			                                // }
			
			                                let newRow = {
			                                    index: vm.tableList.length + 1,
			                                    top1: cl[0] ? {name: cl[0].name, score: cl[0].score} : null,
			                                    top2: cl[1] ? {name: cl[1].name, score: cl[1].score} : null,
			                                    top3: cl[2] ? {name: cl[2].name, score: cl[2].score} : null,
												userResult: '',  
			                                };
			                                vm.tableList.push(newRow);
			
			                                // 移动到循环内部
			                                vm.isHas = true;
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
			
			                                resolve();
			                            },
			                            fail: (error) => {
			                                reject(error);
			                            }
			                        });
			                    });
			                // });
			            }
			        }
			    });
			}
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