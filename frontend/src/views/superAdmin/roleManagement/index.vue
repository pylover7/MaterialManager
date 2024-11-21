<script setup lang="ts">
import { useRole } from "./utils/hook";
import { ref, computed, nextTick, onMounted } from "vue";
import { PureTableBar } from "@/components/RePureTableBar";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import {
  delay,
  subBefore,
  deviceDetection,
  useResizeObserver
} from "@pureadmin/utils";

// import Database from "@iconify-icons/ri/database-2-line";
// import More from "@iconify-icons/ep/more-filled";
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
  menuTreeProps,
  apiTreeProps,
  tabIndex,
  isLinkage,
  apiIsLinkage,
  pagination,
  isExpandAll,
  apiIsExpandAll,
  isSelectAll,
  apiIsSelectAll,
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
} = useRole(menuTreeRef, apiTreeRef);

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
          placeholder="请输入角色名称"
          clearable
          class="!w-[180px]"
        />
      </el-form-item>
      <el-form-item label="角色标识：" prop="code">
        <el-input
          v-model="form.code"
          placeholder="请输入角色标识"
          clearable
          class="!w-[180px]"
        />
      </el-form-item>
      <el-form-item label="状态：" prop="status">
        <el-select
          v-model="form.status"
          placeholder="请选择状态"
          clearable
          class="!w-[180px]"
        >
          <el-option label="已启用" :value="1" />
          <el-option label="已停用" :value="0" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          :icon="useRenderIcon(Search)"
          :loading="loading"
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
        style="transition: width 220ms cubic-bezier(0.4, 0, 0.2, 1)"
        title="角色管理"
        :columns="columns"
        @refresh="onSearch"
      >
        <template #buttons>
          <el-button
            type="primary"
            :icon="useRenderIcon(AddFill)"
            @click="openDialog()"
          >
            新增角色
          </el-button>
        </template>
        <template v-slot="{ size, dynamicColumns }">
          <pure-table
            ref="tableRef"
            align-whole="center"
            showOverflowTooltip
            table-layout="auto"
            :loading="loading"
            :size="size"
            adaptive
            :row-style="rowStyle"
            :adaptiveConfig="{ offsetBottom: 108 }"
            :data="dataList"
            :columns="dynamicColumns"
            :pagination="pagination"
            :paginationSmall="size === 'small'"
            :header-cell-style="{
              background: 'var(--el-fill-color-light)',
              color: 'var(--el-text-color-primary)'
            }"
            @selection-change="handleSelectionChange"
            @page-size-change="handleSizeChange"
            @page-current-change="handleCurrentChange"
          >
            <template #operation="{ row }">
              <el-button
                class="reset-margin"
                link
                type="primary"
                :size="size"
                :icon="useRenderIcon(EditPen)"
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
                    class="reset-margin"
                    link
                    type="primary"
                    :size="size"
                    :icon="useRenderIcon(Delete)"
                  >
                    删除
                  </el-button>
                </template>
              </el-popconfirm>
              <el-button
                class="reset-margin"
                link
                type="primary"
                :size="size"
                :icon="useRenderIcon(Menu)"
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
                class="dark:text-white"
                width="18px"
                height="18px"
                :icon="Close"
                @click="handleMenu"
              />
            </span>
            <span :class="[iconClass, 'ml-2']">
              <IconifyIconOffline
                v-tippy="{
                  content: '保存菜单权限'
                }"
                class="dark:text-white"
                width="18px"
                height="18px"
                :icon="Check"
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
          placeholder="筛选"
          class="mb-1"
          clearable
          @input="onQueryChanged"
        />
        <Segmented v-model="tabIndex" :options="tabOperation" size="small" />
        <el-tabs v-model="tabIndex" type="card" class="myTabs">
          <el-tab-pane :name="tabOperation[0].value">
            <div class="flex flex-wrap">
              <el-checkbox v-model="isExpandAll" label="展开/折叠" />
              <el-checkbox v-model="isSelectAll" label="全选/全不选" />
            </div>
            <el-tree-v2
              ref="menuTreeRef"
              show-checkbox
              :height="treeHeight"
              :data="menuTreeData"
              :props="menuTreeProps"
              :check-strictly="!isLinkage"
              :filter-method="filterMethod"
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
              show-checkbox
              :height="treeHeight"
              :data="apiTreeData"
              :props="apiTreeProps"
              :check-strictly="!apiIsLinkage"
              :filter-method="filterMethod"
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

<style scoped lang="scss">
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
    border: 0;
    height: 0;
    margin: 0;
    .el-tabs__nav {
      border: 0;
      .el-tabs__item {
        border: 0;
        padding: 0;
      }
    }
  }
}
</style>
