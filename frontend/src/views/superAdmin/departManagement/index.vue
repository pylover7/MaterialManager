<script lang="ts" setup>
import { ref } from "vue";
import { useDept } from "./utils/hook";
import { PureTableBar } from "@/components/RePureTableBar";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";

import Delete from "@iconify-icons/ep/delete";
import EditPen from "@iconify-icons/ep/edit-pen";
import Refresh from "@iconify-icons/ep/refresh";
import AddFill from "@iconify-icons/ri/add-circle-line";
import PureTable from "@pureadmin/table";
import Search from "@iconify-icons/ri/search-line";

defineOptions({
  name: "departManagement"
});

const formRef = ref();
const tableRef = ref();
const {
  form,
  loading,
  columns,
  dataList,
  onSearch,
  resetForm,
  openDialog,
  handleDelete,
  handleSelectionChange
} = useDept();
</script>

<template>
  <div class="main">
    <el-form
      ref="formRef"
      :inline="true"
      :model="form"
      class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px] overflow-auto"
    >
      <el-form-item label="部门名称：" prop="name">
        <el-input
          v-model="form.name"
          class="!w-[180px]"
          clearable
          placeholder="请输入部门名称"
        />
      </el-form-item>
      <el-form-item label="状态：" prop="status">
        <el-select
          v-model="form.status"
          class="!w-[180px]"
          clearable
          placeholder="请选择状态"
        >
          <el-option :value="1" label="启用" />
          <el-option :value="0" label="停用" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button
          :icon="useRenderIcon(Search)"
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

    <PureTableBar
      :columns="columns"
      :tableRef="tableRef?.getTableRef()"
      title="部门管理"
      @refresh="onSearch"
    >
      <template #buttons>
        <el-button
          :icon="useRenderIcon(AddFill)"
          type="primary"
          @click="openDialog()"
        >
          新增部门
        </el-button>
      </template>
      <template v-slot="{ size, dynamicColumns }">
        <pure-table
          ref="tableRef"
          :adaptiveConfig="{ offsetBottom: 45 }"
          :columns="dynamicColumns"
          :data="dataList"
          :default-expand-all="false"
          :default-sort="{ prop: 'sort', order: 'ascending' }"
          :header-cell-style="{
            background: 'var(--el-fill-color-light)',
            color: 'var(--el-text-color-primary)'
          }"
          :loading="loading"
          :size="size"
          adaptive
          align-whole="center"
          row-key="id"
          showOverflowTooltip
          table-layout="auto"
          @selection-change="handleSelectionChange"
        >
          <template #operation="{ row }">
            <el-button
              :icon="useRenderIcon(EditPen)"
              :size="size"
              class="reset-margin"
              link
              type="primary"
              @click="openDialog('修改', row)"
            >
              修改
            </el-button>
            <el-popconfirm
              :title="`是否确认删除部门名称为${row.name}的这条数据`"
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
</template>

<style lang="scss" scoped>
:deep(.el-table__inner-wrapper::before) {
  height: 0;
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
