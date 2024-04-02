<script setup lang="ts">
import { $t } from "@/plugins/i18n";
import FluentNumberCircle116Regular from "@iconify-icons/fluent/number-circle-1-16-regular";

defineOptions({
  name: "GlbMaterial"
});
</script>

<template>
  <el-card shadow="never">
    <div class="flex">
      <el-timeline>
        <el-timeline-item size="large" :icon="FluentNumberCircle116Regular">
          {{ $t("glb.title") }}
        </el-timeline-item>
        <el-timeline-item size="large" :icon="FluentNumberCircle116Regular">
          <p>你好</p>
        </el-timeline-item>
      </el-timeline>
    </div>
  </el-card>
</template>

<style scoped></style>
