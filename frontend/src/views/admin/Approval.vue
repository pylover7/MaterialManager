<script setup lang="tsx">
import Segmented, { OptionsType } from "@/components/ReSegmented";
import { computed, reactive, ref } from "vue";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Search from "@iconify-icons/ep/search";
import Approve from "@iconify-icons/fluent/approvals-app-16-filled";
import Reject from "@iconify-icons/fluent/text-change-reject-24-filled";
import { PaginationProps, PureTable } from "@pureadmin/table";
import type { LoadingConfig } from "@pureadmin/table";
import { PureTableBar } from "@/components/RePureTableBar";
import { successNotification } from "@/utils/notification";
import { listBorrowed, updateBorrowedInfo } from "@/api/home";
import { usePublicHooks } from "./utils";
import { useUserStoreHook } from "@/store/modules/user";
import { getKeyList } from "@pureadmin/utils";
import { message } from "@/utils/message";

defineOptions({
  name: "Approval"
});

const userId = computed(() => {
  return useUserStoreHook()?.uuid;
});
const tabIndex = ref(0);
const segmentedOptions: Array<OptionsType> = [
  {
    label: "借出待审批",
    value: 0
  },
  {
    label: "归还待审批",
    value: 1
  }
];

const borrowedOptBar = reactive({
  area: ""
});
const loading = ref(false);

const onSearch = () => {
  listBorrowed(
    borrowedOptBar.area,
    pagination.currentPage,
    pagination.pageSize,
    false
  ).then(res => {
    dataList.value = res.data;
    pagination.total = res.total;
  });
};

/** 标签风格 */
const { tagStyle } = usePublicHooks();

const columns: TableColumnList = [
  {
    label: "勾选列", // 如果需要表格多选，此处label必须设置
    type: "selection",
    fixed: "left",
    reserveSelection: true // 数据刷新后保留选项
  },
  {
    label: "序号",
    type: "index",
    width: 60
  },
  {
    label: "借用物资信息",
    prop: "material",
    cellRenderer: ({ row }) => (
      <el-popover
        placement="right"
        width="200"
        trigger="click"
        v-slots={{
          reference: () => <el-button link>{row.material[0].name}</el-button>,
          default: () => (
            <ul>
              <li>名称：{row.material[0].name}</li>
              <li>型号：{row.material[0].model}</li>
              <li>位置：{row.material[0].position}</li>
            </ul>
          )
        }}
      ></el-popover>
    )
  },
  {
    label: "借用人信息",
    prop: "username",
    cellRenderer: ({ row }) => (
      <el-popover
        placement="right"
        width="200"
        trigger="click"
        v-slots={{
          reference: () => <el-button link>{row.username}</el-button>,
          default: () => (
            <ul>
              <li>姓名：{row.username}</li>
              <li>电话：{row.phone}</li>
              <li>部门：{row.userDepart}</li>
            </ul>
          )
        }}
      ></el-popover>
    )
  },
  {
    label: "借用人电话",
    prop: "phone"
  },
  {
    label: "借用数量",
    prop: "borrowing"
  },
  {
    label: "借用时间",
    prop: "borrowTime"
  },
  {
    label: "审批状态",
    prop: "borrowApproveStatus",
    cellRenderer: ({ row, props }) => (
      <el-tag
        size={props.size}
        style={tagStyle.value(row.borrowApproveStatus ? 1 : 0)}
      >
        {row.borrowApproveStatus ? "已审批" : "待审批"}
      </el-tag>
    )
  },
  {
    label: "操作",
    cellRenderer: ({ row }) => (
      <>
        <el-button
          plain
          type="primary"
          onClick={() => {
            updateBorrowedInfo([row.id], userId.value, true, true).then(() => {
              message("已批准请求", { type: "success" });
              onSearch();
            });
          }}
        >
          批准
        </el-button>
        <el-button
          plain
          type="warning"
          onClick={() => {
            updateBorrowedInfo([row.id], userId.value, true, false).then(() => {
              message("已驳回请求", { type: "info" });
              onSearch();
            });
          }}
        >
          驳回
        </el-button>
      </>
    )
  }
];
const selectedNum = ref(0);
// 表格ref
const tableRef = ref();

/** 取消选择 */
function onSelectionCancel() {
  selectedNum.value = 0;
  // 用于多选表格，清空用户的选择
  tableRef.value.getTableRef().clearSelection();
}

/** 批量批准或驳回 */
function onBatch(whether: boolean) {
  const curSelected = tableRef.value.getTableRef().getSelectionRows();
  updateBorrowedInfo(
    getKeyList(curSelected, "id"),
    userId.value,
    true,
    whether
  ).then(() => {
    onSearch();
    tableRef.value.getTableRef().clearSelection();
    successNotification(`已批${whether ? "通过" : "驳回"}所选请求`);
  });
}

// 表格数据
const dataList = ref([]);

// 分页设置
const pagination = reactive<PaginationProps>({
  total: 0,
  pageSize: 10,
  currentPage: 1,
  background: true,
  pageSizes: [10, 20, 30, 50]
});

/** 当CheckBox选择项发生变化时会触发该事件 */
function handleSelectionChange(val) {
  selectedNum.value = val.length;
  // 重置表格高度
  tableRef.value.setAdaptive();
}

/** 加载动画配置 */
const loadingConfig = reactive<LoadingConfig>({
  text: "正在加载第一页...",
  viewBox: "-10, -10, 50, 50",
  spinner: `
        <path class="path" d="
          M 30 15
          L 28 17
          M 25.61 25.61
          A 15 15, 0, 0, 1, 15 30
          A 15 15, 0, 1, 1, 27.99 7.5
          L 15 15
        " style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"/>
      `
  // svg: "",
  // background: rgba()
});

function handleSizeChange(val: number) {
  console.log(`${val} items per page`);
}

function handleCurrentChange(val: number) {
  console.log(`current page: ${val}`);
}

const returnOptBarRef = ref();
const returnTableRef = ref();
const returnedOptBar = reactive({
  area: ""
});

const onSearchReturn = () => {
  listBorrowed(
    returnedOptBar.area,
    pagination2.currentPage,
    pagination2.pageSize,
    true,
    true,
    false
  ).then(res => {
    returnDataList.value = res.data;
    pagination2.total = res.total;
  });
};

const returnFormColumns: TableColumnList = [
  {
    label: "勾选列", // 如果需要表格多选，此处label必须设置
    type: "selection",
    fixed: "left",
    reserveSelection: true // 数据刷新后保留选项
  },
  {
    label: "序号",
    type: "index",
    width: 60
  },
  {
    label: "借用物资信息",
    prop: "material",
    cellRenderer: ({ row }) => (
      <el-popover
        placement="right"
        width="200"
        trigger="click"
        v-slots={{
          reference: () => <el-button link>{row.material[0].name}</el-button>,
          default: () => (
            <ul>
              <li>名称：{row.material[0].name}</li>
              <li>型号：{row.material[0].model}</li>
              <li>位置：{row.material[0].position}</li>
            </ul>
          )
        }}
      ></el-popover>
    )
  },
  {
    label: "借用人信息",
    prop: "username",
    cellRenderer: ({ row }) => (
      <el-popover
        placement="right"
        width="200"
        trigger="click"
        v-slots={{
          reference: () => <el-button link>{row.username}</el-button>,
          default: () => (
            <ul>
              <li>姓名：{row.username}</li>
              <li>电话：{row.phone}</li>
              <li>部门：{row.userDepart}</li>
            </ul>
          )
        }}
      ></el-popover>
    )
  },
  {
    label: "借用人电话",
    prop: "phone"
  },
  {
    label: "借用数量",
    prop: "borrowing"
  },
  {
    label: "借用时间",
    prop: "borrowTime"
  },
  {
    label: "归还状态",
    prop: "returnApproveStatus",
    cellRenderer: ({ row, props }) => (
      <el-tag
        size={props.size}
        style={tagStyle.value(row.returnApproveStatus ? 1 : 0)}
      >
        {row.returnApproveStatus ? "已归还" : "未归还"}
      </el-tag>
    )
  },
  {
    label: "操作",
    cellRenderer: ({ row }) => (
      <el-button
        plain
        type="primary"
        onClick={() => {
          updateBorrowedInfo([row.id], userId.value, false, false, true).then(
            () => {
              message("已批准请求", { type: "success" });
              onSearchReturn();
            }
          );
        }}
      >
        批准
      </el-button>
    )
  }
];

const returnSelectedNum = ref(0);
const returnLoading = ref(false);
const returnDataList = ref([]);
// 分页设置
const pagination2 = reactive<PaginationProps>({
  total: 0,
  pageSize: 10,
  currentPage: 1,
  background: true,
  pageSizes: [10, 20, 30, 50]
});
const onBatchReturn = () => {
  const curSelected = returnTableRef.value.getTableRef().getSelectionRows();
  updateBorrowedInfo(
    getKeyList(curSelected, "id"),
    userId.value,
    false,
    true,
    true
  ).then(() => {
    onSearchReturn();
    returnTableRef.value.getTableRef().clearSelection();
    successNotification("已批通过选请求");
  });
};
/** 当CheckBox选择项发生变化时会触发该事件 */
function returnHandleSelectionChange(val) {
  returnSelectedNum.value = val.length;
  // 重置表格高度
  returnTableRef.value.setAdaptive();
}
</script>

<template>
  <div class="main">
    <Segmented v-model="tabIndex" :options="segmentedOptions" size="large" />
    <el-tabs v-model="tabIndex" type="card" class="myTabs">
      <el-tab-pane :name="segmentedOptions[0].value" :lazy="true">
        <el-form
          ref="borrowedOptBarRef"
          :inline="true"
          :model="borrowedOptBar"
          class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px] overflow-auto"
        >
          <el-form-item label="选择区域" prop="area">
            <el-select
              v-model="borrowedOptBar.area"
              placeholder="请选择区域"
              class="!w-[150px]"
            >
              <el-option label="隔离办" value="glb" />
              <el-option label="辅控" value="fk" />
              <el-option label="网控" value="wk" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              :icon="useRenderIcon(Search)"
              :loading="loading"
              :disabled="borrowedOptBar.area === ''"
              @click="onSearch"
            >
              搜索
            </el-button>
          </el-form-item>
        </el-form>

        <PureTableBar title="借出待审批" :columns="columns" @refresh="onSearch">
          <template #buttons>
            <div class="h-full mb-2 pl-4 flex items-center">
              <div class="flex-auto">
                <span
                  style="font-size: var(--el-font-size-base)"
                  class="text-[rgba(42,46,54,0.5)] dark:text-[rgba(220,220,242,0.5)]"
                >
                  已选 {{ selectedNum }} 项
                </span>
                <el-button type="primary" text @click="onSelectionCancel">
                  取消选择
                </el-button>
              </div>
            </div>

            <el-popconfirm
              title="确定要批准所选请求吗？"
              @confirm="onBatch(true)"
            >
              <template #reference>
                <el-button type="success" :icon="useRenderIcon(Approve)">
                  批量批准
                </el-button>
              </template>
            </el-popconfirm>
            <el-popconfirm
              title="确定要驳回所选请求吗？"
              @confirm="onBatch(false)"
            >
              <template #reference>
                <el-button type="danger" :icon="useRenderIcon(Reject)">
                  批量驳回
                </el-button>
              </template>
            </el-popconfirm>
          </template>
          <template v-slot="{ size, dynamicColumns }">
            <pure-table
              ref="tableRef"
              row-key="id"
              align-whole="center"
              table-layout="auto"
              :loading="loading"
              :size="size"
              adaptive
              :loadingConfig="loadingConfig"
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
            />
          </template>
        </PureTableBar>
      </el-tab-pane>
      <el-tab-pane :name="segmentedOptions[1].value" :lazy="true">
        <el-form
          ref="returnOptBarRef"
          :inline="true"
          :model="returnedOptBar"
          class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px] overflow-auto"
        >
          <el-form-item label="选择区域" prop="area">
            <el-select
              v-model="returnedOptBar.area"
              placeholder="请选择区域"
              class="!w-[150px]"
            >
              <el-option label="隔离办" value="glb" />
              <el-option label="辅控" value="fk" />
              <el-option label="网控" value="wk" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              :icon="useRenderIcon(Search)"
              :loading="loading"
              :disabled="returnedOptBar.area === ''"
              @click="onSearchReturn"
            >
              搜索
            </el-button>
          </el-form-item>
        </el-form>

        <PureTableBar
          title="归还待审批"
          :columns="returnFormColumns"
          @refresh="onSearchReturn"
        >
          <template #buttons>
            <div class="h-full mb-2 pl-4 flex items-center">
              <div class="flex-auto">
                <span
                  style="font-size: var(--el-font-size-base)"
                  class="text-[rgba(42,46,54,0.5)] dark:text-[rgba(220,220,242,0.5)]"
                >
                  已选 {{ returnSelectedNum }} 项
                </span>
                <el-button type="primary" text @click="onSelectionCancel">
                  取消选择
                </el-button>
              </div>
            </div>

            <el-popconfirm
              title="确定要批准所选请求吗？"
              @confirm="onBatchReturn"
            >
              <template #reference>
                <el-button type="success" :icon="useRenderIcon(Approve)">
                  批量批准
                </el-button>
              </template>
            </el-popconfirm>
          </template>
          <template v-slot="{ size, dynamicColumns }">
            <pure-table
              ref="returnTableRef"
              row-key="id"
              align-whole="center"
              table-layout="auto"
              :loading="returnLoading"
              :size="size"
              adaptive
              :loadingConfig="loadingConfig"
              :adaptiveConfig="{ offsetBottom: 108 }"
              :data="returnDataList"
              :columns="dynamicColumns"
              :pagination="pagination2"
              :paginationSmall="size === 'small'"
              :header-cell-style="{
                background: 'var(--el-fill-color-light)',
                color: 'var(--el-text-color-primary)'
              }"
              @selection-change="returnHandleSelectionChange"
              @page-size-change="handleSizeChange"
              @page-current-change="handleCurrentChange"
            />
          </template>
        </PureTableBar>
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
</style>
