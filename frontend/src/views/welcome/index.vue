<script setup lang="tsx">
import { addDialog, closeDialog } from "@/components/ReDialog";
import { deviceDetection } from "@pureadmin/utils";
import { h, ref } from "vue";
import borrowForm from "./form.vue";
import useDialogStore from "./store";

defineOptions({
  name: "Welcome"
});
const store = useDialogStore();
const bMForm = ref();
// 借用物资弹窗
const borrowMaterial = () => {
  addDialog({
    title: "物资借用",
    props: {},
    width: "60%",
    draggable: true,
    fullscreen: deviceDetection(),
    closeOnClickModal: false,
    contentRenderer: () => h(borrowForm, { ref: bMForm }),
    footerRenderer: ({ options, index }) => (
      <>
        <el-button
          v-show={store.active !== 0}
          type="primary"
          onClick={() => store.prevActive()}
        >
          上一步
        </el-button>
        <el-button
          v-show={store.active < 1}
          type="primary"
          onClick={() => store.nextActive()}
        >
          下一步
        </el-button>
        <el-button
          v-show={store.active == 1}
          type="success"
          onClick={() => {
            closeDialog(options, index);
            store.resetActive();
          }}
        >
          完成
        </el-button>
      </>
    ),
    beforeSure(done, { options }) {
      const formRef = bMForm.value.getRef();
      console.log(formRef);
      done();
    }
  });
};

// 借用钥匙弹窗
const borrowKey = () => {};
</script>

<template>
  <div class="main">
    <el-space alignment="center">
      <el-button class="largeBtn" type="primary" plain @click="borrowMaterial"
        >物资借用</el-button
      >
      <el-button class="largeBtn" type="primary" plain @click="borrowKey"
        >钥匙借用</el-button
      >
    </el-space>
  </div>
</template>

<style scoped lang="scss">
.largeBtn {
  width: 400px;
  height: 200px;
  font-size: 24px;
  border-radius: 20px;
  margin: 20px;
  border: 0;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}
</style>
