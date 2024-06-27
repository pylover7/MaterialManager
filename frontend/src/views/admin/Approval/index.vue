<script setup lang="ts">
import { computed, ref } from "vue";
import Segmented, { OptionsType } from "@/components/ReSegmented";
import Borrowing from "./panels/borrowing.vue";
import Returning from "./panels/returning.vue";
import Returned from "./panels/returned.vue";
import { useUserStoreHook } from "@/store/modules/user";

defineOptions({
  name: "Approval"
});

const tabIndex = ref(0);
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
</script>

<template>
  <div class="main">
    <Segmented v-model="tabIndex" :options="segmentedOptions" size="large" />
    <el-tabs v-model="tabIndex" type="card" class="myTabs">
      <Transition>
        <Borrowing
          v-show="segmentedOptions[0].value == tabIndex"
          :segmentedOptions="segmentedOptions"
          :userId="userId"
        />
      </Transition>
      <Transition>
        <Returning
          v-show="segmentedOptions[1].value == tabIndex"
          :segmentedOptions="segmentedOptions"
          :userId="userId"
        />
      </Transition>
      <Transition>
        <Returned
          v-show="segmentedOptions[2].value == tabIndex"
          :segmentedOptions="segmentedOptions"
          :userId="userId"
        />
      </Transition>
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
