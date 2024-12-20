<script lang="ts" setup>
import { computed, onMounted, ref } from "vue";
import Segmented, { OptionsType } from "@/components/ReSegmented";
import Borrowing from "./panels/borrowing.vue";
import Returning from "./panels/returning.vue";
import Returned from "./panels/returned.vue";
import { useUserStoreHook } from "@/store/modules/user";
import { getAreaList } from "@/api/base";

defineOptions({
  name: "Approval"
});

const tabIndex = ref(0);
const areaOpt = ref([]);
const userId = computed(() => {
  return useUserStoreHook()?.uuid;
});
const segmentedOptions: Array<OptionsType> = [
  {
    label: "借出待审批",
    value: 0
  },
  {
    label: "归还待审批",
    value: 1
  },
  {
    label: "借用记录",
    value: 2
  }
];
onMounted(() => {
  getAreaList().then(res => {
    areaOpt.value = res.data.map(item => {
      return {
        label: item.name,
        value: item.id
      };
    });
  });
});
</script>

<template>
  <div class="main">
    <Segmented v-model="tabIndex" :options="segmentedOptions" size="large" />
    <el-tabs v-model="tabIndex" class="myTabs" type="card">
      <Transition>
        <Borrowing
          v-show="segmentedOptions[0].value == tabIndex"
          :areaOpt="areaOpt"
          :segmentedOptions="segmentedOptions"
          :userId="userId"
        />
      </Transition>
      <Transition>
        <Returning
          v-show="segmentedOptions[1].value == tabIndex"
          :areaOpt="areaOpt"
          :segmentedOptions="segmentedOptions"
          :userId="userId"
        />
      </Transition>
      <Transition>
        <Returned
          v-show="segmentedOptions[2].value == tabIndex"
          :areaOpt="areaOpt"
          :segmentedOptions="segmentedOptions"
          :userId="userId"
        />
      </Transition>
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

.main-content {
  margin: 24px 24px 0 !important;
}

.v-enter-active,
.v-leave-active {
  transition: opacity 1s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
