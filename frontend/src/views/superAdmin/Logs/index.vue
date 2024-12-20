<script lang="ts" setup>
import { ref } from "vue";
import { useRole } from "./hook";
import { getPickerShortcuts } from "./utils";
import { PureTableBar } from "@/components/RePureTableBar";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";

import Delete from "@iconify-icons/ep/delete";
import Refresh from "@iconify-icons/ep/refresh";

defineOptions({
  name: "LoginLog"
});

const formRef = ref();
const tableRef = ref();

const {
  form,
  loading,
  columns,
  dataList,
  pagination,
  onSearch,
  clearAll,
  resetForm,
  handleSizeChange,
  handleCurrentChange,
  handleSelectionChange
} = useRole(tableRef);
</script>

<template>
  <div class="main">
    <el-form
      ref="formRef"
      :inline="true"
      :model="form"
      class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px] overflow-auto"
    >
      <el-form-item label="用户名" prop="username">
        <el-input
          v-model="form.username"
          class="!w-[150px]"
          clearable
          placeholder="请输入用户名"
        />
      </el-form-item>
      <el-form-item label="登录状态" prop="status">
        <el-select
          v-model="form.status"
          class="!w-[150px]"
          clearable
          placeholder="请选择"
        >
          <el-option label="成功" value="1" />
          <el-option label="失败" value="0" />
        </el-select>
      </el-form-item>
      <el-form-item label="登录时间" prop="loginTime">
        <el-date-picker
          v-model="form.loginTime"
          :shortcuts="getPickerShortcuts()"
          end-placeholder="结束日期时间"
          range-separator="至"
          start-placeholder="开始日期时间"
          type="datetimerange"
        />
      </el-form-item>
      <el-form-item>
        <el-button
          :icon="useRenderIcon('ri:search-line')"
          :loading="loading"
          type="primary"
          @click="onSearch"
        >
          搜索
        </el-button>
        <el-button :icon="useRenderIcon(Refresh)" @click="resetForm(formRef)">
          重置
        </el-button>
      </el-form-item>
    </el-form>

    <PureTableBar :columns="columns" title="登录日志" @refresh="onSearch">
      <template #buttons>
        <el-popconfirm title="确定要删除所有日志数据吗？" @confirm="clearAll">
          <template #reference>
            <el-button :icon="useRenderIcon(Delete)" type="danger">
              清空日志
            </el-button>
          </template>
        </el-popconfirm>
      </template>
      <template v-slot="{ size, dynamicColumns }">
        <pure-table
          ref="tableRef"
          :adaptiveConfig="{ offsetBottom: 108 }"
          :columns="dynamicColumns"
          :data="dataList"
          :header-cell-style="{
            background: 'var(--el-fill-color-light)',
            color: 'var(--el-text-color-primary)'
          }"
          :loading="loading"
          :pagination="{ ...pagination, size }"
          :size="size"
          adaptive
          align-whole="center"
          row-key="id"
          table-layout="auto"
          @selection-change="handleSelectionChange"
          @page-size-change="handleSizeChange"
          @page-current-change="handleCurrentChange"
        />
      </template>
    </PureTableBar>
  </div>
</template>

<style lang="scss" scoped>
:deep(.el-dropdown-menu__item i) {
  margin: 0;
}

.main-content {
  margin: 24px 24px 0 !important;
}

.search-form {
  :deep(.el-form-item) {
    margin-bottom: 12px;
  }
}
</style>
