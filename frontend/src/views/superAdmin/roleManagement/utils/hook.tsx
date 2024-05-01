import dayjs from "dayjs";
import editForm from "../form.vue";
import { handleTree, buildApiTree } from "@/utils/tree";
import { message } from "@/utils/message";
import { ElMessageBox } from "element-plus";
import { usePublicHooks } from "../../../hooks";
import { transformI18n } from "@/plugins/i18n";
import { addDialog } from "@/components/ReDialog";
import type { FormItemProps } from "../utils/types";
import type { PaginationProps } from "@pureadmin/table";
import { getKeyList, deviceDetection } from "@pureadmin/utils";
import {
  addRole,
  deleteRole,
  getApiList,
  getMenuList,
  getRoleAuth,
  getRoleList,
  updateRole,
  updateRoleAuth
} from "@/api/system";
import { type Ref, reactive, ref, onMounted, h, toRaw, watch } from "vue";
import type { OptionsType } from "@/components/ReSegmented";
import { successNotification } from "@/utils/notification";

export function useRole(menuTreeRef: Ref, apiTreeRef: Ref) {
  const form = reactive({
    name: "",
    code: "",
    status: null
  });
  const curRow = ref();
  const formRef = ref();
  const dataList = ref([]);
  const menuTreeIds = ref([]);
  const apiParentTreeIds = ref([]);
  const apiTreeIds = ref([]);
  const menuTreeData = ref([]);
  const apiTreeData = ref([]);
  const isShow = ref(false);
  const loading = ref(true);
  const isLinkage = ref(true);
  const apiIsLinkage = ref(true);
  const treeSearchValue = ref();
  const switchLoadMap = ref({});
  const isExpandAll = ref(false);
  const apiIsExpandAll = ref(false);
  const isSelectAll = ref(false);
  const apiIsSelectAll = ref(false);
  const tabIndex = ref(0);
  const { switchStyle } = usePublicHooks();
  const menuTreeProps = {
    value: "id",
    label: "title",
    children: "children"
  };
  const apiTreeProps = {
    value: "id",
    label: "summary",
    children: "children"
  };
  const pagination = reactive<PaginationProps>({
    total: 0,
    pageSize: 10,
    currentPage: 1,
    background: true
  });
  const tabOperation: Array<OptionsType> = [
    {
      label: "菜单权限",
      value: 0
    },
    {
      label: "API权限",
      value: 1
    }
  ];
  const columns: TableColumnList = [
    {
      label: "角色编号",
      prop: "id"
    },
    {
      label: "角色名称",
      prop: "name"
    },
    {
      label: "角色标识",
      prop: "code"
    },
    {
      label: "状态",
      cellRenderer: scope => (
        <el-switch
          size={scope.props.size === "small" ? "small" : "default"}
          loading={switchLoadMap.value[scope.index]?.loading}
          v-model={scope.row.status}
          active-value={1}
          inactive-value={0}
          active-text="已启用"
          inactive-text="已停用"
          inline-prompt
          style={switchStyle.value}
          onChange={() => onChange(scope as any)}
        />
      ),
      minWidth: 90
    },
    {
      label: "备注",
      prop: "remark",
      minWidth: 160
    },
    {
      label: "创建时间",
      prop: "created_at",
      minWidth: 160,
      formatter: ({ created_at }) =>
        dayjs(created_at).format("YYYY-MM-DD HH:mm:ss")
    },
    {
      label: "操作",
      fixed: "right",
      width: 210,
      slot: "operation"
    }
  ];

  function onChange({ row, index }) {
    ElMessageBox.confirm(
      `确认要<strong>${
        row.status === 0 ? "停用" : "启用"
      }</strong><strong style='color:var(--el-color-primary)'>${
        row.name
      }</strong>吗?`,
      "系统提示",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        dangerouslyUseHTMLString: true,
        draggable: true
      }
    )
      .then(() => {
        switchLoadMap.value[index] = Object.assign(
          {},
          switchLoadMap.value[index],
          {
            loading: true
          }
        );
        delete row.updated_at;
        delete row.created_at;
        updateRole(row)
          .then(() => {
            setTimeout(() => {
              switchLoadMap.value[index] = Object.assign(
                {},
                switchLoadMap.value[index],
                {
                  loading: false
                }
              );
              message(`已${row.status === 0 ? "停用" : "启用"}${row.name}`, {
                type: "success"
              });
            }, 300);
            onSearch();
          })
          .catch(() => {
            row.status === 0 ? (row.status = 1) : (row.status = 0);
          });
      })
      .catch(() => {
        row.status === 0 ? (row.status = 1) : (row.status = 0);
      });
  }

  function handleDelete(row) {
    deleteRole(row.id, row.name).then(() => {
      message(`您删除了角色名称为${row.name}的这条数据`, { type: "success" });
      onSearch();
    });
  }

  function handleSizeChange(val: number) {
    console.log(`${val} items per page`);
  }

  function handleCurrentChange(val: number) {
    console.log(`current page: ${val}`);
  }

  function handleSelectionChange(val) {
    console.log("handleSelectionChange", val);
  }

  async function onSearch() {
    loading.value = true;
    const { data, total, currentPage, pageSize } = await getRoleList(
      pagination.currentPage,
      pagination.pageSize,
      toRaw(form)
    );
    dataList.value = data;
    pagination.total = total;
    pagination.pageSize = pageSize;
    pagination.currentPage = currentPage;

    setTimeout(() => {
      loading.value = false;
    }, 500);
  }

  const resetForm = formEl => {
    if (!formEl) return;
    formEl.resetFields();
    onSearch();
  };

  function openDialog(title = "新增", row?: FormItemProps) {
    addDialog({
      title: `${title}角色`,
      props: {
        formInline: {
          id: row?.id ?? 0,
          name: row?.name ?? "",
          code: row?.code ?? "",
          remark: row?.remark ?? ""
        }
      },
      width: "40%",
      draggable: true,
      fullscreen: deviceDetection(),
      fullscreenIcon: true,
      closeOnClickModal: false,
      contentRenderer: () => h(editForm, { ref: formRef }),
      beforeSure: (done, { options }) => {
        const FormRef = formRef.value.getRef();
        const curData = options.props.formInline as FormItemProps;
        function chores() {
          successNotification(
            `您${title}了角色名称为${curData.name}的这条数据`
          );
          done(); // 关闭弹框
          onSearch(); // 刷新表格数据
        }
        FormRef.validate(valid => {
          if (valid) {
            console.log("curData", curData);
            // 表单规则校验通过
            if (title === "新增") {
              delete curData.id;
              // 实际开发先调用新增接口，再进行下面操作
              addRole(curData).then(() => {
                chores();
              });
            } else {
              updateRole(curData).then(() => {
                // 实际开发先调用修改接口，再进行下面操作
                chores();
              });
            }
          }
        });
      }
    });
  }

  /** 菜单权限 */
  async function handleMenu(row?: any) {
    const { id } = row;
    if (id) {
      curRow.value = row;
      isShow.value = true;
      const { data } = await getRoleAuth(id);
      menuTreeRef.value.setCheckedKeys(data.menus);
      apiTreeRef.value.setCheckedKeys(data.apis);
    } else {
      curRow.value = null;
      isShow.value = false;
    }
  }

  /** 高亮当前权限选中行 */
  function rowStyle({ row: { id } }) {
    return {
      cursor: "pointer",
      background: id === curRow.value?.id ? "var(--el-fill-color-light)" : ""
    };
  }

  /** 菜单API权限-保存 */
  function handleSave() {
    const { id, name } = curRow.value;
    const apiIds = apiTreeRef.value
      .getCheckedKeys()
      .filter(item => typeof item === "number");
    let data = {
      id: id,
      menus: menuTreeRef.value.getCheckedKeys(),
      apis: apiIds
    };
    // 根据用户 id 调用实际项目中菜单权限修改接口
    updateRoleAuth(data).then(() => {
      successNotification(`角色名称为${name}的菜单权限修改成功`);
    });
  }

  /** 数据权限 可自行开发 */
  // function handleDatabase() {}

  const onQueryChanged = (query: string) => {
    menuTreeRef.value!.filter(query);
  };

  const filterMethod = (query: string, node) => {
    return transformI18n(node.title)!.includes(query);
  };

  onMounted(async () => {
    onSearch();
    const { data } = await getMenuList();
    menuTreeIds.value = getKeyList(data, "id");
    menuTreeData.value = handleTree(data);
    getApiList().then(res => {
      apiTreeData.value = buildApiTree(res.data);
      apiTreeIds.value = getKeyList(res.data, "id");
      apiParentTreeIds.value = getKeyList(apiTreeData.value, "id");
    });
  });

  watch(isExpandAll, val => {
    val
      ? menuTreeRef.value.setExpandedKeys(menuTreeIds.value)
      : menuTreeRef.value.setExpandedKeys([]);
  });

  watch(isSelectAll, val => {
    val
      ? menuTreeRef.value.setCheckedKeys(menuTreeIds.value)
      : menuTreeRef.value.setCheckedKeys([]);
  });

  watch(apiIsExpandAll, val => {
    val
      ? apiTreeRef.value.setExpandedKeys(apiParentTreeIds.value)
      : apiTreeRef.value.setExpandedKeys([]);
  });

  watch(apiIsSelectAll, val => {
    val
      ? apiTreeRef.value.setCheckedKeys([
          ...apiTreeIds.value,
          ...apiParentTreeIds.value
        ])
      : apiTreeRef.value.setCheckedKeys([]);
  });

  return {
    form,
    isShow,
    curRow,
    loading,
    columns,
    rowStyle,
    dataList,
    menuTreeData,
    apiTreeData,
    tabIndex,
    menuTreeProps,
    apiTreeProps,
    isLinkage,
    pagination,
    isExpandAll,
    apiIsExpandAll,
    isSelectAll,
    apiIsSelectAll,
    apiIsLinkage,
    tabOperation,
    treeSearchValue,
    // buttonClass,
    onSearch,
    resetForm,
    openDialog,
    handleMenu,
    handleSave,
    handleDelete,
    filterMethod,
    transformI18n,
    onQueryChanged,
    // handleDatabase,
    handleSizeChange,
    handleCurrentChange,
    handleSelectionChange
  };
}
