// 这里存放本地图标，在 src/layout/index.vue 文件中加载，避免在首启动加载
import { addIcon } from "@iconify/vue/dist/offline";

// 本地菜单图标，后端在路由的 icon 中返回对应的图标字符串并且前端在此处使用 addIcon 添加即可渲染菜单图标
// @iconify-icons/ep
import Lollipop from "@iconify-icons/ep/lollipop";
import HomeFilled from "@iconify-icons/ep/home-filled";
addIcon("lollipop", Lollipop);
addIcon("Home", HomeFilled);
// @iconify-icons/ri
import Search from "@iconify-icons/ri/search-line";
import InformationLine from "@iconify-icons/ri/information-line";
addIcon("searchLine", Search);
addIcon("informationLine", InformationLine);
// @iconify-icons/fluent
import Desktop from "@iconify-icons/fluent/desktop-flow-24-regular";
import BoxSearch from "@iconify-icons/fluent/box-search-16-regular";
import KeyReset from "@iconify-icons/fluent/key-reset-24-regular";
import BrainCircuit from "@iconify-icons/fluent/brain-circuit-24-regular";
import ShieldPerson from "@iconify-icons/fluent/shield-person-20-regular";
import PersonEdit from "@iconify-icons/fluent/person-edit-48-regular";
import HomeMore from "@iconify-icons/fluent/home-more-32-regular";
import NotepadPerson from "@iconify-icons/fluent/notepad-person-24-regular";
import PersonSync from "@iconify-icons/fluent/person-sync-48-regular";
import PeopleTeam from "@iconify-icons/fluent/people-team-20-regular";
import PeopleCommunity from "@iconify-icons/fluent/people-community-20-regular";
import Clover from "@iconify-icons/fluent/clover-48-regular";
import TextBulletListSquareSearch from "@iconify-icons/fluent/text-bullet-list-square-search-20-regular";
import Settings from "@iconify-icons/fluent/settings-48-regular";
import DesktopKeyboard from "@iconify-icons/fluent/desktop-keyboard-24-regular";
import BoxMultipleArrowRight from "@iconify-icons/fluent/box-multiple-arrow-right-24-regular";
import PersonBoard from "@iconify-icons/fluent/person-board-32-regular";
import PersonVoice from "@iconify-icons/fluent/person-voice-24-regular";

addIcon("Desktop", Desktop);
addIcon("BoxSearch", BoxSearch);
addIcon("KeyReset", KeyReset);
addIcon("BrainCircuit", BrainCircuit);
addIcon("ShieldPerson", ShieldPerson);
addIcon("PersonEdit", PersonEdit);
addIcon("HomeMore", HomeMore);
addIcon("NotepadPerson", NotepadPerson);
addIcon("PersonSync", PersonSync);
addIcon("PeopleTeam", PeopleTeam);
addIcon("PeopleCommunity", PeopleCommunity);
addIcon("Clover", Clover);
addIcon("TextBulletListSquareSearch", TextBulletListSquareSearch);
addIcon("Settings", Settings);
addIcon("DesktopKeyboard", DesktopKeyboard);
addIcon("BoxMultipleArrowRight", BoxMultipleArrowRight);
addIcon("PersonBoard", PersonBoard);
addIcon("PersonVoice", PersonVoice);
