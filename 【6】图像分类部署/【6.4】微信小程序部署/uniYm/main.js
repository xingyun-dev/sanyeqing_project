import Vue from 'vue'
import App from './App'
// //挂载tabbar组件于全局
import zdyTabbar from "components/zdy-tabbar.vue"
 
// 注册全局组件
Vue.component('zdy-tabbar', zdyTabbar)


Vue.config.productionTip = false

App.mpType = 'app'
const app = new Vue({
    ...App
})
app.$mount()
