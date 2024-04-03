<script setup lang="ts">
import { $t } from "@/plugins/i18n";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import FluentNumberCircle116Regular from "@iconify-icons/fluent/number-circle-1-16-regular";

defineOptions({
  name: "GlbMaterial"
});
</script>

<template>
  <div>
    <el-card shadow="never">
      <p>test</p>
    </el-card>
    <el-card shadow="never">
      <div class="flex">
        <el-timeline>
          <el-timeline-item
            size="large"
            :icon="
              useRenderIcon(FluentNumberCircle116Regular, { color: '#0bbd87' })
            "
            key="1"
          >
            {{ $t("glb.title") }}
          </el-timeline-item>
          <el-timeline-item
            size="large"
            :icon="
              useRenderIcon(FluentNumberCircle116Regular, { color: '#0bbd87' })
            "
            key="2"
          >
            <p>你好</p>
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-card>
  </div>
</template>

<style scoped></style>
