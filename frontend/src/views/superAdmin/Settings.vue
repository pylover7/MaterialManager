<script lang="ts" setup>
import { onMounted, reactive, ref, Ref } from "vue";
import type { FormInstance, FormRules } from "element-plus";
import { successNotification, warningNotification } from "@/utils/notification";
import { dbInfoType } from "@/types/superAdmin";
import { removeToken } from "@/utils/auth";
import { resetRouter, router } from "@/router";
import { message } from "@/utils/message";
import Segmented, { OptionsType } from "@/components/ReSegmented";
import { getDB, setDB, testDB } from "@/api/admin";

defineOptions({
  name: "Settings"
});

const segmentedOptions: Array<OptionsType> = [
  {
    label: "数据库",
    value: 0
  },
  {
    label: "其他",
    value: 1
  }
];
const tabIndex = ref(0);

onMounted(async () => {
  await initDbInfoForm();
});

// 表单大小
const formSize: Ref<"" | "default" | "small" | "large"> = ref("default");
// 表格ref
const dbFormRef = ref<FormInstance>();
// 表格信息
const dbInfoForm = reactive<dbInfoType>({
  start: "",
  host: "",
  port: 3306,
  database: "",
  password: "",
  username: ""
});
// 初始化表格信息
const initDbInfoForm = async () => {
  getDB().then(res => {
    for (let key in res.data) {
      dbInfoForm[key] = res.data[key];
    }
  });
};
// 校验规则
const rules = reactive<FormRules<dbInfoType>>({
  start: [
    {
      required: true,
      message: "请选择一种数据库",
      trigger: "change"
    }
  ],
  host: [{ required: true, message: "请输入IP地址或域名", trigger: "blur" }],
  port: [
    {
      required: true,
      message: "请输入正确的端口号",
      trigger: "blur"
    }
  ],
  username: [
    { required: true, message: "请输入数据库用户名", trigger: "blur" }
  ],
  password: [
    {
      required: true,
      message: "请输入数据库密码",
      trigger: "blur"
    }
  ],
  database: [
    {
      required: true,
      message: "请输入数据库名称",
      trigger: "blur"
    }
  ]
});
// 重置按钮回调
const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.resetFields();
};
// 测试按钮回调
const testBtn = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate((valid, fields) => {
    if (valid) {
      testDB(dbInfoForm)
        .then(res => {
          successNotification(res.msg);
          setBtnDisabled.value = false;
        })
        .catch(err => {
          warningNotification(err.msg);
        });
    }
  });
};
// 保存按钮是否可用
const setBtnDisabled = ref(true);
// 保存按钮回调
const setBtn = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate((valid, fields) => {
    if (valid) {
      setDB(dbInfoForm)
        .then(res => {
          successNotification(res.msg);
          initDbInfoForm();
          removeToken();
          resetRouter();
          router.push("/login").then(() => {
            message("请重新登录！", { type: "warning" });
          });
        })
        .catch(err => {
          warningNotification(err.msg);
        });
    }
  });
};
</script>

<template>
  <div>
    <Segmented v-model="tabIndex" :options="segmentedOptions" size="large" />
    <el-tabs v-model="tabIndex" class="myTabs" type="card">
      <el-tab-pane :name="segmentedOptions[0].value">
        <el-card shadow="never">
          <h4>数据库设置</h4>
          <el-divider />
          <el-form
            ref="dbFormRef"
            :model="dbInfoForm"
            :rules="rules"
            :size="formSize"
            class="demo-ruleForm"
            label-width="auto"
            status-icon
            style="max-width: 600px"
          >
            <el-form-item label="数据库种类" prop="start">
              <el-select v-model="dbInfoForm.start" placeholder="请选择">
                <el-option label="mysql" value="mysql" />
              </el-select>
            </el-form-item>
            <el-form-item label="IP或域名" prop="host">
              <el-input v-model="dbInfoForm.host" placeholder="127.0.0.1" />
            </el-form-item>
            <el-form-item label="端口" prop="port">
              <el-input v-model.number="dbInfoForm.port" placeholder="3306" />
            </el-form-item>
            <el-form-item label="用户名" prop="username">
              <el-input v-model="dbInfoForm.username" placeholder="test" />
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input
                v-model="dbInfoForm.password"
                placeholder="test_pwd"
                type="password"
              />
            </el-form-item>
            <el-form-item label="数据库名称" prop="database">
              <el-input v-model="dbInfoForm.database" placeholder="test" />
            </el-form-item>
            <el-form-item>
              <el-popconfirm
                title="确定重置吗？"
                @confirm="resetForm(dbFormRef)"
              >
                <template #reference>
                  <el-button type="danger">重置</el-button>
                </template>
              </el-popconfirm>
              <el-button plain type="warning" @click="testBtn(dbFormRef)">
                测试连接
              </el-button>
              <el-button
                :disabled="setBtnDisabled"
                type="success"
                @click="setBtn(dbFormRef)"
                >保存
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
      <el-tab-pane :name="segmentedOptions[1].value">
        <p>其他</p>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style lang="scss" scoped>
.tab-pane > .el-tabs__items {
  padding: 0;
}

:deep(.myTabs) {
  .el-tabs__header {
    height: 0;
    border: 0;
    border-radius: var(--el-border-radius-base);

    .el-tabs__nav {
      border: 0;

      .el-tabs__item {
        padding: 0;
        border: 0;
      }
    }
  }
}
</style>
