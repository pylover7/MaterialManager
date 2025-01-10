<script lang="tsx" setup>
import { OptionsType } from "@/components/ReSegmented";
import { reactive, ref } from "vue";
import { PaginationProps, PureTable } from "@pureadmin/table";
import { defaultPaginationSizes, usePublicHooks } from "@/views/hooks";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Search from "@iconify-icons/ep/search";
import Reject from "@iconify-icons/fluent/text-change-reject-24-filled";
import PureTableBar from "@/components/RePureTableBar/src/bar";
import { getKeyList } from "@pureadmin/utils";
import { errorNotification, successNotification } from "@/utils/notification";
import { deleteBorrowed, listBorrowed } from "@/api/material";
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
    true,
    true,
    true
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

/** 标签风格 */
const { tagStyle } = usePublicHooks();

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

const onBatchBtnLoading = ref(false);
// 删除所选择的行
const onBatchDel = () => {
  onBatchBtnLoading.value = true;
  const curSelected = tableRef.value.getTableRef().getSelectionRows();
  const idList = getKeyList(curSelected, "id");
  deleteBorrowed(idList)
    .then(res => {
      successNotification(res.msg);
      onSearch();
      tableRef.value.getTableRef().clearSelection();
    })
    .catch(err => {
      errorNotification(err.data.msg);
    })
    .finally(() => {
      onBatchBtnLoading.value = false;
    });
};

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
        placement="bottom"
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
    label: "借出审批",
    prop: "borrowApproveWhether",
    cellRenderer: ({ row, props }) => (
      <el-tag
        size={props.size}
        style={tagStyle.value(row.borrowApproveWhether ? 1 : 0)}
      >
        {row.borrowApproveWhether ? "批准" : "驳回"}
      </el-tag>
    )
  },
  {
    label: "借出批准人",
    prop: "borrowApproveUser",
    cellRenderer: ({ row }) => (
      <el-popover
        placement="right"
        width="180"
        trigger="click"
        v-slots={{
          reference: () => (
            <el-button link>{row.borrowApproveUser?.nickname}</el-button>
          ),
          default: () => (
            <ul>
              <li>工号：{row.borrowApproveUser?.employeeID}</li>
              <li>电话：{row.borrowApproveUser?.mobile}</li>
              <li>部门：{row.borrowApproveUser?.department}</li>
            </ul>
          )
        }}
      ></el-popover>
    )
  },
  {
    label: "借出时间",
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
    label: "归还批准人",
    prop: "returnApproveUser",
    cellRenderer: ({ row, props }) => (
      <el-popover
        placement="right"
        width="180"
        trigger="click"
        v-slots={{
          reference: () => (
            <el-button link>{row.returnApproveUser?.nickname}</el-button>
          ),
          default: () => (
            <ul>
              <li>工号：{row.returnApproveUser?.employeeID}</li>
              <li>电话：{row.returnApproveUser?.mobile}</li>
              <li>部门：{row.returnApproveUser?.department}</li>
            </ul>
          )
        }}
      ></el-popover>
    )
  },
  {
    label: "归还时间",
    prop: "returnApproveTime"
  }
];
</script>

<template>
  <div class="main">
    <el-tab-pane :lazy="true" :name="props.segmentedOptions[2].value">
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

      <PureTableBar :columns="columns" title="借用记录" @refresh="onSearch">
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

          <el-popconfirm title="确定要删除所选记录吗？" @confirm="onBatchDel">
            <template #reference>
              <el-button
                :disabled="selectedNum < 1"
                :icon="useRenderIcon(Reject)"
                :loading="onBatchBtnLoading"
                type="danger"
              >
                删除所选
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
