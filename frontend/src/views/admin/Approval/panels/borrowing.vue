<script lang="tsx" setup>
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Search from "@iconify-icons/ep/search";
import Approve from "@iconify-icons/fluent/approvals-app-16-filled";
import Reject from "@iconify-icons/fluent/text-change-reject-24-filled";
import { reactive, ref } from "vue";
import { PaginationProps, PureTable } from "@pureadmin/table";
import { defaultPaginationSizes, usePublicHooks } from "@/views/hooks";
import { message } from "@/utils/message";
import PureTableBar from "@/components/RePureTableBar/src/bar";
import { successNotification } from "@/utils/notification";
import { getKeyList } from "@pureadmin/utils";
import { OptionsType } from "@/components/ReSegmented";
import { listBorrowed, updateBorrowedInfo } from "@/api/material";
import { SelectOpt } from "@/views/admin/utils/types";

const props = defineProps({
  segmentedOptions: {
    type: Array<OptionsType>,
    required: true
  },
  userId: { type: String, required: true },
  areaOpt: { type: Array<SelectOpt>, required: true }
});

const borrowedOptBar = reactive({
  area: ""
});
const loading = ref(false);
// 表格数据
const dataList = ref([]);
const onSearch = () => {
  loading.value = true;
  listBorrowed(
    borrowedOptBar.area,
    pagination.currentPage,
    pagination.pageSize,
    false
  )
    .then(res => {
      dataList.value = res.data;
      pagination.total = res.total;
    })
    .finally(() => {
      loading.value = false;
    });
};
// 分页设置
const pagination = reactive<PaginationProps>({
  total: 0,
  pageSize: 15,
  currentPage: 1,
  background: true,
  pageSizes: defaultPaginationSizes
});

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
    props.userId,
    true,
    whether
  ).then(() => {
    onSearch();
    tableRef.value.getTableRef().clearSelection();
    successNotification(`已批${whether ? "通过" : "驳回"}所选请求`);
  });
}

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
          reference: () => <el-button link>{row.material.name}</el-button>,
          default: () => (
            <ul>
              <li>名称：{row.material.name}</li>
              <li>型号：{row.material.model}</li>
              <li>位置：{row.material.position}</li>
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
          reference: () => <el-button link>{row.nickname}</el-button>,
          default: () => (
            <ul>
              <li>姓名：{row.nickname}</li>
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
    label: "数量",
    prop: "borrowing"
  },
  {
    label: "借用理由",
    prop: "reason",
    cellRenderer: ({ row }) => (
      <el-popover
        placement="right"
        width="300"
        trigger="hover"
        v-slots={{
          reference: () => (
            <el-text truncated style="width: 100px">
              {row.reason}
            </el-text>
          ),
          default: () => <p>{row.reason}</p>
        }}
      ></el-popover>
    )
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
            updateBorrowedInfo([row.id], props.userId, true, true).then(() => {
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
            updateBorrowedInfo([row.id], props.userId, true, false).then(() => {
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

/** 当CheckBox选择项发生变化时会触发该事件 */
function handleSelectionChange(val) {
  selectedNum.value = val.length;
  // 重置表格高度
  tableRef.value.setAdaptive();
}

function handleSizeChange(val: number) {
  pagination.pageSize = val;
  onSearch();
}

function handleCurrentChange(val: number) {
  pagination.currentPage = val;
  onSearch();
}
</script>

<template>
  <div class="main">
    <el-tab-pane :lazy="true" :name="props.segmentedOptions[0].value">
      <el-form
        ref="borrowedOptBarRef"
        :inline="true"
        :model="borrowedOptBar"
        class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px] overflow-auto"
      >
        <el-form-item label="选择区域" prop="area">
          <el-select
            v-model="borrowedOptBar.area"
            class="!w-[150px]"
            placeholder="请选择区域"
          >
            <el-option
              v-for="item in areaOpt"
              :key="item.label"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button
            :disabled="borrowedOptBar.area === ''"
            :icon="useRenderIcon(Search)"
            :loading="loading"
            type="primary"
            @click="onSearch"
          >
            搜索
          </el-button>
        </el-form-item>
      </el-form>

      <PureTableBar :columns="columns" title="借出待审批" @refresh="onSearch">
        <template #buttons>
          <div class="h-full mb-2 pl-4 flex items-center">
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
          </div>

          <el-popconfirm
            title="确定要批准所选请求吗？"
            @confirm="onBatch(true)"
          >
            <template #reference>
              <el-button
                :disabled="selectedNum < 1"
                :icon="useRenderIcon(Approve)"
                type="success"
              >
                批量批准
              </el-button>
            </template>
          </el-popconfirm>
          <el-popconfirm
            title="确定要驳回所选请求吗？"
            @confirm="onBatch(false)"
          >
            <template #reference>
              <el-button
                :disabled="selectedNum < 1"
                :icon="useRenderIcon(Reject)"
                type="danger"
              >
                批量驳回
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
          />
        </template>
      </PureTableBar>
    </el-tab-pane>
  </div>
</template>
