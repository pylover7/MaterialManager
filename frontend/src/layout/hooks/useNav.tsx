import { storeToRefs } from "pinia";
import { getConfig } from "@/config";
import { useRouter } from "vue-router";
import { emitter } from "@/utils/mitt";
import userAvatar from "@/assets/user.jpg";
import { getTopMenu } from "@/router/utils";
import { useFullscreen } from "@vueuse/core";
import { deviceDetection, isAllEmpty, useGlobal } from "@pureadmin/utils";
import type { routeMetaType } from "../types";
import { transformI18n } from "@/plugins/i18n";
import { router, remainingPaths } from "@/router";
import { computed, type CSSProperties, reactive, ref, watch } from "vue";
import { useAppStoreHook } from "@/store/modules/app";
import { useUserStoreHook } from "@/store/modules/user";
import { useEpThemeStoreHook } from "@/store/modules/epTheme";
import { usePermissionStoreHook } from "@/store/modules/permission";
import ExitFullscreen from "@iconify-icons/ri/fullscreen-exit-fill";
import Fullscreen from "@iconify-icons/ri/fullscreen-fill";
import { addDialog } from "@/components/ReDialog/index";
import { ElForm, ElFormItem, ElInput, ElProgress } from "element-plus";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Refresh from "@iconify-icons/ep/refresh";
import { errorNotification, successNotification } from "@/utils/notification";
import { zxcvbn } from "@zxcvbn-ts/core";
import { generatePassword } from "@/views/superAdmin/UserManagement/utils/util";
import { updatePassword } from "@/api/base";
import { REGEXP_PWD } from "@/views/login/utils/rule";

const errorInfo = "当前路由配置不正确，请检查配置";

export function useNav() {
  const pureApp = useAppStoreHook();
  const routers = useRouter().options.routes;
  const { isFullscreen, toggle } = useFullscreen();
  const { wholeMenus } = storeToRefs(usePermissionStoreHook());
  /** 平台`layout`中所有`el-tooltip`的`effect`配置，默认`light` */
  const tooltipEffect = getConfig()?.TooltipEffect ?? "light";

  const getDivStyle = computed((): CSSProperties => {
    return {
      width: "100%",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      overflow: "hidden"
    };
  });

  /** 用户名 */
  const username = computed(() => {
    return useUserStoreHook()?.username;
  });
  const nickname = computed(() => {
    return useUserStoreHook()?.nickname;
  });

  /** 设置国际化选中后的样式 */
  const getDropdownItemStyle = computed(() => {
    return (locale, t) => {
      return {
        background: locale === t ? useEpThemeStoreHook().epThemeColor : "",
        color: locale === t ? "#f4f4f5" : "#000"
      };
    };
  });

  const getDropdownItemClass = computed(() => {
    return (locale, t) => {
      return locale === t ? "" : "dark:hover:!text-primary";
    };
  });

  const avatarsStyle = computed(() => {
    return username.value ? { marginRight: "10px" } : "";
  });

  const isCollapse = computed(() => {
    return !pureApp.getSidebarStatus;
  });

  const device = computed(() => {
    return pureApp.getDevice;
  });

  const { $storage, $config } = useGlobal<GlobalPropertiesApi>();
  const layout = computed(() => {
    return $storage?.layout?.layout;
  });

  const title = computed(() => {
    return $config.Title;
  });

  /** 动态title */
  function changeTitle(meta: routeMetaType) {
    const Title = getConfig().Title;
    if (Title) document.title = `${transformI18n(meta.title)} | ${Title}`;
    else document.title = transformI18n(meta.title);
  }

  /** 退出登录 */
  function logout() {
    useUserStoreHook().logOut();
  }

  function backTopMenu() {
    router.push(getTopMenu()?.path);
  }

  function onPanel() {
    emitter.emit("openPanel");
  }

  function toggleSideBar() {
    pureApp.toggleSideBar();
  }

  function handleResize(menuRef) {
    menuRef?.handleResize();
  }

  function resolvePath(route) {
    if (!route.children) return console.error(errorInfo);
    const httpReg = /^http(s?):\/\//;
    const routeChildPath = route.children[0]?.path;
    if (httpReg.test(routeChildPath)) {
      return route.path + "/" + routeChildPath;
    } else {
      return routeChildPath;
    }
  }

  function menuSelect(indexPath: string) {
    if (wholeMenus.value.length === 0 || isRemaining(indexPath)) return;
    emitter.emit("changLayoutRoute", indexPath);
  }

  /** 判断路径是否参与菜单 */
  function isRemaining(path: string) {
    return remainingPaths.includes(path);
  }

  /** 获取`logo` */
  function getLogo() {
    return new URL("/logo.svg", import.meta.url).href;
  }

  /** 打开修改密码对话框 */
  function updatePwdDialog() {
    const ruleFormRef = ref();
    // 重置的新密码
    const pwdForm = reactive({
      oldPwd: "",
      newPwd: "",
      renewPwd: ""
    });
    const newPwdLoading = ref(false);
    const pwdProgress = [
      { color: "#e74242", text: "非常弱" },
      { color: "#EFBD47", text: "弱" },
      { color: "#ffa500", text: "一般" },
      { color: "#1bbf1b", text: "强" },
      { color: "#008000", text: "非常强" }
    ];
    const curScore = ref();
    watch(
      pwdForm,
      ({ newPwd }) =>
        (curScore.value = isAllEmpty(newPwd) ? -1 : zxcvbn(newPwd).score)
    );
    const resetPwd = () => {
      newPwdLoading.value = true;
      setTimeout(() => {
        pwdForm.newPwd = generatePassword(12);
        newPwdLoading.value = false;
      }, 1000);
    };
    addDialog({
      title: `修改密码`,
      width: "30%",
      draggable: true,
      closeOnClickModal: false,
      fullscreen: deviceDetection(),
      contentRenderer: () => (
        <>
          <ElForm ref={ruleFormRef} model={pwdForm}>
            <ElFormItem
              prop="oldPwd"
              rules={[
                {
                  required: true,
                  message: "请输入旧密码",
                  trigger: "change"
                }
              ]}
            >
              <ElInput
                clearable
                show-password
                type="password"
                v-model={pwdForm.oldPwd}
                placeholder="请输入旧密码"
              ></ElInput>
            </ElFormItem>
            <ElFormItem
              prop="newPwd"
              rules={[
                {
                  required: true,
                  message: "请输入新密码",
                  trigger: "change"
                },
                {
                  validator: (rule, value, callback) => {
                    if (!REGEXP_PWD.test(value)) {
                      callback(
                        new Error(
                          "密码格式应为8-18位数字、字母、符号的任意两种组合"
                        )
                      );
                    } else if (pwdForm.newPwd === pwdForm.oldPwd) {
                      callback(new Error("新密码不能与旧密码相同"));
                    } else {
                      callback();
                    }
                  },
                  trigger: "blur"
                }
              ]}
            >
              <ElInput
                clearable
                show-password
                type="password"
                v-model={pwdForm.newPwd}
                placeholder="请输入新密码"
              >
                {{
                  append: () => (
                    <el-button
                      icon={useRenderIcon(Refresh)}
                      loading-icon={useRenderIcon(Refresh)}
                      loading={newPwdLoading.value}
                      onClick={() => {
                        resetPwd();
                      }}
                    >
                      随机密码
                    </el-button>
                  )
                }}
              </ElInput>
            </ElFormItem>
            <ElFormItem
              prop="renewPwd"
              rules={[
                {
                  required: true,
                  message: "请再次输入新密码",
                  trigger: "change"
                },
                {
                  validator: (rule, value, callback) => {
                    if (value !== pwdForm.newPwd) {
                      callback(new Error("两次输入的密码不一致"));
                    } else {
                      callback();
                    }
                  },
                  trigger: "confirm"
                }
              ]}
            >
              <ElInput
                clearable
                show-password
                type="password"
                v-model={pwdForm.renewPwd}
                placeholder="请再次输入新密码"
              ></ElInput>
            </ElFormItem>
          </ElForm>
          <div class="mt-4 flex">
            {pwdProgress.map(({ color, text }, idx) => (
              <div
                class="w-[19vw]"
                style={{ marginLeft: idx !== 0 ? "4px" : 0 }}
              >
                <ElProgress
                  striped
                  striped-flow
                  duration={curScore.value === idx ? 6 : 0}
                  percentage={curScore.value >= idx ? 100 : 0}
                  color={color}
                  stroke-width={10}
                  show-text={false}
                />
                <p
                  class="text-center"
                  style={{ color: curScore.value === idx ? color : "" }}
                >
                  {text}
                </p>
              </div>
            ))}
          </div>
        </>
      ),
      closeCallBack: () => {
        pwdForm.newPwd = "";
        pwdForm.oldPwd = "";
        pwdForm.renewPwd = "";
      },
      beforeSure: done => {
        ruleFormRef.value.validate(valid => {
          if (valid) {
            const data = {
              oldPwd: pwdForm.oldPwd,
              newPwd: pwdForm.newPwd
            };
            // 表单规则校验通过
            updatePassword(data)
              .then(res => {
                // 根据实际业务使用pwdForm.newPwd和row里的某些字段去调用重置用户密码接口即可
                done(); // 关闭弹框
                successNotification(res.msg);
              })
              .catch(err => {
                errorNotification(err.msg);
              });
          }
        });
      }
    });
  }

  return {
    title,
    device,
    layout,
    logout,
    routers,
    $storage,
    isFullscreen,
    Fullscreen,
    ExitFullscreen,
    toggle,
    backTopMenu,
    onPanel,
    getDivStyle,
    changeTitle,
    toggleSideBar,
    menuSelect,
    handleResize,
    resolvePath,
    getLogo,
    isCollapse,
    pureApp,
    username,
    nickname,
    userAvatar,
    avatarsStyle,
    tooltipEffect,
    getDropdownItemStyle,
    getDropdownItemClass,
    updatePwdDialog
  };
}
