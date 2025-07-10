<script lang="ts" setup>
import { ref } from "vue";
import { useUser } from "./utils/hook";
import { PureTableBar } from "@/components/RePureTableBar";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";

import Role from "@iconify-icons/ri/admin-line";
import Delete from "@iconify-icons/ep/delete";
import AddFill from "@iconify-icons/ri/add-circle-line";
import PureTable from "@pureadmin/table";

defineOptions({
  name: "UserManagement"
});

const tableRef = ref();

const {
  form,
  roleId,
  loading,
  columns,
  dataList,
  selectedNum,
  pagination,
  roleOptions,
  deviceDetection,
  onSearch,
  onBatchDel,
  openDialog,
  handleDelete,
  handleRole,
  handleSizeChange,
  onSelectionCancel,
  handleCurrentChange,
  handleSelectionChange
} = useUser(tableRef);
</script>

<template>
  <div class="main">
    <el-form
      ref="formRef"
      :inline="true"
      :model="form"
      class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px] overflow-auto"
    >
      <el-form-item label="角色筛选：" prop="name">
        <el-select
          v-model="form.role"
          class="role-select"
          clearable
          placeholder="请选择"
        >
          <el-option
            v-for="(item, index) in roleOptions"
            :key="index"
            :label="item.name"
            :value="item.id"
          >
            {{ item.name }}
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>

    <div :class="['flex', 'justify-between', deviceDetection() && 'flex-wrap']">
      <div :class="[deviceDetection() ? ['w-full', 'mt-2'] : 'w-full mt-2']">
        <PureTableBar :columns="columns" title="用户管理" @refresh="onSearch">
          <template #buttons>
            <el-select
              v-model="roleId"
              class="role-select"
              clearable
              placeholder="请选择"
            >
              <el-option
                v-for="(item, index) in roleOptions"
                :key="index"
                :label="item.name"
                :value="item.id"
              >
                {{ item.name }}
              </el-option>
            </el-select>
            <el-button
              :icon="useRenderIcon(AddFill)"
              type="primary"
              @click="openDialog()"
            >
              新增用户
            </el-button>
          </template>
          <template v-slot="{ size, dynamicColumns }">
            <div
              v-if="selectedNum > 0"
              v-motion-fade
              class="bg-[var(--el-fill-color-light)] w-full h-[46px] mb-2 pl-4 flex items-center"
            >
              <div class="flex-auto">
                <span
                  class="text-[rgba(42,46,54,0.5)] dark:text-[rgba(220,220,242,0.5)]"
                  style="font-size: var(--el-font-size-base)"
                >
                  已选 {{ selectedNum }} 项
                </span>
                <el-button text type="primary" @click="onSelectionCancel">
                  取消选择
                </el-button>
              </div>
              <el-popconfirm title="是否确认删除?" @confirm="onBatchDel">
                <template #reference>
                  <el-button class="mr-1" text type="danger">
                    批量删除
                  </el-button>
                </template>
              </el-popconfirm>
            </div>
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
              :pagination="pagination"
              :paginationSmall="size === 'small'"
              :size="size"
              adaptive
              align-whole="center"
              row-key="id"
              table-layout="auto"
              @selection-change="handleSelectionChange"
              @page-size-change="handleSizeChange"
              @page-current-change="handleCurrentChange"
            >
              <template #operation="{ row }">
                <el-button
                  :icon="useRenderIcon(Role)"
                  :size="size"
                  class="reset-margin"
                  link
                  type="primary"
                  @click="handleRole(row)"
                >
                  分配角色
                </el-button>
                <el-popconfirm
                  :title="`是否确认删除用户【${row.nickname}】`"
                  @confirm="handleDelete(row)"
                >
                  <template #reference>
                    <el-button
                      :icon="useRenderIcon(Delete)"
                      :size="size"
                      class="reset-margin"
                      link
                      type="primary"
                    >
                      删除
                    </el-button>
                  </template>
                </el-popconfirm>
              </template>
            </pure-table>
          </template>
        </PureTableBar>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
:deep(.el-dropdown-menu__item i) {
  margin: 0;
}

:deep(.el-button:focus-visible) {
  outline: none;
}

.main-content {
  margin: 24px 24px 0 !important;
}

.search-form {
  :deep(.el-form-item) {
    margin-bottom: 12px;
  }
}

.role-select {
  width: 120px;
  margin-right: 12px;
}
</style>
