import Intro from "@pages/Intro.svelte";
import Notice from "@/pages/Notice.svelte";
import Project from "@/pages/Project.svelte";
import HallOfFame from "@/pages/Hall_of_fame.svelte";
import Mypage from "@/pages/Mypage.svelte";
import Write from "@/pages/Write.svelte";

import Job from "@/pages/Job.svelte";
import JobDetail from "@/pages/JobDetail.svelte";
import Budget from "@/pages/Budget.svelte";
import BudgetDetail from "@/pages/BudgetDetail.svelte";

import SignUp from "@/pages/SignUp.svelte";
import SignIn from "@/pages/SignIn.svelte";

import ProjectDetail from "@/pages/ProjectDetail.svelte";

export default {
    /**
     * Main Pages
     */
    "/": Intro,
    "/notice": Notice,
    "/project": Project,
    // Project Tab Pages
    "/job": Job,
    "/budget": Budget,
    "/hall_of_fame": HallOfFame,
    "/my_page": Mypage,

    /**
     * Utils
     */
    "/write": Write,
    "/sign-up": SignUp,
    "/sign-in": SignIn,

    /**
     * Sub Pages
     */
    "/project/*": ProjectDetail,
    "/job/*": JobDetail,
    "/budget/*": BudgetDetail,
};
