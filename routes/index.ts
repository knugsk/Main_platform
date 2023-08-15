import MainPage_Intro from "@pages/MainPage_Intro.svelte";
import MainPage_Notice from "@/pages/MainPage_Notice.svelte";
import MainPage_HallOfFame from "@/pages/MainPage_Hall_of_fame.svelte";

import MainPage_Project from "@/pages/MainPage_Project.svelte";
import MainPage_Job from "@/pages/MainPage_Job.svelte";
import MainPage_Budget from "@/pages/MainPage_Budget.svelte";

import SubPage_Write from "@/pages/SubPage_Write.svelte";
import SubPage_Content from "@/pages/SubPage_Content.svelte";
import SubPage_SignUp from "@/pages/SubPage_SignUp.svelte";
import SubPage_SignIn from "@/pages/SubPage_SignIn.svelte";

export default {
    /**
     * Main Pages
     */
    "/": MainPage_Intro,
    "/notice": MainPage_Notice,
    "/project": MainPage_Project,
    // Project Tab Pages
    "/job": MainPage_Job,
    "/budget": MainPage_Budget,

    "/hall_of_fame": MainPage_HallOfFame,

    /**
     * Utils
     */
    "/write": SubPage_Write,
    "/sign-up": SubPage_SignUp,
    "/sign-in": SubPage_SignIn,

    /**
     * Sub Pages
     */
    "/content/*": SubPage_Content,
    "/job/*": SubPage_Content,
    "/budget/*": SubPage_Content,
};
