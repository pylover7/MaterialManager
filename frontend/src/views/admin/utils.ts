/** 日期、时间选择器快捷选项，常搭配 [DatePicker](https://element-plus.org/zh-CN/component/date-picker.html) 和 [DateTimePicker](https://element-plus.org/zh-CN/component/datetime-picker.html) 的`shortcuts`属性使用 */
export const getPickerShortcuts = (): Array<{
  text: string;
  value: Date | Function;
}> => {
  return [
    {
      text: "今天",
      value: () => {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const todayEnd = new Date();
        todayEnd.setHours(23, 59, 59, 999);
        return [today, todayEnd];
      }
    },
    {
      text: "昨天",
      value: () => {
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        yesterday.setHours(0, 0, 0, 0);
        const yesterdayEnd = new Date();
        yesterdayEnd.setDate(yesterdayEnd.getDate() - 1);
        yesterdayEnd.setHours(23, 59, 59, 999);
        return [yesterday, yesterdayEnd];
      }
    },
    {
      text: "前天",
      value: () => {
        const beforeYesterday = new Date();
        beforeYesterday.setDate(beforeYesterday.getDate() - 2);
        beforeYesterday.setHours(0, 0, 0, 0);
        const beforeYesterdayEnd = new Date();
        beforeYesterdayEnd.setDate(beforeYesterdayEnd.getDate() - 2);
        beforeYesterdayEnd.setHours(23, 59, 59, 999);
        return [beforeYesterday, beforeYesterdayEnd];
      }
    },
    {
      text: "本周",
      value: () => {
        const today = new Date();
        const startOfWeek = new Date(
          today.getFullYear(),
          today.getMonth(),
          today.getDate() - today.getDay() + (today.getDay() === 0 ? -6 : 1)
        );
        startOfWeek.setHours(0, 0, 0, 0);
        const endOfWeek = new Date(
          startOfWeek.getTime() +
            6 * 24 * 60 * 60 * 1000 +
            23 * 60 * 60 * 1000 +
            59 * 60 * 1000 +
            59 * 1000 +
            999
        );
        return [startOfWeek, endOfWeek];
      }
    },
    {
      text: "上周",
      value: () => {
        const today = new Date();
        const startOfLastWeek = new Date(
          today.getFullYear(),
          today.getMonth(),
          today.getDate() - today.getDay() - 7 + (today.getDay() === 0 ? -6 : 1)
        );
        startOfLastWeek.setHours(0, 0, 0, 0);
        const endOfLastWeek = new Date(
          startOfLastWeek.getTime() +
            6 * 24 * 60 * 60 * 1000 +
            23 * 60 * 60 * 1000 +
            59 * 60 * 1000 +
            59 * 1000 +
            999
        );
        return [startOfLastWeek, endOfLastWeek];
      }
    },
    {
      text: "本月",
      value: () => {
        const today = new Date();
        const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
        startOfMonth.setHours(0, 0, 0, 0);
        const endOfMonth = new Date(
          today.getFullYear(),
          today.getMonth() + 1,
          0
        );
        endOfMonth.setHours(23, 59, 59, 999);
        return [startOfMonth, endOfMonth];
      }
    },
    {
      text: "上个月",
      value: () => {
        const today = new Date();
        const startOfLastMonth = new Date(
          today.getFullYear(),
          today.getMonth() - 1,
          1
        );
        startOfLastMonth.setHours(0, 0, 0, 0);
        const endOfLastMonth = new Date(
          today.getFullYear(),
          today.getMonth(),
          0
        );
        endOfLastMonth.setHours(23, 59, 59, 999);
        return [startOfLastMonth, endOfLastMonth];
      }
    },
    {
      text: "本年",
      value: () => {
        const today = new Date();
        const startOfYear = new Date(today.getFullYear(), 0, 1);
        startOfYear.setHours(0, 0, 0, 0);
        const endOfYear = new Date(today.getFullYear(), 11, 31);
        endOfYear.setHours(23, 59, 59, 999);
        return [startOfYear, endOfYear];
      }
    }
  ];
};

// 抽离可公用的工具函数等用于系统管理页面逻辑
import { computed } from "vue";
import { useDark } from "@pureadmin/utils";

export function usePublicHooks() {
  const { isDark } = useDark();

  const switchStyle = computed(() => {
    return {
      "--el-switch-on-color": "#6abe39",
      "--el-switch-off-color": "#e84749"
    };
  });

  const tagStyle = computed(() => {
    return (status: number) => {
      return status === 1
        ? {
            "--el-tag-text-color": isDark.value ? "#6abe39" : "#389e0d",
            "--el-tag-bg-color": isDark.value ? "#172412" : "#f6ffed",
            "--el-tag-border-color": isDark.value ? "#274a17" : "#b7eb8f"
          }
        : {
            "--el-tag-text-color": isDark.value ? "#e84749" : "#cf1322",
            "--el-tag-bg-color": isDark.value ? "#2b1316" : "#fff1f0",
            "--el-tag-border-color": isDark.value ? "#58191c" : "#ffa39e"
          };
    };
  });

  return {
    /** 当前网页是否为`dark`模式 */
    isDark,
    /** 表现更鲜明的`el-switch`组件  */
    switchStyle,
    /** 表现更鲜明的`el-tag`组件  */
    tagStyle
  };
}
