<script setup lang="ts">
import { h, onMounted, ref } from "vue";
import useDialogStore from "../store";
import Search from "@iconify-icons/ep/search";
import Add from "@iconify-icons/fluent/add-12-filled";
import Subtract from "@iconify-icons/fluent/subtract-12-filled";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { useUserStoreHook } from "@/store/modules/user";
import { addDialog } from "@/components/ReDialog/index";
import verifyDialog from "./VerifyDialog.vue";
import type { userInfo } from "../types";
import type { borrowInfo } from "../types";
import { auth } from "@/api/base";
import { MaterialItem } from "@/types/material";

type materialItemList = {
  borrowInfo: borrowInfo;
};

const formRef = ref();
function getRef() {
  return formRef.value;
}
defineExpose({ getRef });

const store = useDialogStore();

const props = withDefaults(defineProps<materialItemList>(), {
  borrowInfo: () => ({
    uuid: "",
    username: "",
    phone: "",
    depart: "",
    reason: "",
    baseData: [
      {
        type: "",
        area: "",
        name: "",
        model: "",
        number: 0,
        position: "",
        borrowing: 0,
        borrowed: 0,
        checking: 0
      }
    ]
  })
});

const borrowInfo = ref(props.borrowInfo);

const maxNumber = (item: MaterialItem) => {
  return (
    item.number -
    (item.borrowed ? item.borrowed : 0) -
    (item.checking ? item.checking : 0)
  );
};

const borrowAdd = (item: MaterialItem) => {
  if (item.borrowing) {
    item.borrowing += 1;
  } else {
    item.borrowing = 0;
    item.borrowing += 1;
  }
};

const btnInputShow = (item: MaterialItem) =>
  item.borrowing !== undefined && !(item.borrowing <= 0);

const search = ref("");

const itemSearch = (item: MaterialItem) => {
  if (search.value === "") {
    return true;
  } else {
    return item.name.includes(search.value);
  }
};

onMounted(() => {
  borrowInfo.value.username = useUserStoreHook()?.username;
  borrowInfo.value.uuid = useUserStoreHook()?.uuid;
  borrowInfo.value.depart = useUserStoreHook()?.depart;
});

const verifyForm = ref();
const openVerifyDialog = () => {
  addDialog({
    title: "信息更改",
    width: "30%",
    props: {
      userInfo: {
        account: "",
        password: "",
        name: "",
        phone: "",
        depart: ""
      }
    },
    contentRenderer: () => h(verifyDialog, { ref: verifyForm }),
    beforeSure(done, { options }) {
      const accountFormRef = verifyForm.value.getAccountRef();
      const infoFormRef = verifyForm.value.getInfoRef();
      const curData = options.props.userInfo as userInfo;
      if (curData.account !== "" || curData.password !== "") {
        accountFormRef.validate(valid => {
          if (valid) {
            auth({
              username: curData.account,
              password: curData.password
            }).then(res => {
              borrowInfo.value.username = res.data.username;
              borrowInfo.value.depart = res.data.depart;
              borrowInfo.value.phone = res.data.phone;
              borrowInfo.value.uuid = res.data.uuid;
            });
            done();
          }
        });
      } else {
        infoFormRef.validate(valid => {
          if (valid) {
            borrowInfo.value.username = curData.name;
            borrowInfo.value.depart = curData.depart;
            borrowInfo.value.phone = curData.phone;
            done();
          }
        });
      }
    }
  });
};
</script>

<template>
  <div>
    <el-steps :active="store.active" align-center>
      <el-step title="物资选择" />
      <el-step title="确认信息" />
    </el-steps>
    <el-tabs ref="formRef" v-model="store.active" class="myTabs">
      <el-tab-pane :name="0" style="text-align: center">
        <el-space direction="vertical" fill style="width: 100%">
          <el-input
            v-model="search"
            size="large"
            style="width: 80%"
            placeholder="请输入搜索内容"
            :prefix-icon="useRenderIcon(Search)"
          />
          <el-card style="width: 80%" shadow="never">
            <el-scrollbar height="400" noresize>
              <TransitionGroup name="list" tag="ul">
                <li
                  v-for="(item, index) in borrowInfo.baseData"
                  v-show="itemSearch(item)"
                  :key="index"
                  class="resultItem"
                >
                  <el-row>
                    <el-col :span="20" style="text-align: left">{{
                      item.name
                    }}</el-col>
                    <el-col
                      :span="4"
                      style="text-align: right; padding-right: 8px"
                    >
                      <el-button
                        v-show="btnInputShow(item)"
                        :icon="useRenderIcon(Subtract)"
                        type="primary"
                        circle
                        plain
                        @click="item.borrowing -= 1"
                      />
                      <el-input-number
                        v-show="btnInputShow(item)"
                        v-model="item.borrowing"
                        :min="0"
                        :max="maxNumber(item)"
                        :controls="false"
                        style="width: 60px"
                      />
                      <el-button
                        :disabled="item.borrowing >= maxNumber(item)"
                        :icon="useRenderIcon(Add)"
                        type="primary"
                        circle
                        plain
                        @click="borrowAdd(item)"
                      />
                    </el-col>
                  </el-row>
                </li>
              </TransitionGroup>
            </el-scrollbar>
          </el-card>
        </el-space>
      </el-tab-pane>
      <el-tab-pane :name="1" style="text-align: center">
        <el-space direction="vertical" fill style="width: 100%">
          <el-card
            class="card"
            header="借用物资确认"
            style="width: 80%"
            shadow="never"
          >
            <el-scrollbar height="250" noresize>
              <p
                v-for="(item, index) in borrowInfo.baseData"
                v-show="item.borrowing > 0"
                :key="index"
                class="resultItem"
              >
                <el-row>
                  <el-col :span="20" style="text-align: left">{{
                    item.name
                  }}</el-col>
                  <el-col
                    :span="4"
                    style="text-align: right; padding-right: 8px"
                  >
                    <el-button
                      v-show="btnInputShow(item)"
                      :icon="useRenderIcon(Subtract)"
                      type="primary"
                      circle
                      plain
                      @click="item.borrowing -= 1"
                    />
                    <el-input-number
                      v-show="btnInputShow(item)"
                      v-model="item.borrowing"
                      :min="0"
                      :max="maxNumber(item)"
                      :controls="false"
                      style="width: 60px"
                    />
                    <el-button
                      :disabled="item.borrowing >= maxNumber(item)"
                      :icon="useRenderIcon(Add)"
                      type="primary"
                      circle
                      plain
                      @click="borrowAdd(item)"
                    />
                  </el-col>
                </el-row>
              </p>
            </el-scrollbar>
          </el-card>
          <el-input
            v-model="borrowInfo.reason"
            :rows="2"
            maxlength="200"
            show-word-limit
            type="textarea"
            placeholder="请填写借用理由"
          />
          <el-card class="card" header="借用人信息" shadow="never">
            <el-row>
              <el-col :span="8">
                <p>姓名：{{ borrowInfo.username }}</p>
              </el-col>
              <el-col :span="8">
                <p>部门：{{ borrowInfo.depart }}</p>
              </el-col>
              <el-col :span="8">
                <el-button @click="openVerifyDialog">更换</el-button>
              </el-col>
            </el-row>
          </el-card>
        </el-space>
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
  .el-tabs__content {
    padding-bottom: 4px;
  }
}

.resultItem {
  margin: 0;
  padding: 2px;
  font-size: 20px;
  border-radius: 4px;
  cursor: pointer;
  &:hover {
    background-color: rgba(91, 94, 103, 0.45);
  }
}

:deep(.card) {
  .el-card__header {
    padding: 10px 8px;
  }
}

.list-move, /* 对移动中的元素应用的过渡 */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* 确保将离开的元素从布局流中删除
  以便能够正确地计算移动的动画。 */
.list-leave-active {
  position: absolute;
}
</style>
