<script setup lang="ts">
import { ref } from "vue";
import useDialogStore from "./store";
import Search from "@iconify-icons/ep/search";
import Add from "@iconify-icons/fluent/add-12-filled";
import Subtract from "@iconify-icons/fluent/subtract-12-filled";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { MaterialItem } from "@/types/base";

type materialItemList = {
  borrowInfo: {
    userId: number;
    baseData: [MaterialItem];
  };
};

const formRef = ref();
function getRef() {
  return formRef.value;
}
defineExpose({ getRef });

const store = useDialogStore();

const props = withDefaults(defineProps<materialItemList>(), {
  borrowInfo: () => ({
    userId: 0,
    baseData: [
      {
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

const itemShow = (item: MaterialItem) => {
  if (search.value === "") {
    return true;
  } else {
    return item.name.includes(search.value);
  }
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
              <p
                v-for="(item, index) in borrowInfo.baseData"
                v-show="itemShow(item)"
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
        </el-space>
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
</style>
