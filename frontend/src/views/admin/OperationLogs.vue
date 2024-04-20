<script setup lang="tsx">
import dayjs from "dayjs";
import { ref, reactive } from "vue";
import type { FormInstance } from "element-plus";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { getPickerShortcuts, usePublicHooks } from "./utils";
import { PureTableBar } from "@/components/RePureTableBar";
import { successNotification } from "@/utils/notification";

import Refresh from "@iconify-icons/ep/refresh";
import Delete from "@iconify-icons/ep/delete";
import Search from "@iconify-icons/ep/search";
import { PaginationProps, PureTable } from "@pureadmin/table";
import { getKeyList } from "@pureadmin/utils";

defineOptions({
  name: "OperationLogs"
});
// 操作栏表单
const operationBarRef = ref<FormInstance>();
// 操作栏表单数据
const operationForm = reactive({
  area: "",
  status: "",
  operatingTime: ""
});
// 操作栏表单重置
const resetForm = formEl => {
  if (!formEl) return;
  formEl.resetFields();
  onSearch();
};
// 加载状态
const loading = ref(false);
// 搜索
const onSearch = () => {
  console.log(operationForm);
};
// 表格ref
const tableRef = ref();
// 表格数据
const dataList = ref([]);
// 表格列
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
    minWidth: 60
  },
  {
    label: "位置",
    prop: "position",
    minWidth: 100
  },
  {
    label: "名称",
    prop: "name",
    minWidth: 140
  },
  {
    label: "型号",
    prop: "model",
    minWidth: 140
  },
  {
    label: "数量",
    prop: "number",
    minWidth: 100
  },
  {
    label: "实际数量",
    prop: "nowNumber",
    minWidth: 140
  },
  {
    label: "值班人员",
    prop: "dutyPerson",
    minWidth: 100
  },
  {
    label: "科值",
    prop: "dutyPersonDepart",
    minWidth: 100
  },
  {
    label: "状态",
    prop: "status",
    minWidth: 100,
    cellRenderer: ({ row, props }) => (
      <el-tag size={props.size} style={tagStyle.value(row.status)}>
        {row.number === row.nowNumber ? "正确" : "错误"}
      </el-tag>
    )
  },
  {
    label: "值班时间",
    prop: "dutyDate",
    minWidth: 180,
    formatter: ({ operatingTime }) =>
      dayjs(operatingTime).format("YYYY-MM-DD HH:mm:ss")
  }
];
const { tagStyle } = usePublicHooks();

/** 清空日志 */
function clearAll() {
  // 根据实际业务，调用接口删除所有日志数据
  successNotification("已删除所有日志数据");
  onSearch();
}

// 已选择的行数
const selectedNum = ref(0);

/** 取消选择 */
function onSelectionCancel() {
  selectedNum.value = 0;
  // 用于多选表格，清空用户的选择
  tableRef.value.getTableRef().clearSelection();
}

/** 批量删除 */
function onbatchDel() {
  // 返回当前选中的行
  const curSelected = tableRef.value.getTableRef().getSelectionRows();
  // 接下来根据实际业务，通过选中行的某项数据，比如下面的id，调用接口进行批量删除
  successNotification(`已删除序号为 ${getKeyList(curSelected, "id")} 的数据`);
  tableRef.value.getTableRef().clearSelection();
  onSearch();
}

// 分页设置
const pagination = reactive<PaginationProps>({
  total: 0,
  pageSize: 10,
  currentPage: 1,
  background: true
});

function handleSizeChange(val: number) {
  console.log(`${val} items per page`);
}

function handleCurrentChange(val: number) {
  console.log(`current page: ${val}`);
}

/** 当CheckBox选择项发生变化时会触发该事件 */
function handleSelectionChange(val) {
  selectedNum.value = val.length;
  // 重置表格高度
  tableRef.value.setAdaptive();
}
</script>

<template>
  <div class="main">
    <el-form
      ref="operationBarRef"
      :inline="true"
      :model="operationForm"
      class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px] overflow-auto"
    >
      <el-form-item label="选择区域" prop="area">
        <el-select
          v-model="operationForm.area"
          placeholder="请选择区域"
          clearable
          class="!w-[150px]"
        >
          <el-option label="隔离办" value="glb" />
          <el-option label="辅控" value="fk" />
          <el-option label="网控" value="wk" />
        </el-select>
      </el-form-item>
      <el-form-item label="操作状态" prop="status">
        <el-select
          v-model="operationForm.status"
          placeholder="请选择"
          clearable
          class="!w-[150px]"
        >
          <el-option label="正确" value="1" />
          <el-option label="错误" value="0" />
        </el-select>
      </el-form-item>
      <el-form-item label="操作时间" prop="operatingTime">
        <el-date-picker
          v-model="operationForm.operatingTime"
          :shortcuts="getPickerShortcuts()"
          type="datetimerange"
          range-separator="至"
          start-placeholder="开始日期时间"
          end-placeholder="结束日期时间"
        />
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
        <el-button
          :icon="useRenderIcon(Refresh)"
          @click="resetForm(operationBarRef)"
        >
          重置
        </el-button>
      </el-form-item>
    </el-form>

    <PureTableBar :columns="columns" @refresh="onSearch">
      <template #title>
        <h4>值班日志</h4>
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
      </template>
      <template #buttons>
        <el-popconfirm title="确定要删除所有日志数据吗？" @confirm="clearAll">
          <template #reference>
            <el-button type="danger" :icon="useRenderIcon(Delete)">
              清空日志
            </el-button>
          </template>
        </el-popconfirm>
      </template>
      <template v-slot="{ size, dynamicColumns }">
        <div
          v-if="selectedNum > 0"
          v-motion-fade
          class="bg-[var(--el-fill-color-light)] w-full h-[46px] mb-2 pl-4 flex items-center"
        >
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
          <el-popconfirm title="是否确认删除?" @confirm="onbatchDel">
            <template #reference>
              <el-button type="danger" text class="mr-1"> 批量删除 </el-button>
            </template>
          </el-popconfirm>
        </div>
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
  </div>
</template>

<style scoped lang="scss"></style>
