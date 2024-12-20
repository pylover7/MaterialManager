<script lang="ts" setup>
import { IconJson } from "@/components/ReIcon/data";
import { cloneDeep, isAllEmpty } from "@pureadmin/utils";
import { computed, CSSProperties, ref, watch } from "vue";

type ParameterCSSProperties = (item?: string) => CSSProperties | undefined;

defineOptions({
  name: "IconSelect"
});

const inputValue = defineModel({ type: String });

const iconList = ref(IconJson);
const icon = ref();
const currentActiveType = ref("ep:");
// 深拷贝图标数据，前端做搜索
const copyIconList = cloneDeep(iconList.value);
const totalPage = ref(0);
// 每页显示35个图标
const pageSize = ref(35);
const currentPage = ref(1);

// 搜索条件
const filterValue = ref("");

const tabsList = [
  {
    label: "Element Plus",
    name: "ep:"
  },
  {
    label: "Remix Icon",
    name: "ri:"
  },
  {
    label: "Font Awesome 5 Solid",
    name: "fa-solid:"
  },
  {
    label: "Fluent",
    name: "fluent:"
  }
];

const pageList = computed(() =>
  copyIconList[currentActiveType.value]
    .filter(i => i.includes(filterValue.value))
    .slice(
      (currentPage.value - 1) * pageSize.value,
      currentPage.value * pageSize.value
    )
);

const iconItemStyle = computed((): ParameterCSSProperties => {
  return item => {
    if (inputValue.value === currentActiveType.value + item) {
      return {
        borderColor: "var(--el-color-primary)",
        color: "var(--el-color-primary)"
      };
    }
  };
});

function setVal() {
  currentActiveType.value = inputValue.value.substring(
    0,
    inputValue.value.indexOf(":") + 1
  );
  icon.value = inputValue.value.substring(inputValue.value.indexOf(":") + 1);
}

function onBeforeEnter() {
  if (isAllEmpty(icon.value)) return;
  setVal();
  // 寻找当前图标在第几页
  const curIconIndex = copyIconList[currentActiveType.value].findIndex(
    i => i === icon.value
  );
  currentPage.value = Math.ceil((curIconIndex + 1) / pageSize.value);
}

function onAfterLeave() {
  filterValue.value = "";
}

function handleClick({ props }) {
  currentPage.value = 1;
  currentActiveType.value = props.name;
}

function onChangeIcon(item) {
  icon.value = item;
  inputValue.value = currentActiveType.value + item;
}

function onCurrentChange(page) {
  currentPage.value = page;
}

function onClear() {
  icon.value = "";
  inputValue.value = "";
}

watch(
  () => pageList.value,
  () =>
    (totalPage.value = copyIconList[currentActiveType.value].filter(i =>
      i.includes(filterValue.value)
    ).length),
  { immediate: true }
);
watch(
  () => inputValue.value,
  val => val && setVal(),
  { immediate: true }
);
watch(
  () => filterValue.value,
  () => (currentPage.value = 1)
);
</script>

<template>
  <div class="selector">
    <el-input v-model="inputValue">
      <template #append />
    </el-input>
  </div>
</template>

<style lang="scss" scoped>
.icon-item {
  &:hover {
    color: var(--el-color-primary);
    border-color: var(--el-color-primary);
    transition: all 0.4s;
    transform: scaleX(1.05);
  }
}

:deep(.el-tabs__nav-next) {
  font-size: 15px;
  line-height: 32px;
  box-shadow: -5px 0 5px -6px #ccc;
}

:deep(.el-tabs__nav-prev) {
  font-size: 15px;
  line-height: 32px;
  box-shadow: 5px 0 5px -6px #ccc;
}

:deep(.el-input-group__append) {
  padding: 0;
}

:deep(.el-tabs__item) {
  height: 30px;
  font-size: 12px;
  font-weight: normal;
  line-height: 30px;
}

:deep(.el-tabs__header),
:deep(.el-tabs__nav-wrap) {
  position: static;
  margin: 0;
  box-shadow: 0 2px 5px rgb(0 0 0 / 6%);
}

:deep(.el-tabs__nav-wrap::after) {
  height: 0;
}

:deep(.el-tabs__nav-wrap) {
  padding: 0 24px;
}

:deep(.el-tabs__content) {
  margin-top: 4px;
}
</style>
