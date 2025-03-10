<template>
    <view>
<login-box @passwordLogin="passwordLogin" @capChaLogin="capChaLogin" @getresist="getresist"></login-box>
	</view>
</template>

<script>
	
	import loginBox from '@/components/login_register.vue'
	export default {
		components:{
			loginBox
		},
        methods: {
			getresist(e){
				console.log(e,'注册数据!');
			},
			capChaLogin(e){
				console.log(e,'验证码登录');
			},
			passwordLogin(e){
				console.log(e,'密码登录');
			}
        },
		}
		
</script>