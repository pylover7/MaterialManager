<script lang="ts" setup>
import { useRouter } from "vue-router";
import noExist from "@/assets/status/404.svg?component";

defineOptions({
  name: "404"
});

const router = useRouter();
</script>

<template>
  <div class="flex justify-center items-center h-[640px]">
    <noExist />
    <div class="ml-12">
      <p
        v-motion
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 80
          }
        }"
        :initial="{
          opacity: 0,
          y: 100
        }"
        class="font-medium text-4xl mb-4 dark:text-white"
      >
        404
      </p>
      <p
        v-motion
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 120
          }
        }"
        :initial="{
          opacity: 0,
          y: 100
        }"
        class="mb-4 text-gray-500"
      >
        抱歉，你访问的页面不存在
      </p>
      <el-button
        v-motion
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 160
          }
        }"
        :initial="{
          opacity: 0,
          y: 100
        }"
        type="primary"
        @click="router.push('/')"
      >
        返回首页
      </el-button>
    </div>
  </div>
</template>
