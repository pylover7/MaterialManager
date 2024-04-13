import type { VNode } from "vue";
import { isFunction } from "@pureadmin/utils";
import { ElNotification, type NotificationHandle } from "element-plus";

type notificationStyle = "el" | "antd";
type notificationTypes = "info" | "success" | "warning" | "error";
type notificationPosition =
  | "top-right"
  | "top-left"
  | "bottom-right"
  | "bottom-left";

interface NotificationParams {
  /** 消息类型，可选 `info` 、`success` 、`warning` 、`error` ，默认 `info` */
  type?: notificationTypes;
  /** 自定义图标，该属性会覆盖 `type` 的图标 */
  icon?: any;
  /** 是否将 `message` 属性作为 `HTML` 片段处理，默认 `false` */
  dangerouslyUseHTMLString?: boolean;
  /** 消息风格，可选 `el` 、`antd` ，默认 `antd` */
  customClass?: notificationStyle;
  /** 显示时间，单位为毫秒。设为 `0` 则不会自动关闭，`element-plus` 默认是 `3000` ，平台改成默认 `2000` */
  duration?: number;
  /** 自定义弹出位置，默认值 `top-right` */
  position?: notificationPosition;
  /** 是否显示关闭按钮，默认值 `false` */
  showClose?: boolean;
  /** 关闭时的回调函数, 参数为被关闭的 `message` 实例 */
  onClose?: Function | null;
  /** 相对屏幕顶部的偏移量 偏移的距离，在同一时刻，所有的 Notification 实例应当具有一个相同的偏移量，默认 `100` */
  offset?: number;
  /** 设置组件的根元素，默认 `document.body` */
  appendTo?: string | HTMLElement;
  /** 初始 zIndex，默认值 `0` */
  zIndex?: number;
}

/**
 * `Notification` 消息通知函数
 */
const notification = (
  title: string,
  message: string | VNode,
  params: NotificationParams
): NotificationHandle => {
  if (!params) {
    return ElNotification({
      title,
      message,
      customClass: "zg-notification"
    });
  } else {
    const {
      icon,
      type = "info",
      dangerouslyUseHTMLString = false,
      customClass = "antd",
      duration = 2000,
      position = "top-right",
      showClose = false,
      onClose,
      offset = 100,
      appendTo = document.body,
      zIndex = 0
    } = params;
    return ElNotification({
      title,
      message,
      type,
      icon,
      dangerouslyUseHTMLString,
      duration,
      position,
      showClose,
      offset,
      appendTo,
      zIndex,
      customClass: customClass === "antd" ? "zg-message" : "",
      onClose: () => (isFunction(onClose) ? onClose() : null)
    });
  }
};

/**
 * 信息通知
 */
const infoNotification = (message: string | VNode): NotificationHandle => {
  return notification("信息通知", message, {
    type: "info"
  });
};

/**
 * 成功通知
 */
const successNotification = (message: string | VNode): NotificationHandle => {
  return notification("成功通知", message, {
    type: "success"
  });
};

/**
 * 警告通知
 */
const warningNotification = (message: string | VNode): NotificationHandle => {
  return notification("警告通知", message, {
    type: "warning"
  });
};

/**
 * 错误通知
 */
const errorNotification = (message: string | VNode): NotificationHandle => {
  return notification("错误通知", message, {
    type: "error"
  });
};

/**
 * 关闭所有 `Notification` 消息提示函数
 */
const closeAllNotification = (): void => ElNotification.closeAll();

export {
  notification,
  infoNotification,
  successNotification,
  warningNotification,
  errorNotification,
  closeAllNotification
};
