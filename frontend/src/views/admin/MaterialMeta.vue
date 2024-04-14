<script setup lang="tsx">
import { ref, reactive } from "vue";
import { PureTableBar } from "@/components/RePureTableBar";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Delete from "@iconify-icons/ep/delete";
import Add from "@iconify-icons/ep/circle-plus";
import type { PaginationProps } from "@pureadmin/table";
import { getKeyList } from "@pureadmin/utils";
import { getMaterialMeta } from "@/api/material";
import { warningNotification, errorNotification } from "@/utils/notification";

defineOptions({
  name: "MaterialMeta"
});
const tableRef = ref();
const loading = ref(false);
const area = ref("");

const areaChange = (value: string) => {
  area.value = value;
  onSearch();
};

// 表格选择的数量
const selectedNum = ref(0);
// 取消选择
const onSelectionCancel = () => {
  selectedNum.value = 0;
  // 用于多选表格，清空用户的选择
  tableRef.value.getTableRef().clearSelection();
};

// 删除所选择的行
const onBatchDel = () => {
  const curSelected = tableRef.value.getTableRef().getSelectionRows();
  const idList = getKeyList(curSelected, "id");
  console.log(idList);
  onSearch();

  tableRef.value.getTableRef().clearSelection();
};

function handleSelectionChange(val) {
  selectedNum.value = val.length;
}

const pagination = reactive<PaginationProps>({
  total: 0,
  pageSize: 10,
  currentPage: 1,
  background: true,
  hideOnSinglePage: true
});

const columns: TableColumnList = [
  {
    label: "勾选列", // 如果需要表格多选，此处label必须设置
    type: "selection",
    fixed: "left",
    reserveSelection: true // 数据刷新后保留选项
  },
  { label: "序号", type: "index", width: "60" },
  { label: "位置", prop: "position" },
  { label: "名称", prop: "name" },
  { label: "型号", prop: "model", width: "200" },
  { label: "数量", prop: "number", width: "100" },
  {
    label: "操作",
    prop: "modify",
    width: "160",
    cellRenderer: ({ row }) => (
      <>
        <el-button size="small" type="warning" plain>
          修改
        </el-button>
        <el-button size="small" type="danger" plain>
          删除
        </el-button>
      </>
    )
  }
];

const dataList = reactive([]);

async function onSearch() {
  if (area.value) {
    loading.value = true;
    dataList.length = 0;
    await getMaterialMeta(area.value)
      .then(res => {
        dataList.push(...res.data);
        pagination.total = res.total;
        pagination.pageSize = res.pageSize;
        pagination.currentPage = res.page;
      })
      .finally(() => {
        loading.value = false;
      });
  } else {
    warningNotification("请选择区域");
  }
}
</script>

<template>
  <div class="main">
    <el-form
      ref="formRef"
      :inline="true"
      class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px] overflow-auto"
    >
      <el-form-item label="选择区域" prop="area">
        <el-select
          v-model="area"
          placeholder="请选择"
          clearable
          class="!w-[150px]"
          @change="areaChange"
        >
          <el-option label="隔离办" value="glb" />
          <el-option label="辅控" value="fk" />
          <el-option label="网控" value="wk" />
        </el-select>
      </el-form-item>
    </el-form>

    <PureTableBar :columns="columns">
      <template #title>
        <div v-motion-fade class="h-full mb-2 pl-4 flex items-center">
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
        <el-button type="primary" :icon="useRenderIcon(Add)"> 新增 </el-button>
        <el-popconfirm title="确定要删除选择的数据吗？" @confirm="onBatchDel">
          <template #reference>
            <el-button type="danger" :icon="useRenderIcon(Delete)">
              删除所选
            </el-button>
          </template>
        </el-popconfirm>
      </template>
      <template v-slot="{ size, dynamicColumns }">
        <pure-table
          ref="tableRef"
          :data="dataList"
          row-key="id"
          align-whole="center"
          table-layout="auto"
          :loading="loading"
          border
          :size="size"
          adaptive
          :adaptiveConfig="{ offsetBottom: 108 }"
          :columns="dynamicColumns"
          :paginationSmall="size === 'small'"
          :pagination="pagination"
          :header-cell-style="{
            background: 'var(--el-fill-color-light)',
            color: 'var(--el-text-color-primary)'
          }"
          @selection-change="handleSelectionChange"
        />
      </template>
    </PureTableBar>
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
</style>
