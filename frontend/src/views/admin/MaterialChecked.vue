<script setup lang="tsx">
import { h, reactive, ref } from "vue";
import { PaginationProps, PureTable } from "@pureadmin/table";
import { defaultPaginationSizes } from "@/views/hooks";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Search from "@iconify-icons/ep/search";
import Approve from "@iconify-icons/fluent/approvals-app-16-filled";
import PureTableBar from "@/components/RePureTableBar/src/bar";
import { SelectOpt } from "@/views/admin/utils/types";
import { addDialog } from "@/components/ReDialog/index";
import verifyDialog from "@/views/welcome/dialog/VerifyDialog.vue";
import type { userInfo } from "@/views/welcome/types";
import { successNotification, warningNotification } from "@/utils/notification";
import { deviceDetection, getKeyList } from "@pureadmin/utils";
import { getCheckedMaterial, updateCheckedMaterial } from "@/api/material";
import { auth } from "@/api/base";

defineOptions({
  name: "MaterialChecked"
});

const optionBar = reactive({
  area: "",
  type: "",
  returnStatus: false
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

// 送检状态
const checkOpt: SelectOpt = [
  {
    label: "送检中",
    value: false
  },
  {
    label: "已归还",
    value: true
  }
];
const loading = ref(false);
// 表格数据
const dataList = ref([]);
const returnData = reactive({
  username: "",
  uuid: ""
});
const onSearch = () => {
  getCheckedMaterial(
    optionBar.area,
    optionBar.type,
    optionBar.returnStatus,
    pagination.currentPage,
    pagination.pageSize
  ).then(res => {
    dataList.value = res.data;
    pagination.total = res.total;
    pagination.pageSize = res.pageSize;
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
    label: "数量",
    prop: "number"
  },
  {
    label: "送检时间",
    prop: "created_at"
  },
  {
    label: "送检人",
    prop: "toCheckUser",
    cellRenderer: ({ row }) => (
      <el-popover
        placement="right"
        width="200"
        trigger="click"
        v-slots={{
          reference: () => (
            <el-button link>{row.toCheckUser.nickname}</el-button>
          ),
          default: () => (
            <ul>
              <li>姓名：{row.toCheckUser.nickname}</li>
              <li>电话：{row.toCheckUser.phone}</li>
              <li>部门：{row.toCheckUser.depart}</li>
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
    label: "接收人",
    cellRenderer: ({ row }) => (
      <el-popover
        placement="right"
        width="200"
        trigger="click"
        v-slots={{
          reference: () => (
            <el-button link>{row.toReturnUser?.nickname}</el-button>
          ),
          default: () => (
            <ul>
              <li>姓名：{row.toReturnUser?.nickname}</li>
              <li>电话：{row.toReturnUser?.phone}</li>
              <li>部门：{row.toReturnUser?.depart}</li>
            </ul>
          )
        }}
      ></el-popover>
    )
  },
  {
    label: "备注",
    prop: "note",
    cellRenderer: ({ row }) => (
      <el-popover
        placement="bottom"
        width="300"
        trigger="hover"
        v-slots={{
          reference: () => (
            <el-text truncated style="width: 100px">
              {row.note}
            </el-text>
          ),
          default: () => <p>{row.note}</p>
        }}
      ></el-popover>
    )
  },
  {
    label: "操作",
    cellRenderer: ({ row }) => (
      <>
        <el-button
          disabled={row.returnStatus}
          plain
          type="primary"
          onClick={() => {
            openReturnDialog([row], [row.id]);
          }}
        >
          归还
        </el-button>
      </>
    )
  }
];

const openReturnDialog = (rowList, idList?: [number]) => {
  const data = reactive({
    idList,
    note: "",
    toReturnUser: "",
    toReturnUserUUID: ""
  });
  addDialog({
    title: "归还确认",
    width: "25%",
    draggable: true,
    fullscreen: deviceDetection(),
    fullscreenIcon: true,
    closeOnClickModal: false,
    contentRenderer: () => (
      <>
        <el-form
          label-position="right"
          label-width="auto"
          class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px] overflow-auto"
        >
          <el-form-item label="归还信息">
            <ul>
              {rowList.map(item => (
                <li>
                  <el-space wrap>
                    <span>物资名称：{item.material.name}</span>
                    <span>归还数量：{item.number}</span>
                  </el-space>
                </li>
              ))}
            </ul>
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model={data.note} placeholder="这里可以填写备注信息" />
          </el-form-item>
          <el-form-item label="验证人">
            <el-space>
              <el-input
                v-model={data.toReturnUser}
                placeholder="验证人"
                disabled
              />
              <el-button
                plain
                type="primary"
                onClick={() => {
                  const verifyForm = ref();
                  addDialog({
                    title: "验证人",
                    width: "20%",
                    props: {
                      userInfo: {
                        account: "",
                        password: "",
                        name: "",
                        phone: "",
                        depart: "",
                        disable: true
                      }
                    },
                    draggable: true,
                    fullscreen: deviceDetection(),
                    fullscreenIcon: true,
                    closeOnClickModal: false,
                    contentRenderer: () => h(verifyDialog, { ref: verifyForm }),
                    beforeSure(done, { options }) {
                      const accountFormRef = verifyForm.value.getAccountRef();
                      const curData = options.props.userInfo as userInfo;
                      accountFormRef.validate(valid => {
                        if (valid) {
                          auth({
                            username: curData.account,
                            password: curData.password
                          }).then(res => {
                            data.toReturnUser = res.data.nickname;
                            data.toReturnUserUUID = res.data.uuid;
                          });
                          done();
                        }
                      });
                    }
                  });
                }}
              >
                验证
              </el-button>
            </el-space>
          </el-form-item>
        </el-form>
      </>
    ),
    beforeSure(done, { options, index }) {
      if (data.toReturnUserUUID.length === 0) {
        warningNotification("请验证人验证归还物资信息");
        return;
      }
      updateCheckedMaterial(data).then(() => {
        successNotification("归还成功!");
        done();
        onSelectionCancel();
        onSearch();
      });
    }
  });
};

const onBatchReturn = () => {
  const curSelected = tableRef.value.getTableRef().getSelectionRows();
  const idList = getKeyList(curSelected, "id");
  openReturnDialog(curSelected, idList as [number]);
};

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
      <el-form-item label="归还状态" prop="returnStatus">
        <el-select-v2
          v-model="optionBar.returnStatus"
          :options="checkOpt"
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

        <el-popconfirm title="要批量归还吗？" @confirm="onBatchReturn">
          <template #reference>
            <el-button
              type="success"
              :disabled="selectedNum < 1"
              :icon="useRenderIcon(Approve)"
            >
              批量归还
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
