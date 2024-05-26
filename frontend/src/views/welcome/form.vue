<script setup lang="ts">
import { ref } from "vue";
import useDialogStore from "./store";

const formRef = ref();
function getRef() {
  return formRef.value;
}
defineExpose({ getRef });

const store = useDialogStore();
</script>

<template>
  <div>
    <el-steps :active="store.active" align-center>
      <el-step title="物资选择" />
      <el-step title="确认信息" />
    </el-steps>
    <el-tabs ref="formRef" v-model="store.active" class="myTabs">
      <el-tab-pane :name="0">
        <p>test1</p>
      </el-tab-pane>
      <el-tab-pane :name="1">
        <p>test2</p>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped lang="scss">
.tab-pane > .el-tabs__items {
  padding: 0;
}

:deep(.myTabs) {
  .el-tabs__header {
    border-radius: var(--el-border-radius-base);
    border: 0;
    height: 0;
    .el-tabs__nav {
      border: 0;
      height: 0;
      .el-tabs__item {
        border: 0;
        padding: 0;
      }
    }
  }
}
</style>
