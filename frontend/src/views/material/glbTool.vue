<script lang="ts" setup>
import { computed } from "vue";
import { useMetaInfoStoreHook } from "@/store/modules/metaInfo";
import Tool from "./page/tool.vue";

defineOptions({
  name: "GlbTool"
});
const area = computed(() => useMetaInfoStoreHook().area.glb);
const metaType = computed(() => useMetaInfoStoreHook().metaType.tool);
</script>

<template>
  <div>
    <Tool :area="area" :metaType="metaType" />
  </div>
</template>
