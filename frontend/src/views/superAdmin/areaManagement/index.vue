<script lang="ts" setup>
import { useRole } from "./utils/hook";
import { nextTick, onMounted, ref } from "vue";
import { PureTableBar } from "@/components/RePureTableBar";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import {
  delay,
  deviceDetection,
  subBefore,
  useResizeObserver
} from "@pureadmin/utils";

import Delete from "@iconify-icons/ep/delete";
import EditPen from "@iconify-icons/ep/edit-pen";
import Refresh from "@iconify-icons/ep/refresh";
import AddFill from "@iconify-icons/ri/add-circle-line";
import PureTable from "@pureadmin/table";
import Search from "@iconify-icons/ri/search-line";

defineOptions({
  name: "AreaManagement"
});

const formRef = ref();
const tableRef = ref();
const contentRef = ref();
const treeHeight = ref();

const {
  form,
  isShow,
  loading,
  columns,
  rowStyle,
  dataList,
  pagination,
  onSearch,
  resetForm,
  openDialog,
  handleDelete,
  handleSizeChange,
  handleCurrentChange,
  handleSelectionChange
} = useRole();

onMounted(() => {
  useResizeObserver(contentRef, async () => {
    await nextTick();
    delay(60).then(() => {
      treeHeight.value = parseFloat(
        subBefore(tableRef.value.getTableDoms().tableWrapper.style.height, "px")
      );
    });
  });
});
</script>

<template>
  <div class="main">
    <el-form
      ref="formRef"
      :inline="true"
      :model="form"
      class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px] overflow-auto"
    >
      <el-form-item label="区域名称：" prop="name">
        <el-input
          v-model="form.name"
          class="!w-[180px]"
          clearable
          placeholder="请输入区域名称"
        />
      </el-form-item>
      <el-form-item label="区域标识：" prop="code">
        <el-input
          v-model="form.code"
          class="!w-[180px]"
          clearable
          placeholder="请输入区域标识"
        />
      </el-form-item>
      <el-form-item label="状态：" prop="status">
        <el-select
          v-model="form.status"
          class="!w-[180px]"
          clearable
          placeholder="请选择状态"
        >
          <el-option :value="1" label="已启用" />
          <el-option :value="0" label="已停用" />
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

    <div
      ref="contentRef"
      :class="['flex', deviceDetection() ? 'flex-wrap' : '']"
    >
      <PureTableBar
        :class="[isShow && !deviceDetection() ? '!w-[60vw]' : 'w-full']"
        :columns="columns"
        style="transition: width 220ms cubic-bezier(0.4, 0, 0.2, 1)"
        title="区域管理"
        @refresh="onSearch"
      >
        <template #buttons>
          <el-button
            :icon="useRenderIcon(AddFill)"
            type="primary"
            @click="openDialog()"
          >
            新增区域
          </el-button>
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
            :pagination="pagination"
            :paginationSmall="size === 'small'"
            :row-style="rowStyle"
            :size="size"
            adaptive
            align-whole="center"
            showOverflowTooltip
            table-layout="auto"
            @selection-change="handleSelectionChange"
            @page-size-change="handleSizeChange"
            @page-current-change="handleCurrentChange"
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
                :title="`是否确认删除区域名称为${row.name}的这条数据`"
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

:deep(.myTabs) {
  .el-tabs__header {
    height: 0;
    margin: 0;
    border: 0;

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
