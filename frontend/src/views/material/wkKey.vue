<script lang="ts" setup>
import { computed } from "vue";
import { useMetaInfoStoreHook } from "@/store/modules/metaInfo";
import Key from "./page/key.vue";

defineOptions({
  name: "WkKey"
});
const area = computed(() => useMetaInfoStoreHook().area.wk);
const metaType = computed(() => useMetaInfoStoreHook().metaType.key);
</script>

<template>
  <div>
    <Key :area="area" :metaType="metaType" />
  </div>
</template>
