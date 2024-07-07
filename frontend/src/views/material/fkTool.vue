<script setup lang="ts">
import { computed } from "vue";
import { useMetaInfoStoreHook } from "@/store/modules/metaInfo";
import Tool from "./page/tool.vue";

defineOptions({
  name: "FkTool"
});
const area = computed(() => useMetaInfoStoreHook().area.fk);
const metaType = computed(() => useMetaInfoStoreHook().metaType.tool);
</script>

<template>
  <div>
    <Tool :area="area" :metaType="metaType" />
  </div>
</template>

<style scoped lang="scss"></style>
