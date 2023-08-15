import MainPage_Intro from "@pages/MainPage_Intro.svelte";
import MainPage_Contents from "@/pages/MainPage_Contents.svelte";
import MainPage_HallOfFame from "@/pages/MainPage_Hall_of_fame.svelte";

import SubPage_Write from "@/pages/SubPage_Write.svelte";
import SubPage_Content from "@/pages/SubPage_Content.svelte";
import SubPage_SignUp from "@/pages/SubPage_SignUp.svelte";
import SubPage_SignIn from "@/pages/SubPage_SignIn.svelte";

import ErrorPage_404 from "@/pages/ErrorPage_404.svelte";

export default {
    /**
     * Main Pages
     */
    "/": MainPage_Intro,

    /**
     * Sub Pages
     */
    "/contents/content/:content_id": SubPage_Content,
    "/contents/:contents_id": MainPage_Contents,

    "/hall_of_fame": MainPage_HallOfFame,

    /**
     * Utils
     */
    "/write": SubPage_Write,
    "/sign-up": SubPage_SignUp,
    "/sign-in": SubPage_SignIn,

    /**
     * 404
     */
    "/*": ErrorPage_404,
};
