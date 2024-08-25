<script setup lang="tsx">
import { ref, reactive, h, computed } from "vue";
import { PureTableBar } from "@/components/RePureTableBar";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Delete from "@iconify-icons/ep/delete";
import Add from "@iconify-icons/ep/circle-plus";
import { PaginationProps, PureTable } from "@pureadmin/table";
import { deviceDetection, getKeyList } from "@pureadmin/utils";
import {
  getMaterialMeta,
  addMaterialMeta,
  deleteMaterialMeta,
  addCheckMaterial
} from "@/api/material";
import type { FormInstance, FormRules } from "element-plus";
import { errorNotification, successNotification } from "@/utils/notification";
import { addDialog } from "@/components/ReDialog";
import attentionForm from "./utils/attentionForm.vue";
import { SelectOpt, FormItemProps } from "./utils/types";
import Search from "@iconify-icons/ep/search";
import { message } from "@/utils/message";
import { useUserStoreHook } from "@/store/modules/user";
import { getDutyOverList, updateDutyOverList } from "@/api/duty";
import { MaterialItem } from "@/types/material";

defineOptions({
  name: "MaterialMeta"
});
const userUUId = computed(() => {
  return useUserStoreHook()?.uuid;
});
// 表格ref
const tableRef = ref();
// 表格加载控制
const loading = ref(false);
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

const area = ref("");
const type = ref("");

// 表格选择的数量
const selectedNum = ref(0);
// 取消选择
const onSelectionCancel = () => {
  selectedNum.value = 0;
  // 用于多选表格，清空用户的选择
  tableRef.value.getTableRef().clearSelection();
};
// 删除所选按钮状态
const onBatchBtnLoading = ref(false);
// 删除所选择的行
const onBatchDel = () => {
  onBatchBtnLoading.value = true;
  const curSelected = tableRef.value.getTableRef().getSelectionRows();
  const idList = getKeyList(curSelected, "id");
  deleteMaterialMeta(idList)
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
// 表格勾选项变化回调函数
function handleSelectionChange(val) {
  selectedNum.value = val.length;
}
// 搜索按钮可用
const searchDisable = computed(() => {
  return area.value == "" || type.value == "";
});
// 表格分页配置
const pagination = reactive<PaginationProps>({
  total: 1,
  pageSize: 10,
  currentPage: 1,
  background: true
});
// 表格页面大小改变回调
const pageSizeChange = (size: number) => {
  if (searchDisable.value) {
    message("请选择类型和区域", { type: "warning" });
    return;
  }
  pagination.pageSize = size;
  onSearch();
};
// 表格翻页回调
const pageCurrentChange = (page: number) => {
  pagination.currentPage = page;
  onSearch();
};
// 表格列
const columns: TableColumnList = [
  {
    label: "勾选列", // 如果需要表格多选，此处label必须设置
    type: "selection",
    fixed: "left",
    reserveSelection: true // 数据刷新后保留选项
  },
  { label: "序号", type: "index", width: "60" },
  { label: "编号", prop: "code", width: "100" },
  { label: "名称", prop: "name" },
  { label: "位置", prop: "position" },
  { label: "型号", prop: "model", width: "200" },
  { label: "数量", prop: "number", width: "100" },
  { label: "借出数量", prop: "borrowed", width: "100" },
  { label: "送检数量", prop: "checking", width: "100" },
  {
    label: "描述",
    prop: "description",
    width: "200",
    cellRenderer: ({ row }) => (
      <el-popover
        placement="right"
        width="300"
        trigger="hover"
        v-slots={{
          reference: () => (
            <el-text truncated style="width: 100px">
              {row.description}
            </el-text>
          ),
          default: () => <p>{row.description}</p>
        }}
      ></el-popover>
    )
  },
  {
    label: "操作",
    prop: "modify",
    width: "240",
    cellRenderer: ({ row }) => (
      <>
        <el-button
          size="small"
          type="primary"
          plain
          onClick={() => {
            addDialog({
              title: "送检数量",
              width: "15%",
              contentRenderer: () => (
                <div style="text-align: center; margin-bottom: 10px ">
                  <el-input-number
                    v-model={toCheckNumber.value}
                    min={1}
                    max={row.number - row.borrowed - row.checking}
                  />
                </div>
              ),
              beforeSure(done, { options, index }) {
                const data = {
                  area: row.area,
                  type: row.type,
                  material_id: row.id,
                  number: toCheckNumber.value,
                  toCheckUserUUID: userUUId.value
                };
                addCheckMaterial(data).then(res => {
                  done();
                  successNotification(
                    `物资【${row.name}】送检数量【${toCheckNumber.value}】`
                  );
                  toCheckNumber.value = 1;
                  onSearch();
                });
              },
              beforeCancel(done, { options, index }) {
                done();
                toCheckNumber.value = 1;
              }
            });
          }}
        >
          送检
        </el-button>

        <el-button
          size="small"
          type="warning"
          plain
          onClick={() => {
            addMaterial("修改", row);
          }}
        >
          修改
        </el-button>
        <el-button
          size="small"
          type="danger"
          plain
          onClick={() => {
            deleteById(row.id);
          }}
        >
          删除
        </el-button>
      </>
    )
  }
];

// 表格操作列删除按钮函数
const deleteById = (id: number) => {
  deleteMaterialMeta([id])
    .then(res => {
      successNotification(res.msg);
      onSearch();
    })
    .catch(err => {
      errorNotification(err.msg);
    });
};
const toCheckNumber = ref(1);

// 表格数据
const dataList = reactive([]);
// 表格刷新
function onSearch() {
  loading.value = true;
  dataList.length = 0;
  getMaterialMeta(
    area.value,
    type.value,
    pagination.currentPage,
    pagination.pageSize
  )
    .then(res => {
      dataList.push(...res.data);
      pagination.total = res.total;
      pagination.pageSize = res.pageSize;
      pagination.currentPage = res.page;
    })
    .finally(() => {
      loading.value = false;
    });
}
// 添加物资表单ref
const addFormRef = ref<FormInstance>();
// 添加物资抽屉控制
const addDrawer = ref(false);
// 添加物资确定按钮加载控制
const submitLoading = ref(false);
// 添加物资抽屉标题
const addDrawerTitle = ref("");
// 开启添加物资抽屉
const addMaterial = (title: string, row?: MaterialItem) => {
  addDrawerTitle.value = title;
  addForm.area = area.value;
  addForm.type = type.value;
  addForm.number = row?.number ?? 1;
  addForm.position = row?.position ?? "";
  addForm.name = row?.name ?? "";
  addForm.code = row?.code ?? "";
  addForm.model = row?.model ?? "";
  addForm.borrowed = row?.borrowed ?? 0;
  addForm.checking = row?.checking ?? 0;
  addForm.description = row?.description ?? "";
  addForm.id = row?.id;
  addDrawer.value = true;
};
// 关闭添加物资抽屉
const drawerCancel = () => {
  addDrawer.value = false;
};
// 添加物资表单数据
const addForm = reactive<MaterialItem>({
  type: "",
  area: "",
  name: "",
  code: "",
  model: "",
  position: "",
  number: 1,
  checking: 0,
  borrowed: 0,
  description: ""
});

// 清除添加物资表单数据
const clearAddForm = (formEl: FormInstance | undefined) => {
  delete addForm.id;
  if (!formEl) return;
  formEl.resetFields();
};
// 添加物资表单数据校验
const rules = reactive<FormRules<MaterialItem>>({
  area: [{ required: true, message: "请选择区域！", trigger: "blur" }],
  type: [{ required: true, message: "请选择物资类型！", trigger: "blur" }],
  name: [{ required: true, message: "请输入物资名称信息！", trigger: "blur" }],
  code: [{ required: true, message: "请输入物资编码信息！", trigger: "blur" }],
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
// 添加物资表单确认
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate((valid, fields) => {
    if (valid) {
      submitLoading.value = true;
      addMaterialMeta(addForm)
        .then(res => {
          addDrawer.value = false;
          onSearch();
          successNotification(
            `${addDrawerTitle.value}物资【${res.data.name}】成功`
          );
        })
        .finally(() => {
          submitLoading.value = false;
        });
    }
  });
};
const attRef = ref();
// 注意事项弹窗
function openDialog(area: string) {
  getDutyOverList(area).then(res => {
    const itemList = res.data;
    itemList.forEach(item => {
      item.key = item.id;
    });

    addDialog({
      title: `查看注意事项`,
      props: {
        formData: itemList
      },
      width: "50%",
      draggable: true,
      fullscreen: deviceDetection(),
      fullscreenIcon: true,
      closeOnClickModal: false,
      contentRenderer: () => h(attentionForm, { ref: attRef }),
      beforeSure: (done, { options }) => {
        const FormRef = attRef.value.getRef();
        const curData = options.props.formData as [FormItemProps];

        /** 关闭弹框，刷新表格数据 */
        function chores() {
          done(); // 关闭弹框
          // onSearch(); // 刷新表格数据
        }

        FormRef.validate(valid => {
          if (valid) {
            // 表单规则校验通过
            curData.forEach(item => {
              delete item.key;
              delete item.created_at;
              delete item.updated_at;
            });
            updateDutyOverList(area, curData).then(res => {
              chores();
              successNotification(res.msg);
            });
          }
        });
      }
    });
  });
}
</script>

<template>
  <div class="main">
    <el-form
      ref="formRef"
      :inline="true"
      class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px] overflow-auto"
    >
      <el-form-item label="选择类型" prop="type">
        <el-select-v2
          v-model="type"
          :options="typeOpt"
          placeholder="请选择类型"
          class="!w-[150px]"
        />
      </el-form-item>
      <el-form-item label="选择区域" prop="area">
        <el-select-v2
          v-model="area"
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
          :disabled="searchDisable"
          @click="onSearch"
          >搜索</el-button
        >
      </el-form-item>
      <el-form-item style="margin-left: auto">
        <el-button
          type="primary"
          :disabled="searchDisable"
          @click="openDialog(area)"
          >查看注意事项</el-button
        >
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
          :disabled="searchDisable"
          @click="addMaterial('新增')"
        >
          新增
        </el-button>
        <el-popconfirm title="确定要删除选择的数据吗？" @confirm="onBatchDel">
          <template #reference>
            <el-button
              type="danger"
              :icon="useRenderIcon(Delete)"
              :disabled="selectedNum < 1"
              :loading="onBatchBtnLoading"
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
          @page-current-change="pageCurrentChange"
          @page-size-change="pageSizeChange"
        />
      </template>
    </PureTableBar>

    <el-drawer
      v-model="addDrawer"
      direction="rtl"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :destroy-on-close="true"
      :show-close="false"
      @close="clearAddForm(addFormRef)"
    >
      <template #header>
        <h4>{{ addDrawerTitle }}物资项</h4>
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
            <el-form-item label="类型" prop="type">
              <el-select-v2
                v-model="addForm.type"
                disabled
                :options="typeOpt"
                class="!w-[150px]"
              />
            </el-form-item>
            <el-form-item label="区域" prop="area">
              <el-select-v2
                v-model="addForm.area"
                disabled
                :options="areaOpt"
                class="!w-[150px]"
              />
            </el-form-item>
            <el-form-item label="名称" prop="name">
              <el-input v-model="addForm.name" />
            </el-form-item>
            <el-form-item label="编号" prop="code">
              <el-input v-model="addForm.code" />
            </el-form-item>
            <el-form-item label="型号" prop="model">
              <el-input v-model="addForm.model" />
            </el-form-item>
            <el-form-item label="位置" prop="position">
              <el-input v-model="addForm.position" />
            </el-form-item>
            <el-form-item label="数量" prop="number">
              <el-input-number
                v-model="addForm.number"
                :controls="false"
                size="default"
              />
            </el-form-item>
            <el-form-item label="描述" prop="description">
              <el-input v-model="addForm.description" />
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
  display: flex;
  :deep(.el-form-item) {
    margin-bottom: 12px;
  }
}
</style>
