<script setup lang="tsx">
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Search from "@iconify-icons/ep/search";
import Approve from "@iconify-icons/fluent/approvals-app-16-filled";
import { reactive, ref } from "vue";
import { message } from "@/utils/message";
import { PaginationProps } from "@pureadmin/table";
import { getKeyList } from "@pureadmin/utils";
import { successNotification } from "@/utils/notification";
import { defaultPaginationSizes, usePublicHooks } from "@/views/hooks";
import PureTableBar from "@/components/RePureTableBar/src/bar";
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

const returnOptBarRef = ref();
const returnTableRef = ref();
const returnedOptBar = reactive({
  area: ""
});
const loading = ref(false);
/** 标签风格 */
const { tagStyle } = usePublicHooks();

const onSearchReturn = () => {
  loading.value = true;
  listBorrowed(
    returnedOptBar.area,
    pagination2.currentPage,
    pagination2.pageSize,
    true,
    true,
    false
  )
    .then(res => {
      returnDataList.value = res.data;
      pagination2.total = res.total;
    })
    .finally(() => {
      loading.value = false;
    });
};

const selectedNum = ref(0);
// 表格ref
const tableRef = ref();

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
    label: "借用数量",
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
          updateBorrowedInfo([row.id], props.userId, false, false, true).then(
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
  pageSize: 15,
  currentPage: 1,
  background: true,
  pageSizes: defaultPaginationSizes
});

const onBatchReturn = () => {
  const curSelected = returnTableRef.value.getTableRef().getSelectionRows();
  updateBorrowedInfo(
    getKeyList(curSelected, "id"),
    props.userId,
    false,
    true,
    true
  ).then(() => {
    onSearchReturn();
    returnTableRef.value.getTableRef().clearSelection();
    successNotification("已批通过选请求");
  });
};
/** 取消选择 */
function onSelectionCancel() {
  selectedNum.value = 0;
  // 用于多选表格，清空用户的选择
  tableRef.value.getTableRef().clearSelection();
}
/** 当CheckBox选择项发生变化时会触发该事件 */
function returnHandleSelectionChange(val) {
  returnSelectedNum.value = val.length;
  // 重置表格高度
  returnTableRef.value.setAdaptive();
}

function handleSizeChange(val: number) {
  pagination2.pageSize = val;
  onSearchReturn();
}

function handleCurrentChange(val: number) {
  pagination2.currentPage = val;
  onSearchReturn();
}
</script>

<template>
  <div class="main">
    <el-tab-pane :name="props.segmentedOptions[1].value" :lazy="true">
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
              <el-button
                type="success"
                :disabled="selectedNum < 1"
                :icon="useRenderIcon(Approve)"
              >
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
  </div>
</template>

<style scoped lang="scss"></style>
