<script setup lang="tsx">
import { addDialog, closeDialog } from "@/components/ReDialog";
import { deviceDetection } from "@pureadmin/utils";
import { h, ref } from "vue";
import MaterialBorrowDialog from "./dialog/MaterialBorrowDialog.vue";
import useDialogStore from "./store";
import { getAllMaterialMeta } from "@/api/material";
import { createBorrowed } from "@/api/home";
import type { borrowInfo } from "./types";
import type { MaterialItem } from "@/types/base";
import { successNotification } from "@/utils/notification";
import { message } from "@/utils/message";

defineOptions({
  name: "Welcome"
});
const store = useDialogStore();
const bMForm = ref();
const toolBtnLoading = ref(false);
const keyBtnLoading = ref(false);
// 借用物资弹窗
const borrowMaterial = () => {
  toolBtnLoading.value = true;
  getAllMaterialMeta("glb", "tool").then(res => {
    addDialog({
      title: "物资借用",
      props: {
        borrowInfo: {
          uuid: 0,
          username: "",
          phone: "",
          depart: "",
          reason: "",
          baseData: res.data
        }
      },
      width: "60%",
      draggable: true,
      fullscreen: deviceDetection(),
      closeOnClickModal: false,
      contentRenderer: () => h(MaterialBorrowDialog, { ref: bMForm }),
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
              const done = () => {
                closeDialog(options, index);
                store.resetActive();
              };
              const curData = options.props.borrowInfo as borrowInfo;
              const borrowItemList = [];
              for (const item of curData.baseData) {
                if (item.borrowing !== undefined && item.borrowing > 0) {
                  delete item.created_at;
                  delete item.updated_at;
                  delete item.id;
                  borrowItemList.push(item);
                }
              }
              if (curData.reason == "" || borrowItemList.length == 0) {
                message("借用信息或借用原因不得为空！", { type: "warning" });
                return;
              }
              curData.baseData = borrowItemList as [MaterialItem];
              createBorrowed(curData).then(() => {
                successNotification("物资借用流程发起成功！");
                toolBtnLoading.value = false;
                done();
              });
            }}
          >
            完成
          </el-button>
        </>
      ),
      beforeClose(done) {
        toolBtnLoading.value = false;
        done();
        store.resetActive();
      }
    });
  });
};

// 借用钥匙弹窗
const borrowKey = () => {
  keyBtnLoading.value = true;
  getAllMaterialMeta("glb", "key").then(res => {
    addDialog({
      title: "钥匙借用",
      props: {
        borrowInfo: {
          uuid: 0,
          username: "",
          phone: "",
          depart: "",
          reason: "",
          baseData: res.data
        }
      },
      width: "60%",
      draggable: true,
      fullscreen: deviceDetection(),
      closeOnClickModal: false,
      contentRenderer: () => h(MaterialBorrowDialog, { ref: bMForm }),
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
              const done = () => {
                closeDialog(options, index);
                store.resetActive();
              };
              const curData = options.props.borrowInfo as borrowInfo;
              const borrowItemList = [];
              for (const item of curData.baseData) {
                if (item.borrowing !== undefined && item.borrowing > 0) {
                  delete item.created_at;
                  delete item.updated_at;
                  delete item.id;
                  borrowItemList.push(item);
                }
              }
              if (curData.reason == "" || borrowItemList.length == 0) {
                message("借用信息或借用原因不得为空！", { type: "warning" });
                return;
              }
              curData.baseData = borrowItemList as [MaterialItem];
              createBorrowed(curData).then(() => {
                successNotification("钥匙借用流程发起成功！");
                keyBtnLoading.value = false;
                done();
              });
            }}
          >
            完成
          </el-button>
        </>
      ),
      beforeClose(done) {
        keyBtnLoading.value = false;
        done();
        store.resetActive();
      }
    });
  });
};
</script>

<template>
  <div class="main">
    <el-space alignment="center">
      <el-button
        class="largeBtn"
        type="primary"
        :loading="toolBtnLoading"
        plain
        @click="borrowMaterial"
        >物资借用</el-button
      >
      <el-button
        class="largeBtn"
        type="primary"
        :loading="keyBtnLoading"
        plain
        @click="borrowKey"
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
