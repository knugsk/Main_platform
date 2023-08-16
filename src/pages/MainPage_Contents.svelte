<script lang="ts">
    import "./MainPage_Contents.scss";

    import SubNav_ProjectNav from "@/components/SubNav_ProjectNav.svelte";
    
    import { beforeUpdate } from "svelte";
    import { get_contents } from "query";
    import koreantime from "@/lib/datetime";

    export let params: { contents_id: string } = { contents_id: "" }

    let data: any = null;
    let title: string = "error";
    let page: number = 1;
    let max_page: number = 1;

    const get_data = async () => {
        let id = 1;

        switch (params.contents_id) {
            case "notice":
                id = 1;
                title = "공지사항";
                break;
            case "project":
                id = 2;
                title = "프로젝트";
                break;
            case "job":
                id = 4;
                title = "구인/구직";
                break;
            case "budget":
                id = 3;
                title = "예산 신청";
                break;
            default:
                break;
        }

        get_contents(id)
            .then(res => {
                if(data !== null || data !== undefined) data = res;
            }).catch(err => {
                console.log(err);
            });
    }
    
    beforeUpdate(() => {
        data = null;
        get_data();
    });
</script>

<div class="container_contents">
    {#if params.contents_id !== "notice"}
        <SubNav_ProjectNav />
    {/if}
    <h1 class="title_contents">{title}</h1>
    <div class="container_bar">
        {#if data !== null && data !== undefined}
            {#each data as content, index }
                <button class="bar_content">
                    <p class="text_bar">{content.title}</p>
                    <p class="text_bar">{koreantime(content.published_date)}</p>
                    <p class="text_bar">{`작성자: ${content.author}`}</p>
                </button>
            {/each}
        {/if}
        <div class="pagination">

        </div>
    </div>
</div>

