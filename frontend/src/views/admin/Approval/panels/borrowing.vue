<script setup lang="tsx">
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Search from "@iconify-icons/ep/search";
import Approve from "@iconify-icons/fluent/approvals-app-16-filled";
import Reject from "@iconify-icons/fluent/text-change-reject-24-filled";
import { reactive, ref } from "vue";
import { listBorrowed } from "@/api/home";
import { PaginationProps, PureTable } from "@pureadmin/table";
import { usePublicHooks } from "@/views/hooks";
import { message } from "@/utils/message";
import { updateBorrowedInfo } from "@/api/home";
import PureTableBar from "@/components/RePureTableBar/src/bar";
import { successNotification } from "@/utils/notification";
import { getKeyList } from "@pureadmin/utils";
import { OptionsType } from "@/components/ReSegmented";

const props = defineProps({
  segmentedOptions: {
    type: Array<OptionsType>,
    required: true
  },
  userId: { type: String, required: true }
});

const borrowedOptBar = reactive({
  area: ""
});
const loading = ref(false);
// 表格数据
const dataList = ref([]);
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
// 分页设置
const pagination = reactive<PaginationProps>({
  total: 0,
  pageSize: 10,
  currentPage: 1,
  background: true,
  pageSizes: [10, 20, 30, 50]
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
  console.log(`${val} items per page`);
}

function handleCurrentChange(val: number) {
  console.log(`current page: ${val}`);
}
</script>

<template>
  <div class="main">
    <el-tab-pane :name="props.segmentedOptions[0].value" :lazy="true">
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
              <el-button
                type="success"
                :disabled="selectedNum < 1"
                :icon="useRenderIcon(Approve)"
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
                type="danger"
                :disabled="selectedNum < 1"
                :icon="useRenderIcon(Reject)"
              >
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
  </div>
</template>

<style scoped lang="scss"></style>
