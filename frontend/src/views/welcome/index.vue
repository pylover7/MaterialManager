<script setup lang="tsx">
import { addDialog, closeDialog } from "@/components/ReDialog";
import { deviceDetection } from "@pureadmin/utils";
import { h, ref } from "vue";
import MaterialBorrowDialog from "./dialog/MaterialBorrowDialog.vue";
import useDialogStore from "./store";
import { addBorrowed, getAllMaterialMeta } from "@/api/material";
import type { borrowInfo } from "./types";
import { successNotification } from "@/utils/notification";
import { message } from "@/utils/message";
import type { MaterialItem } from "@/types/material";

defineOptions({
  name: "Welcome"
});
const store = useDialogStore();
const bMForm = ref();
const btnLoading = ref(false);
// 借用物资弹窗
const borrowMaterial = (area: string) => {
  btnLoading.value = true;
  getAllMaterialMeta(area, "tool").then(res => {
    addDialog({
      title: "物资借用",
      props: {
        borrowInfo: {
          uuid: 0,
          username: "",
          nickname: "",
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
              addBorrowed(curData)
                .then(() => {
                  successNotification("物资借用流程发起成功！");
                  done();
                })
                .finally(() => {
                  btnLoading.value = false;
                });
            }}
          >
            完成
          </el-button>
        </>
      ),
      beforeClose(done) {
        btnLoading.value = false;
        done();
        store.resetActive();
      }
    });
  });
};

// 借用钥匙弹窗
const borrowKey = (area: string) => {
  btnLoading.value = true;
  getAllMaterialMeta(area, "key").then(res => {
    addDialog({
      title: "钥匙借用",
      props: {
        borrowInfo: {
          uuid: 0,
          username: "",
          nickname: "",
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
              addBorrowed(curData)
                .then(() => {
                  successNotification("钥匙借用流程发起成功！");
                  done();
                })
                .finally(() => {
                  btnLoading.value = false;
                });
            }}
          >
            完成
          </el-button>
        </>
      ),
      beforeClose(done) {
        btnLoading.value = false;
        done();
        store.resetActive();
      }
    });
  });
};
</script>

<template>
  <div class="main">
    <el-scrollbar>
      <el-space :noresize="true">
        <el-card class="box-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>隔离办</span>
            </div>
          </template>
          <el-space alignment="center" direction="vertical">
            <el-button
              class="largeBtn"
              type="primary"
              :loading="btnLoading"
              plain
              @click="borrowMaterial('glb')"
              >物资借用</el-button
            >
            <el-button
              class="largeBtn"
              type="primary"
              :loading="btnLoading"
              plain
              @click="borrowKey('glb')"
              >钥匙借用</el-button
            >
          </el-space>
        </el-card>
        <el-card class="box-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>辅控</span>
            </div>
          </template>
          <el-space alignment="center" direction="vertical">
            <el-button
              class="largeBtn"
              type="primary"
              :loading="btnLoading"
              plain
              @click="borrowMaterial('fk')"
              >物资借用</el-button
            >
            <el-button
              class="largeBtn"
              type="primary"
              :loading="btnLoading"
              plain
              @click="borrowKey('fk')"
              >钥匙借用</el-button
            >
          </el-space>
        </el-card>
        <el-card class="box-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>网控</span>
            </div>
          </template>
          <el-space alignment="center" direction="vertical">
            <el-button
              class="largeBtn"
              type="primary"
              :loading="btnLoading"
              plain
              @click="borrowMaterial('wk')"
              >物资借用</el-button
            >
            <el-button
              class="largeBtn"
              type="primary"
              :loading="btnLoading"
              plain
              @click="borrowKey('wk')"
              >钥匙借用</el-button
            >
          </el-space>
        </el-card>
      </el-space>
    </el-scrollbar>
  </div>
</template>

<style scoped lang="scss">
.main {
  height: 100%;
}
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

.box-card {
  border: 2px dashed var(--el-border-color);
}
</style>
