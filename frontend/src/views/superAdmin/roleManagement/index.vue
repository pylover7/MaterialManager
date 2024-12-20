<script lang="ts" setup>
import { useRole } from "./utils/hook";
import { computed, nextTick, onMounted, ref } from "vue";
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
import Menu from "@iconify-icons/ep/menu";
import AddFill from "@iconify-icons/ri/add-circle-line";
import Close from "@iconify-icons/ep/close";
import Check from "@iconify-icons/ep/check";
import PureTable from "@pureadmin/table";
import Segmented from "@/components/ReSegmented";
import Search from "@iconify-icons/ri/search-line";

defineOptions({
  name: "roleManagement"
});

const iconClass = computed(() => {
  return [
    "w-[22px]",
    "h-[22px]",
    "flex",
    "justify-center",
    "items-center",
    "outline-none",
    "rounded-[4px]",
    "cursor-pointer",
    "transition-colors",
    "hover:bg-[#0000000f]",
    "dark:hover:bg-[#ffffff1f]",
    "dark:hover:text-[#ffffffd9]"
  ];
});

const menuTreeRef = ref();
const apiTreeRef = ref();
const areaTreeRef = ref();
const formRef = ref();
const tableRef = ref();
const contentRef = ref();
const treeHeight = ref();

const {
  form,
  isShow,
  curRow,
  loading,
  columns,
  rowStyle,
  dataList,
  menuTreeData,
  apiTreeData,
  areaTreeData,
  menuTreeProps,
  apiTreeProps,
  areaProps,
  tabIndex,
  isLinkage,
  apiIsLinkage,
  pagination,
  isExpandAll,
  apiIsExpandAll,
  isSelectAll,
  apiIsSelectAll,
  areaIsSelectAll,
  tabOperation,
  treeSearchValue,
  // buttonClass,
  onSearch,
  resetForm,
  openDialog,
  handleMenu,
  handleSave,
  handleDelete,
  filterMethod,
  transformI18n,
  onQueryChanged,
  // handleDatabase,
  handleSizeChange,
  handleCurrentChange,
  handleSelectionChange
} = useRole(menuTreeRef, apiTreeRef, areaTreeRef);

onMounted(() => {
  useResizeObserver(contentRef, async () => {
    await nextTick();
    delay(60).then(() => {
      treeHeight.value =
        parseFloat(
          subBefore(
            tableRef.value.getTableDoms().tableWrapper.style.height,
            "px"
          )
        ) - 28; // 这个 28 是自己加的，因为加了个tab切换面板
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
      <el-form-item label="角色名称：" prop="name">
        <el-input
          v-model="form.name"
          class="!w-[180px]"
          clearable
          placeholder="请输入角色名称"
        />
      </el-form-item>
      <el-form-item label="角色标识：" prop="code">
        <el-input
          v-model="form.code"
          class="!w-[180px]"
          clearable
          placeholder="请输入角色标识"
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
        title="角色管理"
        @refresh="onSearch"
      >
        <template #buttons>
          <el-button
            :icon="useRenderIcon(AddFill)"
            type="primary"
            @click="openDialog()"
          >
            新增角色
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
                :title="`是否确认删除角色名称为${row.name}的这条数据`"
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
              <el-button
                :icon="useRenderIcon(Menu)"
                :size="size"
                class="reset-margin"
                link
                type="primary"
                @click="handleMenu(row)"
              >
                权限
              </el-button>
            </template>
          </pure-table>
        </template>
      </PureTableBar>

      <div
        v-if="isShow"
        class="!min-w-[calc(100vw-60vw-268px)] mt-2 px-2 pb-2 bg-bg_color ml-2 overflow-auto"
      >
        <div class="flex justify-between w-full px-3 pt-5 pb-4">
          <div class="flex">
            <span :class="iconClass">
              <IconifyIconOffline
                v-tippy="{
                  content: '关闭'
                }"
                :icon="Close"
                class="dark:text-white"
                height="18px"
                width="18px"
                @click="handleMenu"
              />
            </span>
            <span :class="[iconClass, 'ml-2']">
              <IconifyIconOffline
                v-tippy="{
                  content: '保存菜单权限'
                }"
                :icon="Check"
                class="dark:text-white"
                height="18px"
                width="18px"
                @click="handleSave"
              />
            </span>
          </div>
          <p class="font-bold truncate">
            菜单权限
            {{ `${curRow?.name ? `（${curRow.name}）` : ""}` }}
          </p>
        </div>
        <el-input
          v-model="treeSearchValue"
          class="mb-1"
          clearable
          placeholder="筛选"
          @input="onQueryChanged"
        />
        <Segmented v-model="tabIndex" :options="tabOperation" size="small" />
        <el-tabs v-model="tabIndex" class="myTabs" type="card">
          <el-tab-pane :name="tabOperation[0].value">
            <div class="flex flex-wrap">
              <el-checkbox v-model="isExpandAll" label="展开/折叠" />
              <el-checkbox v-model="isSelectAll" label="全选/全不选" />
            </div>
            <el-tree-v2
              ref="menuTreeRef"
              :check-strictly="isLinkage"
              :data="menuTreeData"
              :filter-method="filterMethod"
              :height="treeHeight"
              :props="menuTreeProps"
              show-checkbox
            >
              <template #default="{ node }">
                <span>{{ transformI18n(node.label) }}</span>
              </template>
            </el-tree-v2>
          </el-tab-pane>
          <el-tab-pane :name="tabOperation[1].value">
            <div class="flex flex-wrap">
              <el-checkbox v-model="apiIsExpandAll" label="展开/折叠" />
              <el-checkbox v-model="apiIsSelectAll" label="全选/全不选" />
            </div>
            <el-tree-v2
              ref="apiTreeRef"
              :check-strictly="!apiIsLinkage"
              :data="apiTreeData"
              :filter-method="filterMethod"
              :height="treeHeight"
              :props="apiTreeProps"
              show-checkbox
            >
              <template #default="{ node }">
                <span>{{ transformI18n(node.label) }}</span>
              </template>
            </el-tree-v2>
          </el-tab-pane>
          <el-tab-pane :name="tabOperation[2].value">
            <div class="flex flex-wrap">
              <el-checkbox v-model="areaIsSelectAll" label="全选/全不选" />
            </div>
            <el-tree-v2
              ref="areaTreeRef"
              :data="areaTreeData"
              :filter-method="filterMethod"
              :height="treeHeight"
              :props="areaProps"
              show-checkbox
            >
              <template #default="{ node }">
                <span>{{ transformI18n(node.label) }}</span>
              </template>
            </el-tree-v2>
          </el-tab-pane>
        </el-tabs>
      </div>
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
