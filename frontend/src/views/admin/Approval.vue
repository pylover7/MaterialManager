<script setup lang="tsx">
import Segmented, { OptionsType } from "@/components/ReSegmented";
import { computed, reactive, ref } from "vue";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Search from "@iconify-icons/ep/search";
import Approve from "@iconify-icons/fluent/approvals-app-16-filled";
import { PaginationProps, PureTable } from "@pureadmin/table";
import { PureTableBar } from "@/components/RePureTableBar";
import { successNotification } from "@/utils/notification";
import { listBorrowed, updateBorrowApproveStatus } from "@/api/home";
import { usePublicHooks } from "./utils";
import { useUserStoreHook } from "@/store/modules/user";

defineOptions({
  name: "Approval"
});

const userId = computed(() => {
  return useUserStoreHook()?.uuid;
});
const tabIndex = ref(0);
const segmentedOptions: Array<OptionsType> = [
  {
    label: "待借出",
    value: 0
  },
  {
    label: "待归还",
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
    false,
    pagination.currentPage,
    pagination.pageSize
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
    label: "批准状态",
    prop: "borrowApproveStatus",
    cellRenderer: ({ row, props }) => (
      <el-tag
        size={props.size}
        style={tagStyle.value(row.borrowApproveStatus ? 1 : 0)}
      >
        {row.borrowApproveStatus ? "批准" : "待批准"}
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
          updateBorrowApproveStatus(row.id, userId.value, true).then(() => {
            onSearch();
            successNotification("批准成功");
          });
        }}
      >
        批准
      </el-button>
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

/** 清空日志 */
function clearAll() {
  // 根据实际业务，调用接口删除所有日志数据
  successNotification("已删除所有日志数据");
  onSearch();
}

/** 批量删除 */
function onBatchDel() {
  // 返回当前选中的行
  const curSelected = tableRef.value.getTableRef().getSelectionRows();
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

function handleSizeChange(val: number) {
  console.log(`${val} items per page`);
}

function handleCurrentChange(val: number) {
  console.log(`current page: ${val}`);
}
</script>

<template>
  <div class="main">
    <Segmented v-model="tabIndex" :options="segmentedOptions" size="large" />
    <el-tabs v-model="tabIndex" type="card" class="myTabs">
      <el-tab-pane :name="segmentedOptions[0].value">
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

        <PureTableBar title="待借出审批" :columns="columns" @refresh="onSearch">
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
              title="确定要删除所有日志数据吗？"
              @confirm="clearAll"
            >
              <template #reference>
                <el-button type="danger" :icon="useRenderIcon(Approve)">
                  批量批准
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
      <el-tab-pane :name="segmentedOptions[1].value">
        <p>其他</p>
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
