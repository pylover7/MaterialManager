<script lang="ts" setup>
import { computed } from "vue";
import { useMetaInfoStoreHook } from "@/store/modules/metaInfo";
import Tool from "./page/tool.vue";

defineOptions({
  name: "WkTool"
});
const area = computed(() => useMetaInfoStoreHook().area.wk);
const metaType = computed(() => useMetaInfoStoreHook().metaType.tool);
</script>

<template>
  <div>
    <Tool :area="area" :metaType="metaType" />
  </div>
</template>
