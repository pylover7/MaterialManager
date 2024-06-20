<script setup lang="tsx">
import { reactive, ref } from "vue";
import { PaginationProps, PureTable } from "@pureadmin/table";
import { usePublicHooks } from "@/views/hooks";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Search from "@iconify-icons/ep/search";
import Approve from "@iconify-icons/fluent/approvals-app-16-filled";
import PureTableBar from "@/components/RePureTableBar/src/bar";
import { SelectOpt } from "@/views/admin/utils/types";

defineOptions({
  name: "MaterialChecked"
});

const optionBar = reactive({
  area: "",
  type: ""
});
// 区域配置
const areaOpt: SelectOpt = [
  {
    label: "隔离办",
    value: "glb"
  },
  {
    label: "辅控",
    value: "fk"
  },
  {
    label: "网控",
    value: "wk"
  }
];
// 类型配置
const typeOpt: SelectOpt = [
  {
    label: "工具",
    value: "tool"
  },
  {
    label: "钥匙",
    value: "key"
  }
];
const loading = ref(false);
// 表格数据
const dataList = ref([]);
const onSearch = () => {};
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
    label: "送检物资信息",
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
    label: "数量",
    prop: "number"
  },
  {
    label: "送检时间",
    prop: "created_at"
  },
  {
    label: "送检人信息",
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
    label: "归还时间",
    prop: "returnDate"
  },
  {
    label: "操作",
    cellRenderer: ({ row }) => (
      <>
        <el-button plain type="primary" onClick={() => {}}>
          归还
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
    <el-form
      ref="optionBarRef"
      :inline="true"
      :model="optionBar"
      class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px] overflow-auto"
    >
      <el-form-item label="选择类型" prop="type">
        <el-select-v2
          v-model="optionBar.type"
          :options="typeOpt"
          placeholder="请选择类型"
          class="!w-[150px]"
        />
      </el-form-item>
      <el-form-item label="选择区域" prop="area">
        <el-select-v2
          v-model="optionBar.area"
          :options="areaOpt"
          placeholder="请选择区域"
          class="!w-[150px]"
        />
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          :icon="useRenderIcon(Search)"
          :loading="loading"
          :disabled="optionBar.area === ''"
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

        <el-popconfirm title="确定要批准所选请求吗？">
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
