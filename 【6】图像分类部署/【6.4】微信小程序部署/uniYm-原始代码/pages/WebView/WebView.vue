<!-- WebView.vue 页面 -->
<template>
  <web-view :src="url"></web-view>
</template>

<script>
export default {
  data() {
    return {
      url: ''
    };
  },
  onLoad(options) {
    this.url = options.url;
  }
};
</script>
