<script lang="ts" setup>
import { computed } from "vue";
import { useMetaInfoStoreHook } from "@/store/modules/metaInfo";
import Key from "./page/key.vue";

defineOptions({
  name: "FkKey"
});
const area = computed(() => useMetaInfoStoreHook().area.fk);
const metaType = computed(() => useMetaInfoStoreHook().metaType.key);
</script>

<template>
  <div>
    <Key :area="area" :metaType="metaType" />
  </div>
</template>
