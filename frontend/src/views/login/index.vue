<script setup lang="tsx">
import { useI18n } from "vue-i18n";
import Motion from "./utils/motion";
import { useRouter } from "vue-router";
import { useNav } from "@/layout/hooks/useNav";
import {
  ElForm,
  ElFormItem,
  ElInput,
  ElProgress,
  FormInstance
} from "element-plus";
import { $t, transformI18n } from "@/plugins/i18n";
import { useLayout } from "@/layout/hooks/useLayout";
import { useUserStoreHook } from "@/store/modules/user";
import { initRouter, getTopMenu } from "@/router/utils";
import { bg, avatar, illustration } from "./utils/static";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { ref, reactive, toRaw, onMounted, onBeforeUnmount, watch } from "vue";
import { useDataThemeChange } from "@/layout/hooks/useDataThemeChange";

import dayIcon from "@/assets/svg/day.svg?component";
import darkIcon from "@/assets/svg/dark.svg?component";
import Lock from "@iconify-icons/ri/lock-fill";
import User from "@iconify-icons/ri/user-3-fill";
import { errorNotification, successNotification } from "@/utils/notification";
import { generatePassword } from "@/views/superAdmin/UserManagement/utils/util";
import { addDialog } from "@/components/ReDialog/index";
import { deviceDetection, isAllEmpty } from "@pureadmin/utils";
import { REGEXP_PWD } from "@/views/login/utils/rule";
import Refresh from "@iconify-icons/ep/refresh";
import { initPassword } from "@/api/base";
import { zxcvbn } from "@zxcvbn-ts/core";

defineOptions({
  name: "Login"
});
const router = useRouter();
const loading = ref(false);
const ruleFormRef = ref<FormInstance>();

const { initStorage } = useLayout();
initStorage();

const { t } = useI18n();
const { dataTheme, dataThemeChange } = useDataThemeChange();
dataThemeChange();
const { title } = useNav();

const ruleForm = reactive({
  username: "",
  password: ""
});

const onLogin = async (formEl: FormInstance | undefined) => {
  loading.value = true;
  if (!formEl) return;
  await formEl.validate((valid, fields) => {
    if (valid) {
      useUserStoreHook()
        .loginByUsername({
          username: ruleForm.username,
          password: ruleForm.password
        })
        .then(res => {
          if (res.code === 200) {
            successNotification("登录成功!");
            if (res.resetPwd) {
              initPwd();
            }
            // 获取后端路由
            initRouter().then(() => {
              router.push(getTopMenu(true).path);
            });
          }
        })
        .catch(error => {
          loading.value = false;
          errorNotification(`登录失败:${error.msg}!`);
          ruleForm.password = "";
        });
    } else {
      loading.value = false;
      return fields;
    }
  });
};

/** 使用公共函数，避免`removeEventListener`失效 */
function onkeypress({ code }: KeyboardEvent) {
  if (code === "Enter") {
    onLogin(ruleFormRef.value);
  }
}

const clipboardText = ref("liushuo@cnnp.com.cn");

onMounted(() => {
  window.document.addEventListener("keypress", onkeypress);
});

onBeforeUnmount(() => {
  window.document.removeEventListener("keypress", onkeypress);
});

function initPwd() {
  const pwdForm = reactive({
    newPwd: ""
  });
  const ruleInitFormRef = ref();
  const newPwdLoading = ref(false);
  const curScore = ref();
  watch(
    pwdForm,
    ({ newPwd }) =>
      (curScore.value = isAllEmpty(newPwd) ? -1 : zxcvbn(newPwd).score)
  );
  const pwdProgress = [
    { color: "#e74242", text: "非常弱" },
    { color: "#EFBD47", text: "弱" },
    { color: "#ffa500", text: "一般" },
    { color: "#1bbf1b", text: "强" },
    { color: "#008000", text: "非常强" }
  ];
  const newPwd = () => {
    newPwdLoading.value = true;
    setTimeout(() => {
      pwdForm.newPwd = generatePassword(12);
      newPwdLoading.value = false;
    }, 1000);
  };
  addDialog({
    title: `重置密码`,
    width: "30%",
    draggable: false,
    showClose: false,
    closeOnPressEscape: false,
    closeOnClickModal: false,
    fullscreen: deviceDetection(),
    contentRenderer: () => (
      <>
        <ElForm ref={ruleInitFormRef} model={pwdForm}>
          <ElFormItem
            prop="newPwd"
            rules={[
              {
                required: true,
                message: "请输入新密码",
                trigger: "change"
              },
              {
                validator: (rule, value, callback) => {
                  if (!REGEXP_PWD.test(value)) {
                    callback(
                      new Error(
                        "密码格式应为8-18位数字、字母、符号的任意两种组合"
                      )
                    );
                  } else {
                    callback();
                  }
                },
                trigger: "blur"
              }
            ]}
          >
            <ElInput
              clearable
              show-password
              type="password"
              v-model={pwdForm.newPwd}
              placeholder="请输入新密码"
            >
              {{
                append: () => (
                  <el-button
                    icon={useRenderIcon(Refresh)}
                    loading-icon={useRenderIcon(Refresh)}
                    loading={newPwdLoading.value}
                    onClick={() => {
                      newPwd();
                    }}
                  >
                    随机密码
                  </el-button>
                )
              }}
            </ElInput>
          </ElFormItem>
        </ElForm>
        <div class="mt-4 flex">
          {pwdProgress.map(({ color, text }, idx) => (
            <div class="w-[19vw]" style={{ marginLeft: idx !== 0 ? "4px" : 0 }}>
              <ElProgress
                striped
                striped-flow
                duration={curScore.value === idx ? 6 : 0}
                percentage={curScore.value >= idx ? 100 : 0}
                color={color}
                stroke-width={10}
                show-text={false}
              />
              <p
                class="text-center"
                style={{ color: curScore.value === idx ? color : "" }}
              >
                {text}
              </p>
            </div>
          ))}
        </div>
      </>
    ),
    closeCallBack: () => (pwdForm.newPwd = ""),
    beforeSure: done => {
      ruleInitFormRef.value.validate(valid => {
        if (valid) {
          // 表单规则校验通过
          initPassword(pwdForm.newPwd).then(() => {
            // 根据实际业务使用pwdForm.newPwd和row里的某些字段去调用重置用户密码接口即可
            done(); // 关闭弹框
            successNotification(`密码重置成功`);
          });
        }
      });
    }
  });
}
</script>

<template>
  <div class="select-none">
    <img :src="bg" class="wave" alt="" />
    <div class="flex-c absolute right-5 top-3">
      <!-- 主题 -->
      <el-switch
        v-model="dataTheme"
        inline-prompt
        :active-icon="dayIcon"
        :inactive-icon="darkIcon"
        @change="dataThemeChange"
      />
    </div>
    <div class="login-container">
      <div class="img">
        <component :is="toRaw(illustration)" />
      </div>
      <div class="login-box">
        <div class="login-form">
          <avatar class="avatar" />
          <Motion>
            <h2 class="outline-none">{{ title }}</h2>
          </Motion>

          <el-form ref="ruleFormRef" :model="ruleForm" size="large">
            <Motion :delay="100">
              <el-form-item
                :rules="[
                  {
                    required: true,
                    message: transformI18n($t('login.pureUsernameReg')),
                    trigger: 'blur'
                  }
                ]"
                prop="username"
              >
                <el-input
                  v-model="ruleForm.username"
                  clearable
                  :placeholder="t('login.pureUsername')"
                  :prefix-icon="useRenderIcon(User)"
                >
                  <template #append>@cnnp.com.cn</template>
                </el-input>
              </el-form-item>
            </Motion>

            <Motion :delay="150">
              <el-form-item
                prop="password"
                :rules="[
                  {
                    required: true,
                    message: transformI18n($t('login.purePassWordReg')),
                    trigger: 'blur'
                  }
                ]"
              >
                <el-input
                  v-model="ruleForm.password"
                  clearable
                  show-password
                  :placeholder="t('login.purePassword')"
                  :prefix-icon="useRenderIcon(Lock)"
                />
              </el-form-item>
            </Motion>

            <Motion :delay="250">
              <el-button
                class="w-full mt-4"
                size="default"
                type="primary"
                :loading="loading"
                @click="onLogin(ruleFormRef)"
              >
                {{ t("login.pureLogin") }}
              </el-button>
            </Motion>
            <Motion :delay="300">
              <el-row class="flex mt-4" justify="space-between">
                <el-link
                  href="https://hn-disk.hnpc.cc/ucdisk/s/AraYn2"
                  target="_blank"
                  :underline="false"
                  >使用说明下载</el-link
                >
                <div>
                  <el-text type="info" size="small"
                    >若有使用问题请邮件联系:</el-text
                  >
                  <el-tooltip
                    class="box-item"
                    effect="dark"
                    content="双击复制邮箱"
                    placement="bottom"
                  >
                    <el-button
                      v-copy="clipboardText"
                      type="primary"
                      link
                      size="small"
                      >刘硕</el-button
                    >
                  </el-tooltip>
                </div>
              </el-row>
            </Motion>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url("@/style/login.css");
</style>

<style lang="scss" scoped>
:deep(.el-input-group__append, .el-input-group__prepend) {
  padding: 0 10px;
}

.translation {
  ::v-deep(.el-dropdown-menu__item) {
    padding: 5px 40px;
  }

  .check-zh {
    position: absolute;
    left: 20px;
  }

  .check-en {
    position: absolute;
    left: 20px;
  }
}
</style>
