<script setup lang="ts">
import { computed, reactive, Ref, ref } from "vue";
import Segmented, { OptionsType } from "@/components/ReSegmented";
import type { FormRules } from "element-plus";
import type { userInfo } from "../types";

const accountFormRef = ref();
const infoFormRef = ref();
function getAccountRef() {
  return accountFormRef.value;
}
function getInfoRef() {
  return infoFormRef.value;
}
defineExpose({ getAccountRef, getInfoRef });

type userType = {
  userInfo: userInfo & {
    disable: boolean;
  };
};

const props = withDefaults(defineProps<userType>(), {
  userInfo: () => ({
    account: "",
    password: "",
    name: "",
    phone: "",
    depart: "",
    disable: false
  })
});

const tabIndex = ref(0);
const userInfo = reactive(props.userInfo);

const segmentedDisable = computed(() => {
  return userInfo.account.length > 0 || userInfo.name.length > 0;
});

const segmentedOptions: Array<OptionsType> = [
  {
    label: "账号密码",
    value: 0
  },
  {
    label: "手动输入",
    value: 1,
    disabled: userInfo.disable
  }
];
type accountType = {
  account: string;
  password: string;
};
type infoType = {
  name: string;
  phone: string;
  depart: string;
};

const accountRules = reactive<FormRules<accountType>>({
  account: [{ required: true, message: "请输入工号", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }]
});
const infoRules = reactive<FormRules<infoType>>({
  name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
  phone: [{ required: true, message: "请输入手机号", trigger: "blur" }],
  depart: [{ required: true, message: "请输入部门", trigger: "blur" }]
});
const formSize: Ref<"" | "default" | "small" | "large"> = ref("default");
</script>

<template>
  <div>
    <Segmented
      v-model="tabIndex"
      :options="segmentedOptions"
      size="large"
      :disabled="segmentedDisable"
    />
    <el-tabs v-model="tabIndex" type="card" class="myTabs">
      <el-tab-pane :name="segmentedOptions[0].value">
        <el-card shadow="never">
          <el-form
            ref="accountFormRef"
            style="max-width: 600px"
            :model="userInfo"
            :rules="accountRules"
            label-width="auto"
            class="demo-ruleForm"
            :size="formSize"
            status-icon
          >
            <el-form-item label="工号" prop="account">
              <el-input v-model="userInfo.account" placeholder="工号" />
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input
                v-model="userInfo.password"
                type="password"
                placeholder="密码"
                show-password
              />
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
      <el-tab-pane :name="segmentedOptions[1].value">
        <el-card shadow="never">
          <el-form
            ref="infoFormRef"
            style="max-width: 600px"
            :model="userInfo"
            :rules="infoRules"
            label-width="auto"
            class="demo-ruleForm"
            :size="formSize"
            status-icon
          >
            <el-form-item label="姓名" prop="name">
              <el-input v-model="userInfo.name" placeholder="请输入姓名" />
            </el-form-item>
            <el-form-item label="电话" prop="phone">
              <el-input v-model="userInfo.phone" placeholder="请输入电话号码" />
            </el-form-item>
            <el-form-item label="部门" prop="depart">
              <el-input
                v-model="userInfo.depart"
                placeholder="xx公司xx处xx科/值xx班"
              />
            </el-form-item>
          </el-form>
        </el-card>
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
      .el-tabs__item {
        border: 0;
        padding: 0;
      }
    }
  }
  .el-tabs__content {
    padding-bottom: 4px;
  }
}
</style>
