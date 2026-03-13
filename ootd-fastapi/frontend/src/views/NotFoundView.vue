<template>
  <div class="not-found-view">
    <div class="content">
      <h1>404</h1>
      <p>抱歉，您访问的页面不存在</p>
      <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.not-found-view {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.content {
  text-align: center;
  color: #fff;
}

.content h1 {
  font-size: 120px;
  margin: 0 0 20px;
  font-weight: bold;
}

.content p {
  font-size: 20px;
  margin: 0 0 30px;
}
</style>
