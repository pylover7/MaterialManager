<script lang="ts" setup>
import { ref } from "vue";
import { noticesData } from "./data";
import NoticeList from "./noticeList.vue";
import Bell from "@iconify-icons/ep/bell";

const noticesNum = ref(0);
const notices = ref(noticesData);
const activeKey = ref(noticesData[0].key);

notices.value.map(v => (noticesNum.value += v.list.length));
</script>

<template>
  <el-dropdown placement="bottom-end" trigger="click">
    <span class="dropdown-badge navbar-bg-hover select-none">
      <el-badge :max="99" :value="noticesNum">
        <span class="header-notice-icon">
          <IconifyIconOffline :icon="Bell" />
        </span>
      </el-badge>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-tabs
          v-model="activeKey"
          :stretch="true"
          :style="{ width: notices.length === 0 ? '200px' : '330px' }"
          class="dropdown-tabs"
        >
          <el-empty
            v-if="notices.length === 0"
            :image-size="60"
            description="暂无消息"
          />
          <span v-else>
            <template v-for="item in notices" :key="item.key">
              <el-tab-pane
                :label="`${item.name}(${item.list.length})`"
                :name="`${item.key}`"
              >
                <el-scrollbar max-height="330px">
                  <div class="noticeList-container">
                    <NoticeList :list="item.list" />
                  </div>
                </el-scrollbar>
              </el-tab-pane>
            </template>
          </span>
        </el-tabs>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<style lang="scss" scoped>
.dropdown-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 48px;
  margin-right: 10px;
  cursor: pointer;

  .header-notice-icon {
    font-size: 18px;
  }
}

.dropdown-tabs {
  .noticeList-container {
    padding: 15px 24px 0;
  }

  :deep(.el-tabs__header) {
    margin: 0;
  }

  :deep(.el-tabs__nav-wrap)::after {
    height: 1px;
  }

  :deep(.el-tabs__nav-wrap) {
    padding: 0 36px;
  }
}
</style>
