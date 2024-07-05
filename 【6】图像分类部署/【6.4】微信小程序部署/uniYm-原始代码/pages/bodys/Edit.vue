<template>
<view>
	<view style="margin:10%;">如果预测结果与您已知的实际结果不符，请填写您的已知结果。未填写修改结果的默认按预测结果提交
		感谢您的支持！</view>

    <div>
        <t-table>
            <t-tr>
                <t-th>序号</t-th>
                <t-th>预测结果</t-th>
                <t-th>修改结果</t-th>
            </t-tr>
            <t-tr v-for="row in tableList" :key="row.index">
                <t-td>{{ row.index }}</t-td>
                <t-td>{{ row.top1 && row.top1.name }}</t-td>
                <t-td><input v-model="row.userResult" /></t-td>
            </t-tr>
        </t-table>
		<view class="btn-group">
			<view class="btn_position">
        <button class="cancel"  @click="cancel">取消</button>
		<button class="submit"  @click="submitEdits">确认提交</button>
		</view>
		</view>
    </div>
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
                tableList: [],
                uploadedImages: [],
            };
        },
	created() {
		    this.tableList = JSON.parse(uni.getStorageSync('tableList'));
		    this.uploadedImages = JSON.parse(uni.getStorageSync('uploadedImages'));
		},
   
    methods: {
        cancel() {
                this.tableList.forEach(row => {
                            row.userResult = '';
                        });
				uni.removeStorageSync('tableList');
				uni.removeStorageSync('uploadedImages');
                uni.navigateBack();
                },
        
        submitEdits() {
                // 在这里处理修改后的结果，例如发送到服务器...
        	let vm = this;
        				
        	for (let i = 0; i < vm.tableList.length; i++) {
        		let row = vm.tableList[i];
        		let result = row.userResult || row.top1.name;  // 使用修改后的结果，如果没有修改后的结果，就使用预测结果
        	    let timestamp = new Date().getTime();
        	    let filename = result + "-" + timestamp + "-" + i+".png"; // 添加序列号到文件名
        				
        	    uni.uploadFile({
        	        // url: 'http://10.13.22.218:8086/save',
					url: '',
        	        filePath: vm.uploadedImages[i],
        	        name: 'file',
        	        formData: {
        	            'filename': filename
        	        },
        	        success: (uploadFileRes) => {
        	            // console.log(uploadFileRes.data);
        	            uni.showToast({
        	                title: '成功提交，感谢您的支持！',
        	                icon: 'success',
        	                duration: 2000
        	            });
						if (i === vm.tableList.length - 1) { // 确保所有文件都已上传
						                    uni.removeStorageSync('tableList');
						                    uni.removeStorageSync('uploadedImages');
						                }
						// console.log(this.tableList)
        	        },
        	        fail: (error) => {
        	            // console.log('上传失败：', error);
        	            uni.showToast({
        	                title: '上传失败',
        	                icon: 'none',
        	                duration: 2000
        	            });
        	        }
        	    });
        	}
        				
        	uni.navigateBack();
            },
        
    },
};
</script>


<style lang="scss">
	.btn-group {
		box-shadow: 0px -2px 6px rgba(0, 0, 0, 0.5); 
		position: fixed;  /* 这将使按钮固定在一个位置 */
		bottom: 0;  /* 这将使按钮固定在底部 */
		width: 100%;  /* 这将使按钮的宽度和屏幕的宽度一样 */
		.btn_position {
			display: flex;
			width: 100%;
			.cancel {
				width: 50%;
				text-align: center;
				padding: 4rpx 0;  /* 减小内边距来降低按钮的高度 */
				color: #519fe7;
			}
	 
			.submit {
				width: 50%;
				background-color: #519fe7;
				text-align: center;
				padding: 4rpx 0;  
				color: #fff;
			}
		}
	 
	}
	
</style>