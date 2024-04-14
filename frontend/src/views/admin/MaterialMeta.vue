<script setup lang="tsx">
import { ref, reactive } from "vue";
import { PureTableBar } from "@/components/RePureTableBar";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Delete from "@iconify-icons/ep/delete";
import Add from "@iconify-icons/ep/circle-plus";
import type { PaginationProps } from "@pureadmin/table";
import { getKeyList } from "@pureadmin/utils";
import { getMaterialMeta, addMaterialMeta } from "@/api/material";
import { successNotification, warningNotification } from "@/utils/notification";
import { message } from "@/utils/message";
import type { FormInstance, FormRules } from "element-plus";

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
const areaClear = () => {
  dataList.length = 0;
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
      .catch(e => {
        area.value = "";
      })
      .finally(() => {
        loading.value = false;
      });
  } else {
    warningNotification("请选择区域");
  }
}

const addFormRef = ref<FormInstance>();
const addDrawer = ref(false);
const submitLoading = ref(false);
const addMaterial = () => {
  addDrawer.value = true;
};
const drawerCancel = () => {
  addDrawer.value = false;
};

interface RuleForm {
  name: string;
  model: string;
  position: string;
  number: string;
  depart?: string;
}

const addForm = reactive<RuleForm>({
  name: "",
  model: "",
  position: "",
  number: ""
});

const clearAddForm = () => {
  const keys = Object.keys(addForm);

  for (const key of keys) {
    delete addForm[key];
  }
};

const rules = reactive<FormRules<RuleForm>>({
  name: [{ required: true, message: "请输入物资名称信息！", trigger: "blur" }],
  position: [
    { required: true, message: "请输入物资位置信息", trigger: "blur" }
  ],
  number: [
    {
      required: true,
      message: "请输入物资数量",
      trigger: "blur"
    }
  ]
});

const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate((valid, fields) => {
    if (valid) {
      submitLoading.value = true;
      addForm.depart = area.value;
      addMaterialMeta(addForm)
        .then(res => {
          addDrawer.value = false;
          onSearch();
          successNotification(`添加物资【${res.data.name}】成功`);
        })
        .finally(() => {
          submitLoading.value = false;
        });
    } else {
      message(`验证失败`, { type: "error" });
    }
  });
};
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
          @clear="areaClear"
        >
          <el-option label="隔离办" value="glb" />
          <el-option label="辅控" value="fk" />
          <el-option label="网控" value="wk" />
        </el-select>
      </el-form-item>
    </el-form>

    <PureTableBar :columns="columns" @refresh="onSearch">
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
        <el-button
          type="primary"
          :icon="useRenderIcon(Add)"
          :disabled="!area"
          @click="addMaterial"
        >
          新增
        </el-button>
        <el-popconfirm title="确定要删除选择的数据吗？" @confirm="onBatchDel">
          <template #reference>
            <el-button
              type="danger"
              :icon="useRenderIcon(Delete)"
              :disabled="selectedNum < 1"
            >
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

    <el-drawer
      v-model="addDrawer"
      direction="rtl"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      @close="clearAddForm"
    >
      <template #header>
        <h4>新增物资项</h4>
      </template>
      <template #default>
        <div>
          <el-form
            ref="addFormRef"
            style="max-width: 600px"
            :model="addForm"
            label-width="auto"
            :rules="rules"
            status-icon
          >
            <el-form-item label="名称" prop="name">
              <el-input v-model="addForm.name" />
            </el-form-item>
            <el-form-item label="型号" prop="model">
              <el-input v-model="addForm.model" />
            </el-form-item>
            <el-form-item label="位置" prop="position">
              <el-input v-model="addForm.position" />
            </el-form-item>
            <el-form-item label="数量" prop="number">
              <el-input v-model="addForm.number" />
            </el-form-item>
          </el-form>
        </div>
      </template>
      <template #footer>
        <div style="flex: auto; text-align: left">
          <el-row class="row-bg" justify="space-between">
            <el-col :span="6"
              ><el-button
                type="success"
                plain
                :loading="submitLoading"
                @click="submitForm(addFormRef)"
                >确定</el-button
              ></el-col
            >
            <el-col :span="6" style="text-align: right"
              ><el-button type="warning" plain @click="drawerCancel"
                >取消</el-button
              ></el-col
            >
          </el-row>
        </div>
      </template>
    </el-drawer>
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
