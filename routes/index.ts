import Intro from "@pages/Intro.svelte";
import Notice from "@/pages/Notice.svelte";
import Project from "@/pages/Project.svelte";
import HallOfFame from "@/pages/Hall_of_fame.svelte";
import Mypage from "@/pages/Mypage.svelte";
import Write from "@/pages/Write.svelte";

export default {
    "/": Intro,
    "/notice": Notice,
    "/project": Project,
    "/hall_of_fame": HallOfFame,
    "/my_page": Mypage,

    // Utils
    "/write": Write,
};
